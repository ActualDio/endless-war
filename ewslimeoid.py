import random
import asyncio
import time

import ewcfg
import ewutils
import ewitem
import ewrolemgr
import ewstats
import ewmap
import ewcasino
import ewquadrants

from ew import EwPlayer
from ewmarket import EwMarket
from ewdistrict import EwDistrict
from ewplayer import EwDiscordUser
from ewitem import EwItem

active_slimeoidbattles = {}		

"""
	Commands
"""

# play with your slimeoid
async def playfetch(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	time_now = int(time.time())

	if user_data.life_state == ewcfg.life_state_corpse:
			response = "Slimeoids don't fuck with ghosts."

	elif user_data.has_soul == 0:
		response = "You reel back to throw the stick, but your motivation wears thin halfway through. You drop it on the ground with a sigh."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You do not have a Slimeoid to play fetch with."

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
			response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."

	elif (time_now - slimeoid.time_defeated) < ewcfg.cd_slimeoiddefeated:
			response = "{} is too beat up from its last battle to play fetch right now.".format(slimeoid.name)

	else:
		head = ewcfg.head_map.get(slimeoid.head)
		response = head.str_fetch.format(
			slimeoid_name = slimeoid.name
		)

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def observeslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	time_now = int(time.time())

	if user_data.life_state == ewcfg.life_state_corpse:
			response = "Slimeoids don't fuck with ghosts."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You do not have a Slimeoid to observe."

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
			response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."

	elif (time_now - slimeoid.time_defeated) < ewcfg.cd_slimeoiddefeated:
			response = "{} lies totally inert, recuperating from being recently pulverized.".format(slimeoid.name)

	else:
		options = [
			'body',
			'weapon',
			'special',
			'brain',
		]

		roll = random.randrange(len(options))
		result = options[roll]

		if result == 'body':
			part = ewcfg.body_map.get(slimeoid.body)

		if result == 'weapon':
			part = ewcfg.offense_map.get(slimeoid.weapon)

		if result == 'special':
			part = ewcfg.special_map.get(slimeoid.special)

		if result == 'brain':
			part = ewcfg.brain_map.get(slimeoid.ai)

		response = part.str_observe.format(
			slimeoid_name = slimeoid.name
		)

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def petslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	time_now = int(time.time())
	target = None
	target_data = None
	list_ids = None

	#mentions[0]
	if cmd.mentions_count > 0:
		target = cmd.mentions[0]
		target_data = EwPlayer(member=target)

		list_ids = []

		for quadrant in ewcfg.quadrant_ids:
			quadrant_data = ewquadrants.EwQuadrant(id_server=cmd.guild.id, id_user=cmd.message.author.id, quadrant=quadrant)
			if quadrant_data.id_target != -1 and quadrant_data.check_if_onesided() is False:
				list_ids.append(quadrant_data.id_target)
			if quadrant_data.id_target2 != -1 and quadrant_data.check_if_onesided() is False:
				list_ids.append(quadrant_data.id_target2)


		if target_data.poi != user_data.poi:
			response = "You can't pet them because they aren't here."
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		elif target_data.id_user not in list_ids:
			response = "You try to pet {}'s slimeoid, but you're not close enough for them to trust you. Better whip out those quadrants...".format(target.name)
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		elif target_data.life_state == ewcfg.life_state_corpse:
			response = "Slimeoids don't fuck with ghosts.".format(target.name)
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		else:
			slimeoid = EwSlimeoid(member=target)

	if user_data.life_state == ewcfg.life_state_corpse:
			response = "Slimeoids don't fuck with ghosts."

	elif cmd.mentions_count > 1:
		response = "Getting a bit too touchy-feely with these slimeoids, eh? You can only pet one at a time."

	elif user_data.has_soul == 0:
		response = "The idea doesn't even occur to you because your soul is missing."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You do not have a Slimeoid to pet."

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
			response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."

	elif (time_now - slimeoid.time_defeated) < ewcfg.cd_slimeoiddefeated:
			response = "{} whimpers. It's still recovering from being beaten up.".format(slimeoid.name)

	else:

		armor = ewcfg.defense_map.get(slimeoid.armor)
		response = armor.str_pet.format(
			slimeoid_name = slimeoid.name
		)
		response += " "
		brain = ewcfg.brain_map.get(slimeoid.ai)
		response += brain.str_pet.format(
			slimeoid_name = slimeoid.name
		)

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def abuseslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	time_now = int(time.time())
	target = None
	target_data = None
	list_ids = None

	#mentions[0]
	if cmd.mentions_count > 0:
		target = cmd.mentions[0]
		target_data = EwPlayer(member=target)

		list_ids = []

		for quadrant in ewcfg.quadrant_ids:
			quadrant_data = ewquadrants.EwQuadrant(id_server=cmd.guild.id, id_user=cmd.message.author.id, quadrant=quadrant)
			if quadrant_data.id_target != -1 and quadrant_data.check_if_onesided() is False:
				list_ids.append(quadrant_data.id_target)
			if quadrant_data.id_target2 != -1 and quadrant_data.check_if_onesided() is False:
				list_ids.append(quadrant_data.id_target2)


		if target_data.poi != user_data.poi:
			response = "You can't beat them up them because they aren't here."
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		elif target_data.id_user not in list_ids:
			response = "You try to lynch {}'s slimeoid, but you're not close enough for them to trust you. Better whip out those quadrants...".format(target.name)
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		elif target_data.life_state == ewcfg.life_state_corpse:
			response = "Slimeoids don't fuck with ghosts.".format(target.name)
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		else:
			slimeoid = EwSlimeoid(member=target)

	if user_data.life_state == ewcfg.life_state_corpse:
			response = "Slimeoids don't fuck with ghosts."

	elif cmd.mentions_count > 1:
		response = "Control your anger! Everybody knows it's more efficient to inflict trauma on one slimeoid at a time."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You do not have a Slimeoid to hurt."

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
			response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."

	#elif (time_now - slimeoid.time_defeated) < ewcfg.cd_slimeoiddefeated:
	#		response = "{} whimpers. It's still recovering from being beaten up.".format(slimeoid.name)

	else:

		armor = ewcfg.defense_map.get(slimeoid.armor)
		response = armor.str_abuse.format(
			slimeoid_name = slimeoid.name
		)
		response += " "
		brain = ewcfg.brain_map.get(slimeoid.ai)
		response += brain.str_abuse.format(
			slimeoid_name = slimeoid.name
		)
		slimeoid.time_defeated = time_now
		slimeoid.persist()
	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))



async def walkslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	time_now = int(time.time())

	if user_data.life_state == ewcfg.life_state_corpse:
			response = "Slimeoids don't fuck with ghosts."

	elif user_data.has_soul == 0:
		response = "Why take it on a walk? It's not like it understands your needs."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You do not have a Slimeoid to take for a walk."

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
			response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."

	elif (time_now - slimeoid.time_defeated) < ewcfg.cd_slimeoiddefeated:
			response = "{} can barely move. It's still recovering from its injuries.".format(slimeoid.name)

	else:
		brain = ewcfg.brain_map.get(slimeoid.ai)
		response = brain.str_walk.format(
			slimeoid_name = slimeoid.name
		)
		poi = ewcfg.id_to_poi.get(user_data.poi)
		response += " With that done, you go for a leisurely stroll around {}, while ".format(poi.str_name)
		legs = ewcfg.mobility_map.get(slimeoid.legs)
		response += legs.str_walk.format(
			slimeoid_name = slimeoid.name
		)

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

