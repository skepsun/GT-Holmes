#!/usr/local/bin/python
from gensim.models import Word2Vec
from collections import Counter
from nltk.corpus import stopwords
import numpy as np
import heapq
import json
import sys
import re

def FeatureTextInCategory(word2vec_model, text, words_category):
	words_count = dict(Counter(re.findall(r'\w+', text)))
	# Remove words with insufficent length in text.
	for word in words_count.keys():
		if len(word) < 3:
			words_count.pop(word, None)
	# Remove stop words in text
	for word in words_count.keys():
		if word in stopwords.words('english'):
			words_count.pop(word, None)
	# Init feature dict
	feature = {}
	for category in words_category.keys():
		feature[category] = []
	# Calculate the distance between every words in the text and category
	for category, words_in_category in words_category.iteritems():
		words_in_text     = words_count.keys()
		words_in_category = map(lambda x: x.encode('ascii','ignore'), words_in_category)
		# Calculate the matrix of distances between 
		# words_in_text & words_in_category
		len_w_t  = len(words_in_text)
		len_w_c  = len(words_in_category)
		dist_mat = np.zeros((len_w_t, len_w_c))
		for i in range(len_w_t):
			for j in range(len_w_c):
				try:
					dist_mat[i, j] = word2vec_model.similarity(words_in_text[i], words_in_category[j])
				except KeyError:
					dist_mat[i, j] = -1
		# Find the best matched words in the category for each of words in text
		best_matched_indexs = dist_mat.argmax(axis=1) # The index of the best matched words
		best_matched_dists  = []                      # The distance between the best matched words and the words in text
		for i in range(len(best_matched_indexs)):
			best_matched_dists.append(dist_mat[i, best_matched_indexs[i]])
		best_matched_dists = np.array(best_matched_dists)
		# Find K-nearest words (to the current category) in the text 
		K = 5
		for k in range(K):
			i = best_matched_dists.argmax() # The index of the words in text which has the highest similarity
			j = best_matched_indexs[i]
			# If the current best matched distance is lower than o, then abandon it.
			if best_matched_dists[i] <= 0:
				break
			best_matched_dists[i] = -1      # Remove the largest value in the best_matched_dists
			feature[category].append({
				'in_text':     words_in_text[i],
				'in_category': words_in_category[j],
				'count':       words_count[words_in_text[i]],
				'distance':    dist_mat[i, j]
			})
	return feature

def FeatureDict2FeatureVector(words_category, feature_dict):
	feature_vector = np.zeros(0)
	for category, pairs in feature_dict.iteritems():
		categor_vector = np.zeros(len(words_category[category]))
		for pair in pairs:
			category_word_index = words_category[category].index(pair['in_category'])
			if pair['distance'] >= 0.5 and \
			   categor_vector[category_word_index] < pair['distance']:
				categor_vector[category_word_index] = pair['distance'] * pair['count']
		feature_vector = np.concatenate((feature_vector, categor_vector))
	return feature_vector.tolist()

if __name__ == '__main__':

	word2vec_model_path = sys.argv[1] # '../resource/GoogleNews-vectors-negative300.bin'
	words_category_path = sys.argv[2] #'../tmp/woodie.gen_vectors_from_wordslist/KeyWords.json'

	words_category = {}
	# Load Key Words Dictionary
	with open(words_category_path, 'rb') as f:
		words_category = json.load(f)
	
	# Load Word2Vec Model
	model = Word2Vec.load_word2vec_format(word2vec_model_path, binary=True)

	# Process the data stream from stdin	
	for line in sys.stdin:
		data = line.strip('\n').split('\t')
		if len(data) < 15:
			print >> sys.stderr, '[ERROR] data: [%s] is insufficient.' % line
			continue
		
		# Incident Id:
		incident_id = data[0]
		
		# Text Feature:
		remarks = ' '.join(data[14].strip().split('\2'))
		text_feature_dict   = FeatureTextInCategory(model, remarks, words_category)
		# Organize the text feature into a fixed-length numerical vector
		text_feature_vector = FeatureDict2FeatureVector(words_category, text_feature_dict)
		text_feature_str    = '#'.join(map(str, text_feature_vector))
		
		# Location Feature:
		avg_lat  = str(float(data[4]) / 100000)
		avg_long = str(float(data[5]) / 100000)

		print '\t'.join((incident_id, avg_lat, avg_long, text_feature_str))
		# print json.dumps(text_features, indent=4)