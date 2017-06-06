#!/usr/local/bin/python

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import LatentDirichletAllocation
# from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from os import listdir
import string
import nltk
import sys

class MetaTokenizer:

	def __init__(self):


	def _get_sents_by_words(self, text):
		sentences = []
		# - Remarks for each of the crimes are delimited by '\2'
		for remarks in text.strip('\n').split('\2'):
			# - Free text part for each of the records are delimited by '\1'
			for remark in remarks.strip().split('\1'):
				# - For every sentences in each of the free text part
				for sent in sent_tokenize(remark.decode("utf8")):
					# - Split the text into words
					# - Remove uppercases
					# - Remove punctuation
					sentence = [
						'_'.join(word.split('-'))
						for word in nltk.word_tokenize(sent.lower())
						if word not in string.punctuation
					]
					sentences.append(sentence)
		return sentences

        
