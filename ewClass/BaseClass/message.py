
#Putting a code word here so I remember when I search the files #TODO
#DIOTODO -- Finish the class and all the methods docstrings

import ewutils
import ewcfg
import ewrolemgr
from ewClass import EwBasic

class EwResponse(EwBasic):
	""" Class for storing, passing, editing and posting channel responses and topics\n
    	Attributes:
            ~~~~{inherited: EwBasic}~~~~\n
		    'id_server': int -- ID for the last server used\n
		    'name': string -- General name string\n

            ~~~~{Unique}~~~~\n
            'client': discord.Client -- The dicord client for the bot\n
	        'channel_responses': dict -- ?\n
	        'channel_topics': dict -- ?\n
	        'members_to_update': list -- ?\n
        Methods:
            ~~~~{inherited: EwBasic}~~~~\n
		    'access_database' -- Access the database through a sequel query\n

            ~~~~{Unique}~~~~\n
            '__init__' -- Constructor for this class\n
			'add_channel_response' -- 

	"""

	client = None
	channel_responses = {}
	channel_topics = {}
	members_to_update = []

	def __init__(self, id_server = None):
		self.client = ewutils.get_client()
		self.id_server = id_server
		self.channel_responses = {}
		self.channel_topics = {}
		self.members_to_update = []

	def add_channel_response(self, channel, response):
		if channel in self.channel_responses:
			self.channel_responses[channel].append(response)
		else:
			self.channel_responses[channel] = [response]

	def add_channel_topic(self, channel, topic):
		self.channel_topics[channel] = topic

	def add_member_to_update(self, member):
		for update_member in self.members_to_update:
			if update_member.id == member.id:
				return

		self.members_to_update.append(member)

	def add_response_container(self, resp_cont):
		for ch in resp_cont.channel_responses:
			responses = resp_cont.channel_responses[ch]
			for r in responses:
				self.add_channel_response(ch, r)

		for ch in resp_cont.channel_topics:
			self.add_channel_topic(ch, resp_cont.channel_topics[ch])

		for member in resp_cont.members_to_update:
			self.add_member_to_update(member)

	def format_channel_response(self, channel, member):
		if channel in self.channel_responses:
			for i in range(len(self.channel_responses[channel])):
				self.channel_responses[channel][i] = ewutils.formatMessage(member, self.channel_responses[channel][i])

	async def post(self, channel=None):
		#self.client = ewutils.get_client()
		messages = []

		if self.client == None:
			ewutils.logMsg("Couldn't find client")
			return messages

		server = self.client.get_guild(int(self.id_server))
		if server == None:
			ewutils.logMsg("Couldn't find server with id {}".format(self.id_server))
			return messages

		for member in self.members_to_update:
			await ewrolemgr.updateRoles(client = self.client, member = member)

		for ch in self.channel_responses:
			if channel == None:
				current_channel = ewutils.get_channel(server = server, channel_name = ch)
				if current_channel == None:
					current_channel = ch
			else:
				current_channel = channel
			try:
				response = ""
				while len(self.channel_responses[ch]) > 0:
					if len(self.channel_responses[ch][0]) > ewcfg.discord_message_length_limit:
						response += "\n" + self.channel_responses[ch].pop(0)
						length = len(response)

						split_list = [(response[i:i+2000]) for i in range(0, length, 2000)]
						for blurb in split_list:
							message = await ewutils.send_message(self.client, current_channel, blurb)
							messages.append(message)
						response = ""
					elif len(response) == 0 or len("{}\n{}".format(response, self.channel_responses[ch][0])) < ewcfg.discord_message_length_limit:
						response += "\n" + self.channel_responses[ch].pop(0)
					else:
						message = await ewutils.send_message(self.client, current_channel, response)
						messages.append(message)
						response = ""
				message = await ewutils.send_message(self.client, current_channel, response)
				messages.append(message)
			except:
				ewutils.logMsg('Failed to send message to channel {}: {}'.format(ch, self.channel_responses[ch]))
				

		# for ch in self.channel_topics:
		# 	channel = get_channel(server = server, channel_name = ch)
		# 	try:
		# 		await channel.edit(topic = self.channel_topics[ch])
		# 	except:
		# 		logMsg('Failed to set channel topic for {} to {}'.format(ch, self.channel_topics[ch]))

		return messages
