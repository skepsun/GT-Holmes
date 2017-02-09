import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
# from matplotlib.colors import ListedColormap
from matplotlib.ticker import FormatStrFormatter
from matplotlib import colors
from matplotlib import colorbar
from matplotlib import collections as mc
from scipy import sparse

def ScatterPointsSimilarities(
		ids, location_points, tags, similarity_matrix, 
		mycolormap=['r', 'g'], mytagmap=['Burglary', 'Ped Robbery']
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
			lines.append([location_points[i], location_points[j]])
			weight = similarity_matrix[j][i]
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
	ax.ticklabel_format(useOffset=False)
	plt.show()



if __name__ == '__main__':
	incidents_paths = sys.argv[1].split(',')
	
	# Read data from local files
	incidents_features = []
	for incidents_path in incidents_paths:
		with open(incidents_path, 'rb') as f:
			incidents_features.append([feature.split('\t') for feature in f.readlines()])
	
	# Extract data from files
	text_features = [] # Text feature vector
	locations     = [] # Location (Latitude & Longitude)
	ids           = [] # Incidents id
	tags          = [] # Tags for the type of incidents
	
	i = 0
	for features in incidents_features:
		for feature in features:
			incident_id = feature[0]
			lat  = float(feature[1])
			long = float(feature[2])
			ids.append(incident_id)
			locations.append([long, lat])
			text_features.append(map(float, feature[3].split('#')))
			tags.append(i)
		i += 1
	
	text_features = np.array(text_features)
	locations     = np.array(locations)

	# Calculate the similarities
	feature_sparse = sparse.csr_matrix(text_features)
	similarities   = cosine_similarity(feature_sparse)
	# Plot
	ScatterPointsSimilarities(ids, locations, tags, similarities)

	

	