# read the instructions
async def instructions(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	#roles_map_user = ewutils.getRoleMap(message.author.roles)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "There's no instructions to read here."

	else:
		response = "Welcome to SlimeCorp's Brawlden Laboratory Facilities."
		response += "\n\nThis facility specializes in the emerging technology of Slimeoids, or slime-based artificial lifeforms. Research into the properties of Slimeoids is ongoing, but already great advancements in the field have been made and we are proud to be the first to make them commercially available."
		response += "\n\nThis laboratory is equipped with everything required for the creation of a Slimeoid from scratch. To create a Slimeoid, you will need to supply one (1) Slime Poudrin, which will serve as the locus around which your Slimeoid will be based. You will also need to supply some Slime. You may supply as much or as little slime as you like, but greater Slime contribution will lead to superior Slimeoid genesis. To begin the Slimeoid creation process, use **!incubateslimeoid** followed by the amount of slime you wish to use."
		response += "\n\nAfter beginning incubation, you will need to use the console to adjust your Slimeoid's features while it is still forming. Use **!growbody**, **!growhead**, **!growlegs**, **!growweapon**, **!growarmor**, **!growspecial**, or **!growbrain** followed by a letter (A - G) to choose the appearance, abilities, and temperament of your Slimeoid. You will also need to give youe Slimeoid a name. Use **!nameslimeoid** followed by your desired name. These traits may be changed at any time before the incubation is completed."
		response += "\n\nIn addition to physical features, you will need to allocate your Slimeoid's attributes. Your Slimeoid will have a different amount of potential depending on how much slime you invested in its creation. You must distribute this potential across the three Slimeoid attributes, Moxie, Grit, and Chutzpah. Use **!raisemoxie**, **!lowermoxie**, **!raisegrit**, **!lowergrit**, **!raisechutzpah**, and **!lowerchutzpah** to adjust your Slimeoid's attributes to your liking."
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		response = "\n\nWhen all of your Slimeoid's traits are confirmed, use **!spawnslimeoid** to end the incubation and eject your Slimeoid from the gestation vat. Be aware that once spawned, the Slimeoid's traits are finalized and cannot be changed, so be sure you are happy with your Slimeoid's construction before spawning. Additionally, be aware that you may only have one Slimeoid at a time, meaning should you ever want a new Slimeoid, you will need to euthanise your old one with **!dissolveslimeoid**. SlimeCorp assumes no responsibility for accidents, injuries, infections, physical disabilities, or ideological radicalizations that may occur due to prolonged contact with slime-based lifeforms."
		response += "\n\nYou can read a full description of your or someone else's Slimeoid with the **!slimeoid** command. Note that your Slimeoid, having been made out of slime extracted from your body, will recognize you as its master and follow you until such time as you choose to dispose of it. It will react to your actions, including when you kill an opponent, when you are killed, when you return from the dead, and when you !howl. In addition, you can also perform activities with your Slimeoid. Try **!observeslimeoid**, **!petslimeoid**, **!walkslimeoid**, and **!playfetch** and see what happens."
		response += "\n\nSlimeoid research is ongoing, and the effects of a Slimeoid's physical makeup, brain structure, and attribute allocation on its abilities are a rapidly advancing field. Field studies into the effects of these variables on one-on-one Slimeoid battles are set to begin in the near future. In the meantime, report any unusual findings or behaviors to the Cop Killer and Rowdy Fucker, who have much fewer important things to spend their time on than SlimeCorp employees."
		response += "\n\nThank you for choosing SlimeCorp.{}".format(ewcfg.emote_slimecorp)


	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

# Create a slimeoid
async def incubateslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	#roles_map_user = ewutils.getRoleMap(message.author.roles)

	poudrin = ewitem.find_item(item_search = ewcfg.item_id_slimepoudrin, id_user = cmd.message.author.id, id_server = cmd.guild.id if cmd.guild is not None else None, item_type_filter = ewcfg.it_item)
	slimeoid_count = get_slimeoid_count(user_id=cmd.message.author.id, server_id=cmd.guild.id)
	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
		response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif poudrin is None:
		response = "You need a slime poudrin."

	elif slimeoid_count >= 3:
		response = "You have too many slimeoids."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		value = None
		if cmd.tokens_count > 1:
			value = ewutils.getIntToken(tokens = cmd.tokens, allow_all = True)
		if value != None:
			user_data = EwPlayer(member = cmd.message.author)
			slimeoid = EwSlimeoid(member = cmd.message.author)
			market_data = EwMarket(id_server = cmd.message.author.guild.id)
			if value == -1:
				value = user_data.slime

			if slimeoid.life_state == ewcfg.slimeoid_state_active:
				response = "You have already created a Slimeoid. Dissolve your current slimeoid before incubating a new one."

			elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
				response = "You are already in the process of incubating a Slimeoid."

			elif value > user_data.slime:
				response = "You do not have that much slime to sacrifice."

			else:
				# delete a slime poudrin from the player's inventory
				ewitem.item_delete(id_item = poudrin.get('id_item'))

				level = len(str(value))
				user_data.change_slime(n = -value)
				slimeoid.life_state = ewcfg.slimeoid_state_forming
				slimeoid.level = level
				slimeoid.id_user = str(user_data.id_user)
				slimeoid.id_server = user_data.id_server

				user_data.persist()
				slimeoid.persist()

				response = "You place a poudrin into a small opening on the console. As you do, a needle shoots up and pricks your finger, intravenously extracting {} slime from your body. The poudrin is then dropped into the gestation tank. Looking through the observation window, you see what was once your slime begin to seep into the tank and accrete around the poudrin. The incubation of a new Slimeoid has begun! {}".format(str(value), ewcfg.emote_slime2)

		else:
			response = "You must contribute some of your own slime to create a Slimeoid. Specify how much slime you will sacrifice."

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

# Create a slimeoid
async def dissolveslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)
	#roles_map_user = ewutils.getRoleMap(message.author.roles)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
		response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
		response = "You have no slimeoid to dissolve."

	elif active_slimeoidbattles.get(slimeoid.id_slimeoid):
		response = "You can't do that right now."

	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		if slimeoid.life_state == ewcfg.slimeoid_state_forming:
			response = "You hit a large red button with a white X on it. Immediately a buzzer goes off and the half-formed body of what would have been your new Slimeoid is flushed out of the gestation tank and down a drainage tube, along with your poudrin and slime. What a waste."
		else:
			brain = ewcfg.brain_map.get(slimeoid.ai)
			response = brain.str_dissolve.format(
				slimeoid_name = slimeoid.name
			)
			response += "{}".format(ewcfg.emote_slimeskull)

			cosmetics = ewitem.inventory(
				id_user = cmd.message.author.id,
				id_server = cmd.guild.id,
				item_type_filter = ewcfg.it_cosmetic
			)

			# get the cosmetics worn by the slimeoid
			for item in cosmetics:
				cos = EwItem(id_item = item.get('id_item'))
				if cos.item_props.get('slimeoid') == 'true':
					cos.item_props['slimeoid'] = 'false'
					cos.persist()

			ewutils.execute_sql_query(
				"DELETE FROM slimeoids WHERE {id_user} = %s AND {id_server} = %s".format(
					id_user=ewcfg.col_id_user,
					id_server=ewcfg.col_id_server,
				), (
					slimeoid.id_user,
					slimeoid.id_server,
				))
		
		user_data.active_slimeoid = -1
		user_data.persist()
		

	# Send the response to the player.

	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

# shape your slimeoid's body

async def growbody(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			body = ewcfg.body_map.get(value)
			if body != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(body.str_create)
					slimeoid.body = body.id_body
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the body console labelled A through G."
			else:
				response = "Choose an option from the buttons on the body console labelled A through G."
		else:
			response = "You must specify a body type. Choose an option from the buttons on the body console labelled A through G."

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


# shape your slimeoid's head
async def growhead(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			head = ewcfg.head_map.get(value)
			if head != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(head.str_create)
					slimeoid.head = head.id_head
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the head console labelled A through G."
			else:
				response = "Choose an option from the buttons on the head console labelled A through G."
		else:
			response = "You must specify a head type. Choose an option from the buttons on the head console labelled A through G."

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

# shape your slimeoid's legs
async def growlegs(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			mobility = ewcfg.mobility_map.get(value)
			if mobility != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(mobility.str_create)
					slimeoid.legs = mobility.id_mobility
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the mobility console labelled A through G."
			else:
				response = "Choose an option from the buttons on the mobility console labelled A through G."
		else:
			response = "You must specify means of locomotion. Choose an option from the buttons on the mobility console labelled A through G."

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

# shape your slimeoid's weapon
async def growweapon(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			offense = ewcfg.offense_map.get(value)
			if offense != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(offense.str_create)
					slimeoid.weapon = offense.id_offense
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the weapon console labelled A through G."
			else:
				response = "Choose an option from the buttons on the weapon console labelled A through G."
		else:
			response = "You must specify a means of attack. Choose an option from the buttons on the weapon console labelled A through G."

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

# shape your slimeoid's armor
async def growarmor(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			defense = ewcfg.defense_map.get(value)
			if defense != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(defense.str_create)
					slimeoid.armor = defense.id_defense
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the armor console labelled A through G."
			else:
				response = "Choose an option from the buttons on the armor console labelled A through G."
		else:
			response = "You must specify a method of protection. Choose an option from the buttons on the armor console labelled A through G."

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

# shape your slimeoid's special ability
async def growspecial(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			special = ewcfg.special_map.get(value)
			if special != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(special.str_create)
					slimeoid.special = special.id_special
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the special attack console labelled A through G."
			else:
				response = "Choose an option from the buttons on the special attack console labelled A through G."
		else:
			response = "You must specify a special attack type. Choose an option from the buttons on the special attack console labelled A through G."

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

# shape your slimeoid's brain.
async def growbrain(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		value = None
		if cmd.tokens_count > 1:
			value = cmd.tokens[1]
			value = value.lower()
			brain = ewcfg.brain_map.get(value)
			if brain != None:
				if value in ["a", "b", "c", "d", "e", "f", "g"]:
					response = " {}".format(brain.str_create)
					slimeoid.ai = brain.id_brain
					slimeoid.persist()
				else:
					response = "Choose an option from the buttons on the brain console labelled A through G."
			else:
				response = "Choose an option from the buttons on the brain console labelled A through G."
		else:
			response = "You must specify a brain structure. Choose an option from the buttons on the brain console labelled A through G."

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

# Name your slimeoid.
async def nameslimeoid(cmd):
	name = ""
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid already has a name."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		if cmd.tokens_count < 2:
			response = "You must specify a name."
		else:
			name = cmd.message.content[(len(ewcfg.cmd_nameslimeoid)):].strip()

			if len(name) > 32:
				response = "That name is too long. ({:,}/32)".format(len(name))

			else:
				slimeoid.name = str(name)

				user_data.persist()
				slimeoid.persist()

				response = "You enter the name {} into the console.".format(str(name))

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

#allocate a point to ATK
async def raisemoxie(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		if ((slimeoid.atk + slimeoid.defense + slimeoid.intel) >= (slimeoid.level)):
			response = "You have allocated all of your Slimeoid's potential. Try !lowering some of its attributes first."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))

		else:
			slimeoid.atk += 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid gains more moxie."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

#allocate a point to ATK
async def lowermoxie(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		if (slimeoid.atk <= 0):
			response = "You cannot reduce your slimeoid's moxie any further."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))

		else:
			slimeoid.atk -= 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid loses some moxie."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

#allocate a point to DEF
async def raisegrit(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		if ((slimeoid.atk + slimeoid.defense + slimeoid.intel) >= (slimeoid.level)):
			response = "You have allocated all of your Slimeoid's potential. Try !lowering some of its attributes first."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))

		else:
			slimeoid.defense += 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid gains more grit."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

#allocate a point to ATK
async def lowergrit(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		if (slimeoid.defense <= 0):
			response = "You cannot reduce your slimeoid's grit any further."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))

		else:
			slimeoid.defense -= 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid loses some grit."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

#allocate a point to DEF
async def raisechutzpah(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		if ((slimeoid.atk + slimeoid.defense + slimeoid.intel) >= (slimeoid.level)):
			response = "You have allocated all of your Slimeoid's potential. Try !lowering some of its attributes first."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))

		else:
			slimeoid.intel += 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid gains more chutzpah."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

#allocate a point to ATK
async def lowerchutzpah(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You must begin incubating a new slimeoid first."

	elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "Your slimeoid is already fully formed."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		if (slimeoid.intel <= 0):
			response = "You cannot reduce your slimeoid's chutzpah any further."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))

		else:
			slimeoid.intel -= 1
			points = (slimeoid.level - slimeoid.atk - slimeoid.defense - slimeoid.intel)

			user_data.persist()
			slimeoid.persist()

			response = "Your gestating slimeoid loses some chutzpah."
			response += "\nMoxie: {}".format(str(slimeoid.atk))
			response += "\nGrit: {}".format(str(slimeoid.defense))
			response += "\nChutzpah: {}".format(str(slimeoid.intel))
			response += "\nPoints remaining: {}".format(str(points))

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))




