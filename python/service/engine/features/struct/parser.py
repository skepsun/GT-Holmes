#!/usr/local/bin/python

from commonregex import CommonRegex
from geopy.geocoders import Nominatim
from os import listdir
import string
import nltk
import sys
import re

class StructData:

	def __init__(self, text, coordinates_boundary=None):

		parsed_text = CommonRegex(text) # Init regex parser
		emails      = parsed_text.emails
		phones      = parsed_text.phones
		links       = parsed_text.links
		dates       = parsed_text.dates
		times       = parsed_text.times
		addresses   = parsed_text.street_addresses

		geolocator  = Nominatim() # Init geo locator
		locations   = [ geolocator.geocode(address) for address in addresses ]
		coordinates = [ location.latitude, location.longitude for location in locations ]
		# todo: remove the coordinates which are not in the Atlanta areas

		