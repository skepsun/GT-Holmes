#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import sys
import unittest
from holmes.catscorpus import CatsCorpus

class CatsCorpusTestCase(unittest.TestCase):
	"""
	"""

	def test_loading_corpus(self):
		"""
		"""

		root_path       = "resource/cats_corpus"
		corpus_path     = "%s/%s" % (root_path, "corpus.mm") 
		dictionary_path = "%s/%s" % (root_path, "vocab.dict")
		cats_path       = "%s/%s" % (root_path, "cats")
		cats_corpus     = CatsCorpus(corpus_path, dictionary_path, cats_path)
		print >> sys.stderr, "Corpus Loaded\n%s" % cats_corpus
		
	@unittest.skip("Building corpus is time-consuming.")
	def test_building_corpus(self):
		"""
		"""

		text_path = "data/text.txt"
		cats_path = "data/cats.txt"
		cats_def  = [ "incident_id", "crime_code", "crime_desc", "incident_datetime", \
	                  "ent_datetime", "upd_datetime", "e911_time", "rec_time", "disp_time", \
	                  "enr_time", "arv_time", "transport_time", "booking_time", "clr_time", \
	                  "avg_lat", "avg_long" ]
		# Init CatsCorpus object
		cats_corpus = CatsCorpus()
		# Make input data iterable
		with open(text_path, "rb") as text_fhandle, open(cats_path, "rb") as cats_fhandle:
			# Building cats corpus by processing raw data
			print >> sys.stderr, "Building Cats Corpus."
			cats_corpus.build(text_fhandle, cats_fhandle, cats_def)


			
if __name__ == '__main__':
    unittest.main()