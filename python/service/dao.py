#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script contains an abstract interface for connecting various kinds of database via standard
restful API and the data models that web service needs. Generally speaking, the data models that 
you implement in web service inherit from interface 'DBConnecter' for getting access to the 
database. 
"""

import json
import requests

class DBConnecter():
	"""
	A simple interface (abstract class) for connecting database via secured and standard 
	restful API. The data accessing API was provided by Loopback Database Wrapper, A simple
	loopback server. You can define your own result parser by overriding static method 
	"parse". 

	Parameters:
	- url:   Database restful API base url
	- token: Access token (required by the wrapper of database for safty)
	"""

	def __init__(self, url, token):
		if token == None:
			# TODO: If token was not set, it would request a new token from the server.
			# self.get_access_token()
			return 
		self.url     = url
		self.token   = token
		self.headers = { "Accept": "application/json", "Content-Type": "application/json" }

	def __getitem__(self, id):
		"""
		Rewrite built-in function __getitem__

		Retrieve one data item by its primary key, and return a python dict. The DAO (Data 
		Access Operation) was done by secured and standard Restful API which are provided 
		by Loopback Database Wrapper. 
		"""

		r = requests.get(url="%s/%s" % (self.url, id), headers=self.headers, 
			params={ "access_token": self.token }, verify=False)
		# Return result if success (status == 2XX)
		if r.status_code / 10 == 20:
			return self.parse(r.json())
		# Invalid request
		else:
			return r.json()

	def get(self, key, vals):
		"""
		Get Multiple Items

		Retrieve multiple data items by indicated key and its values. key is supposed to be
		a string, and vals is a list of values. Basically, this method is implemented by 
		sending a restful request with a filter parameter which contains a where filter. It
		would be a better way to fetch multiple data items rather than requesting by id for 
		many times. Noted that the response would return a list of intact data item, and 
		"parse" function would be applied here for each of the item by default. 
		"""

		key_vals = [ {key: val} for val in vals ]
		filter   = { "where": { "or": key_vals } }
		params   = { "access_token": self.token, "filter": json.dumps(filter) }
		r = requests.get(url=self.url, headers=self.headers, params=params, verify=False)
		# Return result if success (status == 2XX)
		if r.status_code / 10 == 20:
			return [ self.parse(item) for item in r.json() ]
		# Invalid request
		else:
			return r.json()

	@staticmethod
	def parse(result):
		"""
		Parse

		The static method would be invoked everytimes when __getitem__ was excuted (getting
		resource by id). it would help to parse the response and return to caller if this 
		method was overrided. In the abstract class DBConnecter, this method would do nothing
		but return response directly. 
		"""

		return result



class BasicInfo(DBConnecter):
	"""
	Basic Info 

	This class is a data model for the table "basic_info" of database "APD_Data" in local MySQL.
	Basically, this class persists a unique url (/api/basic_infos) for acquiring information
	from table "basic_info", and it also overrides the static method "parse" to extract specific
	fields of data from the raw response.
	"""

	def __init__(self, token):
		self.url   = "https://139.162.173.91:3000/api/basic_infos"
		self.token = token
		DBConnecter.__init__(self, self.url, self.token)

	@staticmethod
	def parse(result):
		"""
		Overriding of "parse" in DBConnecter
		
		
		"""
		try:
			avg_lat  = float(result["avg_lat"])/100000.0 
			avg_long = float(result["avg_long"])/100000.0 
			city     = result["city"]
			date     = int(result["incident_date"])
			priority = result["priority"]
		except Exception:
			raise("Invalid Data Format.")
			return None
			

		return result

if __name__ == "__main__":

	# dao = DBConnecter("https://139.162.173.91:3000/api/basic_infos", "gatech1234!")
	# print dao["161881787"]

	dao = DBConnecter("https://139.162.173.91:3000/api/basic_infos", "gatech1234!")
	print dao.get("incident_num", ["130010040", "130010041", "130010039"])
