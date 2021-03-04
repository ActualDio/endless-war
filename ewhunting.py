import time
import random
import math
import asyncio

import ewcfg
import ewutils
import ewitem
import ewrolemgr
import ewstats
import ewwep

from ew import EwPlayer
from ewitem import EwItem
from ewmarket import EwMarket
from ewplayer import EwDiscordUser
from ewdistrict import EwDistrict
from ewslimeoid import EwSlimeoid
from ewstatuseffects import EwEnemyStatusEffect

		
# Debug command. Could be used for events, perhaps?
async def summonenemy(cmd):

	author = cmd.message.author

	if not author.guild_permissions.administrator:
		return

	time_now = int(time.time())
	response = ""
	user_data = EwPlayer(member=cmd.message.author)
	data_level = 0

	enemytype = None
	enemy_location = None
	enemy_coord = None
	poi = None
	enemy_slimes = None
	enemy_displayname = None
	enemy_level = None
	
	resp_cont = None

	if len(cmd.tokens) >= 3:

		enemytype = cmd.tokens[1]
		enemy_location = cmd.tokens[2]
		
		if len(cmd.tokens) >= 6:
			enemy_slimes = cmd.tokens[3]
			enemy_level = cmd.tokens[4]
			enemy_coord = cmd.tokens[5]
			enemy_displayname = " ".join(cmd.tokens[6:])
	
		poi = ewcfg.id_to_poi.get(enemy_location)

	if enemytype != None and poi != None:
		
		data_level = 1

		if enemy_slimes != None and enemy_displayname != None and enemy_level != None and enemy_coord != None:
			data_level = 2
			
		if data_level == 1:
			resp_cont = spawn_enemy(id_server=cmd.message.guild.id, pre_chosen_type=enemytype, pre_chosen_poi=poi.id_poi, manual_spawn=True)
		elif data_level == 2:
			
			resp_cont = spawn_enemy(
				id_server=cmd.message.guild.id,
				pre_chosen_type=enemytype, 
				pre_chosen_poi=poi.id_poi, 
				pre_chosen_level=enemy_level, 
				pre_chosen_slimes=enemy_slimes,
				pre_chosen_initialslimes = enemy_slimes,
				pre_chosen_coord = enemy_coord,
				pre_chosen_displayname=enemy_displayname,
				pre_chosen_weather=ewcfg.enemy_weathertype_normal,
				manual_spawn = True,
			)
			
		await resp_cont.post()
		
	else:
		response = "**DEBUG**: PLEASE RE-SUMMON WITH APPLICABLE TYPING / LOCATION. ADDITIONAL OPTIONS ARE SLIME / LEVEL / COORD / DISPLAYNAME"
		await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


async def summongvsenemy(cmd):
	author = cmd.message.author

	if not author.guild_permissions.administrator:
		return

	time_now = int(time.time())
	response = ""
	user_data = EwPlayer(member=cmd.message.author)

	poi = None
	enemytype = None
	coord = None
	joybean_status = None

	if cmd.tokens_count == 4:
		enemytype = cmd.tokens[1]
		coord = cmd.tokens[2]
		joybean_status = cmd.tokens[3]
		poi = ewcfg.id_to_poi.get(user_data.poi)
	else:
		response = "Correct usage: !summongvsenemy [type] [coord] [joybean status ('yes', otherwise false)]"
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
		
	if enemytype != None and poi != None and joybean_status != None and coord != None:
		props = None
		try:
			props = ewcfg.enemy_data_table[enemytype]["props"]

			if joybean_status.lower() == 'yes':
				props['joybean'] = 'true'
			
		except:
			pass

		resp_cont = spawn_enemy(
			id_server=cmd.message.guild.id, 
			pre_chosen_type=enemytype, 
			pre_chosen_poi=poi.id_poi,
			pre_chosen_coord=coord.upper(),
			pre_chosen_props=props,
			pre_chosen_weather=ewcfg.enemy_weathertype_normal,
			manual_spawn=True,
		)
	
		await resp_cont.post()


async def delete_all_enemies(cmd=None, query_suffix="", id_server_sent=""):
	
	if cmd != None:
		author = cmd.message.author
	
		if not author.guild_permissions.administrator:
			return
		
		id_server = cmd.message.guild.id
		
		ewutils.execute_sql_query("DELETE FROM enemies WHERE id_server = {id_server}".format(
			id_server=id_server
		))
		
		ewutils.logMsg("Deleted all enemies from database connected to server {}".format(id_server))
		
	else:
		id_server = id_server_sent

		ewutils.execute_sql_query("DELETE FROM enemies WHERE id_server = {} {}".format(
			id_server,
			query_suffix
		))

		ewutils.logMsg("Deleted all enemies from database connected to server {}. Query suffix was '{}'".format(id_server, query_suffix))

# Gathers all enemies from the database (that are either raid bosses or have users in the same district as them) and has them perform an action
async def enemy_perform_action(id_server):
	#time_start = time.time()
	
	client = ewcfg.get_client()

	time_now = int(time.time())

	enemydata = ewutils.execute_sql_query(
		"SELECT {id_enemy} FROM enemies WHERE ((enemies.poi IN (SELECT users.poi FROM users WHERE NOT (users.life_state = %s OR users.life_state = %s) AND users.id_server = {id_server})) OR (enemies.enemytype IN %s) OR (enemies.life_state = %s OR enemies.expiration_date < %s) OR (enemies.id_target != -1)) AND enemies.id_server = {id_server}".format(
		id_enemy=ewcfg.col_id_enemy,
		id_server=id_server
	), (
		ewcfg.life_state_corpse,
		ewcfg.life_state_kingpin,
		ewcfg.raid_bosses,
		ewcfg.enemy_lifestate_dead,
		time_now
	))
	#enemydata = ewutils.execute_sql_query("SELECT {id_enemy} FROM enemies WHERE id_server = %s".format(
	#	id_enemy = ewcfg.col_id_enemy
	#),(
	#	id_server,
	#))

	# Remove duplicates from SQL query
	#enemydata = set(enemydata)

	for row in enemydata:
		enemy = EwEnemy(id_enemy=row[0], id_server=id_server)
		enemy_statuses = enemy.getStatusEffects()
		resp_cont = ewutils.EwResponseContainer(id_server=id_server)

		# If an enemy is marked for death or has been alive too long, delete it
		if enemy.life_state == ewcfg.enemy_lifestate_dead or (enemy.expiration_date < time_now):
			delete_enemy(enemy)
		else:
			# If an enemy is an activated raid boss, it has a 1/20 chance to move between districts.
			if enemy.enemytype in ewcfg.enemy_movers and enemy.life_state == ewcfg.enemy_lifestate_alive and check_raidboss_movecooldown(enemy):
				if random.randrange(20) == 0:
					resp_cont = enemy.move()
					if resp_cont != None:
						await resp_cont.post()

			# If an enemy is alive and not a sandbag, make it perform the kill function.
			if enemy.enemytype != ewcfg.enemy_type_sandbag:
				
				ch_name = ewcfg.id_to_poi.get(enemy.poi).channel 

				# Check if the enemy can do anything right now
				if enemy.life_state == ewcfg.enemy_lifestate_unactivated and check_raidboss_countdown(enemy):
					# Raid boss has activated!
					response = "*The ground quakes beneath your feet as slime begins to pool into one hulking, solidified mass...*" \
							"\n{} **{} has arrived! It's level {} and has {} slime!** {}\n".format(
						ewcfg.emote_megaslime,
						enemy.name,
						enemy.level,
						enemy.slime,
						ewcfg.emote_megaslime
					)
					resp_cont.add_channel_response(ch_name, response)

					enemy.life_state = ewcfg.enemy_lifestate_alive
					enemy.time_lastenter = int(time.time())
					enemy.persist()

				# If a raid boss is currently counting down, delete the previous countdown message to reduce visual clutter.
				elif check_raidboss_countdown(enemy) == False:
					timer = (enemy.raidtimer - (int(time.time())) + ewcfg.time_raidcountdown)

					if timer < ewcfg.enemy_attack_tick_length and timer != 0:
						timer = ewcfg.enemy_attack_tick_length

					countdown_response = "A sinister presence is lurking. Time remaining: {} seconds...".format(timer)
					resp_cont.add_channel_response(ch_name, countdown_response)

					#TODO: Edit the countdown message instead of deleting and reposting
					last_messages = await resp_cont.post()
					asyncio.ensure_future(ewutils.delete_last_message(client, last_messages, ewcfg.enemy_attack_tick_length))
					resp_cont = None

				elif any([ewcfg.status_evasive_id, ewcfg.status_aiming_id]) not in enemy_statuses and random.randrange(10) == 0:
					resp_cont = random.choice([enemy.dodge, enemy.taunt, enemy.aim])()
				else:
					resp_cont = await enemy.kill()
			else:
				resp_cont = None
				
			if resp_cont != None:
				await resp_cont.post()

	#time_end = time.time()
	#ewutils.logMsg("time spent on performing enemy actions: {}".format(time_end - time_start))

