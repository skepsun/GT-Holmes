#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import sys
import arrow
import pickle
import numpy as np
from gensim.matutils import corpus2dense
from gensim.models.ldamodel import LdaModel
from gensim.models.lsimodel import LsiModel

from holmes import catscorpus, utils

class Feature(catscorpus.CatsCorpus, utils.Config):
	"""
	
	"""

	def __init__(self, root_path, is_tfidf=False):
		catscorpus.CatsCorpus.__init__(self, root_path=root_path)
		# Select training corpus
		if is_tfidf:
			self.training_corpus = self.tfidf  # Take tfidf matrxi as input
		else:
			self.training_corpus = self.corpus # Take bow corpus as input

	def train_lda(self, num_topics=100, chunksize=500):
		"""
		
		"""

		self.num_topics = num_topics
		# Train LDA based on training dataset
		self.lda = LdaModel(corpus=self.training_corpus, id2word=self.dictionary, \
			                num_topics=num_topics, update_every=1, chunksize=chunksize, passes=1)

		# Convert bow into topic vectors
		self.corpus_lda = self.lda[self.training_corpus]

	def train_lsi(self, num_components=100, chunksize=500, is_tfidf=False):
		"""
		
		"""

		self.num_components = num_components
		# Select training corpus
		if is_tfidf:
			corpus = self.tfidf  # Take tfidf matrxi as input
		else:
			corpus = self.corpus # Take bow corpus as input

		# Train LSI based on training dataset
		self.lsi = LsiModel(corpus=self.training_corpus, id2word=self.dictionary, \
		                           num_topics=num_components, chunksize=chunksize) # initialize an LSI transformation
		# Convert bow into LSI projections
		self.corpus_lsi = self.lsi[self.training_corpus]

	def save_lda(self, model_path=None, output_path=None):
		"""

		"""

		model_path  = "%s/%s" % (model_path, "model")
		output_path = "%s/%s" % (output_path, "npy.mat.txt")

		if model_path:
			self.lda.save(model_path)
		if output_path:
			numpy_matrix = corpus2dense(self.corpus_lda, num_terms=self.num_topics)
			np.savetxt(output_path, numpy_matrix, delimiter=',')

	def save_lsi(self, model_path=None, output_path=None):
		"""

		"""

		model_path  = "%s/%s" % (model_path, "model")
		output_path = "%s/%s" % (output_path, "npy.mat.txt")

		if model_path:
			self.lsi.save(model_path)
		if output_path:
			numpy_matrix = corpus2dense(self.corpus_lsi, num_terms=self.num_components)
			np.savetxt(output_path, numpy_matrix, delimiter=',')

	def __iter__(self):
		pass



		