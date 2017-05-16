from gensim import corpora, models, similarities
import string
import arrow
import nltk
import json
import sys

pruned_dict_path      = "../resource/universe_pruned.dict"
mm_corpus_path        = "../resource/corpus.mm"
crime_codes_desc_path = "../resource/CrimeCode.json"
labels_path           = "../resource/labels.txt"

print >> sys.stderr, "Loading Crime Codes Dictionary & Labels..."
crime_codes_dict = {}
with open(crime_codes_desc_path, "rb") as f:
	crime_codes_dict = json.load(f)
labels = []
with open(labels_path, "rb") as f:
	labels = [ [ label for label in line.strip("\n").split("#") ] for line in f.readlines() ]
descs  = []
for label_tuple in labels:
	non_9999 = [ label for label in label_tuple if label != "9999"]
	desc = []
	for label in non_9999:
		if label in crime_codes_dict.keys():
			desc.append(crime_codes_dict[label])
		else:
			desc.append(label)
	descs.append(desc)

print >> sys.stderr, "[%s] Loading existed dictionary." % arrow.now()
dictionary = corpora.Dictionary()
dictionary = dictionary.load(pruned_dict_path)
print dictionary

print >> sys.stderr, "[%s] Loading existed corpus." % arrow.now()
corpus = corpora.MmCorpus(mm_corpus_path)
print corpus

print >> sys.stderr, "[%s] Init Tfidf model." % arrow.now()
tfidf = models.TfidfModel(corpus)
print tfidf

print >> sys.stderr, "[%s] Calculating similarities" % arrow.now()
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=74945)
sims = index[tfidf[corpus[4]]]

i = 0
for sim in list(enumerate(sims)):
	print sim, descs[i]
	i += 1
