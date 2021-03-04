
import random

import ewcfg
import ewutils

sb_count = 0

sb_games = {}
sb_idserver_to_gamemap = {}

sb_slimeballerid_to_player = {}
sb_userid_to_player = {}
#sports

class EwSlimeballPlayer:

	id_user = -1
	id_server = -1
	id_player = -1

	id_game = -1

	coords = None
	velocity = None
	team = ""

	def __init__(self, id_user, id_server, id_game, team):

		self.id_user = id_user
		self.id_server = id_server
		self.id_game = id_game
		self.team = team

		global sb_count

		self.id_player = sb_count
		sb_count += 1

		global sb_games

		self.velocity = [0, 0]
		

		game_data = sb_games.get(id_game)
		while not game_data.coords_free(self.coords):
			self.coords = get_starting_position(self.team)

		game_data.players.append(self)

		global sb_slimeballerid_to_player
		global sb_userid_to_player
		sb_userid_to_player[self.id_user] = self
		sb_slimeballerid_to_player[self.id_player] = self


	def move(self):
		resp_cont = ewutils.EwResponse(id_server = self.id_server)
		abs_x = abs(self.velocity[0])
		abs_y = abs(self.velocity[1])
		abs_sum = abs_x + abs_y
		if abs_sum == 0:
			return resp_cont

		if random.random() * abs_sum < abs_x:
			move = [self.velocity[0] / abs_x, 0]
		else:
			move = [0, self.velocity[1] / abs_y]


		move_vector = ewutils.EwVector2D(move)
		position_vector = ewutils.EwVector2D(self.coords)

		destination_vector = position_vector.add(move_vector)

		global sb_games
		game_data = sb_games.get(self.id_game)

		player_data = EwDiscordUser(id_user = self.id_user)
		response = ""
		ball_contact = False
		for i in range(-1, 2):
			for j in range(-1, 2):
				neighbor_direction = [i, j]
				neighbor_vector = ewutils.EwVector2D(neighbor_direction)
				if move_vector.scalar_product(neighbor_vector) > 0:
					neighbor_position = position_vector.add(neighbor_vector)
					if neighbor_position.vector == game_data.ball_coords:
						ball_contact = True
						break

		if ball_contact:
			game_data.ball_velocity = [round(5 * self.velocity[0]), round(5 * self.velocity[1])]
			game_data.last_contact = self.id_player
			self.velocity = [0, 0]
			response = "{} has kicked the ball in direction {}!".format(player_data.name, game_data.ball_velocity)

		elif game_data.coords_free(destination_vector.vector):
			self.coords = destination_vector.vector

		elif game_data.out_of_bounds(destination_vector.vector):
			self.velocity = [0, 0]
			response = "{} has walked against the outer bounds and stopped at {}.".format(player_data.name, self.coords)
		else:
			vel = self.velocity

			for p in game_data.players:
				if p.coords == destination_vector.vector:
					self.velocity = p.velocity
					p.velocity = vel
					other_player_data = EwDiscordUser(id_user = p.id_user)
					response = "{} has collided with {}.".format(player_data.name, other_player_data.name)
					break			
					
		if len(response) > 0:
			poi_data = ewcfg.id_to_poi.get(game_data.poi)
			resp_cont.add_channel_response(poi_data.channel, response)

		return resp_cont
		
	

