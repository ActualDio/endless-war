import time
import random
import asyncio

import ewcfg
import ewutils
import ewmap

from ew import EwPlayer
from ewplayer import EwDiscordUser
from ewdistrict import EwDistrict

		
async def slimeball_tick_loop(id_server):
	global sb_games
	while not ewutils.TERMINATE:
		await slimeball_tick(id_server)
		await asyncio.sleep(ewcfg.slimeball_tick_length)
		

async def slimeball_tick(id_server):
	resp_cont = ewutils.EwResponse(id_server = id_server)

	for id_game in sb_games:
		game = sb_games.get(id_game)
		if game == None:
			continue
		if game.id_server == id_server:
			if len(game.players) > 0:
				for player in game.players:
					resp_cont.add_response_container(player.move())

				resp_cont.add_response_container(game.move_ball())

			else:
				poi_data = ewcfg.id_to_poi.get(game.poi)
				response = "Slimeball game ended with score purple {} : {} pink.".format(game.score_purple, game.score_pink)
				resp_cont.add_channel_response(poi_data.channel, response)
					
				game.kill()

	await resp_cont.post()

def get_starting_position(team):
	coords = []
	if team == "purple":
		coords.append(random.randrange(10, 40))
		coords.append(random.randrange(10, 40))
	elif team == "pink":
		coords.append(random.randrange(60, 90))
		coords.append(random.randrange(10, 40))
	else:
		coords.append(random.randrange(49, 51))
		coords.append(random.randrange(20, 30))

	return coords

def get_coords(tokens):

	coords = []
	for token in tokens:
		if len(coords) == 2:
			break
		try:
			int_token = int(token)
			coords.append(int_token)
		except:
			pass
	
	return coords

async def slimeball(cmd):

	user_data = EwPlayer(member = cmd.message.author)

	if not ewutils.channel_name_is_poi(cmd.message.channel.name):
		response = "You have to go into the city to play Slimeball."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	poi_data = ewcfg.id_to_poi.get(user_data.poi)

	if poi_data.id_poi != ewcfg.poi_id_vandalpark:
		response = "You have to go Vandal Park to play {}.".format(cmd.cmd[1:])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if poi_data.is_subzone or poi_data.is_transport:
		response = "This place is too cramped for playing {}. Go outside!".format(cmd.cmd[1:])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	district_data = EwDistrict(district = poi_data.id_poi, id_server = cmd.message.guild.id)

	global sb_userid_to_player
	slimeball_player = sb_userid_to_player.get(cmd.message.author.id)
	
	game_data = None

	if slimeball_player != None:
		global sb_games
		game_data = sb_games.get(slimeball_player.id_game)

		if game_data != None and game_data.poi != poi_data.id_poi:
			game_data.players.remove(slimeball_player)
			game_data = None

	if game_data == None:
		global sb_idserver_to_gamemap
		
		gamemap = sb_idserver_to_gamemap.get(cmd.guild.id)
		if gamemap != None:
			game_data = gamemap.get(poi_data.id_poi)

		team = ewutils.flattenTokenListToString(cmd.tokens[1:])
		if team not in ["purple", "pink"]:
			response = "Please choose if you want to play on the pink team or the purple team."
			return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

		if game_data == None:
			game_data = EwSlimeballGame(poi_data.id_poi, cmd.message.guild.id)
			response = "You grab a stray ball and start a new game of {game} as a {team} team player."
		else:
			response = "You join the {game} game on the {team} team."

		slimeball_player = EwSlimeballPlayer(cmd.message.author.id, cmd.message.guild.id, game_data.id_game, team)
	else:
		response = "You are playing {game} on the {team} team. You are currently at {player_coords} going in direction {player_vel}. The ball is currently at {ball_coords} going in direction {ball_vel}. The score is purple {score_purple} : {score_pink} pink."

	response = response.format(
			game = cmd.cmd[1:],
			team = slimeball_player.team,
			player_coords = slimeball_player.coords,
		   	ball_coords = game_data.ball_coords,
		   	player_vel = slimeball_player.velocity,
		   	ball_vel = game_data.ball_velocity,
		   	score_purple = game_data.score_purple,
		   	score_pink = game_data.score_pink
	)
	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

async def slimeballgo(cmd):

	global sb_userid_to_player
	slimeball_player = sb_userid_to_player.get(cmd.message.author.id)

	if slimeball_player == None:
		response = "You have to join a game using {} first.".format(cmd.cmd[1:-2])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if not ewutils.channel_name_is_poi(cmd.message.channel.name):
		response = "You have to go into the city to play Slimeball."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	global sb_games
	game_data = sb_games.get(slimeball_player.id_game)

	poi_data = ewcfg.chname_to_poi.get(cmd.message.channel.name)

	if poi_data.id_poi != game_data.poi:
		game_poi = ewcfg.chname_to_poi.get(cmd.message.channel.name)
		response = "Your Slimeball game is happening in the #{} channel.".format(game_poi.channel)
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))


	target_coords = get_coords(cmd.tokens[1:])

	if len(target_coords) != 2:
		response = "Specify where you want to {} to.".format(cmd.cmd)
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	target_vector = ewutils.EwVector2D(target_coords)
	current_vector = ewutils.EwVector2D(slimeball_player.coords)

	target_direction = target_vector.subtract(current_vector)
	target_direction = target_direction.normalize()

	current_direction = ewutils.EwVector2D(slimeball_player.velocity)

	result_direction = current_direction.add(target_direction)
	result_direction = result_direction.normalize()

	slimeball_player.velocity = result_direction.vector

async def slimeballstop(cmd):
	global sb_userid_to_player
	slimeball_player = sb_userid_to_player.get(cmd.message.author.id)

	if slimeball_player == None:
		response = "You have to join a game using {} first.".format(cmd.cmd[1:-4])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	if not ewutils.channel_name_is_poi(cmd.message.channel.name):
		response = "You have to go into the city to play Slimeball."
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	global sb_games
	game_data = sb_games.get(slimeball_player.id_game)

	poi_data = ewcfg.chname_to_poi.get(cmd.message.channel.name)

	if poi_data.id_poi != game_data.poi:
		game_poi = ewcfg.id_to_poi.get(game_data.poi)
		response = "Your {} game is happening in the #{} channel.".format(cmd.cmd[1:-4], game_poi.channel)
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	slimeball_player.velocity = [0, 0]

async def slimeballleave(cmd):
	global sb_userid_to_player
	slimeball_player = sb_userid_to_player.get(cmd.message.author.id)

	if slimeball_player == None:
		response = "You have to join a game using {} first.".format(cmd.cmd[1:-5])
		return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))

	global sb_games
	game_data = sb_games.get(slimeball_player.id_game)

	game_data.players.remove(slimeball_player)
	slimeball_player.id_game = -1

	response = "You quit the game of {}.".format(cmd.cmd[1:-5])
	return await ewutils.send_message(cmd.client, cmd.message.channel, ewutils.formatMessage(cmd.message.author, response))
