import os
import sys
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

from lib.narratives.text import TextAnalysor

def LoadVariables(file_path):
	if not os.path.exists(file_path + '.txt') or not os.path.exists(file_path + '.npy'):
		print >> sys.stderr, '[WARN] Loading failed. Invalid file path: %s' % file_path
		return
	# Load the document-term matrix
	dt_matrix = np.load(file_path + '.npy').tolist()
	# Load the labels information
	labels    = []
	with open(file_path + '.txt', 'r') as f:
		try:
			labels = f.readlines()
			labels = [
				list(set(label.strip('\n').split('#')))
				for label in labels
			]
		except: 
			print >> sys.stderr, '[ERROR] Loading failed. Unknown error'
	return dt_matrix, labels

def TagLabels(labels, tag_label_map):
	tags = []
	for label in labels:
		if ('*' in tag_label_map) and (label not in tag_label_map):
			tags.append(tag_label_map.index('*'))
		elif label in tag_label_map:
			tags.append(tag_label_map.index(label))
		else:
			tags.append(-1)
	return tags

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
		ids, location_points, tags, similarity_matrix, 
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
	for i in range(len(ids)):
		ax.annotate(
			ids[i],
            xy=location_points[i],
			color='k'
        )
	
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
				linescolor.append(cmap(weight))
				lineswidth.append(weight * 5)
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



if __name__ == '__main__':

	# Parse input parameters
	parser = argparse.ArgumentParser()
	parser.add_argument('--mock_geo_location', action="store_true", help='Enable mock geo location')
	parser.add_argument('--feature_analysor_path', type=str, help='path for folder of feature analysor')
	args = parser.parse_args()
	feature_analysor_path = args.feature_analysor_path
	print >> sys.stderr, '[INFO] Path for feature analysor: %s' % feature_analysor_path
	print >> sys.stderr, '[INFO] Enable mock geo location: %s' % args.mock_geo_location 

	# Initialize the text analysor
	text_features, labels = LoadVariables(feature_analysor_path)

	# text_features = text_features[0:24]
	# labels        = labels[0:24]

	# The mapping relationship between tags and labels
	# It must be a list whose index of the label in the list indicates its tag
	tag_label_map = ['pedrobbery', 'bulglary', '*']

	# TODO: Change codes to crime descriptions

	tags = TagLabels(
		[ label[0] for label in labels ], 
		tag_label_map
	)

	locations = []
	if args.mock_geo_location:
		locations = MockGeoLocation(
			tags, 
			seed=10,
			means=[(0, 0), (0, 6), (10, 3)], 
			cov=[[1, 0], [0, 1]]
		)

	# Calculate the similarities
	feature_sparse = sparse.csr_matrix(text_features)
	similarities   = cosine_similarity(feature_sparse)
	# Plot
	ScatterPointsSimilarities(
		tags, locations, tags, similarities, 
		mycolormap=['r', 'g', 'y'], 
		mytagmap=['Burglary', 'Ped Robbery', 'Random Cases'],
		# xlim=[-4, 8], ylim=[0, 9]
	)