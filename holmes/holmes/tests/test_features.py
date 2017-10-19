#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import sys
import arrow
import unittest
from holmes.catscorpus import CatsCorpus
from holmes.feature import Feature

# Root path of the input corpus
root_path = "resource/220klabeled.corpus"
# root_path = "resource/6labeled.corpus"

class FeaturesTestCase(unittest.TestCase):

	def test_LDA(self):
		"""
		
		"""

		# Initializing LDA feature
		lda_feature  = Feature(root_path, is_tfidf=True)
		print >> sys.stderr, "[%s] Corpus Loaded.\n%s" % (arrow.now(), lda_feature)

		lda_path    = "%s/%s" % (root_path, "lda_model")
		output_path = "%s/%s" % (root_path, "lda_output")

		# Train LDA model with randomly selected sub samples
		lda_feature.train_lda(num_topics=20, chunksize=500)
		print >> sys.stderr, "[%s] LDA model is well-trained." % arrow.now()
		# Save well-trained LDA model and converted topic vectors in local files
		lda_feature.save_lda(model_path=lda_path, output_path=output_path)
		print >> sys.stderr, "[%s] LDA model and its outcome has been saved." % arrow.now()

	def test_LSI(self):
		"""
		
		"""

		# Initializing LSI feature
		lsi_feature  = Feature(root_path, is_tfidf=True)
		print >> sys.stderr, "[%s] Corpus Loaded.\n%s" % (arrow.now(), lsi_feature)

		lsi_path    = "%s/%s" % (root_path, "lsi_model")
		output_path = "%s/%s" % (root_path, "lsi_output")

		# Train LSI model with randomly selected sub samples
		lsi_feature.train_lsi(num_components=20, chunksize=500)
		print >> sys.stderr, "[%s] LSI model is well-trained." % arrow.now()
		# Save well-trained LSI model and converted projections vectors in local files
		lsi_feature.save_lsi(model_path=lsi_path, output_path=output_path)
		print >> sys.stderr, "[%s] LSI model and its outcome has been saved." % arrow.now()



if __name__ == "__main__":
    unittest.main()