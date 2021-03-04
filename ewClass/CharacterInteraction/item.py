
import ewcfg
import ewutils

"""
	These are unassuming, tangible, multi-faceted, customizable items that you can actually interact with in-game.
"""
class EwGeneralItem:
	item_type = "item"
	id_item = " "
	alias = []
	context = ""
	str_name = ""
	str_desc = ""
	ingredients = ""
	acquisition = ""
	price = 0
	durability = 0
	vendors = []

	def __init__(
		self,
		id_item = " ",
		alias = [],
		context = "",
		str_name = "",
		str_desc = "",
		ingredients = "",
		acquisition = "",
		price = 0,
		durability = 0,
		vendors = [],
	):
		self.item_type = ewcfg.it_item
		self.id_item = id_item
		self.alias = alias
		self.context = context
		self.str_name = str_name
		self.str_desc = str_desc
		self.ingredients = ingredients
		self.acquisition = acquisition
		self.price = price
		self.durability = durability
		self.vendors = vendors


"""
	EwItem is the instance of an item (described by EwItemDef, linked by
	item_type) which is possessed by a player and stored in the database.
"""
class EwItem:
	id_item = -1
	id_server = -1
	id_owner = ""
	item_type = ""
	time_expir = -1

	stack_max = -1
	stack_size = 0
	soulbound = False

	template = "-2"

	item_props = None

	def __init__(
		self,
		id_item = None
	):
		if(id_item != None):
			self.id_item = id_item

			self.item_props = {}
			# the item props don't reset themselves automatically which is why the items_prop table had tons of extraneous rows (like food items having medal_names)
			#self.item_props.clear()

			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor()

				# Retrieve object
				cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {}, {} FROM items WHERE id_item = %s".format(
					ewcfg.col_id_server,
					ewcfg.col_id_user,
					ewcfg.col_item_type,
					ewcfg.col_time_expir,
					ewcfg.col_stack_max,
					ewcfg.col_stack_size,
					ewcfg.col_soulbound,
					ewcfg.col_template
				), (
					self.id_item,
				))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.id_server = result[0]
					self.id_owner = result[1]
					self.item_type = result[2]
					self.time_expir = result[3]
					self.stack_max = result[4]
					self.stack_size = result[5]
					self.soulbound = (result[6] != 0)
					self.template = result[7]

					# Retrieve additional properties
					cursor.execute("SELECT {}, {} FROM items_prop WHERE id_item = %s".format(
						ewcfg.col_name,
						ewcfg.col_value
					), (
						self.id_item,
					))

					for row in cursor:
						# this try catch is only necessary as long as extraneous props exist in the table
						try:
							self.item_props[row[0]] = row[1]
						except:
							ewutils.logMsg("extraneous item_prop row detected.")

				else:
					# Item not found.
					self.id_item = -1
			
				if self.template == "-2":
					self.persist()

			finally:
				# Clean up the database handles.
				cursor.close()
				ewutils.databaseClose(conn_info)

	""" Save item data object to the database. """
	def persist(self):
		
		if self.template == "-2":
			if self.item_type == ewcfg.it_item:
				self.template = self.item_props.get("id_item", "bad general item id")
			elif self.item_type == ewcfg.it_food:
				self.template = self.item_props.get("id_food", "bad food id")
			elif self.item_type == ewcfg.it_weapon:
				self.template = self.item_props.get("weapon_type", "bad weapon id")
			elif self.item_type == ewcfg.it_cosmetic:
				self.template = self.item_props.get("id_cosmetic", "bad cosmetic id")
			elif self.item_type == ewcfg.it_furniture:
				self.template = self.item_props.get("id_furniture", "bad furniture id")
			elif self.item_type == ewcfg.it_book:
				self.template = "player book"
			elif self.item_type == ewcfg.it_medal:
				self.template = "MEDAL ITEM????" #p sure these are fake news
			elif self.item_type == ewcfg.it_questitem:
				self.template = "QUEST ITEM????"

		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

			# Save the object.
			cursor.execute("REPLACE INTO items({}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
				ewcfg.col_id_item,
				ewcfg.col_id_server,
				ewcfg.col_id_user,
				ewcfg.col_item_type,
				ewcfg.col_time_expir,
				ewcfg.col_stack_max,
				ewcfg.col_stack_size,
				ewcfg.col_soulbound,
				ewcfg.col_template
			), (
				self.id_item,
				self.id_server,
				self.id_owner,
				self.item_type,
				self.time_expir if self.time_expir is not None else self.item_props['time_expir'] if 'time_expir' in self.item_props.keys() else 0,
				self.stack_max,
				self.stack_size,
				(1 if self.soulbound else 0),
				self.template
			))

			# Remove all existing property rows.
			cursor.execute("DELETE FROM items_prop WHERE {} = %s".format(
				ewcfg.col_id_item
			), (
				self.id_item,
			))

			# Write out all current property rows.
			for name in self.item_props:
				cursor.execute("INSERT INTO items_prop({}, {}, {}) VALUES(%s, %s, %s)".format(
					ewcfg.col_id_item,
					ewcfg.col_name,
					ewcfg.col_value
				), (
					self.id_item,
					name,
					self.item_props[name]
				))

			conn.commit()			
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)

