#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
import json
from nltk.corpus import stopwords
from nltk.tokenize.mwe import MWETokenizer

from engine.features.struct.text_feature import StructFeature



if __name__ == "__main__":
	# Basic configuration
	input_file_path = "../../tmp/woodie.validate_24_cases/incidents.stream"
	crime_code_path = "../../resource/CrimeCode.json"

	# Load crime codes dictionary
	crime_codes_dict = {}
	with open(crime_code_path, "r") as f:
		crime_codes_dict = json.load(f)

	with open(input_file_path, "r") as f:
		for line in f.readlines():
			incident_id, crime_code, text = line.strip().split("\t")
			struct = StructFeature(text)
			print "\t".join([incident_id, crime_code, str(struct)])



