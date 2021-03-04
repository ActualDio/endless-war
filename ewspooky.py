from ewdistrict import EwDistrict

"""
	Commands and utilities related to dead players.
"""
import time
import random
import re
import asyncio

import ewcmd
import ewcfg
import ewutils
import ewmap
import ewrolemgr
import ewslimeoid
import ewitem
import ewquadrants
import ewstats
from ew import EwPlayer
from ewmarket import EwMarket
from ewslimeoid import EwSlimeoid

""" revive yourself from the dead. """
async def revive(cmd):
	time_now = int(time.time())
	response = ""

	if cmd.message.channel.name != ewcfg.channel_endlesswar and cmd.message.channel.name != ewcfg.channel_sewers:
		response = "Come to me. I hunger. #{}.".format(ewcfg.channel_sewers)
	else:
		player_data = EwPlayer(member = cmd.message.author)

		#time_until_revive = (player_data.time_lastdeath + 600) - time_now
		time_until_revive = (player_data.time_lastdeath + player_data.degradation) - time_now
		
		if time_until_revive > 0:
			response = "ENDLESS WAR is not ready to {} you yet ({}s).".format(cmd.tokens[0], time_until_revive)
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		slimeoid = EwSlimeoid(member = cmd.message.author)

		if player_data.life_state == ewcfg.life_state_corpse:
			market_data = EwMarket(id_server = cmd.guild.id)

			# Endless War collects his fee.
			#fee = (player_data.slimecoin / 10)
			#player_data.change_slimecoin(n = -fee, coinsource = ewcfg.coinsource_revival)
			#market_data.slimes_revivefee += fee
			#player_data.busted = False
			
			# Preserve negaslime
			if player_data.slime < 0:
				#market_data.negaslime += player_data.slime
				player_data.change_slime(n = -player_data.slime) # set to 0

			# reset slimelevel to zero
			player_data.slimelevel = 0

			# Set time of last revive. This used to provied spawn protection, but currently isn't used.
			player_data.time_lastrevive = time_now

			
			if player_data.degradation >= 100:
				player_data.life_state = ewcfg.life_state_shambler
				player_data.change_slime(n = 0.5 * ewcfg.slimes_shambler)
				player_data.trauma = ""
				poi_death = ewcfg.id_to_poi.get(player_data.poi_death)
				if ewmap.inaccessible(poi = poi_death, user_data = player_data):
					player_data.poi = ewcfg.poi_id_endlesswar
				else:
					player_data.poi = poi_death.id_poi
			else:
				# Set life state. This is what determines whether the player is actually alive.
				player_data.life_state = ewcfg.life_state_juvenile
				# Give player some initial slimes.
				player_data.change_slime(n = ewcfg.slimes_onrevive)
				# Get the player out of the sewers.
				player_data.poi = ewcfg.poi_id_endlesswar



			player_data.persist()
			market_data.persist()

			# Shower every district in the city with slime from the sewers.
			sewer_data = EwDistrict(district = ewcfg.poi_id_thesewers, id_server = cmd.guild.id)
			# the amount of slime showered is divided equally amongst the districts
			districts_amount = len(ewcfg.capturable_districts)
			geyser_amount = int(0.5 * sewer_data.slime / districts_amount)
			# Get a list of all the districts
			for poi in ewcfg.capturable_districts:
				district_data = EwDistrict(district = poi, id_server = cmd.guild.id)

				district_data.change_slime(n = geyser_amount)
				sewer_data.change_slime(n = -1 * geyser_amount)

				district_data.persist()
				sewer_data.persist()

			sewer_inv = ewitem.inventory(id_user=sewer_data.name, id_server=sewer_data.id_server)
			for item in sewer_inv:
				district = ewcfg.poi_id_slimesea
				if random.random() < 0.5:
					district = random.choice(ewcfg.capturable_districts)
				ewitem.give_item(id_item=item.get("id_item"), id_user=district, id_server=sewer_data.id_server)

			await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)

			response = '{slime4} Geysers of fresh slime erupt from every manhole in the city, showering their surrounding districts. {slime4} {name} has been reborn in slime. {slime4}'.format(
				slime4 = ewcfg.emote_slime4, name = cmd.message.author.name)
		else:
			response = 'You\'re not dead just yet.'

	#	deathreport = "You were {} by {}. {}".format(kill_descriptor, cmd.message.author.name, ewcfg.emote_slimeskull)
	#	deathreport = "{} ".format(ewcfg.emote_slimeskull) + ewutils.formatMessage(member, deathreport)

		if slimeoid.life_state == ewcfg.slimeoid_state_active:
			reunite = ""
			brain = ewcfg.brain_map.get(slimeoid.ai)
			reunite += brain.str_revive.format(
			slimeoid_name = slimeoid.name
			)
			new_poi = ewcfg.id_to_poi.get(player_data.poi)
			revivechannel = ewutils.get_channel(cmd.guild, new_poi.channel)
			reunite = ewutils.formatMessage(cmd.message.author, reunite)
			await ewutils.send_message(cmd.client, revivechannel, reunite)

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


