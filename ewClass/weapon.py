
import ewcfg

""" A weapon object which adds flavor text to kill/shoot. """
class EwWeapon:

	item_type = "weapon"

	# A unique name for the weapon. This is used in the database and typed by
	# users, so it should be one word, all lowercase letters.
	id_weapon = ""

	# An array of names that might be used to identify this weapon by the player.
	alias = None#[]

	# Displayed when !equip-ping this weapon
	str_equip = ""

	# Displayed when this weapon is used for a !kill
	str_kill = ""

	# Displayed to the dead victim in the sewers. Brief phrase such as "gunned down" etc.
	str_killdescriptor = ""

	# Displayed when viewing the !trauma of another player.
	str_trauma = ""

	# Displayed when viewing the !trauma of yourself.
	str_trauma_self = ""
	
	# like str_weapon but without the article
	str_name = ""

	# Displayed when viewing the !weapon of another player.
	str_weapon = ""

	# Displayed when viewing the !weapon of yourself.
	str_weapon_self = ""

	# Same as weapon and weapon_self, but used when the player's weapon skill is max.
	str_weaponmaster = ""
	str_weaponmaster_self = ""

	# Displayed when a non-lethal hit occurs.
	str_damage = ""

	# Displayed when two players wielding the same weapon !spar with each other.
	str_duel = ""

	# Function that applies the special effect for this weapon.
	fn_effect = None#[]

	# Displayed when a weapon effect causes a critical hit.
	str_crit = ""

	# Displayed when a weapon effect causes a miss.
	str_miss = ""

	# Displayed when !inspect-ing
	str_description = ""

	# Displayed when reloading
	str_reload = ""

	# Displayed when the weapon used it's last ammo
	str_reload_warning = ""
	
	# Displayed in a scalp's description.
	str_scalp = ""

	# Clip size
	clip_size = 0

	# Cost
	price = 0

	# Hard Cooldown 
	cooldown = 0

	# Vendor
	vendors = None#[]

	# Classes the weapon belongs to
	classes = None#[]

	acquisition = "dojo"

	# Statistics metric
	stat = ""
	
	# sap needed to fire
	#sap_cost = 0

	# length of captcha you need to solve to fire
	captcha_length = 0

	#whether the weapon is a tool
	is_tool = 0

	#an array for storing extra string data for different tools
	tool_props = {}

	def __init__(
		self,
		id_weapon = "",
		alias =   [],
		str_equip = "",
		str_kill = "",
		str_killdescriptor = "",
		str_trauma = "",
		str_trauma_self = "",
		str_name = "",
		str_weapon = "",
		str_weapon_self = "",
		str_damage = "",
		str_duel = "",
		str_weaponmaster = "",
		str_weaponmaster_self = "",
		fn_effect = None,
		str_crit = "",
		str_miss = "",
		str_description = "",
		str_reload = "",
		str_reload_warning = "",
		str_scalp = "",
		clip_size = 0,
		price = 0,
		cooldown = 0,
		vendors = [],
		classes = [],
		acquisition = "dojo",
		stat = "",
		#sap_cost = 0,
		captcha_length = 0,
		is_tool = 0,
		tool_props = None
	):
		self.item_type = ewcfg.it_weapon

		self.id_weapon = id_weapon
		self.alias = alias
		self.str_equip = str_equip
		self.str_kill = str_kill
		self.str_killdescriptor = str_killdescriptor
		self.str_trauma = str_trauma
		self.str_trauma_self = str_trauma_self
		self.str_name = str_name
		self.str_weapon = str_weapon
		self.str_weapon_self = str_weapon_self
		self.str_damage = str_damage
		self.str_duel = str_duel
		self.str_weaponmaster = str_weaponmaster
		self.str_weaponmaster_self = str_weaponmaster_self
		self.fn_effect = fn_effect
		self.str_crit = str_crit
		self.str_miss = str_miss
		self.str_description = str_description
		self.str_reload = str_reload
		self.str_reload_warning = str_reload_warning
		self.str_scalp = str_scalp
		self.clip_size = clip_size
		self.price = price
		self.cooldown = cooldown
		self.vendors = vendors
		self.classes = classes
		self.acquisition = acquisition
		self.stat = stat
		#self.sap_cost = sap_cost
		self.captcha_length = captcha_length
		self.is_tool = is_tool
		self.tool_props = tool_props,
		#self.str_name = self.str_weapon,



# Reskinned version of weapon class from ewwep.
class EwAttackType:

	# An name used to identify the attacking type
	id_type = ""

	# Displayed when this weapon is used for a !kill
	str_kill = ""

	# Displayed to the dead victim in the sewers. Brief phrase such as "gunned down" etc.
	str_killdescriptor = ""

	# Displayed when viewing the !trauma of another player.
	str_trauma = ""

	# Displayed when viewing the !trauma of yourself.
	str_trauma_self = ""

	# Displayed when a non-lethal hit occurs.
	str_damage = ""

	# Function that applies the special effect for this weapon.
	fn_effect = None

	# Displayed when a weapon effect causes a critical hit.
	str_crit = ""

	# Displayed when a weapon effect causes a miss.
	str_miss = ""
	
	# Displayed when a weapon effect targets a group.
	str_groupattack = ""

	def __init__(
			self,
			id_type="",
			str_kill="",
			str_killdescriptor="",
			str_trauma="",
			str_trauma_self="",
			str_damage="",
			fn_effect=None,
			str_crit="",
			str_miss="",
			str_groupattack = "",
	):
		self.id_type = id_type
		self.str_kill = str_kill
		self.str_killdescriptor = str_killdescriptor
		self.str_trauma = str_trauma
		self.str_trauma_self = str_trauma_self
		self.str_damage = str_damage
		self.fn_effect = fn_effect
		self.str_crit = str_crit
		self.str_miss = str_miss
		self.str_groupattack = str_groupattack

class EwTrauma:

	# The trauma's name
	id_trauma = ""

	# String used to describe the trauma when you !data yourself
	str_trauma_self = ""

	# String used to describe the trauma when you !data another player
	str_trauma = ""

	# the trauma's effect
	trauma_class = ""

	def __init__(self,
		id_trauma = "",
		str_trauma_self = "",
		str_trauma = "",
		trauma_class = "",
	):

		self.id_trauma = id_trauma

		if str_trauma_self == "":
			str_trauma_self = "You have the {} trauma.".format(self.id_trauma)
		self.str_trauma_self = str_trauma_self

		if str_trauma == "":
			str_trauma = "They have the {} trauma.".format(self.id_trauma)
		self.str_trauma = str_trauma

		self.trauma_class = trauma_class

class EwHitzone:
	

	name = ""

	aliases = []

	id_injury = ""

	def __init__(self,
		name = "",
		aliases = [],
		id_injury = "",
	):
		self.name = name
		self.aliases = aliases
		self.id_injury = id_injury