# complete a slimeoid
async def spawnslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)
	response = ""
	#roles_map_user = ewutils.getRoleMap(message.author.roles)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to create a Slimeoid."

	elif user_data.life_state == ewcfg.life_state_corpse:
			response = "Ghosts cannot interact with the SlimeCorp Lab apparati."


	else:

		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		if slimeoid.life_state == ewcfg.slimeoid_state_active:
			response = "You have already created a Slimeoid. Dissolve your current slimeoid before incubating a new one."

		elif slimeoid.life_state == ewcfg.slimeoid_state_none:
			response = "You have not yet begun incubating a slimeoid."

		else:
			needsbody = False
			needshead = False
			needslegs = False
			needsarmor = False
			needsweapon = False
			needsspecial = False
			needsbrain = False
			needsname = False
			needsstats = False
			incomplete = False

			if (slimeoid.body == ""):
				needsbody = True
				incomplete = True
			if (slimeoid.head == ""):
				needshead = True
				incomplete = True
			if (slimeoid.legs == ""):
				needslegs = True
				incomplete = True
			if (slimeoid.armor == ""):
				needsarmor = True
				incomplete = True
			if (slimeoid.weapon == ""):
				needsweapon = True
				incomplete = True
			if (slimeoid.special == ""):
				needsspecial = True
				incomplete = True
			if (slimeoid.ai == ""):
				needsbrain = True
				incomplete = True
			if (slimeoid.name == ""):
				needsname = True
				incomplete = True
			if ((slimeoid.atk + slimeoid.defense + slimeoid.intel) < (slimeoid.level)):
				needsstats = True
				incomplete = True

			if incomplete == True:
				response = "Your slimeoid is not yet ready to be spawned from the gestation vat."
				if needsbody == True:
					response += "\nIts body has not yet been given a distinct form."
				if needshead == True:
					response += "\nIt does not yet have a head."
				if needslegs == True:
					response += "\nIt has no means of locomotion."
				if needsarmor == True:
					response += "\nIt lacks any form of protection."
				if needsweapon == True:
					response += "\nIt lacks a means of attack."
				if needsspecial == True:
					response += "\nIt lacks a special ability."
				if needsbrain == True:
					response += "\nIt does not yet have a brain."
				if needsstats == True:
					response += "\nIt still has potential that must be distributed between Moxie, Grit and Chutzpah."
				if needsname == True:
					response += "\nIt needs a name."
			else:
				slimeoid.life_state = ewcfg.slimeoid_state_active
				response = "You press the big red button labelled 'SPAWN'. The console lights up and there is a rush of mechanical noise as the fluid drains rapidly out of the gestation tube. The newly born Slimeoid within writhes in confusion before being sucked down an ejection chute and spat out messily onto the laboratory floor at your feet. Happy birthday, {} the Slimeoid!! {}".format(slimeoid.name, ewcfg.emote_slimeheart)


				response += "\n\n{} is a {}-foot-tall Slimeoid.".format(slimeoid.name, str(slimeoid.level))
				response += slimeoid_describe(slimeoid)

				brain = ewcfg.brain_map.get(slimeoid.ai)
				response += "\n\n" + brain.str_spawn.format(
					slimeoid_name = slimeoid.name
				)

			user_data.persist()
			slimeoid.persist()

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

"""
	Describe the specified slimeoid. Used for the !slimeoid command and while it's being created.
"""
def slimeoid_describe(slimeoid):
	response = ""

	body = ewcfg.body_map.get(slimeoid.body)
	if body != None:
		response += " {}".format(body.str_body)

	head = ewcfg.head_map.get(slimeoid.head)
	if head != None:
		response += " {}".format(head.str_head)

	mobility = ewcfg.mobility_map.get(slimeoid.legs)
	if mobility != None:
		response += " {}".format(mobility.str_mobility)

	offense = ewcfg.offense_map.get(slimeoid.weapon)
	if offense != None:
		response += " {}".format(offense.str_offense)

	defense = ewcfg.defense_map.get(slimeoid.armor)
	if defense != None:
		response += " {}".format(defense.str_armor)

	special = ewcfg.special_map.get(slimeoid.special)
	if special != None:
		response += " {}".format(special.str_special)

	brain = ewcfg.brain_map.get(slimeoid.ai)
	if brain != None:
		response += " {}".format(brain.str_brain)

	hue = ewcfg.hue_map.get(slimeoid.hue)
	if hue != None:
		response += " {}".format(hue.str_desc)
		
	# coating = ewcfg.hue_map.get(slimeoid.coating)
	# if coating != None:
	# 	response += " {}".format(coating.str_desc)

	stat_desc = []

	stat = slimeoid.atk
	if stat == 0:
		statlevel = "almost no"
	if stat == 1:
		statlevel = "just a little bit of"
	if stat == 2:
		statlevel = "a decent amount of"
	if stat == 3:
		statlevel = "quite a bit of"
	if stat == 4:
		statlevel = "a whole lot of"
	if stat == 5:
		statlevel = "loads of"
	if stat == 6:
		statlevel = "massive amounts of"
	if stat == 7:
		statlevel = "seemingly inexhaustible stores of"
	if stat >= 8:
		statlevel = "truly godlike levels of"
	stat_desc.append("{} moxie".format(statlevel))

	stat = slimeoid.defense
	if stat == 0:
		statlevel = "almost no"
	if stat == 1:
		statlevel = "just a little bit of"
	if stat == 2:
		statlevel = "a decent amount of"
	if stat == 3:
		statlevel = "quite a bit of"
	if stat == 4:
		statlevel = "a whole lot of"
	if stat == 5:
		statlevel = "loads of"
	if stat == 6:
		statlevel = "massive amounts of"
	if stat == 7:
		statlevel = "seemingly inexhaustible stores of"
	if stat >= 8:
		statlevel = "truly godlike levels of"
	stat_desc.append("{} grit".format(statlevel))

	stat = slimeoid.intel
	if stat == 0:
		statlevel = "almost no"
	if stat == 1:
		statlevel = "just a little bit of"
	if stat == 2:
		statlevel = "a decent amount of"
	if stat == 3:
		statlevel = "quite a bit of"
	if stat == 4:
		statlevel = "a whole lot of"
	if stat == 5:
		statlevel = "loads of"
	if stat == 6:
		statlevel = "massive amounts of"
	if stat == 7:
		statlevel = "seemingly inexhaustible stores of"
	if stat >= 8:
		statlevel = "truly godlike levels of"
	stat_desc.append("{} chutzpah".format(statlevel))

	response += " It has {}.".format(ewutils.formatNiceList(names = stat_desc))

	clout = slimeoid.clout
	if slimeoid.sltype != ewcfg.sltype_nega:
		if clout >= 50:
			response += " A **LIVING LEGEND** on the arena."
		elif clout >= 30:
			response += " A **BRUTAL CHAMPION** on the arena."
		elif clout >= 15:
			response += " This slimeoid has proven itself on the arena."
		elif clout >= 1:
			response += " This slimeoid has some clout, but has not yet realized its potential."
		elif clout == 0:
			response += " A pitiable baby, this slimeoid has no clout whatsoever."

	if (int(time.time()) - slimeoid.time_defeated) < ewcfg.cd_slimeoiddefeated:
			response += " It is currently incapacitated after being defeated."

	return response

# Show a player's slimeoid data.
async def slimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	member = None
	selfcheck = True
	response = ""

	if cmd.mentions_count == 0:
		selfcheck = True
		slimeoid = EwSlimeoid(member = cmd.message.author)
	else:
		selfcheck = False
		member = cmd.mentions[0]
		user_data = EwPlayer(member = member)
		slimeoid = EwSlimeoid(member = member)

	if user_data.life_state == ewcfg.life_state_corpse:
		response = "Slimeoids don't fuck with ghosts."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
		if selfcheck == True:
			response = "You have not yet created a slimeoid."
		else:
			response = "{} has not yet created a slimeoid.".format(member.name)

	else:
		if slimeoid.life_state == ewcfg.slimeoid_state_forming:
			if selfcheck == True:
				response = "Your Slimeoid is still forming in the gestation vat. It is about {} feet from end to end.".format(str(slimeoid.level))
			else:
				response = "{}'s Slimeoid is still forming in the gestation vat. It is about {} feet from end to end.".format(member.name, str(slimeoid.level))
		elif slimeoid.life_state == ewcfg.slimeoid_state_active:
			if selfcheck == True:
				response = "You are accompanied by {}, a {}-foot-tall Slimeoid.".format(slimeoid.name, str(slimeoid.level))
			else:
				response = "{} is accompanied by {}, a {}-foot-tall Slimeoid.".format(member.name, slimeoid.name, str(slimeoid.level))

		response += slimeoid_describe(slimeoid)

		cosmetics = ewitem.inventory(
			id_user = user_data.id_user,
			id_server = cmd.guild.id,
			item_type_filter = ewcfg.it_cosmetic
		)

		# get the cosmetics worn by the slimeoid
		adorned_cosmetics = []
		for item in cosmetics:
			cos = EwItem(id_item = item.get('id_item'))
			if cos.item_props.get('slimeoid') == 'true':
				hue = ewcfg.hue_map.get(cos.item_props.get('hue'))
				adorned_cosmetics.append((hue.str_name + " colored " if hue != None else "") + cos.item_props.get('cosmetic_name'))

		if len(adorned_cosmetics) > 0:
			response += "\n\nIt has {} adorned.".format(ewutils.formatNiceList(adorned_cosmetics, "and"))

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


