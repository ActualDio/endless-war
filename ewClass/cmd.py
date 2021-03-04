

""" class to send general data about an interaction to a command """
class EwCmd:
	cmd = ""
	tokens = []
	tokens_count = 0
	message = None
	client = None
	mentions = []
	mentions_count = 0
	guild = None

	#EwId system
	client_id = None
	author_id = None
	mention_ids = []


	def __init__(
		self,
		tokens = [],
		message = None,
		client = None,
		mentions = [],
		guild = None,
		admin = False,
	):
		self.tokens = tokens
		self.message = message
		self.client = client
		self.guild = guild

		if len(tokens) >= 1:
			self.tokens_count = len(tokens)
			self.cmd = tokens[0]

		#Endless War's EwId
		self.client_id = EwId(client.user.id, self.guild.id, client.user.name, admin = admin) 
		#Author's EwId
		self.author_id = EwId(message.author.id, self.guild.id, message.author.name, admin = admin) 
		#List of mentions' EwIds
		self.mention_ids = []
		for user in mentions:
			self.mention_ids.append(EwId(user.id, self.guild.id, user.name, user.guild_permissions.administrator))
			# print(EwId(user.id, user.guild.id, user.name, user.guild_permissions.administrator))

		# remove mentions to us for commands that dont yet handle Endless War mentions with EwIds
		self.mentions = list(filter(lambda user : user.id != client.user.id, mentions))
		self.mentions_count = len(self.mentions)
