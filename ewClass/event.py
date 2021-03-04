"""
	Database persistence object describing some discrete event. Player
	death/resurrection, item discovery, etc.
"""
class EwEvent:
	id_server = -1

	event_type = None

	id_user = None
	id_target = None

	def __init__(
		self,
		id_server = -1,
		event_type = None,
		id_user = None,
		id_target = None
	):
		self.id_server = id_server
		self.event_type = event_type
		self.id_user = id_user
		self.id_target = id_target

	"""
		Write event to the database.
	"""
	def persist(self):
		# TODO
		pass



class EwDungeonScene:

	# The text sent when a scene starts
	text = ""

	# Whether or not the dungeon is active
	dungeon_state = True

	# Where the scene is taking place
	poi = None

	# life state to assign for this scene
	life_state = None

	# Commands that can be used in a scene, and what scene ID that leads to
	options = {}

	def __init__(
			self,
			text="",
			dungeon_state=True,
			options={},
			poi=None,
			life_state=None,
	):
		self.text = text
		self.dungeon_state = dungeon_state
		self.options = options
		self.poi = poi
		self.life_state = life_state

class EwEventDef:
	event_type = ""
	
	str_event_start = ""
	str_event_end = ""

	def __init__(
		self,
		event_type = "",
		str_event_start = "",
		str_event_end = "",
	):
		self.event_type = event_type
		self.str_event_start = str_event_start
		self.str_event_end = str_event_end
		

class EwWorldEvent:
	id_event = -1
	id_server = -1
	event_type = ""
	time_activate = -1
	time_expir = -1

	event_props = None

	def __init__(
		self,
		id_event = None
	):
		if(id_event != None):
			self.id_event = id_event

			self.event_props = {}

			try:
				# Retrieve object
				result = ewutils.execute_sql_query("SELECT {}, {}, {}, {} FROM world_events WHERE id_event = %s".format(
					ewcfg.col_id_server,
					ewcfg.col_event_type,
					ewcfg.col_time_activate,
					ewcfg.col_time_expir,
				), (
					self.id_event,
				))

				if len(result) > 0:
					result = result[0]

					# Record found: apply the data to this object.
					self.id_server = result[0]
					self.event_type = result[1]
					self.time_activate = result[2]
					self.time_expir = result[3]

					# Retrieve additional properties
					props = ewutils.execute_sql_query("SELECT {}, {} FROM world_events_prop WHERE id_event = %s".format(
						ewcfg.col_name,
						ewcfg.col_value
					), (
						self.id_event,
					))

					for row in props:
						# this try catch is only necessary as long as extraneous props exist in the table
						try:
							self.event_props[row[0]] = row[1]
						except:
							ewutils.logMsg("extraneous event_prop row detected.")

				else:
					# Item not found.
					self.id_event = -1
			except:
				ewutils.logMsg("Error while retrieving world event {}".format(id_event))


	""" Save event data object to the database. """
	def persist(self):
		try:
			# Save the object.
			ewutils.execute_sql_query("REPLACE INTO world_events({}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s)".format(
				ewcfg.col_id_event,
				ewcfg.col_id_server,
				ewcfg.col_event_type,
				ewcfg.col_time_activate,
				ewcfg.col_time_expir,
			), (
				self.id_event,
				self.id_server,
				self.event_type,
				self.time_activate,
				self.time_expir,
			))

			# Remove all existing property rows.
			ewutils.execute_sql_query("DELETE FROM world_events_prop WHERE {} = %s".format(
				ewcfg.col_id_event
			), (
				self.id_event,
			))

			# Write out all current property rows.
			for name in self.event_props:
				ewutils.execute_sql_query("INSERT INTO world_events_prop({}, {}, {}) VALUES(%s, %s, %s)".format(
					ewcfg.col_id_event,
					ewcfg.col_name,
					ewcfg.col_value
				), (
					self.id_event,
					name,
					self.event_props[name]
				))
		except:
			ewutils.logMsg("Error while persisting world event {}".format(self.id_event))
