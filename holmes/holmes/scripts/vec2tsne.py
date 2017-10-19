import pickle
import argparse
import numpy as np

import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold import TSNE
from scipy.stats import gaussian_kde
# from matplotlib import pylab

"""
"""

def main():
	# Parse the input parameters
	parser = argparse.ArgumentParser(description="Script for converting vectors to t-SNE projections")
	parser.add_argument("-v", "--vpath", required=True, help="The path of the numpy txt file")
	parser.add_argument("-l", "--lpath", required=True, help="The path of the cats txt file")
	# parser.add_argument("-d", "--dim", default=2, type=int, help="The number of components in t-SNE")
	args = parser.parse_args()

	vec_path = args.vpath
	lab_path = args.lpath
	# TODO: Support dim = 3 in the future
	tsne_dim = 2 # args.dim
	
	# Get vectors
	vectors = np.loadtxt(vec_path, delimiter=",").transpose()
	# Get labels
	labels  = []
	with open(lab_path, "r") as f:
		cats_obj = pickle.load(f)
		# TODO: Locate category field by "C" in definitions
		# TODO: Clean category before use it 
		labels   = [ category.strip().split("#")[0] for _id, category in cats_obj["collections"] ]
	# Get the set of the labels
	label_set = [ label for label in list(set(labels)) if label is not "" ]

	Xs = [ [] for i in range(len(label_set)) ]
	for ind in range(len(labels)):
		if labels[ind] in label_set:
			Xs[label_set.index(labels[ind])].append(vectors[ind])

	for ind in range(len(label_set)):
		if len(Xs[ind]) > 500:
			print "label:\t", label_set[ind]
			print "len:\t", len(Xs[ind])
			# Train t-SNE
			embedded_vecs = TSNE(n_components=tsne_dim).fit_transform(Xs[ind])
			x = embedded_vecs[:,0]
			y = embedded_vecs[:,1]
			# Calculate the point density
			xy = np.vstack([x,y])
			z  = gaussian_kde(xy)(xy)
			
			fig, ax = plt.subplots()
			plt.scatter(x, y, c=z, s=100, edgecolor='')

			fig.savefig("results/%s.png" % label_set[ind])
			plt.close(fig)
			# plt.show()
			# break	

	# print embedded_vecs.shape

	# Xs = [ [] for i in range(len(label_set)) ]
	# Ys = [ [] for i in range(len(label_set)) ]
	# for ind in range(len(labels)):
	# 	if labels[ind] not in label_set:
	# 		continue
	# 	Xs[label_set.index(labels[ind])].append(embedded_vecs[ind][0])
	# 	Ys[label_set.index(labels[ind])].append(embedded_vecs[ind][1])

	# # Plotting

	
	# for label in label_set:
	# 	print label
	# 	fig, ax = plt.subplots()
	# 	x = Xs[label_set.index(label)]
	# 	y = Ys[label_set.index(label)]
		
	# 	ax.scatter(x, y, c=z, s=100, edgecolor='')
	# 	plt.show()
	# 	break


if __name__ == "__main__":
	main()

# # Load sparse vector
# sparse_vecs = None
# with open("resource/lda_test/lda_topics", "rb") as h:
#     sparse_vecs = pickle.load(h)
# # Load cats tuples collection
# with open("resource/lda_test/cats", "r") as h:
# 	cats = pickle.load(h)

# vectors = []
# init_vector = [ 0 for i in range(100) ]
# for sparse_vec in sparse_vecs:
# 	vec = init_vector 
# 	for index, value in sparse_vec:
# 		vec[index] = value
# 	vectors.append(vec)

# embedded_vecs = TSNE(n_components=3).fit_transform(vectors)

# # Find the universal set for appeared categories
# categories = [ category for _id, category in cats["collections"] ]
# categories = [ category for category in list(set(categories)) \
#                         if (category is not "") or (category is not None) ]
# # for _id, category in cats:
# # 	if category is not in categories and \
# # 	   (category is not "" or category is not None):
# # 		categories.append(category)
# Xs = [ [] for i in range(len(categories)) ]
# Ys = [ [] for i in range(len(categories)) ]
# Zs = [ [] for i in range(len(categories)) ]
# print embedded_vecs.shape
# print len(cats["collections"])
# for i in range(len(cats["collections"])):
# 	Xs[categories.index(cats["collections"][i][1])].append(embedded_vecs[i][0])
# 	Ys[categories.index(cats["collections"][i][1])].append(embedded_vecs[i][1])
# 	Zs[categories.index(cats["collections"][i][1])].append(embedded_vecs[i][2])

# print Xs
# print Ys
# print Zs

# print len(Xs)
# print len(Ys)
# print len(Zs)

# fig = pylab.figure()

# ax  = Axes3D(fig)

# # ax.scatter(x, y, z) 



# print cm

# for i in range(len(Xs)):
# 	ax.scatter(Xs[i], Ys[i], Zs[i], c=[np.clip(i, 0, len(categories)) for i in range(len(Xs[i]))], cmap=cm, vmin=0, vmax=len(categories))
	
# plt.show()