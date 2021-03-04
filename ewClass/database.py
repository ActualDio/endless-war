
import MySQLdb
import time
import ewutils
import ewcfg

db_pool = {}
db_pool_id = 0
""" Basic class that contains all the general variables and methods that are inherited
    by most or all other classes that interact with the database

    Methods:
        > databaseConnect() -> Opens a connection to the central database
		> databaseClose(conn_info) -> Closes the active connection  
"""
class EwDatabase:
    id_server = -1
    name = ""

    def __init__(self, id_server = -1, name = ""):
        self.id_server = id_server
        self.name = name


    """ Opens a connection to the central database. Returns the "conn_info" dictionary with 
		the general information of the connection
	"""
    def databaseConnect():
        conn_info = None

        conn_id_todelete = []

        global db_pool 
        global db_pool_id

        # Iterate through open connections and find the currently active one.
        for pool_id in db_pool:
            conn_info_iter = db_pool.get(pool_id)

            if conn_info_iter['closed'] == True:
                if conn_info_iter['count'] <= 0:
                    conn_id_todelete.append(pool_id)
            else:
                conn_info = conn_info_iter

        # Close and remove dead connections.
        if len(conn_id_todelete) > 0:
            for pool_id in conn_id_todelete:
                conn_info_iter = db_pool[pool_id]
                conn_info_iter['conn'].close()

                del db_pool[pool_id]

        # Create a new connection.
        if conn_info == None:
            db_pool_id += 1
            conn_info = {
            'conn': MySQLdb.connect(host = "localhost", user = "rfck-bot", passwd = "rfck" , db = ewcfg.database, charset = "utf8"),
                'created': int(time.time()),
                'count': 1,
                'closed': False
            }
            db_pool[db_pool_id] = conn_info
        else:
            conn_info['count'] += 1

        return conn_info

    """ Closes (maybe) the active database connection. Takes a dictionary 
		containing the connection info as its only argument
	"""
    def databaseClose(conn_info):
	    conn_info['count'] -= 1

	    # Expire old database connections.
	    if (conn_info['created'] + 60) < int(time.time()):
		    conn_info['closed'] = True


"""
	EwServer is a representation of a server, if the name of the server or
	other meta data is needed in a scope where it's not normally available.
	
		Methods:
			> persist(self) -> Save a server data object to the database
"""
class EwServer(EwDatabase):

	icon = ""

	def __init__(
		self,
		id_server = None
	):
		if(id_server != None):
			self.id_server = id_server

			try:
				conn_info = self.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor()

				# Retrieve object
				cursor.execute("SELECT {}, {} FROM servers WHERE id_server = %s".format(
					ewcfg.col_name,
					ewcfg.col_icon
				), (self.id_server, ))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.name = result[0]
				else:
					# Create a new database entry if the object is missing.
					cursor.execute("REPLACE INTO servers({}) VALUES(%s)".format(
						ewcfg.col_id_server
					), (
						self.id_server,
					))

					conn.commit()
			finally:
				# Clean up the database handles.
				cursor.close()
				self.databaseClose(conn_info)

	""" Save server data object to the database. """
	def persist(self):
		if self.icon == None:
			self.icon = ""

		try:
			conn_info = self.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

			# Save the object.
			cursor.execute("REPLACE INTO servers({}, {}, {}) VALUES(%s, %s, %s)".format(
				ewcfg.col_id_server,
				ewcfg.col_name,
				ewcfg.col_icon
			), (
				self.id_server,
				self.name,
				self.icon
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			self.databaseClose(conn_info)
