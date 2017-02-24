#!/usr/local/bin/python

from collections import defaultdict # Counter, 
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.tokenize.mwe import MWETokenizer
import numpy as np
import json
import sys

from phrases import PhrasesSimilarity, isPhrase, PhrasesExtractor
from words import WordsCounter, WordsSimilarity, GetSentsByWords
from .. utils import ConfigSectionMap


class Text:
	
	def __init__(self, text):
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
		self.interested_phrases = list(set([
			item
			for sublist in self.words_category.values() # Get sublist
			for item in sublist                         # Merge sublist
			if isPhrase(item)                           # Filter non phrases
		]))
		# - word2vec model
		self.word2vec_model     = Word2Vec.load_word2vec_format(word2vec_model_path, binary=True)
		# - phrases extractor (n-gram kernel)
		self.phrases_extractor  = PhrasesExtractor(
			phrases_extractor_path, 
			self.word2vec_model, 
			interested_phrases=self.interested_phrases
		)

		# Tokenize the raw text
		self._tokenize()

	def _tokenize(self):
		self.sents_by_tokens = []
		self.sents_by_words  = GetSentsByWords(self.text)
		self.mwe             = MWETokenizer()
		# Take interested phrases from the text into consideration
		phrases_info = self.phrases_extractor.phrases_info(self.text) # Get all possible phrases from the text
		for p in phrases_info.keys():
			self.mwe.add_mwe(str(p).split('_'))
		for sent in self.sents_by_words:
			# Text by tokens
			sent_by_tokens = [
				token
				for token in self.mwe.tokenize(sent)
			]
			self.sents_by_tokens.append(sent_by_tokens)

	def text_structure(self):
		tokens_info = defaultdict(lambda: {
			# The list of indexs of the token in the whole text
			'token_indexs': [],
			# The list of indexs of the sentences in the whole text
			'sent_indexs': [],
			# The list of indexs of the token in their sentences
			'inner_indexs': []
		})
		token_i = 0
		sent_i  = 0
		inner_i = 0
		for sent in self.sents_by_words:
			# Tokens structure info
			for token in self.mwe.tokenize(sent):
				if token not in stopwords.words('english') and len(token) > 2:
					tokens_info[token]['token_indexs'].append(token_i)
					tokens_info[token]['sent_indexs'].append(sent_i)
					tokens_info[token]['inner_indexs'].append(inner_i)
				token_i += 1
				inner_i += 1
			sent_i += 1
			inner_i = 0
		
		return tokens_info

	def anchor_keywords(words_category, tokens_info):
		anchors = {}
		for categories in words_category.keys():
			category_list = categories.strip().split('/')
			similar_tokens_info = defaultdict(lambda: 0)
			for category in category_list:
				for token in tokens_info.keys():
					sim = PhrasesSimilarity(self.word2vec_model, category, token)
					if sim > 0.5 and sim > similar_tokens_info[token]:
						similar_tokens_info[token] = sim
			anchors[categories] = similar_tokens_info
		return anchors

	def visualize_anchor(sents_by_tokens, anchors):
		for sent in sents_by_tokens:
			for token in sent:
				for key_word in anchors.keys():
					for anchor in anchors[key_word].keys():
						if anchor == token:
							print '[%s]' % key_word,
				print '%s ' % token,
			print '\n'