
import ewcfg
import ewutils

class EwQuadrant:

	id_server = -1

	id_user = -1

	quadrant = ""

	id_target = -1

	id_target2 = -1


	def __init__(self, id_server = None, id_user = None, quadrant = None, id_target = None, id_target2 = None):
		if id_server is not None and id_user is not None and quadrant is not None:
			self.id_server = id_server
			self.id_user = id_user
			self.quadrant = quadrant

			if id_target is not None:
				
				self.id_target = id_target
				if quadrant == ewcfg.quadrant_policitous and id_target2 is not None:
					self.id_target2 = id_target2

				ewutils.execute_sql_query("REPLACE INTO quadrants ({col_id_server}, {col_id_user}, {col_quadrant}, {col_target}, {col_target2}) VALUES (%s, %s, %s, %s, %s)".format(
					col_id_server = ewcfg.col_id_server,
					col_id_user = ewcfg.col_id_user,
					col_quadrant = ewcfg.col_quadrant,
					col_target = ewcfg.col_quadrants_target,
					col_target2 = ewcfg.col_quadrants_target2
					), (    
					self.id_server,
					self.id_user,
					self.quadrant,
					self.id_target,
					self.id_target2
				))

			else:
				data = ewutils.execute_sql_query("SELECT {col_target}, {col_target2} FROM quadrants WHERE {col_id_server} = %s AND {col_id_user} = %s AND {col_quadrant} = %s".format(
					col_target = ewcfg.col_quadrants_target,
					col_target2 = ewcfg.col_quadrants_target2,
					col_id_server = ewcfg.col_id_server,
					col_id_user = ewcfg.col_id_user,
					col_quadrant = ewcfg.col_quadrant
					), (
					self.id_server,
					self.id_user,
					self.quadrant
				))
				
				if len(data) > 0:
					self.id_target = data[0][0]
					self.id_target2 = data[0][1]



	def persist(self):
		ewutils.execute_sql_query("REPLACE INTO quadrants ({col_id_server}, {col_id_user}, {col_quadrant}, {col_target}, {col_target2}) VALUES (%s, %s, %s, %s, %s)".format(
			col_id_server = ewcfg.col_id_server,
			col_id_user = ewcfg.col_id_user,
			col_quadrant = ewcfg.col_quadrant,
			col_target = ewcfg.col_quadrants_target,
			col_target2 = ewcfg.col_quadrants_target2
			), (    
			self.id_server,
			self.id_user,
			self.quadrant,
			self.id_target,
			self.id_target2
		))
	
	def check_if_onesided(self):
		target_quadrant = EwQuadrant(id_server = self.id_server, id_user = self.id_target, quadrant = self.quadrant)

		if self.quadrant == ewcfg.quadrant_policitous:
			if self.id_target2 is not None:
				target2_quadrant = EwQuadrant(id_server = self.id_server, id_user = self.id_target2, quadrant = self.quadrant)
				target_targets = [target_quadrant.id_target, target_quadrant.id_target2]
				target2_targets = [target2_quadrant.id_target, target2_quadrant.id_target2]

				if self.id_user in target_targets and \
				    self.id_user in target2_targets and \
				    self.id_target in target2_targets and \
				    self.id_target2 in target_targets:
					return False
			return True

		elif target_quadrant.id_target == self.id_user:
			return False
		else:
			return True


class EwQuadrantFlavor:
	id_quadrant = ""
	
	aliases = []

	resp_add_onesided = ""

	resp_add_relationship = ""

	resp_view_onesided = ""

	resp_view_onesided_self = ""

	resp_view_relationship = ""

	resp_view_relationship_self = ""

	def __init__(self,
		id_quadrant = "",
		aliases = [],
		resp_add_onesided = "",
		resp_add_relationship = "",
		resp_view_onesided = "",
		resp_view_onesided_self = "",
		resp_view_relationship = "",
		resp_view_relationship_self = ""
	    ):
		self.id_quadrant = id_quadrant
		self.aliases = aliases
		self.resp_add_onesided = resp_add_onesided
		self.resp_add_relationship = resp_add_relationship
		self.resp_view_onesided = resp_view_onesided
		self.resp_view_onesided_self = resp_view_onesided_self
		self.resp_view_relationship = resp_view_relationship
		self.resp_view_relationship_self = resp_view_relationship_self 
