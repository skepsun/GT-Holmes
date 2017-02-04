#!/usr/local/bin/python
import sys

if __name__ == '__main__':

	# [ Sprout Unit ]
	# Primary key:	
	#   1. incident_id;
	# Attributes:	
	# - TAG 1: 
	#   2. incident_date, 3. cad_call_type, 4. call_type, 5. location, 6. avg_lat, 
	#   7. avg_long, 8. city, 9. command_area, 
	# - TAG 2:
	#   10. reporting_dst, 11. shift, 12. occur_date, 13. occur_time,
	#   14. how_committed
	# - TAG 3:
	#   15. remarks

	# Initiation
	incident_date = ''
	cad_call_type = ''
	call_type     = ''
	location      = ''
	avg_lat       = ''
	avg_long      = ''
	city          = ''
	command_area  = ''
	reporting_dst = ''
	shift         = ''
	occur_date    = ''
	occur_time    = ''
	how_committed = ''
	remarks       = ''

	last_incident_id = '-1'

	for line in sys.stdin:
		data = line.strip('\n').split('\t')
		if len(data) <= 2:
			print >> sys.stderr, '[ERROR] data: [%s] is insufficient.' % line
			continue
		incident_id = data[0]
		tag         = data[1]

		# Process data by incident id
		if incident_id != last_incident_id and last_incident_id != '-1':
			print '\t'.join([
				incident_id, incident_date, cad_call_type, call_type, \
				location, avg_lat, avg_long, city, command_area, reporting_dst, \
				shift, occur_date, occur_time, how_committed, remarks \
			])
			incident_date = ''
			cad_call_type = ''
			call_type     = ''
			location      = ''
			avg_lat       = ''
			avg_long      = ''
			city          = ''
			command_area  = ''
			reporting_dst = ''
			shift         = ''
			occur_date    = ''
			occur_time    = ''
			how_committed = ''
			remarks       = ''

		# Process data by tag
		try:
			if tag == '1':
				incident_date = data[2]
				cad_call_type = data[3]
				call_type     = data[4]
				location      = data[5]
				avg_lat       = data[6]
				avg_long      = data[7]
				city          = data[8]
				command_area  = data[9]
				# shift         = data[10]
			elif tag == '2':
				# location      = data[2]
				# city          = data[3]
				reporting_dst = data[4]
				# command_area  = data[5]
				shift         = data[6]
				occur_date    = data[7]
				occur_time    = data[8]
				how_committed = data[9]
			elif tag == '3':
				if remarks != '':
					remarks += '\2' # Separator of documents
				remarks += data[2]
		except Exception:
			print >> sys.stderr, 'Error! Invalid tag [%s] occurred. Line: [%s].' % (tag, line)
			continue

		last_incident_id = incident_id