async def enemy_perform_action_gvs(id_server):

	client = ewcfg.get_client()

	time_now = int(time.time())

	# condition_gaia_sees_shambler_player = "enemies.poi IN (SELECT users.poi FROM users WHERE (users.life_state = '{}'))".format(ewcfg.life_state_shambler)
	# condition_gaia_sees_shampler_enemy = "enemies.poi IN (SELECT enemies.poi FROM enemies WHERE (enemies.enemyclass = '{}'))".format(ewcfg.enemy_class_shambler)
	# condition_shambler_sees_alive_player = "enemies.poi IN (SELECT users.poi FROM users WHERE (users.life_state IN {}))".format(tuple([ewcfg.life_state_juvenile, ewcfg.life_state_enlisted, ewcfg.life_state_executive]))
	# condition_shambler_sees_gaia_enemy = "enemies.poi IN (SELECT enemies.poi FROM enemies WHERE (enemies.enemyclass = '{}'))".format(ewcfg.enemy_class_gaiaslimeoid)

	#print(despawn_timenow)
	#"SELECT {id_enemy} FROM enemies WHERE (enemies.enemytype IN %s) AND (({condition_1}) OR ({condition_2}) OR ({condition_3}) OR ({condition_4}) OR (enemies.enemytype IN %s) OR (enemies.life_state = %s OR enemies.expiration_date < %s) OR (enemies.id_target != '')) AND enemies.id_server = {id_server}"
	
	enemydata = ewutils.execute_sql_query(
		"SELECT {id_enemy} FROM enemies WHERE ((enemies.enemytype IN %s) OR (enemies.life_state = %s OR enemies.expiration_date < %s) OR (enemies.id_target != -1)) AND enemies.id_server = {id_server}".format(
			id_enemy=ewcfg.col_id_enemy,
			id_server=id_server,
		), (
			ewcfg.gvs_enemies,
			ewcfg.enemy_lifestate_dead,
			time_now
		))
	# enemydata = ewutils.execute_sql_query("SELECT {id_enemy} FROM enemies WHERE id_server = %s".format(
	#	id_enemy = ewcfg.col_id_enemy
	# ),(
	#	id_server,
	# ))

	# Remove duplicates from SQL query
	# enemydata = set(enemydata)

	for row in enemydata:
		
		enemy = EwEnemy(id_enemy=row[0], id_server=id_server)
		
		if enemy == None:
			continue

		if ewcfg.id_to_poi.get(enemy.poi) != None:
			ch_name = ewcfg.id_to_poi.get(enemy.poi).channel
		else:
			continue
		
		server = client.get_guild(id_server)
		channel = ewutils.get_channel(server, ch_name)

		# This function returns a false value if that enemy can't act on that turn.
		if not check_enemy_can_act(enemy):
			continue
		
		# Go through turn counters unrelated to the prevention of acting on that turn. 
		turn_timer_response = handle_turn_timers(enemy)
		if turn_timer_response != None and turn_timer_response != "":
			await ewutils.send_message(client, channel, turn_timer_response)

		enemy = EwEnemy(id_enemy=row[0], id_server=id_server)
		
		# Unarmed Gaiaslimeoids have no role in combat.
		if enemy.attacktype == ewcfg.enemy_attacktype_unarmed:
			continue
		
		resp_cont = ewutils.EwResponseContainer(id_server=id_server)

		# If an enemy is marked for death or has been alive too long, delete it
		if enemy.life_state == ewcfg.enemy_lifestate_dead or (enemy.expiration_date < time_now):
			delete_enemy(enemy)
		else:
			# The GvS raidboss has pre-determined pathfinding
			if enemy.enemytype in ewcfg.raid_bosses and enemy.life_state == ewcfg.enemy_lifestate_alive and check_raidboss_movecooldown(enemy):
				resp_cont = enemy.move()
				if resp_cont != None:
					await resp_cont.post()

			# If an enemy is alive, make it perform the kill (or cannibalize) function.

			# Check if the enemy can do anything right now
			if enemy.life_state == ewcfg.enemy_lifestate_unactivated and check_raidboss_countdown(enemy):
				# Raid boss has activated!
				response = "*The dreaded creature of Dr. Downpour claws its way into {}.*" \
						   "\n{} **{} has arrived! It's level {} and has {} slime. Good luck.** {}\n".format(
					enemy.poi,
					ewcfg.emote_megaslime,
					enemy.name,
					enemy.level,
					enemy.slime,
					ewcfg.emote_megaslime
				)
				resp_cont.add_channel_response(ch_name, response)

				enemy.life_state = ewcfg.enemy_lifestate_alive
				enemy.time_lastenter = int(time.time())
				enemy.persist()

			# If a raid boss is currently counting down, delete the previous countdown message to reduce visual clutter.
			elif check_raidboss_countdown(enemy) == False:
				timer = (enemy.raidtimer - (int(time.time())) + ewcfg.time_raidcountdown)

				if timer < ewcfg.enemy_attack_tick_length and timer != 0:
					timer = ewcfg.enemy_attack_tick_length

				countdown_response = "A sinister presence is lurking. Time remaining: {} seconds...".format(timer)
				resp_cont.add_channel_response(ch_name, countdown_response)

				# TODO: Edit the countdown message instead of deleting and reposting
				last_messages = await resp_cont.post()
				asyncio.ensure_future(
					ewutils.delete_last_message(client, last_messages, ewcfg.enemy_attack_tick_length))
				resp_cont = None
			else:
				district_data = EwDistrict(district = enemy.poi, id_server = enemy.id_server)
				
				# Look for enemies of the opposing 'class'. If none are found, look for players instead.
				if enemy.enemytype in ewcfg.gvs_enemies_gaiaslimeoids:
					if len(district_data.get_enemies_in_district(classes = [ewcfg.enemy_class_shambler])) > 0:
						await enemy.cannibalize()
					# elif len(district_data.get_players_in_district(life_states = [ewcfg.life_state_shambler])) > 0:
					# 	await enemy.kill()
				elif enemy.enemytype in ewcfg.gvs_enemies_shamblers:
					life_states = [ewcfg.life_state_juvenile, ewcfg.life_state_enlisted, ewcfg.life_state_executive]
					
					if enemy.gvs_coord in ewcfg.gvs_coords_end:
						if len(district_data.get_players_in_district(life_states=life_states)) > 0 and enemy.gvs_coord in ewcfg.gvs_coords_end:
							await enemy.kill()
						else:
							continue
					else:
						if len(district_data.get_enemies_in_district(classes = [ewcfg.enemy_class_gaiaslimeoid])) > 0:
							await enemy.cannibalize()
						else:
							await sh_move(enemy)
				else:
					continue
				
			if resp_cont != None:
				await resp_cont.post()

