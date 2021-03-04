
from ewClass import EwBasic

class EwCharacter(EwBasic):
	""" Character class to manage general character methods and variables.\n
	Parameters:
		~~~~{inherited: EwBasic}~~~~\n
		'id_server': int -- ID for the last server used \n
		'name': string -- General name string \n

		~~~~{Unique}~~~~\n
		'char_type': string -- Character type, as in Enemy, Player, etc.\n
		'slime': int -- Amount of slime in the character\n
		'slimelevel': int -- Character's level, like in an rpg\n
		'poi': string -- Location the character is in\n
		'life_state': int -- How your character is doing in\n
		'attacktype': string -- Weapon class or type of this character\n
		'bleed_storage': int -- Blood storage for the "bleeding" mechanic\n
		'faction': string -- Character's faction affiliation\n
		'self_status': list -- Status that are applied to the character\n
    Methods:
		~~~~{inherited: EwBasic}~~~~\n
		'access_database' -- Access the database through a sequel query\n

		~~~~{Unique}~~~~\n
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
	self_status = [] 

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
