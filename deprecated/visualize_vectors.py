from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pylab
import matplotlib.pyplot as plt
import numpy as np
import json
import sys

colormap = {
	'VEHICLE DESCRIPTORS': 'r',
	'GANG NAMES': 'b',
	'Burglary/Larceny / Car Break-Ins': 'm',
	'WEAPONS': 'c',
	'CLOTHING DESCRIPTORS': 'k',
	'Simple Assault / Battery': 'y',
	'Aggravated Assaults/ Homicide': 'g',
	'SUSPECT DESCRIPTORS': '#111fff',
	'Crimes /Offenses': '#333666',
	'Robbery/Carjackings': '#444555'
}

def ScatterPoints2D(points, annotations, tags):
	
	if points.shape[1] != 2:
		print >> sys.stderr, '[ERROR] The dimension of the points should be 2, not %d' % points.shape[1]
		return 

	x = points[:, 0]
	y = points[:, 1]

	fig, ax = plt.subplots()
	ax.scatter(x, y)
	for i, txt in enumerate(annotations):
		# Set color for the annotation
		for k, v in tags.iteritems():
			if annotations[i] in v:
				c = colormap[k]
		ax.annotate(txt, (x[i], y[i]), color=c)
	plt.show()

def ScatterPoints3D(points, annotations, tags):

	if points.shape[1] != 3:
		print >> sys.stderr, '[ERROR] The dimension of the points should be 3, not %d' % points.shape[1]
		return 
	
	x = points[:, 0]
	y = points[:, 1]
	z = points[:, 2]

	fig = pylab.figure()
	ax  = Axes3D(fig)

	ax.scatter(x, y, z) 
	for i in range(len(x)):
		# Set color for the annotation
		for k, v in tags.iteritems():
			if annotations[i] in v:
				c = colormap[k]
		# Add annotation
		ax.text(
			x[i], y[i], z[i], 
			'%s' % (annotations[i]), size=20, zorder=1, color=c
		) 

	plt.show()

if __name__ == '__main__':
	word_vec_path = sys.argv[1]
	word_tag_path = sys.argv[2]

	with open(word_vec_path) as data_file:
		word_vec_data = json.load(data_file)
	with open(word_tag_path) as data_file:
		word_tag_data = json.load(data_file)

	# Use t-SNE to reduct the dimensionality of word vectors
	embedded_dim = int(sys.argv[3])
	model        = TSNE(n_components=embedded_dim, random_state=0)
	# Get points (numerical vectors) and the annotations (words)
	points      = model.fit_transform(np.array(word_vec_data.values()))
	annotations = word_vec_data.keys()

	print >> sys.stderr, '[INFO] %d words have been converted.' % len(annotations)

	if embedded_dim == 2:
		ScatterPoints2D(points, annotations, word_tag_data)
	elif embedded_dim == 3:
		ScatterPoints3D(points, annotations, word_tag_data)
	else:
		print >> sys.stderr, '[ERROR] Invalid embedded dimensionality %d' % embedded_dim