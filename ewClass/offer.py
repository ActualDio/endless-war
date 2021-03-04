
import ewutils
import ewcfg

class EwOffer:
	id_server = -1
	id_user = -1
	offer_give = 0
	offer_receive = ""
	time_sinceoffer = 0

	def __init__(
		self,
		id_server = None,
		id_user = None,
		offer_give = None,

	):
		if id_server is not None and id_user is not None and offer_give is not None:
			self.id_server = id_server
			self.id_user = id_user
			self.offer_give = offer_give

			data = ewutils.execute_sql_query(
				"SELECT {time_sinceoffer} FROM offers WHERE id_server = %s AND id_user = %s AND {col_offer_give} = %s".format(
					time_sinceoffer = ewcfg.col_time_sinceoffer,
					col_offer_give = ewcfg.col_offer_give,
				), (
					id_server,
					id_user,
					offer_give,
				)
			)

			if len(data) > 0:  # if data is not empty, i.e. it found an entry
				# data is always a two-dimensional array and if we only fetch one row, we have to type data[0][x]
				self.time_sinceoffer = data[0][0]

			data = ewutils.execute_sql_query(
				"SELECT {col_offer_receive} FROM offers WHERE id_server = %s AND id_user = %s AND {col_offer_give} = %s".format(
					col_offer_receive = ewcfg.col_offer_receive,
					col_offer_give = ewcfg.col_offer_give,
				), (
					id_server,
					id_user,
					offer_give,
				)
			)

			if len(data) > 0:  # if data is not empty, i.e. it found an entry
				# data is always a two-dimensional array and if we only fetch one row, we have to type data[0][x]
				self.offer_receive = data[0][0]

			else:  # create new entry
				ewutils.execute_sql_query(
					"REPLACE INTO offers(id_server, id_user, {col_offer_give}) VALUES (%s, %s, %s)".format(
						col_offer_give = ewcfg.col_offer_give,
					), (
						id_server,
						id_user,
						offer_give,
					)
				)

	def persist(self):
		ewutils.execute_sql_query(
			"REPLACE INTO offers(id_server, id_user, {col_offer_give}, {col_offer_receive}, {col_time_sinceoffer}) VALUES (%s, %s, %s, %s, %s)".format(
				col_offer_give = ewcfg.col_offer_give,
				col_offer_receive = ewcfg.col_offer_receive,
				col_time_sinceoffer = ewcfg.col_time_sinceoffer
			), (
				self.id_server,
				self.id_user,
				self.offer_give,
				self.offer_receive,
				self.time_sinceoffer
			)
		)

	def deal(self):
		ewutils.execute_sql_query("DELETE FROM offers WHERE {id_user} = %s AND {id_server} = %s AND {col_offer_give} = %s".format(
			id_user = ewcfg.col_id_user,
			id_server = ewcfg.col_id_server,
			col_offer_give = ewcfg.col_offer_give,
		),(
			self.id_user,
			self.id_server,
			self.offer_give
		))
