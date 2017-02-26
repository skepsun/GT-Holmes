#!/usr/local/bin/python
from gensim.models import Word2Vec
from collections import Counter
from nltk.corpus import stopwords
import numpy as np
import string
import json
import sys
import re

from lib.narratives.text import Text

# def FeatureTextInCategory(word2vec_model, phrases_extractor, text, words_category):
# 	# Deprecated: 
# 	# words_count = dict(Counter(re.findall(r'\w+', text)))

# 	sents_by_words = GetSentsByWords(text)
# 	# Take interested phrases from the text into consideration
# 	phrases_info   = phrases_extractor.phrases_info(text) # Get all possible phrases from the text
# 	mwe = MWETokenizer()
# 	for p in phrases_count.keys():
# 		mwe.add_mwe(str(p).split('_'))
# 	# Get tokens from the text
# 	# The sents_by_tokens tokenize the text as words and phrases, 
# 	# and also preserve the sentences structure. 
# 	sents_by_tokens = []
# 	for sent in sents_by_words:
# 		sent_by_tokens = [
# 			token
# 			for token in mwe.tokenize(sent)
# 		]
# 		sents_by_tokens.append(sent_by_tokens)

# 	print >> sys.stderr, sents_by_tokens
	# Words count dictionary
	# tokens_count = dict(Counter(tokens))
	# Remove words with insufficent length in text.
	# for word in words_count.keys():
	# 	if len(word) < WORD_MIN_LEN:
	# 		words_count.pop(word, None)
	# Remove stop words in text
	# for token in tokens_count.keys():
	# 	if token in stopwords.words('english'):
	# 		tokens_count.pop(token, None)
	
	# Merge two dictionaries into item dict
	# items_count   = words_count.copy()
	# items_count.update(phrases_count)

def FeatureDict2FeatureVector(words_category, feature_dict, threshold):
	feature_vector = np.zeros(0)
	for category, pairs in feature_dict.iteritems():
		category_vector = np.zeros(len(words_category[category]))
		for pair in pairs:
			category_word_index = words_category[category].index(pair['in_category'])
			# If the item is a word
			if (not isPhrase(pair['in_category'])) and pair['distance'] >= threshold and \
			   category_vector[category_word_index] < pair['distance']:
				category_vector[category_word_index] = pair['distance'] * pair['count']
			# If the item is a phrase
			elif isPhrase(pair['in_category']) and \
			   category_vector[category_word_index] < pair['distance']:
				category_vector[category_word_index] = pair['distance'] # * pair['count']
		feature_vector = np.concatenate((feature_vector, category_vector))
	return feature_vector.tolist()

if __name__ == '__main__':

	json_feature_path      = sys.argv[1]
	text_index             = int(sys.argv[2]) # The index for the text feature (default = 14)
	threshold = 0.5

	text_features = {'features': []}
	# Process the data stream from stdin
	for line in sys.stdin:
		data = line.strip('\n').split('\t')
		if len(data) < text_index:
			print >> sys.stderr, '[ERROR] data: [%s] is insufficient.' % line
			continue
		
		# Text Feature:
		remarks = data[text_index]
		t = Text(remarks)