class EwSlimeballGame:

	id_server = -1
	id_game = -1

	players = []

	poi = ""

	ball_coords = None

	ball_velocity = None

	score_pink = 0
	score_purple = 0
	last_contact = -1

	def	__init__(self, poi, id_server):
		self.poi = poi
		self.id_server = id_server

		global sb_count
		self.id_game = sb_count

		sb_count += 1

		global sb_games
		sb_games[self.id_game] = self

		global sb_idserver_to_gamemap
		gamemap = sb_idserver_to_gamemap.get(self.id_server)
		if gamemap == None:
			gamemap = {}
			sb_idserver_to_gamemap[self.id_server] = gamemap

		gamemap[self.poi] = self

		self.players = []

		ball_coords = []
		while not self.coords_free(ball_coords):
			ball_coords = get_starting_position("")
		self.ball_coords = ball_coords

		self.ball_velocity = [0, 0]

		self.score_pink = 0
		self.score_purple = 0
		self.last_contact = -1

	def coords_free(self, coords):

		if coords == None or len(coords) != 2:
			return False

		if self.out_of_bounds(coords):
			return False

		if coords == self.ball_coords:
			return False

		if self.player_at_coords(coords) != -1:
			return False

		return True

	def out_of_bounds(self, coords):
		return coords[0] < 0 or coords[0] > 99 or coords[1] < 0 or coords[1] > 49

	def is_goal(self):
		return self.is_goal_purple() or self.is_goal_pink()

	def is_goal_purple(self):
		return self.ball_coords[0] == 0 and self.ball_coords[1] in range(20, 30)
		
	def is_goal_pink(self):
		return self.ball_coords[0] == 99 and self.ball_coords[1] in range(20, 30)
		
	def player_at_coords(self, coords):
		player = -1

		for p in self.players:
			if p.coords == coords:
				player = p.id_player
				break

		return player

	def move_ball(self):
		resp_cont = ewutils.EwResponse(id_server = self.id_server)
		abs_x = abs(self.ball_velocity[0])
		abs_y = abs(self.ball_velocity[1])
		abs_sum = abs_x + abs_y
		if abs_sum == 0:
			return resp_cont

		move = [self.ball_velocity[0], self.ball_velocity[1]]
		whole_move_vector = ewutils.EwVector2D(move)

		response = ""
		while abs_sum != 0:
			if random.random() * abs_sum < abs_x:
				part_move = [move[0] / abs_x, 0]
			else:
				part_move = [0, move[1] / abs_y]

			

			move_vector = ewutils.EwVector2D(part_move)
			position_vector = ewutils.EwVector2D(self.ball_coords)

			destination_vector = position_vector.add(move_vector)

			player_contact = False
			for i in range(-1, 2):
				for j in range(-1, 2):
					neighbor_direction = [i, j]
					neighbor_vector = ewutils.EwVector2D(neighbor_direction)
					if move_vector.scalar_product(neighbor_vector) > 0:
						neighbor_position = position_vector.add(neighbor_vector)
						player = self.player_at_coords(neighbor_position.vector)
						if player != -1:
							self.ball_velocity = [0, 0]
							self.last_contact = player
							player_contact = True
							break

			if player_contact:
				break

			elif self.coords_free(destination_vector.vector):
				self.ball_coords = destination_vector.vector
			elif self.out_of_bounds(destination_vector.vector):
				for i in range(2):
					if part_move[i] != 0:
						whole_move_vector.vector[i] *= -1
						self.ball_velocity[i] *= -1


			if self.is_goal():

				global sb_slimeballerid_to_player

				scoring_player = sb_slimeballerid_to_player.get(self.last_contact)
				if scoring_player != None:
					player_data = EwDiscordUser(id_user = scoring_player.id_user)
				else:
					player_data = None

				if self.is_goal_purple():

					if player_data != None:
						response = "{} scored a goal for the pink team!".format(player_data.name)
					else:
						response = "The pink team scored a goal!"
					self.score_pink += 1
				elif self.is_goal_pink():

					if player_data != None:
						response = "{} scored a goal for the purple team!".format(player_data.name)
					else:
						response = "The purple team scored a goal!"
					self.score_purple += 1


				self.ball_velocity = [0, 0]
				self.ball_coords = get_starting_position("")
				self.last_contact = -1
				break

			else:
				whole_move_vector = whole_move_vector.subtract(move_vector)
				abs_x = abs(whole_move_vector.vector[0])
				abs_y = abs(whole_move_vector.vector[1])
				abs_sum = abs_x + abs_y
				move = whole_move_vector.vector

		for i in range(2):
			if self.ball_velocity[i] > 0:
				self.ball_velocity[i] -= 1
			elif self.ball_velocity[i] < 0:
				self.ball_velocity[i] += 1

		if len(response) > 0:
			poi_data = ewcfg.id_to_poi.get(self.poi)
			resp_cont.add_channel_response(poi_data.channel, response)

		return resp_cont

	def kill(self):
		global sb_games
		global sb_poi_to_gamemap

		sb_games[self.id_game] = None
		gamemap = sb_idserver_to_gamemap.get(self.id_server)
		gamemap[self.poi] = None
