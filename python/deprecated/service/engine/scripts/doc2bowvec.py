#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script is used to generate gensim's objects of dictionary and corpus from local text 
files. It would also save those substantiated objects as local files again for further using.

gensim's dictionary and corpus is a friendly way for processing text documents, which provides
various of helpful methods and decent NLP algorithm interface.
"""

from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from collections import defaultdict
from six import iteritems
import string
import arrow
import nltk
import sys
import re

class Documents(object):
	"""
	Documents is an utility class for preprocessing documents text in a memory-friendly way.
	It mainly provides an iterable way to load the documents and help substantiate gensim's
	dictionary and corpus.

	Essentially, a documents object is simply an iterable, where each iteration step yields 
	one document, then splits and formats their words by an unified standards. 
	"""

	def __init__(self, fname):
		self.fname    = fname
		self.fhandler = open(self.fname)
		self.index    = 0

	def __iter__(self):
		"""
        Iterate over the corpus, yielding one document at a time.
        """

		for line in self.fhandler:
			if self.index > 0 and self.index % 1000 == 0:
				print >> sys.stderr, "[%s] [Documents] %s docs have been processed." % (arrow.now(), self.index)
			yield self.tokenize(line)
			self.index += 1

	@staticmethod
	def tokenize(text):
		"""
		Tokenize each of the words in the text (one document).

		It utilizes nltk to help tokenize the sentences and the words in the text. 
		What needsto be noted is one document is consist of multiple remarks, which are delimited 
		by "/2" within the text.
		"""

		tokens = []
		# Remarks for each of the crimes are delimited by "\2"
		for remarks in text.strip("\n").split("\2"):
			# Free text part for each of the records are delimited by "\1"
			for remark in remarks.strip().split("\1"):
				# For every sentences in each of the free text part
				for sent in sent_tokenize(remark.decode("utf8")):
					# For every token
					for token in nltk.word_tokenize(sent.lower()):
						# Replace "-" with "_"
						tokens.append("_".join(token.split("-")))
		return tokens



if __name__ == "__main__":
	
	# Basic configuration
	# ---------------------------------------------------------------

	raw_text_path      = "tmp/woodie.validate_24_cases/corpus.txt"
	universe_dict_path = "resource/universe.dict"
	pruned_dict_path   = "resource/universe_pruned.dict"
	mm_corpus_path     = "resource/corpus.mm"



	# Create a new dictionary from raw text file
	# ---------------------------------------------------------------

	print >> sys.stderr, "[%s] Init document object from local file %s." % (arrow.now(), raw_text_path)
	docs = Documents(raw_text_path)

	print >> sys.stderr, "[%s] Creating dictionary." % arrow.now()
	dictionary = corpora.Dictionary([ doc for doc in docs ])
	print >> sys.stderr, "[%s] Saving dictionary at %s." % (arrow.now(), universe_dict_path)
	dictionary.save(universe_dict_path)



	# Load and prune existed dictionary from dict file 
	# ---------------------------------------------------------------

	print >> sys.stderr, "[%s] Loading existed dictionary" % arrow.now()
	dictionary = corpora.Dictionary()
	dictionary = dictionary.load(universe_dict_path)
	print dictionary

	print >> sys.stderr, "[%s] Removing stopwords, words that appear only once, and other non-words" % arrow.now()
	non_ids  = [ tokenid for token, tokenid in iteritems(dictionary.token2id) if not re.match("^[A-Za-z_]*$", token) ]
	once_ids = [ tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1 ]
	stop_ids = [ dictionary.token2id[stopword] for stopword in stopwords.words("english") if stopword in dictionary.token2id ]
	dictionary.filter_tokens(stop_ids + once_ids + non_ids)
	# remove gaps in id sequence after words that were removed
	dictionary.compactify()
	print dictionary

	print >> sys.stderr, "[%s] Saving dictionary at %s." % (arrow.now(), pruned_dict_path)
	dictionary.save(pruned_dict_path)



	# Create a new corpus based on the raw text file and a dictionary
	# ---------------------------------------------------------------

	print >> sys.stderr, "[%s] Init document object from local file %s." % (arrow.now(), raw_text_path)
	docs = Documents(raw_text_path)
	corpus = [dictionary.doc2bow(doc) for doc in docs]

	print >> sys.stderr, "[%s] Saving corpus at %s." % (arrow.now(), mm_corpus_path)
	corpora.MmCorpus.serialize(mm_corpus_path, corpus)



