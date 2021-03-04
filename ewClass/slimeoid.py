
import random

import ewcfg
import ewutils
from ewClass import EwMarket
from ewClass import EwDiscordUser
from ewClass import EwPlayer

active_slimeoidbattles = {}

""" Slimeoid data model for database persistence """
class EwSlimeoid:
	id_slimeoid = 0
	id_user = ""
	id_server = -1

	life_state = 0
	body = ""
	head = ""
	legs = ""
	armor = ""
	weapon = ""
	special = ""
	ai = ""
	sltype = "Lab"
	name = ""
	atk = 0
	defense = 0
	intel = 0
	level = 0
	time_defeated = 0
	clout = 0
	hue = ""
	coating = ""
	poi = ""

	#slimeoid = EwSlimeoid(member = cmd.message.author, )
	#slimeoid = EwSlimeoid(id_slimeoid = 12)

	""" Load the slimeoid data for this user from the database. """
	def __init__(self, member = None, id_slimeoid = None, life_state = None, id_user = None, id_server = None, sltype = "Lab", slimeoid_name = None):
		query_suffix = ""
		user_data = None
		if member != None:
			id_user = str(member.id)
			id_server = member.guild.id
		elif id_user != None:
			id_user = str(id_user)

		#	user_data = EwPlayer(member = member)

		#if user_data != None:
		#	if user_data.active_slimeoid > -1:
		#		id_slimeoid = user_data.active_slimeoid

		if id_slimeoid != None:
			query_suffix = " WHERE id_slimeoid = '{}'".format(id_slimeoid)
		else:

			if id_user != None and id_server != None:
				query_suffix = " WHERE id_user = '{}' AND id_server = '{}'".format(id_user, id_server)
				if life_state != None:
					query_suffix += " AND life_state = '{}'".format(life_state)
				if sltype != None:
					query_suffix += " AND type = '{}'".format(sltype)
				if slimeoid_name != None:
					query_suffix += " AND name = '{}'".format(slimeoid_name)


		if query_suffix != "":
			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor();

				# Retrieve object
				cursor.execute("SELECT {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} FROM slimeoids{}".format(
					ewcfg.col_id_slimeoid,
					ewcfg.col_id_user,
					ewcfg.col_id_server,
					ewcfg.col_life_state,
					ewcfg.col_body,
					ewcfg.col_head,
					ewcfg.col_legs,
					ewcfg.col_armor,
					ewcfg.col_weapon,
					ewcfg.col_special,
					ewcfg.col_ai,
					ewcfg.col_type,
					ewcfg.col_name,
					ewcfg.col_atk,
					ewcfg.col_defense,
					ewcfg.col_intel,
					ewcfg.col_level,
					ewcfg.col_time_defeated,
					ewcfg.col_clout,
					ewcfg.col_hue,
					ewcfg.col_coating,
					ewcfg.col_poi,
					query_suffix
				))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.id_slimeoid = result[0]
					self.id_user = result[1]
					self.id_server = result[2]
					self.life_state = result[3]
					self.body = result[4]
					self.head = result[5]
					self.legs = result[6]
					self.armor = result[7]
					self.weapon = result[8]
					self.special = result[9]
					self.ai= result[10]
					self.sltype = result[11]
					self.name = result[12]
					self.atk = result[13]
					self.defense = result[14]
					self.intel = result[15]
					self.level = result[16]
					self.time_defeated = result[17]
					self.clout = result[18]
					self.hue = result[19]
					self.coating = result[20]
					self.poi = result[21]

			finally:
				# Clean up the database handles.
				cursor.close()
				ewutils.databaseClose(conn_info)


	""" Save slimeoid data object to the database. """
	def persist(self):
		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			# Save the object.
			cursor.execute("REPLACE INTO slimeoids({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
				ewcfg.col_id_slimeoid,
				ewcfg.col_id_user,
				ewcfg.col_id_server,
				ewcfg.col_life_state,
				ewcfg.col_body,
				ewcfg.col_head,
				ewcfg.col_legs,
				ewcfg.col_armor,
				ewcfg.col_weapon,
				ewcfg.col_special,
				ewcfg.col_ai,
				ewcfg.col_type,
				ewcfg.col_name,
				ewcfg.col_atk,
				ewcfg.col_defense,
				ewcfg.col_intel,
				ewcfg.col_level,
				ewcfg.col_time_defeated,
				ewcfg.col_clout,
				ewcfg.col_hue,
				ewcfg.col_coating,
				ewcfg.col_poi
			), (
				self.id_slimeoid,
				self.id_user,
				self.id_server,
				self.life_state,
				self.body,
				self.head,
				self.legs,
				self.armor,
				self.weapon,
				self.special,
				self.ai,
				self.sltype,
				self.name,
				self.atk,
				self.defense,
				self.intel,
				self.level,
				self.time_defeated,
				self.clout,
				self.hue,
				self.coating,
				self.poi
			))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)

	def die(self):
		self.life_state = ewcfg.slimeoid_state_dead
		self.id_user = ""


	def delete(self):
		ewutils.execute_sql_query("DELETE FROM slimeoids WHERE {id_slimeoid} = %s".format(
			id_slimeoid = ewcfg.col_id_slimeoid
		),(
			self.id_slimeoid,
		))
	
	def haunt(self):
		resp_cont = ewutils.EwResponse(id_server = self.id_server)
		if (self.sltype != ewcfg.sltype_nega) or active_slimeoidbattles.get(self.id_slimeoid):
			return resp_cont
		market_data = EwMarket(id_server = self.id_server)
		ch_name = ewcfg.id_to_poi.get(self.poi).channel

		data = ewutils.execute_sql_query("SELECT {id_user} FROM users WHERE {poi} = %s AND {id_server} = %s".format(
			id_user = ewcfg.col_id_user,
			poi = ewcfg.col_poi,
			id_server = ewcfg.col_id_server
		),(
			self.poi,
			self.id_server
		))

		for row in data:
			haunted_data = EwPlayer(id_user = row[0], id_server = self.id_server)
			haunted_player = EwDiscordUser(id_user = row[0])

			if haunted_data.life_state in [ewcfg.life_state_juvenile, ewcfg.life_state_enlisted]:
				haunted_slimes = 2 * int(haunted_data.slime / ewcfg.slimes_hauntratio)

				haunt_cap = 10 ** (self.level-1)
				haunted_slimes = min(haunt_cap, haunted_slimes) # cap on for how much you can haunt

				haunted_data.change_slime(n = -haunted_slimes, source = ewcfg.source_haunted)
				market_data.negaslime -= haunted_slimes

				# Persist changes to the database.
				haunted_data.persist()
		response = "{} lets out a blood curdling screech. Everyone in the district loses slime.".format(self.name)
		resp_cont.add_channel_response(ch_name, response)
		market_data.persist()

		return resp_cont

	def move(self):
		resp_cont = ewutils.EwResponse(id_server = self.id_server)
		if active_slimeoidbattles.get(self.id_slimeoid):
			return resp_cont
		try:
			destinations = ewcfg.poi_neighbors.get(self.poi).intersection(set(ewcfg.capturable_districts))
			if len(destinations) > 0:
				self.poi = random.choice(list(destinations))
				poi_def = ewcfg.id_to_poi.get(self.poi)
				ch_name = poi_def.channel
		
				response = "The air grows colder and color seems to drain from the streets and buildings around you. {} has arrived.".format(self.name)
				resp_cont.add_channel_response(ch_name, response)
				response = "There are reports of a sinister presence in {}.".format(poi_def.str_name)
				resp_cont.add_channel_response(ewcfg.channel_rowdyroughhouse, response)
				resp_cont.add_channel_response(ewcfg.channel_copkilltown, response)
		finally:
			return resp_cont

	def eat(self, food_item):
		if food_item.item_props.get('context') != ewcfg.context_slimeoidfood:
			return False
		
		if food_item.item_props.get('decrease') == ewcfg.slimeoid_stat_moxie:
			if self.atk < 1:
				return False
			
			self.atk -= 1
		elif food_item.item_props.get('decrease') == ewcfg.slimeoid_stat_grit:
			if self.defense < 1:
				return False
			
			self.defense -= 1
		elif food_item.item_props.get('decrease') == ewcfg.slimeoid_stat_chutzpah:
			if self.intel < 1:
				return False
			
			self.intel -= 1
		if food_item.item_props.get('increase') == ewcfg.slimeoid_stat_moxie:
			self.atk += 1
		elif food_item.item_props.get('increase') == ewcfg.slimeoid_stat_grit:
			self.defense += 1
		elif food_item.item_props.get('increase') == ewcfg.slimeoid_stat_chutzpah:
			self.intel += 1

		return True

