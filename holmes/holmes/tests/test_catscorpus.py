#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
from holmes.catscorpus import CatsCorpus

class CatsCorpusTestCase(unittest.TestCase):
	"""
	"""

	def test_building_corpus(self):
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
		# Serializing and saving built catscorpus in local files
		print >> sys.stderr, "Serializing and saving the corpus in local file."
		cats_corpus.save("resource/cats_corpus/corpus.mm", \
			             "resource/cats_corpus/vocab.dict", \
			             "resource/cats_corpus/cats")

	# def test_upper(self):
	# 	self.assertEqual('foo'.upper(), 'FOO')

	# def test_isupper(self):
	# 	self.assertTrue('FOO'.isupper())
	# 	self.assertFalse('Foo'.isupper())

	# def test_split(self):
	# 	s = 'hello world'
	# 	self.assertEqual(s.split(), ['hello', 'world'])
	# 	# check that s.split fails when the separator is not a string
	# 	with self.assertRaises(TypeError):
	# 		s.split(2)

if __name__ == '__main__':
    unittest.main()