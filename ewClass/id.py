
""" wrapper for discord members """
from ewClass.game_element import EwBasic


class EwId(EwBasic):
	user = -1
	guild = -1
	name = ""
	admin = False

	def __init__(self, user, guild, name, admin):
		self.user = user
		self.guild = guild
		self.name = name
		self.admin = admin

	def __repr__(self): #print() support
		return "<EwId - {}>".format(self.name)