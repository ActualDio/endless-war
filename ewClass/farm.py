
import ewutils
import ewcfg

class EwFarm:
	id_server = -1
	id_user = -1
	name = ""
	time_lastsow = 0
	phase = 0
	time_lastphase = 0
	slimes_onreap = 0
	action_required = 0
	crop = ""
	# player's life state at sow
	sow_life_state = 0

	def __init__(
		self,
		id_server = None,
		id_user = None,
		farm = None
	):
		if id_server is not None and id_user is not None and farm is not None:
			self.id_server = id_server
			self.id_user = id_user
			self.name = farm

			data = ewutils.execute_sql_query(
				"SELECT {time_lastsow}, {phase}, {time_lastphase}, {slimes_onreap}, {action_required}, {crop}, {life_state} FROM farms WHERE id_server = %s AND id_user = %s AND {col_farm} = %s".format(
					time_lastsow = ewcfg.col_time_lastsow,
					col_farm = ewcfg.col_farm,
					phase = ewcfg.col_phase,
					time_lastphase = ewcfg.col_time_lastphase,
					slimes_onreap = ewcfg.col_slimes_onreap,
					action_required = ewcfg.col_action_required,
					crop = ewcfg.col_crop,
					life_state = ewcfg.col_sow_life_state,
				), (
					id_server,
					id_user,
					farm
				)
			)

			if len(data) > 0:  # if data is not empty, i.e. it found an entry
				# data is always a two-dimensional array and if we only fetch one row, we have to type data[0][x]
				self.time_lastsow = data[0][0]
				self.phase = data[0][1]
				self.time_lastphase = data[0][2]
				self.slimes_onreap = data[0][3]
				self.action_required = data[0][4]
				self.crop = data[0][5]
				self.sow_life_state = data[0][6]

			else:  # create new entry
				ewutils.execute_sql_query(
					"REPLACE INTO farms (id_server, id_user, {col_farm}) VALUES (%s, %s, %s)".format(
						col_farm = ewcfg.col_farm
					), (
						id_server,
						id_user,
						farm
					)
				)

	def persist(self):
		ewutils.execute_sql_query(
			"REPLACE INTO farms(id_server, id_user, {farm}, {time_lastsow}, {phase}, {time_lastphase}, {slimes_onreap}, {action_required}, {crop}, {life_state}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
				farm = ewcfg.col_farm,
				time_lastsow = ewcfg.col_time_lastsow,
				phase = ewcfg.col_phase,
				time_lastphase = ewcfg.col_time_lastphase,
				slimes_onreap = ewcfg.col_slimes_onreap,
				action_required = ewcfg.col_action_required,
				crop = ewcfg.col_crop,
				life_state = ewcfg.col_sow_life_state,
			), (
				self.id_server,
				self.id_user,
				self.name,
				self.time_lastsow,
				self.phase,
				self.time_lastphase,
				self.slimes_onreap,
				self.action_required,
				self.crop,
				self.sow_life_state,
			)
		)


class EwFarmAction:
	id_action = 0

	action = ""
	
	str_check = ""

	str_execute = ""

	str_execute_fail = ""

	aliases = []

	def __init__(self,
		id_action = 0,
		action = "",
		str_check = "",
		str_execute = "",
		str_execute_fail = "",
		aliases = []
	):
		self.id_action = id_action
		self.action = action
		self.str_check = str_check
		self.str_execute = str_execute
		self.str_execute_fail = str_execute_fail
		self.aliases = aliases
