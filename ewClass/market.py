
import time

import ewutils
import ewcfg

class EwCompany:
	id_server = -1

	id_stock = ""

	recent_profits = 0

	total_profits = 0

	""" Load the Company data from the database. """
	def __init__(self, id_server = None, stock = None):
		if id_server is not None and stock is not None:
			self.id_server = id_server
			self.id_stock = stock

			try:
				# Retrieve object
				result = ewutils.execute_sql_query("SELECT {recent_profits}, {total_profits} FROM companies WHERE {id_server} = %s AND {stock} = %s".format(
					recent_profits = ewcfg.col_recent_profits,
					total_profits = ewcfg.col_total_profits,
					id_server = ewcfg.col_id_server,
					stock = ewcfg.col_stock
				), (self.id_server, self.id_stock))

				if len(result) > 0:
					# Record found: apply the data to this object.
					self.recent_profits = result[0][0]
					self.total_profits = result[0][1]
				else:
					# Create a new database entry if the object is missing.
					self.persist()
			except:
				ewutils.logMsg("Failed to retrieve company {} from database.".format(self.id_stock))


	""" Save company data object to the database. """
	def persist(self):
		try:
			ewutils.execute_sql_query("REPLACE INTO companies({recent_profits}, {total_profits}, {id_server}, {stock}) VALUES(%s,%s,%s,%s)".format(
				recent_profits = ewcfg.col_recent_profits,
				total_profits = ewcfg.col_total_profits,
				id_server = ewcfg.col_id_server,
				stock = ewcfg.col_stock
			    ), (self.recent_profits, self.total_profits, self.id_server, self.id_stock ))
		except:
			ewutils.logMsg("Failed to save company {} to the database.".format(self.id_stock))


class EwStock:
	id_server = -1

	# The stock's identifying string
	id_stock = ""

	market_rate = 1000

	exchange_rate = 1000000

	boombust = 0

	total_shares = 0

	timestamp = 0

	previous_entry = 0

	def limit_fix(self):
		data = ewutils.execute_sql_query("SELECT SUM({shares}) FROM shares WHERE {stock} = %s".format(
			shares = ewcfg.col_shares,
			stock = ewcfg.col_stock,
		),(
			self.id_stock,
		))

		self.total_shares = data[0][0]
		
		if self.total_shares == None or self.total_shares < 0:
			self.total_shares = 0

	def __init__(self, id_server = None, stock = None, timestamp = None):
		if id_server is not None and stock is not None:
			self.id_server = id_server
			self.id_stock = stock

			# get stock data at specified timestamp
			if timestamp is not None:
				data = ewutils.execute_sql_query("SELECT {stock}, {market_rate}, {exchange_rate}, {boombust}, {total_shares}, {timestamp} FROM stocks WHERE id_server = %s AND {stock} = %s AND {timestamp} = %s".format(
					stock = ewcfg.col_stock,
					market_rate = ewcfg.col_market_rate,
					exchange_rate = ewcfg.col_exchange_rate,
					boombust = ewcfg.col_boombust,
					total_shares = ewcfg.col_total_shares,
					timestamp = ewcfg.col_timestamp
				), (
					id_server,
					stock,
					timestamp
				))
			# otherwise get most recent data
			else:

				data = ewutils.execute_sql_query("SELECT {stock}, {market_rate}, {exchange_rate}, {boombust}, {total_shares}, {timestamp} FROM stocks WHERE id_server = %s AND {stock} = %s ORDER BY {timestamp} DESC".format(
					stock = ewcfg.col_stock,
					market_rate = ewcfg.col_market_rate,
					exchange_rate = ewcfg.col_exchange_rate,
					boombust = ewcfg.col_boombust,
					total_shares = ewcfg.col_total_shares,
					timestamp = ewcfg.col_timestamp,
				), (
					id_server,
					stock
				))

			# slimecoin_total = ewutils.execute_sql_query()

			if len(data) > 0:  # if data is not empty, i.e. it found an entry
				# data is always a two-dimensional array and if we only fetch one row, we have to type data[0][x]
				self.id_stock = data[0][0]
				self.market_rate = data[0][1]
				self.exchange_rate = data[0][2]
				self.boombust = data[0][3]
				self.total_shares = data[0][4]
				self.timestamp = data[0][5]
				self.previous_entry = data[1] if len(data) > 1 else 0 #gets the previous stock
			else:  # create new entry
				self.timestamp = time.time()
				self.market_rate = ewcfg.default_stock_market_rate
				self.exchange_rate = ewcfg.default_stock_exchange_rate
				self.persist()

	def persist(self):
		self.limit_fix()

		ewutils.execute_sql_query("INSERT INTO stocks ({id_server}, {stock}, {market_rate}, {exchange_rate}, {boombust}, {total_shares}, {timestamp}) VALUES(%s, %s, %s, %s, %s, %s, %s)".format(
			id_server = ewcfg.col_id_server,
			stock = ewcfg.col_stock,
			market_rate = ewcfg.col_market_rate,
			exchange_rate = ewcfg.col_exchange_rate,
			boombust = ewcfg.col_boombust,
			total_shares = ewcfg.col_total_shares,
			timestamp = ewcfg.col_timestamp
		), (
			self.id_server,
			self.id_stock,
			self.market_rate,
			self.exchange_rate,
			self.boombust,
			self.total_shares,
			self.timestamp
		))


