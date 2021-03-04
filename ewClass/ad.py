
import ewcfg
import ewutils

class EwAd:

	id_ad = -1

	id_server = -1
	id_sponsor = ""

	content = ""
	time_expir = 0

	def __init__(
		self,
		id_ad = None
	):
		if id_ad != None:
			self.id_ad = id_ad
			data = ewutils.execute_sql_query("SELECT {id_server}, {id_sponsor}, {content}, {time_expir} FROM ads WHERE {id_ad} = %s".format(
				id_server = ewcfg.col_id_server,
				id_sponsor = ewcfg.col_id_sponsor,
				content = ewcfg.col_ad_content,
				time_expir = ewcfg.col_time_expir,
				id_ad = ewcfg.col_id_ad,
			),(
				self.id_ad,
			))

			if len(data) > 0:
				result = data[0]
				
				self.id_server = result[0]
				self.id_sponsor = result[1]
				self.content = result[2]
				self.time_expir = result[3]
			else:
				self.id_ad = -1

	def persist(self):
		ewutils.execute_sql_query("REPLACE INTO ads ({}, {}, {}, {}, {}) VALUES (%s, %s, %s, %s, %s)".format(
			ewcfg.col_id_ad,
			ewcfg.col_id_server,
			ewcfg.col_id_sponsor,
			ewcfg.col_ad_content,
			ewcfg.col_time_expir,
		),(
			self.id_ad,
			self.id_server,
			self.id_sponsor,
			self.content,
			self.time_expir
		))
	
