#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
import sys
import pickle
from gensim.models.ldamodel import LdaModel

from holmes import catscorpus, utils

class TopicsFeature(catscorpus.CatsCorpus, utils.Config):
	"""
	
	"""

	def __init__(self, corpus_path, dictionary_path, cats_path):
		catscorpus.CatsCorpus.__init__(self, corpus_path=corpus_path, \
			                           dictionary_path=dictionary_path, cats_path=cats_path)

	def train_lda(self, num_samples=None, num_topics=100, chunksize=500):
		"""
		"""
		# Randomly downsampling from original corpus and cats collections
		if num_samples and num_samples < len(self.corpus):
			self.random_sampling(num_samples)
		# Train LDA based on training dataset
		self.lda = LdaModel(corpus=self.corpus, id2word=self.dictionary, num_topics=num_topics, \
			                update_every=1, chunksize=chunksize, passes=1)
		print >> sys.stderr, "test1"
		# Convert bow into topic vectors
		self.doc_lda = [] # self.doc_lda = [ self.lda[doc_bow] for doc_bow in self.corpus ]
		i = 0
		for i in range(len(self.corpus)):
			self.doc_lda.append(self.lda[self.corpus[i]])
			if i % 1000 == 0:
				print >> sys.stderr, "[%s] Converting %s bow documents into topic vectors" % \
				         (arrow.now(), i)

		print >> sys.stderr, "test2"

	def save_lda(self, lda_path=None, topics_path=None):
		"""

		"""

		if lda_path:
			self.lda.save(lda_path)
		if topics_path:
			with open(topics_path, "wb") as h:
				pickle.dump(self.doc_lda, h)
		if self.sampling_flag:
			self.save_corpus()


		