""" slimeoid model object """
class EwBody:
	id_body = ""
	alias = []
	str_create = ""
	str_body = ""
	def __init__(
		self,
		id_body = "",
		alias = [],
		str_create = "",
		str_body = "",
		str_observe = ""
	):
		self.id_body = id_body
		self.alias = alias
		self.str_create = str_create
		self.str_body = str_body
		self.str_observe = str_observe

class EwHead:
	id_head = ""
	alias = []
	str_create = ""
	str_head = ""
	def __init__(
		self,
		id_head = "",
		alias = [],
		str_create = "",
		str_head = "",
		str_feed = "",
		str_fetch = ""
	):
		self.id_head = id_head
		self.alias = alias
		self.str_create = str_create
		self.str_head = str_head
		self.str_feed = str_feed
		self.str_fetch = str_fetch
	
class EwMobility:
	id_mobility = ""
	alias = []
	str_advance = ""
	str_retreat = ""
	str_create = ""
	str_mobility = ""
	def __init__(
		self,
		id_mobility = "",
		alias = [],
		str_advance = "",
		str_advance_weak = "",
		str_retreat = "",
		str_retreat_weak = "",
		str_create = "",
		str_mobility = "",
		str_defeat = "",
		str_walk = ""
	):
		self.id_mobility = id_mobility
		self.alias = alias
		self.str_advance = str_advance
		self.str_advance_weak = str_advance_weak
		self.str_retreat = str_retreat
		self.str_retreat_weak = str_retreat_weak
		self.str_create = str_create
		self.str_mobility = str_mobility
		self.str_defeat = str_defeat
		self.str_walk = str_walk

