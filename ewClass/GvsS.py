#Just here for archival purposes and if its needed later. It never should be called

import ewcfg
import ewutils

class EwSeedPacket:
	item_type = "item"
	id_item = " "

	alias = []

	context = ""
	str_name = ""
	str_desc = ""

	cooldown = ""  # How long before they can plant another gaiaslimeoid
	cost = 0 # How much gaiaslime it costs to use
	time_nextuse = 0 # When they can next !plant it in a district
	durability = 0 # How many times it can be used in a raid before it runs out

	ingredients = ""
	enemytype = ""
	vendors = []
	acquisition = ""

	def __init__(
		self,
		id_item=" ",
		alias=[],
		context="",
		str_name="",
		str_desc="",
		cooldown=0,
		cost=0,
		time_nextuse=0,
		durability=0,
		ingredients="",
		enemytype="",
		vendors=[],
		acquisition = ""
	):
		self.item_type = "item"
		self.id_item = id_item
		self.alias = alias
		self.context = "seedpacket"
		self.str_name = str_name
		self.str_desc = str_desc
		self.cooldown = cooldown
		self.cost = cost
		self.time_nextuse = time_nextuse
		self.durability = 3
		self.ingredients = ingredients
		self.enemytype = enemytype
		self.vendors = vendors
		self.acquisition = acquisition

class EwTombstone:
	item_type = "item"
	id_item = " "

	alias = []

	context = ""
	str_name = ""
	str_desc = ""
	
	cost = 0 # How much gaiaslime it costs to use
	brainpower = 0 # Used for adding cooldowns to tombstone additions in graveyard ops
	stock = 0 # How many shamblers of that type it spawns
	durability = 0 # How many times it can be used in a raid before it runs out

	ingredients = ""
	enemytype = ""
	vendors = []
	acquisition = ""

	def __init__(
		self,
		id_item=" ",
		alias=[],
		context="",
		str_name="",
		str_desc="",
		cost=0,
		brainpower=0,
		stock=0,
		durability=0,
		ingredients="",
		enemytype="",
		vendors=[],
		acquisition = "",
	):
		self.item_type = "item"
		self.id_item = id_item
		self.alias = alias
		self.context = "tombstone"
		self.str_name = str_name
		self.str_desc = str_desc
		self.cost = cost
		self.brainpower = brainpower
		self.stock = stock
		self.durability = 3
		self.ingredients = ingredients
		self.enemytype = enemytype
		self.vendors = vendors
		self.acquisition = acquisition
		
class EwOperationData:
	
	# The ID of the user who chose a seedpacket/tombstone for that operation
	id_user = 0
	
	# The district that the operation takes place in
	district = ""
	
	# The enemytype associated with that seedpacket/tombstone.
	# A single Garden Ganker can not choose two of the same enemytype. No duplicate tombstones are allowed at all.
	enemytype = ""
	
	# The 'faction' of whoever chose that enemytype. This is either set to 'gankers' or 'shamblers'.
	faction = ""
	
	# The ID of the item used in the operation
	id_item = 0
	
	# The amount of shamblers stored in a tombstone.
	shambler_stock = 0

	def __init__(
		self,
		id_user = -1,
		district = "",
		enemytype = "",
		faction = "",
		id_item = -1,
		shambler_stock = 0,
	):
		self.id_user = id_user
		self.district = district
		self.enemytype = enemytype
		self.faction = faction
		self.id_item = id_item
		self.shambler_stock = shambler_stock
		
		if(id_user != ""):

			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor()
	
				# Retrieve object
				cursor.execute("SELECT {}, {}, {} FROM gvs_ops_choices WHERE {} = %s AND {} = %s AND {} = %s".format(
					ewcfg.col_faction,
					ewcfg.col_id_item,
					ewcfg.col_shambler_stock,
					
					ewcfg.col_id_user,
					ewcfg.col_district,
					ewcfg.col_enemy_type
				), (
					self.id_user,
					self.district,
					self.enemytype,
				))
				result = cursor.fetchone()
	
				if result != None:
					# Record found: apply the data to this object.
					self.faction = result[0]
					self.id_item = result[1]
					self.shambler_stock = result[2]
				else:
					# Create a new database entry if the object is missing.
					cursor.execute("REPLACE INTO gvs_ops_choices({}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s)".format(
						ewcfg.col_id_user,
						ewcfg.col_district,
						ewcfg.col_enemy_type,
						ewcfg.col_faction,
						ewcfg.col_id_item,
						ewcfg.col_shambler_stock,
					), (
						self.id_user,
						self.district,
						self.enemytype,
						self.faction,
						self.id_item,
						self.shambler_stock,
					))
	
					conn.commit()

			finally:
				# Clean up the database handles.
				cursor.close()
				ewutils.databaseClose(conn_info)

	def persist(self):
		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

			# Save the object.
			cursor.execute("REPLACE INTO gvs_ops_choices({}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s)".format(
				ewcfg.col_id_user,
				ewcfg.col_district,
				ewcfg.col_enemy_type,
				ewcfg.col_faction,
				ewcfg.col_id_item,
				ewcfg.col_shambler_stock
			), (
				self.id_user,
				self.district,
				self.enemytype,
				self.faction,
				self.id_item,
				self.shambler_stock
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)
	
	def delete(self):
		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

			cursor.execute("DELETE FROM gvs_ops_choices WHERE {id_user} = %s AND {enemytype} = %s AND {district} = %s".format(
				id_user=ewcfg.col_id_user,
				enemytype=ewcfg.col_enemy_type,
				district=ewcfg.col_district,
			), (
				self.id_user,
				self.enemytype,
				self.district
			))
			
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)