# Spawns an enemy in a randomized outskirt district. If a district is full, it will try again, up to 5 times.
def spawn_enemy(
		id_server, 
		pre_chosen_type = None, 
		pre_chosen_level = None,
		pre_chosen_slimes = None,
		pre_chosen_displayname = None,
		pre_chosen_expiration = None,
		pre_chosen_initialslimes = None,
		pre_chosen_poi = None,
		pre_chosen_identifier = None,
		#pre_chosen_hardened_sap = None,
		pre_chosen_weather = None,
		pre_chosen_faction = None,
		pre_chosen_owner = None,
		pre_chosen_coord = None,
		pre_chosen_rarity = False,
		pre_chosen_props = None,
		manual_spawn = False,
	):
	
	time_now = int(time.time())
	response = ""
	ch_name = ""
	resp_cont = ewutils.EwResponseContainer(id_server = id_server)
	chosen_poi = ""
	potential_chosen_poi = ""
	threat_level = ""
	boss_choices = []

	enemies_count = ewcfg.max_enemies
	try_count = 0

	rarity_choice = random.randrange(10000)

	if rarity_choice <= 5200:
		# common enemies
		enemytype = random.choice(ewcfg.common_enemies)
	elif rarity_choice <= 8000:
		# uncommon enemies
		enemytype = random.choice(ewcfg.uncommon_enemies)
	elif rarity_choice <= 9700:
		# rare enemies
		enemytype = random.choice(ewcfg.rare_enemies)
	else:
		# raid bosses
		threat_level_choice = random.randrange(1000)
		
		if threat_level_choice <= 450:
			threat_level = "micro"
		elif threat_level_choice <= 720:
			threat_level = "monstrous"
		elif threat_level_choice <= 900:
			threat_level = "mega"
		else:
			threat_level = "mega"
			#threat_level = "nega"
		
		boss_choices = ewcfg.raid_boss_tiers[threat_level]
		enemytype = random.choice(boss_choices)
		
	if pre_chosen_type is not None:
		enemytype = pre_chosen_type
	
	if not manual_spawn:

		while enemies_count >= ewcfg.max_enemies and try_count < 5:

			# Sand bags only spawn in the dojo
			if enemytype == ewcfg.enemy_type_sandbag:
				potential_chosen_poi = ewcfg.poi_id_dojo
			else:
				potential_chosen_poi = random.choice(ewcfg.outskirts)

			potential_chosen_district = EwDistrict(district=potential_chosen_poi, id_server=id_server)
			enemies_list = potential_chosen_district.get_enemies_in_district()
			enemies_count = len(enemies_list)

			if enemies_count < ewcfg.max_enemies:
				chosen_poi = potential_chosen_poi
				try_count = 5
			else:
				# Enemy couldn't spawn in that district, try again
				try_count += 1

		# If it couldn't find a district in 5 tries or less, back out of spawning that enemy.
		if chosen_poi == "":
			return resp_cont

		# If an enemy spawns in the Nuclear Beach, it should be remade as a 'pre-historic' enemy.
		if potential_chosen_poi in [ewcfg.poi_id_nuclear_beach_edge, ewcfg.poi_id_nuclear_beach, ewcfg.poi_id_nuclear_beach_depths]:
			enemytype = random.choice(ewcfg.pre_historic_enemies)
			# If the enemy is a raid boss, re-roll it once to make things fair
			if enemytype in ewcfg.raid_bosses:
				enemytype = random.choice(ewcfg.pre_historic_enemies)
	else:
		if pre_chosen_poi == None:
			return
		
	if pre_chosen_poi != None:
		chosen_poi = pre_chosen_poi

	if enemytype != None:
		enemy = get_enemy_data(enemytype)

		# Assign enemy attributes that weren't assigned in get_enemy_data
		enemy.id_server = id_server
		enemy.slime = enemy.slime if pre_chosen_slimes is None else pre_chosen_slimes
		enemy.name = enemy.name if pre_chosen_displayname is None else pre_chosen_displayname
		enemy.level = level_byslime(enemy.slime) if pre_chosen_level is None else pre_chosen_level
		enemy.expiration_date = time_now + ewcfg.time_despawn if pre_chosen_expiration is None else pre_chosen_expiration
		enemy.initialslimes = enemy.slime if pre_chosen_initialslimes is None else pre_chosen_initialslimes
		enemy.poi = chosen_poi
		enemy.identifier = set_identifier(chosen_poi, id_server) if pre_chosen_identifier is None else pre_chosen_identifier
		#enemy.hardened_sap = int(enemy.level / 2) if pre_chosen_hardened_sap is None else pre_chosen_hardened_sap
		enemy.weathertype = ewcfg.enemy_weathertype_normal if pre_chosen_weather is None else pre_chosen_weather
		enemy.faction = '' if pre_chosen_faction is None else pre_chosen_faction
		enemy.owner = -1 if pre_chosen_owner is None else pre_chosen_owner
		enemy.gvs_coord = '' if pre_chosen_coord is None else pre_chosen_coord
		enemy.rare_status = enemy.rare_status if pre_chosen_rarity is None else pre_chosen_rarity

		if pre_chosen_weather != ewcfg.enemy_weathertype_normal:
			if pre_chosen_weather == ewcfg.enemy_weathertype_rainresist:
				enemy.name = "Bicarbonate {}".format(enemy.name)
				enemy.slime *= 2
		
		#TODO delete after double halloween
		market_data = EwMarket(id_server=id_server)
		if (enemytype == ewcfg.enemy_type_doubleheadlessdoublehorseman or enemytype == ewcfg.enemy_type_doublehorse) and market_data.horseman_deaths >= 1:
			enemy.slime *= 1.5

		props = None
		try:
			props = ewcfg.enemy_data_table[enemytype]["props"]
		except:
			pass

		enemy.enemy_props = props if pre_chosen_props is None else pre_chosen_props

		enemy.persist()

		# Recursively spawn enemies that belong to groups.
		if enemytype in ewcfg.enemy_group_leaders:
			sub_enemies_list = ewcfg.enemy_spawn_groups[enemytype]
			sub_enemies_list_item_max = len(sub_enemies_list)
			sub_enemy_list_item_count = 0

			while sub_enemy_list_item_count < sub_enemies_list_item_max:
				sub_enemy_type = sub_enemies_list[sub_enemy_list_item_count][0]
				sub_enemy_spawning_max = sub_enemies_list[sub_enemy_list_item_count][1]
				sub_enemy_spawning_count = 0

				sub_enemy_list_item_count += 1
				while sub_enemy_spawning_count < sub_enemy_spawning_max:
					sub_enemy_spawning_count += 1

					sub_resp_cont = spawn_enemy(id_server=id_server, pre_chosen_type=sub_enemy_type, pre_chosen_poi=chosen_poi, manual_spawn=True)

					resp_cont.add_response_container(sub_resp_cont)

		if enemytype not in ewcfg.raid_bosses:
			
			if enemytype in ewcfg.gvs_enemies_gaiaslimeoids:
				response = "**A {} has been planted in {}!!**".format(enemy.name, enemy.gvs_coord)
			elif enemytype in ewcfg.gvs_enemies_shamblers:
				response = "**A {} creeps forward!!** It spawned in {}!".format(enemy.name, enemy.gvs_coord)
			elif enemytype == ewcfg.enemy_type_doubleheadlessdoublehorseman:
				response = "***BEHOLD!!!***  The {} has arrvied to challenge thee! He is of {} slime, and {} in level. Happy Double Halloween, you knuckleheads!".format(enemy.name, enemy.slime, enemy.level)

				if market_data.horseman_deaths >= 1:
					response += "\n***BACK SO SOON, MORTALS? I'M JUST GETTING WARMED UP, BAHAHAHAHAHAHA!!!***"

			elif enemytype == ewcfg.enemy_type_doublehorse:
				response = "***HARK!!!***  Clopping echoes throughout the cave! The {} has arrived with {} slime, and {} levels. And on top of him rides...".format(enemy.name, enemy.slime, enemy.level)

			else:
				response = "**An enemy draws near!!** It's a level {} {}, and has {} slime.".format(enemy.level, enemy.name, enemy.slime)
				if enemytype == ewcfg.enemy_type_sandbag:
					response = "A new {} just got sent in. It's level {}, and has {} slime.\n*'Don't hold back!'*, the Dojo Master cries out from afar.".format(
						enemy.name, enemy.level, enemy.slime)

		ch_name = ewcfg.id_to_poi.get(enemy.poi).channel

	if len(response) > 0 and len(ch_name) > 0:
		resp_cont.add_channel_response(ch_name, response)

	return resp_cont

