#!/usr/local/bin/python

from collections import defaultdict
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.tokenize.mwe import MWETokenizer
import numpy as np
import arrow
import json
import sys

from phrases import isPhrase, PhrasesExtractor
from words import WordsCounter, GetSentsByWords
from .. utils import ConfigSectionMap


class Text:
	'''
	Text

	This is a class for processing the raw text information, 
	extracting useful features and also providing user-friendly data API.
	'''
	WORD_MIN_LEN = 2

	def __init__(self, text):
		print >> sys.stderr, '[TEXT]\t%s\t*** Initializing Text Object ***' % arrow.now()
		# Read Configuration from ini file
		phrases_extractor_path = ConfigSectionMap('Model')['n_gram']
		word2vec_model_path    = ConfigSectionMap('Model')['word2vec']
		words_category_path    = ConfigSectionMap('Corpus')['key_words']

		# Variable initialization
		# - raw text
		self.text               = text
		# - key words and their related words
		self.words_category     = None
		with open(words_category_path, 'rb') as f:
			self.words_category = json.load(f)
		# - all of the related words in the words_category
		print >> sys.stderr, '[TEXT]\t%s\tLoading n-Gram model ...' % arrow.now()
		self.interested_phrases = list(set([
			item
			for sublist in self.words_category.values() # Get sublist
			for item in sublist                         # Merge sublist
			if isPhrase(item)                           # Filter non phrases
		]))
		# - word2vec model
		print >> sys.stderr, '[TEXT]\t%s\tLoading word2vec model ...' % arrow.now()
		self.word2vec_model     = Word2Vec.load_word2vec_format(word2vec_model_path, binary=True)
		# - phrases extractor (n-gram kernel)
		self.phrases_extractor  = PhrasesExtractor(
			phrases_extractor_path, 
			self.word2vec_model, 
			interested_phrases=self.interested_phrases
		)
		
		# Tokenize the raw text
		print >> sys.stderr, '[TEXT]\t%s\tTokenizing ...' % arrow.now()
		self._tokenize()
		# Get the structure of the tokenized text
		print >> sys.stderr, '[TEXT]\t%s\tGetting Structure ...' % arrow.now()
		self._get_structure()
		# Anchor the locations of keywords in the text
		print >> sys.stderr, '[TEXT]\t%s\tAnchorring Keywords ...' % arrow.now()
		self._anchor_keywords()
		# Find K-nearest tokens from the text to the tokens in the words_category
		print >> sys.stderr, '[TEXT]\t%s\tFinding K nearest tokens ...' % arrow.now()
		self._find_k_nearest_tokens()

	def _tokenize(self):
		self.sents_by_tokens = []
		self.sents_by_words  = GetSentsByWords(self.text)
		self.mwe             = MWETokenizer()
		# Take interested phrases from the text into consideration
		self.phrases_count    = self.phrases_extractor.phrases_count(self.text) # Get all possible phrases from the text
		self.filtered_phrases = self._phrases_filter(self.phrases_count.keys())
		for p in self.filtered_phrases.keys():
			self.mwe.add_mwe(str(p).split('_'))
		for sent in self.sents_by_words:
			# Text by tokens
			sent_by_tokens = [
				token
				for token in self.mwe.tokenize(sent)
			]
			self.sents_by_tokens.append(sent_by_tokens)

	def _get_structure(self):
		self.structure = defaultdict(lambda: {
			# The list of indexs of the token in the whole text
			'text_indexs': [],
			# The list of indexs of the sentences in the whole text
			'sent_indexs': [],
			# The list of indexs of the token in their sentences
			'inner_indexs': []
		})
		text_i  = 0
		sent_i  = 0
		inner_i = 0
		for sent in self.sents_by_words:
			# Tokens structure info
			for token in self.mwe.tokenize(sent):
				if token not in stopwords.words('english') and len(token) > self.WORD_MIN_LEN:
					self.structure[token]['text_indexs'].append(text_i)
					self.structure[token]['sent_indexs'].append(sent_i)
					self.structure[token]['inner_indexs'].append(inner_i)
				text_i  += 1
				inner_i += 1
			sent_i += 1
			inner_i = 0

	def _anchor_keywords(self):
		self.anchors = {}
		for categories in self.words_category.keys():
			category_list = categories.strip().split('/')
			similar_tokens_info = defaultdict(lambda: 0)
			for category in category_list:
				for token in self.structure.keys():
					sim = self._phrases_similarity(category, token)
					if sim > 0.5 and sim > similar_tokens_info[token]:
						similar_tokens_info[token] = sim
			self.anchors[categories] = similar_tokens_info
		return self.anchors

	def _find_k_nearest_tokens(self, k=5):
		self.k_nearest_tokens = {}
		for category in self.words_category.keys():
			self.k_nearest_tokens[category] = []
		# Calculate the distance between every word/phrase in the text and category
		for category, words_in_category in self.words_category.iteritems():
			tokens_in_text     = self.structure.keys()
			tokens_in_category = map(lambda x: x.encode('ascii', 'ignore'), words_in_category)
			# Calculate the matrix of distances between 
			# words_in_text & words_in_category
			len_i_t  = len(tokens_in_text)
			len_i_c  = len(tokens_in_category)
			dist_mat = np.zeros((len_i_t, len_i_c))
			for i in range(len_i_t):
				for j in range(len_i_c):
					if isPhrase(tokens_in_text[i]) and isPhrase(tokens_in_category[j]):
						dist_mat[i, j] = self._phrases_similarity(tokens_in_text[i], tokens_in_category[j])
						# print >> sys.stderr, 'Phrase [%s] and phrase [%s] similarity is: %f' % \
						# 	(tokens_in_text[i], tokens_in_category[j], dist_mat[i, j])
					elif (not isPhrase(tokens_in_text[i])) and (not isPhrase(tokens_in_category[j])):
						dist_mat[i, j] = self._words_similarity(tokens_in_text[i], tokens_in_category[j])
					else:
						dist_mat[i, j] = 0
			# Find the best matched words in the category for each of words in text
			best_matched_indexs = dist_mat.argmax(axis=1) # The index of the best matched words
			best_matched_dists  = []                      # The distance between the best matched words and the words in text
			for i in range(len(best_matched_indexs)):
				best_matched_dists.append(dist_mat[i, best_matched_indexs[i]])
			best_matched_dists = np.array(best_matched_dists)
			# Find K-nearest words (to the current category) in the text 
			K = 15
			for k in range(K):
				i = best_matched_dists.argmax() # The index of the words in text which has the highest similarity
				j = best_matched_indexs[i]
				# If the current best matched distance is lower than o, then abandon it.
				if best_matched_dists[i] <= 0:
					break
				best_matched_dists[i] = -1      # Remove the largest value in the best_matched_dists
				self.k_nearest_tokens[category].append({
					'in_text':     tokens_in_text[i],
					'in_category': tokens_in_category[j],
					'count':       len(self.structure[tokens_in_text[i]]['text_indexs']),
					'distance':    dist_mat[i, j]
				})

	def _generate_text_feature(self):
		for 
		

	def _phrases_filter(self, phrases):
		filtered_phrases = {}
		for p in phrases:
			sims = [ self._phrases_similarity(p, p_i) for p_i in self.interested_phrases ]
			# sims = zip(*sim_phrase_list)[0]
			# Remove irrelevant phrases according to the interested phrases list
			if max(sims) > 0.8:
				filtered_phrases[p] = {}
				filtered_phrases[p]['similar_phrase'] = self.interested_phrases[np.argmax(sims)]
				filtered_phrases[p]['similarity'] = max(sims)
		return filtered_phrases

	def _words_similarity(self, word_A, word_B):
		try:
			similarity = self.word2vec_model.similarity(word_A, word_B)
		except KeyError, m:
			# TODO
			if word_A == word_B:
				similarity = 1
			else:
				similarity = 0
		return similarity

	def _phrases_similarity(self, phrase_A, phrase_B):
		words_A = phrase_A.split('_')
		words_B = phrase_B.split('_')
		similarity = 0
		if len(words_A) == len(words_B):
			for i in range(len(words_A)):
				similarity += self._words_similarity(words_A[i], words_B[i])
			similarity /= len(words_A)
		elif len(words_A) != len(words_B):
			sim_mat = np.zeros((len(words_A), len(words_B)))
			# for i in range(len(words_A)):
			# 	for j in range(len(words_B)):
			# 		sim_mat[i][j] = word2vec_model.similarity(words_A[i], words_B[j])
			# TODO: Find the trace in the sim_mat
			similarity = 0
		# TODO: elif one is phrase, the other is word
		# elif min(len(words_A), len(words_B)) == 1 and \
		# 	max(len(words_A), len(words_B)) > 1:
					
		return similarity

	def visualize_anchor(self, sents_by_tokens, anchors):
		for sent in sents_by_tokens:
			for token in sent:
				for key_word in anchors.keys():
					for anchor in anchors[key_word].keys():
						if anchor == token:
							print '[%s]' % key_word,
				print '%s ' % token,
			print '\n'