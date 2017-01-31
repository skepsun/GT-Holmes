from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import sys
# from nltk.corpus import stopwords

def TfIdfAnalyzer(documents):
	cv = TfidfVectorizer(stop_words='english')
	# "tf_idf_mat" is a sparse matrix in SciPy
	# - You can access the element in X by " X[2,1] "
	#   or some row or col in X by " X[1,:] "
	tf_idf_mat = cv.fit_transform(documents)

	# "words_list" is a list which contains all the words in the corpus
	# - The index for each of the words is the corresponding value in the dictionary
	words_list = cv.get_feature_names()

	# "vocabulary" is a dictionary 
	# - Keys are the words 
	# - Values are the token (a unit number for each of the words)
	vocabulary = cv.vocabulary_

	def k_largest_in_matrix(mat, K):
		k_largest_list = []
		max     = 1
		sec_max = 0
		sec_i   = -1
		sec_j   = -1
		for k in range(K):
			for i in range(mat.shape[0]):
				for j in range(mat.shape[1]):
					if mat[i,j] < max and mat[i,j] > sec_max:
						sec_max = mat[i,j]
						sec_i   = i
						sec_j   = j
			k_largest_list.append([words_list[sec_j], sec_i, sec_j, sec_max])
			max     = sec_max
			sec_max = 0
			sec_i   = -1
			sec_j   = -1

		for item in k_largest_list:
			print '\t'.join(map(str, item))

		return k_largest_list
	
	k_largest_in_matrix(tf_idf_mat, 50)

	return words_list, tf_idf_mat

if __name__ == '__main__':
	import sys

	# Extract documents from local temp file.
	# TODO: The method of reading data needs to be improved,
	# TODO: Read line by line rather than reading all data once for all.
	documents_path = sys.argv[1]
	with open(documents_path, 'rb') as f:
		documents = f.readlines()
	documents = [x.strip() for x in documents]

	
	TfIdfAnalyzer(documents)
	