""" haunt living players to steal slime """
async def haunt(cmd):
	time_now = int(time.time())
	response = ""
	resp_cont = ewutils.EwResponse(id_server = cmd.guild.id)

	if cmd.mentions_count > 1:
		response = "You can only spook one person at a time. Who do you think you are, the Lord of Ghosts?"
	else: 
		haunted_data = None
		member = None
		if cmd.mentions_count == 0 and cmd.tokens_count > 1:
			server = cmd.guild
			member = server.get_member(ewutils.getIntToken(cmd.tokens))
			haunted_data = EwPlayer(member = member)
		elif cmd.mentions_count == 1:
			member = cmd.mentions[0]
			haunted_data = EwPlayer(member = member)
		
		if member:
			# Get the user and target data from the database.
			user_data = EwPlayer(member = cmd.message.author)
			market_data = EwMarket(id_server = cmd.guild.id)
			target_mutations = haunted_data.get_mutations()
			target_poi = ewcfg.id_to_poi.get(haunted_data.poi)
			target_is_shambler = haunted_data.life_state == ewcfg.life_state_shambler
			target_is_inhabitted = haunted_data.id_user == user_data.get_inhabitee()


			if user_data.life_state != ewcfg.life_state_corpse:
				# Only dead players can haunt.
				response = "You can't haunt now. Try {}.".format(ewcfg.cmd_suicide)
			elif haunted_data.life_state == ewcfg.life_state_kingpin:
				# Disallow haunting of generals.
				response = "He is too far from the sewers in his ivory tower, and thus cannot be haunted."
			elif (time_now - user_data.time_lasthaunt) < ewcfg.cd_haunt:
				# Disallow haunting if the user has haunted too recently.
				response = "You're being a little TOO spooky lately, don't you think? Try again in {} seconds.".format(int(ewcfg.cd_haunt-(time_now-user_data.time_lasthaunt)))
			elif ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
				response = "You can't commit violence from here."
			elif target_poi.pvp == False:
			#Require the target to be in a PvP area, and flagged if it's a remote haunt
				response = "{} is not mired in the ENDLESS WAR right now.".format(member.name)
			elif haunted_data.life_state == ewcfg.life_state_corpse:
				# Dead players can't be haunted.
				response = "{} is already dead.".format(member.name)
			elif haunted_data.life_state == ewcfg.life_state_grandfoe:
				# Grand foes can't be haunted.
				response = "{} is invulnerable to ghosts.".format(member.name)
			elif haunted_data.life_state == ewcfg.life_state_enlisted or haunted_data.life_state == ewcfg.life_state_juvenile or haunted_data.life_state == ewcfg.life_state_shambler:
				haunt_power_multiplier = 1

				# power to the ancients
				ghost_age = time_now - user_data.time_lastdeath
				if ghost_age > 60 * 60 * 24 * 7: # dead for longer than
					if ghost_age > 60 * 60 * 24 * 365: # one friggin year
						haunt_power_multiplier *= 2.5
					if ghost_age > 60 * 60 * 24 * 90: # three months
						haunt_power_multiplier *= 2
					elif ghost_age > 60 * 60 * 24 * 30: # one month
						haunt_power_multiplier *= 1.5
					else: # one week
						haunt_power_multiplier *= 1.25

				# vitriol as virtue
				list_ids = []
				for quadrant in ewcfg.quadrant_ids:
					quadrant_data = ewquadrants.EwQuadrant(id_server=cmd.guild.id, id_user=cmd.message.author.id, quadrant=quadrant)
					if quadrant_data.id_target != -1 and quadrant_data.check_if_onesided() is False:
						list_ids.append(quadrant_data.id_target)
					if quadrant_data.id_target2 != -1 and quadrant_data.check_if_onesided() is False:
						list_ids.append(quadrant_data.id_target2)
				if haunted_data.id_user in list_ids: # any mutual quadrants
					haunt_power_multiplier *= 1.2
				if haunted_data.faction and ((not user_data.faction) or (user_data.faction != haunted_data.faction)): # opposite faction (or no faction at all)
					haunt_power_multiplier *= 1.2
				if user_data.id_killer == haunted_data.id_user: # haunting your murderer/buster
					haunt_power_multiplier *= 1.2

				# places of power.
				if haunted_data.poi in [ewcfg.poi_id_thevoid, ewcfg.poi_id_wafflehouse, ewcfg.poi_id_blackpond]:
					haunt_power_multiplier *= 2
				elif haunted_data.poi in ewmap.get_void_connection_pois(cmd.guild.id):
					haunt_power_multiplier *= 1.25

				# glory to the vanquished
				target_kills = haunted_data.get_stat(metric = ewcfg.stat_kills)
				if target_kills > 5:
					haunt_power_multiplier *= 1.25 + ((target_kills - 5) / 100) # 1% per kill after 5
				else:
					haunt_power_multiplier *= 1 + (target_kills * 5 / 100) # 5% per kill
					
				if time_now - haunted_data.time_lastkill < (60 * 15):
					haunt_power_multiplier *= 1.5 # wet hands

				# misc
				if ewcfg.weather_map.get(market_data.weather) == ewcfg.weather_foggy:
					haunt_power_multiplier *= 1.1
				if not haunted_data.has_soul:
					haunt_power_multiplier *= 1.2
				# uncomment this after moon mechanics update
				# if (market_data.day % 31 == 15 and market_data.clock >= 20) or (market_data.day % 31 == 16 and market_data.clock <= 6):
				# 	haunt_power_multiplier *= 2

				# divide haunt power by 2 if not in same area
				if user_data.poi != haunted_data.poi:
					haunt_power_multiplier /= 2

				# Double Halloween
				#haunt_power_multiplier *= 4

				haunted_slimes = int((haunted_data.slime / ewcfg.slimes_hauntratio) * haunt_power_multiplier)
				slimes_lost = int(haunted_slimes / 5) # hauntee only loses 1/5th of what the ghost gets as antislime

				if ewcfg.mutation_id_coleblooded in target_mutations:
					haunted_slimes = -10000
					if user_data.slime > haunted_slimes:
						haunted_slimes = user_data.slime

				haunted_data.change_slime(n = -slimes_lost, source = ewcfg.source_haunted)
				user_data.change_slime(n = -haunted_slimes, source = ewcfg.source_haunter)
				market_data.negaslime -= haunted_slimes

				user_data.time_lasthaunt = time_now
				user_data.busted = False
				
				resp_cont.add_member_to_update(cmd.message.author)
				# Persist changes to the database.
				user_data.persist()
				haunted_data.persist()
				market_data.persist()

				response = "{} has been haunted by the ghost of {}! Slime has been lost! {} antislime congeals within you.".format(member.name, cmd.message.author.name, haunted_slimes)
				if ewcfg.mutation_id_coleblooded in target_mutations:
					response = "{} has been haunted by the ghost of {}! Their exorcising coleslaw blood purges {} antislime from your being! Better not do that again.".format(member.name, cmd.message.author.name, -haunted_slimes)

				haunted_channel = ewcfg.id_to_poi.get(haunted_data.poi).channel
				haunt_message = "You feel a cold shiver run down your spine"
				if cmd.tokens_count > 2:
					haunt_message_content = re.sub("<.+>" if cmd.mentions_count == 1 else "\d{17,}", "", cmd.message.content[(len(cmd.tokens[0])):]).strip()
					# Cut down really big messages so discord doesn't crash
					if len(haunt_message_content) > 500:
						haunt_message_content = haunt_message_content[:-500]
					haunt_message += " and faintly hear the words \"{}\"".format(haunt_message_content)
				haunt_message += ". {} slime evaporates from your body.".format(slimes_lost)
				if ewcfg.mutation_id_coleblooded in target_mutations:
					haunt_message += " The ghost that did it wails in agony as their ectoplasm boils in your coleslaw blood!"

				haunt_message = ewutils.formatMessage(member, haunt_message)
				resp_cont.add_channel_response(haunted_channel, haunt_message)
		else:
			# No mentions, or mentions we didn't understand.
			response = "Your spookiness is appreciated, but ENDLESS WAR didn\'t understand that name."

	# Send the response to the player.
	resp_cont.add_channel_response(cmd.message.channel.name, response)
	await resp_cont.post()
	#await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def negapool(cmd):
	# Add persisted negative slime.
	market_data = EwMarket(id_server = cmd.guild.id)
	negaslime = market_data.negaslime

	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "The dead have a total of {:,} negative slime at their disposal for summoning.".format(negaslime)))

