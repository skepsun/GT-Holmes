import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

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
	for feature in feature_A:
		feature[1] = float(feature[1])
		feature[2] = float(feature[2])
		text_feature_A.append(map(float, feature[3].split('#')))

	text_feature_B = []
	for feature in feature_B:
		feature[1] = float(feature[1])
		feature[2] = float(feature[2])
		text_feature_B.append(map(float, feature[3].split('#')))
	
	text_features = np.array(text_feature_A + text_feature_B)
	A_sparse = sparse.csr_matrix(text_features)

	similarities = cosine_similarity(A_sparse)

	# for row in similarities.tolist():
	# 	print '\t'.join(map(str, row))

	

	