# Finds an enemy based on its regular/shorthand name, or its ID.
def find_enemy(enemy_search=None, user_data=None):
	enemy_found = None
	enemy_search_alias = None
	

	if enemy_search != None:

		enemy_search_tokens = enemy_search.split(' ')
		enemy_search_tokens_upper = enemy_search.upper().split(' ')

		for enemy_type in ewcfg.enemy_data_table:
			aliases = ewcfg.enemy_data_table[enemy_type]["aliases"]
			if enemy_search.lower() in aliases:
				enemy_search_alias = enemy_type
				break
			if not set(enemy_search_tokens).isdisjoint(set(aliases)):
				enemy_search_alias = enemy_type
				break

		# Check if the identifier letter inputted was a user's captcha. If so, ignore it.
		if user_data.weapon >= 0:
			weapon_item = EwItem(id_item=user_data.weapon)
			weapon = ewcfg.weapon_map.get(weapon_item.item_props.get("weapon_type"))
			captcha = weapon_item.item_props.get('captcha')

			if weapon != None and ewcfg.weapon_class_captcha in weapon.classes and captcha not in [None, ""] and captcha in enemy_search_tokens_upper:
				enemy_search_tokens_upper.remove(captcha)

		tokens_set_upper = set(enemy_search_tokens_upper)
		
		identifiers_found = tokens_set_upper.intersection(set(ewcfg.identifier_letters))
		# coordinates_found = tokens_set_upper.intersection(set(ewcfg.gvs_valid_coords_gaia))

		if len(identifiers_found) > 0:

			# user passed in an identifier for a district specific enemy

			searched_identifier = identifiers_found.pop()

			enemydata = ewutils.execute_sql_query(
				"SELECT {id_enemy} FROM enemies WHERE {poi} = %s AND {identifier} = %s AND {life_state} = 1".format(
					id_enemy=ewcfg.col_id_enemy,
					poi=ewcfg.col_enemy_poi,
					identifier=ewcfg.col_enemy_identifier,
					life_state=ewcfg.col_enemy_life_state
				), (
					user_data.poi,
					searched_identifier,
				))

			for row in enemydata:
				enemy = EwEnemy(id_enemy=row[0], id_server=user_data.id_server)
				enemy_found = enemy
				break
				
		# elif len(coordinates_found) > 0:
		# 	# user passed in a GvS coordinate for a district specific enemy
		# 
		# 	searched_coord= coordinates_found.pop()
		# 
		# 	enemydata = ewutils.execute_sql_query(
		# 		"SELECT {id_enemy} FROM enemies WHERE {poi} = %s AND {coord} = %s AND {life_state} = 1".format(
		# 			id_enemy=ewcfg.col_id_enemy,
		# 			poi=ewcfg.col_enemy_poi,
		# 			coord=ewcfg.col_enemy_gvs_coord,
		# 			life_state=ewcfg.col_enemy_life_state
		# 		), (
		# 			user_data.poi,
		# 			searched_coord,
		# 		))
		# 
		# 	for row in enemydata:
		# 		enemy = EwEnemy(id_enemy=row[0], id_server=user_data.id_server)
		# 		enemy_found = enemy
		# 		break
		else:
			# last token was a string, identify enemy by name

			enemydata = ewutils.execute_sql_query("SELECT {id_enemy} FROM enemies WHERE {poi} = %s AND {life_state} = 1".format(
				id_enemy=ewcfg.col_id_enemy,
				poi=ewcfg.col_enemy_poi,
				life_state=ewcfg.col_enemy_life_state
			), (
				user_data.poi,
			))

			# find the first (i.e. the oldest) item that matches the search
			for row in enemydata:
				enemy = EwEnemy(id_enemy=row[0], id_server=user_data.id_server)
				
				if (enemy.name.lower() == enemy_search) or (enemy.enemytype == enemy_search_alias):
					enemy_found = enemy
					break

				if (enemy.name.lower() in enemy_search) or (enemy.enemytype in enemy_search_tokens):
					enemy_found = enemy
					break


	return enemy_found

# Deletes an enemy the database.
def delete_enemy(enemy_data):
	# print("DEBUG - {} - {} DELETED".format(enemy_data.id_enemy, enemy_data.name))
	enemy_data.clear_allstatuses()
	ewutils.execute_sql_query("DELETE FROM enemies WHERE {id_enemy} = %s".format(
		id_enemy=ewcfg.col_id_enemy
	), (
		enemy_data.id_enemy,
	))
	

# Drops items into the district when an enemy dies.
def drop_enemy_loot(enemy_data, district_data):
	loot_poi = ewcfg.id_to_poi.get(district_data.name)
	loot_resp_cont = ewutils.EwResponseContainer(id_server=enemy_data.id_server)
	response = ""

	item_counter = 0
	loot_multiplier = 1
	
	drop_chance = None
	drop_min = None
	drop_max = None
	drop_range = None
	
	has_dropped_item = False
	drop_table = ewcfg.enemy_drop_tables[enemy_data.enemytype]

	for drop_data_set in drop_table:
		value = None
		for key in drop_data_set.keys():
			value = key
			break
		
		drop_chance = drop_data_set[value][0]
		drop_min = drop_data_set[value][1]
		drop_max = drop_data_set[value][2]
		
		item = ewcfg.item_map.get(value)

		item_type = ewcfg.it_item
		if item != None:
			item_id = item.id_item
			name = item.str_name
	
		# Finds the item if it's an EwFood item.
		if item == None:
			item = ewcfg.food_map.get(value)
			item_type = ewcfg.it_food
			if item != None:
				item_id = item.id_food
				name = item.str_name
	
		# Finds the item if it's an EwCosmeticItem.
		if item == None:
			item = ewcfg.cosmetic_map.get(value)
			item_type = ewcfg.it_cosmetic
			if item != None:
				item_id = item.id_cosmetic
				name = item.str_name
	
		if item == None:
			item = ewcfg.furniture_map.get(value)
			item_type = ewcfg.it_furniture
			if item != None:
				item_id = item.id_furniture
				name = item.str_name
				if item_id in ewcfg.furniture_pony:
					item.vendors = [ewcfg.vendor_bazaar]
	
		if item == None:
			item = ewcfg.weapon_map.get(value)
			item_type = ewcfg.it_weapon
			if item != None:
				item_id = item.id_weapon
				name = item.str_weapon
		
		# Some entries in the drop table aren't item IDs, they're general values for random drops like cosmetics/crops	
		if item == None:
			
			if value == "crop":
				item = random.choice(ewcfg.vegetable_list)
				item_type = ewcfg.it_food
			
			elif value in [ewcfg.rarity_plebeian, ewcfg.rarity_patrician]:
				item_type = ewcfg.it_cosmetic

				cosmetics_list = []
				for result in ewcfg.cosmetic_items_list:
					if result.ingredients == "":
						cosmetics_list.append(result)
					else:
						pass
				
				if value == ewcfg.rarity_plebeian:
					items = []
	
					for cosmetic in cosmetics_list:
						if cosmetic.rarity == ewcfg.rarity_plebeian:
							items.append(cosmetic)
	
					item = items[random.randint(0, len(items) - 1)]
				elif value == ewcfg.rarity_patrician:
					items = []
	
					for cosmetic in cosmetics_list:
						if cosmetic.rarity == ewcfg.rarity_plebeian:
							items.append(cosmetic)
	
					item = items[random.randint(0, len(items) - 1)]

		if item != None:

			item_dropped = random.randrange(100) <= (drop_chance - 1)
			if item_dropped:
				has_dropped_item = True
				
				drop_range = list(range(drop_min, drop_max + 1))
				item_amount = random.choice(drop_range)

				if enemy_data.rare_status == 1:
					loot_multiplier *= 1.5

				if enemy_data.enemytype == ewcfg.enemy_type_unnervingfightingoperator:
					loot_multiplier *= math.ceil(enemy_data.slime / 1000000)
					
				item_amount = math.ceil(item_amount * loot_multiplier)
			else:
				item_amount = 0
				
			for i in range(item_amount):

				item_props = ewitem.gen_item_props(item)
	
				generated_item_id = ewitem.item_create(
					item_type=item_type,
					id_user=enemy_data.poi,
					id_server=enemy_data.id_server,
					stack_max= -1,
					stack_size= 0,
					item_props=item_props
				)

				response = "They dropped a {item_name}!".format(item_name=item.str_name)
				loot_resp_cont.add_channel_response(loot_poi.channel, response)

		else:
			ewutils.logMsg("ERROR: COULD NOT DROP ITEM WITH VALUE '{}'".format(value))
	if not has_dropped_item:
		response = "They didn't drop anything...\n"
		loot_resp_cont.add_channel_response(loot_poi.channel, response)

	return loot_resp_cont

# Determines what level an enemy is based on their slime count.
def level_byslime(slime):
	return int(abs(slime) ** 0.25)
		

# Check if an enemy is dead. Implemented to prevent enemy data from being recreated when not necessary.
def check_death(enemy_data):
	if enemy_data.slime <= 0 or enemy_data.life_state == ewcfg.enemy_lifestate_dead:
		# delete_enemy(enemy_data)
		return True
	else:
		return False

# Assigns enemies most of their necessary attributes based on their type.
def get_enemy_data(enemy_type):
	enemy = EwEnemy()
	
	rare_status = 0
	if random.randrange(5) == 0 and enemy_type not in ewcfg.overkill_enemies and enemy_type not in ewcfg.gvs_enemies:
		rare_status = 1

	enemy.id_server = -1
	enemy.slime = 0
	enemy.totaldamage = 0
	enemy.level = 0
	enemy.life_state = ewcfg.enemy_lifestate_alive
	enemy.enemytype = enemy_type
	enemy.bleed_storage = 0
	enemy.time_lastenter = 0
	enemy.initialslimes = 0
	enemy.id_target = -1
	enemy.raidtimer = 0
	enemy.rare_status = rare_status
		
	if enemy_type in ewcfg.raid_bosses:
		enemy.life_state = ewcfg.enemy_lifestate_unactivated
		enemy.raidtimer = int(time.time())

	slimetable = ewcfg.enemy_data_table[enemy_type]["slimerange"]
	minslime = slimetable[0]
	maxslime = slimetable[1]

	slime = random.randrange(minslime, (maxslime + 1))
	
	enemy.slime = slime
	enemy.ai = ewcfg.enemy_data_table[enemy_type]["ai"]
	enemy.name = ewcfg.enemy_data_table[enemy_type]["displayname"]
	enemy.attacktype = ewcfg.enemy_data_table[enemy_type]["attacktype"]
	
	try:
		enemy.enemyclass = ewcfg.enemy_data_table[enemy_type]["class"]
	except:
		enemy.enemyclass = ewcfg.enemy_class_normal
		
	if rare_status == 1:
		enemy.name = ewcfg.enemy_data_table[enemy_type]["raredisplayname"]
		enemy.slime *= 2

	return enemy