"""
	EwItemDef is a class used to model base items. These are NOT the items
	owned by players, but rather the description of what those items are.
"""
class EwItemDef:
	# This is the unique reference name for this item.
	item_type = ""

	# If this is true, the item can not be traded or stolen.
	soulbound = False

	# If this value is positive, the item may actually be a pile of the same type of item, up to the specified size.
	stack_max = -1

	# If this value is greater than one, creating this item will actually give the user that many of them.
	stack_size = 1

	# Nice display name for this item.
	str_name = ""

	# The long description of this item's appearance.
	str_desc = ""

	# A map of default additional properties.
	item_props = None

	def __init__(
		self,
		item_type = "",
		str_name = "",
		str_desc = "",
		soulbound = False,
		stack_max = -1,
		stack_size = 1,
		item_props = None
	):
		self.item_type = item_type
		self.str_name = str_name
		self.str_desc = str_desc
		self.soulbound = soulbound
		self.stack_max = stack_max
		self.stack_size = stack_size
		self.item_props = item_props


class EwFish:
	# A unique name for the fish. This is used in the database and typed by users, so it should be one word, all lowercase letters.
	id_fish = ""

	# A list of alternative names.
	alias = []

	# Name of the fish.
	str_name = ""

	# Size of fish. Only assigned upon generation.
	size = ""

	# How rare a fish species is.
	rarity = ""

	# When it can be caught.
	catch_time = None

	# What weather the fish can be exclusively caught in.
	catch_weather = None

	# Description of the fish.
	str_desc = ""

	# What type of slime it exclusively resides in. None means both.
	slime = None

	# List of the vendors selling this item. (This will basically exclusively be none.)
	vendors = []

	def __init__(
			self,
			id_fish = "",
			str_name = "",
			size = "",
			rarity = "",
			catch_time = None,
			catch_weather = None,
			str_desc = "",
			slime = None,
			vendors = []
	):
		self.id_fish = id_fish
		self.str_name = str_name
		self.size = size
		self.rarity = rarity
		self.catch_time = catch_time
		self.catch_weather = catch_weather
		self.str_desc = str_desc
		self.slime = slime
		self.vendors = vendors


""" Food model object """
class EwFood:
	item_type = "food"

	# The main name of this food.
	id_food = ""

	# A list of alternative names.
	alias = []

	# Hunger reduced by eating this food.
	recover_hunger = 0

	# Cost in SlimeCoin to eat this food.
	price = 0

	# A nice string name describing this food.
	str_name = ""

	# Names of the vendors selling this food in the food court.
	vendors = []

	# Flavor text displayed when you eat this food.
	str_eat = ""

	# Alcoholic effect
	inebriation = 0

	# Flavor text displayed when you inspect this food.
	str_desc = ""

	# Expiration time (can be left blank for standard expiration time)
	time_expir = 0

	# The ingredients necessary to make this item via it's acquisition method
	ingredients = ""

	# The way that you can acquire this item. If blank, it's not relevant.
	acquisition = ""

	# Whether or not the item expires
	perishable = True

	#Timestamp when an item was fridged.

	time_fridged = 0

	def __init__(
		self,
		id_food = "",
		alias = [],
		recover_hunger = 0,
		price = 0,
		str_name = "",
		vendors = [],
		str_eat = "",
		inebriation = 0,
		str_desc = "",
		time_expir = 0,
		time_fridged =0,
		ingredients = "",
		acquisition = "",
		perishable = True
	):
		self.item_type = ewcfg.it_food

		self.id_food = id_food
		self.alias = alias
		self.recover_hunger = recover_hunger
		self.price = price
		self.str_name = str_name
		self.vendors = vendors
		self.str_eat = str_eat
		self.inebriation = inebriation
		self.str_desc = str_desc
		self.time_expir = time_expir if time_expir > 0 else ewcfg.std_food_expir
		self.time_fridged = time_fridged
		self.ingredients = ingredients
		self.acquisition = acquisition
		self.perishable = perishable


