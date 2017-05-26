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
from engine.utilities.utils import Config
from engine.utilities.plot import MockGeoLocation, ScatterPointsSimilarities

def code2desc(codes, crime_codes_dict):
	"""
	Interpret crime codes as a brief description by crime-codes-dictionary

	Note that if code is '9999' which means non-crime or there is no description for the code
	in dictionary, it'd disgard this code without interpretation.
	"""
	codes = [ code for code in codes if code != "9999"]
	desc = "/".join([crime_codes_dict[code] for code in codes if code in crime_codes_dict.keys()])
	return desc



if __name__ == "__main__":

	# Read configuration from ini file
	conf = Config("../../conf/text.ini")
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
	id_list   = []
	code_list = []
	with open(code_list_path, "rb") as f:
		for line in f.readlines():
			id, codes_str = line.strip("\n").split("\t")
			id_list.append(id)
			code_list.append([ code for code in codes_str.strip("\n").split("#") ])
	descs = [ code2desc(codes, crime_codes_dict) for codes in code_list ]

	# ----------------------------------------------------------------------
	# Uncomment the following snippets of code to load dictionary and corpus
	# for calculating similarities between each of the crime records, and 
	# print the results to standard output.

	# Load dictionary
	print >> sys.stderr, "[%s] Loading existed dictionary ..." % arrow.now()
	dictionary = corpora.Dictionary()
	dictionary = dictionary.load(pruned_dict_path)
	print >> sys.stderr, "[%s] Dictionary: %s" % (arrow.now(), dictionary)

	# Load corpus
	print >> sys.stderr, "[%s] Loading existed corpus ..." % arrow.now()
	corpus = corpora.MmCorpus(mm_corpus_path)
	print >> sys.stderr, "[%s] Corpus: %s" % (arrow.now(), corpus)

	print >> sys.stderr, "[%s] Init Tfidf model." % arrow.now()
	tfidf = models.TfidfModel(corpus)

	print >> sys.stderr, "[%s] Calculating similarities ..." % arrow.now()
	index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=74945)
	sim_np_mat = index[tfidf[corpus[0:25]]]
	
	with open("sims.txt", "w") as f:
		for no, sim_np_vec in list(enumerate(sim_np_mat)):
			f.write("%s\n" % "\t".join([str(sim) for sim in sim_np_vec.tolist()]))

	# End of the snippets
	# ----------------------------------------------------------------------

	# Load similariites files into a 2D python list (matrix) with the order of crime records
	print >> sys.stderr, "[%s] Loading Similarities ..." % arrow.now()
	sim_mat = []
	with open("sims.txt", "rb") as f:
		sim_mat = [ [ float(float_str) for float_str in line.strip("\n").split("\t") ] for line in f.readlines() ]
	sim_mat = np.array(sim_mat)

	# Plot similarities
	print >> sys.stderr, "[%s] Plotting Similarities ..." % arrow.now()
	# Prepare tags
	descs = descs[:24]
	prest_tags = ["Ped Robbery", "Burglary"]
	# unset_tag  = "Random Cases"
	tags = []
	for desc  in descs:
		if desc not in prest_tags:
			tags.append(2)
		else:
			tags.append(prest_tags.index(desc))
	print tags
	# Generate mock locations
	locations = MockGeoLocation(
		tags, 
		seed=10,
		means=[(0, 0), (10, 3)], 
		cov=[[1, 0], [0, 1]]
	)
	# Plot
	ScatterPointsSimilarities(
		descs, locations, tags, sim_mat[:24, :24], 
		mycolormap=['r', 'g'], 
		mytagmap=prest_tags,
		threshold=0.0
		# xlim=[-4, 8], ylim=[0, 9]
	)

	# ----------------------------------------------------------------------
	# Uncomment the following snippet of code to print first num_res results 
	# to local text file.

	# num_res = 30
	# for i in range(num_res):
	# 	inds = sim_mat[i,:100].argsort()
	# 	print >> sys.stderr, "[%s] Writting result %d ..." % (arrow.now(), i)
	# 	with open("sims_with_first100/res_%s.txt" % id_list[i], "w") as f:
	# 		for ind in inds[-100:]:
	# 			f.write("\t".join([id_list[ind], str(sim_mat[i,ind]), descs[ind]]) + "\n")

	# End of the snippets
	# ----------------------------------------------------------------------
