import ewutils
import ewcfg
import ewstats
import ewitem

stat_fn_map = {}
fns_initialized = False

def init_stat_function_map():
	global stat_fn_map
	stat_fn_map = {
		ewcfg.stat_slimesmined: process_slimesmined,
		ewcfg.stat_max_slimesmined: process_max_slimesmined,
		ewcfg.stat_slimesfromkills: process_slimesfromkills,
		ewcfg.stat_max_slimesfromkills: process_max_slimesfromkills,
		ewcfg.stat_kills: process_kills,
		ewcfg.stat_max_kills: process_max_kills,
		ewcfg.stat_ghostbusts: process_ghostbusts,
		ewcfg.stat_max_ghostbusts: process_max_ghostbusts,
		ewcfg.stat_poudrins_looted: process_poudrins_looted,
                ewcfg.stat_slimesfarmed: process_slimesfarmed,
                ewcfg.stat_slimesscavenged: process_slimesscavenged
	}
	global fns_initialized
	fns_initialized = True

def process_stat_change(id_server = None, id_user = None, metric = None, value = None):
	if fns_initialized == False:
		init_stat_function_map()

	fn = stat_fn_map.get(metric)

	if fn != None:
		fn(id_server = id_server, id_user = id_user, value = value)

def process_slimesmined(player = None, value = None):
	if player != None:
		player.track_maximum(metric = ewcfg.stat_max_slimesmined, value = value)

def process_max_slimesmined(player = None, value = None):
	# TODO give apropriate medal
	pass

def process_slimesfromkills(player = None, value = None):
	if player != None:
		player.track_maximum(metric = ewcfg.stat_max_slimesfromkills, value = value)

def process_max_slimesfromkills(player = None, value = None):
	# TODO give apropriate medal
	pass

def process_slimesfarmed(player = None, value = None):
	if player != None:
		player.track_maximum(metric = ewcfg.stat_max_slimesfarmed, value = value)

def process_slimesscavenged(player = None, value = None):
	if player != None:
		player.track_maximum(metric = ewcfg.stat_max_slimesscavenged, value = value)

def process_kills(player = None, value = None):
	if player != None:
		player.track_maximum(metric = ewcfg.stat_max_kills, value = value)
		player.increment_stat(metric = ewcfg.stat_lifetime_kills)

def process_max_kills(player = None, value = None):
	# TODO give apropriate medal
	pass

def process_ghostbusts(player = None, value = None):
	if player != None:
		player.track_maximum(metric = ewcfg.stat_max_ghostbusts, value = value)
		player.increment_stat(metric = ewcfg.stat_lifetime_ghostbusts)

def process_max_ghostbusts(id_server = None, id_user = None, value = None):
	# TODO give apropriate medal
	pass

def process_poudrins_looted(player = None, value = None):
	if player != None:
		poudrin_amount = ewitem.find_poudrin(id_user = player.id_user, id_server = player.id_server)

		player.track_maximum(metric = ewcfg.stat_max_poudrins, value = poudrin_amount)
		player.change_stat(metric = ewcfg.stat_lifetime_poudrins, n = value)
