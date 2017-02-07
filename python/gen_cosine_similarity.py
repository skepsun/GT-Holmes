import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from matplotlib.colors import ListedColormap
from matplotlib import colors
from matplotlib import colorbar
from matplotlib import collections  as mc
from scipy import sparse

# colormap = {
# 	'burglary': 'b',
# 	'pedrobbery': 'r'
# }

# def ScatterPoints2D(points, annotations):
	
# 	if points.shape[1] != 2:
# 		print >> sys.stderr, '[ERROR] The dimension of the points should be 2, not %d' % points.shape[1]
# 		return 

# 	x = points[:, 0]
# 	y = points[:, 1]

# 	fig, ax = plt.subplots()
# 	ax.scatter(x, y)
# 	for i, txt in enumerate(annotations):
# 		ax.annotate(txt, (x[i], y[i]), color=colormap[txt])
# 	plt.show()

def ScatterOnMap(ids, location_points, tags, similarity_matrix):
	fig, ax = plt.subplots()

	# Plot points
	for i in range(len(location_points)):
		ax.plot(location_points[i][0], location_points[i][1], color=tags[i], marker='o', ms=10)
	
	# Plot annotations
	for i in range(len(ids)):
		ax.annotate(ids[i],
            xy=location_points[i],
			color='k',
			# horizontalalignment='left',
            # verticalalignment='bottom'
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
	for i in range(similarity_matrix.shape[1]):
		for j in range(i, similarity_matrix.shape[0]):
			lines.append([location_points[i], location_points[j]])
			weight = similarity_matrix[j][i]
			linescolor.append(cmap(weight))
	# - Plot lines		
	lc = mc.LineCollection(lines, color=linescolor, cmap='PuBu_r', linewidths=2)
	ax.add_collection(lc)
	ax.autoscale()
	ax.margins(0.1)
	
	plt.show()

if __name__ == '__main__':
	incidents_A_path = sys.argv[1]
	incidents_B_path = sys.argv[2]

	feature_A = []
	feature_B = []
	with open(incidents_A_path, 'rb') as f:
		feature_A = [feature.split('\t') for feature in f.readlines()]
	with open(incidents_B_path, 'rb') as f:
		feature_B = [feature.split('\t') for feature in f.readlines()]
	
	text_feature_A = []
	location_A     = []
	id_A           = []
	for feature in feature_A:
		incident_id = feature[0]
		lat  = float(feature[1])
		long = float(feature[2])

		id_A.append(incident_id)
		location_A.append([lat, long])
		text_feature_A.append(map(float, feature[3].split('#')))

	text_feature_B = []
	location_B     = []
	id_B           = []
	for feature in feature_B:
		incident_id = feature[0]
		lat  = float(feature[1])
		long = float(feature[2])
		
		id_B.append(incident_id)
		location_B.append([lat, long])
		text_feature_B.append(map(float, feature[3].split('#')))
	

	text_features = np.array(text_feature_A + text_feature_B)
	locations     = np.array(location_A + location_B)
	ids           = id_A + id_B
	tags          = []
	for i in range(len(text_feature_A)):
		tags.append('r')
	for i in range(len(text_feature_B)):
		tags.append('g')

	# embedded_dim = 2
	# model  = TSNE(n_components=embedded_dim, random_state=0)
	# points      = model.fit_transform(text_features)
	# ScatterPoints2D(points, annotations)

	feature_sparse = sparse.csr_matrix(text_features)
	similarities   = cosine_similarity(feature_sparse)
	# for row in similarities.tolist():
	# 	print '\t'.join(map(str, row))

	ScatterOnMap(ids, locations, tags, similarities)

	

	


