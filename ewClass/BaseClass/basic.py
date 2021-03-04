
#import MySQLdb
import ewutils

class EwBasic:
	""" Basic class that contains all the general variables and methods that are inherited
    by most or all other classes\n
	Attributes:
		'id_server': int -- ID for the last server used\n
		'name': string -- General name string\n
    Methods:
		'access_database' -- Access the database through a sequel query\n
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

# class EwServer(EwBasic):
# 	"""EwServer is a representation of a server, if the name of the server or
# 	other meta data is needed in a scope where it's not normally available.\n
# 	Parameters:
# 		'icon': string -- Server icon link
# 	Methods:
# 		'__init__' -- Create or retrieve a server object from data in the database\n
# 		'persist' -- Save server data object to the database
# 	"""
# 	icon = ""

# 	def __init__(
# 		self,
# 		id_server = None
# 	):
# 		if(id_server != None):
# 			self.id_server = id_server

# 		# Retrieve object
# 		result = self.access_database("SELECT {}, {} FROM servers WHERE id_server = %s".format(
# 			ewcfg.col_name,
# 			ewcfg.col_icon
# 		), (self.id_server, ))
# 		result = result[0]

# 		if result != None:
# 			# Record found: apply the data to this object.
# 			self.name = result[0]
# 		else:
# 			# Create a new database entry if the object is missing.
# 			self.access_database("REPLACE INTO servers({}) VALUES(%s)".format(
# 				ewcfg.col_id_server
# 			), (
# 				self.id_server,
# 			))


	
# 	def persist(self):
# 		""" Save server data object to the database. """
# 		if self.icon == None:
# 			self.icon = ""

# 		# Save the object.
# 		self.access_database("REPLACE INTO servers({}, {}, {}) VALUES(%s, %s, %s)".format(
# 			ewcfg.col_id_server,
# 			ewcfg.col_name,
# 			ewcfg.col_icon
# 		), (
# 			self.id_server,
# 			self.name,
# 			self.icon
# 		))