async def negaslime(cmd):
	total = ewutils.execute_sql_query("SELECT SUM(slimes) FROM users WHERE slimes < 0 AND id_server = '{}'".format(cmd.guild.id))
	total_negaslimes = total[0][0]
	
	if total_negaslimes:
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "The dead have amassed {:,} negative slime.".format(total_negaslimes)))
	else:
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "There is no negative slime in this world."))


async def summon_negaslimeoid(cmd):
	response = ""
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state != ewcfg.life_state_corpse:
		response = "Only the dead have the occult knowledge required to summon a cosmic horror."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if user_data.poi not in ewcfg.capturable_districts:
		response = "You can't conduct the ritual here."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	name = None
	if cmd.tokens_count > 1:
		#value = ewutils.getIntToken(tokens = cmd.tokens, allow_all = True, negate = True)
		slimeoid = EwSlimeoid(member = cmd.message.author, sltype = ewcfg.sltype_nega)
		if slimeoid.life_state != ewcfg.slimeoid_state_none:
			response = "You already have an active negaslimeoid."
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		negaslimeoid_name = cmd.message.content[(len(cmd.tokens[0])):].strip()

		if len(negaslimeoid_name) > 32:
			response = "That name is too long. ({:,}/32)".format(len(negaslimeoid_name))
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		market_data = EwMarket(id_server = cmd.message.author.guild.id)

		if market_data.negaslime >= 0:
			response = "The dead haven't amassed any negaslime yet."
		else:
			max_level = min(len(str(user_data.slime)) - 1, len(str(market_data.negaslime)) - 1)
			level = random.randint(1, max_level)
			value = 10 ** (level - 1)
			#user_data.change_slime(n = int(value/10))
			market_data.negaslime += value
			slimeoid.sltype = ewcfg.sltype_nega
			slimeoid.life_state = ewcfg.slimeoid_state_active
			slimeoid.level = level
			slimeoid.id_user = str(user_data.id_user)
			slimeoid.id_server = user_data.id_server
			slimeoid.poi = user_data.poi
			slimeoid.name = negaslimeoid_name
			slimeoid.body = random.choice(ewcfg.body_names)
			slimeoid.head = random.choice(ewcfg.head_names)
			slimeoid.legs = random.choice(ewcfg.mobility_names)
			slimeoid.armor = random.choice(ewcfg.defense_names)
			slimeoid.weapon = random.choice(ewcfg.offense_names)
			slimeoid.special = random.choice(ewcfg.special_names)
			slimeoid.ai = random.choice(ewcfg.brain_names)
			for i in range(level):
				rand = random.randrange(3)
				if rand == 0:
					slimeoid.atk += 1
				elif rand == 1:
					slimeoid.defense += 1
				else:
					slimeoid.intel += 1



			user_data.persist()
			slimeoid.persist()
			market_data.persist()

			response = "You have summoned **{}**, a {}-foot-tall Negaslimeoid.".format(slimeoid.name, slimeoid.level)
			desc = ewslimeoid.slimeoid_describe(slimeoid)
			response += desc

	else:
		response = "To summon a negaslimeoid you must first know its name."
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

