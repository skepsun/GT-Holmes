#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import numpy as np
from copy import deepcopy
from holmes import utils

"""

"""

class BootstrappingShuffle(object):
	"""
	Bootstrapping Shuffle
	


	>>> ds = np.array([[1,0,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0,0], [0,0,1,0,0,0,0,0,0,0], \
	>>>                [0,0,0,1,0,0,0,0,0,0], [0,0,0,0,1,0,0,0,0,0], [0,0,0,0,0,1,0,0,0,0], \
	>>>	               [0,0,0,0,0,0,1,0,0,0], [0,0,0,0,0,0,0,1,0,0], [0,0,0,0,0,0,0,0,1,0], \
	>>>                [0,0,0,0,0,0,0,0,0,1]])
    >>> ys = np.array([1,1,1,1,1,1,1,0,0,0])
    >>> shuffle = BootstrappingShuffle(ds, ys, num_test=1)
    >>> for dataset in shuffle:
    >>>     ... ...
	"""

	def __init__(self, Xs, ys, num_test=1):

		# The set of all possible value of y
		self.y_set = list(set(ys))
		# Step 1: <Sub training set> Organize input data by the value of y
		# e.g. Xs = [ x_1, x_2, ..., x_n ] and 
		#      ys = [ y_a, y_b, ..., y_a ] ( y belongs to {y_a, y_b} ) => 
		#      subsets = [ 
		#          [ (x_1, y_a), (x_i, y_a), ... ], 
		#          [ (x_2, y_b), (x_j, y_b), ... ] ]
		self.subsets = [
			[ [x, y] for x, y in zip(Xs, ys) if y == k ] # Sub training set: list of tuple (X, y) with same y
			for k in self.y_set ]                             # Iterate through every possible y
		# Step 2: Validate if the num_test is greater than the minimum number of test samples
		min_num_sample = min([ len(xys) for xys in self.subsets ])
		if min_num_sample <= num_test:
			raise Exception("The number of samples (%d) is less than indicated num_test (%s)." % 
				(min_num_sample, num_test))
		# Step 3: <Combinations of indexs of test samples> Get test sample set for each of the sub training set.
		# e.g. combs = [ 
		#          [ [index_xys, ...], [index_xys, ...], ... ] combinations for subset of y_a
		#          [ [index_xys, ...], [index_xys, ...], ... ] combinations for subset of y_b
		#          ... ] 
		self.combs = [ 
			list(itertools.combinations(    # Combinations of all possible of [num_test] indexs of test samples
				range(len(xys)), num_test)) # List of indexs of a sub training set
			for xys in self.subsets ]            # Iterate through every sub training set
		# List of numbers of combinations for each of possible value of y
		combs_index_list = [ range(len(comb)) for comb in self.combs ]
		# All possible combinations of the indexs between each of the possible value of y
		self.product_combs_index = list(itertools.product(*combs_index_list))

	def __iter__(self):
		"""
		Iterate through every bootstrapping test subset. Because all the possible combinations of 
		bootstrapping selections would be enormous amount of generative data, this method is designed
		to be independent on the actual size of the raw dataset, which is a memory friendly way to 
		generate subsets.  
		"""

		# Iterate throught every bootstrapping test subset
		# Each subset is one possible selection from the raw dataset
		for combs_index in self.product_combs_index:
			testset  = []
			trainset = []
			# i is the index of the possible value of y
			for i in range(len(combs_index)):
				c = self.combs[i][combs_index[i]]    # a combinations of the indexs of the test samples with y_i
				xys_cp   = deepcopy(self.subsets[i]) # deep copy of the raw dataset (list of tuple (x, y)) with y_i
				testset  += utils.pops(c, xys_cp)    # test samples 
				trainset += xys_cp                   # train samples
			# Each time only yield one possible test subset, 
			# which is a more memory friendly way
			testset_Xs  = np.array([ x for x, _ in testset ])
			testset_ys  = np.array([ y for _, y in testset ])
			trainset_Xs = np.array([ x for x, _ in trainset ])
			trainset_ys = np.array([ y for _, y in trainset ])
			yield trainset_Xs, trainset_ys, testset_Xs, testset_ys



# TODO: Refine the script to a class

if __name__ == "__main__":

	from holmes.models.clicks2score import Clicks2Score
	from holmes.catscorpus import CatsCorpus
	from scipy.sparse import csc_matrix
	import tensorflow as tf

	# Configurations
	num_test = 1


	root_path       = "resource/test_corpus"
	corpus_path     = "%s/%s" % (root_path, "corpus.mm") 
	dictionary_path = "%s/%s" % (root_path, "vocab.dict")
	cats_path       = "%s/%s" % (root_path, "cats")
	cats_corpus     = CatsCorpus(corpus_path, dictionary_path, cats_path)

	# TODO: Integrate it into catscorpus

	doc_len  = len(cats_corpus.corpus)
	dict_len = len(cats_corpus.dictionary)

	# Improve the way of creating sparse matrix
	doc_ind = 0
	row = []
	col = []
	val = []

	for doc in cats_corpus.corpus:
		row += [ doc_ind for _ in range(len(doc)) ]
		col += [ term_ind for term_ind, freq in doc ]
		val += [ freq for term_ind, freq in doc ]
		doc_ind += 1

	rawdata = csc_matrix((val, (row, col)), shape=(doc_len, dict_len)).toarray()

	q_ind  = 0
	d_inds = range(doc_len)
	d_inds.pop(q_ind)
	
	q = rawdata[q_ind]
	ds = np.delete(rawdata, q_ind, 0)
	ys = np.array([ 
		int(cats_corpus.cats["collections"][q_ind][1] == cats_corpus.cats["collections"][d_ind][1]) 
		for d_ind in d_inds ])

	qs      = np.array([ q for _ in range(len(d_inds)-num_test*2) ])
	test_qs = np.array([ q for _ in range(num_test*2) ])

	accs = []
	shuffle = BootstrappingShuffle(ds.tolist(), ys.tolist(), num_test=num_test)
	for train_ds, train_ys, test_ds, test_ys in shuffle:

		# Train
		model = Clicks2Score(dict_len, iters=100, lr=0.1, batch_size=1)

		with tf.Session() as sess:
			model.train(sess, qs, train_ds, train_ys, test_qs, test_ds, test_ys)
			acc = model.test_acc(sess, test_qs, test_ds, test_ys)
			print acc
			accs.append(acc)

	print accs


	
