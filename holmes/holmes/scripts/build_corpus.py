#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from holmes.catscorpus import CatsCorpus

"""
	
"""

if __name__ == "__main__":

	text_path = "data/records_56+500/text.txt"
	cats_path = "data/records_56+500/cats.txt"
	cats_def  = [ "ID", "C", "T", "LAT", "LONG"]

	# Init CatsCorpus object
	cats_corpus = CatsCorpus()
	# Make input data iterable
	with open(text_path, "rb") as text_fhandle, open(cats_path, "rb") as cats_fhandle:
		# Building cats corpus by processing raw data
		print >> sys.stderr, "Building Cats Corpus."
		cats_corpus.build(text_fhandle, cats_fhandle, cats_def, n=3)

	# Serializing and saving built catscorpus in local files
	print >> sys.stderr, "Serializing and saving the corpus in local file."
	cats_corpus.save_corpus("resource/56labeld+500random.corpus", \
		                    "resource/56labeld+500random.corpus", \
		                    "resource/56labeld+500random.corpus")