#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script calculates and plots the similarities of crime records. In particular, you can
uncomment some parts of the code (which have been marked within two dash lines) to only do
the plotting based on the previous results.

Similarities are operated in a form of text file. Each line of the text file is a list of 
similarities between the related crime record and others. 

Noted if we run the program on top of the whole dataset, which is super large, it would bring
up a horrible problem: Huge memory and storage consuming. There are two possible way to solve
this issue.
1. Do this job in batch, run every N ( N < 500 ) crime records.
2. Override the code of calculating similarities ( provided by gensim.similarities ) to make
   the program iterable and avoid unlimited memory&storage consuming
"""

import string
import arrow
import nltk
import json
import sys
import numpy as np
from gensim import corpora, models, similarities
from holmes.utilities.config import Config
# from holmes.utilities.plot import MockGeoLocation, ScatterPointsSimilarities

def code2desc(codes, crime_codes_dict):
	"""
	Interpret crime codes as a brief description by crime-codes-dictionary

	Note that if code is '9999' which means non-crime or there is no description for the code
	in dictionary, it'd disgard this code without interpretation.
	"""
	codes = [ code for code in codes if code != "9999"]
	desc = "/".join([crime_codes_dict[code] for code in codes if code in crime_codes_dict.keys()])
	return desc



class BagOfWords:

	def __init__(self):
		# Read configuration from ini file
		conf = Config("conf/text.ini")
		# Read Crime Codes Descriptions
		pruned_dict_path      = conf.config_section_map("Corpus")["pruned_dict_path"]
		mm_corpus_path        = conf.config_section_map("Corpus")["mm_corpus_path"]
		crime_codes_desc_path = conf.config_section_map("Corpus")["crime_codes_desc_path"]
		code_list_path        = conf.config_section_map("Corpus")["labels_path"]

		print >> sys.stderr, "[%s] Loading Crime Codes Dictionary & Labels ..." % arrow.now()
		# Load (crime codes vs description) dictionary
		crime_codes_dict = {}
		with open(crime_codes_desc_path, "rb") as f:
			crime_codes_dict = json.load(f)
		# Load codes list & interpret code as description
		self.id_list   = []
		self.code_list = []
		with open(code_list_path, "rb") as f:
			for line in f.readlines():
				id, codes_str = line.strip("\n").split("\t")
				self.id_list.append(id)
				self.code_list.append([ code for code in codes_str.strip("\n").split("#") ])
		self.descs = [ code2desc(codes, crime_codes_dict) for codes in self.code_list ]

		# # for testing
		# self.pos_list = [ (33.7490 + (lat_diff - 0.5) * 0.05, -84.3880 + (lon_diff - 0.5) * 0.05)
		# 	for lat_diff, lon_diff in np.random.random_sample((len(self.id_list), 2)).tolist() ]

		# Load dictionary
		print >> sys.stderr, "[%s] Loading existed dictionary ..." % arrow.now()
		dictionary = corpora.Dictionary()
		dictionary = dictionary.load(pruned_dict_path)
		print >> sys.stderr, "[%s] Dictionary: %s" % (arrow.now(), dictionary)

		# Load corpus
		print >> sys.stderr, "[%s] Loading existed corpus ..." % arrow.now()
		self.corpus = corpora.MmCorpus(mm_corpus_path)
		print >> sys.stderr, "[%s] Corpus: %s" % (arrow.now(), self.corpus)

		print >> sys.stderr, "[%s] Init Tfidf model." % arrow.now()
		self.tfidf = models.TfidfModel(self.corpus)

		print >> sys.stderr, "[%s] Calculating similarities ..." % arrow.now()
		self.index = similarities.SparseMatrixSimilarity(self.tfidf[self.corpus], num_features=74945)

		# sim_np_mat = index[tfidf[corpus[0:25]]]
		# self.sim_mat = np.array([ sim_np_vec for no, sim_np_vec in list(enumerate(sim_np_mat)) ])

	def similarityVector(self, id, limit):

		if id not in self.id_list:
			return None

		query_ind = self.id_list.index(id)
		sim_vec = self.index[self.tfidf[self.corpus[query_ind]]]
		res_inds = sim_vec.argsort()
		return [ [self.id_list[ind], sim_vec[ind], self.descs[ind]] 
			for ind in res_inds[-1 * limit:] ]

	def similarityMatrix(self, ids):

		query_inds = [ self.id_list.index(id) for id in ids if id in self.id_list ]
		sim_mat    = self.index


if __name__ == "__main__":

	f = Feature()
	print >> sys.stderr, "test start"
	print f.query_via_id("170160001", 50)


