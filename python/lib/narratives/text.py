#!/usr/local/bin/python

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import LatentDirichletAllocation
from itertools import permutations, repeat
from collections import defaultdict
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.tokenize.mwe import MWETokenizer
import numpy as np
import arrow
import json
import sys
import os

from phrases import isPhrase, PhrasesExtractor
from words import WordsAnalysor
from utils import Config

class TextAnalysor:
	'''
	Text

	This is a class for processing the raw text information, 
	extracting useful features and also providing user-friendly data API.
	'''
	INI_PATH       = 'conf/text.ini'
	WORD_MIN_LEN   = 2
	ANCHOR_MIN_SIM = 0.5
	PHRASE_MIN_SIM = 0.8

	def __init__(self):
		print >> sys.stderr, '[TEXT]\t%s\t*** Initializing Text Object ***' % arrow.now()
		# Read Configuration from ini file
		conf = Config(self.INI_PATH)
		phrases_extractor_path = conf.config_section_map('Model')['n_gram']
		word2vec_model_path    = conf.config_section_map('Model')['word2vec']
		words_category_path    = conf.config_section_map('Corpus')['key_words']

		# Variable initialization
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
			interested_phrases=self.interested_phrases
		)
		# - MWE Tokenizer
		self.mwe            = MWETokenizer()
		# Init words analysor
		self.words_analysor = WordsAnalysor()
		# Document-Term Vectors
		self.dt_matrix      = []
		# Labels for documents
		self.labels         = []

	def save_variables(self, file_path):
		# Save the document-term matrix
		np.save(file_path, self.dt_matrix)
		# Save the labels information
		labels = [
			'#'.join(multiple_labels) + '\n'
			for multiple_labels in self.labels
		]
		with open(file_path + '.txt', 'w') as f:
			try:
				f.writelines(labels)
			except:
				print >> sys.stderr, '[ERROR] Saving failed. Invalid file path: %s' % file_path

	def load_variables(self, file_path):
		if not os.path.exists(file_path + '.txt') or not os.path.exists(file_path + '.npy'):
			print >> sys.stderr, '[WARN] Loading failed. Invalid file path: %s' % file_path
			return
		# Load the document-term matrix
		self.dt_matrix = np.load(file_path + '.npy').tolist()
		# Load the labels information
		with open(file_path + '.txt', 'r') as f:
			try:
				labels      = f.readlines()
				self.labels = [
					list(set(label.strip('\n').split('#')))
					for label in labels
				]
			except: 
				print >> sys.stderr, '[ERROR] Loading failed. Unknown error'

	def fuzzy_LSA(self, n_components_for_svd=2):
		print >> sys.stderr, '[TEXT]\t%s\tFuzzy LSA ...' % arrow.now()
		# Tf-idf Transformation
		tfidf = TfidfTransformer()
		tfidf_matrix = tfidf.fit_transform(self.dt_matrix).toarray()
		# SVD
		# n_components is recommended to be 100 by Sklearn Documentation for LSA
		# http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html
		svd = TruncatedSVD(n_components=n_components_for_svd)
		svd_matrix = svd.fit_transform(tfidf_matrix)
		# print >> sys.stderr, tfidf_matrix
		# print >> sys.stderr, svd_matrix
		feature_matrix = svd_matrix.tolist()
		return feature_matrix, \
		       self._sort_by_labels(feature_matrix), \
		       tfidf_matrix.tolist()

	def regular_LSA(self, n_components_for_svd=2):
		print >> sys.stderr, '[TEXT]\t%s\tRegular LSA ...' % arrow.now()
		self.words_analysor.LSA(n_components_for_svd=n_components_for_svd)
		feature_matrix = self.words_analysor.svd_matrix.tolist()
		return feature_matrix, \
		       self._sort_by_labels(feature_matrix), \
		       self.words_analysor.tfidf_matrix.tolist(), \
		       self.words_analysor.dt_matrix.tolist(), \
		       self.words_analysor.feature_names

	# def fuzzy_LDA(self, n_topics_for_lda=2):
	# 	print >> sys.stderr, '[TEXT]\t%s\tFuzzy LDA ...' % arrow.now()
	# 	feature_matrix = LatentDirichletAllocation(
	# 		n_topics=n_topics_for_lda, max_iter=5, 
 #            learning_method='online', 
 #            learning_offset=50., 
 #            random_state=0
 #        ).fit_transform(self.dt_matrix).tolist()
 #        return feature_matrix, \
	# 	       self._sort_by_labels(feature_matrix)

	# def regular_LDA(self, n_topics_for_lda=2):
	# 	print >> sys.stderr, '[TEXT]\t%s\tRegular LDA ...' % arrow.now()
	# 	self.words_analysor.LDA(n_topics=n_topics_for_lda)
	# 	feature_matrix = self.words_analysor.lda_matrix.tolist()
	# 	return feature_matrix, \
	# 	       self._sort_by_labels(feature_matrix), \
	# 	       self.words_analysor.dt_matrix.tolist(), \
	# 	       self.words_analysor.feature_names

	def _sort_by_labels(self, feature_matrix):
		# Get the set for all the labels that appearred
		labels_set         = list(set([ item for sublist in self.labels for item in sublist ]))
		label_feature_dict = {} 
		for label_in_set in labels_set:
			label_feature_dict[label_in_set] = []
			for i in range(len(self.labels)):
				for label_for_feature in self.labels[i]:
					if label_for_feature == label_in_set:
						label_feature_dict[label_in_set].append(feature_matrix[i])
		return label_feature_dict

	def set_text(self, text, label):
		# Init
		self._initialize_temporal_variables()
		# raw text
		self.text = text
		# # Init words analysor
		self.words_analysor.add_document(text)
		# Tokenize the raw text
		# print >> sys.stderr, '[TEXT]\t%s\tTokenizing ...' % arrow.now()
		self._tokenize()
		# Get the structure of the tokenized text
		# print >> sys.stderr, '[TEXT]\t%s\tGetting Structure ...' % arrow.now()
		self._get_structure()
		# Anchor the locations of keywords in the text
		# print >> sys.stderr, '[TEXT]\t%s\tAnchorring Keywords ...' % arrow.now()
		# self._anchor_keywords()
		# Find K-nearest tokens from the text to the tokens in the words_category
		# print >> sys.stderr, '[TEXT]\t%s\tFinding K nearest tokens ...' % arrow.now()
		self._find_k_nearest_tokens()
		self.dt_matrix.append(self.term_vector)
		self.labels.append(label)

	def _initialize_temporal_variables(self):
		self.sents_by_tokens  = []
		self.sents_by_words   = []
		self.phrases_count    = {}
		self.filtered_phrases = {}
		self.length_of_sents  = []
		self.length_of_text   = -1
		self.structure        = {}
		self.anchors          = {}

	def _tokenize(self):
		self.sents_by_tokens  = []
		self.sents_by_words   = self.words_analysor.cur_sents_by_words
		# Take interested phrases from the text into consideration
		self.phrases_count    = self.phrases_extractor.phrases_count(self.text) # Get all possible phrases from the text
		self.filtered_phrases = self._phrases_filter(self.phrases_count.keys())
		# Add the filtered phrases into the MWE Tokenizer
		for p in self.filtered_phrases.keys():
			self.mwe.add_mwe(str(p).split('_'))
		# Tokenize by MWE
		for sent in self.sents_by_words:
			# Text by tokens
			sent_by_tokens = [
				token
				for token in self.mwe.tokenize(sent)
			]
			self.sents_by_tokens.append(sent_by_tokens)

	def _get_structure(self):
		self.length_of_sents = [ len(sents) for sents in self.sents_by_tokens ]
		self.length_of_text  = sum(self.length_of_sents)
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
		for sent in self.sents_by_tokens:
			# Tokens structure info
			for token in sent:
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
					if sim > self.ANCHOR_MIN_SIM and sim > similar_tokens_info[token]:
						similar_tokens_info[token] = sim
			self.anchors[categories] = similar_tokens_info
		# print >> sys.stderr, json.dumps(self.anchors, indent=4)

	def _find_k_nearest_tokens(self, K=10):
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
					elif (not isPhrase(tokens_in_text[i])) and (not isPhrase(tokens_in_category[j])):
						dist_mat[i, j] = self._words_similarity(tokens_in_text[i], tokens_in_category[j])
					else:
						dist_mat[i, j] = 0
			# Find the best matched token in the text for each of token under the category
			best_matched_indexs = dist_mat.argmax(axis=0) # The index of the best matched tokens for each of the category
			best_matched_dists  = []                      # The distance between the best matched words and the words in text
			for j in range(len(best_matched_indexs)):
				best_matched_dists.append(dist_mat[best_matched_indexs[j], j])
			best_matched_dists = np.array(best_matched_dists)
			# Find K-nearest words (to the current category) in the text
			for k in range(K):
				j = best_matched_dists.argmax() # The index of the words in text which has the highest similarity
				i = best_matched_indexs[j]
				# If the current best matched distance is lower than 0, then abandon it.
				if best_matched_dists[j] <= 0:
					break
				best_matched_dists[j] = -1      # Remove the largest value in the best_matched_dists
				self.k_nearest_tokens[category].append({
					'in_text':     tokens_in_text[i],
					'in_category': tokens_in_category[j],
					'count':       len(self.structure[tokens_in_text[i]]['text_indexs']),
					'distance':    dist_mat[i, j]
					# 'rate':        self._rate_token_candidates(category, tokens_in_text[i])
				})
		# Convert term dict to numerical term vector
		self.term_vector = self._term_dict2term_vector(self.k_nearest_tokens)
		# print >> sys.stderr, json.dumps(self.k_nearest_tokens, indent=4)

	def _rate_token_candidates(self, category, candidate_token):
		if not bool(self.anchors[category]):
			return 0
		else:
			dist = np.array([
				self._tokens_min_distance(candidate_token, anchor_token)
				for anchor_token in self.anchors[category].keys()
			]).astype('float')
			# anchor_sim = np.array([self.anchors[category][anchor_token] for anchor_token in self.anchors[category].keys()]).astype('float')
			anchor_sim = np.array(self.anchors[category].values()).astype('float')
			# Rate: determine which token candidate under a category in the text is the most informative, and 
			#       most accurate item as to the category.
			# rate = max(anchor_sim * ((1.0 - dist[:,0] / self.length_of_text) ** dist[:,1]))
			rate = max((1.0 - dist[:,0] / self.length_of_text) ** (dist[:,1] + 1.0))
			return rate
	
	def _phrases_filter(self, phrases):
		filtered_phrases = {}
		for p in phrases:
			sims = [ self._phrases_similarity(p, p_i) for p_i in self.interested_phrases ]
			# Remove irrelevant phrases according to the interested phrases list
			if max(sims) > self.PHRASE_MIN_SIM:
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

	# TODO: We use the minimum distance between two arbitrary tokens to measure the correlation 
	#       of these two tokens. We can propose a more sophisticated method to describe a such 
	#       relationship in the future.
	def _tokens_min_distance(self, token_A, token_B):
		# print >> sys.stderr, token_A, token_B
		# Combinations gives the all the possible combinations of two arbitrary lists
		def combinations(list_A, list_B):
			# Remove the duplicate in the lists
			list_A = list(set(list_A))
			list_B = list(set(list_B))
			_3d_list = list(list(zip(r, p)) for (r, p) in zip(repeat(list_A), permutations(list_B)))
			_2d_list = [ item for sublist in _3d_list for item in sublist ] # flatten 3d list to 2d
			return _2d_list
		# Calculate the distances for every possible combinations of indexs
		if self.structure.has_key(token_A) and self.structure.has_key(token_B):
			text_ind_combs = combinations(self.structure[token_A]['text_indexs'], self.structure[token_B]['text_indexs'])
			sent_ind_combs = combinations(self.structure[token_A]['sent_indexs'], self.structure[token_B]['sent_indexs'])
			text_dists = [ abs(ind_A - ind_B) for ind_A, ind_B in text_ind_combs ]
			sent_dists = [ abs(ind_A - ind_B) for ind_A, ind_B in sent_ind_combs ]
			return min(text_dists), min(sent_dists)
		else:
			print >> sys.stderr, '[TEXT]\t%s\tError: Invalid token %s or %s for measuring distances.' % \
				(arrow.now(), token_A, token_B)
			return -1, -1

	def _term_dict2term_vector(self, term_dict, threshold=0.4):
		term_vector = np.zeros(0)
		for category, pairs in term_dict.iteritems():
			category_vector = np.zeros(len(self.words_category[category]))
			for pair in pairs:
				if pair['distance'] > threshold:
					category_word_index = self.words_category[category].index(pair['in_category'])
					category_vector[category_word_index] = pair['distance'] * pair['count']
			term_vector = np.concatenate((term_vector, category_vector))
		return term_vector.tolist()


