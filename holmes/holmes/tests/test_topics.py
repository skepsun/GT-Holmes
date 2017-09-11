#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import sys
import unittest
from holmes.catscorpus import CatsCorpus
from holmes.features.topics import TopicsFeature

class TopicsTestCase(unittest.TestCase):

	def test_training_lda(self):
		"""

		"""

		root_path       = "resource/lda_test"
		corpus_path     = "%s/%s" % (root_path, "corpus.mm") 
		dictionary_path = "%s/%s" % (root_path, "vocab.dict")
		cats_path       = "%s/%s" % (root_path, "cats")
		topic_feature   = TopicsFeature(corpus_path, dictionary_path, cats_path)
		print >> sys.stderr, "Corpus Loaded\n%s" % topic_feature

		root_path   = "resource/lda_test"
		lda_path    = "%s/%s" % (root_path, "lda_model")
		topics_path = "%s/%s" % (root_path, "lda_topics")

		# Train LDA model with randomly selected sub samples
		topic_feature.train_lda(num_samples=10000, num_topics=100, chunksize=500, \
			                    is_corpus_saved=True)
		# Save well-trained LDA model and converted topic vectors in local files
		topic_feature.save_lda(lda_path=lda_path, topics_path=topics_path)



if __name__ == '__main__':
    unittest.main()