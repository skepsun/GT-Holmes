#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains basic interface used throught the whole holmes package.

The interfaces are realized as abstract base classes for the basic natural language
processing. 
"""

from gensim import corpora
import itertools
import string
import pickle
import arrow
import nltk
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class Documents(object):
	"""
	Documents is a simple class for: 
	1. preprocessing documents text in a memory-friendly way.
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
				         (arrow.now(), self.counter)
			try:
				yield self.tokenize(line)
			except UnicodeDecodeError as e:
				print >> sys.stderr, "[%s] [Documents] No. %s doc raise expection: %s." % \
				         (arrow.now(), self.counter, e)
				yield ""

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
		for remark in text_string.strip().split("\1"):
			# For every sentences in each of the free text part
			for sent in nltk.tokenize.sent_tokenize(remark):
				# For every token
				for token in nltk.word_tokenize(sent.lower()):
					# Remove punctuations and stopwords
					if token not in nltk.corpus.stopwords.words('english') and \
					   token not in string.punctuation:
						tokens.append(token)
		return tokens



class CatsCorpus(object):
	"""
	CaTS Corpus

	CaTS (Categoried Temporal Spatial) Corpus is a base class for handling basic corpus 
	operations. It defines several basic components for a corpus, which includes a dictionary,
	a sequential text corpus, and the <categoried, temporal, spatial> information tuples in the 
	same order. You can build your personal Cats corpus from scratch by processing raw text and 
	other data files, otherwise you need to load an existed cats corpus. 
	"""

	def __init__(self, corpus_path=None, dictionary_path=None, cats_path=None):
		# Load existed corpus if the params are not None
		if corpus_path and dictionary_path and cats_path:
			self.load(corpus_path, dictionary_path, cats_path)

	def build(self, text_iter_obj, cats_iter_obj, cats_def=None, min_term_freq=2):
		"""
		Build

		Building a new Cats corpus. It would process the documents in the raw text file interatively 
		by handing a iterable object "text_iter_obj". It requires each line of the raw text file only
		contains a single document. During the mean time, the function would generate a dictionary file 
		which contains all the non-stop english words (vocabulary) appeared in the corpus at least 
		"min_term_freq" times. It contributes to less storage space for corpus and easier/faster 
		corpus operations. 

		Params: 
		1. text_iter_obj: is a streaming data handler. It could be a file handler or a stdin handler. 
		   The content it yield each time is supposed to be a single line of string (without "\"). 
		2. cats_iter_obj: is a streaming data handler. It could be a file handler or a stdin handler. 
		   The content it yield each time is supposed to be a tuple of information delimited by tabs
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
		self.corpus = [ self.dictionary.doc2bow(doc) for doc in docs ]
		# Build Cats tuples collection
		self.cats   = { "collections": [ cats_tuple.strip("\n").split("\t") for cats_tuple in cats_iter_obj ] }
		if type(cats_def) is list and len(cats_def) == len(self.cats["collections"]):
			self.cats["definitions"] = cats_def

	def add_documents(self, text_iter_obj, cats_iter_obj):
		"""
		Add documents

		Update corpus by adding new documents to the existed dataset. Specifically this function 
		would firstly update existed dictionary, then convert the upcoming documents to bag of words 
		according to the new dictionary and add them to the existed corpus, finally append new cats 
		information to the cats tuples collection.

		Notes: it would be better to rebuild the whole corpus after adding a certain amount of new 
		documents. Because the updated dictionary would contain some low-frequency vocabulary which 
		need to be pruned. However, the added documents have been turned into bow by the unpruned 
		dictionary.
		"""

		# Update dictionary
		self.dictionary.add_documents([Documents.tokenize(doc_text)])
		# Update corpus
		for doc in Documents(text_iter_obj):
			self.corpus.append(self.dictionary.doc2bow(doc))
		# Update cats tuples collection
		for cats_tuple in cats_iter_obj:
			self.cats["collection"].append(cats_tuple.strip("\n").split("\t"))

	def load(self, corpus_path, dictionary_path, cats_path):
		"""
		Load
		
		Read dataset from local files and load them into objects (dictionary, corpus and cats) 
		respectively.
		"""

		# Load dictionary
		self.dictionary = corpora.Dictionary()
		self.dictionary = self.dictionary.load(dictionary_path)
		# Load corpus text and convert it to bow list
		self.corpus     = [ bow for bow in corpora.MmCorpus(corpus_path) ]
		# Load cats tuples collection
		with open(cats_path, "r") as h:
			self.cats = pickle.load(h)

	def save(self, corpus_path, dictionary_path, cats_path):
		"""
		Save

		Persist corpus and dictionary and other basic information at local file system. 
		Corpus is in the Matrix Market format. The file format of the dictionary is defined
		by Gensim.Dictionary. Other basic information (including categories and other features) 
		would be serialized by pickle.
		"""

		# Persist dictionary
		self.dictionary.save(dictionary_path)
		# Persist corpus text
		corpora.MmCorpus.serialize(corpus_path, self.corpus)
		# Persist cats tuples collection by pickle
		with open(cats_path, "wb") as h:
			pickle.dump(self.cats, h)

	def _clean_corpus(self):
		"""
		Clean Corpus

		This function would remove empty documents and their according cats tuples. 
		"""

		clean_corpus = []
		clean_cats   = []
		for bow, cats_tuple in itertools.izip(self.corpus, self.cats["collection"]):
			if len(bow) > 0:
				clean_corpus.append(bow)
				clean_cats.append(cats_tuple)
		self.corpus             = clean_corpus
		self.cats["collection"] = clean_cats

	def __len__(self):
		"""
		Return the size of the corpus (the number of the documents)
		"""
		return len(self.corpus)

	def __str__(self):
		return "%s\n%s\n%s" % (self.dictionary, self.corpus, self.cats["definitions"])
