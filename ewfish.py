import random
import asyncio
import time
import ewcfg
import ewutils
import ewitem
import ewrolemgr

from ewmarket import EwMarket
from ew import EwPlayer
from ewitem import EwItem
from ewdistrict import EwDistrict

fishers = {}
fishing_counter = 0

# Randomly generates a fish.
def gen_fish(x, fisher, has_fishingrod):
	fish_pool = []

	rarity_number = random.randint(0, 100)

	# TODO: reimplement chance to get items in black pond using negapoudrin 
	# fragments when any of that shit has any use beyond making staves.
	# just ctrl+f the variable below and remove anything to do with it
	voidfishing = fisher.pier.pier_type == ewcfg.fish_slime_void
	if has_fishingrod == True:
		if rarity_number >= 0 and rarity_number < 21 and not voidfishing:  # 20%
			fish = "item"
			return fish

		elif voidfishing or rarity_number >= 21 and rarity_number < 31:  # 10%
			for fish in ewcfg.fish_names:
				if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_common:
					fish_pool.append(fish)

		elif rarity_number >= 31 and rarity_number < 71:  # 40%
			for fish in ewcfg.fish_names:
				if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_uncommon:
					fish_pool.append(fish)

		elif rarity_number >= 71 and rarity_number < 91:  # 20%
			for fish in ewcfg.fish_names:
				if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_rare:
					fish_pool.append(fish)
		else:  # 10%
			for fish in ewcfg.fish_names:
				if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_promo:
					fish_pool.append(fish)

	else:
		if rarity_number >= 0 and rarity_number < 11 and not voidfishing: # 10%
			fish = "item"
			return fish

		elif rarity_number >= 11 and rarity_number < 61: # 50%
			for fish in ewcfg.fish_names:
				if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_common:
					fish_pool.append(fish)

		elif voidfishing or rarity_number >= 61 and rarity_number < 91: # 30%
			for fish in ewcfg.fish_names:
				if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_uncommon:
					fish_pool.append(fish)

		elif rarity_number >= 91 and rarity_number < 100: # 9%
			for fish in ewcfg.fish_names:
				if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_rare:
					fish_pool.append(fish)
		else: # 1%
			for fish in ewcfg.fish_names:
				if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_promo:
					fish_pool.append(fish)

	market_data = x #todo ?
	weather_data = ewcfg.weather_map.get(market_data.weather)

	if weather_data.name != "rainy":
		for fish in fish_pool:
			if ewcfg.fish_map[fish].catch_time == ewcfg.fish_catchtime_rain:
				fish_pool.remove(fish)

	if market_data.clock < 20 or market_data.clock > 5:
		for fish in fish_pool:
			if ewcfg.fish_map[fish].catch_time == ewcfg.fish_catchtime_night:
				fish_pool.remove(fish)
	elif market_data.clock < 8 or market_data.clock > 17:
		for fish in fish_pool:
			if ewcfg.fish_map[fish].catch_time == ewcfg.fish_catchtime_day:
				fish_pool.remove(fish)
	else:
		for fish in fish_pool:
			if ewcfg.fish_map[fish].catch_time != None:
				fish_pool.remove(fish)

	# Filter out fish from other pier types
	fish = random.choice([fish for fish in fish_pool if ewcfg.fish_map[fish].slime == fisher.pier.pier_type])
	
	# Get fucked
	if fisher.pier.id_poi == ewcfg.poi_id_juviesrow_pier:
		fish = 'plebefish'

	return fish

# Determines the size of the fish
def gen_fish_size(has_fishingrod):
	size_number = random.randint(0, 100)

	if has_fishingrod == True:
		if size_number >= 0 and size_number < 6:  # 5%
			size = ewcfg.fish_size_miniscule
		elif size_number >= 6 and size_number < 11:  # 5%
			size = ewcfg.fish_size_small
		elif size_number >= 11 and size_number < 31:  # 20%
			size = ewcfg.fish_size_average
		elif size_number >= 31 and size_number < 71:  # 40%
			size = ewcfg.fish_size_big
		elif size_number >= 71 and size_number < 91:  # 20
			size = ewcfg.fish_size_huge
		else:  # 10%
			size = ewcfg.fish_size_colossal

	else:
		if size_number >= 0 and size_number < 6:  # 5%
			size = ewcfg.fish_size_miniscule
		elif size_number >= 6 and size_number < 21:  # 15%
			size = ewcfg.fish_size_small
		elif size_number >= 21 and size_number < 71:  # 50%
			size = ewcfg.fish_size_average
		elif size_number >= 71 and size_number < 86:  # 15%
			size = ewcfg.fish_size_big
		elif size_number >= 86 and size_number < 100:  # 4
			size = ewcfg.fish_size_huge
		else:  # 1%
			size = ewcfg.fish_size_colossal

	return size

# Determines bite text
def gen_bite_text(size):
	if size == "item":
		text = "You feel a distinctly inanimate tug at your fishing pole!"

	elif size == ewcfg.fish_size_miniscule:
		text = "You feel a wimpy tug at your fishing pole!"
	elif size == ewcfg.fish_size_small:
		text = "You feel a mediocre tug at your fishing pole!"
	elif size == ewcfg.fish_size_average:
		text = "You feel a modest tug at your fishing pole!"
	elif size == ewcfg.fish_size_big:
		text = "You feel a mildly threatening tug at your fishing pole!"
	elif size == ewcfg.fish_size_huge:
		text = "You feel a startlingly strong tug at your fishing pole!"
	else:
		text = "You feel a tug at your fishing pole so intense that you nearly get swept off your feet!"

	text += " **!REEL NOW!!!!!**"
	return text

