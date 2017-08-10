#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import requests

class DBConnecter():
	"""
	Interface (abstract class) for Connecting database via standard restful API. 

	"""

	def __init__(self, url, token):
		if token == None:
			# TODO: If token was not set, it would request a new token from the server.
			# self.get_access_token()
			return 
		self.url    = url
		self.token  = token
		self.header = { "Accept": "application/json", "Content-Type": "application/json" }

	def __getitem__(self, id):
		r = requests.get(url=self.url + "/%s" % id, headers=self.header, 
			params={ "access_token": self.token }, verify=False)
		print r.status_code
		# Return result if success
		if r.status_code / 10 == 20: # status_code starts with 20*
			return r.json()
		# Invalid token
		elif r.status_code == 401:
			raise Exception("Invalid token")
		else:
			raise Exception("Failed to get value.")

	@staticmethod
	def get_access_token(email, password):
		pass

if __name__ == "__main__":

	dao = DBConnecter("https://139.162.173.91:3000/api/basic_infos", "gatech1234!")
	print dao["161881787"]
