import ewutils
import ewcfg


""" update the player record with the current data. """
def player_update(member = None, server = None):
	id_server_old = ""

	try:
		conn_info = ewutils.databaseConnect()
		conn = conn_info.get('conn')
		cursor = conn.cursor()

		# Get existing player info (or create a record if it's a new player)
		player = EwDiscordUser(
			id_user = member.id,
			id_server = server.id
		)

		# Update values with Member data.
		id_server_old = player.id_server
		player.id_server = server.id
		player.avatar = member.avatar_url
		player.name = member.name

		# Save the updated data.
		player.persist()

		conn.commit()
	finally:
		cursor.close()
		ewutils.databaseClose(conn_info)

	# Log server changes
	if(server.id != int(id_server_old)):
		
		ewutils.logMsg('active server for {} changed from "{}" to "{}"'.format(
			member.name,
			id_server_old,
			server.id
		))
