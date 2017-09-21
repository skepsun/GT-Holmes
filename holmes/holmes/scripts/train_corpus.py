#!/usr/bin/env python
# -*- coding: utf-8 -*-



"""

"""

# TODO: Refine the script to a class
if __name__ == "__main__":

	from holmes.models.clicks2score import Clicks2Score
	from holmes.catscorpus import CatsCorpus
	from scipy.sparse import csc_matrix
	import tensorflow as tf
	import numpy as np

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
	print rawdata.shape
	print rawdata

	q_ind  = 0
	d_inds = range(doc_len)
	d_inds.pop(q_ind)
	
	q = rawdata[q_ind]
	ds = np.delete(rawdata, q_ind, 0)
	print q.shape, q
	print ds.shape, ds

	ys = np.array([ int(cats_corpus.cats["collections"][q_ind][1] == cats_corpus.cats["collections"][d_ind][1]) for d_ind in d_inds ])
	print ys

	# Train

	qs = np.array([ q for _ in range(len(d_inds)) ])

	test_qs = qs
	test_ds = ds
	test_ys = ys

	print qs.shape
	print ds.shape
	print ys.shape

	model = Clicks2Score(dict_len, iters=10000, lr=0.00001, batch_size=1)

	with tf.Session() as sess:
		model.train(sess, qs, ds, ys, test_qs, test_ds, test_ys)



		
