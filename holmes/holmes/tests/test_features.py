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
root_path = "resource/56labeld+500random.corpus"
# root_path = "resource/6labeled.corpus"

class FeaturesTestCase(unittest.TestCase):

	@unittest.skip("Skipping LDA test")
	def test_LDA(self):
		"""
		
		"""

		# Initializing LDA feature
		lda_feature = Feature(root_path, is_tfidf=True)
		print >> sys.stderr, "[%s] Corpus Loaded.\n%s" % (arrow.now(), lda_feature)

		lda_path    = "%s/%s" % (root_path, "lda_model")
		output_path = "%s/%s" % (root_path, "lda_output")

		# Train LDA model with randomly selected sub samples
		lda_feature.encoder_lda(num_topics=1000, chunksize=20)
		print >> sys.stderr, "[%s] LDA model is well-trained." % arrow.now()
		# Save well-trained LDA model and converted topic vectors in local files
		lda_feature.save_lda(model_path=lda_path, output_path=output_path)
		print >> sys.stderr, "[%s] LDA model and its outcome has been saved." % arrow.now()

	@unittest.skip("Skipping LSI test")
	def test_LSI(self):
		"""
		
		"""

		# Initializing LSI feature
		lsi_feature = Feature(root_path, is_tfidf=True)
		print >> sys.stderr, "[%s] Corpus Loaded.\n%s" % (arrow.now(), lsi_feature)

		lsi_path    = "%s/%s" % (root_path, "lsi_model")
		output_path = "%s/%s" % (root_path, "lsi_output")

		# Train LSI model with randomly selected sub samples
		lsi_feature.encoder_lsi(num_components=1000, chunksize=20)
		print >> sys.stderr, "[%s] LSI model is well-trained." % arrow.now()
		# Save well-trained LSI model and converted projections vectors in local files
		lsi_feature.save_lsi(model_path=lsi_path, output_path=output_path)
		print >> sys.stderr, "[%s] LSI model and its outcome has been saved." % arrow.now()

	# @unittest.skip("Skipping GBRBM test")
	def test_GBRBM(self):
		"""
		"""

		rbm_feature = Feature(root_path, is_tfidf=True)
		print >> sys.stderr, "[%s] Corpus Loaded.\n%s" % (arrow.now(), rbm_feature)

		rbm_path    = "%s/%s" % (root_path, "rbm_model")
		output_path = "%s/%s" % (root_path, "rbm_output")

		# # # Sampling from raw data
		# sample_size = 10000
		# rbm_feature.random_sampling(sample_size)
		# rbm_feature.save_cats(output_path)
		# print >> sys.stderr, "[%s] Sampled %d cases." % (arrow.now(), sample_size)

		rbm_feature.encoder_gbrbm(n_hidden=5000, lr=0.005, n_epoches=30, batch_size=20)
		print >> sys.stderr, "[%s] GBRBM model is well-trained." % arrow.now()

		rbm_feature.save_gbrbm(model_path=rbm_path, output_path=output_path)
		print >> sys.stderr, "[%s] GBRBM model and its outcome has been saved." % arrow.now()



if __name__ == "__main__":
    unittest.main()