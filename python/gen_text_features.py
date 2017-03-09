#!/usr/local/bin/python
from gensim.models import Word2Vec
from collections import Counter
from nltk.corpus import stopwords
import numpy as np
import string
import json
import sys
import re

from lib.narratives.text import TextAnalysor


if __name__ == '__main__':
	# Initialize the text analysor
	text_analysor = TextAnalysor()
	crime_types   = []
	# Process the data stream from stdin
	i = 0
	for line in sys.stdin:
		data = line.strip('\n').split('\t')
		if len(data) < 5:
			print >> sys.stderr, '[ERROR] data: [%s] is insufficient.' % line
			continue
		incident_id  = data[0]
		timestamp    = data[1]
		crime_code_1 = data[2]
		crime_code_2 = data[3]
		location     = data[4]
		remarks      = data[5]

		print >> sys.stderr, '[INFO] No. %d, Incident Id: %s' % (i, incident_id)
		try:
			text_analysor.set_text(remarks)
			crime_types.append(crime_code_1.split('#'))
		except Exception, e:
			print >> sys.stderr, '[ERROR] Invalid remarks.'

		if i >= 10000:
			break
		i += 1

	print >> sys.stderr, '[INFO] %d incidents have been processed.' % len(text_analysor.dt_matrix)
	fuzzy_svd_matrix, _         = text_analysor.fuzzy_LSA()
	regular_svd_matrix, _, _, _ = text_analysor.regular_LSA()
	fuzzy_lda_matrix            = text_analysor.fuzzy_LDA()
	regular_lda_matrix, _, _    = text_analysor.regular_LDA()


	crime_types_set     = list(set([ item for sublist in crime_types for item in sublist ]))
	crime_features_dict = {} 
	for c_i in crime_types_set:
		crime_features_dict[c_i] = {
			"fuzzy_svd":   [],
			"regular_svd": [],
			"fuzzy_lda":   [],
			"regular_lda": []
		}
		for j in range(len(crime_types)):
			for c_j in crime_types[j]:
				if c_j == c_i:
					crime_features_dict[c_i]["fuzzy_svd"].append(fuzzy_svd_matrix[j])
					crime_features_dict[c_i]["regular_svd"].append(regular_svd_matrix[j])
					crime_features_dict[c_i]["fuzzy_lda"].append(fuzzy_lda_matrix[j])
					crime_features_dict[c_i]["regular_lda"].append(regular_lda_matrix[j])

	# DEGUG
	# for key, value in crime_features_dict.iteritems():
	# 	print >> sys.stderr, 'crime_code:\t%s' % key
	# 	for v in value["fuzzy_svd"]:
	# 		print >> sys.stderr, 'Fuzzy_SVD:\t', 
	# 		print >> sys.stderr, v
	# 	for v in value["regular_svd"]:
	# 		print >> sys.stderr, 'Regular_SVD:\t', 
	# 		print >> sys.stderr, v
	# 	for v in value["fuzzy_lda"]:
	# 		print >> sys.stderr, 'Fuzzy_LDA:\t', 
	# 		print >> sys.stderr, v
	# 	for v in value["regular_lda"]:
	# 		print >> sys.stderr, 'Regular_LDA:\t', 
	# 		print >> sys.stderr, v

	# print >> sys.stderr, len(crime_types_set)

	print json.dumps(crime_features_dict)













