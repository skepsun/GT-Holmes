from sklearn.manifold import TSNE
import numpy as np
import json
import sys

if __name__ == '__main__':
	data_path = sys.argv[1]
	
	with open(data_path) as data_file:
		data = json.load(data_file)

	embedded_dim = sys.argv[2]
	model    = TSNE(n_components=embedded_dim, random_state=0)
	new_data = model.fit_transform(np.array(data.values()))
	
	axis = []
	for i in range(nembedded_dim):
		axis.append(new_data[:, i])
	label = data.keys()

	# Plot the scatter figure
	fig, ax = plt.subplots()
	if embedded_dim == 2:
		ax.scatter(axis[0], axis[1])
		for i, txt in enumerate(label):
			ax.annotate(txt, (axis[0][i],axis[1][i]))
	elif embedded_dim == 3:
		ax.scatter(axis[0], axis[1], axis[2])
		for i, txt in enumerate(label):
			ax.annotate(txt, (axis[0][i],axis[1][i],axis[2][i]))

	fig.show()