# Show a player's slimeoid data.
async def negaslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	response = ""

	if cmd.mentions_count > 0:
		# Can't mention any players
		response = "Negaslimeoids obey no masters. You'll have to address the beast directly."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	if cmd.tokens_count < 2:
		response = "Name the horror you wish to behold."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid_search = cmd.message.content[len(cmd.tokens[0]):].lower().strip()


	potential_slimeoids = ewutils.get_slimeoids_in_poi(id_server = cmd.guild.id, sltype = ewcfg.sltype_nega)

	negaslimeoid = None
	for id_slimeoid in potential_slimeoids:
		
		slimeoid_data = EwSlimeoid(id_slimeoid = id_slimeoid)
		name = slimeoid_data.name.lower()
		if slimeoid_search in name:
			negaslimeoid = slimeoid_data
			break

	if negaslimeoid is None:
		response = "There is no Negaslimeoid by that name."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	response = "{} is a {}-foot-tall Negaslimeoid.".format(negaslimeoid.name, negaslimeoid.level)
	response += slimeoid_describe(negaslimeoid)

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def slimeoidbattle(cmd):

	#if cmd.message.channel.name != ewcfg.channel_arena:
		#Only at the arena
	#	response = "You can only have Slimeoid Battles at the Battle Arena."
	#	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if ewutils.channel_name_is_poi(str(cmd.message.channel)) is False:
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

	if cmd.mentions_count != 1:
		#Must mention only one player
		response = "Mention the player you want to challenge."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	author = cmd.message.author
	member = cmd.mentions[0]

	if author.id == member.id:
		response = "You can't challenge yourself, dumbass."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	challenger = EwPlayer(member = author)
	challenger_slimeoid = EwSlimeoid(member = author)
	challengee = EwPlayer(member = member)
	challengee_slimeoid = EwSlimeoid(member = member)

	bet = ewutils.getIntToken(tokens=cmd.tokens, allow_all=True)

	if bet == None or challenger.poi != ewcfg.poi_id_arena:
		bet = 0
	if bet == -1:
		bet = challenger.slime

	#Players have been challenged
	if active_slimeoidbattles.get(challenger_slimeoid.id_slimeoid):
		response = "You are already in the middle of a challenge."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	if active_slimeoidbattles.get(challengee_slimeoid.id_slimeoid):
		response = "{} is already in the middle of a challenge.".format(member.name).replace("@", "\{at\}")
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	if challenger.poi != challengee.poi:
		#Challangee must be in the arena
		response = "Both players must be in the same place."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	if challenger_slimeoid.life_state != ewcfg.slimeoid_state_active:
		response = "You do not have a Slimeoid ready to battle with!"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))
	if challengee_slimeoid.life_state != ewcfg.slimeoid_state_active:
		response = "{} does not have a Slimeoid ready to battle with!".format(member.name)
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))
	
	if challenger.slime < bet:
		response = "You don't have enough slime!"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))
	if challengee.slime < bet:
		response = "They don't have enough slime!"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))	

	time_now = int(time.time())

	if (time_now - challenger_slimeoid.time_defeated) < ewcfg.cd_slimeoiddefeated:
			time_until = ewcfg.cd_slimeoiddefeated - (time_now - challenger_slimeoid.time_defeated)
			response = "Your Slimeoid is still recovering from its last defeat! It'll be ready in {} seconds.".format(int(time_until))
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	if (time_now - challengee_slimeoid.time_defeated) < ewcfg.cd_slimeoiddefeated:
			time_until = ewcfg.cd_slimeoiddefeated - (time_now - challengee_slimeoid.time_defeated)
			response = "{}'s Slimeoid is still recovering from its last defeat! It'll be ready in {} seconds.".format(member.name, time_until)
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	#Players have to be enlisted
	if challenger.life_state == ewcfg.life_state_corpse or challengee.life_state == ewcfg.life_state_corpse:
		if challenger.life_state == ewcfg.life_state_corpse:
			response = "Your Slimeoid won't battle for you while you're dead.".format(author.name).replace("@", "\{at\}")
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

		elif challengee.life_state == ewcfg.life_state_corpse:
			response = "{}'s Slimeoid won't battle for them while they're dead.".format(member.name).replace("@", "\{at\}")
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	#Assign a challenger so players can't be challenged
	challenger_slimeoid_id = challenger_slimeoid.id_slimeoid
	challengee_slimeoid_id = challengee_slimeoid.id_slimeoid
	active_slimeoidbattles[challenger_slimeoid_id] = True
	active_slimeoidbattles[challengee_slimeoid_id] = True

	ewutils.active_target_map[challengee.id_user] = challenger.id_user

	challengee.persist()

	response = "You have been challenged by {} to a Slimeoid Battle. Do you !accept or !refuse?".format(author.name).replace("@", "\{at\}")
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(member, response))

	#Wait for an answer
	accepted = 0
	try:
		msg = await cmd.client.wait_for('message', timeout = 30, check=lambda message: message.author == member and 
												message.content.lower() in [ewcfg.cmd_accept, ewcfg.cmd_refuse])

		if msg != None:
			if msg.content == ewcfg.cmd_accept:
				accepted = 1
	except:
		accepted = 0

	challengee = EwPlayer(member = member)
	challengee_slimeoid = EwSlimeoid(member = member)
	challenger = EwPlayer(member = author)
	challengee_slimeoid = EwSlimeoid(member = member)

	ewutils.active_target_map[challengee.id_user] = ""
	ewutils.active_target_map[challenger.id_user] = ""

	#challengee.persist()
	#challenger.persist()

	if challenger_slimeoid.life_state != ewcfg.slimeoid_state_active:
		active_slimeoidbattles[challenger_slimeoid_id] = False
		active_slimeoidbattles[challengee_slimeoid_id] = False
		response = "You do not have a Slimeoid ready to battle with!"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))
	if challengee_slimeoid.life_state != ewcfg.slimeoid_state_active:
		active_slimeoidbattles[challenger_slimeoid_id] = False
		active_slimeoidbattles[challengee_slimeoid_id] = False
		response = "{} does not have a Slimeoid ready to battle with!".format(member.name)
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	#Start game
	if accepted == 1:
		challengee.change_slime(n = -bet, source = ewcfg.source_slimeoid_betting)
		challenger.change_slime(n = -bet, source = ewcfg.source_slimeoid_betting)
		
		challengee.persist()
		challenger.persist()

		slimecorp_fee, winnings = ewcasino.slimecorp_collectfee(bet*2)

		result = await battle_slimeoids(id_s1 = challengee_slimeoid.id_slimeoid, id_s2 = challenger_slimeoid.id_slimeoid, channel = cmd.message.channel, battle_type = ewcfg.battle_type_arena)
		if result == -1:
			response = "\n**{} has won the Slimeoid battle!! The crowd erupts into cheers for {} and {}!!** :tada:{}".format(challenger_slimeoid.name, challenger_slimeoid.name, author.name, "" if bet == 0 else "\nThey recieve {:,} slime! The remaining {:,} slime goes to SlimeCorp.".format(winnings, slimecorp_fee))
			
			if challengee_slimeoid.coating != '':
				response += "\n{} coating has been tarnished by battle.".format(challengee_slimeoid.name, challengee_slimeoid.coating)
				challengee_slimeoid.coating = ''
				challengee_slimeoid.persist()
			if challenger_slimeoid.coating != '':
				response += "\n{} coating has been tarnished by battle.".format(challenger_slimeoid.name, challenger_slimeoid.coating)
				challenger_slimeoid.coating = ''
				challenger_slimeoid.persist()
			
			await ewutils.send_message(cmd.client, cmd.message.channel, response)
			challenger = EwPlayer(member = author)
			if challenger.life_state != ewcfg.life_state_corpse:
				challenger.change_slime(n = winnings)
				challenger.persist()
		elif result == 1:
			response = "\n**{} has won the Slimeoid battle!! The crowd erupts into cheers for {} and {}!!** :tada:{}".format(challengee_slimeoid.name, challengee_slimeoid.name, member.name, "" if bet == 0 else "\nThey recieve {:,} slime! The remaining {:,} slime goes to SlimeCorp.".format(winnings, slimecorp_fee))

			if challengee_slimeoid.coating != '':
				challengee_slimeoid.coating = ''
				response += "\n{} sheds its {} coating.".format(challengee_slimeoid.name, challengee_slimeoid.coating)
				challengee_slimeoid.persist()
			if challenger_slimeoid.coating != '':
				challenger_slimeoid.coating = ''
				response += "\n{} sheds its {} coating.".format(challenger_slimeoid.name, challenger_slimeoid.coating)
				challenger_slimeoid.persist()
			
			await ewutils.send_message(cmd.client, cmd.message.channel, response)
			challengee = EwPlayer(member = member)
			if challengee.life_state != ewcfg.life_state_corpse:
				challengee.change_slime(n = winnings)
				challengee.persist()
	else:
		response = "{} was too cowardly to accept your challenge.".format(member.name).replace("@", "\{at\}")

		# Send the response to the player.
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	active_slimeoidbattles[challenger_slimeoid_id] = False
	active_slimeoidbattles[challengee_slimeoid_id] = False

