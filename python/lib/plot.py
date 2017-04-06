#!/usr/local/bin/python

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

from narratives.text import TextAnalysor

def ScatterPointsDensity(label, points):
	image_path = 'tmp/woodie.new_data/img/'
	points = np.array(points)
	count, dim = points.shape
	if dim != 2:
		print >> sys.stderr, '[ERROR] Invalid dimensionality dim=%d.' % dim
		return
	# Get the x, y data
	x, y = points.transpose()
	# Calculate the point density
	xy = np.vstack([x,y])
	z  = gaussian_kde(xy)(xy)
	fig, ax = plt.subplots()
	ax.scatter(x, y, c=z, s=100, edgecolor='')
	# plt.show()
	plt.savefig(image_path + label + '.png')

if __name__ == '__main__':
	json_file_path  = 'resource/CrimeCode.json'
	crime_code_dict = {}
	with open(json_file_path, 'rb') as f:
		crime_code_dict = json.load(f)

	# for key, value in features_dict.iteritems():
	# 	print key, len(value['fuzzy_svd'])
	# 	if len(value['fuzzy_svd']) > 130:
	# 		ScatterPointsDensity('fuzzy_svd_' + key, features_dict[key]['fuzzy_svd'])
			# ScatterPointsDensity('regular_svd_' + key, features_dict[key]['regular_svd'])
			# print features_dict[key]['fuzzy_lda']
			# ScatterPointsDensity('fuzzy_lda_' + key, features_dict[key]['fuzzy_lda'])
			# ScatterPointsDensity('regular_lda_' + key, features_dict[key]['regular_lda'])

	file_path = 'tmp/woodie.new_data/text_analysor_data/test'
	text_analysor = TextAnalysor()
	text_analysor.load_variables(file_path)
	_, fuzzy_feature_dict, _  = text_analysor.fuzzy_LSA()
	# _, regular_feature_dict, _, _ = text_analysor.regular_LSA()

	print 

	for key, value in fuzzy_feature_dict.iteritems():
		if len(value) > 50:
			if key == '':
				continue
			img_name = '-'.join(crime_code_dict[key].split('/'))
			img_name = '_'.join(img_name.split(' '))
			ScatterPointsDensity('fuzzy_svd [%s]' % img_name, value)

	# for key, value in regular_feature_dict.iteritems():
	# 	if len(value) > 200:
	# 		ScatterPointsDensity('regular_svd [%s]' % crime_code_dict[key], value)