# Selects which non-ghost user to attack based on certain parameters.
def get_target_by_ai(enemy_data, cannibalize = False):

	target_data = None
	group_attack = False

	time_now = int(time.time())

	# If a player's time_lastenter is less than this value, it can be attacked.
	targettimer = time_now - ewcfg.time_enemyaggro
	raidbossaggrotimer = time_now - ewcfg.time_raidbossaggro

	if not cannibalize:
		if enemy_data.ai == ewcfg.enemy_ai_defender:
			if enemy_data.id_target != -1:
				target_data = EwPlayer(id_user=enemy_data.id_target, id_server=enemy_data.id_server, data_level = 1)
	
		elif enemy_data.ai == ewcfg.enemy_ai_attacker_a:
			users = ewutils.execute_sql_query(
				"SELECT {id_user}, {life_state}, {time_lastenter} FROM users WHERE {poi} = %s AND {id_server} = %s AND {time_lastenter} < {targettimer} AND ({level} > {safe_level} OR {life_state} != {life_state_juvenile}) AND NOT ({life_state} = {life_state_corpse} OR {life_state} = {life_state_kingpin} OR {id_user} IN (SELECT {id_user} FROM status_effects WHERE id_status = '{repel_status}')) ORDER BY {time_lastenter} ASC".format(
					id_user = ewcfg.col_id_user,
					life_state = ewcfg.col_life_state,
					time_lastenter = ewcfg.col_time_lastenter,
					poi = ewcfg.col_poi,
					id_server = ewcfg.col_id_server,
					targettimer = targettimer,
					life_state_corpse = ewcfg.life_state_corpse,
					life_state_kingpin = ewcfg.life_state_kingpin,
					life_state_juvenile = ewcfg.life_state_juvenile,
					repel_status = ewcfg.status_repelled_id,
					slimes = ewcfg.col_slimes,
					safe_level = ewcfg.max_safe_level,
					level = ewcfg.col_slimelevel
				), (
					enemy_data.poi,
					enemy_data.id_server
				))
			if len(users) > 0:
				target_data = EwPlayer(id_user=users[0][0], id_server=enemy_data.id_server, data_level = 1)
	
		elif enemy_data.ai == ewcfg.enemy_ai_attacker_b:
			users = ewutils.execute_sql_query(
				"SELECT {id_user}, {life_state}, {slimes} FROM users WHERE {poi} = %s AND {id_server} = %s AND {time_lastenter} < {targettimer} AND ({level} > {safe_level} OR {life_state} != {life_state_juvenile}) AND NOT ({life_state} = {life_state_corpse} OR {life_state} = {life_state_kingpin} OR {id_user} IN (SELECT {id_user} FROM status_effects WHERE id_status = '{repel_status}')) ORDER BY {slimes} DESC".format(
					id_user = ewcfg.col_id_user,
					life_state = ewcfg.col_life_state,
					slimes = ewcfg.col_slimes,
					poi = ewcfg.col_poi,
					id_server = ewcfg.col_id_server,
					time_lastenter = ewcfg.col_time_lastenter,
					targettimer = targettimer,
					life_state_corpse = ewcfg.life_state_corpse,
					life_state_kingpin = ewcfg.life_state_kingpin,
					life_state_juvenile = ewcfg.life_state_juvenile,
					repel_status = ewcfg.status_repelled_id,
					safe_level = ewcfg.max_safe_level,
					level = ewcfg.col_slimelevel
				), (
					enemy_data.poi,
					enemy_data.id_server
				))
			if len(users) > 0:
				target_data = EwPlayer(id_user=users[0][0], id_server=enemy_data.id_server, data_level = 1)
				
		elif enemy_data.ai == ewcfg.enemy_ai_gaiaslimeoid:
			
			users = ewutils.execute_sql_query(
				"SELECT {id_user}, {life_state}, {slimes} FROM users WHERE {poi} = %s AND {id_server} = %s AND {time_lastenter} < {targettimer} AND ({life_state} = {life_state_shambler}) ORDER BY {slimes} DESC".format(
					id_user=ewcfg.col_id_user,
					life_state=ewcfg.col_life_state,
					slimes=ewcfg.col_slimes,
					poi=ewcfg.col_poi,
					id_server=ewcfg.col_id_server,
					time_lastenter=ewcfg.col_time_lastenter,
					targettimer=targettimer,
					life_state_shambler=ewcfg.life_state_shambler,
					time_now=time_now,
				), (
					enemy_data.poi,
					enemy_data.id_server
				))
			if len(users) > 0:
				target_data = EwPlayer(id_user=users[0][0], id_server=enemy_data.id_server, data_level=1)
				
		elif enemy_data.ai == ewcfg.enemy_ai_shambler:

			users = ewutils.execute_sql_query(
				"SELECT {id_user}, {life_state}, {slimes} FROM users WHERE {poi} = %s AND {id_server} = %s AND {time_lastenter} < {targettimer} AND NOT ({life_state} = {life_state_shambler} OR {life_state} = {life_state_corpse} OR {life_state} = {life_state_kingpin}) ORDER BY {slimes} DESC".format(
					id_user=ewcfg.col_id_user,
					life_state=ewcfg.col_life_state,
					slimes=ewcfg.col_slimes,
					poi=ewcfg.col_poi,
					id_server=ewcfg.col_id_server,
					time_lastenter=ewcfg.col_time_lastenter,
					targettimer=targettimer,
					life_state_shambler=ewcfg.life_state_shambler,
					life_state_corpse=ewcfg.life_state_corpse,
					life_state_kingpin=ewcfg.life_state_kingpin,
				), (
					enemy_data.poi,
					enemy_data.id_server
				))
			if len(users) > 0:
				target_data = EwPlayer(id_user=users[0][0], id_server=enemy_data.id_server, data_level=1)
				
		# If an enemy is a raidboss, don't let it attack until some time has passed when entering a new district.
		if enemy_data.enemytype in ewcfg.raid_bosses and enemy_data.time_lastenter > raidbossaggrotimer:
			target_data = None
			
	elif cannibalize:
		if enemy_data.ai == ewcfg.enemy_ai_gaiaslimeoid:
			
			range = 1 if enemy_data.enemy_props.get('range') == None else int(enemy_data.enemy_props.get('range'))
			direction = 'right' if enemy_data.enemy_props.get('direction') == None else enemy_data.enemy_props.get('direction')
			piercing = 'false' if enemy_data.enemy_props.get('piercing') == None else enemy_data.enemy_props.get('piercing')
			splash = 'false' if enemy_data.enemy_props.get('splash') == None else enemy_data.enemy_props.get('splash')
			pierceamount = '0' if enemy_data.enemy_props.get('pierceamount') == None else enemy_data.enemy_props.get('pierceamount')
			singletilepierce = 'false' if enemy_data.enemy_props.get('singletilepierce') == None else enemy_data.enemy_props.get('singletilepierce')
			
			enemies = ga_check_coord_for_shambler(enemy_data, range, direction, piercing, splash, pierceamount, singletilepierce)
			if len(enemies) > 1:
				group_attack = True
				
			target_data = enemies
				
		elif enemy_data.ai == ewcfg.enemy_ai_shambler:
			range = 1 if enemy_data.enemy_props.get('range') == None else int(enemy_data.enemy_props.get('range'))
			direction = 'left' if enemy_data.enemy_props.get('direction') == None else enemy_data.enemy_props.get('direction')
			
			enemies = sh_check_coord_for_gaia(enemy_data, range, direction)
			if len(enemies) > 0:
				target_data = EwEnemy(id_enemy=enemies[0], id_server=enemy_data.id_server)
		
		# If an enemy is a raidboss, don't let it attack until some time has passed when entering a new district.
		if enemy_data.enemytype in ewcfg.raid_bosses and enemy_data.time_lastenter > raidbossaggrotimer:
			target_data = None

	return target_data, group_attack

