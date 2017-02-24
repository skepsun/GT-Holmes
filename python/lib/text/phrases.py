#!/usr/local/bin/python

# from gensim.models import Word2Vec
from gensim.models import Phrases
from collections import Counter
# from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import numpy as np
import string
import nltk
import json
import sys

from words import WordsSimilarity, GetSentsByWords

class PhrasesExtractor:
	'''
	Phrases Model

	A class for building, training and providing API for n-gram model
	which was built in gensim. 
	'''

	MIN_COUNT = 2
	THRESHOLD = 4

	def __init__(self, model_path, word2vec, interested_phrases=['rear_door']):
		self.n_gram     = None
		self.model_path = model_path
		self.interested_phrases = interested_phrases
		self.word2vec   = word2vec
		try:
			self.n_gram = Phrases().load(self.model_path)
		except IOError, msg:
			print >> sys.stderr, '[WARN] Invalid model file. A new model will be initialized.'
			self.n_gram = Phrases(
				# - min_count:
				# Ignore all words and bigrams with total collected 
				# count lower than this. Bydefault it value is 5
				min_count=self.MIN_COUNT, 
				# - threshold:
				# A threshold for forming the phrases (higher means fewer phrases). 
				# A phrase of words a and b is accepted if 
				# (cnt(a, b) - min_count) * N / (cnt(a) * cnt(b)) > threshold, 
				# where N is the total vocabulary size. Bydefault it value is 10.0
				threshold=self.THRESHOLD
			)
		except Exception, msg:
			print >> sys.stderr, '[ERROR] Please make sure you used the correct model file.'
	
	def train(self, corpus):
		'''
		Train

		corpus is a 2D list, which contains multiple texts for training
		'''
		sentences = []
		# Get sentences from raw text.
		# text contains all the narratives of one crime records (with an unique crime id)
		for text in corpus:
			sents = GetSentsByWords(text)
			sentences += sents
		# Train phrases with sentences
		self.n_gram.add_vocab(sentences)
		# Save the trained model
		self.n_gram.save(self.model_path)

	def get_phrases(self, text):
		# If the n_gram model is invalid
		if self.n_gram is None:
			return None
		# Remove the delimiter in the free text
		text = ' '.join(text.strip('\n').split('\2'))
		text = ' '.join(text.strip().split('\1'))
		# - Split the text into words
		# - Remove uppercases
		# - Remove punctuation
		phrases = []
		for sent in sent_tokenize(text):
			words = [
				word
				for word in nltk.word_tokenize(sent.lower())
				if word not in string.punctuation
			]
			# Get phrases
			ps = self.n_gram[words]
			# Remove the single words in the phrases
			ps = [ p for p in ps if len(p.split('_')) > 1 ]
			phrases += ps
		
		return phrases
	
	def phrases_info(self, text):
		phrases = self.get_phrases(text)
		phrases_count = dict(Counter(phrases))
		info_dict = {}
		for p in phrases_count.keys():
			sims = [ PhrasesSimilarity(self.word2vec, p, p_i) for p_i in self.interested_phrases ]
			# sims = zip(*sim_phrase_list)[0]
			# Remove irrelevant phrases according to the interested phrases list
			if max(sims) > 0.8:
				info_dict[p] = {}
				info_dict[p]['count'] = phrases_count[p]
				info_dict[p]['similar_phrase'] = self.interested_phrases[np.argmax(sims)]
				info_dict[p]['similarity'] = max(sims)
		return info_dict



def PhrasesSimilarity(word2vec_model, phrase_A, phrase_B):
	words_A = phrase_A.split('_')
	words_B = phrase_B.split('_')
	similarity = 0
	if len(words_A) == len(words_B):
		for i in range(len(words_A)):
			similarity += WordsSimilarity(word2vec_model, words_A[i], words_B[i])
		similarity /= len(words_A)
	elif len(words_A) != len(words_B):
		sim_mat = np.zeros((len(words_A), len(words_B)))
		# for i in range(len(words_A)):
		# 	for j in range(len(words_B)):
		# 		sim_mat[i][j] = word2vec_model.similarity(words_A[i], words_B[j])
		# TODO: Find the trace in the sim_mat
		similarity = 0
	# TODO: elif one is phrase, the other is word
	# elif min(len(words_A), len(words_B)) == 1 and \
	# 	max(len(words_A), len(words_B)) > 1:
				
	return similarity

def isPhrase(phrase):
	if '_' in phrase:
		return True
	else:
		return False

# if __name__ == '__main__':
	
# 	text = "On 07-08-2016, I officer L.Lundi was dispatched to a robbery call at 540 King Rd Nw. Upon arrival at the above location, I made contact with the victims Mr Cecil and Mrs.Susie Chang. According to the victims, it was approximately 10:30 am when they left their residence and as they returned home at  11:45 pm, they observed that a white in color pickup truck appeared  to be a late model Dodge Ram with round shape front grill. Mr. Chan stated as he walked over to the car garage, he saw 2 black males inside of the garage picking up his lawn equipments to put inside of the pickup truck. According to Mr. Chan when he saw one of the male put a black ski-mask over his head, that's when he quickly realized that it was a burglary in progress and start running. Mr Chan stated as he was running, one of suspect ran after him, pushed him to the ground and start beating on him with a steel pipe, trying to give him a choke hold then demanded that he give him the key to his vehicle that was blocking the suspect vehicle.i According to Mr. Chan the su The Victim Mr. Chan stated after he handed over his vehicle's key to the suspect, the suspect then walked over his white in color Lexus Ls 430 got inside of the vehicle and parked it on the grass away fr Mr. Chan sustained several cuts and bruises to his left and right arm. However, Mrs. Chan stated that she was watching the entire incident but was not hurt. Mr Chan stated as he went inside of his residence to verify if anything was taken, he observed that the rear door from the garage door leading to the house had been kicked in and the entire house was ransacked and several items were stolen. Among the stolen items were 1 backpack blower, a weed-eater, chain-saw, a lawnmower. Among the jewelries stolen were a rolex watch, a raymond wile watch, a silver diamond ring, a jay stone, a red coral necklace an There was no witnesses and no surveillance video. Zone-2 C.I.D along with Zone-2 Supervisor unit#2294 Sgt. Stephens along with Lt. childess were advised of the incident. Atlanta Police Crime Scene unit# 7320 were advised of the incident and came to process the scene for DNA, Fingerprints and photographs. The Victims were advised of the rights and a robbery report was completed for the incident. I officer L.Lundi  along With unit#2203  canvass the area for the suspects but could not locate them, also went door to door for potential witnesses but could not find any witnesses. I officer L.Lundi unit#2202 waCannon camerater FS56S181 pendantnty watch"

# 	model_path  = '../../tmp/woodie.burglary&pedrobbery.corpus/phrases.model' # sys.argv[1]
# 	corpus_path = '../../tmp/corpus/corpus.txt' # sys.argv[2]

# 	with open(corpus_path, 'rb') as f:
# 		 corpus = f.readlines()

# 	phrases_extractor = PhrasesExtractor(model_path)
# 	# phrases_extractor.train(corpus)
# 	phrases = phrases_extractor.get_phrases(text)
# 	print phrases
# 	# print json.dumps(phrases_count, indent=4)