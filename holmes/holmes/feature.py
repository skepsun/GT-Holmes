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

from tfrbm import GBRBM
from holmes import catscorpus, utils

class Feature(catscorpus.CatsCorpus, utils.Config):
	"""
	
	"""

	def __init__(self, root_path, is_tfidf=False):
		catscorpus.CatsCorpus.__init__(self, root_path=root_path)
		# Select training corpus
		self.is_tfidf = is_tfidf
		if self.is_tfidf:
			self.training_corpus = self.tfidf  # Take tfidf matrxi as input
		else:
			self.training_corpus = self.corpus # Take bow corpus as input

	def encoder_lda(self, num_topics=100, chunksize=500):
		"""
		
		"""

		self.num_topics = num_topics
		# Train LDA based on training dataset
		self.lda = LdaModel(corpus=self.training_corpus, id2word=self.dictionary, \
			                num_topics=num_topics, update_every=1, chunksize=chunksize, passes=1)
		# Convert bow into topic vectors
		self.corpus_lda = self.lda[self.training_corpus]

	def encoder_lsi(self, num_components=100, chunksize=500, is_tfidf=False):
		"""
		
		"""

		self.num_components = num_components
		# Train LSI based on training dataset
		self.lsi = LsiModel(corpus=self.training_corpus, id2word=self.dictionary, \
		                           num_topics=num_components, chunksize=chunksize) # initialize an LSI transformation
		# Convert bow into LSI projections
		self.corpus_lsi = self.lsi[self.training_corpus]

	def encoder_gbrbm(self, n_hidden=1000, lr=0.01, n_epoches=10, batch_size=100):
		"""
		"""

		n_visible        = len(self.dictionary)
		training_dataset = corpus2dense(self.training_corpus, num_terms=n_visible).transpose()
		self.rbm = GBRBM(n_visible, n_hidden=n_hidden, learning_rate=lr, momentum=0.95, \
			             err_function='mse', use_tqdm=False, sample_visible=False, sigma=1)
		self.rbm.fit(training_dataset, n_epoches=n_epoches, batch_size=batch_size, \
			         shuffle=True, verbose=True)
		self.corpus_rbm = self.rbm.transform(training_dataset)

	def save_gbrbm(self, model_path=None, output_path=None):
		"""
		"""
		
		model_path  = "%s/%s" % (model_path, "model")
		output_path = "%s/%s" % (output_path, "npy.mat.txt")

		# if model_path:
			# self.rbm.save(model_path)
		if output_path:
			# numpy_matrix = corpus2dense(self.corpus_lda, num_terms=self.num_topics)
			np.savetxt(output_path, self.corpus_rbm, delimiter=',')


	def save_lda(self, model_path=None, output_path=None):
		"""

		"""

		model_path  = "%s/%s" % (model_path, "model")
		output_path = "%s/%s" % (output_path, "npy.mat.txt")

		if model_path:
			self.lda.save(model_path)
		if output_path:
			numpy_matrix = corpus2dense(self.corpus_lda, num_terms=self.num_topics).transpose()
			np.savetxt(output_path, numpy_matrix, delimiter=',')

	def save_lsi(self, model_path=None, output_path=None):
		"""

		"""

		model_path  = "%s/%s" % (model_path, "model")
		output_path = "%s/%s" % (output_path, "npy.mat.txt")

		if model_path:
			self.lsi.save(model_path)
		if output_path:
			numpy_matrix = corpus2dense(self.corpus_lsi, num_terms=self.num_components).transpose()
			np.savetxt(output_path, numpy_matrix, delimiter=',')

	def random_sampling(self, num_samples):
		catscorpus.CatsCorpus.random_sampling(self, num_samples)
		# Select training corpus
		if self.is_tfidf:
			self.training_corpus = self.tfidf  # Take tfidf matrxi as input
		else:
			self.training_corpus = self.corpus # Take bow corpus as input

	def category_sampling(self, categories):
		catscorpus.CatsCorpus.category_sampling(self, categories)
		# Select training corpus
		if self.is_tfidf:
			self.training_corpus = self.tfidf  # Take tfidf matrxi as input
		else:
			self.training_corpus = self.corpus # Take bow corpus as input


	def __iter__(self):
		pass



		