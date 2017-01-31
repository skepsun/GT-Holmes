from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
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

	
	return words_list, tf_idf_mat

if __name__ == '__main__':
	import sys

	# Extract documents from local temp file.
	documents_path = sys.argv[1]
	with open(documents_path, 'rb') as f:
		documents = f.readlines()
	documents = [x.strip() for x in documents]

	TfIdfAnalyzer(documents)
	

