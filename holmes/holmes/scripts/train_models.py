#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import sys
import math
import arrow
import random
import argparse
import itertools
import numpy as np
import tensorflow as tf

from copy import deepcopy
from holmes import utils
from scipy.sparse import csc_matrix

from holmes.models.correlation import Correlation
from holmes.catscorpus import CatsCorpus



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



def train_correlation(cats_corpus, test_train_ratio=0.1, lr=0.01, batch_size=1):
	"""
	Train Correlation


	"""

	# All of the categories that appeared in the corpus at least once
	categories_set = list(set(cats_corpus.categories()))
	if "RANDOM" not in categories_set:
		# TODO: If there is no random category, then do the testing among the labeled cases
		return None

	# Random cases
	random_cases = cats_corpus["RANDOM"]
	# Dataset of Labeled cases
	labeled_dataset = [ 
		[ category, cats_corpus[category] ]
		for category in categories_set 
		if category != "RANDOM" ]
	
	for category, labeled_cases in labeled_dataset:
		# Split dataset into test group and train group by the test_train_ratio
		# Labeled dataset
		labeled_test_num     = int(math.ceil(float(len(labeled_cases)) * test_train_ratio)) # At least one test sample
		labeled_test_indice  = random.sample(range(len(labeled_cases)), labeled_test_num)
		labeled_train_indice = list(set(range(len(labeled_cases))) - set(labeled_test_indice))
		labeled_test_cases   = labeled_cases[labeled_test_indice, :].tolist()
		labeled_train_cases  = labeled_cases[labeled_train_indice, :].tolist()
		# Random dataset (unlabeled, i.e. uncorrelated)
		random_test_num      = int(math.ceil(float(len(random_cases)) * test_train_ratio)) # At least one test sample
		random_test_indice   = random.sample(range(len(random_cases)), random_test_num)
		random_train_indice  = list(set(range(len(random_cases))) - set(random_test_indice))
		random_test_cases    = random_cases[random_test_indice, :].tolist()
		random_train_cases   = random_cases[random_train_indice, :].tolist()
		# Preparation of training data and testing data
		q        = labeled_train_cases.pop(0)
		train_ds = np.array(labeled_train_cases + random_train_cases)
		train_ys = np.array([ 1 ] * len(labeled_train_cases) + \
			                [ 0 ] * len(random_train_cases))
		train_qs = np.array([ q ] * len(train_ds))
		test_ds  = np.array(labeled_test_cases + random_test_cases)
		test_ys  = np.array([ 1 ] * len(labeled_test_cases) + \
			                [ 0 ] * len(random_test_cases))
		test_qs  = np.array([ q ] * len(test_ds))

		iters = int(math.ceil(len(train_qs)/batch_size))
		# Logging
		print >> sys.stderr, "----------------------------"
		print >> sys.stderr, "Category:\t%s" % category
		print >> sys.stderr, "Number of training dataset:\t(+) %d + (-) %d = %d" % \
			(len(labeled_train_cases), len(random_train_cases), len(train_ds))
		print >> sys.stderr, "Number of testing dataset:\t(+) %d + (-) %d = %d" % \
			(len(labeled_test_cases), len(random_test_cases), len(test_ds))
		print >> sys.stderr, "Batch size:\t%d, Iterations:\t%d, Learning Rate:\t%f" % \
			(batch_size, iters, lr)
		# Training process
		model = Correlation(len(q), iters=iters, lr=lr, batch_size=batch_size)
		with tf.Session() as sess:
			model.train(sess, train_qs, train_ds, train_ys, test_qs, test_ds, test_ys)
			acc = model.test_acc(sess, test_qs, test_ds, test_ys)
			# Logging
			print >> sys.stderr, "<Accuracy>:\t%f" % acc


def main():
	# Parse the input parameters
	parser = argparse.ArgumentParser(description="Script for training corpus")
	parser.add_argument("-p", "--path", required=True, help="The path of root folder which contains the corpus")
	parser.add_argument("-i", "--iters", default=100, type=int, help="Iterations")
	parser.add_argument("-b", "--batch", default=1, type=int, help="Batch size")
	parser.add_argument("-l", "--lr", default=0.01, type=float, help="Learning rate")
	parser.add_argument("-t", "--test", default=1, type=int, help="Number of positive/negative test samples")
	args = parser.parse_args()

	# Basic config
	root_path   = args.path
	cats_corpus = CatsCorpus(root_path)

	# Model config	
	batch_size = args.batch
	iters      = args.iters
	lr         = args.lr

	cats_corpus.cats["definitions"] = [ "ID", "C", "T", "LAT", "LONG" ]
	train_correlation(cats_corpus, lr=lr, batch_size=batch_size)

	# Create sparse matrix for corpus' documents
	# TODO: Improve the way of creating sparse matrix
	# doc_ind = 0
	# row = []
	# col = []
	# val = []

	# for doc in cats_corpus.corpus:
	# 	row += [ doc_ind for _ in range(len(doc)) ]
	# 	col += [ term_ind for term_ind, freq in doc ]
	# 	val += [ freq for term_ind, freq in doc ]
	# 	doc_ind += 1

	# rawdata = csc_matrix((val, (row, col)), shape=(doc_len, dict_len)).toarray()

	# # The indexs of the documents which would be trained
	# d_inds = range(doc_len)
	# d_inds.pop(q_ind)

	# # Preparation of the training data
	# q  = rawdata[q_ind]
	# qs = np.array([ q for _ in range(len(d_inds)-num_test*2) ])
	# ds = np.delete(rawdata, q_ind, 0)
	# ys = np.array([ 
	# 	int(cats_corpus.cats["collections"][q_ind][1] == cats_corpus.cats["collections"][d_ind][1])
	# 	for d_ind in d_inds ])
	# test_qs = np.array([ q for _ in range(num_test*2) ])

	# # Apply bootstrapping to generate new dataset
	# accs = []
	# shuffle = BootstrappingShuffle(ds.tolist(), ys.tolist(), num_test=num_test)
	# for train_ds, train_ys, test_ds, test_ys in shuffle:
	# 	# Train
	# 	model = Clicks2Score(dict_len, iters=iters, lr=lr, batch_size=batch_size)
	# 	with tf.Session() as sess:
	# 		model.train(sess, qs, train_ds, train_ys, test_qs, test_ds, test_ys)
	# 		acc = model.test_acc(sess, test_qs, test_ds, test_ys)
	# 		print acc
	# 		accs.append(acc)

	# print accs



# TODO: Refine the script to a class
if __name__ == "__main__":
	main()