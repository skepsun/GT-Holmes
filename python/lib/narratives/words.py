#!/usr/local/bin/python

# from gensim.models import Word2Vec
# from collections import Counter
# from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import string
import nltk
import sys

class WordsAnalysor:

	def __init__(self, text):
		self.text = text
		self.sents_by_words = self._get_sents_by_words()


	def _get_sents_by_words(self):
		sentences = []
		# - Remarks for each of the crimes are delimited by '\2'
		for remarks in self.text.strip('\n').split('\2'):
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

	

	# def WordsCounter(text):
	# 	# Get words from the text
	# 	words = GetSentsByWords(text)
	# 	# Words count dictionary
	# 	words_count = dict(Counter(words))
	# 	# Remove words with insufficent length in text.
	# 	for word in words_count.keys():
	# 		if len(word) < WORD_MIN_LEN:
	# 			words_count.pop(word, None)
	# 	# Remove stop words in text
	# 	for word in words_count.keys():
	# 		if word in stopwords.words('english'):
	# 			words_count.pop(word, None)
	# 	return words_count