""" Casts a line into the Slime Sea """
async def cast(cmd):
	time_now = round(time.time())
	has_reeled = False
	user_data = EwPlayer(member = cmd.message.author)
	mutations = user_data.get_mutations()
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

	market_data = EwMarket(id_server = cmd.message.author.guild.id)
	statuses = user_data.getStatusEffects()

	if cmd.message.author.id not in fishers.keys():
		fishers[cmd.message.author.id] = EwFisher()

	fisher = fishers[cmd.message.author.id]

	# Ghosts cannot fish.
	if user_data.life_state == ewcfg.life_state_corpse:
		response = "You can't fish while you're dead. Try {}.".format(ewcfg.cmd_revive)

	# Players who are already cast a line cannot cast another one.
	elif fisher.fishing == True:
		response = "You've already cast a line."

	# Only fish at The Pier
	elif user_data.poi in ewcfg.piers:
		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		rod_possession = user_data.get_possession('rod')
		if rod_possession: 
			fisher.inhabitant_id = rod_possession[0]

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		elif user_data.hunger >= user_data.get_hunger_max():
			response = "You're too hungry to fish right now."
		elif (not fisher.inhabitant_id) and (poi.id_poi == ewcfg.poi_id_blackpond):
			response = "You cast your fishing line into the pond, but your hook bounces off its black waters like hard concrete."
		else:
			has_fishingrod = False

			if user_data.weapon >= 0:
				weapon_item = EwItem(id_item = user_data.weapon)
				weapon = ewcfg.weapon_map.get(weapon_item.item_props.get("weapon_type"))
				if weapon.id_weapon == "fishingrod":
					has_fishingrod = True

			if ewcfg.status_high_id in statuses:
				fisher.high = True
			fisher.fishing = True
			fisher.bait = False
			fisher.pier = poi
			fisher.current_fish = gen_fish(market_data, fisher, has_fishingrod)
			
			high_value_bait_used = False

			global fishing_counter
			fishing_counter += 1
			current_fishing_id = fisher.fishing_id = fishing_counter

			item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
			author = cmd.message.author
			server = cmd.guild

			item_sought = ewitem.find_item(item_search = item_search, id_user = author.id, id_server = server.id)

			if item_sought:
				item = EwItem(id_item = item_sought.get('id_item'))

				if item.item_type == ewcfg.it_food:

					str_name = item.item_props['food_name']
					id_food = item.item_props.get('id_food')
					fisher.bait = True

					if id_food in ewcfg.plebe_bait:
						fisher.current_fish = "plebefish"

					elif id_food == "doublestuffedcrust":
						if random.randrange(5) == 3:
							fisher.current_fish = "doublestuffedflounder"

					elif id_food in ["chickenbucket", "familymeal"]:
						if random.randrange(5) == 3:
							fisher.current_fish = "seacolonel"

					elif id_food in ["steakvolcanoquesomachorito", "nachosupreme"]:
						if random.randrange(5) == 3:
							fisher.current_fish = "marlinsupreme"

					elif id_food in ["blacklimes", "blacklimesour"]:
						if random.randrange(2) == 1:
							fisher.current_fish = "blacklimesalmon"

					elif id_food in ["pinkrowddishes", "pinkrowdatouille"]:
						if random.randrange(2) == 1:
							fisher.current_fish = "thrash"

					elif id_food in ["purplekilliflowercrustpizza", "purplekilliflower"]:
						if random.randrange(2) == 1:
							fisher.current_fish = "dab"

					elif id_food == "kingpincrab":
						if random.randrange(5) == 1:
							fisher.current_fish = "uncookedkingpincrab"
							
					elif id_food == "masterbait":
						high_value_bait_used = True

					elif id_food == "ferroslimeoid":
						fisher.current_fish = "seaitem"

					elif float(item.time_expir if item.time_expir is not None else 0) < time.time():
						if random.randrange(2) == 1:
							fisher.current_fish = "plebefish"
					ewitem.item_delete(item_sought.get('id_item'))

			if fisher.current_fish == "item":
				fisher.current_size = "item"

			else:
				fisher.current_size = gen_fish_size(has_fishingrod)

			if fisher.bait == False:
				response = "You cast your fishing line into the "
			else:
				response = "You attach your {} to the hook as bait and then cast your fishing line into the ".format(str_name)


			if fisher.pier.pier_type == ewcfg.fish_slime_saltwater:
				response += "vast Slime Sea."
			elif fisher.pier.pier_type == ewcfg.fish_slime_freshwater:
				response += "glowing Slime Lake."
			elif fisher.pier.pier_type == ewcfg.fish_slime_void:
				response += "pond's black waters."

			user_data.hunger += ewcfg.hunger_perfish * ewutils.hunger_cost_mod(user_data.slimelevel)
			user_data.persist()
			
			await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	
			bite_text = gen_bite_text(fisher.current_size)
			
			# User has a 1/10 chance to get a bite
			fun = 100

			if fisher.bait == True:
				# Bait attatched, chance to get a bite increases from 1/10 to 1/7
				fun -= 30
			if fisher.pier == ewcfg.poi_id_ferry:
				# Fisher is on the ferry, chance to get a bite increases from 1/10 to 1/9
				fun -= 10
			if ewcfg.mutation_id_lucky in mutations:
				fun -= 20
			if fisher.inhabitant_id:
				# Having your rod possessed increases your chance to get a bite by 50%
				fun = int(fun // 2)
			if high_value_bait_used:
				fun = 5
				
			bun = 0

			while not ewutils.TERMINATE:
				
				if fun <= 0:
					fun = 1
				else:
					damp = random.randrange(fun)
				
				if fisher.high:
					await asyncio.sleep(30)
				elif high_value_bait_used:
					await asyncio.sleep(5)
				else:
					await asyncio.sleep(60)

				# Cancel if fishing was interrupted
				if current_fishing_id != fisher.fishing_id:
					return
				if fisher.fishing == False:
					return

				user_data = EwPlayer(member=cmd.message.author)

				if fisher.pier == "" or user_data.poi != fisher.pier.id_poi:
					fisher.stop()
					return
				if user_data.life_state == ewcfg.life_state_corpse:
					fisher.stop()
					return

				if damp > 10:
					await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, random.choice(ewcfg.void_fishing_text if fisher.pier.pier_type == ewcfg.fish_slime_void else ewcfg.normal_fishing_text)))
					fun -= 2
					bun += 1
					if bun >= 5:
						fun -= 1
					if bun >= 15:
						fun -= 1
					continue
				else:
					break


			fisher.bite = True
			await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, bite_text))

			await asyncio.sleep(8)

			if fisher.bite != False:
				response = "The fish got away..."
				response += cancel_rod_possession(fisher, user_data)
				fisher.stop()
				return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
			else:
				has_reeled = True

	else:
		response = "You can't fish here. Go to a pier."
	
	# Don't send out a response if the user actually reeled in a fish, since that gets sent by the reel command instead.
	if has_reeled == False:
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		

