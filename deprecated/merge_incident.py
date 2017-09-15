#!/usr/local/bin/python
import sys

if __name__ == '__main__':

	# Initiation
	incident_date = ''
	location      = ''
	crime_code_1  = ''
	crime_code_2  = ''
	remarks       = ''

	last_incident_id = '-1'

	for line in sys.stdin:
		data = line.strip('\n').split('\t')
		if len(data) <= 2:
			print >> sys.stderr, '[ERROR] data: [%s] is insufficient.' % line
			continue
		incident_id = data[0].strip()
		tag         = data[1]

		# Process data by incident id
		if incident_id != last_incident_id and last_incident_id != '-1':
			print '\t'.join([incident_id, incident_date, crime_code_1, crime_code_2, location, remarks])
			incident_date = ''
			location      = ''
			crime_code_1  = ''
			crime_code_2  = ''
			remarks       = ''

		# Process data by tag
		try:
			if tag == '1':
				incident_date = data[3]
				location      = data[2]
			elif tag == '2':
				if crime_code_1 != '':
					crime_code_1 += '#'
				crime_code_1 += data[3]
				if crime_code_2 != '':
					crime_code_2 += '#'
				crime_code_2 += data[2]
			elif tag == '3':
				if remarks != '':
					remarks += '\2' # Separator of documents
				remarks += data[2]
		except Exception:
			print >> sys.stderr, 'Error! Invalid tag [%s] occurred. Line: [%s].' % (tag, line)
			continue

		last_incident_id = incident_id
