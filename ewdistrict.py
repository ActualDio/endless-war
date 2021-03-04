import asyncio
import math
import time

import discord

import ewcfg
import ewstats
import ewutils
import ewrolemgr

from ew import EwPlayer

"""
	Informs the player about their current zone's capture progress
"""
async def capture_progress(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	response = ""

	poi = ewcfg.id_to_poi.get(user_data.poi)
	response += "**{}**: ".format(poi.str_name)

	if not user_data.poi in ewcfg.capturable_districts:
		response += "This zone cannot be captured."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	district_data = EwDistrict(id_server=user_data.id_server, district=user_data.poi)

	if district_data.controlling_faction != "":
		response += "{} control this district. ".format(district_data.controlling_faction.capitalize())
	elif district_data.capturing_faction != "" and district_data.cap_side != district_data.capturing_faction:
		response += "{} are de-capturing this district. ".format(district_data.capturing_faction.capitalize())
	elif district_data.capturing_faction != "":
		response += "{} are capturing this district. ".format(district_data.capturing_faction.capitalize())
	else:
		response += "Nobody has staked a claim to this district yet."

	response += "\n\n**Current influence: {:,}**\nMinimum influence: {:,}\nMaximum influence: {:,}\nPercentage to maximum influence: {:,}%".format(abs(district_data.capture_points), int(ewcfg.min_influence[district_data.property_class]), int(ewcfg.limit_influence[district_data.property_class]), round((abs(district_data.capture_points) * 100/(ewcfg.limit_influence[district_data.property_class])), 1))


	#if district_data.time_unlock > 0:


		#response += "\nThis district cannot be captured currently. It will unlock in {}.".format(ewutils.formatNiceTime(seconds = district_data.time_unlock, round_to_minutes = True))
	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


"""async def annex(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	response = ""
	resp_cont = ewutils.EwResponse(id_server = cmd.guild.id)
	time_now = int(time.time())

	poi = ewcfg.id_to_poi.get(user_data.poi)

	if user_data.life_state == ewcfg.life_state_corpse:
		response = "You ineffectively try shaking your can of spraypaint to whip up some sick graffiti. Alas, you’re all outta slime. " \
                   "They should really make these things compatible with ectoplasm."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if not (len(user_data.faction) > 0 and user_data.life_state == ewcfg.life_state_enlisted):
		response = "Juveniles are too chickenshit to make graffiti and risk getting busted by the cops. Fuckin’ losers."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if user_data.poi in [ewcfg.poi_id_rowdyroughhouse, ewcfg.poi_id_copkilltown]:
		response = "There’s no point, the rest of your gang has already covered this place in spraypaint. Focus on exporting your graffiti instead."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if user_data.poi == ewcfg.poi_id_juviesrow:
		response = "Nah, the Rowdys and Killers have both agreed this is neutral ground. You don’t want to start a diplomatic crisis, " \
                   "just stick to spraying down sick graffiti and splattering your rival gang across the pavement in the other districts."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if not user_data.poi in ewcfg.capturable_districts:
		response = "This zone cannot be captured."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	district_data = EwDistrict(id_server = user_data.id_server, district = user_data.poi)


	if district_data.is_degraded():
		response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	if district_data.time_unlock > 0:
		response = "You can’t spray graffiti here yet, it’s too soon after your rival gang extended their own cultural dominance over it. Try again in {}.".format(ewutils.formatNiceTime(seconds = district_data.time_unlock, round_to_minutes = True))
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if district_data.all_neighbors_friendly():
		response = "What the hell are you doing, dude? You can’t put down any graffiti here, it’s been completely overrun by your rival gang. " \
                   "You can only spray districts that have at least one unfriendly neighbor, duh!"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	
	users_in_district = district_data.get_players_in_district(
		life_states = [ewcfg.life_state_enlisted],
		ignore_offline = True,
		pvp_only = True
	)

	allies_in_district = district_data.get_players_in_district(
		factions = [user_data.faction],
		life_states = [ewcfg.life_state_enlisted],
		ignore_offline = True,
		pvp_only = True
	)

	if len(users_in_district) > len(allies_in_district):
		response = "Holy shit, deal with your rival gangsters first! You can’t spray graffiti while they’re on the prowl!"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	mutations = user_data.get_mutations()

	slimes_spent = ewutils.getIntToken(tokens = cmd.tokens, allow_all = True)
	capture_discount = 1

	if ewcfg.mutation_id_lonewolf in mutations:
		if user_data.time_expirpvp > time_now:
			if len(users_in_district) == 1:
				capture_discount *= 0.8
		else:
			if len(users_in_district) == 0:
				capture_discount *= 0.8

	if ewcfg.mutation_id_patriot in mutations:
		capture_discount *= 0.8

	if slimes_spent == None:
		response = "How much slime do you want to spend on spraying graffiti in this district?"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if slimes_spent < 0:
		slimes_spent = user_data.slime

	if slimes_spent > user_data.slime:
		response = "You don't have that much slime, retard."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	num_lock = len(allies_in_district)
	if user_data.time_expirpvp < time_now:
		num_lock += 1

	if (district_data.controlling_faction not in ["", user_data.faction]) or (district_data.capturing_faction not in ["", user_data.faction]):
		slimes_decap = min(district_data.capture_points, int(slimes_spent / capture_discount))
		decap_resp = district_data.change_capture_points(
			progress = -slimes_decap,
			actor = user_data.faction,
			num_lock = num_lock
		)
		resp_cont.add_response_container(decap_resp)
		
		user_data.change_slime(n = -slimes_decap * capture_discount, source = ewcfg.source_spending)
		slimes_spent -= slimes_decap * capture_discount

	slimes_cap = min(district_data.max_capture_points - district_data.capture_points, int(slimes_spent / capture_discount))
	cap_resp = district_data.change_capture_points(
		progress = slimes_cap,
		actor = user_data.faction,
		num_lock = num_lock
	)
	resp_cont.add_response_container(cap_resp)
		
	user_data.change_slime(n = -slimes_cap * capture_discount, source = ewcfg.source_spending)

	# Flag the user for PvP
	# user_data.time_expirpvp = ewutils.calculatePvpTimer(user_data.time_expirpvp, ewcfg.time_pvp_annex, True)

	user_data.persist()
	district_data.persist()
	await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)

	return await resp_cont.post()
"""
async def shamble(cmd):

	user_data = EwPlayer(member = cmd.message.author)

	if user_data.life_state != ewcfg.life_state_shambler and user_data.poi != ewcfg.poi_id_assaultflatsbeach:
		response = "You have too many higher brain functions left to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	elif user_data.life_state in [ewcfg.life_state_juvenile, ewcfg.life_state_enlisted] and user_data.poi == ewcfg.poi_id_assaultflatsbeach:
		response = "You feel an overwhelming sympathy for the plight of the Shamblers and decide to join their ranks."
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		await asyncio.sleep(5)
		
		user_data = EwPlayer(member=cmd.message.author)
		user_data.life_state = ewcfg.life_state_shambler
		user_data.degradation = 100

		ewutils.moves_active[user_data.id_user] = 0

		user_data.poi = ewcfg.poi_id_nuclear_beach_edge
		user_data.persist()
		
		member = cmd.message.author
		
		base_poi_channel = ewutils.get_channel(cmd.message.guild, 'nuclear-beach-edge')

		response = 'You arrive inside the facility and are injected with a unique strain of the Modelovirus. Not long after, a voice on the intercom chimes in.\n**"Welcome, {}. Welcome to Downpour Laboratories. It\'s safer here. Please treat all machines and facilities with respect, they are precious to our cause."**'.format(member.name)

		await ewrolemgr.updateRoles(client=cmd.client, member=member)
		return await ewutils.send_message(cmd.client, base_poi_channel, ewutils.formatMessage(cmd.message.author, response))
	
	else:
		pass

	# Rest in fucking pieces

	# if poi is None:
	# 	return
	# elif not poi.is_district:
	# 	response = "This doesn't seem like an important place to be shambling. Try a district zone instead."
	# 	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	# elif poi.id_poi == ewcfg.poi_id_oozegardens:
	# 	response = "The entire district is covered in Brightshades! You have no business shambling this part of town!"
	# 	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	# 
	# in_operation, op_poi = ewutils.gvs_check_if_in_operation(user_data)
	# if in_operation:
	# 	if op_poi != user_data.poi:
	# 		response = "You aren't allowed to !shamble this district, per Dr. Downpour's orders.\n(**!goto {}**)".format(op_poi)
	# 		return await ewutils.send_message(cmd.client, cmd.message.channel,  ewutils.formatMessage(cmd.message.author, response))
	# else:
	# 	response = "You aren't even in a Graveyard Op yet!\n(**!joinops [tombstone]**)"
	# 	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	# 
	# if (time_now - user_data.time_lasthaunt) < ewcfg.cd_shambler_shamble:
	# 	response = "You know, you really just don't have the energy to shamble this place right now. Try again in {} seconds.".format(int(ewcfg.cd_shambler_shamble-(time_now-user_data.time_lasthaunt)))
	# 	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	# 
	# district_data = EwDistrict(district = poi.id_poi, id_server = cmd.guild.id)
	# 
	# if district_data.degradation < poi.max_degradation:
	# 	district_data.degradation += 1
	# 	# user_data.degradation += 1
	# 	user_data.time_lasthaunt = time_now
	# 	district_data.persist()
	# 	user_data.persist()
	# 	
	# 	response = "You shamble {}.".format(poi.str_name)
	# 	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	# 
	# 	if district_data.degradation == poi.max_degradation:
	# 		response = ewcfg.str_zone_degraded.format(poi = poi.str_name)
	# 		await ewutils.send_message(cmd.client, cmd.message.channel, response)

async def rejuvenate(cmd):
	user_data = EwPlayer(member=cmd.message.author)

	if user_data.life_state == ewcfg.life_state_shambler and user_data.poi != ewcfg.poi_id_oozegardens:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	elif user_data.life_state == ewcfg.life_state_shambler and user_data.poi == ewcfg.poi_id_oozegardens:
		response = "You decide to change your ways and become one of the Garden Gankers in order to overthrow your old master."
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		await asyncio.sleep(5)

		user_data = EwPlayer(member=cmd.message.author)
		user_data.life_state = ewcfg.life_state_juvenile
		user_data.degradation = 0
		#user_data.gvs_currency = 0

		ewutils.moves_active[user_data.id_user] = 0

		user_data.poi = ewcfg.poi_id_og_farms
		user_data.persist()

		client = ewutils.get_client()
		server = client.get_guild(user_data.id_server)
		member = server.get_member(user_data.id_user)
		
		base_poi_channel = ewutils.get_channel(cmd.message.guild, ewcfg.channel_og_farms)

		response = "You enter into Atomic Forest inside the farms of Ooze Gardens and are sterilized of the Modelovirus. Hortisolis gives you a big hug and says he's glad you've overcome your desire for vengeance in pursuit of deposing Downpour."

		await ewrolemgr.updateRoles(client=cmd.client, member=member)
		return await ewutils.send_message(cmd.client, base_poi_channel, ewutils.formatMessage(cmd.message.author, response))

	else:
		pass


"""
	Updates/Increments the capture_points values of all districts every time it's called
"""

async def capture_tick(id_server):
	# the variables might apparently be accessed before assignment if i didn't declare them here
	cursor = None
	conn_info = None

	resp_cont_capture_tick = ewutils.EwResponse(client = ewutils.get_client(), id_server = id_server)

	all_districts = ewcfg.capturable_districts


	if len(all_districts) > 0:  # if all_districts isn't empty
		server = ewcfg.server_list[id_server]
		time_old = time.time()

		for district in all_districts:
			district_name = district
			dist = EwDistrict(id_server = id_server, district = district_name)

			if dist.time_unlock > 0 and not dist.all_neighbors_friendly():
				responses = dist.change_capture_lock(progress = -ewcfg.capture_tick_length)
				resp_cont_capture_tick.add_response_container(responses)
				dist.persist()

			if dist.time_unlock > 0:
				continue

			# no more automatic capping
			continue

			controlling_faction = dist.controlling_faction

			gangsters_in_district = dist.get_players_in_district(min_slimes = ewcfg.min_slime_to_cap, life_states = [ewcfg.life_state_enlisted], ignore_offline = True)
					

			slimeoids = ewutils.get_slimeoids_in_poi(poi = district_name, id_server = id_server, sltype = ewcfg.sltype_nega)
			
			nega_present = len(slimeoids) > 0
#			if nega_present:
#				continue

			# the faction that's actively capturing the district this tick
			# if no players are present, it's None, if only players of one faction (ignoring juvies and ghosts) are,
			# it's the faction's name, i.e. 'rowdys' or 'killers', and if both are present, it's 'both'
			faction_capture = None

			# how much progress will be made. is higher the more people of one faction are in a district, and is 0 if both teams are present
			capture_speed = 0

			# number of players actively capturing
			num_capturers = 0

			dc_stat_increase_list = []

			# checks if any players are in the district and if there are only players of the same faction, i.e. progress can happen
			for player in gangsters_in_district:
				player_id = player
				user_data = EwPlayer(id_user = player_id, id_server = id_server)
				player_faction = user_data.faction

				mutations = user_data.get_mutations()

				try:
					player_online = server.get_member(player_id).status != discord.Status.offline
				except:
					player_online = False

				#ewutils.logMsg("Online status checked. Time elapsed: %f" % (time.time() - time_old) + " Server: %s" % id_server + " Player: %s" % player_id + " Status: %s" % ("online" if player_online else "offline"))

				if player_online:
					if faction_capture not in [None, player_faction]:  # if someone of the opposite faction is in the district
						faction_capture = 'both'  # standstill, gang violence has to happen
						capture_speed = 0
						num_capturers = 0
						dc_stat_increase_list.clear()

					else:  # if the district isn't already controlled by the player's faction and the capture isn't halted by an enemy
						faction_capture = player_faction
						player_capture_speed = 1
						if ewcfg.mutation_id_lonewolf in mutations and len(gangsters_in_district) == 1:
							player_capture_speed *= 2
						if ewcfg.mutation_id_patriot in mutations:
							player_capture_speed *= 2
							

						capture_speed += player_capture_speed
						num_capturers += 1
						dc_stat_increase_list.append(player_id)


			if faction_capture not in ['both', None]:  # if only members of one faction is present
				if district_name in ewcfg.capturable_districts:
					friendly_neighbors = dist.get_number_of_friendly_neighbors()
					if dist.all_neighbors_friendly():
						capture_speed = 0
					elif dist.controlling_faction == faction_capture:
						capture_speed *= 1 + 0.1 * friendly_neighbors
					else:
						capture_speed /= 1 + 0.1 * friendly_neighbors

					capture_progress = dist.capture_points

					if faction_capture != dist.capturing_faction:
						capture_progress *= -1

					capture_speed *= ewcfg.baseline_capture_speed


					if dist.capture_points < dist.max_capture_points:
						for stat_recipient in dc_stat_increase_list:
							ewstats.change_stat(
								id_server = id_server,
								id_user = stat_recipient,
								metric = ewcfg.stat_capture_points_contributed,
								n = ewcfg.capture_tick_length * capture_speed
							)

					if faction_capture == dist.capturing_faction:  # if the faction is already in the process of capturing, continue
						responses = dist.change_capture_points(ewcfg.capture_tick_length * capture_speed, faction_capture, num_capturers)
						resp_cont_capture_tick.add_response_container(responses)

					elif dist.capture_points == 0 and dist.controlling_faction == "":  # if it's neutral, start the capture
						responses =  dist.change_capture_points(ewcfg.capture_tick_length * capture_speed, faction_capture, num_capturers)
						resp_cont_capture_tick.add_response_container(responses)

						dist.capturing_faction = faction_capture

					# lower the enemy faction's progress to revert it to neutral (or potentially get it onto your side without becoming neutral first)
					else:  # if the (de-)capturing faction is not in control
						responses =  dist.change_capture_points(-(ewcfg.capture_tick_length * capture_speed * ewcfg.decapture_speed_multiplier), faction_capture)
						resp_cont_capture_tick.add_response_container(responses)

					dist.persist()

	# await resp_cont_capture_tick.post()

"""
	Coroutine that continually calls capture_tick; is called once per server, and not just once globally
"""
async def capture_tick_loop(id_server):
	interval = ewcfg.capture_tick_length
	# causes a capture tick to happen exactly every 10 seconds (the "elapsed" thing might be unnecessary, depending on how long capture_tick ends up taking on average)
	while not ewutils.TERMINATE:
		await capture_tick(id_server = id_server)
		# ewutils.logMsg("Capture tick happened on server %s." % id_server + " Timestamp: %d" % int(time.time()))

		await asyncio.sleep(interval)

"""
	Gives both kingpins the appropriate amount of slime for how many districts they own and lowers the capture_points property of each district by a certain amount, turning them neutral after a while
"""
async def give_kingpins_slime_and_decay_capture_points(id_server):
	resp_cont_decay_loop = ewutils.EwResponse(client = ewutils.get_client(), id_server = id_server)

	for kingpin_role in [ewcfg.role_rowdyfucker, ewcfg.role_copkiller]:
		kingpin = ewutils.find_kingpin(id_server = id_server, kingpin_role = kingpin_role)

		if kingpin is not None:
			total_slimegain = 0
			for id_district in ewcfg.capturable_districts:

				district = EwDistrict(id_server = id_server, district = id_district)

				# if the kingpin is controlling this district give the kingpin slime based on the district's property class
				if district.controlling_faction == (ewcfg.faction_killers if kingpin.faction == ewcfg.faction_killers else ewcfg.faction_rowdys):
					poi = ewcfg.id_to_poi.get(id_district)

					slimegain = ewcfg.district_control_slime_yields[poi.property_class]

					# increase slimeyields by 10 percent per friendly neighbor
					friendly_mod = 1 + 0.1 * district.get_number_of_friendly_neighbors()
					total_slimegain += slimegain * friendly_mod

			kingpin.change_slime(n = total_slimegain)
			kingpin.persist()

			ewutils.logMsg(kingpin_role + " just received %d" % total_slimegain + " slime for their captured districts.")

	# Decay capture points.
	for id_district in ewcfg.capturable_districts:
		district = EwDistrict(id_server = id_server, district = id_district)

		responses =  district.decay_capture_points()
		resp_cont_decay_loop.add_response_container(responses)
		district.persist()
	# await resp_cont_decay_loop.post()

async def change_spray(cmd):
	user_data = EwPlayer(member=cmd.message.author)
	newspray = cmd.message.content[(len(ewcfg.cmd_changespray)):].strip()

	if newspray == "":
		response = "You need to add an image link to change your spray."
	elif len(newspray) > 400:
		response = "Fucking christ, are you painting the Sistine Chapel? Use a shorter link."
	else:
		response = "Got it. Spray set."
		user_data.spray = newspray
		user_data.persist()

	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


async def tag(cmd):
	user_data = EwPlayer(member=cmd.message.author)

	if user_data.life_state in(ewcfg.life_state_enlisted, ewcfg.life_state_kingpin):
		response = user_data.spray
	else:
		response = "Save the spraying for the gangsters. You're either too gay or dead to participate in this sort of thing."
	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


