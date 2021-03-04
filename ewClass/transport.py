
import asyncio

import ewcfg
import ewutils

from ewClass.poi import EwDistrict
"""
	Database Object for public transportation vehicles, such as ferries or subway trains
"""
class EwTransport:
	# server id
	id_server = -1

	# id of the EwPoi object for this transport
	poi = ""

	# string describing the kind of vehicle it is
	transport_type = ""

	# which line the vehicle follows. see EwTransportLine object
	current_line = ""

	# connection to the world map
	current_stop = ""

	""" Retrieve object from database, or initialize it, if it doesn't exist yet """
	def __init__(self, id_server = None, poi = None):
		if id_server is not None and poi is not None:
			self.id_server = id_server
			self.poi = poi
			try:
				data = ewutils.execute_sql_query("SELECT {transport_type}, {current_line}, {current_stop} FROM transports WHERE {id_server} = %s AND {poi} = %s".format(
						transport_type = ewcfg.col_transport_type,
						current_line = ewcfg.col_current_line,
						current_stop = ewcfg.col_current_stop,
						id_server = ewcfg.col_id_server,
						poi = ewcfg.col_poi
					),(
						self.id_server,
						self.poi
					))
				# Retrieve data if the object was found
				if len(data) > 0:
					self.transport_type = data[0][0]
					self.current_line = data[0][1]
					self.current_stop = data[0][2]
				# initialize it per the Poi default otherwise
				else:
					poi_data = ewcfg.id_to_poi.get(self.poi)
					if poi_data is not None:
						self.transport_type = poi_data.transport_type
						self.current_line = poi_data.default_line
						self.current_stop = poi_data.default_stop

						self.persist()
			except:
				ewutils.logMsg("Failed to retrieve transport {} from database.".format(self.poi))

	""" Write object to database """
	def persist(self):

		try:
			ewutils.execute_sql_query("REPLACE INTO transports ({id_server}, {poi}, {transport_type}, {current_line}, {current_stop}) VALUES (%s, %s, %s, %s, %s)".format(
					id_server = ewcfg.col_id_server,
					poi = ewcfg.col_poi,
					transport_type = ewcfg.col_transport_type,
					current_line = ewcfg.col_current_line,
					current_stop = ewcfg.col_current_stop
				),(
					self.id_server,
					self.poi,
					self.transport_type,
					self.current_line,
					self.current_stop
				))
		except:
			ewutils.logMsg("Failed to write transport {} to database.".format(self.poi))

	""" Makes the object move across the world map. Called once at client startup for every object """
	async def move_loop(self):
		response = ""
		poi_data = ewcfg.id_to_poi.get(self.poi)
		last_messages = []
		while not ewutils.TERMINATE:

			district_data = EwDistrict(district = self.poi, id_server = self.id_server)

			if district_data.is_degraded():
				return

			transport_line = ewcfg.id_to_transport_line[self.current_line]
			client = ewutils.get_client()
			resp_cont = ewutils.EwResponseContainer(client = client, id_server = self.id_server)

			if self.current_stop == transport_line.last_stop:
				self.current_line = transport_line.next_line
				self.persist()
			else:
				schedule = transport_line.schedule[self.current_stop]
				await asyncio.sleep(schedule[0])
				for message in last_messages:
					try:
						await message.delete()
						pass
					except:
						ewutils.logMsg("Failed to delete message while moving transport {}.".format(transport_line.str_name))
				self.current_stop = schedule[1]
				self.persist()

				stop_data = ewcfg.id_to_poi.get(self.current_stop)

				# announce new stop inside the transport
				# if stop_data.is_subzone:
				# 	stop_mother = ewcfg.id_to_poi.get(stop_data.mother_district)
				# 	response = "We have reached {}.".format(stop_mother.str_name)
				# else:
				response = "We have reached {}.".format(stop_data.str_name)

				next_line = transport_line

				if stop_data.is_transport_stop:
					response += " You may exit now."

				if stop_data.id_poi == transport_line.last_stop:
					next_line = ewcfg.id_to_transport_line[transport_line.next_line]
					response += " This {} will proceed on {}.".format(self.transport_type, next_line.str_name.replace("The", "the"))
				else:
					next_stop = ewcfg.id_to_poi.get(transport_line.schedule.get(stop_data.id_poi)[1])
					if next_stop.is_transport_stop:
						# if next_stop.is_subzone:
						# 	stop_mother = ewcfg.id_to_poi.get(next_stop.mother_district)
						# 	response += " The next stop is {}.".format(stop_mother.str_name)
						# else:
						response += " The next stop is {}.".format(next_stop.str_name)
				resp_cont.add_channel_response(poi_data.channel, response)

				# announce transport has arrived at the stop
				if stop_data.is_transport_stop:
					response = "{} has arrived. You may board now.".format(next_line.str_name)
					resp_cont.add_channel_response(stop_data.channel, response)
				elif self.transport_type == ewcfg.transport_type_ferry:
					response = "{} sails by.".format(next_line.str_name)
					resp_cont.add_channel_response(stop_data.channel, response)
				elif self.transport_type == ewcfg.transport_type_blimp:
					response = "{} flies overhead.".format(next_line.str_name)
					resp_cont.add_channel_response(stop_data.channel, response)


				last_messages = await resp_cont.post()


""" Object that defines a public transportation line """
class EwTransportLine:

	# name of the transport line
	id_line = ""

	# alternative names
	alias = []

	# Nice name for output
	str_name = ""

	# which stop the line starts at
	first_stop = ""

	# which stop the line ends at
	last_stop = ""

	# which line transports switch to after the last stop
	next_line = ""

	# how long to stay at each stop, and which stop follows
	schedule = {}

	def __init__(self,
		id_line = "",
		alias = [],
		str_name = "",
		first_stop = "",
		last_stop = "",
		next_line = "",
		schedule = {}
		):
		self.id_line = id_line
		self.alias = alias
		self.str_name = str_name
		self.first_stop = first_stop
		self.last_stop = last_stop
		self.next_line = next_line
		self.schedule = schedule