"""
	Cosmetic item model object
"""
class EwCosmeticItem:
	item_type = "cosmetic"

	# The proper name of the cosmetic item
	id_cosmetic = ""

	# The string name of the cosmetic item
	str_name = ""

	# The text displayed when you !inspect it
	str_desc = ""

	# The text displayed when you !adorn it
	str_onadorn = ""

	# The text displayed when you take it off
	str_unadorn = ""

	# The text displayed when it breaks! Oh no!
	str_onbreak = ""

	# How rare the item is, can be "Plebeian", "Patrician", or "Princeps"
	rarity = ""

	# The stats the item increases/decreases
	stats = {}

	# Some items have special abilities that act like less powerful Mutations
	ability = ""

	# While !adorn'd, this item takes damage-- If this reaches 0, it breaks
	durability = 0

	# How much space this item takes up on your person-- You can only wear so many items at a time, the amount is determined by your level
	size = 0

	# What fashion style the cosmetic belongs to: Goth, jock, prep, nerd
	style = ""

	# How fresh a cosmetic is, in other words how fleek, in other words how godDAMN it is, in other words how good it looks
	freshness = 0

	# The ingredients necessary to make this item via it's acquisition method
	ingredients = ""

	# Cost in SlimeCoin to buy this item.
	price = 0

	# Names of the vendors selling this item.
	vendors = []

	#Whether a cosmetic is a hat or not
	is_hat = False

	def __init__(
		self,
		id_cosmetic = "",
		str_name = "",
		str_desc = "",
		str_onadorn = "",
		str_unadorn = "",
		str_onbreak = "",
		rarity = "",
		stats = {},
		ability = "",
		durability = 0,
		size = 0,
		style = "",
		freshness = 0,
		ingredients = "",
		acquisition = "",
		price = 0,
		vendors = [],
		is_hat = False,

	):
		self.item_type = ewcfg.it_cosmetic

		self.id_cosmetic = id_cosmetic
		self.str_name = str_name
		self.str_desc = str_desc
		self.str_onadorn = str_onadorn
		self.str_unadorn = str_unadorn
		self.str_onbreak = str_onbreak
		self.rarity = rarity
		self.stats = stats
		self.ability = ability
		self.durability = durability
		self.size = size
		self.style = style
		self.freshness = freshness
		self.ingredients = ingredients
		self.acquisition = acquisition
		self.price = price
		self.vendors = vendors
		self.is_hat = is_hat

