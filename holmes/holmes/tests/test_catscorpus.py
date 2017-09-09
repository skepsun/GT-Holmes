#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
from holmes.catscorpus import CatsCorpus
from holmes.features.topics import TopicsFeature

class CatsCorpusTestCase(unittest.TestCase):
	"""
	"""

	def load_corpus(self):
		"""
		"""

		root_path       = "resource/cats_corpus"
		corpus_path     = "%s/%s" % (root_path, "corpus.mm") 
		dictionary_path = "%s/%s" % (root_path, "vocab.dict")
		cats_path       = "%s/%s" % (root_path, "cats")
		topic_feature   = TopicsFeature(corpus_path, dictionary_path, cats_path)
		print >> sys.stderr, "Corpus Loaded\n%s" % topic_feature
		return topic_feature
		
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
		# Serializing and saving built catscorpus in local files
		print >> sys.stderr, "Serializing and saving the corpus in local file."
		cats_corpus.save_corpus("resource/cats_corpus/corpus.mm", \
			             "resource/cats_corpus/vocab.dict", \
			             "resource/cats_corpus/cats")

	# @unittest.skip("Training LDA model is time-consuming.")
	def test_LDA(self):
		"""
		
		"""

		root_path   = "resource/lda"
		lda_path    = "%s/%s" % (root_path, "lda_model")
		topics_path = "%s/%s" % (root_path, "lda_topics")

		# Load test corpus from local files
		topic_feature = self.load_corpus()
		# Train LDA model with randomly selected sub samples
		topic_feature.train_lda()
		# Save well-trained LDA model and converted topic vectors in local files
		topic_feature.save_lda(lda_path=lda_path, topics_path=topics_path)

	@unittest.skip("Training LDA model is time-consuming.")
	def test_sub_LDA(self):
		"""

		"""

		root_path   = "resource/lda_test"
		lda_path    = "%s/%s" % (root_path, "lda_model")
		topics_path = "%s/%s" % (root_path, "lda_topics")

		# Load test corpus from local files
		topic_feature = self.load_corpus()
		# Train LDA model with randomly selected sub samples
		topic_feature.train_lda(num_samples=1000, num_topics=100, chunksize=50)
		# Save well-trained LDA model and converted topic vectors in local files
		topic_feature.save_lda(lda_path=lda_path, topics_path=topics_path)



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