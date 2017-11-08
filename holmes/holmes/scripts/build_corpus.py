#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from holmes.catscorpus import CatsCorpus

"""
	
"""

if __name__ == "__main__":
	
	# Parse the input parameters
	parser = argparse.ArgumentParser(description="Script for parsing xml format crime records.")
	parser.add_argument("-q", "--query_id", required=True, help="The query id")
	parser.add_argument("-n", "--num", default=1, type=int, help="Return the top n results")
	parser.add_argument("-s", "--score", default=0.0, type=float, help="Return the results that have the similarities above the threshold")
	parser.add_argument("-c", "--config", required=True, help="The path of the configuration file")

	text_path = "data/records_56+500/text.txt"
	cats_path = "data/records_56+500/cats.txt"
	cats_def  = [ "ID", "C", "T" ]

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