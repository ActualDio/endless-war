
from ewClass.basic import EwBasic
import ewcfg
import ewutils
	

class EwResponseContainer(EwBasic):
	""" Class for storing, passing, editing and posting channel responses and topics

	"""
	client = None
	channel_responses = {}
	channel_topics = {}
	members_to_update = []

	def __init__(self, client = None, id_server = None):
		self.client = client
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
				self.channel_responses[channel][i] = formatMessage(member, self.channel_responses[channel][i])

	async def post(self, channel=None):
		self.client = ewutils.get_client()
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
				current_channel = get_channel(server = server, channel_name = ch)
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
							message = await send_message(self.client, current_channel, blurb)
							messages.append(message)
						response = ""
					elif len(response) == 0 or len("{}\n{}".format(response, self.channel_responses[ch][0])) < ewcfg.discord_message_length_limit:
						response += "\n" + self.channel_responses[ch].pop(0)
					else:
						message = await send_message(self.client, current_channel, response)
						messages.append(message)
						response = ""
				message = await send_message(self.client, current_channel, response)
				messages.append(message)
			except:
				logMsg('Failed to send message to channel {}: {}'.format(ch, self.channel_responses[ch]))
				

		# for ch in self.channel_topics:
		# 	channel = get_channel(server = server, channel_name = ch)
		# 	try:
		# 		await channel.edit(topic = self.channel_topics[ch])
		# 	except:
		# 		logMsg('Failed to set channel topic for {} to {}'.format(ch, self.channel_topics[ch]))

		return messages

class Message:
	# Send the message to this exact channel by name.
	channel = None

	# Send the message to the channel associated with this point of interest.
	id_poi = None

	# Should this message echo to adjacent points of interest?
	reverb = None
	message = ""

	def __init__(
		self,
		channel = None,
		reverb = False,
		message = "",
		id_poi = None
	):
		self.channel = channel
		self.reverb = reverb
		self.message = message
		self.id_poi = id_poi

	def readMessage(fname):
		msg = Message()

		try:
			f = open(fname, "r")
			f_lines = f.readlines()

			count = 0
			for line in f_lines:
				line = line.rstrip()
				count += 1
				if len(line) == 0:
					break

				args = line.split('=')
				if len(args) == 2:
					field = args[0].strip().lower()
					value = args[1].strip()

					if field == "channel":
						msg.channel = value.lower()
					elif field == "poi":
						msg.poi = value.lower()
					elif field == "reverb":
						msg.reverb = True if (value.lower() == "true") else False
				else:
					count -= 1
					break

			for line in f_lines[count:]:
				msg.message += (line.rstrip() + "\n")
		except:
			logMsg('failed to parse message.')
			traceback.print_exc(file = sys.stdout)
		finally:
			f.close()

		return msg

