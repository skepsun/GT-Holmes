from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
import numpy as np
import json
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
	# vocabulary = cv.vocabulary_

	

	# def k_largest_in_matrix(mat, K):
	# 	k_largest_list = []
	# 	max     = 1
	# 	sec_max = 0
	# 	sec_i   = -1
	# 	sec_j   = -1
	# 	for k in range(K):
	# 		for i in range(mat.shape[0]):
	# 			for j in range(mat.shape[1]):
	# 				if mat[i,j] < max and mat[i,j] > sec_max:
	# 					sec_max = mat[i,j]
	# 					sec_i   = i
	# 					sec_j   = j
	# 		k_largest_list.append([words_list[sec_j], sec_i, sec_j, sec_max])
	# 		max     = sec_max
	# 		sec_max = 0
	# 		sec_i   = -1
	# 		sec_j   = -1
	# 	for item in k_largest_list:
	# 		print '\t'.join(map(str, item))
	# 	return k_largest_list
	
	# k_largest_in_matrix(tf_idf_mat, 50)
	
	return words_list, tf_idf_mat

def VectorizeVocabulary(word2vec_model, vocabulary):
	word_vec_dict = {}
	for word in vocabulary:
		try:
			word_vec_dict[word] = word2vec_model[word].tolist()
		except KeyError:
			print >> sys.stderr, 'Invalid word [%s].' % word
			continue
	return word_vec_dict

def GenerateVectorsFromDocuments(word2vec_model_path, documents_path):
	# documents is a txt file,
	# - each line of the documents is an individous document (txt)

	# Get documents from local file
	# TODO: The method of reading data needs to be improved,
	# TODO: Read line by line rather than reading all data once for all.
	with open(documents_path, 'rb') as f:
		documents = f.readlines()
	documents = [x.strip() for x in documents]

	# Get vocabulary of the documents
	vocabulary, _ = TfIdfAnalyzer(documents)

	# Get word2vec model by loading pretrained model
	model = Word2Vec.load_word2vec_format(word2vec_model_path, binary=True)
	# Get words-vectors dictionary
	word_vec_dict = VectorizeVocabulary(model, vocabulary)
	return json.dumps(word_vec_dict, indent=4)

def GenerateVectorsFromWordsList(word2vec_model_path, words_list_path):
	# words_list is a json file,
	# - Key is the tags of the words
	# - Value is the words list

	# Get words list from local file
	with open(words_list_path, 'rb') as f:
		data = json.load(f)
	# Merge all of the words list into one
	words = []
	for words_list in data.values():
		words += words_list
	words = list(set(words))
	
	# Get word2vec model by loading pretrained model
	model = Word2Vec.load_word2vec_format(word2vec_model_path, binary=True)
	# Get words-vectors dictionary
	word_vec_dict = VectorizeVocabulary(model, words)
	return json.dumps(word_vec_dict, indent=4)

if __name__ == '__main__':

	mode       = sys.argv[1]
	file_path  = sys.argv[2]
	model_path = sys.argv[3]

	if mode == 'wordslist':
		word_vec_dict = GenerateVectorsFromWordsList(model_path, file_path)
		print word_vec_dict

	elif mode == 'documents':
		word_vec_dict = GenerateVectorsFromDocuments(model_path, file_path)
		print word_vec_dict

	




	