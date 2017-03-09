#!/usr/local/bin/python

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import LatentDirichletAllocation
# from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from os import listdir
import string
import nltk
import sys

class WordsAnalysor:

	def __init__(self):
		self.corpus = []

	def add_document(self, text):
		self.corpus.append(text)
		self.cur_sents_by_words = self._get_sents_by_words(text)

	def _get_sents_by_words(self, text):
		sentences = []
		# - Remarks for each of the crimes are delimited by '\2'
		for remarks in text.strip('\n').split('\2'):
			# - Free text part for each of the records are delimited by '\1'
			for remark in remarks.strip().split('\1'):
				# - For every sentences in each of the free text part
				for sent in sent_tokenize(remark.decode("utf8")):
					# - Split the text into words
					# - Remove uppercases
					# - Remove punctuation
					sentence = [
						'_'.join(word.split('-'))
						for word in nltk.word_tokenize(sent.lower())
						if word not in string.punctuation
					]
					sentences.append(sentence)
		return sentences

	def LSA(
			self,
			stop_words=nltk.corpus.stopwords.words('english'),
			vocabulary=None,
			n_components_for_svd=3
		):
		# Give preference to the vocabulary
		if vocabulary is not None:
			stop_words = None
		# Document-Term Matrix
		cv = CountVectorizer(strip_accents='ascii', stop_words=stop_words, vocabulary=vocabulary)
		self.dt_matrix = cv.fit_transform(self.corpus).toarray()
		self.feature_names = cv.get_feature_names()
		# Tf-idf Transformation
		self.tfidf = TfidfTransformer()
		self.tfidf_matrix = self.tfidf.fit_transform(self.dt_matrix).toarray()
		# SVD
		# n_components is recommended to be 100 by Sklearn Documentation for LSA
		# http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html
		svd = TruncatedSVD(n_components=n_components_for_svd)
		self.svd_matrix = svd.fit_transform(self.tfidf_matrix)

	def LDA(
			self,
			stop_words=nltk.corpus.stopwords.words('english'),
			vocabulary=None,
			n_topics=100
		):
		# Give preference to the vocabulary
		if vocabulary is not None:
			stop_words = None
		# Document-Term Matrix
		cv = CountVectorizer(strip_accents='ascii', stop_words=stop_words, vocabulary=vocabulary)
		self.dt_matrix = cv.fit_transform(self.corpus).toarray()
		self.feature_names = cv.get_feature_names()
		# LDA 
		self.lda_matrix = LatentDirichletAllocation(
			n_topics=n_topics, 
			max_iter=5, 
			learning_method='online', 
			learning_offset=50., 
			random_state=0).fit_transform(self.dt_matrix)
        
