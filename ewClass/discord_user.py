
from ewClass.basic import EwBasic
import random
import time

import ewcfg
import ewutils
from ewClass.poi import EwDistrict

class EwDiscordUser(EwBasic):
	""" EwDiscordUser is a representation of an actual player discord account. There is
	one record for each person, no matter how many servers they interact with
	endless-war on.\n
	Attributes:
		'id_user' : int -- The Discord User ID stored in the database.\n
		'avatar' : string -- The discord avatar for this user.\n
		(Inherited)'name' : string -- The user's display name.\n 
	Methods:
		'__init__' -- Accesses the database to populate the object or generates a new entry in the database.\n
		'persist' -- Save object data to the database.\n
	"""
	id_user = -1
	avatar = ""

	def __init__(
		self,
		id_user = None,
		id_server = None
	):
		if(id_user != None):
			self.id_user = id_user
			self.id_server = id_server

			# Retrieve object
			cursor = self.access_database("SELECT {}, {}, {} FROM players WHERE id_user = %s".format(
				ewcfg.col_id_server,
				ewcfg.col_avatar,
				ewcfg.col_display_name
			), (self.id_user, ))
			result = cursor[0]

			if result != None:
				# Record found: apply the data to this object.
				self.id_server = result[0]
				self.avatar = result[1]
				self.name = result[2]
			elif id_server != None:
				# Create a new database entry if the object is missing.
				self.access_database("REPLACE INTO players({}, {}) VALUES(%s, %s)".format(
					ewcfg.col_id_user,
					ewcfg.col_id_server
				), (
					self.id_user,
					self.id_server
				))

	def persist(self):
		""" Save user data object to the database. """
		self.access_database("REPLACE INTO players({}, {}, {}, {}) VALUES(%s, %s, %s, %s)".format(
			ewcfg.col_id_user,
			ewcfg.col_id_server,
			ewcfg.col_avatar,
			ewcfg.col_display_name
		), (
			self.id_user,
			self.id_server,
			self.avatar,
			self.name
		))


