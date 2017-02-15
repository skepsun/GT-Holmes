#!/usr/local/bin/python

from collections import Counter
from nltk.corpus import stopwords
import string
import nltk

WORD_MIN_LEN = 3

def WordsCounter(text):
	# Replace the delimiter with stops.
	text = '. '.join(text.strip('\n').split('\2'))
	text = '. '.join(text.strip().split('\1'))
	# Get words from the text
	words = [
		word 
		for word in nltk.word_tokenize(text.lower())
		if word not in string.punctuation
	]
	# Words count dictionary
	words_count = dict(Counter(words))
	# Remove words with insufficent length in text.
	for word in words_count.keys():
		if len(word) < WORD_MIN_LEN:
			words_count.pop(word, None)
	# Remove stop words in text
	for word in words_count.keys():
		if word in stopwords.words('english'):
			words_count.pop(word, None)
	return words_count