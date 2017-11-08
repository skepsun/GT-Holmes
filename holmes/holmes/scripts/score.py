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



def query_crime_record(incident_id, driver, server, database, uid, password):
	# Connecting to the database
	cnxn   = pyodbc.connect("Driver={%s};Server=%s;Database=%s;Uid=%s;Pwd=%s;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;" 
		% (driver, server, database, uid, password))
	cursor = cnxn.cursor()
	# Perform the query by incident id
	cursor.execute("SELECT * FROM IncidentNarrativeView WHERE IncidentId=%s;" % (incident_id))
	return cursor.fetchone()



def main():
	# Parse the input parameters
	parser = argparse.ArgumentParser(description="Script for parsing xml format crime records.")
	parser.add_argument("-q", "--query_id", required=True, help="The query id")
	parser.add_argument("-n", "--num", default=1, type=int, help="Return the top n results")
	parser.add_argument("-s", "--score", default=0.0, type=float, help="Return the results that have the similarities above the threshold")
	parser.add_argument("-c", "--config", required=True, help="The path of the configuration file")
	args = parser.parse_args()

	# Read configuration from ini file
	conf = Config(args.config)
	# Get configuration of the model
	pruned_dict_path = conf.get_section("Model")["pruned_dict_path"]
	id_info_path     = conf.get_section("Model")["id_info_path"]
	index_path       = conf.get_section("Model")["index_path"]
	# Get configuration of the database connection
	driver   = conf.get_section("Database")["driver"]
	server   = conf.get_section("Database")["server"]
	database = conf.get_section("Database")["database"]
	uid      = conf.get_section("Database")["uid"]
	password = conf.get_section("Database")["password"]

	# Loading Id information
	id_list = load_id_info(id_info_path)
	print >> sys.stderr, "[%s] Ids list has been loaded %s... ." % (arrow.now(), id_list[:5])

	# Query raw data via the query_id and get the narratives
	query_res   = query_crime_record(args.query_id, driver, server, database, uid, password)
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

	sims = sorted(enumerate(sims), key=lambda item: -item[1])
	# Return the similarities that above the threshold
	if args.score != 0.0:
		results = [ (id_list[ind], score) for ind, score in sims if score >= args.score ]
	# Return the top n results
	results = [ (id_list[ind], score) for ind, score in results[:args.num] ]
	print >> sys.stderr, "[%s] Results have been output to the stdout." % (arrow.now())
	print results

if __name__ == "__main__":
	main()