class EwMarket:
	id_server = -1

	clock = 0
	weather = 'sunny'
	day = 0

	slimes_casino = 0
	slimes_revivefee = 0

	market_rate = 1000
	exchange_rate = 1000000
	boombust = 0
	time_lasttick = 0
	negaslime = 0
	decayed_slimes = 0
	donated_slimes = 0
	donated_poudrins = 0
	caught_fish = 0
	splattered_slimes = 0
	global_swear_jar = 0

	# Double halloween
	horseman_deaths = 0
	horseman_timeofdeath = 0

	# Dict of bazaar items available for purchase
	bazaar_wares = None

	""" Load the market data for this server from the database. """
	def __init__(self, id_server = None):
		if(id_server != None):
			self.id_server = id_server
			self.bazaar_wares = {}

			try:
				conn_info = ewutils.databaseConnect()
				conn = conn_info.get('conn')
				cursor = conn.cursor();

				# Retrieve object
				cursor.execute("SELECT {time_lasttick}, {slimes_revivefee}, {negaslime}, {clock}, {weather}, {day}, {decayed_slimes}, {donated_slimes}, {donated_poudrins}, {caught_fish}, {splattered_slimes}, {global_swear_jar}, {horseman_deaths}, {horseman_timeofdeath} FROM markets WHERE id_server = %s".format(
					time_lasttick = ewcfg.col_time_lasttick,
					slimes_revivefee = ewcfg.col_slimes_revivefee,
					negaslime = ewcfg.col_negaslime,
					clock = ewcfg.col_clock,
					weather = ewcfg.col_weather,
					day = ewcfg.col_day,
					decayed_slimes = ewcfg.col_decayed_slimes,
					donated_slimes = ewcfg.col_donated_slimes,
					donated_poudrins = ewcfg.col_donated_poudrins,
					caught_fish = ewcfg.col_caught_fish,
					splattered_slimes = ewcfg.col_splattered_slimes,
					global_swear_jar = ewcfg.col_global_swear_jar,
					horseman_deaths = ewcfg.col_horseman_deaths,
					horseman_timeofdeath = ewcfg.col_horseman_timeofdeath,
					
				), (self.id_server, ))
				result = cursor.fetchone();

				if result != None:
					# Record found: apply the data to this object.
					self.time_lasttick = result[0]
					self.slimes_revivefee = result[1]
					self.negaslime = result[2]
					self.clock = result[3]
					self.weather = result[4]
					self.day = result[5]
					self.decayed_slimes = result[6]
					self.donated_slimes = result[7]
					self.donated_poudrins = result[8]
					self.caught_fish = result[9]
					self.splattered_slimes = result[10]
					self.global_swear_jar = result[11]
					self.horseman_deaths = result[12]
					self.horseman_timeofdeath = result[13]

					cursor.execute("SELECT {}, {} FROM bazaar_wares WHERE {} = %s".format(
						ewcfg.col_name,
						ewcfg.col_value,
						ewcfg.col_id_server,
					), (
						self.id_server,
					))

					for row in cursor:
						# this try catch is only necessary as long as extraneous props exist in the table
						try:
							self.bazaar_wares[row[0]] = row[1]
						except:
							ewutils.logMsg("extraneous bazaar item row detected.")

				else:
					# Create a new database entry if the object is missing.
					cursor.execute("REPLACE INTO markets(id_server) VALUES(%s)", (id_server, ))

					conn.commit()
			finally:
				# Clean up the database handles.
				cursor.close()
				ewutils.databaseClose(conn_info)

	""" Save market data object to the database. """
	def persist(self):
		try:
			conn_info = ewutils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor();

			# Save the object.
			cursor.execute("REPLACE INTO markets ({id_server}, {time_lasttick}, {slimes_revivefee}, {negaslime}, {clock}, {weather}, {day}, {decayed_slimes}, {donated_slimes}, {donated_poudrins}, {caught_fish}, {splattered_slimes}, {global_swear_jar}, {horseman_deaths}, {horseman_timeofdeath}) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
				id_server = ewcfg.col_id_server,
				time_lasttick = ewcfg.col_time_lasttick,
				slimes_revivefee = ewcfg.col_slimes_revivefee,
				negaslime = ewcfg.col_negaslime,
				clock = ewcfg.col_clock,
				weather = ewcfg.col_weather,
				day = ewcfg.col_day,
				decayed_slimes = ewcfg.col_decayed_slimes,
				donated_slimes = ewcfg.col_donated_slimes,
				donated_poudrins = ewcfg.col_donated_poudrins,
				caught_fish = ewcfg.col_caught_fish,
				splattered_slimes = ewcfg.col_splattered_slimes,
				global_swear_jar = ewcfg.col_global_swear_jar,
				horseman_deaths = ewcfg.col_horseman_deaths,
				horseman_timeofdeath = ewcfg.col_horseman_timeofdeath,
			), (
				self.id_server,
				self.time_lasttick,
				self.slimes_revivefee,
				self.negaslime,
				self.clock,
				self.weather,
				self.day,
				self.decayed_slimes,
				self.donated_slimes,
				self.donated_poudrins,
				self.caught_fish,
				self.splattered_slimes,
				self.global_swear_jar,
				self.horseman_deaths,
				self.horseman_timeofdeath,
			))

			cursor.execute("DELETE FROM bazaar_wares WHERE {} = %s".format(
				ewcfg.col_id_server,
			), (
				self.id_server,
			))

			# Write out all current item rows.
			for name in self.bazaar_wares:
				cursor.execute("INSERT INTO bazaar_wares({}, {}, {}) VALUES(%s, %s, %s)".format(
					ewcfg.col_id_server,
					ewcfg.col_name,
					ewcfg.col_value,
				), (
					self.id_server,
					name,
					self.bazaar_wares[name],
				))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			ewutils.databaseClose(conn_info)