async def negaslimeoidbattle(cmd):

	if not ewutils.channel_name_is_poi(cmd.message.channel.name):
		response = "You must go into the city to challenge an eldritch abomination."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if cmd.mentions_count > 0:
		# Can't mention any players
		response = "Negaslimeoids obey no masters. You'll have to address the beast directly."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if cmd.tokens_count < 2:
		response = "Name the horror you wish to face."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid_search = cmd.message.content[len(cmd.tokens[0]):].lower().strip()

	author = cmd.message.author

	challenger = EwPlayer(member = author)
	challenger_slimeoid = EwSlimeoid(member = author)

	#Player has to be alive
	if challenger.life_state == ewcfg.life_state_corpse:
		response = "Your Slimeoid won't battle for you while you're dead.".format(author.name).replace("@", "\{at\}")
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))


	potential_challengees = ewutils.get_slimeoids_in_poi(id_server = cmd.guild.id, poi = challenger.poi, sltype = ewcfg.sltype_nega)

	challengee_slimeoid = None
	for id_slimeoid in potential_challengees:
		
		slimeoid_data = EwSlimeoid(id_slimeoid = id_slimeoid)
		name = slimeoid_data.name.lower()
		if slimeoid_search in name:
			challengee_slimeoid = slimeoid_data
			break

	if challengee_slimeoid is None:
		response = "There is no Negaslimeoid by that name here."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	#Players have been challenged
	if active_slimeoidbattles.get(challenger_slimeoid.id_slimeoid):
		response = "Your slimeoid is already in the middle of a battle."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	if active_slimeoidbattles.get(challengee_slimeoid.id_slimeoid):
		response = "{} is already in the middle of a battle.".format(challengee_slimeoid.name)
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	if challenger_slimeoid.life_state != ewcfg.slimeoid_state_active:
		response = "You do not have a Slimeoid ready to battle with!"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	time_now = int(time.time())

	if (time_now - challenger_slimeoid.time_defeated) < ewcfg.cd_slimeoiddefeated:
		response = "Your Slimeoid is still recovering from its last defeat!"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(author, response))

	#Assign a challenger so players can't be challenged
	active_slimeoidbattles[challenger_slimeoid.id_slimeoid] = True
	active_slimeoidbattles[challengee_slimeoid.id_slimeoid] = True


	#Start game
	try:
		result = await battle_slimeoids(id_s1 = challengee_slimeoid.id_slimeoid, id_s2 = challenger_slimeoid.id_slimeoid, channel = cmd.message.channel, battle_type = ewcfg.battle_type_nega)
		if result == -1:
			# Losing in a nega battle means death
			district_data = EwDistrict(district = challenger.poi, id_server = cmd.guild.id)
			slimes = int(2 * 10 ** (challengee_slimeoid.level - 2))
			district_data.change_slime(n = slimes)
			district_data.persist()
			challengee_slimeoid.delete()
			response = "The dulled colors become vibrant again, as {} fades back into its own reality.".format(challengee_slimeoid.name)
			await ewutils.send_message(cmd.client, cmd.message.channel, response)
		elif result == 1:
			# Dedorn all items
			cosmetics = ewitem.inventory(
				id_user = cmd.message.author.id,
				id_server = cmd.guild.id,
				item_type_filter = ewcfg.it_cosmetic
			)
			# get the cosmetics worn by the slimeoid
			for item in cosmetics:
				cos = EwItem(id_item = item.get('id_item'))
				if cos.item_props.get('slimeoid') == 'true':
					cos.item_props['slimeoid'] = 'false'
					cos.persist()
			# Losing in a nega battle means death
			item_props = {
				'context': ewcfg.context_slimeoidheart,
				'subcontext': challenger_slimeoid.id_slimeoid,
				'item_name': "Heart of {}".format(challenger_slimeoid.name),
				'item_desc': "A poudrin-like crystal. If you listen carefully you can hear something that sounds like a faint heartbeat."
			}
			ewitem.item_create(
				id_user = cmd.message.author.id,
				id_server = cmd.guild.id,
				item_type = ewcfg.it_item,
				item_props = item_props
			)
			challenger_slimeoid.die()
			challenger_slimeoid.persist()
			challenger = EwPlayer(member = author)
			challenger.active_slimeoid = -1
			challenger.persist()
			response = "{} feasts on {}'s slime. All that remains is a small chunk of crystallized slime.".format(challengee_slimeoid.name, challenger_slimeoid.name)
			response += "\n\n{} is no more. {}".format(challenger_slimeoid.name, ewcfg.emote_slimeskull)
			if challenger_slimeoid.level > challengee_slimeoid.level:
				challengee_slimeoid.level += 1
				rand = random.randrange(3)
				if rand == 0:
					challengee_slimeoid.atk += 1
				elif rand == 1:
					challengee_slimeoid.defense += 1
				else:
					challengee_slimeoid.intel += 1
				challengee_slimeoid.persist()
				response += "\n\n{} was empowered by the slaughter and grew a foot taller.".format(challengee_slimeoid.name)
			await ewutils.send_message(cmd.client, cmd.message.channel, response)
	except:
		ewutils.logMsg("An error occured in the Negaslimeoid battle against {}".format(challengee_slimeoid.name))
	finally:
		active_slimeoidbattles[challenger_slimeoid.id_slimeoid] = False
		active_slimeoidbattles[challengee_slimeoid.id_slimeoid] = False

# Slimeoids lose more clout for losing at higher levels.
def calculate_clout_loss(clout):
	if clout >= 100:
		clout -= 6
	elif clout >= 40:
		clout -= 5
	elif clout >= 30:
		clout -= 4
	elif clout >= 20:
		clout -= 3
	elif clout >= 10:
		clout -= 2
	elif clout >= 1:
		clout -= 1

	return clout

def calculate_clout_gain(clout):
	clout += 2

	if clout > 100:
		clout = 100

	return clout

async def saturateslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
	item_sought = ewitem.find_item(item_search = item_search, id_user = cmd.message.author.id, id_server = cmd.guild.id if cmd.guild is not None else None, item_type_filter = ewcfg.it_item)

	if user_data.life_state == ewcfg.life_state_corpse:
		response = "Slimeoids don't fuck with ghosts."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
		response = "Wow, great idea! Too bad you don’t even have a slimeoid with which to saturate! You’d think you’d remember really obvious stuff like that, but no. What a dumbass."

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
		response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."

	elif item_sought:
		value = item_search
		hue = ewcfg.hue_map.get(value)
		
		

		if hue != None:
			if hue.id_hue in [ewcfg.hue_id_copper, ewcfg.hue_id_chrome, ewcfg.hue_id_gold]:
				response = "You saturate your {} with the {} paint! {}".format(slimeoid.name, hue.str_name, hue.str_saturate)
				slimeoid.hue = hue.id_hue
				slimeoid.coating = hue.id_hue
				slimeoid.persist()
				
				paint_bucket_item = EwItem(id_item=item_sought.get('id_item'))
				if int(paint_bucket_item.item_props.get('durability')) <= 1:
					ewitem.item_delete(id_item=item_sought.get('id_item'))
					response += "\nThe paint bucket is consumed in the process."
				else:
					await ewitem.lower_durability(item_sought)
				user_data.persist()
			else:
				response = "You saturate your {} with the {} dye! {}".format(slimeoid.name, hue.str_name, hue.str_saturate)
				slimeoid.hue = hue.id_hue
				slimeoid.persist()
	
				ewitem.item_delete(id_item = item_sought.get('id_item'))
				user_data.persist()

		else:
			response = "You can only saturate your slimeoid with dyes and paints."

	else:
		if item_search:  # if they didn't forget to specify an item and it just wasn't found
			response = "You can only saturate your slimeoid with dyes and paints."
		else:
			response = "Saturate your slimeoid with what, exactly? (check **!inventory**)"

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def restoreslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(member = cmd.message.author)
	item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
	item_sought = ewitem.find_item(item_search = item_search, id_user = cmd.message.author.id, id_server = cmd.guild.id if cmd.guild is not None else None)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "You must go to the SlimeCorp Laboratories in Brawlden to restore a Slimeoid."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	poi = ewcfg.id_to_poi.get(user_data.poi)
	district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

	if district_data.is_degraded():
		response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if user_data.life_state == ewcfg.life_state_corpse:
		response = "Ghosts cannot interact with the SlimeCorp Lab apparati."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if slimeoid.life_state != ewcfg.slimeoid_state_none:
		response = "You already have an active slimeoid."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	
	if item_sought is None:
		if item_search:
			response = "You need a slimeoid's heart to restore it to life."
		else:
			response = "Restore which slimeoid?"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	item_data = ewitem.EwItem(id_item = item_sought.get('id_item'))

	if item_data.item_props.get('context') != ewcfg.context_slimeoidheart:
		response = "You need a slimeoid's heart to restore it to life."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid = EwSlimeoid(id_slimeoid = item_data.item_props.get('subcontext'))
	slimes_to_restore = 2 * 10 ** (slimeoid.level - 2) # 1/5 of the original cost

	if user_data.slime < slimes_to_restore:
		response = "You need at least {} slime to restore this slimeoid.".format(slimes_to_restore)
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		

	slimeoid.life_state = ewcfg.slimeoid_state_active
	slimeoid.id_user = str(user_data.id_user)
	slimeoid.persist()

	ewitem.item_delete(id_item = item_data.id_item)

	user_data.change_slime(n = -slimes_to_restore, source = ewcfg.source_spending)
	user_data.persist()

	response = "You insert the heart of your beloved {} into one of the restoration tanks. A series of clattering sensors analyze the crystalline core. Then, just like when it was first incubated, the needle pricks you and extracts slime from your body, which coalesces around the poudrin-like heart. Bit by bit the formless mass starts to assume a familiar shape.\n\n{} has been restored to its former glory!".format(slimeoid.name, slimeoid.name)
	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
			
		


