import pickle
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold import TSNE
from matplotlib import pylab


# Load sparse vector
sparse_vecs = None
with open("resource/lda_test/lda_topics", "rb") as h:
    sparse_vecs = pickle.load(h)
# Load cats tuples collection
with open("resource/lda_test/cats", "r") as h:
	cats = pickle.load(h)

vectors = []
init_vector = [ 0 for i in range(100) ]
for sparse_vec in sparse_vecs:
	vec = init_vector 
	for index, value in sparse_vec:
		vec[index] = value
	vectors.append(vec)

embedded_vecs = TSNE(n_components=3).fit_transform(vectors)

# Find the universal set for appeared categories
categories = [ category for _id, category in cats["collections"] ]
categories = [ category for category in list(set(categories)) \
                        if (category is not "") or (category is not None) ]
# for _id, category in cats:
# 	if category is not in categories and \
# 	   (category is not "" or category is not None):
# 		categories.append(category)
Xs = [ [] for i in range(len(categories)) ]
Ys = [ [] for i in range(len(categories)) ]
Zs = [ [] for i in range(len(categories)) ]
print embedded_vecs.shape
print len(cats["collections"])
for i in range(len(cats["collections"])):
	Xs[categories.index(cats["collections"][i][1])].append(embedded_vecs[i][0])
	Ys[categories.index(cats["collections"][i][1])].append(embedded_vecs[i][1])
	Zs[categories.index(cats["collections"][i][1])].append(embedded_vecs[i][2])

print Xs
print Ys
print Zs

print len(Xs)
print len(Ys)
print len(Zs)

fig = pylab.figure()

ax  = Axes3D(fig)

# ax.scatter(x, y, z) 

cm = plt.cm.get_cmap('RdYlBu')

print cm

for i in range(len(Xs)):
	ax.scatter(Xs[i], Ys[i], Zs[i], c=[np.clip(i, 0, len(categories)) for i in range(len(Xs[i]))], cmap=cm, vmin=0, vmax=len(categories))
	
plt.show()