def generate_negaslimeoid_name():
	titles = ["Angel", "Emissary", "Gaping Maw", "Apostle", "Nemesis", "Harbinger", "Reaper", "Incarnation", "Wanderer", "Berserker", "Outcast", "Monarch", "Anomaly"]
	domains = ["Curses", "Doom", "Oblivion", "Darkness", "Madness", "the Void", "the Deep", "Nightmares", "Wrath", "Pestilence", "the End", "Terror", "Sorrow", "Pain", "Despair", "Souls", "Secrets", "Ruin", "Hatred", "Shadows", "the Night"]
	title = "{} of {}".format(random.choice(titles), random.choice(domains))
	name_length = random.randrange(5,min(10,30-len(title)))
	consonants = random.choice(["chlt","crwx","fhlt","bghl","brpq"])
	vowels = "aeuuooyy"
	num_vowels = random.randrange(int(name_length / 4), int(name_length/3)+1)
	name_list = []
	for i in range(name_length):
		if i < num_vowels:
			name_list.append(random.choice(vowels))
		else:
			name_list.append(random.choice(consonants))
	random.shuffle(name_list)
	apostrophe = random.randrange(1,name_length)
	name = ewutils.flattenTokenListToString(name_list[:apostrophe]) + "'" + ewutils.flattenTokenListToString(name_list[apostrophe:])
	name = name.capitalize()
	full_name = "{}, {}".format(name, title)
	return full_name


