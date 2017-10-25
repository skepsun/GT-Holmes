#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import arrow
import pyodbc
import argparse

from gensim import corpora, models, similarities

from holmes.utils import Config
from holmes.catscorpus import Documents

def load_id_info(id_info_path):
	with open(id_info_path, "r") as f:
		return [ line.strip("\n").split("\t")[0] for line in f ]



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
	cursor.execute("SELECT * FROM IncidentNarrativeView WHERE IncidentId=%s;" % (incident_id))
	return cursor.fetchone()



def main():
	# Parse the input parameters
	parser = argparse.ArgumentParser(description="Script for parsing xml format crime records.")
	parser.add_argument("-q", "--query_id", required=True, help="The path of the input xml file")
	parser.add_argument("-n", "--num", default=1, type=int, help="The path of the input xml file")
	parser.add_argument("-c", "--config", required=True, help="The path of the output folder")
	args = parser.parse_args()

	# Read configuration from ini file
	conf = Config(args.config)
	# Read Crime Codes Descriptions
	pruned_dict_path = conf.get_section("Model")["pruned_dict_path"]
	mm_corpus_path   = conf.get_section("Model")["mm_corpus_path"]
	id_info_path     = conf.get_section("Model")["id_info_path"]
	index_path       = conf.get_section("Model")["index_path"]

	# Loading Id information
	id_list = load_id_info(id_info_path)
	print >> sys.stderr, "[%s] Ids list has been loaded %s... ." % (arrow.now(), id_list[:5])

	# Query raw data via the query_id and get the narratives
	query_res   = query_crime_record(args.query_id)
	text_string = query_res[6]
	print >> sys.stderr, "[%s] The query narratives is {%s}." % (arrow.now(), text_string)

	# Preprocessing the narratives
	query_tokens = Documents.tokenize(text_string, N=1)
	print >> sys.stderr, "[%s] The query has been tokenized as: %s... ." % (arrow.now(), query_tokens[:5])

	# Load dictionary
	dictionary = corpora.Dictionary()
	dictionary = dictionary.load(pruned_dict_path)
	print >> sys.stderr, "[%s] Dictionary has been loaded %s" % (arrow.now(), dictionary) 

	# Get BoW representation of the query
	query_bow = dictionary.doc2bow(query_tokens)
	print >> sys.stderr, "[%s] The query has been converted into BoW as: %s... ." % (arrow.now(), query_bow[:5]) 

	# Load indexing
	index = similarities.MatrixSimilarity.load(index_path)
	print >> sys.stderr, "[%s] Well-trained indexings has been loaded." % (arrow.now()) 

	# perform a similarity query against the corpus
	sims = index[query_bow]
	print >> sys.stderr, "[%s] Performed a similarity query against the corpus." % (arrow.now())

	sims    = sorted(enumerate(sims), key=lambda item: -item[1])
	results = [ (id_list[ind], score) for ind, score in sims[:args.n] ]
	print results

if __name__ == "__main__":
	main()