# Check if raidboss is ready to attack / be attacked
def check_raidboss_countdown(enemy_data):
	time_now = int(time.time())

	# Wait for raid bosses
	if enemy_data.enemytype in ewcfg.raid_bosses and enemy_data.raidtimer <= time_now - ewcfg.time_raidcountdown:
		# Raid boss has activated!
		return True
	elif enemy_data.enemytype in ewcfg.raid_bosses and enemy_data.raidtimer > time_now - ewcfg.time_raidcountdown:
		# Raid boss hasn't activated.
		return False

def check_raidboss_movecooldown(enemy_data):
	time_now = int(time.time())
	
	if enemy_data.enemytype in ewcfg.raid_bosses:
		if enemy_data.enemytype in ewcfg.gvs_enemies:
			if enemy_data.time_lastenter <= time_now - 600:
				# Raid boss can move
				return True
			elif enemy_data.time_lastenter > time_now - 600:
				# Raid boss can't move yet
				return False
		else:
			if enemy_data.time_lastenter <= time_now - ewcfg.time_raidboss_movecooldown:
				# Raid boss can move
				return True
			elif enemy_data.time_lastenter > time_now - ewcfg.time_raidboss_movecooldown:
				# Raid boss can't move yet
				return False

# Gives enemy an identifier so it's easier to pick out in a crowd of enemies
def set_identifier(poi, id_server):
	
	district = EwDistrict(district=poi, id_server=id_server)
	enemies_list = district.get_enemies_in_district()

	# A list of identifiers from enemies in a district
	enemy_identifiers = []

	new_identifier = ewcfg.identifier_letters[0]

	if len(enemies_list) > 0:
		for enemy_id in enemies_list:
			enemy = EwEnemy(id_enemy=enemy_id)
			enemy_identifiers.append(enemy.identifier)

		# Sort the list of identifiers alphabetically
		enemy_identifiers.sort()

		for checked_enemy_identifier in enemy_identifiers:
			# If the new identifier matches one from the list of enemy identifiers, give it the next applicable letter
			# Repeat until a unique identifier is given
			if new_identifier == checked_enemy_identifier:
				next_letter = (ewcfg.identifier_letters.index(checked_enemy_identifier) + 1)
				new_identifier = ewcfg.identifier_letters[next_letter]
			else:
				continue

	return new_identifier

async def sh_move(enemy_data):
	current_coord = enemy_data.gvs_coord
	has_moved = False
	index = None
	row = None
	new_coord = None

	if current_coord in ewcfg.gvs_coords_start and enemy_data.enemytype == ewcfg.enemy_type_juvieshambler:
		delete_enemy(enemy_data)
	
	if current_coord not in ewcfg.gvs_coords_end:
		for row in ewcfg.gvs_valid_coords_shambler:

			if current_coord in row:
				index = row.index(current_coord)
				new_coord = row[index - 1]
				# print(new_coord)
				break
				
		if new_coord == None:
			return
				
		enemy_data.gvs_coord = new_coord
		enemy_data.persist()
		
		for gaia_row in ewcfg.gvs_valid_coords_gaia:
			if new_coord in gaia_row and index != None and row != None:
				poi_channel = ewcfg.id_to_poi.get(enemy_data.poi).channel
				
				try:
					previous_gaia_coord = row[index - 2]
				except:
					break
					
				response = "The {} moved from {} to {}!".format(enemy_data.name, new_coord, previous_gaia_coord)
				client = ewutils.get_client()
				server = client.get_guild(enemy_data.id_server)
				channel = ewutils.get_channel(server, poi_channel)
				
				await ewutils.send_message(client, channel, response)

		# print('shambler moved from {} to {} in {}.'.format(current_coord, new_coord, enemy_data.poi))


	return has_moved

def sh_check_coord_for_gaia(enemy_data, sh_range, direction):
	current_coord = enemy_data.gvs_coord
	gaias_in_coord = []

	if current_coord not in ewcfg.gvs_coords_end:
		
		for sh_row in ewcfg.gvs_valid_coords_shambler:

			if current_coord in sh_row:
				index = sh_row.index(current_coord)
				checked_coord = gvs_grid_gather_coords(enemy_data.enemyclass, sh_range, direction, sh_row, index)[0]

				for gaia_row in ewcfg.gvs_valid_coords_gaia:
					if checked_coord in gaia_row:
						# Check coordinate for gaiaslimeoids in front of the shambler.
						gaia_data = ewutils.execute_sql_query(
							"SELECT {id_enemy}, {enemytype} FROM enemies WHERE {enemyclass} = %s AND {gvs_coord} = %s AND {poi} = %s AND {id_server} = %s AND NOT ({life_state} = {life_state_dead})".format(
								id_enemy=ewcfg.col_id_enemy,
								enemyclass=ewcfg.col_enemy_class,
								enemytype=ewcfg.col_enemy_type,
								gvs_coord=ewcfg.col_enemy_gvs_coord,
								poi=ewcfg.col_poi,
								id_server=ewcfg.col_id_server,
								life_state=ewcfg.col_life_state,
								life_state_dead=ewcfg.enemy_lifestate_dead,
							), (
								ewcfg.enemy_class_gaiaslimeoid,
								checked_coord,
								enemy_data.poi,
								enemy_data.id_server
							))
						
						#print(len(gaia_data))
						if len(gaia_data) > 0:
							
							low_attack_priority = [ewcfg.enemy_type_gaia_rustealeaves]
							high_attack_priority = [ewcfg.enemy_type_gaia_steelbeans]
							mid_attack_priority = []
							for enemy_id in ewcfg.gvs_enemies_gaiaslimeoids:
								if enemy_id not in low_attack_priority and enemy_id not in high_attack_priority:
									mid_attack_priority.append(enemy_id)
							
							gaia_types = {}
							for gaia in gaia_data:
								gaia_types[gaia[1]] = gaia[0]
							
							# Rustea Leaves only have a few opposing shamblers that can damage them
							if ewcfg.enemy_type_gaia_rustealeaves in gaia_types.keys() and enemy_data.enemytype not in [ewcfg.enemy_type_gigashambler, ewcfg.enemy_type_shambonidriver, ewcfg.enemy_type_ufoshambler]:
								del gaia_types[ewcfg.enemy_type_gaia_rustealeaves]

							for target in high_attack_priority:
								if target in gaia_types.keys():
									gaias_in_coord.append(gaia_types[target])
									
							for target in mid_attack_priority:
								if target in gaia_types.keys():
									gaias_in_coord.append(gaia_types[target])
									
							for target in low_attack_priority:
								if target in gaia_types.keys():
									gaias_in_coord.append(gaia_types[target])

							# print('shambler in coord {} found gaia in coord {} in {}.'.format(current_coord, checked_coord, enemy_data.poi))
	
	return gaias_in_coord