async def battle_slimeoids(id_s1, id_s2, channel, battle_type):

	# fetch slimeoid data
	challengee_slimeoid = EwSlimeoid(id_slimeoid = id_s1)
	challenger_slimeoid = EwSlimeoid(id_slimeoid = id_s2)

	# fetch player data
	challengee = EwDiscordUser(id_user = int(challengee_slimeoid.id_user))
	challenger = EwDiscordUser(id_user = int(challenger_slimeoid.id_user))

	client = ewutils.get_client()
	
	# calculate starting hp
	s1hpmax = 50 + (challengee_slimeoid.level * 20)
	s2hpmax = 50 + (challenger_slimeoid.level * 20)

	# calculate starting sap
	s1sapmax = challengee_slimeoid.level * 2
	s2sapmax = challenger_slimeoid.level * 2

	# initialize combat data for challengee
	s1_combat_data = EwSlimeoidCombatData(
		name = str(challengee_slimeoid.name),
		weapon = ewcfg.offense_map.get(challengee_slimeoid.weapon),
		armor = ewcfg.defense_map.get(challengee_slimeoid.armor),
		special = ewcfg.special_map.get(challengee_slimeoid.special),
		legs = ewcfg.mobility_map.get(challengee_slimeoid.legs),
		brain = ewcfg.brain_map.get(challengee_slimeoid.ai),
		hue = ewcfg.hue_map.get(challengee_slimeoid.hue),
		coating = challengee_slimeoid.coating,
		moxie = challengee_slimeoid.atk + 1,
		grit = challengee_slimeoid.defense + 1,
		chutzpah = challengee_slimeoid.intel + 1,
		hpmax = s1hpmax,
		hp = s1hpmax,
		sapmax = s1sapmax,
		sap = s1sapmax,
		slimeoid = challengee_slimeoid,
		owner = challengee,
	)

	# initialize combat data for challenger
	s2_combat_data = EwSlimeoidCombatData(
		name = str(challenger_slimeoid.name),
		weapon = ewcfg.offense_map.get(challenger_slimeoid.weapon),
		armor = ewcfg.defense_map.get(challenger_slimeoid.armor),
		special = ewcfg.special_map.get(challenger_slimeoid.special),
		legs = ewcfg.mobility_map.get(challenger_slimeoid.legs),
		brain = ewcfg.brain_map.get(challenger_slimeoid.ai),
		hue = ewcfg.hue_map.get(challenger_slimeoid.hue),
		coating = challenger_slimeoid.coating,
		moxie = challenger_slimeoid.atk + 1,
		grit = challenger_slimeoid.defense + 1,
		chutzpah = challenger_slimeoid.intel + 1,
		hpmax = s2hpmax,
		hp = s2hpmax,
		sapmax = s2sapmax,
		sap = s2sapmax,
		slimeoid = challenger_slimeoid,
		owner = challenger,
	)

	s1_combat_data.apply_weapon_matchup(s2_combat_data)
	s2_combat_data.apply_weapon_matchup(s1_combat_data)

	s1_combat_data.apply_hue_matchup(s2_combat_data)
	s2_combat_data.apply_hue_matchup(s1_combat_data)

	# decide which slimeoid gets to move first
	s1_active = False
	in_range = False

	if challengee_slimeoid.defense > challenger_slimeoid.defense:
		s1_active = True
	elif challengee_slimeoid.defense == challenger_slimeoid.defense:
		coinflip = random.randrange(1,3)
		if coinflip == 1:
			s1_active = True

	# flavor text for arena battles
	if battle_type == ewcfg.battle_type_arena:
		response = "**{} sends {} out into the Battle Arena!**".format(challenger.name, s2_combat_data.name)
		await ewutils.send_message(client, channel, response)
		await asyncio.sleep(1)
		response = "**{} sends {} out into the Battle Arena!**".format(challengee.name, s1_combat_data.name)
		await ewutils.send_message(client, channel, response)
		await asyncio.sleep(1)
		response = "\nThe crowd erupts into cheers! The battle between {} and {} has begun! :crossed_swords:".format(s1_combat_data.name, s2_combat_data.name)
#		response += "\n{} {} {} {} {} {}".format(str(s1moxie),str(s1grit),str(s1chutzpah),str(challengee_slimeoid.weapon),str(challengee_slimeoid.armor),str(challengee_slimeoid.special))
#		response += "\n{} {} {} {} {} {}".format(str(s2moxie),str(s2grit),str(s2chutzpah),str(challenger_slimeoid.weapon),str(challenger_slimeoid.armor),str(challenger_slimeoid.special))
#		response += "\n{}, {}".format(str(challengee_resistance),str(challengee_weakness))
#		response += "\n{}, {}".format(str(challenger_resistance),str(challenger_weakness))
		await ewutils.send_message(client, channel, response)
		await asyncio.sleep(3)


	turncounter = 100
	# combat loop
	while s1_combat_data.hp > 0 and s2_combat_data.hp > 0 and turncounter > 0:
		# Limit the number of turns in battle.
		turncounter -= 1

		response = ""
		battlecry = random.randrange(1,4)

		first_turn = (turncounter % 2) == 1

		# slimeoids regenerate their sap every odd turn
		if first_turn:
			s1_combat_data.sap = s1_combat_data.sapmax - s1_combat_data.hardened_sap
			s2_combat_data.sap = s2_combat_data.sapmax - s2_combat_data.hardened_sap
	
		# assign active and passive role for the turn
		if s1_active:
			active_data = s1_combat_data
			passive_data = s2_combat_data
		else:
			active_data = s2_combat_data
			passive_data = s1_combat_data

		# obtain action and how much sap to spend on it for both slimeoids
		active_strat, active_sap_spend = active_data.brain.get_strat(combat_data = active_data, active = True, in_range = in_range, first_turn = first_turn)
		passive_strat, passive_sap_spend = passive_data.brain.get_strat(combat_data = passive_data, active = False, in_range = in_range, first_turn = first_turn)

		#potentially add brain-based flavor text
		if active_strat == ewcfg.slimeoid_strat_attack and battlecry == 1:
			if (active_data.hpmax/active_data.hp) > 3:
				response = active_data.brain.str_battlecry_weak.format(
					slimeoid_name=active_data.name
				)
			else:
				response = active_data.brain.str_battlecry.format(
					slimeoid_name=active_data.name
				)
			await ewutils.send_message(client, channel, response)
			await asyncio.sleep(1)

		elif active_strat == ewcfg.slimeoid_strat_evade and battlecry == 1:
			if (active_data.hpmax/active_data.hp) > 3:
				response = active_data.brain.str_movecry_weak.format(
					slimeoid_name=active_data.name
				)
			else:
				response = active_data.brain.str_movecry.format(
					slimeoid_name=active_data.name
				)
			await ewutils.send_message(client, channel, response)
			await asyncio.sleep(1)

		# announce active slimeoid's chosen action
		response = ""
		if active_strat == ewcfg.slimeoid_strat_attack:
			if in_range:
				response = "{} attempts to strike {} in close combat!".format(active_data.name, passive_data.name)
			else:
				response = "{} attempts to strike {} from a distance!".format(active_data.name, passive_data.name)

		elif active_strat == ewcfg.slimeoid_strat_evade:
			if in_range:
				response = "{} attempts to avoid being hit, while gaining distance from {}.".format(active_data.name, passive_data.name)
			else:
				response = "{} attempts to avoid being hit, while closing the distance to {}.".format(active_data.name, passive_data.name)

		elif active_strat == ewcfg.slimeoid_strat_block:
			response = "{} focuses on blocking incoming attacks.".format(active_data.name)

		response += " (**{} sap**)".format(active_sap_spend)

		await ewutils.send_message(client, channel, response)
		await asyncio.sleep(1)


		# announce passive slimeoid's chosen action
		response = ""
		if passive_strat == ewcfg.slimeoid_strat_attack:
			if in_range:
				response = "{} attempts to strike {} in close combat!".format(passive_data.name, active_data.name)
			else:
				response = "{} attempts to strike {} from a distance!".format(passive_data.name, active_data.name)

		elif passive_strat == ewcfg.slimeoid_strat_evade:
			if in_range:
				response = "{} attempts to avoid being hit, while gaining distance from {}.".format(passive_data.name, active_data.name)
			else:
				response = "{} attempts to avoid being hit, while closing the distance to {}.".format(passive_data.name, active_data.name)

		elif passive_strat == ewcfg.slimeoid_strat_block:
			response = "{} focuses on blocking incoming attacks.".format(passive_data.name)

		response += " (**{} sap**)".format(passive_sap_spend)

		await ewutils.send_message(client, channel, response)
		await asyncio.sleep(1)


		# if the chosen actions are in direct competition, the roll is opposed. only one of them can succeed
		# otherwise both actions are resolved separately
		roll_opposed = False

		if active_strat == ewcfg.slimeoid_strat_attack:
			roll_opposed = passive_strat in [ewcfg.slimeoid_strat_evade, ewcfg.slimeoid_strat_block]
		elif active_strat == ewcfg.slimeoid_strat_evade:
			roll_opposed = passive_strat in [ewcfg.slimeoid_strat_attack, ewcfg.slimeoid_strat_evade]
		elif active_strat == ewcfg.slimeoid_strat_block:
			roll_opposed = passive_strat in [ewcfg.slimeoid_strat_attack]

		active_dos = active_data.attempt_action(strat = active_strat, sap_spend = active_sap_spend, in_range = in_range)

		# simultaneous attacks are a special case. the passive slimeoid only rolls the dice, after the active slimeoid's attack has been resolved
		if passive_strat != ewcfg.slimeoid_strat_attack:
			passive_dos = passive_data.attempt_action(strat = passive_strat, sap_spend = passive_sap_spend, in_range = in_range)
			if roll_opposed:
				active_dos -= passive_dos
				passive_dos = -active_dos

				# on an opposed roll, priority for the next turn (the active role) is passed to the winner of the roll
				if active_dos < 0:
					s1_active = not s1_active
		else:
			passive_dos = 0

				

		# resolve active slimeoid's attack
		if active_strat == ewcfg.slimeoid_strat_attack:
			# the attack was successful
			if active_dos > 0:
				# calculate damage
				if in_range:
					damage = int(active_dos * 30 / (passive_data.hardened_sap + 1))
				else:
					damage = int(active_dos * 20)

				response = active_data.execute_attack(passive_data, damage, in_range)
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)

				response = passive_data.take_damage(active_data, damage, active_dos, in_range)
				if len(response) > 0:
					await ewutils.send_message(client, channel, response)
					await asyncio.sleep(1)
		
			elif not roll_opposed:
				response = "{} whiffs its attack!".format(active_data.name)
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)
			elif passive_strat == ewcfg.slimeoid_strat_evade:
				response = "{} dodges {}'s attack!".format(passive_data.name, active_data.name)
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)
			elif passive_strat == ewcfg.slimeoid_strat_block:
				response = "{} blocks {}'s attack!".format(passive_data.name, active_data.name)
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)

		# if the active slimeoid's attack killed the passive slimeoid
		if passive_data.hp <= 0:
			break

		if passive_strat == ewcfg.slimeoid_strat_attack:
			passive_dos = passive_data.attempt_action(strat = passive_strat, sap_spend = passive_sap_spend, in_range = in_range)

			if roll_opposed:
				active_dos -= passive_dos
				passive_dos = -active_dos

				if active_dos < 0:
					s1_active = not s1_active
		
		# resolve passive slimeoid's attack		
		if passive_strat == ewcfg.slimeoid_strat_attack:
			# attack was successful
			if passive_dos > 0:
				# calculate damage
				if in_range:
					damage = int(passive_dos * 30 / (active_data.hardened_sap + 1))
				else:
					damage = int(passive_dos * 20)

				response = passive_data.execute_attack(active_data, damage, in_range)
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)

				response = active_data.take_damage(passive_data, damage, passive_dos, in_range)
				if len(response) > 0:
					await ewutils.send_message(client, channel, response)
					await asyncio.sleep(1)
		
			elif not roll_opposed:
				response = "{} whiffs its attack!".format(passive_data.name)
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)
			elif active_strat == ewcfg.slimeoid_strat_evade:
				response = "{} dodges {}'s attack!".format(active_data.name, passive_data.name)
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)
			elif active_strat == ewcfg.slimeoid_strat_block:
				response = "{} blocks {}'s attack!".format(active_data.name, passive_data.name)
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)
		
		# resolve active slimeoid's movement
		if active_strat == ewcfg.slimeoid_strat_evade:
			if active_dos > 0:
				response = active_data.change_distance(passive_data, in_range)
				in_range = not in_range
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)
			elif active_dos == 0 and passive_strat == ewcfg.slimeoid_strat_evade:
				in_range = not in_range
				response = "{} and {} circle each other, looking for an opening...".format(active_data.name, passive_data.name)
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)
		
		# resolve active slimeoid's defense
		if active_strat == ewcfg.slimeoid_strat_block:
			if active_dos > 0:
				response = active_data.harden_sap(active_dos)
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)

		# resolve passive slimeoid's movement
		if passive_strat == ewcfg.slimeoid_strat_evade:
			if passive_dos > 0:
				response = passive_data.change_distance(active_data, in_range)
				in_range = not in_range
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)

		# resolve passive slimeoid's defense
		if passive_strat == ewcfg.slimeoid_strat_block:
			if passive_dos > 0:
				response = passive_data.harden_sap(passive_dos)
				await ewutils.send_message(client, channel, response)
				await asyncio.sleep(1)


		# re-fetch slimeoid data
		challenger_slimeoid = EwSlimeoid(id_slimeoid = id_s2)
		challengee_slimeoid = EwSlimeoid(id_slimeoid = id_s1)

		s1_combat_data.slimeoid = challengee_slimeoid
		s2_combat_data.slimeoid = challenger_slimeoid

		# Check if slimeoids have died during the fight
		if challenger_slimeoid.life_state == ewcfg.slimeoid_state_dead:
			s2_combat_data.hp = 0
		elif challengee_slimeoid.life_state == ewcfg.slimeoid_state_dead:
			s1_combat_data.hp = 0

		await asyncio.sleep(2)

	# the challengee has lost
	if s1_combat_data.hp <= 0:
		result = -1
		response = "\n" + s1_combat_data.legs.str_defeat.format(
			slimeoid_name=s1_combat_data.name
		)
		response += " {}".format(ewcfg.emote_slimeskull)
		response += "\n" + s2_combat_data.brain.str_victory.format(
			slimeoid_name=s2_combat_data.name
		)

		challenger_slimeoid = EwSlimeoid(id_slimeoid = id_s2)
		challengee_slimeoid = EwSlimeoid(id_slimeoid = id_s1)

		# Losing slimeoid loses clout and has a time_defeated cooldown.
		if channel.name == ewcfg.channel_arena:
			challengee_slimeoid.clout = calculate_clout_loss(challengee_slimeoid.clout)
			challengee_slimeoid.time_defeated = int(time.time())
			challengee_slimeoid.persist()
		
		if channel.name == ewcfg.channel_arena:
			challenger_slimeoid.clout = calculate_clout_gain(challenger_slimeoid.clout)
			challenger_slimeoid.persist()

		await ewutils.send_message(client, channel, response)
		await asyncio.sleep(2)
	# the challenger has lost
	else:
		result = 1
		response = "\n" + s2_combat_data.legs.str_defeat.format(
			slimeoid_name=s2_combat_data.name
		)
		response += " {}".format(ewcfg.emote_slimeskull)
		response += "\n" + s1_combat_data.brain.str_victory.format(
			slimeoid_name=s1_combat_data.name
		)

		challenger_slimeoid = EwSlimeoid(id_slimeoid = id_s2)
		challengee_slimeoid = EwSlimeoid(id_slimeoid = id_s1)
	
		# store defeated slimeoid's defeat time in the database
		if channel.name == ewcfg.channel_arena:
			challenger_slimeoid.clout = calculate_clout_loss(challenger_slimeoid.clout)
			challenger_slimeoid.time_defeated = int(time.time())
			challenger_slimeoid.persist()
		
		if channel.name == ewcfg.channel_arena:
			challengee_slimeoid.clout = calculate_clout_gain(challengee_slimeoid.clout)
			challengee_slimeoid.persist()

		await ewutils.send_message(client, channel, response)
		await asyncio.sleep(2)
	return result

