#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import arrow
import pyodbc
import argparse

from gensim import corpora, models, similarities

from holmes.utils import Config
from holmes.catscorpus import Documents

# def load_index():
# 	pass

def query_crime_record(incident_id):
	# Configuration
	driver   = "ODBC Driver 13 for SQL Server"
	server   = "tcp:awarecorecdsserver2308170150.database.usgovcloudapi.net,1433"
	database = "awarecorecdsdb2308170150"
	uid      = "IncidentNarrativeRetrainReader"
	password = "Pass@w0rd"
	encrypt  = "yes"
	timeout  = 30
	# Connecting to the database
	# cnxn   = pyodbc.connect('Driver={%s};Server=%s;Database=%s;Uid=%s;Pwd=%s;Encrypt=%s;TrustServerCertificate=;Connection Timeout=%s;')
	cnxn   = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:awarecorecdsserver2308170150.database.usgovcloudapi.net,1433;Database=awarecorecdsdb2308170150;Uid=IncidentNarrativeRetrainReader;Pwd=Pass@w0rd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
	cursor = cnxn.cursor()
	# Perform the query by incident id
	cursor.execute("SELECT * FROM IncidentNarrativeView WHERE IncidentId=%d;" % (incident_id))
	return cursor.fetchone()


def main():
	# Parse the input parameters
	parser = argparse.ArgumentParser(description="Script for parsing xml format crime records.")
	parser.add_argument("-q", "--query_id", required=True, help="The path of the input xml file")
	parser.add_argument("-c", "--config", required=True, help="The path of the output folder")
	args = parser.parse_args()

	# Read configuration from ini file
	conf = Config("conf/text.ini")
	# Read Crime Codes Descriptions
	pruned_dict_path = conf.get_section("Corpus")["pruned_dict_path"]
	mm_corpus_path   = conf.get_section("Corpus")["mm_corpus_path"]
	index_path       = conf.get_section("Corpus")["index_path"]

	# Query raw data via the query_id and get the narratives
	query_crime_record(args.query_id)

	# Preprocessing the narratives
	query_tokens = Documents.tokenize(text_string, N=1)
	print >> sys.stderr, "[%s] The query has been tokenized as [%s, ... ]." % (arrow.now(), query_tokens[:5])

	# Load dictionary
	dictionary = corpora.Dictionary()
	dictionary = dictionary.load(pruned_dict_path)
	print >> sys.stderr, "[%s] Dictionary has been loaded %s" % (arrow.now(), dictionary) 

	# Get BoW representation of the query
	query_bow = dictionary.doc2bow(query_tokens)
	print >> sys.stderr, "[%s] The query has been converted into BoW as [%s, ... ]." % (arrow.now(), query_bow[:5]) 

	# Load indexing
	index = similarities.MatrixSimilarity.load(index_path)
	print >> sys.stderr, "[%s] Well-trained indexings has been loaded." % (arrow.now()) 

	# perform a similarity query against the corpus
	sims = index[query_bow]
	print >> sys.stderr, "[%s] Performed a similarity query against the corpus." % (arrow.now())

	# sims = sorted(enumerate(sims), key=lambda item: -item[1])

if __name__ == "__main__":
	main()