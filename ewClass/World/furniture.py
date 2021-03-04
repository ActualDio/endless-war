

import ewcfg

class EwFurniture:
	item_type = "furniture"

	# The proper name of the furniture item
	id_furniture = ""

	# The string name of the furniture item
	str_name = ""

	# The text displayed when you look at it
	str_desc = ""

	# How rare the item is, can be "Plebeian", "Patrician", or "Princeps"
	rarity = ""

	# Cost in SlimeCoin to buy this item. (slime now, but hopefully we make an exception for furniture)
	price = 0

	# Names of the vendors selling this item. (yo munchy/ben, i kind of want to add a furniture mart)
	vendors = []

	#Text when placing the item
	furniture_place_desc = ""

	#Text when the generic "look" is used
	furniture_look_desc = ""

	#How you received this item
	acquisition = ""

	#the set that the furniture belongs to
	furn_set = ""

	#furniture color
	hue = ""



	def __init__(
		self,
		id_furniture = "",
		str_name = "",
		str_desc = "",
		rarity = "",
		acquisition = "",
		price = 0,
		vendors = [],
		furniture_place_desc = "",
		furniture_look_desc = "",
		furn_set = "",
		hue="",
		num_keys = 0

	):
		self.item_type = ewcfg.it_furniture
		self.id_furniture = id_furniture
		self.str_name = str_name
		self.str_desc = str_desc
		self.rarity = rarity
		self.acquisition = acquisition
		self.price = price
		self.vendors = vendors
		self.furniture_place_desc = furniture_place_desc
		self.furniture_look_desc = furniture_look_desc
		self.furn_set = furn_set
		self.hue = hue
		self.num_keys = num_keys