async def slimeoid_tick_loop(id_server):
	while not ewutils.TERMINATE:
		await asyncio.sleep(ewcfg.slimeoid_tick_length)
		await slimeoid_tick(id_server)

async def slimeoid_tick(id_server):
	data = ewutils.execute_sql_query("SELECT {id_slimeoid} FROM slimeoids WHERE {sltype} = %s AND {id_server} = %s".format(
		id_slimeoid = ewcfg.col_id_slimeoid,
		sltype = ewcfg.col_type,
		id_server = ewcfg.col_id_server
	),(
		ewcfg.sltype_nega,
		id_server
	))

	resp_cont = ewutils.EwResponse(id_server = id_server)
	for row in data:
		slimeoid_data = EwSlimeoid(id_slimeoid = row[0])
		haunt_resp = slimeoid_data.haunt()
		resp_cont.add_response_container(haunt_resp)
		if random.random() < 0.1:
			move_resp = slimeoid_data.move()
			resp_cont.add_response_container(move_resp)
		slimeoid_data.persist()

	await resp_cont.post()

async def bottleslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if user_data.life_state == ewcfg.life_state_corpse:
		response = "Slimeoids don't fuck with ghosts."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
		response = "You do not have a Slimeoid to bottle."

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
		response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."

	elif active_slimeoidbattles.get(slimeoid.id_slimeoid):
		response = "You can't do that right now."

	else:
		items = ewitem.inventory(id_user = user_data.id_user, id_server = user_data.id_server, item_type_filter = ewcfg.it_item)

		bottles = []
		for item in items:
			item_data = EwItem(id_item = item.get('id_item'))
			if item_data.item_props.get('context') == ewcfg.context_slimeoidbottle:
				bottles.append(item_data)

		if len(bottles) >= 2:
			response = "You can't carry any more slimeoid bottles."

		else:
			slimeoid.life_state = ewcfg.slimeoid_state_stored
			slimeoid.id_user = ""

			user_data.active_slimeoid = -1
		
			slimeoid.persist()
			user_data.persist()

			item_props = {
				'context': ewcfg.context_slimeoidbottle,
				'subcontext': slimeoid.id_slimeoid,
				'item_name': "Bottle containing {}".format(slimeoid.name),
				'item_desc': "A slimeoid bottle."
			}
			ewitem.item_create(
				id_user = cmd.message.author.id,
				id_server = cmd.guild.id,
				item_type = ewcfg.it_item,
				item_props = item_props
			)

			response = "You shove {} into a random bottle. It's a tight squeeze, but in the end you manage to make it fit.".format(slimeoid.name)

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def dress_slimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if user_data.life_state == ewcfg.life_state_corpse:
		response = "Slimeoids don't fuck with ghosts."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
		response = "You'll have to create a Slimeoid if you want to play dress up."

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
		response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."
	
	elif slimeoid.life_state != ewcfg.slimeoid_state_active:
		response = "You don't have a Slimeoid with you."

	else:
		item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
		
		try:
			item_id_int = int(item_search)
		except:
			item_id_int = None
		
		if item_search != None and len(item_search) > 0:

			cosmetics = ewitem.inventory(
				id_user = cmd.message.author.id,
				id_server = cmd.guild.id,
				item_type_filter = ewcfg.it_cosmetic
			)

			item_sought = None
			already_adorned = False
			item_from_user = None
			for item in cosmetics:
				if item.get('id_item') == item_id_int or item_search in ewutils.flattenTokenListToString(item.get('name')):
					cos = EwItem(item.get('id_item'))
					if item_from_user == None and cos.item_props.get('adorned') == 'true':
						item_from_user = cos
						continue

					if cos.item_props.get('slimeoid') == 'true':
						already_adorned = True
					elif cos.item_props.get("context") == 'costume':
						if not ewutils.check_fursuit_active(cos.id_server):
							response = "You can't dress your slimeoid with your costume right now."
							return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
						else:
							item_sought = cos
							break
					else:
						item_sought = cos
						break

			if item_sought == None:
				item_sought = item_from_user

			if item_sought != None:
				# get the cosmetics worn by the slimeoid
				adorned_cosmetics = []
				for item in cosmetics:
					cos = EwItem(id_item = item.get('id_item'))
					if cos.item_props.get('slimeoid') == 'true':
						adorned_cosmetics.append(cos)

				if len(adorned_cosmetics) < slimeoid.level:
					# Remove hat from player if adorned
					if item_sought.item_props.get('adorned') == 'true':
						item_sought.item_props['adorned'] = 'false'

						response = "You take off your {} and give it to {}.".format(item_sought.item_props.get('cosmetic_name'), slimeoid.name)
					else:
						response = "You give {} a {}.".format(slimeoid.name, item_sought.item_props.get('cosmetic_name'))
					
					item_sought.item_props['slimeoid'] = 'true'
					item_sought.persist()
					user_data.persist()
				else:
					response = 'Your slimeoid is too small to wear any more clothes.'
			elif already_adorned:
				response = "Your slimeoid is already wearing it."
			else:
				response = 'You don\'t have one.'
		else:
			response = 'Adorn which cosmetic? Check your **!inventory**.'
		
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def undress_slimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)

	if user_data.life_state == ewcfg.life_state_corpse:
		response = "Slimeoids don't fuck with ghosts."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
		response = "You'll have to create a Slimeoid if you want to play dress up."

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
		response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."

	elif slimeoid.life_state != ewcfg.slimeoid_state_active:
		response = "You don't have a Slimeoid with you."

	elif active_slimeoidbattles.get(slimeoid.id_slimeoid):
		response = "You can't do that right now."

	else:
		item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])

		try:
			item_id_int = int(item_search)
		except:
			item_id_int = None

		if item_search != None and len(item_search) > 0:

			cosmetics = ewitem.inventory(
				id_user = cmd.message.author.id,
				id_server = cmd.guild.id,
				item_type_filter = ewcfg.it_cosmetic
			)

			item_sought = None
			for item in cosmetics:
				if item.get('id_item') == item_id_int or item_search in ewutils.flattenTokenListToString(item.get('name')):
					cos = EwItem(item.get('id_item'))
					if cos.item_props.get('slimeoid') == 'true':
						item_sought = cos
						break

			if item_sought != None:

				response = "You take the {} back from {}".format(item_sought.item_props.get('cosmetic_name'), slimeoid.name)
				item_sought.item_props['slimeoid'] = 'false'

				item_sought.persist()
			else:
				response = 'You don\'t have one.'
		else:
			response = 'Dedorn which cosmetic? Check your **!inventory**.'
		
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def unbottleslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	response = ""

	if user_data.life_state == ewcfg.life_state_corpse:
		response = "Slimeoids don't fuck with ghosts."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if cmd.tokens_count < 2:
		response = "Specify which Slimeoid you want to unbottle."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeoid_search = cmd.message.content[len(cmd.tokens[0]):].lower().strip()


	items = ewitem.inventory(id_user = user_data.id_user, id_server = user_data.id_server, item_type_filter = ewcfg.it_item)

	bottles = []
	for item in items:
		item_data = EwItem(id_item = item.get('id_item'))
		if item_data.item_props.get('context') == ewcfg.context_slimeoidbottle:
			bottles.append(item_data)

	slimeoid = None
	bottle_data = None
	for bottle in bottles:
		slimeoid_data = EwSlimeoid(id_slimeoid = bottle.item_props.get('subcontext'))
		name = slimeoid_data.name.lower()
		if slimeoid_search in name or bottle.id_item == slimeoid_search:
			slimeoid = slimeoid_data
			bottle_data = bottle
			break

	if slimeoid is None:
		response = "You aren't carrying a bottle containing that Slimeoid."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	active_slimeoid = EwSlimeoid(member= cmd.message.author)

	if active_slimeoid.life_state == ewcfg.slimeoid_state_active:

		active_slimeoid.life_state = ewcfg.slimeoid_state_stored
		active_slimeoid.id_user = ""

		user_data.active_slimeoid = -1
		
		active_slimeoid.persist()
		user_data.persist()

		item_props = {
			'context': ewcfg.context_slimeoidbottle,
			'subcontext': active_slimeoid.id_slimeoid,
			'item_name': "Bottle containing {}".format(active_slimeoid.name),
			'item_desc': "A slimeoid bottle."
		}
		ewitem.item_create(
			id_user = cmd.message.author.id,
			id_server = cmd.guild.id,
			item_type = ewcfg.it_item,
			item_props = item_props
		)
		response += "You shove {} into a random bottle. It's a tight squeeze, but in the end you manage to make it fit.\n\n".format(active_slimeoid.name)

	slimeoid.life_state = ewcfg.slimeoid_state_active
	slimeoid.id_user = str(user_data.id_user)

	slimeoid.persist()

	user_data.active_slimeoid = slimeoid.id_slimeoid
	user_data.persist()

	ewitem.item_delete(id_item = bottle_data.id_item)

	response += "You crack open a fresh bottle of Slimeoid. After a bit of shaking {} sits beside you again, fully formed.".format(slimeoid.name)
	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


