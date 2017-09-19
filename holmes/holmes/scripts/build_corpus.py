#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from holmes.catscorpus import CatsCorpus

"""
	
"""

if __name__ == "__main__":

	text_path = "data/26_labeled_records/text.txt"
	cats_path = "data/26_labeled_records/cats.txt"
	cats_def  = [ "incident_id", "crime_code", "crime_desc", "incident_datetime", \
                  "avg_lat", "avg_long" ]

	# Init CatsCorpus object
	cats_corpus = CatsCorpus()
	# Make input data iterable
	with open(text_path, "rb") as text_fhandle, open(cats_path, "rb") as cats_fhandle:
		# Building cats corpus by processing raw data
		print >> sys.stderr, "Building Cats Corpus."
		cats_corpus.build(text_fhandle, cats_fhandle, cats_def, n=3)

	# Serializing and saving built catscorpus in local files
	print >> sys.stderr, "Serializing and saving the corpus in local file."
	cats_corpus.save_corpus("resource/test_corpus/corpus.mm", \
		                    "resource/test_corpus/vocab.dict", \
		                    "resource/test_corpus/cats")