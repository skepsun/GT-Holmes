#!/usr/local/bin/python
import sys
import xlrd
import json
import datetime

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
	incident_id = ''
	type_desc   = set()
	type_id     = set()
	officer_id  = ''
	location    = ''
	avg_lat     = ''
	avg_long    = ''
	occur_time  = ''
	remarks     = ''

	last_incident_id = '-1'
	last_tag         = '-1'
	last_remark      = '-1'

	for line in sys.stdin:
		data = line.strip('\n').split('\t')
		if len(data) <= 2:
			print >> sys.stderr, '[ERROR] data: [%s] is insufficient.' % line
			continue
		incident_id = data[0]
		tag         = data[1]

		# Processing a new incident
		if incident_id != last_incident_id and last_incident_id != '-1':
			type_desc = '#'.join(list(type_desc))
			type_id   = '#'.join(list(type_id))
			print '\t'.join((
				incident_id, type_desc, type_id, location, avg_lat, 
				avg_long, officer_id, occur_time, remarks
			))
			# res_dict['incidents_info'].append({
			# 	'incident_id': incident_id,
			# 	'type_desc': list(type_desc),
			# 	'type_id': list(type_id),
			# 	'location': location,
			# 	'avg_lat': avg_lat,
			# 	'avg_long': avg_long,
			# 	'occur_time': occur_time,
			# 	'officer_id': officer_id
			# })
			type_desc   = set()
			type_id     = set()
			officer_id  = ''
			location    = ''
			avg_lat     = ''
			avg_long    = ''
			occur_time  = ''
			remarks     = ''
			last_remark = '-1'
		# Processing a new tag for the same incident
		elif tag == '1':
			avg_long = str(float(data[2])/100000)
			avg_lat  = str(float(data[3])/100000)
		elif tag == '2':
			location   = data[2]
			occur_date = datetime.datetime(*xlrd.xldate_as_tuple(float(data[10]), 0))
			occur_hour = int(data[11][0:2])
			occur_min  = int(data[11][2:4])
			occur_time = str(occur_date + datetime.timedelta(hours=occur_hour) + datetime.timedelta(minutes=occur_min))
			officer_id = data[16]
		elif tag == '3':
			type_desc.add(data[2])
			type_id.add(data[3])
		elif tag == '4':
			if remarks != '':
				remarks += '\2' # Separator of documents
			# If current remarks is the same with the last one,
			# Then abandon this remarks
			if data[2] != last_remark:
				remarks += data[2]
			else:
				# TODO: Count the number of duplicate content
				print >> sys.stderr, '[ERROR] Abandon the same remarks.'
			last_remark = data[2]

		last_incident_id = incident_id