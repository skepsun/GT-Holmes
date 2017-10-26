#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains basic interface used throught the whole holmes package.

The interfaces are realized as abstract base classes for the basic natural language
processing. 
"""

from scipy.sparse import csc_matrix
from gensim import corpora, models
from nltk.util import ngrams
from six import iteritems
import numpy as np
import itertools
import string
import pickle
import random
import arrow
import nltk
import copy
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

class Documents(object):
	"""
	Documents is a simple class for: 
	1. preprocessing documents text in a memory-friendly way.
	2. outputting tokenized terms of each of the documents iteratively. 

	It's mainly used to load the documents and help substantiate gensim's dictionary and 
	corpus.

	Essentially, a documents object is simply an iterable, where each iteration step yields 
	one document, then splits and formats their words by an unified and standard method. 
	"""

	def __init__(self, iter_object, n=1, pad_right=False, pad_left=False, \
		         left_pad_symbol=None, right_pad_symbol=None):
		self.iter_object = iter_object
		self.counter     = 0
		self.n           = n
		self.pad_right   = pad_right
		self.pad_left    = pad_left
		self.left_pad_symbol  = left_pad_symbol
		self.right_pad_symbol = right_pad_symbol

	def __iter__(self):
		"""
        Iterate over the corpus, yielding one line (document) at a time.
        """

		for line in self.iter_object:
			if self.counter > 0 and self.counter % 1000 == 0:
				print >> sys.stderr, "[%s] [Documents] %s docs have been processed." % \
				         (arrow.now(), self.counter)
			try:
				yield self.tokenize(line, N=self.n, \
					                pad_right=self.pad_right, pad_left=self.pad_left, \
					                left_pad_symbol=self.left_pad_symbol, \
					                right_pad_symbol=self.right_pad_symbol)
			# Yield empty token list if tokenization failed as UnicodeDecodeError was raised
			except UnicodeDecodeError as e:
				print >> sys.stderr, "[%s] [Documents] No. %s doc raise expection: %s." % \
				         (arrow.now(), self.counter, e)
				yield []

			self.counter += 1

	@staticmethod
	def tokenize(text_string, N=1, pad_right=False, pad_left=False, \
		         left_pad_symbol=None, right_pad_symbol=None):
		"""
		Tokenize each of the words in the text (one document).

		It utilizes nltk to help tokenize the sentences and the words in the text. 
		What needsto be noted is one document is consist of multiple remarks, which are  
		delimited by "/1" within the text.
		
		Also, parameters of ngrams module, like n, pad_right, pad_left, left_pad_symbol, and
		right_pad_symbol, are optional to input. 
		"""

		ngram_tokens = []
		# Free text part for each of the records are delimited by "\1"
		for remark in text_string.strip().split("\1"):
			# For every sentences in each of the free text part
			for sent in nltk.tokenize.sent_tokenize(remark.encode('utf-8').strip()):
				# Tokenize a sentence by english word level of granularity
				tokens_in_sentence = [ 
					token
					for token in nltk.word_tokenize(sent.translate(None, string.punctuation).lower()) 
					if token not in nltk.corpus.stopwords.words("english")]
				# Calculate all the grams terms from unigram to N-grams
				for n in range(1, N+1):
					# Calculate ngram of a tokenized sentence
					ngram_tokens_in_sentence = [ 
						"_".join(ngram_tuple)
						for ngram_tuple in \
							list(ngrams(tokens_in_sentence, n, pad_right=pad_right, pad_left=pad_left, \
								        left_pad_symbol=left_pad_symbol, \
								        right_pad_symbol=right_pad_symbol)) ]
					# Append ngrams terms to the list
					ngram_tokens += ngram_tokens_in_sentence
		return ngram_tokens



class CatsCorpus(object):
	"""
	CaTS Corpus

	CaTS (Categoried Temporal Spatial) Corpus is a base class for handling basic corpus 
	operations. It defines several basic components for a corpus, which includes a dictionary,
	a sequential BoW corpus, and the <categoried, temporal, spatial> information tuples in the 
	same order. You can build your personal Cats corpus from scratch by processing raw text and 
	other data files, otherwise you need to load an existed cats corpus. 
	"""

	def __init__(self, root_path=None):

		self.tfidf = None
		# Non-sampling for original corpus
		self.sampling_flag = False
		# Load existed corpus if the params are not None
		if root_path:
			self.load_corpus(root_path)
			# self.csc_corpus = self._csc_corpus()
			self.tfidf = models.TfidfModel(self.corpus)[self.corpus]
			
		

	def build(self, text_iter_obj, cats_iter_obj, cats_def=None, min_term_freq=1, \
		      n=1, pad_right=False, pad_left=False, left_pad_symbol=None, right_pad_symbol=None):
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
		3. cats_def: is the definition of the fields of the CaTS information. It is required to be a 
		   list, each of the elements is a brief description of the corresponding field.
		4. min_term_freq: will keep the terms whose times of apperance are greater than this minimum 
		   number of the terms.
		5. n, pad_right, pad_left, left_pad_symbol, right_pad_symbol:
		   are the parameters of Documents class.
		"""

		# Init document object by loading an iterable object (for reading text iteratively),
		# the iterable object could be a file handler, or standard input handler and so on
		docs = Documents(text_iter_obj, n=n, pad_right=pad_right, pad_left=pad_left, \
						 left_pad_symbol=left_pad_symbol, \
						 right_pad_symbol=right_pad_symbol)
		# TODO: Make it more memory friendly
		docs = [ doc for doc in docs ]
		# Build dictionary based on the words appeared in documents
		self.dictionary = corpora.Dictionary(docs)
		# Remove non-character and low-frequency terms in the dictionary
		nonchar_ids = [ tokenid for token, tokenid in iteritems(self.dictionary.token2id) \
		                if not re.match("^[A-Za-z_]*$", token) ]
		lowfreq_ids = [ tokenid for tokenid, docfreq in iteritems(self.dictionary.dfs) \
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
		# Remove empty documents
		self._clean_corpus()
		# Calculate tfidf matrix
		self.tfidf = models.TfidfModel(self.corpus)
		# self.csc_corpus = self._csc_corpus()

		print >> sys.stderr, self.dictionary
		print >> sys.stderr, "The size of the corpus is %d" % len(self.corpus)

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
		# TODO: 
		# self.dictionary.add_documents([Documents.tokenize(doc_text)])
		# Update corpus
		for doc in Documents(text_iter_obj):
			self.corpus.append(self.dictionary.doc2bow(doc))
		# Update cats tuples collection
		for cats_tuple in cats_iter_obj:
			self.cats["collections"].append(cats_tuple.strip("\n").split("\t"))

	# def _csc_corpus(self):
	# 	"""
	# 	Corpus in Compressed Sparse Column Matrix Format

	# 	Return the corpus of the object in Compressed Sparse Column Matrix Format. This format also 
	# 	supports to be converted to numpy array by calling 'csc_matrix.toarray()'.
		
	# 	In order to accelarate the process of getting csc_corpus after the first request. This function
	# 	would do the computation only once at the first request for the csc_corpus, and save the 
	# 	result in a private member.
	# 	"""

	# 	if self.csc_corpus is None:
	# 		doc_ind  = 0  # Index of documents in corpus
	# 		row_inds = [] # The list of indexs of rows (means docs) in csc matrix
	# 		col_inds = [] # The list of indexs of columns (means terms) in csc matrix
	# 		vals     = [] # The list of nonzero values in csc matrix

	# 		for doc in self.corpus:
	# 			row_inds += [ doc_ind for _ in range(len(doc)) ]
	# 			col_inds += [ term_ind for term_ind, freq in doc ]
	# 			vals     += [ freq for term_ind, freq in doc ]
	# 			doc_ind  += 1

	# 		self.csc_corpus = csc_matrix((vals, (row_inds, col_inds)), 
	# 			shape=(len(self.corpus), len(self.dictionary)))

	def load_corpus(self, root_path):
		"""
		Load
		
		Read dataset from local files and load them into objects (dictionary, corpus and cats) 
		respectively.
		"""

		# Persist the path information
		self.root_path  = root_path
		# Load dictionary
		self.dictionary = corpora.Dictionary()
		self.dictionary = self.dictionary.load("%s/%s" % (root_path, "vocab.dict"))
		# Load corpus text and convert it to bow list
		self.corpus     = [ doc_bow 
			for doc_bow in corpora.MmCorpus("%s/%s" % (root_path, "corpus.mm")) ]
		# Load cats tuples collection
		with open("%s/%s" % (root_path, "cats.txt"), "r") as h:
			self.cats = pickle.load(h)

	def save_corpus(self, root_path=None):
		"""
		Save

		Persist corpus and dictionary and other basic information at local file system. 
		Corpus is in the Matrix Market format. The file format of the dictionary is defined
		by Gensim.Dictionary. Other basic information (including categories and other features) 
		would be serialized by pickle.
		"""

		if self.sampling_flag:
			print >> sys.stderr, "The current corpus is incomplete (sampled), saving operation is not allowed."
			return
		
		if root_path is not None:
			# Persist dictionary
			self.dictionary.save("%s/%s" % (root_path, "vocab.dict"))
			# Persist corpus text
			corpora.MmCorpus.serialize("%s/%s" % (root_path, "corpus.mm"), self.corpus)
			# Persist cats tuples collection by pickle
			with open("%s/%s" % (root_path, "cats.txt"), "wb") as h:
				pickle.dump(self.cats, h)

	def save_cats(self, cats_folder_path):
		"""
		"""

		# Persist cats tuples collection by pickle
		if cats_folder_path is not None:
			with open("%s/%s" % (cats_folder_path, "cats.txt"), "wb") as h:
				pickle.dump(self.cats, h)

	def category_sampling(self, categories):
		"""
		Category Sampling

		Select the documents whose categories are included in the specific categories list.
		"""

		all_categories = self.categories()
		indices        = [ ind for ind, category in enumerate(all_categories) if C in categories ]
		self.corpus    = self.corpus[indices, :]
		self.tfidf     = models.TfidfModel(self.corpus)[self.corpus]
		# Set sampling falg as True for indicating the current corpus is incomplete.
		self.sampling_flag = True


	def random_sampling(self, num_samples):
		"""
		Random Sampling
		
		Randomly select and keep specific number of samples from the dataset.
		"""

		if num_samples < len(self.corpus):
			self.corpus, self.cats["collections"] = zip(*random.sample(
				list(zip(self.corpus, self.cats["collections"])), num_samples))
			self.tfidf = models.TfidfModel(self.corpus)[self.corpus]
			# Set sampling flag as True, for indicating the current corpus is not
			# the original one.
			self.sampling_flag = True

	def categories(self):
		"""
		Categories

		Return the list of categories corresponding to the documents in the corpus
		"""

		category_ind = self.cats["definitions"].index("C")
		return np.array(self.cats["collections"])[:, category_ind].tolist()

	def _clean_corpus(self):
		"""
		Clean Corpus

		This function would remove empty documents and their according cats tuples. 
		"""

		clean_corpus = []
		clean_cats   = []
		for doc_bow, cats_tuple in itertools.izip(self.corpus, self.cats["collections"]):
			if len(doc_bow) > 0:
				clean_corpus.append(doc_bow)
				clean_cats.append(cats_tuple)
			else: 
				print >> sys.stderr, "Empty document is discarded."
		self.corpus              = clean_corpus
		self.cats["collections"] = clean_cats

	# def __add__(self, other):
	# 	"""
	# 	Overloading addition operation for cats objects
	# 	"""
	# 	if len(self.cats["definitions"]) is not len(other.cats["definitions"]):
	# 		raise Exception("The cats definitions of two cats object are different.")
	# 	corpus_obj = CatsCorpus()
	# 	corpus_obj.corpus = self.corpus + other.corpus
	# 	corpus_obj.cats["collections"] = self.cats["collections"] + other.cats["collections"]
	# 	return corpus_obj

	def __len__(self):
		"""
		Return the size of the corpus (the number of the documents)
		"""
		return len(self.corpus)

	def __str__(self):
		"""
		Return the details of the cats corpus object
		"""
		return "<Cats Corpus Object>\nDictionary:\t%s\nCorpus Size:\t%s\nCATS Info:\n  Collections size:\t%s\n" % \
		       (self.dictionary, len(self.corpus), len(self.cats["collections"]))