class EwOffense:
	id_offense = ""
	alias = []
	str_attack = ""
	str_create = ""
	str_offense = ""
	def __init__(
		self,
		id_offense = "",
		alias = [],
		str_attack = "",
		str_attack_weak = "",
		str_attack_coup = "",
		str_create = "",
		str_offense = "",
		str_observe = ""
	):
		self.id_offense = id_offense
		self.alias = alias
		self.str_attack = str_attack
		self.str_attack_weak = str_attack_weak
		self.str_attack_coup = str_attack_coup
		self.str_create = str_create
		self.str_offense = str_offense
		self.str_observe = str_observe

class EwDefense:
	id_defense = ""
	alias = []
	str_create = ""
	str_defense = ""
	id_resistance = ""
	id_weakness = ""
	str_resistance = ""
	str_weakness = ""
	str_abuse = ""
	def __init__(
		self,
		id_defense = "",
		alias = [],
		str_create = "",
		str_defense = "",
		str_armor = "",
		str_pet = "",
		id_resistance = "",
		id_weakness = "",
		str_resistance = "",
		str_weakness = "",
		str_abuse = "",
	):
		self.id_defense = id_defense
		self.alias = alias
		self.str_create = str_create
		self.str_defense = str_defense
		self.str_armor = str_armor
		self.str_pet = str_pet
		self.id_resistance = id_resistance
		self.id_weakness = id_weakness
		self.str_resistance = str_resistance
		self.str_weakness = str_weakness
		self.str_abuse = str_abuse

	def get_resistance(self, offense = None):
		if offense is None:
			return ""

		if offense.id_offense == self.id_resistance:
			return self.str_resistance

		else:
			return ""

	def get_weakness(self, special = None):
		if special is None:
			return ""

		if special.id_special == self.id_weakness:
			return self.str_weakness

		else:
			return ""

