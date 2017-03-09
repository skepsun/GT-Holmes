#!/usr/local/bin/python

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde


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
	json_file_path = 'tmp/woodie.new_data/feature.stream'
	features_dict = {}
	with open(json_file_path, 'rb') as f:
		features_dict = json.load(f)

	for key, value in features_dict.iteritems():
		print key, len(value['fuzzy_svd'])
		if len(value['fuzzy_svd']) > 130:
			ScatterPointsDensity('fuzzy_svd_' + key, features_dict[key]['fuzzy_svd'])
			ScatterPointsDensity('regular_svd_' + key, features_dict[key]['regular_svd'])
			# print features_dict[key]['fuzzy_lda']
			# ScatterPointsDensity('fuzzy_lda_' + key, features_dict[key]['fuzzy_lda'])
			# ScatterPointsDensity('regular_lda_' + key, features_dict[key]['regular_lda'])
