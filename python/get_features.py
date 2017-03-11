#!/usr/local/bin/python

from gensim.models import Word2Vec
from collections import Counter
from nltk.corpus import stopwords
import numpy as np
import argparse
import string
import json
import sys
import re

from lib.narratives.text import TextAnalysor
from lib.utils import Config

FEATURES_INI_PATH = 'conf/feature.ini'

if __name__ == '__main__':

	# Parse input parameters
	parser = argparse.ArgumentParser()
	parser.add_argument('--load_text_analysor_var', action="store_true", help='load the data to the text_analysor')
	parser.add_argument('--save_text_analysor_var', action="store_true", help='save the data in the text_analysor')
	parser.add_argument('--text_analysor_path', type=str, help='path for text analysor')
	parser.add_argument('--id_index', default=0, type=int, help='index of incident id')
	parser.add_argument('--code_index', default=1, type=int, help='index of crime code')
	parser.add_argument('--remarks_index', default=2, type=int, help='index of remarks')
	args = parser.parse_args()
	id_index           = args.id_index
	code_index         = args.code_index
	remarks_index      = args.remarks_index
	max_index          = max((id_index, code_index, remarks_index))
	text_analysor_path = ''
	if args.load_text_analysor_var or args.save_text_analysor_var:
		text_analysor_path = args.text_analysor_path
	print >> sys.stderr, '[INFO] Index of Incident ID: %d' % id_index
	print >> sys.stderr, '[INFO] Index of Crime Codes: %d' % code_index
	print >> sys.stderr, '[INFO] Index of Remarks: %d' % remarks_index
	print >> sys.stderr, '[INFO] Path for data of text analysor: %s' % text_analysor_path

	# Read configuration from ini file
	conf = Config(FEATURES_INI_PATH)
	# Read Crime Codes Descriptions
	crime_codes_desc_path = conf.config_section_map('Labels')['crime_codes_desc']
	print >> sys.stderr, '[INFO] Loading Crime Codes Dictionary...'
	with open(crime_codes_desc_path, 'rb') as f:
		crime_codes_dict = json.load(f)

	# Initialize the text analysor
	text_analysor = TextAnalysor()
	print >> sys.stderr, '[INFO] Loading text analysor...'
	if args.load_text_analysor_var:
		text_analysor.load_variables(text_analysor_path)
		

	# Process the data stream from stdin
	i = 0
	for line in sys.stdin:
		data = line.strip('\n').split('\t')
		# Check the number of the fields
		if len(data) < max_index:
			print >> sys.stderr, '[ERROR] data: [%s] is insufficient.' % line
			continue
		incident_id = data[id_index]
		crime_code  = data[code_index]
		remarks     = data[remarks_index]
		# timestamp    = data[1]
		# crime_code_2 = data[3]
		# location     = data[4]

		print >> sys.stderr, '[INFO] No. %d, Incident Id: %s, Labels: %s' % (i, incident_id, crime_code)
		try:
			crime_types = list(set(crime_code.split('#')))
			text_analysor.set_text(remarks, crime_types)
		except KeyboardInterrupt:
			# Save the results before exits.
			print >> sys.stderr, '[INFO] Saving text analysor...'
			if args.save_text_analysor_var:
				text_analysor.save_variables(text_analysor_path)
			# Then exit
			sys.exit(0)
		# except:
		# 	print >> sys.stderr, '[ERROR] Unknow failure occurred.'

		i += 1

	# Save the results before exits.
	if args.save_text_analysor_var:
		print >> sys.stderr, '[INFO] Saving text analysor...'
		text_analysor.save_variables(text_analysor_path)













