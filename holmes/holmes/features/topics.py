#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

from gensim.models.ldamodel import LdaModel

from holmes import catscorpus, utils

class TopicsFeature(catscorpus.CatsCorpus, utils.Config):
	"""
	
	"""

	def __init__(self, corpus_name, config_path=None, num_topics=10):
		if config_path:
			uitls.Config.__init__(config_path)
			corpus_path     = self.get_section(corpus_name)["corpus_path"]
			dictionary_path = self.get_section(corpus_name)["dictionary_path"]
			cats_path       = self.get_section(corpus_name)["cats_path"]
			interface.CatsCorpus.load(corpus_path, dictionary_path, cats_path)
		else:
			


		self.lda = LdaModel(corpus, num_topics=num_topics)
		