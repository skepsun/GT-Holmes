#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains basic interface used throught the whole holmes package.

The interfaces are realized as abstract base classes for the basic natural language
processing. 
"""

from gensim import corpora, models
# from collections import defaultdict
# from six import iteritems
import string
import arrow
import nltk
import sys

from holmes import utils

class Documents(object):
	"""
	Documents is a simple class for 1. preprocessing documents text in a memory-friendly way.
	2. outputting tokenized terms of each of the documents iteratively. 

	It's mainly used to be the load the documents and help substantiate gensim's
	dictionary and corpus.

	Essentially, a documents object is simply an iterable, where each iteration step yields 
	one document, then splits and formats their words by an unified and standard method. 
	"""

	def __init__(self, iter_object):
		self.iter_object = iter_object
		self.counter     = 0

	def __iter__(self):
		"""
        Iterate over the corpus, yielding one line (document) at a time.
        """

		for line in self.iter_object:
			if self.counter > 0 and self.counter % 1000 == 0:
				print >> sys.stderr, "[%s] [Documents] %s docs have been processed." % \
				         (arrow.now(), self.index)
			yield self.tokenize(line)
			self.counter += 1

	@staticmethod
	def tokenize(text_string):
		"""
		Tokenize each of the words in the text (one document).

		It utilizes nltk to help tokenize the sentences and the words in the text. 
		What needsto be noted is one document is consist of multiple remarks, which are  
		delimited by "/2" within the text.
		"""

		tokens = []
		# Free text part for each of the records are delimited by "\1"
		for remark in text_string.decode("utf8").strip().split("\1"):
			# For every sentences in each of the free text part
			for sent in nltk.tokenize.sent_tokenize(remark):
				# For every token
				for token in nltk.word_tokenize(sent.lower()):
					# Remove punctuations and stopwords
					if token not in nltk.corpus.stopwords.words('english') and \
					   token not in string.punctuation:
						tokens.append(token)
		return tokens



class CategoriedTemporalCorpus(object):
	"""
	"""

	def __init__(self, ):
		pass

	def build(text_iter_obj, min_term_freq=2):
		"""
		"""

		# Init document object by loading an iterable object (for reading text iteratively),
		# the iterable object could be a file handler, or standard input handler and so on
		docs            = Documents(text_iter_obj)
		# Build dictionary based on the words appeared in documents
		self.dictionary = corpora.Dictionary([ doc for doc in docs ])
		# Remove non-character and low-frequency terms in the dictionary
		nonchar_ids = [ tokenid for token, tokenid in iteritems(dictionary.token2id) \
		                if not re.match("^[A-Za-z_]*$", token) ]
		lowfreq_ids = [ tokenid for tokenid, docfreq in iteritems(dictionary.dfs) \
		                if docfreq <= min_term_freq ]
		self.dictionary.filter_tokens(lowfreq_ids + nonchar_ids)
		# Remove gaps in id sequence after some of the words being removed
		self.dictionary.compactify()
		# Build corpus (numeralize the documents and only keep the terms that exist in dictionary)
		self.corpus = [dictionary.doc2bow(doc) for doc in docs]

	def load_mm():
		pass

	def save_():
		pass



class BagOfWords():

	def __init__(self, config_path):
		# self.config = utils.Config(config_path)
		# pruned_dict_path      = conf.config_section_map("Corpus")["pruned_dict_path"]
		# mm_corpus_path        = conf.config_section_map("Corpus")["mm_corpus_path"]
		# crime_codes_desc_path = conf.config_section_map("Corpus")["crime_codes_desc_path"]
		# code_list_path        = conf.config_section_map("Corpus")["labels_path"]
		pass



if __name__ == "__main__":
	import sys
	d = Documents(sys.stdin)
	for doc in d:
		print doc

