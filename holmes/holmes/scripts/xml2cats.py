#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""
import argparse
from xml.etree import ElementTree


def main():

	# Parse the input parameters
	parser = argparse.ArgumentParser(description="Script for parsing xml format crime records.")
	parser.add_argument("-p", "--path", required=True, help="The path of the input xml file")
	parser.add_argument("-o", "--output", required=True, help="The path of the output folder")
	parser.add_argument("-l", "--label", required=True, help="The label of this record")
	args = parser.parse_args()

	label     = args.label
	file_name = args.path.split("/")[-1].split(".")[0] 

	with open(args.path, "r") as f1, \
	     open("%s/%s_cats.txt" % (args.output, file_name), "w") as f2, \
	     open("%s/%s_remarks.txt" % (args.output, file_name), "w") as f3:
		tree = ElementTree.parse(f1)
		root = tree.getroot()

		last_id = "-1"
		text    = ""
		cats    = ""
		incident_id = "-1"
		for row in root:
			record = [ item.text for item in row ]

			try:
				incident_id, address, lat_str, long_str, call_date, call_time, remarks, _, _ = record
			except Exception as e:
				print e
				continue

			if incident_id == last_id or last_id == "-1":
				text += "".join(remarks.strip().split("\n"))
				# cats = "\t".join((incident_id, label, label, lat_str, long_str, call_date, lat_str, long_str))
			else:
				f2.write(cats + "\n")
				f3.write(text + "\n")
				text = "".join(remarks.strip().split("\n"))
				# cats = "\t".join((incident_id, label, label, lat_str, long_str, call_date, lat_str, long_str))
			cats = "\t".join((incident_id, label, label, call_date, lat_str, long_str))

			last_id = incident_id

		f2.write(cats + "\n")
		f3.write(text + "\n")

if __name__ == "__main__":
	main()