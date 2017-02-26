#!/usr/local/bin/python
from gensim.models import Word2Vec
from collections import Counter
from nltk.corpus import stopwords
import numpy as np
import string
import json
import sys
import re

from lib.text.text import Text

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


	# # Init feature dict
	# feature = {}
	# for category in words_category.keys():
	# 	feature[category] = []
	# # Calculate the distance between every word/phrase in the text and category
	# for category, words_in_category in words_category.iteritems():
	# 	items_in_text     = items_count.keys()
	# 	items_in_category = map(lambda x: x.encode('ascii', 'ignore'), words_in_category)
	# 	# Calculate the matrix of distances between 
	# 	# words_in_text & words_in_category
	# 	len_i_t  = len(items_in_text)
	# 	len_i_c  = len(items_in_category)
	# 	dist_mat = np.zeros((len_i_t, len_i_c))
	# 	for i in range(len_i_t):
	# 		for j in range(len_i_c):
	# 			try:
	# 				if isPhrase(items_in_text[i]) and isPhrase(items_in_category[j]):
	# 					dist_mat[i, j] = PhrasesSimilarity(word2vec_model, items_in_text[i], items_in_category[j])
	# 					# print >> sys.stderr, 'Phrase [%s] and phrase [%s] similarity is: %f' % \
	# 					# 	(items_in_text[i], items_in_category[j], dist_mat[i, j])
	# 				elif (not isPhrase(items_in_text[i])) and (not isPhrase(items_in_category[j])):
	# 					dist_mat[i, j] = word2vec_model.similarity(items_in_text[i], items_in_category[j])
	# 				else:
	# 					dist_mat[i, j] = 0
	# 			except KeyError, msg:
	# 				# print >> sys.stderr, '[WARN] There is no word [%s] or [%s] in the model. (MSG: %s)' % \
	# 					# (items_in_text[i], items_in_category[j], msg)
	# 				dist_mat[i, j] = -1
	# 	# Find the best matched words in the category for each of words in text
	# 	best_matched_indexs = dist_mat.argmax(axis=1) # The index of the best matched words
	# 	best_matched_dists  = []                      # The distance between the best matched words and the words in text
	# 	for i in range(len(best_matched_indexs)):
	# 		best_matched_dists.append(dist_mat[i, best_matched_indexs[i]])
	# 	best_matched_dists = np.array(best_matched_dists)
	# 	# Find K-nearest words (to the current category) in the text 
	# 	K = 15
	# 	for k in range(K):
	# 		i = best_matched_dists.argmax() # The index of the words in text which has the highest similarity
	# 		j = best_matched_indexs[i]
	# 		# If the current best matched distance is lower than o, then abandon it.
	# 		if best_matched_dists[i] <= 0:
	# 			break
	# 		best_matched_dists[i] = -1      # Remove the largest value in the best_matched_dists
	# 		feature[category].append({
	# 			'in_text':     items_in_text[i],
	# 			'in_category': items_in_category[j],
	# 			'count':       items_count[items_in_text[i]],
	# 			'distance':    dist_mat[i, j]
	# 		})
	# return feature

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
		t = Text(remarks, words_category)
		# tokens_info, sents_by_tokens = TextStructure(remarks, phrases_extractor)
		# anchors = AnchorCategory(words_category, tokens_info, word2vec_model)
		# VisualizeAnchor(sents_by_tokens, anchors)
		# text_features['features'].append(text_feature_dict)
		# # Organize the text feature into a fixed-length numerical vector
		# text_feature_vector = FeatureDict2FeatureVector(words_category, text_feature_dict, threshold)
	# 	text_feature_str    = '#'.join(map(str, text_feature_vector))
	# 	# Replace the text with the text feature
	# 	data[text_index]    = text_feature_str
	# 	print '\t'.join(data)
	# 	# print json.dumps(text_feature_dict, indent=4)
	
	# # Save the feature json file.
	# with open(json_feature_path, 'w') as f:
	# 	json.dump(text_features, f, indent=4)