#!/usr/local/bin/python

import os
import sys
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
# from matplotlib.colors import ListedColormap
from matplotlib.ticker import FormatStrFormatter
from matplotlib import colors
from matplotlib import colorbar
from matplotlib import collections as mc
from scipy import sparse
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

def MockGeoLocation(
		tags, 
		seed=None,
		means=[(2, 2), (2, 10), (6, 10)], 
		cov=[[1, 0], [0, 1]]
	):
	# number of each kind of tag in tags
	tag_num = [ 0 for i in range(len(set(tags))) ]
	for tag in tags:
		tag_num[tag] += 1

	if seed is not None:
		np.random.seed(seed)
	locations = np.random.multivariate_normal(means[0], cov, tag_num[0])
	for i in range(1, len(set(tags))):
		locations = np.concatenate((
			locations,
			np.random.multivariate_normal(means[i], cov, tag_num[i])
		))
	return locations.tolist()

def ScatterPointsSimilarities(
		annotations, location_points, tags, similarity_matrix, 
		mycolormap=['r', 'g'], mytagmap=['Burglary', 'Ped Robbery'], 
		xlim=None, ylim=None, threshold=0.7
	):
	fig, ax = plt.subplots()
	
	# Plot points
	handles  = []
	last_tag = '' 
	for i in range(len(location_points)):
		h, = ax.plot(location_points[i][0], location_points[i][1], color=mycolormap[tags[i]], marker='o', ms=10)
		if tags[i] != last_tag:
			handles.append(h)
		last_tag = tags[i]
	
	# Plot annotations
	for i in range(len(annotations)):
		ax.annotate(
			annotations[i],
            xy=location_points[i],
			color='k')
	
	# Plot connections
	# - Add colormap for the line
	cmap = plt.cm.cool
	norm = colors.Normalize(vmin=0, vmax=1)
	cax = fig.add_axes([0.93, 0.2, 0.02, 0.6])
	cb  = colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, spacing='proportional')
	cb.set_label('Similarity')
	# - Set color for lines
	lines      = []
	linescolor = []
	lineswidth = []
	for i in range(similarity_matrix.shape[1]):
		for j in range(i, similarity_matrix.shape[0]):
			weight = similarity_matrix[j][i]
			if weight >= threshold:
				lines.append([location_points[i], location_points[j]])
				linescolor.append(cmap(weight * 30))
				lineswidth.append(weight * 20)
	# - Plot lines
	lc = mc.LineCollection(lines, color=linescolor, cmap='PuBu_r', linewidths=lineswidth)
	ax.add_collection(lc)
	
	# Basic plotting configuration
	ax.autoscale()
	ax.margins(0.1)
	ax.legend(handles, mytagmap, bbox_to_anchor=(0.75, 0.15), loc=2, borderaxespad=0., numpoints=1)
	ax.set_xlabel('Longitude')
	ax.set_ylabel('Latitude')
	if xlim is not None and ylim is not None:
		ax.set_xlim(xlim)
		ax.set_ylim(ylim)
	ax.ticklabel_format(useOffset=False)
	plt.show()

# if __name__ == '__main__':
# 	json_file_path  = 'resource/CrimeCode.json'
# 	crime_code_dict = {}
# 	with open(json_file_path, 'rb') as f:
# 		crime_code_dict = json.load(f)

# 	# for key, value in features_dict.iteritems():
# 	# 	print key, len(value['fuzzy_svd'])
# 	# 	if len(value['fuzzy_svd']) > 130:
# 	# 		ScatterPointsDensity('fuzzy_svd_' + key, features_dict[key]['fuzzy_svd'])
# 			# ScatterPointsDensity('regular_svd_' + key, features_dict[key]['regular_svd'])
# 			# print features_dict[key]['fuzzy_lda']
# 			# ScatterPointsDensity('fuzzy_lda_' + key, features_dict[key]['fuzzy_lda'])
# 			# ScatterPointsDensity('regular_lda_' + key, features_dict[key]['regular_lda'])

# 	file_path = 'tmp/woodie.new_data/text_analysor_data/test'
# 	text_analysor = TextAnalysor()
# 	text_analysor.load_variables(file_path)
# 	_, fuzzy_feature_dict, _  = text_analysor.fuzzy_LSA()
# 	# _, regular_feature_dict, _, _ = text_analysor.regular_LSA()

# 	print 

# 	for key, value in fuzzy_feature_dict.iteritems():
# 		if len(value) > 50:
# 			if key == '':
# 				continue
# 			img_name = '-'.join(crime_code_dict[key].split('/'))
# 			img_name = '_'.join(img_name.split(' '))
# 			ScatterPointsDensity('fuzzy_svd [%s]' % img_name, value)

# 	# for key, value in regular_feature_dict.iteritems():
# 	# 	if len(value) > 200:
# 	# 		ScatterPointsDensity('regular_svd [%s]' % crime_code_dict[key], value)