class EwSpecial:
	id_special = ""
	alias = []
	str_special_attack = ""
	str_create = ""
	str_special = ""
	def __init__(
		self,
		id_special = "",
		alias = [],
		str_special_attack = "",
		str_special_attack_weak = "",
		str_special_attack_coup = "",
		str_create = "",
		str_special = "",
		str_observe = ""
	):
		self.id_special = id_special
		self.alias = alias
		self.str_special_attack = str_special_attack
		self.str_special_attack_weak = str_special_attack_weak
		self.str_special_attack_coup = str_special_attack_coup
		self.str_create = str_create
		self.str_special = str_special
		self.str_observe = str_observe

class EwBrain:
	id_brain = ""
	alias = []
	str_create = ""
	str_brain = ""
	def __init__(
		self,
		id_brain = "",
		alias = [],
		str_create = "",
		str_brain = "",
		str_dissolve = "",
		str_spawn = "",
		str_revive = "",
		str_death = "",
		str_victory = "",
		str_battlecry = "",
		str_battlecry_weak = "",
		str_movecry = "",
		str_movecry_weak = "",
		str_kill = "",
		str_walk = "",
		str_pet = "",
		str_observe = "",
		str_feed = "",
		get_strat = None,
		str_abuse = "",
	):
		self.id_brain = id_brain
		self.alias = alias
		self.str_create = str_create
		self.str_brain = str_brain
		self.str_dissolve = str_dissolve
		self.str_spawn = str_spawn
		self.str_revive = str_revive
		self.str_death = str_death
		self.str_victory = str_victory
		self.str_battlecry = str_battlecry
		self.str_battlecry_weak = str_battlecry_weak
		self.str_movecry = str_movecry
		self.str_movecry_weak = str_movecry_weak
		self.str_kill = str_kill
		self.str_pet = str_pet
		self.str_walk = str_walk
		self.str_observe = str_observe
		self.str_feed = str_feed
		self.get_strat = get_strat
		self.str_abuse = str_abuse

