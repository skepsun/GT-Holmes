from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pylab
import matplotlib.pyplot as plt
import numpy as np
import json
import sys

def ScatterPoints2D(points, annotations):
	
	if points.shape[1] != 2:
		print >> sys.stderr, 'Error! The dimension of the points should be 2, not %d' % points.shape[1]
		return 

	x = points[:, 0]
	y = points[:, 1]

	fig, ax = plt.subplots()
	ax.scatter(x, y)
	for i, txt in enumerate(annotations):
		ax.annotate(txt, (x[i], y[i]))
	plt.show()

def ScatterPoints3D(points, annotations):

	if points.shape[1] != 3:
		print >> sys.stderr, 'Error! The dimension of the points should be 3, not %d' % points.shape[1]
		return 
	
	x = points[:, 0]
	y = points[:, 1]
	z = points[:, 2]

	fig = pylab.figure()
	ax  = Axes3D(fig)

	ax.scatter(x, y, z) 
	for i in range(len(x)):
		ax.text(
			x[i], y[i], z[i], 
			'%s' % (annotations[i]), size=20, zorder=1, color='k'
		) 

	plt.show()

if __name__ == '__main__':
	data_path = sys.argv[1]
	
	with open(data_path) as data_file:
		data = json.load(data_file)
	# Use t-SNE to reduct the dimensionality of word vectors
	embedded_dim = int(sys.argv[2])
	model        = TSNE(n_components=embedded_dim, random_state=0)
	# Get points (numerical vectors) and the annotations (words)
	points      = model.fit_transform(np.array(data.values()))
	annotations = data.keys()

	if embedded_dim == 2:
		ScatterPoints2D(points, annotations)
	elif embedded_dim == 3:
		ScatterPoints3D(points, annotations)
	else:
		print >> sys.stderr, 'Error! Invalid embedded dimensionality %d' % embedded_dim