def ga_check_coord_for_shambler(enemy_data, ga_range, direction, piercing, splash, pierceamount, singletilepierce):
	current_coord = enemy_data.gvs_coord
	detected_shamblers = {}
	
	for sh_row in ewcfg.gvs_valid_coords_shambler:

		if current_coord in sh_row:
			index = sh_row.index(current_coord)
			checked_coords = gvs_grid_gather_coords(enemy_data.enemyclass, int(ga_range), direction, sh_row, index)
			
			# print('GAIA -- CHECKED COORDS FOR {} WITH ID {}: {}'.format(enemy_data.enemytype, enemy_data.id_enemy, checked_coords))

			
			# Check coordinate for shamblers in range of gaiaslimeoid.
			shambler_data = ewutils.execute_sql_query(
				"SELECT {id_enemy}, {enemytype} FROM enemies WHERE {enemyclass} = %s AND {gvs_coord} IN %s AND {poi} = %s AND {id_server} = %s AND NOT ({life_state} = {life_state_dead} OR {life_state} = {life_state_unactivated})".format(
					id_enemy=ewcfg.col_id_enemy,
					enemyclass=ewcfg.col_enemy_class,
					enemytype=ewcfg.col_enemy_type,
					gvs_coord=ewcfg.col_enemy_gvs_coord,
					poi=ewcfg.col_poi,
					id_server=ewcfg.col_id_server,
					life_state=ewcfg.col_life_state,
					life_state_dead=ewcfg.enemy_lifestate_dead,
					life_state_unactivated=ewcfg.enemy_lifestate_unactivated,
				), (
					ewcfg.enemy_class_shambler,
					tuple(checked_coords),
					enemy_data.poi,
					enemy_data.id_server
				))

			#print(len(shambler_data))
			if len(shambler_data) > 0:

				for shambler in shambler_data:

					current_shambler_data = EwEnemy(id_enemy=shambler[0], id_server=enemy_data.id_server)
					detected_shamblers[current_shambler_data.id_enemy] = current_shambler_data.gvs_coord

					if shambler[1] in [ewcfg.enemy_type_juvieshambler] and current_shambler_data.enemy_props.get('underground') == 'true':
						del detected_shamblers[current_shambler_data.id_enemy]

				if piercing == 'false':
					detected_shamblers = gvs_find_nearest_shambler(checked_coords, detected_shamblers)
				elif int(pierceamount) > 0:
					detected_shamblers = gvs_find_nearest_shambler(checked_coords, detected_shamblers, pierceamount, singletilepierce)
				
				# print('gaia in coord {} found shambler in coords {} in {}.'.format(current_coord, checked_coords, enemy_data.poi))

			if splash == 'true':
				
				if detected_shamblers == {}:
					checked_splash_coords = checked_coords
				else:
					checked_splash_coords = []
					for shambler in detected_shamblers.keys():
						checked_splash_coords.append(detected_shamblers[shambler])
				
				splash_coords = gvs_get_splash_coords(checked_splash_coords)

				splash_shambler_data = ewutils.execute_sql_query(
					"SELECT {id_enemy}, {enemytype}, {gvs_coord} FROM enemies WHERE {enemyclass} = %s AND {gvs_coord} IN %s AND {poi} = %s AND {id_server} = %s".format(
						id_enemy=ewcfg.col_id_enemy,
						enemyclass=ewcfg.col_enemy_class,
						enemytype=ewcfg.col_enemy_type,
						gvs_coord=ewcfg.col_enemy_gvs_coord,
						poi=ewcfg.col_poi,
						id_server=ewcfg.col_id_server,
					), (
						ewcfg.enemy_class_shambler,
						tuple(splash_coords),
						enemy_data.poi,
						enemy_data.id_server
					))
				
				for splashed_shambler in splash_shambler_data:
					detected_shamblers[splashed_shambler[0]] = splashed_shambler[2]			
			break

	return detected_shamblers

def gvs_grid_gather_coords(enemyclass, gr_range, direction, row, index):
	checked_coords = []
	
	if enemyclass == ewcfg.enemy_class_shambler:
		index_change = -2
		if direction == 'right':
			index_change *= -1
			
		try:
			checked_coords.append(row[index + index_change])
		except:
			pass
		
	else:
		
		index_changes = []
		
		# Default if range is 1, only reaches 0.5 and 1 full tile ahead
		for i in range(gr_range):
			index_changes.append(i + 1)
			
		# If it reaches backwards with a range of 1, reflect current index changes
		if direction == 'left':
			new_index_changes = []
			
			for change in index_changes:
				change *= -1
				new_index_changes.append(change)
				
			index_changes = new_index_changes
			
		# If it reaches both directions with a range of 1, add in opposite tiles.
		elif direction == 'frontandback':
			new_index_changes = []
			
			for change in index_changes:
				change *= -1
				new_index_changes.append(change)

			index_changes += new_index_changes
			
		# If it attacks in a ring formation around itself, there are no coord changes.
		# The proper coordinates will be fetched later as 'splash' damage.
		elif direction == 'ring':
			index_changes = [0]
			
		# Catch exceptions when necessary
		for index_change in index_changes:
			try:
				checked_coords.append(row[index + index_change])
			except:
				pass
	
		# print(index_changes)
		
	# print(gr_range)
	# print(checked_coords)
	# print(enemyclass)
	
	return checked_coords

def gvs_find_nearest_shambler(checked_coords, detected_shamblers, pierceamount = 1, singletilepierce = 'false'):
	pierceattempts = 0
	current_dict = {}
	chosen_coord = ''
	
	for coord in checked_coords:
		for shambler in detected_shamblers.keys():
			if detected_shamblers[shambler] == coord:
				current_dict[shambler] = coord
				
				if singletilepierce == 'true':
					chosen_coord = coord
					for shambler in detected_shamblers.keys():
						if detected_shamblers[shambler] == chosen_coord:
							current_dict[shambler] = chosen_coord
						pierceattempts += 1
						if pierceattempts == pierceamount:
							return current_dict
					
			pierceattempts += 1
			if pierceattempts == pierceamount:
				return current_dict
			
def gvs_get_splash_coords(checked_splash_coords):
	# Grab any random coordinate from the supplied splash coordinates, then get the row that it's in.
	plucked_coord = checked_splash_coords[0]
	plucked_row = plucked_coord[0]
	top_row = None
	middle_row = None
	bottom_row = None
	
	extra_top_row = None # Joybean Pawpaw
	extra_bottom_row = None # Joybean Pawpaw
	row_range = 5 # Joybean Dankwheat = 9
	row_backpedal = 2 # Joybean Dankwheat = 4
	
	current_index = 0
	
	all_splash_coords = []
	if plucked_row == 'A':
		middle_row = 0
		bottom_row = 1
	elif plucked_row == 'B':
		top_row = 0
		middle_row = 1
		bottom_row = 2
	elif plucked_row == 'C':
		top_row = 1
		middle_row = 2
		bottom_row = 3
	elif plucked_row == 'D':
		top_row = 2
		middle_row = 3
		bottom_row = 4
	elif plucked_row == 'E':
		top_row = 3
		middle_row = 4
	
	for coord in checked_splash_coords:
		for sh_row in ewcfg.gvs_valid_coords_shambler:
			if coord in sh_row:
				current_index = sh_row.index(coord)
				break
		
		if top_row != None:
			for i in range(row_range):
				try:
					all_splash_coords.append(ewcfg.gvs_valid_coords_shambler[top_row][current_index - row_backpedal + i])
				except:
					pass
		if bottom_row != None:
			for i in range(row_range):
				try:
					all_splash_coords.append(ewcfg.gvs_valid_coords_shambler[bottom_row][current_index - row_backpedal + i])
				except:
					pass
				
		for i in range(row_range):
			try:
				all_splash_coords.append(ewcfg.gvs_valid_coords_shambler[middle_row][current_index - row_backpedal + i])
			except:
				pass
			
	return all_splash_coords