""" Reels in the fishing line.. """
async def reel(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

	if cmd.message.author.id not in fishers.keys():
		fishers[cmd.message.author.id] = EwFisher()
	fisher = fishers[cmd.message.author.id]
	poi = ewcfg.id_to_poi.get(user_data.poi)

	if user_data.life_state == ewcfg.life_state_corpse:
		valid_possession = user_data.get_possession('rod')
		if valid_possession:
			inhabitee = user_data.get_inhabitee()
			fisher = fishers[inhabitee] if inhabitee in fishers.keys() else None
			if fisher:
				if fisher.bite == False:
					fisher.fleshling_reeled = True
					response = "You reeled in too early! You and your pal get nothing."
					response += cancel_rod_possession(fisher, user_data)
					fisher.fleshling_reeled = True
					fisher.stop()
				else:
					if fisher.fleshling_reeled:
						response = await award_fish(fisher, cmd, user_data)
					else:
						fisher.ghost_reeled = True
						response = "You reel in anticipation of your fleshy partner!"
			else:
				response = "You fleshy partner hasn't even cast their hook yet."
		else:
			response = "You can't fish while you're dead."

	elif user_data.poi in ewcfg.piers:
		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		# Players who haven't cast a line cannot reel.
		if fisher.fishing == False:
			response = "You haven't cast your hook yet. Try !cast."

		# If a fish isn't biting, then a player reels in nothing.
		elif fisher.bite == False:
			response = ''
			if fisher.inhabitant_id:
				fisher.ghost_reeled = True
				response = "You reeled in too early! You and your pal get nothing."
				response += cancel_rod_possession(fisher, user_data)
			else:
				response = "You reeled in too early! Nothing was caught."
			fisher.stop()

		# On successful reel.
		else:
			if fisher.ghost_reeled or not fisher.inhabitant_id:
				response = await award_fish(fisher, cmd, user_data)
			else:
				fisher.fleshling_reeled = True
				response = "You reel in anticipation of your ghostly partner!"
	else:
		response = "You cast your fishing rod unto a sidewalk. That is to say, you've accomplished nothing. Go to a pier if you want to fish."

	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
	# gangsters don't need their roles updated
	if user_data.life_state == ewcfg.life_state_juvenile:
		await ewrolemgr.updateRoles(client = cmd.client, member = cmd.message.author)

async def award_fish(fisher, cmd, user_data): 
	response = ""

	actual_fisherman = None
	actual_fisherman_data = user_data
	if fisher.inhabitant_id:
		actual_fisherman = user_data.get_possession()[1]
		actual_fisherman_data = EwPlayer(id_user=actual_fisherman, id_server=cmd.guild.id)

	if fisher.current_fish in ["item", "seaitem"]:
		slimesea_inventory = ewitem.inventory(id_server = cmd.guild.id, id_user = ewcfg.poi_id_slimesea)			

		if (fisher.pier.pier_type != ewcfg.fish_slime_saltwater or len(slimesea_inventory) == 0 or random.random() < 0.5) and fisher.current_fish == "item":

			item = random.choice(ewcfg.mine_results)
		
			if actual_fisherman_data.juviemode:
				unearthed_item_amount = 1
			else:
				unearthed_item_amount = (random.randrange(5) + 8) # anywhere from 8-12 drops

			item_props = ewitem.gen_item_props(item)

			for creation in range(unearthed_item_amount):
				ewitem.item_create(
					item_type = item.item_type,
					id_user = actual_fisherman or cmd.message.author.id,
					id_server = cmd.guild.id,
					item_props = item_props
				)

			response = "You reel in {} {}s! ".format(unearthed_item_amount, item.str_name)

		else:
			item = random.choice(slimesea_inventory)

			ewitem.give_item(id_item = item.get('id_item'), member = cmd.message.author)

			response = "You reel in a {}!".format(item.get('name'))

		fisher.stop()
		user_data.persist()

	else:
		user_initial_level = user_data.slimelevel

		gang_bonus = False

		has_fishingrod = False

		if user_data.weapon >= 0:
			weapon_item = EwItem(id_item = user_data.weapon)
			weapon = ewcfg.weapon_map.get(weapon_item.item_props.get("weapon_type"))
			if weapon.id_weapon == "fishingrod":
				has_fishingrod = True

		value = 0

		if fisher.current_size == ewcfg.fish_size_miniscule:
			slime_gain = ewcfg.fish_gain * 1
			value += 10

		elif fisher.current_size == ewcfg.fish_size_small:
			slime_gain = ewcfg.fish_gain * 2

			value += 20

		elif fisher.current_size == ewcfg.fish_size_average:
			slime_gain = ewcfg.fish_gain * 3
			value += 30

		elif fisher.current_size == ewcfg.fish_size_big:
			slime_gain = ewcfg.fish_gain * 4
			value += 40

		elif fisher.current_size == ewcfg.fish_size_huge:
			slime_gain = ewcfg.fish_gain * 5
			value += 50

		else:
			slime_gain = ewcfg.fish_gain * 6
			value += 60

		if ewcfg.fish_map[fisher.current_fish].rarity == ewcfg.fish_rarity_common:
			value += 10

		if ewcfg.fish_map[fisher.current_fish].rarity == ewcfg.fish_rarity_uncommon:
			value += 20

		if ewcfg.fish_map[fisher.current_fish].rarity == ewcfg.fish_rarity_rare:
			value += 30

		if ewcfg.fish_map[fisher.current_fish].rarity == ewcfg.fish_rarity_promo:
			value += 40

		if user_data.life_state == 2:
			if ewcfg.fish_map[fisher.current_fish].catch_time == ewcfg.fish_catchtime_day and user_data.faction == ewcfg.faction_rowdys:
				gang_bonus = True
				slime_gain = slime_gain * 1.5
				value += 20

			if ewcfg.fish_map[fisher.current_fish].catch_time == ewcfg.fish_catchtime_night and user_data.faction == ewcfg.faction_killers:
				gang_bonus = True
				slime_gain = slime_gain * 1.5
				value += 20

		if has_fishingrod == True:
			slime_gain = slime_gain * 2

		#trauma = ewcfg.trauma_map.get(user_data.trauma)
		#if trauma != None and trauma.trauma_class == ewcfg.trauma_class_slimegain:
		#	slime_gain *= (1 - 0.5 * user_data.degradation / 100)

		if fisher.pier.pier_type == ewcfg.fish_slime_void:
			slime_gain = slime_gain * 1.5
			value += 30

		if fisher.current_fish == "plebefish":
			slime_gain = ewcfg.fish_gain * .5
			value = 10
			
		controlling_faction = ewutils.get_subzone_controlling_faction(user_data.poi, user_data.id_server)

		if controlling_faction != "" and controlling_faction == user_data.faction:
			slime_gain *= 2


		if user_data.poi == ewcfg.poi_id_juviesrow_pier:
			slime_gain = int(slime_gain / 4)

		trauma = ewcfg.trauma_map.get(user_data.trauma)
		if trauma != None and trauma.trauma_class == ewcfg.trauma_class_slimegain:
			slime_gain *= (1 - 0.5 * user_data.degradation / 100)

		slime_gain = max(0, round(slime_gain))

		ewitem.item_create(
			id_user = actual_fisherman or cmd.message.author.id,
			id_server = cmd.guild.id,
			item_type = ewcfg.it_food,
			item_props = {
				'id_food': ewcfg.fish_map[fisher.current_fish].id_fish,
				'food_name': ewcfg.fish_map[fisher.current_fish].str_name,
				'food_desc': ewcfg.fish_map[fisher.current_fish].str_desc,
				'recover_hunger': 20,
				'str_eat': ewcfg.str_eat_raw_material.format(ewcfg.fish_map[fisher.current_fish].str_name),
				'rarity': ewcfg.fish_map[fisher.current_fish].rarity,
				'size': fisher.current_size,
				'time_expir': time.time() + ewcfg.std_food_expir,
				'time_fridged': 0,
				'acquisition': ewcfg.acquisition_fishing,
				'value': value,
				'noslime': 'true' if actual_fisherman_data.juviemode else 'false'
			}
		)

		if fisher.inhabitant_id:
			server = cmd.guild
			inhabitant_member = server.get_member(fisher.inhabitant_id)
			inhabitant_name = inhabitant_member.name
			inhabitant_data = EwPlayer(id_user = fisher.inhabitant_id, id_server = user_data.id_server)
			inhabitee_name = server.get_member(actual_fisherman).name

			slime_gain = int(0.25 * slime_gain)

			response = "The two of you together manage to reel in a {fish}! {flavor} {ghost} haunts {slime:,} slime away from the fish before placing it on {fleshling}'s hands."\
				.format(
					fish = ewcfg.fish_map[fisher.current_fish].str_name, 
					flavor = ewcfg.fish_map[fisher.current_fish].str_desc, 
					ghost = inhabitant_name,
					fleshling = inhabitee_name,
					slime = slime_gain,
				)

			inhabitant_data.change_slime(n = -slime_gain)
			inhabitant_data.persist()
			fisher.stop()
		else:
			response = "You reel in a {fish}! {flavor} You grab hold and wring {slime:,} slime from it. "\
				.format(fish = ewcfg.fish_map[fisher.current_fish].str_name, flavor = ewcfg.fish_map[fisher.current_fish].str_desc, slime = slime_gain)
			if gang_bonus == True:
				if user_data.faction == ewcfg.faction_rowdys:
					response += "The Rowdy-pride this fish is showing gave you more slime than usual. "
				elif user_data.faction == ewcfg.faction_killers:
					response += "The Killer-pride this fish is showing gave you more slime than usual. "

			levelup_response = user_data.change_slime(n = slime_gain, source = ewcfg.source_fishing)
			was_levelup = True if user_initial_level < user_data.slimelevel else False
			# Tell the player their slime level increased.
			if was_levelup:
				response += levelup_response

		fisher.stop()

		user_data.persist()
	return response

async def appraise(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

	market_data = EwMarket(id_server = user_data.id_server)
	item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
	item_sought = ewitem.find_item(item_search = item_search, id_user = cmd.message.author.id, id_server = cmd.guild.id if cmd.guild is not None else None)
	payment = ewitem.find_item(item_search = "manhattanproject", id_user = cmd.message.author.id, id_server = cmd.guild.id if cmd.guild is not None else None, item_type_filter = ewcfg.it_food)

	# Checking availability of appraisal
	#if market_data.clock < 8 or market_data.clock > 17:
	#	response = "You ask the bartender if he knows someone who would want to trade you something for your recently caught fish. Apparently, at night, an old commodore by the name of Captain Albert Alexander comes to drown his sorrows at this very tavern. You guess you’ll just have to sit here and wait for him, then."

	if cmd.message.channel.name != ewcfg.channel_speakeasy:
		if user_data.poi in ewcfg.piers:
			response = 'You ask a nearby fisherman if he could appraise this fish you just caught. He tells you to fuck off, but also helpfully informs you that there’s an old sea captain that frequents the Speakeasy that might be able to help you. What an inexplicably helpful/grouchy fisherman!'
		else:
			response = 'What random passerby is going to give two shits about your fish? You’ll have to consult a fellow fisherman… perhaps you’ll find some on a pier?'

	elif item_sought:
		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		name = item_sought.get('name')
		fish = EwItem(id_item = item_sought.get('id_item'))
		item_props = fish.item_props
		# str_fish = fish.item_props.get('str_name')
		# id_fish = item_props['id_food']
		acquisition = item_props.get('acquisition')

		response = "You approach a man of particularly swashbuckling appearance, adorned in an old sea captain's uniform and bicorne cap, and surrounded by empty glass steins. You ask him if he is Captain Albert Alexander and he replies that he hasn’t heard that name in a long time. You submit your {} for appraisal".format(name)

		if acquisition != ewcfg.acquisition_fishing:
			response += '. \n"Have you lost yer mind, laddy? That’s not a fish!! Just what’re you trying to pull??"'.format(name)

		else:

			if payment == None:
				response += ", but he says he won’t provide his services for free... but, if you bring him a Manhattan Project, you might be able to get an appraisal."

			else:
				item_props = fish.item_props
				rarity = item_props['rarity']
				size = item_props['size']
				value = int(item_props['value'])

				response += ' and offer him a Manhattan Project as payment. \n"Hm, alright, let’s see here...'

				if rarity == ewcfg.fish_rarity_common:
					response += "Ah, a {}, that’s a pretty common fish... ".format(name)

				if rarity == ewcfg.fish_rarity_uncommon:
					response += "Interesting, a {}, that’s a pretty uncommon fish you’ve got there... ".format(name)

				if rarity == ewcfg.fish_rarity_rare:
					response += "Amazing, it’s a {}! Consider yourself lucky, that’s a pretty rare fish! ".format(name)

				if rarity == ewcfg.fish_rarity_promo:
					response += "Shiver me timbers, is that a {}?? Unbelievable, that’s an extremely rare fish!! It was only ever released as a promotional item in Japan during the late ‘90s. ".format(name)

				if size == ewcfg.fish_size_miniscule:
					response += "Or, is it just a speck of dust? Seriously, that {} is downright miniscule! ".format(name)

				if size == ewcfg.fish_size_small:
					response += "Hmmm, it’s a little small, don’t you think? "

				if size == ewcfg.fish_size_average:
					response += "It’s an average size for the species. "

				if size == ewcfg.fish_size_big:
					response += "Whoa, that’s a big one, too! "

				if size == ewcfg.fish_size_huge:
					response += "Look at the size of that thing, it’s huge! "

				if size == ewcfg.fish_size_colossal:
					response += "By Neptune’s beard, what a sight to behold, this {name} is absolutely colossal!! In all my years in the Navy, I don’t think I’ve ever seen a {name} as big as yours!! ".format(name = name)

				response += "So, I’d say this fish "

				if value <= 20:
					response += 'is absolutely worthless."'

				if value <= 40 and value >= 21:
					response += 'isn’t worth very much."'

				if value <= 60 and value >= 41:
					response += 'is somewhat valuable."'

				if value <= 80 and value >= 61:
					response += 'is highly valuable!"'

				if value <= 99 and value >= 81:
					response += 'is worth a fortune!!"'

				if value >= 100:
					response += 'is the most magnificent specimen I’ve ever seen!"'

				ewitem.item_delete(id_item = payment.get('id_item'))

				user_data.persist()
	else:
		if item_search:  # If they didn't forget to specify an item and it just wasn't found.
			response = "You don't have one."

		else:
			response = "Ask Captain Albert Alexander to appraise which fish? (check **!inventory**)"

	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


async def barter(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	mutations = user_data.get_mutations()
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

	market_data = EwMarket(id_server = user_data.id_server)
	item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
	item_sought = ewitem.find_item(item_search = item_search, id_user = cmd.message.author.id, id_server = cmd.guild.id if cmd.guild is not None else None)

	# Checking availability of appraisal
	#if market_data.clock < 8 or market_data.clock > 17:
	#	response = "You ask the bartender if he knows someone who would want to trade you something for your recently caught fish. Apparently, at night, an old commodore by the name of Captain Albert Alexander comes to drown his sorrows at this very tavern. You guess you’ll just have to sit here and wait for him, then."

	if cmd.message.channel.name != ewcfg.channel_speakeasy:
		if user_data.poi in ewcfg.piers:
			response = 'You ask a nearby fisherman if he wants to trade you anything for this fish you just caught. He tells you to fuck off, but also helpfully informs you that there’s an old sea captain that frequents the Speakeasy that might be able to help you. What an inexplicably helpful/grouchy fisherman!'
		else:
			response = 'What random passerby is going to give two shits about your fish? You’ll have to consult a fellow fisherman… perhaps you’ll find some on a pier?'

	elif item_sought:
		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		name = item_sought.get('name')
		fish = EwItem(id_item = item_sought.get('id_item'))
		id_fish = fish.id_item
		# str_fish = fish.item_props.get('str_name')
		item_props = fish.item_props
		acquisition = item_props.get('acquisition')
		response = "You approach a man of particularly swashbuckling appearance, adorned in an old sea captain's uniform and bicorne cap, and surrounded by empty glass steins. You ask him if he is Captain Albert Alexander and he replies that he hasn’t heard that name in a long time. You submit your {} for bartering".format(name)

		if acquisition != ewcfg.acquisition_fishing:
			response += '. \n"Have you lost yer mind, laddy? That’s not a fish!! Just what’re you trying to pull??"'

		else:
			value = int(item_props['value'])

			items = []

			# Filters out all non-generic items without the current fish as an ingredient.
			for result in ewcfg.appraise_results:
				if result.ingredients == fish.item_props.get('id_item') or result.ingredients == "generic" and result.acquisition == ewcfg.acquisition_bartering:  # Generic means that it can be made with any fish.
					items.append(result)
				else:
					pass

			# Filters out items of greater value than your fish.
			for value_filter in items:
				if value < value_filter.context:
					items.remove(value_filter)
				else:
					pass

			else:
				offer = EwOffer(
					id_server = cmd.guild.id,
					id_user = cmd.message.author.id,
					offer_give = id_fish
				)

				cur_time_min = time.time() / 60
				time_offered = cur_time_min - offer.time_sinceoffer

				if offer.time_sinceoffer > 0 and time_offered < ewcfg.fish_offer_timeout:
					offer_receive = str(offer.offer_receive)

					if offer_receive.isdigit() == True:
						slime_gain = int(offer.offer_receive)

						response = '\n"Well, back again I see! My offer still stands, I’ll trade ya {} slime for your {}"'.format(slime_gain, name)

					elif ewcfg.mutation_id_davyjoneskeister in mutations and item_props.get('noslime') != "true":
						max_value = value * 6000  # 600,000 slime for a colossal promo fish, 120,000 for a miniscule common fish.
						min_value = max_value / 10  # 60,000 slime for a colossal promo fish, 12,000 for a miniscule common fish.

						slime_gain = round(random.triangular(min_value, max_value, min_value * 2))

						offer.offer_receive = slime_gain
						offer.persist()
						response = '\n"You know what, laddy? I like the cut of your jib. I\'ll change my offer. How about {} slime for your {}?"'.format(slime_gain, name)

					else:
						for result in ewcfg.appraise_results:
							if hasattr(result, 'id_item'):
								if result.id_item != offer.offer_receive:
									pass
								else:
									item = result

							if hasattr(result, 'id_food'):
								if result.id_food != offer.offer_receive:
									pass
								else:
									item = result

							if hasattr(result, 'id_cosmetic'):
								if result.id_cosmetic != offer.offer_receive:
									pass
								else:
									item = result

						response = '\n"Well, back again I see! My offer still stands, I’ll trade ya a {} for your {}"'.format(item.str_name, name)

					response += "\n**!accept** or **!refuse** Captain Albert Alexander's deal."

					await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

				else:
					# Random choice between 0, 1, and 2
					offer_decision = random.randint(0, 2)

					if (offer_decision != 2 or ewcfg.mutation_id_davyjoneskeister in mutations) and item_props.get('noslime') != "true": # If Captain Albert Alexander wants to offer you slime for your fish. 66% chance.
						max_value = value * 6000 # 600,000 slime for a colossal promo fish, 120,000 for a miniscule common fish.
						min_value = max_value / 10 # 60,000 slime for a colossal promo fish, 12,000 for a miniscule common fish.

						slime_gain = round(random.triangular(min_value, max_value, min_value * 2))

						offer.offer_receive = slime_gain

						response = '"Hm, alright… for this {}... I’ll offer you {} slime! Trust me, you’re not going to get a better deal anywhere else, laddy."'.format(name, slime_gain)

					else: # If Captain Albert Alexander wants to offer you an item for your fish. 33% chance. Once there are more unique items, we'll make this 50%.
						item = random.choice(items)

						if hasattr(item, 'id_item'):
							offer.offer_receive = item.id_item

						if hasattr(item, 'id_food'):
							offer.offer_receive = item.id_food

						if hasattr(item, 'id_cosmetic'):
							offer.offer_receive = item.id_cosmetic

						response = '"Hm, alright… for this {}... I’ll offer you a {}! Trust me, you’re not going to get a better deal anywhere else, laddy."'.format(name, item.str_name)

					offer.time_sinceoffer = int(time.time() / 60)
					offer.persist()

					response += "\n**!accept** or **!refuse** Captain Albert Alexander's deal."

					await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

				# Wait for an answer
				accepted = False

				try:
					message = await cmd.client.wait_for('message', timeout = 20, check=lambda message: message.author == cmd.message.author and 
															message.content.lower() in [ewcfg.cmd_accept, ewcfg.cmd_refuse])

					if message != None:
						if message.content.lower() == ewcfg.cmd_accept:
							accepted = True
						if message.content.lower() == ewcfg.cmd_refuse:
							accepted = False
				except:
					accepted = False

				offer = EwOffer(
					id_server = cmd.guild.id,
					id_user = cmd.message.author.id,
					offer_give = id_fish
				)

				user_data = EwPlayer(member = cmd.message.author)
				fish = EwItem(id_item = id_fish)

				# cancel deal if fish is no longer in user's inventory
				if fish.id_owner != str(user_data.id_user):
					accepted = False

				# cancel deal if the user has left Vagrant's Corner
				if user_data.poi != ewcfg.poi_id_speakeasy:
					accepted = False

				# cancel deal if the offer has been deleted
				if offer.time_sinceoffer == 0:
					accepted = False


				if accepted == True:
					offer_receive = str(offer.offer_receive)

					response = ""

					if offer_receive.isdigit() == True:
						slime_gain = int(offer_receive)

						user_initial_level = user_data.slimelevel

						levelup_response = user_data.change_slime(n = slime_gain, source = ewcfg.source_fishing)

						was_levelup = True if user_initial_level < user_data.slimelevel else False

						# Tell the player their slime level increased.
						if was_levelup:
							response += levelup_response
							response += "\n\n"

					else:
						item_props = ewitem.gen_item_props(item)	

						ewitem.item_create(
							item_type = item.item_type,
							id_user = cmd.message.author.id,
							id_server = cmd.guild.id,
							item_props = item_props
						)


					ewitem.item_delete(id_item = item_sought.get('id_item'))

					user_data.persist()

					offer.deal()

					response += '"Pleasure doing business with you, laddy!"'

				else:
					response = '"Ah, what a shame. Maybe you’ll change your mind in the future…?"'

	else:
		if item_search:  # If they didn't forget to specify an item and it just wasn't found.
			response = "You don't have one."
		else:
			response = "Offer Captain Albert Alexander which fish? (check **!inventory**)"

	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def barter_all(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	mutations = user_data.get_mutations()
	#if shambler, break
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	#if non-zone channel, break
	if ewutils.channel_name_is_poi(cmd.message.channel.name) == False:
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, "You must {} in a zone's channel.".format(cmd.tokens[0])))

	#if not in speakeasy, break
	if cmd.message.channel.name != ewcfg.channel_speakeasy:
		if user_data.poi in ewcfg.piers:
			response = 'You ask a nearby fisherman if he wants to trade you anything for this fish you just caught. He tells you to fuck off, but also helpfully informs you that there’s an old sea captain that frequents the Speakeasy that might be able to help you. What an inexplicably helpful/grouchy fisherman!'
		else:
			response = 'What random passerby is going to give two shits about your fish? You’ll have to consult a fellow fisherman… perhaps you’ll find some on a pier?'

		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	food_items = ewitem.inventory(id_user = user_data.id_user, id_server = user_data.id_server,item_type_filter = ewcfg.it_food)
	offer_items = [] #list of items to create when offer goes through
	offer_slime = 0 #slime to give player when offer goes through
	fish_ids_to_remove = [] #list of fish to delete when offer goes through

	

	#check if food item is a fish and add to offer if it is
	for item in food_items:
		fish =  EwItem(id_item = item.get('id_item'))
		#if item is a fish, add to offer
		if fish.item_props.get('acquisition') == ewcfg.acquisition_fishing:
			fish_ids_to_remove.append(fish.id_item)
			value = int(fish.item_props['value'])
			
			# Random choice between 0, 1, and 2
			offer_decision = random.randint(0, 2)

			if (offer_decision != 2 or ewcfg.mutation_id_davyjoneskeister in mutations) and fish.item_props.get('noslime') != "true": # If Captain Albert Alexander wants to offer you slime for your fish. 66% chance.
				max_value = value * 6000 # 600,000 slime for a colossal promo fish, 120,000 for a miniscule common fish.
				min_value = max_value / 10 # 60,000 slime for a colossal promo fish, 12,000 for a miniscule common fish.

				slime_gain = round(random.triangular(min_value, max_value, min_value * 2))

				offer_slime += slime_gain

			else: # If Captain Albert Alexander wants to offer you an item for your fish. 33% chance. Once there are more unique items, we'll make this 50%.
				potential_items = []
				# Filters out all non-generic items without the current fish as an ingredient.
				for result in ewcfg.appraise_results:
					if result.ingredients == fish.item_props.get('id_item') or result.ingredients == "generic" and result.acquisition == ewcfg.acquisition_bartering:  # Generic means that it can be made with any fish.
						potential_items.append(result)
					else:
						pass
				# Filters out items of greater value than your fish.
				for value_filter in potential_items:
					if value < value_filter.context:
						potential_items.remove(value_filter)
					else:
						pass
				
				offer_items.append(random.choice(potential_items))

	#if player had some fish to offer
	if offer_slime > 0 or len(offer_items) > 0:
		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		
		
		response = "You approach a man of particularly swashbuckling appearance, adorned in an old sea captain's uniform and bicorne cap, and surrounded by empty glass steins. You ask him if he is Captain Albert Alexander and he replies that he hasn’t heard that name in a long time. You drop all of your fish at his feet"
		
		
		items_desc = ""
		if len(offer_items) > 0:
			if len(offer_items) > 4:
				items_desc = "a handful items"
			elif len(offer_items) > 1:
				items_desc = "a few items"
			else:
				items_desc = "a {}".format(offer_items[0].str_name)


		offer_desc = "{}{}{}".format((str(offer_slime) + " slime") if (offer_slime > 0) else "", " and " if (offer_slime > 0 and len(items_desc) > 0) else "", items_desc if (len(items_desc) > 0) else "")
		response += ' \n"Hm, alright… for your fish... I’ll trade you {}!"'.format(offer_desc)

		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		

		response = ""

		if offer_slime > 0:
			slime_gain = offer_slime

			user_initial_level = user_data.slimelevel

			levelup_response = user_data.change_slime(n = slime_gain, source = ewcfg.source_fishing)

			was_levelup = True if user_initial_level < user_data.slimelevel else False

			# Tell the player their slime level increased.
			if was_levelup:
				response += levelup_response
				response += "\n\n"

		if len(offer_items):
			for item in offer_items:
				item_props = ewitem.gen_item_props(item)	

				ewitem.item_create(
					item_type = item.item_type,
					id_user = cmd.message.author.id,
					id_server = cmd.guild.id,
					item_props = item_props
				)

		for id in fish_ids_to_remove:
			ewitem.item_delete(id_item = id)

		user_data.persist()


		response += '"Pleasure doing business with you, laddy!"'


	#player has no fish
	else:
		response = "You need some fish to barter with Captain Albert Alexander. Get out there and do some fishing!"

	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def debug_create_random_fish(cmd):
	
	if ewutils.DEBUG or cmd.message.author.guild_permissions.administrator:
		pass
	else:
		return
	
	fish = random.choice(ewcfg.fish_names) 
	

	size_number = random.randint(0, 100)

	if size_number >= 0 and size_number < 6:  # 5%
		size = ewcfg.fish_size_miniscule
	elif size_number >= 6 and size_number < 11:  # 5%
		size = ewcfg.fish_size_small
	elif size_number >= 11 and size_number < 31:  # 20%
		size = ewcfg.fish_size_average
	elif size_number >= 31 and size_number < 71:  # 40%
		size = ewcfg.fish_size_big
	elif size_number >= 71 and size_number < 91:  # 20
		size = ewcfg.fish_size_huge
	else:  # 10%
		size = ewcfg.fish_size_colossal

	value = 0

	if size == ewcfg.fish_size_miniscule:
		value += 10

	elif size == ewcfg.fish_size_small:
		value += 20

	elif size == ewcfg.fish_size_average:
		value += 30

	elif size == ewcfg.fish_size_big:
		value += 40

	elif size == ewcfg.fish_size_huge:
		value += 50

	else:
		value += 60

	if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_common:
		value += 10

	if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_uncommon:
		value += 20

	if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_rare:
		value += 30

	if ewcfg.fish_map[fish].rarity == ewcfg.fish_rarity_promo:
		value += 40

	ewitem.item_create(
		id_user = cmd.message.author.id,
		id_server = cmd.guild.id,
		item_type = ewcfg.it_food,
		item_props = {
			'id_food': ewcfg.fish_map[fish].id_fish,
			'food_name': ewcfg.fish_map[fish].str_name,
			'food_desc': ewcfg.fish_map[fish].str_desc,
			'recover_hunger': 20,
			'str_eat': ewcfg.str_eat_raw_material.format(ewcfg.fish_map[fish].str_name),
			'rarity': ewcfg.fish_map[fish].rarity,
			'size': size,
			'time_expir': time.time() + ewcfg.std_food_expir,
			'time_fridged': 0,
			'acquisition': ewcfg.acquisition_fishing,
			'value': value
		}
	)



def kill_dead_offers(id_server):
	time_now = int(time.time() / 60)
	ewutils.execute_sql_query("DELETE FROM offers WHERE {id_server} = %s AND {time_sinceoffer} < %s".format(
		id_server = ewcfg.col_id_server,
		time_sinceoffer = ewcfg.col_time_sinceoffer,
	),(
		id_server,
		time_now - ewcfg.fish_offer_timeout,
	))

async def embiggen(cmd):
	user_data = EwPlayer(member = cmd.message.author)
	if user_data.life_state == ewcfg.life_state_shambler:
		response = "You lack the higher brain functions required to {}.".format(cmd.tokens[0])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	market_data = EwMarket(id_server = user_data.id_server)
	item_search = ewutils.flattenTokenListToString(cmd.tokens[1:])
	item_sought = ewitem.find_item(item_search = item_search, id_user = cmd.message.author.id, id_server = cmd.guild.id if cmd.guild is not None else None)

	if cmd.message.channel.name != ewcfg.channel_slimeoidlab:
		response = "How are you going to embiggen your fish on the side of the street? You’ve got to see a professional for this, man. Head to the SlimeCorp Laboratory, they’ve got dozens of modern day magic potions ‘n shit over there."

	elif item_sought:
		poi = ewcfg.id_to_poi.get(user_data.poi)
		district_data = EwDistrict(district = poi.id_poi, id_server = user_data.id_server)

		if district_data.is_degraded():
			response = "{} has been degraded by shamblers. You can't {} here anymore.".format(poi.str_name, cmd.tokens[0])
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		name = item_sought.get('name')
		fish = EwItem(id_item = item_sought.get('id_item'))
		acquisition = fish.item_props.get('acquisition')

		if fish.item_props.get('id_furniture') == "singingfishplaque":

			poudrins_owned = ewitem.find_item_all(item_search="slimepoudrin", id_user=user_data.id_user, id_server=user_data.id_server, item_type_filter=ewcfg.it_item)
			poudrin_amount = len(poudrins_owned)

			if poudrin_amount < 2:
				response = "You don't have the poudrins for it."
			else:
				for delete in range(2):
					poudrin = poudrins_owned.pop()
					ewitem.item_delete(id_item = poudrin.get("id_item"))
				fish.item_props['id_furniture'] = "colossalsingingfishplaque"
				fish.item_props['furniture_look_desc'] = "There's a fake fish mounted on the wall. Hoo boy, it's a whopper."
				fish.item_props['furniture_place_desc'] = "You take a nail gun to the wall to force it to hold this fish. Christ,  this thing is your fucking Ishmael. Er, Moby Dick. Whatever."
				fish.item_props['furniture_name'] = "colossal singing fish plaque"
				fish.item_props['furniture_desc'] = "You press the button on your gigantic plaque.\n***" + fish.item_props.get('furniture_desc')[38:-87].upper().replace(":NOTES:", ":notes:") + "***\nYou abruptly turn the fish off before you rupture an eardrum."
				fish.persist()
				response = "The elevator ride down to the embiggening ward feels like an eterninty. Are they going to find out the fish you're embiggening is fake? God, you hope not. But eventually, you make it down, and place the plaque in the usual reclined surgeon's chair. A stray spark from one of the defibrilators nearly gives you a heart attack. But even so, the embiggening process begins like usual. You sign the contract, and they take a butterfly needle to your beloved wall prop. And sure enough, it begins to grow. You hear the sounds of cracked plastic and grinding electronics, and catch a whiff of burnt wires. It's growing. It's 6 feet, no, 10 feet long. Good god. You were hoping for growth, but science has gone too far. Eventually, it stops. Although you raise a few eyebrows with ths anomaly, you still get back the colossal fish plaque without a hitch."
		elif acquisition != ewcfg.acquisition_fishing:
			response = "You can only embiggen fishes, dummy. Otherwise everyone would be walking around with colossal nunchucks and huge chicken buckets. Actually, that gives me an idea..."

		else:
			size = fish.item_props.get('size')

			poudrin_cost = 0

			if size == ewcfg.fish_size_miniscule:
				poudrin_cost = 2

			if size == ewcfg.fish_size_small:
				poudrin_cost = 4

			if size == ewcfg.fish_size_average:
				poudrin_cost = 8

			if size == ewcfg.fish_size_big:
				poudrin_cost = 16

			if size == ewcfg.fish_size_huge:
				poudrin_cost = 32

			poudrins_owned = ewitem.find_item_all(item_search = "slimepoudrin", id_user = user_data.id_user, id_server = user_data.id_server, item_type_filter = ewcfg.it_item)
			poudrin_amount = len(poudrins_owned)

			if poudrin_cost == 0:
				response = "Your {} is already as colossal as a fish can get!".format(name)

			elif poudrin_amount < poudrin_cost:
				response = "You need {} poudrins to embiggen your {}, but you only have {}!!".format(poudrin_cost, name, poudrin_amount)

			else:
				if size == ewcfg.fish_size_miniscule:
					fish.item_props['size'] = ewcfg.fish_size_small

				if size == ewcfg.fish_size_small:
					fish.item_props['size'] = ewcfg.fish_size_average

				if size == ewcfg.fish_size_average:
					fish.item_props['size'] = ewcfg.fish_size_big

				if size == ewcfg.fish_size_big:
					fish.item_props['size'] = ewcfg.fish_size_huge

				if size == ewcfg.fish_size_huge:
					fish.item_props['size'] = ewcfg.fish_size_colossal

				fish.persist()

				for delete in range(poudrin_cost):
					poudrin = poudrins_owned.pop()
					ewitem.item_delete(id_item = poudrin.get("id_item"))

				market_data.donated_poudrins += poudrin_cost
				market_data.persist()
				user_data.poudrin_donations += poudrin_cost
				user_data.persist()

				response = "After several minutes long elevator descents, in the depths of some basement level far below the laboratory's lobby, you lay down your {} on a reclined medical chair. A SlimeCorp employee finishes the novel length terms of service they were reciting and asks you if you have any questions. You weren’t listening so you just tell them to get on with it so you can go back to haggling prices with Captain Albert Alexander. They oblige.\nThey grab a butterfly needle and carefully stab your fish with it, injecting filled with some bizarre, multi-colored serum you’ve never seen before. Sick, it’s bigger now!!".format(name)

	else:
		if item_search:  # If they didn't forget to specify an item and it just wasn't found.
			response = "You don't have one."
		else:
			response = "Embiggen which fish? (check **!inventory**)"

	await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

def cancel_rod_possession(fisher, user_data):
	response = ''
	if fisher.inhabitant_id:
		user_data.cancel_possession()
		response += '\n'
		if fisher.fleshling_reeled:
			response += "Fucking ghosts, can't rely on them for anything."
		elif fisher.ghost_reeled:
			response += "You can't trust the living even for the simplest shit, I guess."
		else:
			response += "Are you two even trying?"
		response += ' Your contract is dissolved.'
	return response