async def feedslimeoid(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	slimeoid = EwSlimeoid(member = cmd.message.author)
	time_now = int(time.time())
	response = ""

	if user_data.life_state == ewcfg.life_state_corpse:
		response = "Slimeoids don't fuck with ghosts."

	elif slimeoid.life_state == ewcfg.slimeoid_state_none:
		response = "You do not have a Slimeoid to feed."

	elif slimeoid.life_state == ewcfg.slimeoid_state_forming:
		response = "Your Slimeoid is not yet ready. Use !spawnslimeoid to complete incubation."

	elif cmd.tokens_count < 2:
		response = "Specify which item you want to feed to your slimeoid."
	else:
		item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])

		item_sought = ewitem.find_item(item_search = item_search, id_user = user_data.id_user, id_server = user_data.id_server)

		if item_sought:
			item_data = EwItem(id_item = item_sought.get('id_item'))
			if item_data.item_type == ewcfg.it_item and item_data.item_props.get('context') == ewcfg.context_slimeoidfood:
				feed_success = slimeoid.eat(item_data)
				if feed_success:
					slimeoid.persist()
					ewitem.item_delete(id_item = item_data.id_item)
					response = "{slimeoid_name} eats the {food_name}."
					slimeoid_brain = ewcfg.brain_map.get(slimeoid.ai)
					slimeoid_head = ewcfg.head_map.get(slimeoid.head)
					if slimeoid_brain != None and slimeoid_head != None:
						response = "{} {}".format(slimeoid_brain.str_feed, slimeoid_head.str_feed)
				else:
					response = "{slimeoid_name} refuses to eat the {food_name}."

				response = response.format(slimeoid_name = slimeoid.name, food_name = item_sought.get('name'))
			else:
				response = "That item is not suitable for slimeoid consumption."
			
		else:
			response = "You don't have an item like that."

	# Send the response to the player.
	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


def get_slimeoid_count(user_id = None, server_id = None):
	if user_id != None and server_id != None:
		count = 0
		slimeoid_data = EwSlimeoid(id_user=user_id, id_server=server_id)
		secondary_user = str(user_id) + "freeze"
		name_list = []
		if slimeoid_data.name != "":
			count += 1

		items = ewitem.inventory(id_user = user_id, id_server = server_id, item_type_filter = ewcfg.it_item)

		bottles = []
		for item in items:
			item_data = EwItem(id_item = item.get('id_item'))
			if item_data.item_props.get('context') == ewcfg.context_slimeoidbottle:
				count += 1
		
		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

			sql = "SELECT {} FROM slimeoids WHERE {} = %s"
			cursor.execute(sql.format(ewcfg.col_name, ewcfg.col_id_user), [secondary_user])

			count += cursor.rowcount
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)
			return count

def get_slimeoid_look_string(user_id = None, server_id = None):
	if user_id != None and server_id != None:
		finalString = ""
		slimeoid_data = EwSlimeoid(id_user=user_id, id_server=server_id)

		if slimeoid_data:

			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor()

				sql = "SELECT {} FROM slimeoids WHERE {} = %s"
				cursor.execute(sql.format(ewcfg.col_name, ewcfg.col_id_user), [user_id])
				if cursor.rowcount > 0:
					iterate = 0
					finalString += "\n\nIn the freezer, you hear "
					for sloid in cursor:
						if iterate > 0:
							finalString += ", "
						if iterate >= cursor.rowcount - 1 and cursor.rowcount > 1:
							finalString += "and "
						finalString += sloid[0]
						iterate+=1
					finalString += " cooing to themselves."


			finally:
				# Clean up the database handles.
				cursor.close()
				ewutils.databaseClose(conn_info)

				return finalString


def find_slimeoid(slimeoid_search=None, id_user=None, id_server=None):
	slimeoid_sought = None

	# search for an ID instead of a name
	slimeoid_list = []
	try:
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

		cursor.execute( "SELECT {} FROM slimeoids WHERE {} = %s AND {} = %s".format(
			ewcfg.col_name,
			ewcfg.col_id_user,
			ewcfg.col_id_server
		), (
			id_user,
			id_server))
		#print (sql)

		slimeoid_sought = None
		for row in cursor:
			slimeoid_name = row[0]
			slimeboy = EwSlimeoid(slimeoid_name=slimeoid_name, id_server=id_server, id_user=id_user)
			if ewutils.flattenTokenListToString(slimeoid_search) in ewutils.flattenTokenListToString(slimeboy.name):
				slimeoid_sought = slimeboy.id_slimeoid
				break
				
	finally:
		cursor.close()
		ewutils.databaseClose(conn_info)

	return slimeoid_sought
