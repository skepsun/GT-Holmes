#!/usr/local/bin/python
from gensim.models import Word2Vec
from gensim.models import Phrases
from collections import Counter
from nltk.corpus import stopwords
import numpy as np
import string
import nltk
import json

def TrainPhrases(sentences, ):


word2vec_model_path = 'resource/GoogleNews-vectors-negative300.bin'
words_category_path = 'tmp/woodie.gen_vectors_from_wordslist/KeyWords.json'

# Load Word2Vec Model
model = Word2Vec.load_word2vec_format(word2vec_model_path, binary=True)
text = ["On 07-08-2016, I officer L.Lundi was dispatched to a robbery call at 540 King Rd Nw. Upon arrival at the above location, I made contact with the victims Mr Cecil and Mrs.Susie Chang. According to the victims, it was approximately 10:30 am when they left their residence and as they returned home at  11:45 pm, they observed that a white in color pickup truck appeared  to be a late model Dodge Ram with round shape front grill. Mr. Chan stated as he walked over to the car garage, he saw 2 black males inside of the garage picking up his lawn equipments to put inside of the pickup truck. According to Mr. Chan when he saw one of the male put a black ski-mask over his head, that's when he quickly realized that it was a burglary in progress and start running. Mr Chan stated as he was running, one of suspect ran after him, pushed him to the ground and start beating on him with a steel pipe, trying to give him a choke hold then demanded that he give him the key to his vehicle that was blocking the suspect vehicle.i According to Mr. Chan the su The Victim Mr. Chan stated after he handed over his vehicle's key to the suspect, the suspect then walked over his white in color Lexus Ls 430 got inside of the vehicle and parked it on the grass away fr Mr. Chan sustained several cuts and bruises to his left and right arm. However, Mrs. Chan stated that she was watching the entire incident but was not hurt. Mr Chan stated as he went inside of his residence to verify if anything was taken, he observed that the rear door from the garage door leading to the house had been kicked in and the entire house was ransacked and several items were stolen. Among the stolen items were 1 backpack blower, a weed-eater, chain-saw, a lawnmower. Among the jewelries stolen were a rolex watch, a raymond wile watch, a silver diamond ring, a jay stone, a red coral necklace an There was no witnesses and no surveillance video. Zone-2 C.I.D along with Zone-2 Supervisor unit#2294 Sgt. Stephens along with Lt. childess were advised of the incident. Atlanta Police Crime Scene unit# 7320 were advised of the incident and came to process the scene for DNA, Fingerprints and photographs. The Victims were advised of the rights and a robbery report was completed for the incident. I officer L.Lundi  along With unit#2203  canvass the area for the suspects but could not locate them, also went door to door for potential witnesses but could not find any witnesses. I officer L.Lundi unit#2202 waCannon camerater FS56S181 pendantnty watch"]
# Process the data stream from stdin

for line in text:
	data = line
	# Text Feature:
	remarks = ' '.join(data.strip().split('\2'))
	sentence = [
		word
		for word in nltk.word_tokenize(remarks.lower())
		if word not in string.punctuation
	]
	bigram = Phrases([sentence], min_count=1, threshold=2)
	print list(bigram[sentence])
	break