class EwBook:
	id_book = 0
	id_server = -1
	id_user = -1

	# The name of the book
	title = ""

	# The name of the author
	author = ""

	# If its been published or not
	book_state = 0

	# The in-game day it was published
	date_published = 0

	# Genre of zine (0-7)
	genre = -1

	# Length of the book after publishing
	length = 0

	# The total sales of the published book
	sales = 0

	# The average rating of the published book
	rating = 0

	# The number of people who have rated the book
	rates = 0

	# The number of pages in a book (between 5 and 20)
	pages = 10

	# The contents of the book
	book_pages = {}

	def __init__(
			self,
			id_book = None,
			member = None,
			book_state = None,
	):
		self.book_pages = {}

		query_suffix = ""
		if id_book is not None:
			self.id_book = id_book
			query_suffix = " id_book = {}".format(self.id_book)

		elif member is not None:
			self.id_server = member.guild.id
			self.id_user = member.id
			query_suffix = " id_server = {} AND id_user = {}".format(self.id_server, self.id_user)
			if book_state is not None:
				self.book_state = book_state
				query_suffix += " AND book_state = {}".format(self.book_state)

		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

			# Retrieve object
			cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} FROM books WHERE{}".format(
				ewcfg.col_id_book,
				ewcfg.col_id_user,
				ewcfg.col_id_server,
				ewcfg.col_title,
				ewcfg.col_author,
				ewcfg.col_book_state,
				ewcfg.col_date_published,
				ewcfg.col_genre,
				ewcfg.col_length,
				ewcfg.col_sales,
				ewcfg.col_rating,
				ewcfg.col_rates,
				ewcfg.col_pages,
				query_suffix,
			))
			result = cursor.fetchone();

			if result != None:
				# Record found: apply the data to this object.
				self.id_book = result[0]
				self.id_user = result[1]
				self.id_server = result[2]
				self.title = result[3]
				self.author = result[4]
				self.book_state = result[5]
				self.date_published = result[6]
				self.genre = result[7]
				self.length = result[8]
				self.sales = result[9]
				self.rating = result[10]
				self.rates = result[11]
				self.pages = result[12]

				# Retrieve additional properties
				cursor.execute("SELECT {}, {} FROM book_pages WHERE id_book = %s".format(
					ewcfg.col_page,
					ewcfg.col_contents
				), (
					self.id_book,
				))

				for row in cursor:
					# this try catch is only necessary as long as extraneous props exist in the table
					try:
						self.book_pages[row[0]] = row[1]
					except:
						ewutils.logMsg("extraneous book_pages row detected.")

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
			cursor.execute(
				"REPLACE INTO books({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
					ewcfg.col_id_book,
					ewcfg.col_id_server,
					ewcfg.col_id_user,
					ewcfg.col_title,
					ewcfg.col_author,
					ewcfg.col_book_state,
					ewcfg.col_date_published,
					ewcfg.col_genre,
					ewcfg.col_length,
					ewcfg.col_sales,
					ewcfg.col_rating,
					ewcfg.col_rates,
					ewcfg.col_pages,
				), (
					self.id_book,
					self.id_server,
					self.id_user,
					self.title,
					self.author,
					self.book_state,
					self.date_published,
					self.genre,
					self.length,
					self.sales,
					self.rating,
					self.rates,
					self.pages,
				))

			# Remove all existing property rows.
			cursor.execute("DELETE FROM book_pages WHERE {} = %s".format(
				ewcfg.col_id_book
			), (
				self.id_book,
			))

			# Write out all current property rows.
			for name in self.book_pages:
				cursor.execute("INSERT INTO book_pages({}, {}, {}) VALUES(%s, %s, %s)".format(
					ewcfg.col_id_book,
					ewcfg.col_page,
					ewcfg.col_contents
				), (
					self.id_book,
					name,
					self.book_pages[name]
				))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)

# The purpose of this is to make finding the average rating easier and to measure sales based on the amount of different people that buy them.

class EwBookSale:
	id_book = 0
	id_user = -1
	id_server = -1

	# If a user bought the book. 0 is not bought.
	bought = 0

	# A user's rating of a book. 0 is unrated.
	rating = 0

	def __init__(
			self,
			id_book = None,
			member = None,
	):
		self.id_book = id_book
		self.id_user = member.id
		self.id_server = member.guild.id

		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

			# Retrieve object
			cursor.execute("SELECT {}, {} FROM book_sales WHERE {} = %s AND {} = %s AND {} = %s".format(
				ewcfg.col_bought,
				ewcfg.col_rating,
				ewcfg.col_id_book,
				ewcfg.col_id_user,
				ewcfg.col_id_server,
			), (
				self.id_book,
				self.id_user,
				self.id_server,
			))
			result = cursor.fetchone();

			if result != None:
				# Record found: apply the data to this object.
				self.bought = result[0]
				self.rating = result[1]

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
			cursor.execute(
				"REPLACE INTO book_sales({}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s)".format(
					ewcfg.col_id_book,
					ewcfg.col_id_server,
					ewcfg.col_id_user,
					ewcfg.col_bought,
					ewcfg.col_rating,
				), (
					self.id_book,
					self.id_server,
					self.id_user,
					self.bought,
					self.rating,
				))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)

