#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import pickle
import argparse
import numpy as np

import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from scipy.stats import gaussian_kde

colorbar = ['y', 'g', 'r', 'c', 'm', 'b', 'k', 'w']
label_legend = ['Random', 'Crime Series 1', 'Crime Series 2', 'Crime Series 3', 'Crime Series 4', 'Crime Series 5']

def main():
	# Parse the input parameters
	parser = argparse.ArgumentParser(description="Script for converting vectors to t-SNE projections")
	parser.add_argument("-v", "--vpath", required=True, help="The path of the numpy txt file")
	parser.add_argument("-l", "--lpath", required=True, help="The path of the cats txt file")
	parser.add_argument("-o", "--opath", required=True, help="The path of the output file")
	# parser.add_argument("-d", "--dim", default=2, type=int, help="The number of components in t-SNE")
	args = parser.parse_args()

	vec_path = args.vpath
	lab_path = args.lpath
	out_path = args.opath
	# TODO: Support dim = 3 in the future
	tsne_dim = 2 # args.dim

	# Get vectors
	vectors = np.loadtxt(vec_path, delimiter=",")
	# Get labels
	labels  = []
	with open(lab_path, "r") as f:
		cats_obj = pickle.load(f)
		# TODO: Locate category field by "C" in definitions
		# TODO: Clean category before use it 
		labels   = [ cats[1] for cats in cats_obj["collections"] ]
	# Get the set of the labels
	label_set = [ label for label in list(set(labels)) if label is not "" ]

	embedded_vecs = TSNE(n_components=2).fit_transform(vectors)

	Xs = [ [] for i in range(len(label_set)) ]
	Ys = [ [] for i in range(len(label_set)) ]
	for ind in range(len(labels)):
		if labels[ind] in label_set:
			Xs[label_set.index(labels[ind])].append(embedded_vecs[ind][0])
			Ys[label_set.index(labels[ind])].append(embedded_vecs[ind][1])

	fig, ax = plt.subplots()
	for ind in range(len(label_set)):
		print "label:\t", label_set[ind]
		print "len:\t", len(Xs[ind])
		x = Xs[ind]
		y = Ys[ind]
		ax.scatter(x, y, c=colorbar[ind], s=30, edgecolor='', label=label_legend[ind])
		
	ax.legend()
	plt.axis('off')
	fig.savefig("%s/%s.png" % (out_path, "test"))
	plt.close(fig)



if __name__ == "__main__":
	main()