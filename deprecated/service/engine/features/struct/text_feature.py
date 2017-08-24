#!/usr/local/bin/python

from commonregex import CommonRegex
from os import listdir
import geopy
import string
import nltk
import sys
import re

class StructFeature:
	"""

	"""

	def __init__(self, text, coordinates_boundary=None):

		parsed_text = CommonRegex(text) # Init regex parser
		self.emails = list(set(parsed_text.emails))
		self.phones = list(set(parsed_text.phones))
		self.links  = list(set(parsed_text.links))
		self.dates  = list(set(parsed_text.dates))
		self.times  = list(set(parsed_text.times))
		self.addresses = list(set(parsed_text.street_addresses))

		# geolocator  = geopy.geocoders.Nominatim() # Init geo locator
		# try: 
		# 	locations = [ geolocator.geocode(address) for address in self.addresses ]
		# 	self.coordinates = [ [location.latitude, location.longitude] 
		# 		for location in locations if location is not None]
		# except Exception, msg:
		# 	print >> sys.stderr, "There is an exception of geopy, %s" % msg
		# 	self.coordinates = None
		
		# todo: remove the coordinates which are not in the Atlanta areas
		
	def __str__(self):
		"""

		"""
		return  "\t".join([ "#".join(feature) for feature in 
			[self.addresses, self.dates, self.times, self.emails, self.phones, self.links] ])