# This function takes care of all win conditions within Gankers Vs. Shamblers.
# It also handles turn counters, including gaiaslime generation, as well as spawning in shamblers
async def gvs_update_gamestate(id_server):
	
	op_districts = ewutils.execute_sql_query("SELECT district FROM gvs_ops_choices GROUP BY district")
	for op_district in op_districts:
		district = op_district[0]
		
		graveyard_ops = ewutils.execute_sql_query("SELECT id_user, enemytype, shambler_stock FROM gvs_ops_choices WHERE faction = 'shamblers' AND district = '{}' AND shambler_stock > 0".format(district))
		bot_garden_ops = ewutils.execute_sql_query("SELECT id_user, enemytype FROM gvs_ops_choices WHERE faction = 'gankers' AND district = '{}' AND id_user = 56709".format(district))
		op_district_data = EwDistrict(district=district, id_server=id_server)

		# Generate Gaiaslime passively over time, but in small amounts
		op_district_data.gaiaslime += 5
		op_district_data.persist()
		
		victor = None
		time_now = int(time.time())

		op_poi = ewcfg.id_to_poi.get(district)
		client = ewutils.get_client()
		server = client.get_guild(id_server)
		channel = ewutils.get_channel(server, op_poi.channel)
		
		if len(bot_garden_ops) > 0:
			if random.randrange(25) == 0:
			
				# random_op = random.choice(bot_garden_ops)
				# random_op_data = EwOperationData(id_user=random_op[0], district=district, enemytype=random_op[1])
	
				possible_bot_types = [
					ewcfg.enemy_type_gaia_suganmanuts,
					ewcfg.enemy_type_gaia_pinkrowddishes,
					ewcfg.enemy_type_gaia_purplekilliflower,
					ewcfg.enemy_type_gaia_poketubers,
					ewcfg.enemy_type_gaia_razornuts
				]
				
				possible_bot_coords = [
					'A1', 'A2', 'A3', 'A4', 'A5',
					'B1', 'B2', 'B3', 'B4', 'B5',
					'C1', 'C2', 'C3', 'C4', 'C5',
					'D1', 'D2', 'D3', 'D4', 'D5',
					'E1', 'E2', 'E3', 'E4', 'E5'
				]
				
				for i in range(5):
					chosen_type = random.choice(possible_bot_types)
					chosen_coord = random.choice(possible_bot_coords)
				
					existing_gaias = ewutils.gvs_get_gaias_from_coord(district, chosen_coord)
				
					# If the coordinate is completely empty, spawn a gaiaslimeoid there.
					# Otherwise, make up to 5 attempts when choosing random coordinates
					if len(existing_gaias) == 0:
						resp_cont = spawn_enemy(
							id_server=id_server,
							pre_chosen_type=chosen_type,
							pre_chosen_level=50,
							pre_chosen_poi=district,
							pre_chosen_identifier='',
							pre_chosen_faction=ewcfg.psuedo_faction_gankers,
							pre_chosen_owner=56709,
							pre_chosen_coord=chosen_coord,
							manual_spawn=True,
						)
						await resp_cont.post()
						
						break
					

		if len(graveyard_ops) > 0:

			# The chance for a shambler to spawn is inversely proportional to the amount of shamblers left in stock
			# The less shamblers there are left, the more likely they are to spawn
			current_stock = 0
			full_stock = 0
			
			for op in graveyard_ops:
				current_stock += op[2]
				full_stock += ewcfg.tombstone_fullstock_map[op[1]]
				
			# Example: If full_stock is 50, and current_stock is 20, then the spawn chance is 70%
			# ((1 - (20 / 50)) * 100) + 10 = 70

			shambler_spawn_chance = int(((1 - (current_stock / full_stock)) * 100) + 10)
			if random.randrange(100) + 1 < shambler_spawn_chance:

				random_op = random.choice(graveyard_ops)
				random_op_data = EwOperationData(id_user=random_op[0], district=district, enemytype=random_op[1])
				
				# Don't spawn if there aren't available identifiers
				if len(op_district_data.get_enemies_in_district(classes = [ewcfg.enemy_class_shambler])) < 26:
					resp_cont = spawn_enemy(
						id_server=id_server,
						pre_chosen_type=random_op_data.enemytype,
						pre_chosen_level=50,
						pre_chosen_poi=district,
						pre_chosen_faction=ewcfg.psuedo_faction_shamblers,
						pre_chosen_owner=random_op_data.id_user,
						pre_chosen_coord=random.choice(ewcfg.gvs_coords_start),
						manual_spawn=True
					)
					
					random_op_data.shambler_stock -= 1
					random_op_data.persist()
					
					if random_op_data.shambler_stock == 0:
						breakdown_response = "The tombstone spawning in {}s breaks down and collapses!".format(random_op_data.enemytype.capitalize())
						resp_cont.add_channel_response(channel, breakdown_response)
					else:
						random_op_data.persist()
						
					await resp_cont.post()
		else:
			shamblers = ewutils.execute_sql_query("SELECT id_enemy FROM enemies WHERE enemyclass = '{}' AND poi = '{}'".format(ewcfg.enemy_class_shambler, district))
			if len(shamblers) == 0:
				# No more stocked tombstones, and no more enemy shamblers. Garden Gankers win!
				victor = ewcfg.psuedo_faction_gankers
				
		op_juvies = ewutils.execute_sql_query("SELECT id_user FROM gvs_ops_choices WHERE faction = 'gankers' AND district = '{}' AND id_user != 56709 GROUP BY id_user".format(district))
		
		# No more Garden Gankers left. Shamblers win?
		if len(op_juvies) == 0:
			
			# Check if the shamblers are fighting against the bot.
			# If they are, they can only win if at least one shambler has reached the back.
			if len(bot_garden_ops) > 0:
				back_shamblers = ewutils.execute_sql_query("SELECT id_enemy FROM enemies WHERE gvs_coord IN {}".format(tuple(ewcfg.gvs_coords_end)))
				if len(back_shamblers) > 0:
					# Shambler reached the back while no juveniles were around to help the bot. Shamblers win!
					victor = ewcfg.psuedo_faction_shamblers
			else:
				# No juveniles left in the district, and there were no bot operations. Shamblers win!
				victor = ewcfg.psuedo_faction_shamblers
		
		all_garden_ops = ewutils.execute_sql_query("SELECT id_user FROM gvs_ops_choices WHERE faction = 'gankers' AND district = '{}'".format(district))
		# No garden ops at all. Shamblers win!
		if len(all_garden_ops) == 0:
			victor = ewcfg.psuedo_faction_shamblers
				
		if victor != None:
			if victor == ewcfg.psuedo_faction_gankers:
				response = "***All tombstones have been emptied out! The Garden Gankers take victory!\nThe district is rejuvenated completely!!***"
				
				for juvie in op_juvies:
					ewutils.active_restrictions[juvie[0]] = 0 
				
				op_district_data.gaiaslime = 0
				op_district_data.degradation = 0
				op_district_data.time_unlock = time_now + 3600
				op_district_data.persist()
			else:
				response = "***The shamblers have eaten the brainz of the Garden Gankers and take control of the district!\nIt's shambled completely!!***"
				op_district_data.gaiaslime = 0
				op_district_data.degradation = ewcfg.district_max_degradation
				op_district_data.time_unlock = time_now + 3600
				op_district_data.persist()

			ewutils.execute_sql_query("DELETE FROM gvs_ops_choices WHERE district = '{}'".format(district))			
			await delete_all_enemies(cmd=None, query_suffix="AND poi = '{}'".format(district), id_server_sent=id_server)
			return await ewutils.send_message(client, channel, response)

# Certain conditions may prevent a shambler from acting.
def check_enemy_can_act(enemy_data):
	
	enemy_props = enemy_data.enemy_props
	
	turn_countdown = enemy_props.get('turncountdown')
	dank_countdown = enemy_props.get('dankcountdown')
	sludge_countdown = enemy_props.get('sludgecountdown')
	hardened_sludge_countdown = enemy_props.get('hardsludgecountdown')
	
	waiting = False
	stoned = False
	sludged = False
	hardened = False
	
	if turn_countdown != None:
		if int(turn_countdown) > 0:
			waiting = True
			enemy_props['turncountdown'] -= 1
		else:
			waiting = False
		
	if dank_countdown != None:
		if int(dank_countdown) > 0:
			# If the countdown number is even, they can act. Otherwise, they cannot.
			if dank_countdown % 2 == 0:
				stoned = False
			else:
				stoned = True
			
			enemy_props['dankcountdown'] -= 1
		else:
			stoned = False
		
	# Regular sludge only slows a shambler down every other turn. Hardened sludge immobilizes them completely.
	if sludge_countdown != None:
		if int(sludge_countdown) > 0:
			# If the countdown number is even, they can act. Otherwise, they cannot.
			if sludge_countdown % 2 == 0:
				sludged = False
			else:
				sludged = True

			enemy_props['sludgecountdown'] -= 1
		else:
			sludged = False

	if hardened_sludge_countdown != None:
		if int(hardened_sludge_countdown) > 0:
			hardened = True
			enemy_props['hardsludgecountdown'] -= 1
		else:
			hardened = False
	
	enemy_data.persist()
	
	if not waiting and not stoned and not sludged and not hardened:
		return True
	else:
		return False

def handle_turn_timers(enemy_data):
	response = ""
	
	# Handle specific turn counters of all GvS enemies.
	if enemy_data.enemytype == ewcfg.enemy_type_gaia_brightshade:
		countdown = enemy_data.enemy_props.get('gaiaslimecountdown')

		if countdown != None:
			int_countdown = int(countdown)

			if int_countdown == 0:

				gaiaslime_amount = 0
				
				enemy_data.enemy_props['gaiaslimecountdown'] = 2
				district_data = EwDistrict(district=enemy_data.poi, id_server=enemy_data.id_server)

				if enemy_data.enemy_props.get('joybean') != None:
					if enemy_data.enemy_props.get('joybean') == 'true':
						gaiaslime_amount = 50
					else:
						gaiaslime_amount = 25
				else:
					gaiaslime_amount = 25
					
				district_data.gaiaslime += gaiaslime_amount
				district_data.persist()
				
				response = "{} ({}) produced {} gaiaslime!".format(enemy_data.name, enemy_data.gvs_coord, gaiaslime_amount)

			else:
				enemy_data.enemy_props['gaiaslimecountdown'] = int_countdown - 1

			enemy_data.persist()
			return response

	elif enemy_data.enemytype == ewcfg.enemy_type_gaia_poketubers:
		
		countdown = enemy_data.enemy_props.get('primecountdown')
		
		if countdown != None:
			int_countdown = int(countdown)
		
			if enemy_data.enemy_props.get('primed') != 'true':
	
				if int_countdown == 0:
					enemy_data.enemy_props['primed'] = 'true'
					
					response = "{} ({}) is primed and ready.".format(enemy_data.name, enemy_data.gvs_coord)
					
				else:
					enemy_data.enemy_props['primecountdown'] = int_countdown - 1
	
				enemy_data.persist()
				return response
