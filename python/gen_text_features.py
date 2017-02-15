#!/usr/local/bin/python
from gensim.models import Word2Vec
import numpy as np
# import heapq
import json
import sys
import re

from lib.phrases import PhrasesExtractor, PhrasesSimilarity, isPhrase
from lib.words import WordsCounter

def FeatureTextInCategory(word2vec_model, phrases_extractor, text, words_category):
	# Deprecated: 
	# words_count = dict(Counter(re.findall(r'\w+', text)))

	# Get the count of words and phrases
	words_count   = WordsCounter(text)
	phrases_count = phrases_extractor.phrases_counter(text)
	# Merge two dictionaries into item dict
	items_count   = words_count.copy()
	items_count.update(phrases_count)
	# Init feature dict
	feature = {}
	for category in words_category.keys():
		feature[category] = []
	# Calculate the distance between every word/phrase in the text and category
	for category, words_in_category in words_category.iteritems():
		items_in_text     = items_count.keys()
		items_in_category = map(lambda x: x.encode('ascii', 'ignore'), words_in_category)
		# Calculate the matrix of distances between 
		# words_in_text & words_in_category
		len_i_t  = len(items_in_text)
		len_i_c  = len(items_in_category)
		dist_mat = np.zeros((len_i_t, len_i_c))
		for i in range(len_i_t):
			for j in range(len_i_c):
				try:
					if isPhrase(items_in_text[i]) and isPhrase(items_in_category[j]):
						dist_mat[i, j] = PhrasesSimilarity(word2vec_model, items_in_text[i], items_in_category[j])
					elif (not isPhrase(items_in_text[i])) and (not isPhrase(items_in_category[j])):
						dist_mat[i, j] = word2vec_model.similarity(items_in_text[i], items_in_category[j])
					else:
						dist_mat[i, j] = 0
				except KeyError:
					dist_mat[i, j] = -1
		# Find the best matched words in the category for each of words in text
		best_matched_indexs = dist_mat.argmax(axis=1) # The index of the best matched words
		best_matched_dists  = []                      # The distance between the best matched words and the words in text
		for i in range(len(best_matched_indexs)):
			best_matched_dists.append(dist_mat[i, best_matched_indexs[i]])
		best_matched_dists = np.array(best_matched_dists)
		# Find K-nearest words (to the current category) in the text 
		K = 10
		for k in range(K):
			i = best_matched_dists.argmax() # The index of the words in text which has the highest similarity
			j = best_matched_indexs[i]
			# If the current best matched distance is lower than o, then abandon it.
			if best_matched_dists[i] <= 0:
				break
			best_matched_dists[i] = -1      # Remove the largest value in the best_matched_dists
			feature[category].append({
				'in_text':     items_in_text[i],
				'in_category': items_in_category[j],
				'count':       items_count[items_in_text[i]],
				'distance':    dist_mat[i, j]
			})
	return feature

def FeatureDict2FeatureVector(words_category, feature_dict):
	feature_vector = np.zeros(0)
	for category, pairs in feature_dict.iteritems():
		category_vector = np.zeros(len(words_category[category]))
		for pair in pairs:
			category_word_index = words_category[category].index(pair['in_category'])
			# If the item is a word
			if (not isPhrase(pair['in_category'])) and pair['distance'] >= 0.5 and \
			   category_vector[category_word_index] < pair['distance']:
				category_vector[category_word_index] = pair['distance'] * pair['count']
			# If the item is a phrase
			elif isPhrase(pair['in_category']) and \
			   category_vector[category_word_index] < pair['distance']:
				category_vector[category_word_index] = pair['distance'] * pair['count']
		feature_vector = np.concatenate((feature_vector, category_vector))
	return feature_vector.tolist()

if __name__ == '__main__':

	word2vec_model_path    = sys.argv[1] # '../resource/GoogleNews-vectors-negative300.bin'
	words_category_path    = sys.argv[2] # '../tmp/woodie.gen_vectors_from_wordslist/KeyWords.json'
	phrases_extractor_path = sys.argv[3]
	text_index             = int(sys.argv[4]) # The index for the text feature (default = 14)

	words_category = {}
	# Load Key Words Dictionary
	with open(words_category_path, 'rb') as f:
		words_category = json.load(f)
	
	# Load Word2Vec Model
	print >> sys.stderr, '[INFO] Loading Word2Vec Model...'
	word2vec_model = Word2Vec.load_word2vec_format(word2vec_model_path, binary=True)

	# Load PhrasesExtractor
	print >> sys.stderr, '[INFO] Loading PhrasesExtractor...'
	phrases_extractor = PhrasesExtractor(phrases_extractor_path)

	# Process the data stream from stdin	
	for line in sys.stdin:
		data = line.strip('\n').split('\t')
		if len(data) < text_index:
			print >> sys.stderr, '[ERROR] data: [%s] is insufficient.' % line
			continue
		
		# Text Feature:
		remarks             = data[text_index]
		text_feature_dict   = FeatureTextInCategory(word2vec_model, phrases_extractor, remarks, words_category)
		# Organize the text feature into a fixed-length numerical vector
		text_feature_vector = FeatureDict2FeatureVector(words_category, text_feature_dict)
		text_feature_str    = '#'.join(map(str, text_feature_vector))
		# Replace the text with the text feature
		data[text_index]    = text_feature_str
		print '\t'.join(data)
		# print json.dumps(text_feature_dict, indent=4)