# manages a slimeoid's combat stats during a slimeoid battle
class EwSlimeoidCombatData:

	# slimeoid name
	name = ""

	# slimeoid weapon object
	weapon = None

	# slimeoid armor object
	armor = None

	# slimeoid special attack object
	special = None

	# slimeoid legs object
	legs = None

	# slimeoid brain object
	brain = None

	# slimeoid hue object
	hue = None
	
	# slimeoid coating object
	coating = None

	# slimeoid physical attack stat
	moxie = 0

	# slimeoid physical defense stat
	grit = 0

	# slimeoid special attack stat
	chutzpah = 0
	
	# slimeoid maximum hp
	hpmax = 0

	# slimeoid current hp
	hp = 0

	# slimeoid maximum sap
	sapmax = 0

	# slimeoid current sap
	sap = 0

	# slimeoid current hardened sap
	hardened_sap = 0

	# slimeoid shock (reduces effective sap)
	shock = 0

	# slimeoid database object (EwSlimeoid)
	slimeoid = None

	# slimeoid owner database object (EwDiscordUser)
	owner = None

	# slimeoid armor weakness string
	resistance = ""

	# slimeoid armor resistance string
	weakness = ""
	
	# slimeoid hue physical resistance string
	analogous = ""
	
	# slimeoid hue physical weakness string
	splitcomplementary_physical = ""

	# slimeoid hue special weakness string
	splitcomplementary_special = ""

	def __init__(self,
		name = "",
		weapon = None,
		armor = None,
		special = None,
		legs = None,
		brain = None,
		hue = None,
		coating = None,
		moxie = 0,
		grit = 0,
		chutzpah = 0,
		hpmax = 0,
		hp = 0,
		sapmax = 0,
		sap = 0,
		slimeoid = None,
		owner = None
	):
		self.name = name
		self.weapon = weapon
		self.armor = armor
		self.special = special
		self.legs = legs
		self.brain = brain
		self.hue = hue
		self.coating = coating
		self.moxie = moxie
		self.grit = grit
		self.chutzpah = chutzpah
		self.hpmax = hpmax
		self.hp = hp
		self.sapmax = sapmax
		self.sap = sap
		self.hardened_sap = 0
		self.shock = 0
		self.slimeoid = slimeoid
		self.owner = owner
	
	# initializes the physical resistance and special weakness strings and applies corresponding stat changes
	def apply_weapon_matchup(self, enemy_combat_data = None):
		challengee_slimeoid = self.slimeoid
		challenger_slimeoid = enemy_combat_data.slimeoid

		resistance = self.armor.get_resistance(enemy_combat_data.weapon)
		weakness = self.armor.get_weakness(enemy_combat_data.special)

		if len(resistance) > 0:
			enemy_combat_data.moxie -= 2
			enemy_combat_data.moxie = max(1, enemy_combat_data.moxie)

		if len(weakness) > 0:
			enemy_combat_data.chutzpah += 2

		self.resistance = resistance.format(self.name)
		self.weakness = weakness.format(self.name)

	# initializes the hue resistance and weakness strings and applies corresponding stat changes
	def apply_hue_matchup(self, enemy_combat_data = None):
		color_matchup = ewcfg.hue_neutral
		# get color matchups
		if self.hue is not None:
			color_matchup = self.hue.effectiveness.get(enemy_combat_data.slimeoid.hue)

		if color_matchup is None:
			color_matchup = ewcfg.hue_neutral

		if color_matchup < 0:
			enemy_combat_data.grit += 2
			enemy_combat_data.analogous = "It's not very effective against {}...".format(enemy_combat_data.name)
			
		elif color_matchup > 0:
			if color_matchup == ewcfg.hue_atk_complementary:
				self.moxie += 2
				enemy_combat_data.splitcomplementary_physical = "It's Super Effective against {}!".format(enemy_combat_data.name)
			elif color_matchup == ewcfg.hue_special_complementary:
				self.chutzpah += 2
				enemy_combat_data.splitcomplementary_special = "It's Super Effective against {}!".format(enemy_combat_data.name)
			elif color_matchup == ewcfg.hue_full_complementary:
				self.moxie += 2
				self.chutzpah += 2
				enemy_combat_data.splitcomplementary_physical = "It's Super Effective against {}!".format(enemy_combat_data.name)
				enemy_combat_data.splitcomplementary_special = "It's Super Effective against {}!".format(enemy_combat_data.name)
			
		# print(self.coating)
		if self.coating == ewcfg.hue_id_copper:
			self.moxie += 2
		elif self.coating == ewcfg.hue_id_chrome:
			self.grit += 2
		elif self.coating == ewcfg.hue_id_gold:
			self.chutzpah += 2

	# roll the dice on whether an action succeeds and by how many degrees of success
	def attempt_action(self, strat, sap_spend, in_range):
		# reduce sap available by shock
		self.sap -= self.shock
		self.sap = max(0, self.sap)
		self.shock = 0
		sap_spend = min(sap_spend, self.sap)
		
		# obtain target number based on the type of action attempted
		target_number = 0
		if strat == ewcfg.slimeoid_strat_attack:
			if in_range:
				target_number = self.moxie
			else:
				target_number = self.chutzpah

		elif strat == ewcfg.slimeoid_strat_evade:
			target_number = 6
		elif strat == ewcfg.slimeoid_strat_block:
			target_number = self.grit

		dos = 0
		dice = []
		# roll the dice
		for i in range(sap_spend):
			die_roll = random.randrange(10)
			dice.append(die_roll)
			# a result lower than the target number confers a degree of success. a result of 0 always succeeds and a result of 9 always fails.
			if (die_roll < target_number and die_roll != 9) or die_roll == 0:
				dos += 1

		#ewutils.logMsg("Rolling {} check with {} sap, target number {}: {}, {} successes".format(strat, sap_spend, target_number, dice, dos))
		# spend sap
		self.sap -= sap_spend

		# return degrees of success
		return dos

	# obtain response for attack
	def execute_attack(self, enemy_combat_data, damage, in_range):
		hp = enemy_combat_data.hp
		hp -= damage

		thrownobject = random.choice(ewcfg.thrownobjects_list)

		response = "**"
		if in_range:
			if hp <= 0:
				response += self.weapon.str_attack_coup.format(
					active=self.name,
					inactive=enemy_combat_data.name,
				)
			elif (self.hpmax/self.hp) > 3:
				response += self.weapon.str_attack_weak.format(
					active=self.name,
					inactive=enemy_combat_data.name,
				)
			else:
				response += self.weapon.str_attack.format(
					active=self.name,
					inactive=enemy_combat_data.name,
				)
		else:
			if hp <= 0:
				response += self.special.str_special_attack_coup.format(
					active=self.name,
					inactive=enemy_combat_data.name,
					object=thrownobject
				)
			elif (self.hpmax/self.hp) > 3:
				response += self.special.str_special_attack_weak.format(
					active=self.name,
					inactive=enemy_combat_data.name,
					object=thrownobject
				)
			else:
				response += self.special.str_special_attack.format(
					active=self.name,
					inactive=enemy_combat_data.name,
					object=thrownobject
				)
		response += "**"
		response += " :boom:"

		return response

	# apply damage and obtain response
	def take_damage(self, enemy_combat_data, damage, active_dos, in_range):
		
		# apply damage
		self.hp -= damage
		hp = self.hp

		# crush sap on physical attacks only
		sap_crush = 0
		if in_range:
			sap_crush = min(self.hardened_sap, active_dos)
			self.hardened_sap -= sap_crush

		# store shock taken for next turn
		self.shock += 2 * active_dos

		# get proper response
		response = ""
		if self.hp > 0:
			if in_range:
				if self.resistance != "":
					response = self.resistance

				if self.analogous != "":
					response += " {}".format(self.analogous)

				if self.splitcomplementary_physical != "":
					response += " {}".format(self.splitcomplementary_physical)

			else:
				if self.weakness != "":
					response = self.weakness

				if self.splitcomplementary_special != "":
					response += " {}".format(self.splitcomplementary_special)


			if hp/damage > 10:
				response += " {} barely notices the damage.".format(self.name)
			elif hp/damage > 6:
				response += " {} is hurt, but shrugs it off.".format(self.name)
			elif hp/damage > 4:
				response += " {} felt that one!".format(self.name)
			elif hp/damage >= 3:
				response += " {} really felt that one!".format(self.name)
			elif hp/damage < 3:
				response += " {} reels from the force of the attack!!".format(self.name)

			if sap_crush > 0:
				response += " (-{} hardened sap)".format(sap_crush)


		return response

	# obtain movement response
	def change_distance(self, enemy_combat_data, in_range):
		response = ""
		if in_range:
			if (self.hpmax/self.hp) > 3:
				response = self.legs.str_retreat_weak.format(
					active=self.name,
					inactive=enemy_combat_data.name,
				)
			else:
				response = self.legs.str_retreat.format(
					active=self.name,
					inactive=enemy_combat_data.name,
				)
		else:
			if (self.hpmax/self.hp) > 3:
				response = self.legs.str_advance_weak.format(
					active=self.name,
					inactive=enemy_combat_data.name,
				)
			else:
				response = self.legs.str_advance.format(
					active=self.name,
					inactive=enemy_combat_data.name,
				)
		return response

	# harden sap and obtain response
	def harden_sap(self, dos):
		response = ""
		
		sap_hardened = min(dos, self.grit - self.hardened_sap)
		self.hardened_sap += sap_hardened

		if sap_hardened <= 0:
			response = "{} fails to harden any sap!".format(self.name)
		else:
			response = "{} hardens {} sap!".format(self.name, sap_hardened)

		return response

class EwHue:
	id_hue = ""
	alias = []
	str_saturate = ""
	str_name= ""
	str_desc = ""
	effectiveness = {}
	palette = []
	is_neutral = False
	def __init__(
		self,
		id_hue = "",
		alias = [],
		str_saturate = "",
		str_name= "",
		str_desc = "",
		effectiveness = {},
		palette = [],
		is_neutral = False
	):
		self.id_hue = id_hue
		self.alias = alias
		self.str_saturate = str_saturate
		self.str_name= str_name
		self.str_desc = str_desc
		self.effectiveness = effectiveness
		self.style_palette = palette
		self.is_neutral = is_neutral