"""
	allows ghosts to hook on to living players and follow them around
"""
async def inhabit(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	response = ""
		
	if user_data.life_state != ewcfg.life_state_corpse:
		# Only ghosts can inhabit other players
		response = "You have no idea what you're doing."
	else:
		if cmd.mentions_count > 1:
			response = "Are you trying to split yourself in half? You can only inhabit one body at a time."
		elif cmd.mentions_count == 1:
			member = cmd.mentions[0]
			target_data = EwPlayer(member = member)

			if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
				# Has to be done in a gameplay channel
				response = "You can't disturb the living from here."
			elif cmd.message.channel.name == ewcfg.channel_sewers:
				# Can't be done from the sewers
				response = "Try doing that in the overworld, it's difficult from down here."
			elif target_data.life_state == ewcfg.life_state_kingpin:
				# Can't target generals
				response = "He is far too strong for you to inhabit his body."
			elif user_data.poi != target_data.poi:
				# Player must be on the same location as their target
				response = "You'll have to find them first."
			elif target_data.life_state == ewcfg.life_state_corpse:
				# Can't target ghosts
				response = "You can't do that to your fellow ghost."
			elif ewmap.poi_is_pvp(target_data.poi) == False:
				response = "You can't torment the living here."
			else:
				# cancel the ghost's movement
				ewutils.moves_active[cmd.message.author.id] = 0
				# drop any previous inhabitation by the ghost
				user_data.remove_inhabitation()
				# add the new inhabitation
				ewutils.execute_sql_query(
					"REPLACE INTO inhabitations({id_ghost}, {id_fleshling}, {id_server}) VALUES (%s, %s, %s)".format(
						id_ghost = ewcfg.col_id_ghost,
						id_fleshling = ewcfg.col_id_fleshling,
						id_server = ewcfg.col_id_server,
					),(
						user_data.id_user,
						target_data.id_user,
						user_data.id_server,
					)
				)

				response = "{}\'s body is inhabitted by the ghost of {}!".format(member.name, cmd.message.author.name)
		else:
			response = "Your spookiness is appreciated, but ENDLESS WAR didn\'t understand that name."

	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def let_go(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	response = ""

	if user_data.life_state != ewcfg.life_state_corpse:
		# Only ghosts can inhabit other players
		response = "You feel a bit more at peace with the world."
	elif not user_data.get_inhabitee():
		response = "You're not **{}**ing anyone right now.".format(ewcfg.cmd_inhabit)
	else:
		user_data.remove_inhabitation()
		response = "You let go of the soul you've been tormenting."

	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def possess_weapon(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	response = ""
	if user_data.life_state != ewcfg.life_state_corpse:
		response = "You have no idea what you're doing."
	elif not user_data.get_inhabitee():
		response = "You're not **{}**ing anyone right now.".format(ewcfg.cmd_inhabit)
	elif user_data.slime >= ewcfg.slimes_to_possess_weapon:
		response = "You'll have to become stronger before you can perform occult arts of this level."
	else:
		server = cmd.guild
		inhabitee_id = user_data.get_inhabitee()
		inhabitee_data = EwPlayer(id_user = inhabitee_id, id_server = user_data.id_server)
		inhabitee_member = server.get_member(inhabitee_id)
		inhabitee_name = inhabitee_member.name
		if inhabitee_data.weapon < 0:
			response = "{} is not wielding a weapon right now.".format(inhabitee_name)
		elif inhabitee_data.get_possession():
			response = "{} is already being possessed.".format(inhabitee_name)
		else:
			proposal_response = "You propose a trade to {}.\n" \
				"You will possess their weapon to empower it, and in return they'll sacrifice a fifth of their slime to your name upon their next kill.\n" \
				"Will they **{}** this exchange, or **{}** it?".format(inhabitee_name, ewcfg.cmd_accept, ewcfg.cmd_refuse)
			await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, proposal_response))
    
			accepted = False
			try:
				msg = await cmd.client.wait_for('message', timeout = 30, check=lambda message: message.author == inhabitee_member and 
														message.content.lower() in [ewcfg.cmd_accept, ewcfg.cmd_refuse])
				if msg != None:
					if msg.content.lower() == ewcfg.cmd_accept:
						accepted = True
					elif msg.content.lower() == ewcfg.cmd_refuse:
						accepted = False
			except:
				accepted = False

			if accepted:
				ewutils.execute_sql_query(
				"UPDATE inhabitations SET {empowered} = %s WHERE {id_fleshling} = %s AND {id_ghost} = %s".format(
					empowered = ewcfg.col_empowered,
					id_fleshling = ewcfg.col_id_fleshling,
					id_ghost = ewcfg.col_id_ghost,
				), (
					'weapon',
					inhabitee_id,
					user_data.id_user,
				))
				user_data.change_slime(n = -ewcfg.slimes_to_possess_weapon, source = ewcfg.source_ghost_contract)
				user_data.persist()
				accepted_response = "You feel a metallic taste in your mouth as you sign {}'s spectral contract. You see them bind themselves to your weapon, which now bears their mark. It feels cold to the touch.".format(cmd.message.author.name)
				await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(inhabitee_member, accepted_response))
			else:
				response = "You should've known better, why would anyone ever trust you?"
	
	if response:
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def possess_fishing_rod(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	response = ""
	if user_data.life_state != ewcfg.life_state_corpse:
		response = "You have no idea what you're doing."
	elif not user_data.get_inhabitee():
		response = "You're not **{}**ing anyone right now.".format(ewcfg.cmd_inhabit)
	elif user_data.slime >= ewcfg.slimes_to_possess_fishing_rod:
		response = "You'll have to become stronger before you can perform occult arts of this level."
	else:
		server = cmd.guild
		inhabitee_id = user_data.get_inhabitee()
		inhabitee_data = EwPlayer(id_user = inhabitee_id, id_server = user_data.id_server)
		inhabitee_member = server.get_member(inhabitee_id)
		inhabitee_name = inhabitee_member.name
		if inhabitee_data.get_possession():
			response = "{} is already being possessed.".format(inhabitee_name)
		else:
			proposal_response = "You propose a trade to {}.\n" \
				"You will possess their fishing rod to enhance it, making it more attractive to fish. In exchange, you will corrupt away all of the fish's slime, and absorb it as antislime.\n" \
				"Both of you will need to reel the fish in together, and failing to do so will nullify this contract.\nWill they **{}** this exchange, or **{}** it?".format(inhabitee_name, ewcfg.cmd_accept, ewcfg.cmd_refuse)
			await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, proposal_response))
    
			accepted = False
			try:
				msg = await cmd.client.wait_for('message', timeout = 30, check=lambda message: message.author == inhabitee_member and 
														message.content.lower() in [ewcfg.cmd_accept, ewcfg.cmd_refuse])
				if msg != None:
					if msg.content.lower() == ewcfg.cmd_accept:
						accepted = True
					elif msg.content.lower() == ewcfg.cmd_refuse:
						accepted = False
			except:
				accepted = False

			if accepted:
				ewutils.execute_sql_query(
				"UPDATE inhabitations SET {empowered} = %s WHERE {id_fleshling} = %s AND {id_ghost} = %s".format(
					empowered = ewcfg.col_empowered,
					id_fleshling = ewcfg.col_id_fleshling,
					id_ghost = ewcfg.col_id_ghost,
				), (
					'rod',
					inhabitee_id,
					user_data.id_user,
				))
				user_data.change_slime(n = -ewcfg.slimes_to_possess_fishing_rod, source = ewcfg.source_ghost_contract)
				user_data.persist()
				accepted_response = "You feel a metallic taste in your mouth as you sign {}'s spectral contract. Their ghastly arms superpose yours, enhancing your grip and causing shadowy tendrils to appear near your rod's hook.".format(cmd.message.author.name)
				await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(inhabitee_member, accepted_response))
			else:
				response = "You should've known better, why would anyone ever trust you?"
	
	if response:
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def crystalize_negapoudrin(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	response = ""
	if user_data.life_state != ewcfg.life_state_corpse:
		response = "What the fuck do you think you're doing, you corporeal bitch?"
	elif user_data.slime >= ewcfg.slimes_to_crystalize_negapoudrin:
		response = "Crystalizing a negapoudrin requires a lot of negaslime, and you're not quite there yet."
	else:
		negapoudrin_data = next(i for i in ewcfg.item_list if i.id_item == ewcfg.item_id_negapoudrin)
		ewitem.item_create(
			item_type = ewcfg.it_item,
			id_user = user_data.id_user,
			id_server = cmd.guild.id,
			item_props={
				'id_item': negapoudrin_data.id_item,
				'item_name': negapoudrin_data.str_name,
				'item_desc': negapoudrin_data.str_desc,
			}
		)
		user_data.change_slime(n = -ewcfg.slimes_to_crystalize_negapoudrin, source = ewcfg.source_spending)
		user_data.persist()
		response = "The cathedral's bells toll in the distance, and a rumbling {} can be heard echoing from deep within the sewers. A negapoudrin has formed.".format(ewcfg.cmd_boo)
	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
