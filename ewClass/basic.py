
import MySQLdb
import time
import ewutils
import ewcfg

class EwBasic:
	""" Basic class that contains all the general variables and methods that are inherited
    by most or all other classes
	Attributes:
		'id_server': int -- ID for the last server used
		'name': string -- General name string
    Methods:
		'access_database' -- Access the database through a sequel query
	"""
	id_server = -1
	name = ""

	def access_database(self, query, replacements = None):
		""" Access the database through a sequel query. Returns database data if requested\n
		Parameters:
			'query': string -- SQL query string for database instructions\n
			'replacements': string -- The data entries to replace in the database if necessary\n
		Return: undefined -- Database data if requested in the query, otherwise None
		"""
		return ewutils.execute_sql_query(query, replacements)


class EwCharacter(EwBasic):
	""" Character class to manage general character methods and variables.\n
	Parameters:
		'char_type': string -- Character type, as in Enemy, Player, etc.\n
		'slime': int -- Amount of slime in the character\n
		'slimelevel': int -- Character's level, like in an rpg\n
		'poi': string -- Location the character is in\n
		'life_state': int -- How your character is doing in\n
		'attacktype': string -- Weapon class or type of this character\n
		'bleed_storage': int -- Blood storage for the "bleeding" mechanic\n
		'faction': string -- Character's faction affiliation\n
		'self_status': string -- Status that are applied to the character\n
    Methods:
		'slime_bylevel' -- Calculate the slime amount needed to reach a certain level\n
		'level_byslime' -- Calculate what level the character should be at, given their slime amount\n
	"""
	char_type = ""
	slime = 0
	slimelevel = 0
	poi = ""
	life_state = 0
	attacktype = "" 
	bleed_storage = 0 
	faction = ""
	self_status = "" 

	def slime_bylevel(self):
		""" Calculate the slime amount needed to reach a certain level.\n
		Return: int -- Slime amount needed
		"""
		return int(self.slimelevel ** 4)

	
	def level_byslime(self):
		""" Calculate what level the character should be at, given their slime amount.\n
		Return: int -- Level equivalent to the slime
		"""
		return int(abs(self.slime) ** 0.25)


class EwServer(EwBasic):
	"""EwServer is a representation of a server, if the name of the server or
	other meta data is needed in a scope where it's not normally available.\n
	Parameters:
		'icon': string -- Server icon link
	Methods:
		'__init__' -- Create or retrieve a server object from data in the database\n
		'persist' -- Save server data object to the database
	"""
	icon = ""

	def __init__(
		self,
		id_server = None
	):
		if(id_server != None):
			self.id_server = id_server

		# Retrieve object
		result = self.access_database("SELECT {}, {} FROM servers WHERE id_server = %s".format(
			ewcfg.col_name,
			ewcfg.col_icon
		), (self.id_server, ))
		result = result[0]

		if result != None:
			# Record found: apply the data to this object.
			self.name = result[0]
		else:
			# Create a new database entry if the object is missing.
			self.access_database("REPLACE INTO servers({}) VALUES(%s)".format(
				ewcfg.col_id_server
			), (
				self.id_server,
			))


	
	def persist(self):
		""" Save server data object to the database. """
		if self.icon == None:
			self.icon = ""

		# Save the object.
		self.access_database("REPLACE INTO servers({}, {}, {}) VALUES(%s, %s, %s)".format(
			ewcfg.col_id_server,
			ewcfg.col_name,
			ewcfg.col_icon
		), (
			self.id_server,
			self.name,
			self.icon
		))