"""
	Prank items for Swilldermuk
"""
class EwPrankItem:
	item_type = "item"
	id_item = " "
	
	
	alias = []
	
	context = "prankitem"
	str_name = ""
	str_desc = ""
	
	prank_type = "" # Type of prank item. Can be an instant use, trap, or response item
	prank_desc = "" # A line of text that appears when the prank item gets used
	rarity = "" # Rarity of prank item. Used in determining how often it should spawn
	gambit = 0 # Gambit multiplier
	response_command = "" # All response items need a different command to break out of them
	response_desc_1 = "" # Response items contain additonal text which is indicative of how far the prank has progressed.
	response_desc_2 = ""
	response_desc_3 = ""
	response_desc_4 = ""
	trap_chance = 0 # All trap items only have a certain chance to activate
	trap_stored_credence = 0 # Trap items store half your current credence up front for later
	trap_user_id = "" # Trap items store your user id when you lay them down for later
	side_effect = "" # Some prank items have side-effects. Example: The 'bungis beam' will change a player's name to '[player name] (Bungis)'
	
	ingredients = ""
	acquisition = ""
	vendors = []

	def __init__(
		self,
		id_item=" ",
		alias = [],
		str_name = "",
		str_desc = "",
		prank_type = "",
		prank_desc = "",
		rarity = "",
		gambit = 0,
		response_command = "",
		response_desc_1 = "",
		response_desc_2 = "",
		response_desc_3 = "",
		response_desc_4 = "",
		trap_chance = 0,
		trap_stored_credence = 0,
		trap_user_id = "",
		side_effect = "",
		ingredients = "",
		acquisition = "",
		vendors = [],
	):
		self.item_type = "item"
		self.id_item = id_item
		self.alias = alias
		self.context = "prankitem"
		self.str_name = str_name
		self.str_desc = str_desc
		self.prank_type = prank_type
		self.prank_desc = prank_desc
		self.rarity = rarity
		self.gambit = gambit
		self.response_command = response_command
		self.response_desc_1 = response_desc_1
		self.response_desc_2 = response_desc_2
		self.response_desc_3 = response_desc_3
		self.response_desc_4 = response_desc_4
		self.trap_chance = trap_chance
		self.trap_stored_credence = trap_stored_credence
		self.trap_user_id = trap_user_id
		self.side_effect = side_effect
		self.ingredients = ingredients
		self.acquisition = acquisition
		self.vendors = vendors

class PrankIndex:
	id_server = -1
	id_user_pranker = -1
	id_user_pranked = -1
	prank_count = 0 # How many times has user 1 (pranker) pranked user 2 (pranked)?
	
	def __init__(
		self,
		id_server = -1,
		id_user_pranker = -1,
		id_user_pranked = -1,
		prank_count = 0,
	):
		self.id_server = id_server
		self.id_user_pranker = id_user_pranker
		self.id_user_pranked = id_user_pranked
		self.prank_count = prank_count

		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

			# Retrieve object
			cursor.execute("SELECT {count} FROM swilldermuk_prank_index WHERE {id_user_pranker} = %s AND {id_user_pranked} = %s AND {id_server} = %s".format(
				count=ewcfg.col_prank_count,
				id_user_pranker=ewcfg.col_id_user_pranker,
				id_user_pranked=ewcfg.col_id_user_pranked,
				id_server=ewcfg.col_id_server,
			), (
				self.id_user_pranker,
				self.id_user_pranked,
				self.id_server,
			))
			result = cursor.fetchone();

			if result != None:
				# Record found: apply the data to this object.
				self.prank_count = result[0]

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
			cursor.execute(
				"REPLACE INTO swilldermuk_prank_index({}, {}, {}, {}) VALUES(%s, %s, %s, %s)".format(
					ewcfg.col_id_server,
					ewcfg.col_id_user_pranker,
					ewcfg.col_id_user_pranked,
					ewcfg.col_prank_count,
				), (
					self.id_server,
					self.id_user_pranker,
					self.id_user_pranked,
					self.prank_count,
				))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)

"""
	Slimeoid Food Items
"""
class EwSlimeoidFood:
	item_type = "item"
	id_item = " "
	alias = []
	context = "slimeoidfood"
	str_name = ""
	str_desc = ""
	ingredients = ""
	acquisition = ""
	price = 0
	vendors = []

	increase = ""
	decrease = ""

	def __init__(
		self,
		id_item = " ",
		alias = [],
		str_name = "",
		str_desc = "",
		ingredients = "",
		acquisition = "",
		price = 0,
		vendors = [],
		increase = "",
		decrease = "",
	):
		self.item_type = ewcfg.it_item
		self.id_item = id_item
		self.alias = alias
		self.context = ewcfg.context_slimeoidfood
		self.str_name = str_name
		self.str_desc = str_desc
		self.ingredients = ingredients
		self.acquisition = acquisition
		self.price = price
		self.vendors = vendors
		self.increase = increase
		self.decrease = decrease

"""
	Smelting Recipe Model Object
"""
class EwSmeltingRecipe:
	# The proper name of the recipe.
	id_recipe = ""

	# The string name of the recipe.
	str_name = ""

	# A list of alternative names.
	alias = []

	# The ingredients for the recipe, by str_name of the object.
	ingredients = []

	# The product(s) created by the recipe, A tuple of the item type (it_food, it_cosmetic, etc) and item_props.
	products = []

	def __init__(
		self,
		id_recipe="",
		str_name="",
		alias = [],
		ingredients = [],
		products = [],
	):
		self.id_recipe = id_recipe
		self.str_name = str_name
		self.alias = alias
		self.ingredients = ingredients
		self.products = products
