import random

import ewutils
import ewstats
import ewitem
import random
import json
import os
from ewcosmeticitem import EwCosmeticItem
from ewwep import EwWeapon
from ewhunting import EwAttackType
from ewweather import EwWeather
from ewfood import EwFood
from ewitem import EwItemDef, EwGeneralItem
from ewmap import EwPoi
from ewmutation import EwMutationFlavor
from ewslimeoid import EwBody, EwHead, EwMobility, EwOffense, EwDefense, EwSpecial, EwBrain, EwHue, EwSlimeoidFood
from ewquadrants import EwQuadrantFlavor
from ewtransport import EwTransportLine
from ewsmelting import EwSmeltingRecipe
from ewstatuseffects import EwStatusEffectDef
from ewfarm import EwFarmAction
from ewfish import EwFish
from ewapt import EwFurniture
from ewworldevent import EwEventDef
from ewdungeons import EwDungeonScene
from ewtrauma import EwTrauma, EwHitzone
from ewprank import EwPrankItem
from ewmarket import EwMarket
from ewhunting import EwSeedPacket, EwTombstone

import ewdebug

# Global configuration options.

version = "v3.71 - No Slimernalia"


dir_msgqueue = 'msgqueue'

database = "rfck"

discord_message_length_limit = 2000

# Update intervals
update_hookstillactive = 60 * 60 * 1
update_twitch = 60
update_pvp = 60
update_market = 900 #15 min

# Number of times the bot should try a permissions-related API call. This is done purely for safety measures.
permissions_tries = 1

# Time saved moving through friendly territory (or lost in hostile territory).
territory_time_gain = 10

# A variable which is used to determine how certain functions of enemies are to perform
gvs_active = False

# The max amount of degradation a district can have before it is shambled completely
district_max_degradation = 10000

# Market delta
max_iw_swing = 30

# An inventory limit for every item type that's not food or weapons
generic_inv_limit = 1000

# combatant ids to differentiate players and NPCs in combat
char_type_player = "player"
char_type_enemy = "enemy"

# Life states. How the player is living (or deading) in the database
life_state_corpse = 0
life_state_juvenile = 1
life_state_enlisted = 2
life_state_shambler = 3
life_state_executive = 6
life_state_lucky = 7
life_state_grandfoe = 8
life_state_kingpin = 10
life_state_observer = 20

# Player stats. What, you ever play an RPG before, kid?
stat_attack = 'attack'
stat_defense = 'defense'
stat_speed = 'speed'

playerstats_list = [
	stat_attack,
	stat_defense,
	stat_speed,
]

slimeoid_tick_length = 5 * 60 #5 minutes

# slimeoid life states
slimeoid_state_none = 0
slimeoid_state_forming = 1
slimeoid_state_active = 2
slimeoid_state_stored = 3
slimeoid_state_dead = 4

# slimeoid types
sltype_lab = 'Lab'
sltype_nega = 'Nega'
sltype_wild = 'Wild'

# slimeoid battle types
battle_type_arena = 0
battle_type_nega = 1

# slimeoid stats
slimeoid_stat_moxie = 'moxie'
slimeoid_stat_grit = 'grit'
slimeoid_stat_chutzpah = 'chutzpah'

# ID tags for points of interest that are needed in code.
poi_id_thesewers = "thesewers"
poi_id_slimeoidlab = "slimecorpslimeoidlaboratory"
poi_id_realestate = "realestateagency"
poi_id_glocksburycomics = "glocksburycomics"
poi_id_slimypersuits = "slimypersuits"
poi_id_mine = "themines"
poi_id_mine_sweeper = "theminessweeper"
poi_id_mine_bubble = "theminesbubble"
poi_id_thecasino = "thecasino"
poi_id_711 = "outsidethe711"
poi_id_speakeasy = "thekingswifessonspeakeasy"
poi_id_dojo = "thedojo"
poi_id_arena = "thebattlearena"
poi_id_nlacu = "newlosangelescityuniversity"
poi_id_foodcourt = "thefoodcourt"
poi_id_cinema = "nlacakanmcinemas"
poi_id_bazaar = "thebazaar"
poi_id_recyclingplant = "recyclingplant"
poi_id_stockexchange = "theslimestockexchange"
poi_id_endlesswar = "endlesswar"
poi_id_slimecorphq = "slimecorphq"
poi_id_cv_mines = "cratersvillemines"
poi_id_cv_mines_sweeper = "cratersvilleminessweeper"
poi_id_cv_mines_bubble = "cratersvilleminesbubble"
poi_id_tt_mines = "toxingtonmines"
poi_id_tt_mines_sweeper = "toxingtonminessweeper"
poi_id_tt_mines_bubble = "toxingtonminesbubble"
poi_id_diner = "smokerscough"
poi_id_seafood = "redmobster"
poi_id_jr_farms = "juviesrowfarms"
poi_id_og_farms = "oozegardensfarms"
poi_id_ab_farms = "arsonbrookfarms"
poi_id_neomilwaukeestate = "neomilwaukeestate"
poi_id_beachresort = "thebeachresort"
poi_id_countryclub = "thecountryclub"
poi_id_slimesea = "slimesea"
poi_id_slimesendcliffs = "slimesendcliffs"
poi_id_greencakecafe = "greencakecafe"
poi_id_sodafountain = "sodafountain"
poi_id_bodega = "bodega"
poi_id_wafflehouse = "wafflehouse"
poi_id_blackpond = "blackpond"
poi_id_basedhardware = "basedhardware"
poi_id_clinicofslimoplasty = "clinicofslimoplasty"
poi_id_thebreakroom = "thebreakroom"
poi_id_underworld = "underworld"

# transports
poi_id_ferry = "ferry"
poi_id_subway_pink01 = "subwaypink01"
poi_id_subway_pink02 = "subwaypink02"
poi_id_subway_gold01 = "subwaygold01"
poi_id_subway_gold02 = "subwaygold02"
poi_id_subway_green01 = "subwaygreen01"
poi_id_subway_green02 = "subwaygreen02"
poi_id_subway_black01 = "subwayblack01"
poi_id_subway_black02 = "subwayblack01"
poi_id_subway_purple01 = "subwaypurple01"
poi_id_subway_purple02 = "subwaypurple02"
poi_id_blimp = "blimp"
poi_id_apt = "apt"

# ferry ports
poi_id_wt_port = "wreckingtonport"
poi_id_vc_port = "vagrantscornerport"

# subway stations
poi_id_tt_subway_station = "toxingtonsubwaystation"
poi_id_ah_subway_station = "astatineheightssubwaystation"
poi_id_gd_subway_station = "gatlingsdalesubwaystation"
poi_id_ck_subway_station = "copkilltownsubwaystation"
poi_id_ab_subway_station = "arsonbrooksubwaystation"
poi_id_sb_subway_station = "smogsburgsubwaystation"
poi_id_dt_subway_station = "downtownsubwaystation"
poi_id_kb_subway_station = "krakbaysubwaystation"
poi_id_gb_subway_station = "glocksburysubwaystation"
poi_id_wgb_subway_station = "westglocksburysubwaystation"
poi_id_jp_subway_station = "jaywalkerplainsubwaystation"
poi_id_nsb_subway_station = "northsleezesubwaystation"
poi_id_ssb_subway_station = "southsleezesubwaystation"
poi_id_bd_subway_station = "brawldensubwaystation"
poi_id_cv_subway_station = "cratersvillesubwaystation"
poi_id_wt_subway_station = "wreckingtonsubwaystation"
poi_id_rr_subway_station = "rowdyroughhousesubwaystation"
poi_id_gld_subway_station = "greenlightsubwaystation"
poi_id_jr_subway_station = "juviesrowsubwaystation"
poi_id_vc_subway_station = "vagrantscornersubwaystation"
poi_id_afb_subway_station = "assaultflatssubwaystation"
poi_id_vp_subway_station = "vandalparksubwaystation"
poi_id_pa_subway_station = "poudrinalleysubwaystation"
poi_id_og_subway_station = "oozegardenssubwaystation"
poi_id_cl_subway_station = "crooklinesubwaystation"
poi_id_lc_subway_station = "littlechernobylsubwaystation"
poi_id_bd_subway_station = "brawldensubwaystation"
poi_id_nny_subway_station = "newnewyonkerssubwaystation"


poi_id_underworld_subway_station = "underworldsubwaystation"

# ferry ports
poi_id_df_blimp_tower = "dreadfordblimptower"
poi_id_afb_blimp_tower = "assaultflatsblimptower"

# district pois
poi_id_downtown = "downtown"
poi_id_smogsburg = "smogsburg"
poi_id_copkilltown = "copkilltown"
poi_id_krakbay = "krakbay"
poi_id_poudrinalley = "poudrinalley"
poi_id_rowdyroughhouse = "rowdyroughhouse"
poi_id_greenlightdistrict = "greenlightdistrict"
poi_id_oldnewyonkers = "oldnewyonkers"
poi_id_littlechernobyl = "littlechernobyl"
poi_id_arsonbrook = "arsonbrook"
poi_id_astatineheights = "astatineheights"
poi_id_gatlingsdale = "gatlingsdale"
poi_id_vandalpark = "vandalpark"
poi_id_glocksbury = "glocksbury"
poi_id_northsleezeborough = "northsleezeborough"
poi_id_southsleezeborough = "southsleezeborough"
poi_id_oozegardens = "oozegardens"
poi_id_cratersville = "cratersville"
poi_id_wreckington = "wreckington"
poi_id_juviesrow = "juviesrow"
poi_id_slimesend = "slimesend"
poi_id_vagrantscorner = "vagrantscorner"
poi_id_assaultflatsbeach = "assaultflatsbeach"
poi_id_newnewyonkers = "newnewyonkers"
poi_id_brawlden = "brawlden"
poi_id_toxington = "toxington"
poi_id_charcoalpark = "charcoalpark"
poi_id_poloniumhill = "poloniumhill"
poi_id_westglocksbury = "westglocksbury"
poi_id_jaywalkerplain = "jaywalkerplain"
poi_id_crookline = "crookline"
poi_id_dreadford = "dreadford"
poi_id_maimridge = "maimridge"
poi_id_thevoid = "thevoid"

poi_id_toxington_pier = "toxingtonpier"
poi_id_jaywalkerplain_pier = "jaywalkerplainpier"
poi_id_crookline_pier = "crooklinepier"
poi_id_assaultflatsbeach_pier = "assaultflatsbeachpier"
poi_id_vagrantscorner_pier = "vagrantscornerpier" # NOT USED
poi_id_slimesend_pier = "slimesendpier"
poi_id_juviesrow_pier = "juviesrowpier"

#Apartment subzones
poi_id_apt_downtown ="aptdowntown"
poi_id_apt_smogsburg ="aptsmogsburg"
poi_id_apt_krakbay = "aptkrakbay"
poi_id_apt_poudrinalley = "aptpoudrinalley"
poi_id_apt_greenlightdistrict = "aptgreenlightdistrict"
poi_id_apt_oldnewyonkers = "aptoldnewyonkers"
poi_id_apt_littlechernobyl = "aptlittlechernobyl"
poi_id_apt_arsonbrook = "aptarsonbrook"
poi_id_apt_astatineheights = "aptastatineheights"
poi_id_apt_gatlingsdale = "aptgatlingsdale"
poi_id_apt_vandalpark = "aptvandalpark"
poi_id_apt_glocksbury = "aptglocksbury"
poi_id_apt_northsleezeborough = "aptnorthsleezeborough"
poi_id_apt_southsleezeborough = "aptsouthsleezeborough"
poi_id_apt_oozegardens = "aptoozegardens"
poi_id_apt_cratersville = "aptcratersville"
poi_id_apt_wreckington = "aptwreckington"
poi_id_apt_slimesend = "aptslimesend"
poi_id_apt_vagrantscorner = "aptvagrantscorner"
poi_id_apt_assaultflatsbeach = "aptassaultflatsbeach"
poi_id_apt_newnewyonkers = "aptnewnewyonkers"
poi_id_apt_brawlden = "aptbrawlden"
poi_id_apt_toxington = "apttoxington"
poi_id_apt_charcoalpark = "aptcharcoalpark"
poi_id_apt_poloniumhill = "aptpoloniumhill"
poi_id_apt_westglocksbury = "aptwestglocksbury"
poi_id_apt_jaywalkerplain = "aptjaywalkerplain"
poi_id_apt_crookline = "aptcrookline"
poi_id_apt_dreadford = "aptdreadford"
poi_id_apt_maimridge = "aptmaimridge"

# The streets -- There are 123 of them, to be exact
poi_id_copkilltown_street_a = "copkilltownstreeta" # NOT USED
poi_id_rowdyroughhouse_street_a = "rowdyroughhousestreeta" # NOT USED
poi_id_juviesrow_street_a = "juviesrowstreeta" # NOT USED

poi_id_downtown_street_a = "downtownstreeta"
poi_id_downtown_street_b = "downtownstreetb"
poi_id_downtown_street_c = "downtownstreetc"
poi_id_downtown_street_d = "downtownstreetd"
poi_id_downtown_street_e = "downtownstreete"
poi_id_downtown_street_f = "downtownstreetf"

poi_id_krakbay_street_a = "krakbaystreeta"
poi_id_krakbay_street_b = "krakbaystreetb"
poi_id_krakbay_street_c = "krakbaystreetc"
poi_id_krakbay_street_d = "krakbaystreetd"
poi_id_krakbay_street_e = "krakbaystreete"
poi_id_krakbay_street_f = "krakbaystreetf"

poi_id_poudrinalley_street_a = "poudrinalleystreeta" 
poi_id_poudrinalley_street_b = "poudrinalleystreetb"
poi_id_poudrinalley_street_c = "poudrinalleystreetc"
poi_id_poudrinalley_street_d = "poudrinalleystreetd"
poi_id_poudrinalley_street_e = "poudrinalleystreete"

poi_id_cratersville_street_a = "cratersvillestreeta"
poi_id_cratersville_street_b = "cratersvillestreetb"
poi_id_cratersville_street_c = "cratersvillestreetc"

poi_id_wreckington_street_a = "wreckingtonstreeta"
poi_id_wreckington_street_b = "wreckingtonstreetb"

poi_id_oozegardens_street_a = "oozegardensstreeta"
poi_id_oozegardens_street_b = "oozegardensstreetb"
poi_id_oozegardens_street_c = "oozegardensstreetc"
poi_id_oozegardens_street_d = "oozegardensstreetd"

poi_id_southsleezeborough_street_a = "southsleezeboroughstreeta" 
poi_id_southsleezeborough_street_b = "southsleezeboroughstreetb"
poi_id_southsleezeborough_street_c = "southsleezeboroughstreetc"
poi_id_southsleezeborough_street_d = "southsleezeboroughstreetd"

poi_id_northsleezeborough_street_a = "northsleezeboroughstreeta"
poi_id_northsleezeborough_street_b = "northsleezeboroughstreetb"
poi_id_northsleezeborough_street_c = "northsleezeboroughstreetc"
poi_id_northsleezeborough_street_d = "northsleezeboroughstreetd"
poi_id_northsleezeborough_street_e = "northsleezeboroughstreete"

poi_id_glocksbury_street_a = "glocksburystreeta"
poi_id_glocksbury_street_b = "glocksburystreetb"
poi_id_glocksbury_street_c = "glocksburystreetc"
poi_id_glocksbury_street_d = "glocksburystreetd"
poi_id_glocksbury_street_e = "glocksburystreete"

poi_id_westglocksbury_street_a = "westglocksburystreeta" 
poi_id_westglocksbury_street_b = "westglocksburystreetb"
poi_id_westglocksbury_street_c = "westglocksburystreetc"
poi_id_westglocksbury_street_d = "westglocksburystreetd"

poi_id_jaywalkerplain_street_a = "jaywalkerplainstreeta"
poi_id_jaywalkerplain_street_b = "jaywalkerplainstreetb"
poi_id_jaywalkerplain_street_c = "jaywalkerplainstreetc"
poi_id_jaywalkerplain_street_d = "jaywalkerplainstreetd"
poi_id_jaywalkerplain_street_e = "jaywalkerplainstreete"

poi_id_crookline_street_a = "crooklinestreeta" 
poi_id_crookline_street_b = "crooklinestreetb"
poi_id_crookline_street_c = "crooklinestreetc"
poi_id_crookline_street_d = "crooklinestreetd"

poi_id_dreadford_street_a = "dreadfordstreeta"
poi_id_dreadford_street_b = "dreadfordstreetb"

poi_id_vandalpark_street_a = "vandalparkstreeta"
poi_id_vandalpark_street_b = "vandalparkstreetb"
poi_id_vandalpark_street_c = "vandalparkstreetc"
poi_id_vandalpark_street_d = "vandalparkstreetd"

poi_id_poloniumhill_street_a = "poloniumhillstreeta"
poi_id_poloniumhill_street_b = "poloniumhillstreetb"
poi_id_poloniumhill_street_c = "poloniumhillstreetc"
poi_id_poloniumhill_street_d = "poloniumhillstreetd"
poi_id_poloniumhill_street_e = "poloniumhillstreete"

poi_id_charcoalpark_street_a = "charcoalparkstreeta" 
poi_id_charcoalpark_street_b = "charcoalparkstreetb"

poi_id_toxington_street_a = "toxingtonstreeta"
poi_id_toxington_street_b = "toxingtonstreetb"
poi_id_toxington_street_c = "toxingtonstreetc"
poi_id_toxington_street_d = "toxingtonstreetd"
poi_id_toxington_street_e = "toxingtonstreete"

poi_id_gatlingsdale_street_a = "gatlingsdalestreeta" 
poi_id_gatlingsdale_street_b = "gatlingsdalestreetb"
poi_id_gatlingsdale_street_c = "gatlingsdalestreetc"
poi_id_gatlingsdale_street_d = "gatlingsdalestreetd"
poi_id_gatlingsdale_street_e = "gatlingsdalestreete"

poi_id_astatineheights_street_a = "astatineheightsstreeta"
poi_id_astatineheights_street_b = "astatineheightsstreetb"
poi_id_astatineheights_street_c = "astatineheightsstreetc"
poi_id_astatineheights_street_d = "astatineheightsstreetd"
poi_id_astatineheights_street_e = "astatineheightsstreete"
poi_id_astatineheights_street_f = "astatineheightsstreetf"

poi_id_smogsburg_street_a = "smogsburgstreeta" 
poi_id_smogsburg_street_b = "smogsburgstreetb"
poi_id_smogsburg_street_c = "smogsburgstreetc"
poi_id_smogsburg_street_d = "smogsburgstreetd"
poi_id_smogsburg_street_e = "smogsburgstreete"

poi_id_arsonbrook_street_a = "arsonbrookstreeta"
poi_id_arsonbrook_street_b = "arsonbrookstreetb"
poi_id_arsonbrook_street_c = "arsonbrookstreetc"
poi_id_arsonbrook_street_d = "arsonbrookstreetd"
poi_id_arsonbrook_street_e = "arsonbrookstreete"

poi_id_maimridge_street_a = "maimridgestreeta"
poi_id_maimridge_street_b = "maimridgestreetb"
poi_id_maimridge_street_c = "maimridgestreetc"

poi_id_brawlden_street_a = "brawldenstreeta" 
poi_id_brawlden_street_b = "brawldenstreetb"
poi_id_brawlden_street_c = "brawldenstreetc"
poi_id_brawlden_street_d = "brawldenstreetd"

poi_id_littlechernobyl_street_a = "littlechernobylstreeta"
poi_id_littlechernobyl_street_b = "littlechernobylstreetb"
poi_id_littlechernobyl_street_c = "littlechernobylstreetc"

poi_id_oldnewyonkers_street_a = "oldnewyonkersstreeta"
poi_id_oldnewyonkers_street_b = "oldnewyonkersstreetb"
poi_id_oldnewyonkers_street_c = "oldnewyonkersstreetc"
poi_id_oldnewyonkers_street_d = "oldnewyonkersstreetd"
poi_id_oldnewyonkers_street_e = "oldnewyonkersstreete"

poi_id_newnewyonkers_street_a = "newnewyonkersstreeta"
poi_id_newnewyonkers_street_b = "newnewyonkersstreetb"
poi_id_newnewyonkers_street_c = "newnewyonkersstreetc"
poi_id_newnewyonkers_street_d = "newnewyonkersstreetd"

poi_id_assaultflatsbeach_street_a = "assaultflatsbeachstreeta"
poi_id_assaultflatsbeach_street_b = "assaultflatsbeachstreetb"

poi_id_vagrantscorner_street_a = "vagrantscornerstreeta" 
poi_id_vagrantscorner_street_b = "vagrantscornerstreetb"
poi_id_vagrantscorner_street_c = "vagrantscornerstreetc"
poi_id_vagrantscorner_street_d = "vagrantscornerstreetd"
poi_id_vagrantscorner_street_e = "vagrantscornerstreete"
poi_id_vagrantscorner_street_f = "vagrantscornerstreetf"

poi_id_greenlightdistrict_street_a = "greenlightdistrictstreeta"
poi_id_greenlightdistrict_street_b = "greenlightdistrictstreetb"
poi_id_greenlightdistrict_street_c = "greenlightdistrictstreetc"

poi_id_slimesend_street_a = "slimesendstreeta"

# Tutorial zones
poi_id_tutorial_classroom = "classroom"
poi_id_tutorial_ghostcontainment = "ghostcontainment"
poi_id_tutorial_hallway = "hallway"

compartment_id_closet = "closet"
compartment_id_fridge = "fridge"
compartment_id_decorate = "decorate"
compartment_id_bookshelf = "bookshelf"
location_id_empty = "empty"

# Outskirts
# Layer 1
poi_id_south_outskirts_edge = "southoutskirtsedge"
poi_id_southwest_outskirts_edge = "southwestoutskirtsedge"
poi_id_west_outskirts_edge = "westoutskirtsedge"
poi_id_northwest_outskirts_edge = "northwestoutskirtsedge"
poi_id_north_outskirts_edge = "northoutskirtsedge"
poi_id_nuclear_beach_edge = "nuclearbeachedge" # aka Assault Flats Beach Outskirts Edge
# Layer 2
poi_id_south_outskirts = "southoutskirts"
poi_id_southwest_outskirts = "southwestoutskirts"
poi_id_west_outskirts = "westoutskirts"
poi_id_northwest_outskirts = "northwestoutskirts"
poi_id_north_outskirts = "northoutskirts"
poi_id_nuclear_beach = "nuclearbeach"
# Layer 3
poi_id_south_outskirts_depths = "southoutskirtsdepths"
poi_id_southwest_outskirts_depths = "southwestoutskirtsdepths"
poi_id_west_outskirts_depths = "westoutskirtsdepths"
poi_id_northwest_outskirts_depths = "northwestoutskirtsdepths"
poi_id_north_outskirts_depths = "northoutskirtsdepths"
poi_id_nuclear_beach_depths = "nuclearbeachdepths" 

# The Sphere
poi_id_thesphere = "thesphere"

# Community Chests
chest_id_copkilltown = "copkilltownchest"
chest_id_rowdyroughhouse = "rowdyroughhousechest"
chest_id_juviesrow = "juviesrowchest"
chest_id_thesewers = "sewerschest"
chest_id_breakroom = "breakroomchest"

# Transport types
transport_type_ferry = "ferry"
transport_type_subway = "subway"
transport_type_blimp = "blimp"

# Ferry lines
transport_line_ferry_wt_to_vc = "ferrywttovc"
transport_line_ferry_vc_to_wt = "ferryvctowt"

# Subway lines
transport_line_subway_yellow_northbound = "subwayyellownorth"
transport_line_subway_yellow_southbound = "subwayyellowsouth"

transport_line_subway_red_northbound = "subwayrednorth"
transport_line_subway_red_southbound = "subwayredsouth"

transport_line_subway_blue_eastbound = "subwayblueeast"
transport_line_subway_blue_westbound = "subwaybluewest"

transport_line_subway_white_eastbound = "subwaywhiteeast"
transport_line_subway_white_westbound = "subwaywhitewest"

transport_line_subway_green_eastbound = "subwaygreeneast"
transport_line_subway_green_westbound = "subwaygreenwest"

# Blimp lines
transport_line_blimp_df_to_afb = "blimpdftoafb"
transport_line_blimp_afb_to_df = "blimpafbtodf"


# Role names. All lower case with no spaces.
role_juvenile = "juveniles"
role_juvenile_pvp = "juvenilewanted"
role_juvenile_active = "juvenileotp"
role_rowdyfucker = "rowdyfucker"
role_rowdyfuckers = "rowdys"
role_rowdyfuckers_pvp = "rowdywanted"
role_rowdyfuckers_active = "rowdyotp"
role_copkiller = "copkiller"
role_copkillers = "killers"
role_copkillers_pvp = "killerwanted"
role_copkillers_active = "killerotp"
role_corpse = "corpse"
role_corpse_pvp = "corpsewanted"
role_corpse_active = "corpseotp"
role_shambler = "shamblers"
role_kingpin = "kingpin"
role_grandfoe = "grandfoe"
role_slimecorp = "slimecorp"
role_slimecorp_pvp = "slimecorpvulnerable"
role_slimecorp_active = "slimecorpotp"
role_executive = "executive"
role_deathfurnace = "deathfurnace"
role_donor = "terezigang"
role_tutorial = "newintown"
role_slimernalia = "kingpinofslimernalia"
role_gellphone = "gellphone"
role_null_major_role = "nullmajorrole"
role_null_minor_role = "nullminorrole"

permission_read_messages = "read"
permission_send_messages = "send"
permission_connect_to_voice = "connect"
#permission_see_history = "history"
#permission_upload_files = "upload" -- everything else including this should be true by default. 
# Read, Send, and History should be false by default but set to true.

permissions_general = [permission_read_messages, permission_send_messages, permission_connect_to_voice]

faction_roles = [
	role_juvenile,
	role_juvenile_pvp,
	role_juvenile_active,
	role_rowdyfucker,
	role_rowdyfuckers,
	role_rowdyfuckers_pvp,
	role_rowdyfuckers_active,
	role_copkiller,
	role_copkillers,
	role_copkillers_pvp,
	role_copkillers_active,
	role_executive,
	role_slimecorp,
	role_slimecorp_pvp,
	role_slimecorp_active,
	role_corpse,
	role_corpse_pvp,
	role_corpse_active,
	role_kingpin,
	role_grandfoe,
	role_tutorial,
	role_shambler,
	]

role_to_pvp_role = {
	role_juvenile : role_juvenile_pvp,
	role_rowdyfuckers : role_rowdyfuckers_pvp,
	role_copkillers : role_copkillers_pvp,
	role_corpse : role_corpse_pvp,
	role_slimecorp : role_slimecorp_pvp
	}

role_to_active_role = {
	role_juvenile : role_juvenile_active,
	role_rowdyfuckers : role_rowdyfuckers_active,
	role_copkillers : role_copkillers_active,
	role_corpse : role_corpse_active,
	role_slimecorp : role_slimecorp_active
	}

misc_roles = {
	role_slimernalia,
	role_gellphone
}

# used for checking if a user has the donor role
role_donor_proper = "Terezi Gang"

# used for checking if a user has the gellphone role
role_gellphone_proper = "Gellphone"

# Faction names and bases
faction_killers = "killers"
gangbase_killers = "Cop Killtown"
faction_rowdys = "rowdys"
gangbase_rowdys = "Rowdy Roughhouse"
faction_slimecorp = "slimecorp"
gangbase_slimecorp = "The Breakroom"
faction_banned = "banned"
factions = [faction_killers, faction_rowdys, faction_slimecorp]
psuedo_faction_gankers = 'gankers' # not attatched to a user's data
psuedo_faction_shamblers = 'shamblers' # same as above

# Channel names
channel_mines = "the-mines"
channel_mines_sweeper = "the-mines-minesweeper"
channel_mines_bubble = "the-mines-bubble-breaker"
channel_downtown = "downtown"
channel_combatzone = "combat-zone"
channel_endlesswar = "endless-war"
channel_sewers = "the-sewers"
channel_dojo = "the-dojo"
channel_twitch_announcement = "rfck-chat"
channel_casino = "slimecorp-casino"
channel_stockexchange = "slimecorp-stock-exchange"
channel_foodcourt = "food-court"
channel_slimeoidlab = "slimecorp-labs"
channel_711 = "outside-the-7-11"
channel_speakeasy = "speakeasy"
channel_arena = "battle-arena"
channel_nlacu = "nlac-university"
channel_cinema = "nlacakanm-cinemas"
channel_bazaar = "bazaar"
channel_recyclingplant = "slimecorp-recycling-plant"
channel_slimecorphq = "slimecorp-hq"
channel_leaderboard = "leaderboard"
channel_cv_mines = "cratersville-mines"
channel_cv_mines_sweeper = "cratersville-mines-minesweeper"
channel_cv_mines_bubble = "cratersville-mines-bubble-breaker"
channel_tt_mines = "toxington-mines"
channel_tt_mines_sweeper = "toxington-mines-minesweeper"
channel_tt_mines_bubble = "toxington-mines-bubble-breaker"
channel_diner = "smokers-cough"
channel_seafood = "red-mobster"
channel_jr_farms = "juvies-row-farms"
channel_og_farms = "ooze-gardens-farms"
channel_ab_farms = "arsonbrook-farms"
channel_neomilwaukeestate = "neo-milwaukee-state"
channel_beachresort = "the-resort"
channel_countryclub = "the-country-club"
channel_rowdyroughhouse = "rowdy-roughhouse"
channel_copkilltown = "cop-killtown"
channel_slimesea = "slime-sea"
channel_tt_pier = "toxington-pier"
channel_jp_pier = "jaywalker-plain-pier"
channel_cl_pier = "crookline-pier"
channel_afb_pier = "assault-flats-beach-pier"
channel_vc_pier = "vagrants-corner-pier"
channel_se_pier = "slimes-end-pier"
channel_jr_pier = "juvies-row-pier"
channel_juviesrow = "juvies-row"
channel_realestateagency = "slimecorp-real-estate-agency"
channel_apt = "apartment"
channel_sodafountain = "the-bicarbonate-soda-fountain"
channel_greencakecafe = "green-cake-cafe"
channel_glocksburycomics = "glocksbury-comics"
channel_breakroom = "the-breakroom"

channel_wt_port = "wreckington-port"
channel_vc_port = "vagrants-corner-port"
channel_tt_subway_station = "toxington-subway-station"
channel_ah_subway_station = "astatine-heights-subway-station"
channel_gd_subway_station = "gatlingsdale-subway-station"
channel_ck_subway_station = "cop-killtown-subway-station"
channel_ab_subway_station = "arsonbrook-subway-station"
channel_sb_subway_station = "smogsburg-subway-station"
channel_dt_subway_station = "downtown-subway-station"
channel_kb_subway_station = "krak-bay-subway-station"
channel_gb_subway_station = "glocksbury-subway-station"
channel_wgb_subway_station = "west-glocksbury-subway-station"
channel_jp_subway_station = "jaywalker-plain-subway-station"
channel_nsb_subway_station = "north-sleeze-subway-station"
channel_ssb_subway_station = "south-sleeze-subway-station"
channel_cv_subway_station = "cratersville-subway-station"
channel_wt_subway_station = "wreckington-subway-station"
channel_rr_subway_station = "rowdy-roughhouse-subway-station"
channel_gld_subway_station = "green-light-subway-station"
channel_jr_subway_station = "juvies-row-subway-station"
channel_vc_subway_station = "vagrants-corner-subway-station"
channel_afb_subway_station = "assault-flats-subway-station"
channel_vp_subway_station = "vandal-park-subway-station"
channel_pa_subway_station = "poudrin-alley-subway-station"
channel_og_subway_station = "ooze-gardens-subway-station"
channel_cl_subway_station = "crookline-subway-station"
channel_lc_subway_station = "little-chernobyl-subway-station"
channel_bd_subway_station = "brawlden-subway-station"
channel_nny_subway_station = "new-new-yonkers-subway-station"
channel_df_blimp_tower = "dreadford-blimp-tower"
channel_afb_blimp_tower = "assault-flats-blimp-tower"

channel_ferry = "ferry"
channel_subway_pink01 = "subway-train-pink-01"
channel_subway_pink02 = "subway-train-pink-02"
channel_subway_gold01 = "subway-train-gold-01"
channel_subway_gold02 = "subway-train-gold-02"
channel_subway_green01 = "subway-train-green-01"
channel_subway_green02 = "subway-train-green-02"
channel_subway_black01 = "subway-train-black-01"
channel_subway_black02 = "subway-train-black-02"
channel_subway_purple01 = "subway-train-purple-01"
channel_subway_purple02 = "subway-train-purple-02"
channel_blimp = "blimp"

channel_killfeed = "kill-feed"
channel_jrmineswall_sweeper = "the-mines-wall-minesweeper"
channel_ttmineswall_sweeper = "toxington-mines-wall-minesweeper"
channel_cvmineswall_sweeper = "cratersville-mines-wall-minesweeper"
channel_jrmineswall_bubble = "the-mines-wall-bubble-breaker"
channel_ttmineswall_bubble = "toxington-mines-wall-bubble-breaker"
channel_cvmineswall_bubble = "cratersville-mines-wall-bubble-breaker"

channel_apt_downtown = "downtown-apartments"
channel_apt_smogsburg ="smogsburg-apartments"
channel_apt_krakbay ="krak-bay-apartments"
channel_apt_poudrinalley ="poudrin-alley-apartments"
channel_apt_greenlightdistrict ="green-light-district-apartments"
channel_apt_oldnewyonkers ="old-new-yonkers-apartments"
channel_apt_littlechernobyl ="little-chernobyl-apartments"
channel_apt_arsonbrook ="arsonbrook-apartments"
channel_apt_astatineheights ="astatine-heights-apartments"
channel_apt_gatlingsdale ="gatlingsdale-apartments"
channel_apt_vandalpark ="vandal-park-apartments"
channel_apt_glocksbury ="glocksbury-apartments"
channel_apt_northsleezeborough ="north-sleezeborough-apartments"
channel_apt_southsleezeborough ="south-sleezeborough-apartments"
channel_apt_oozegardens ="ooze-gardens-apartments"
channel_apt_cratersville ="cratersville-apartments"
channel_apt_wreckington ="wreckington-apartments"
channel_apt_slimesend ="slimes-end-apartments"
channel_apt_vagrantscorner ="vagrants-corner-apartments"
channel_apt_assaultflatsbeach ="assault-flats-beach-apartments"
channel_apt_newnewyonkers ="new-new-yonkers-apartments"
channel_apt_brawlden ="brawlden-apartments"
channel_apt_toxington ="toxington-apartments"
channel_apt_charcoalpark ="charcoal-park-apartments"
channel_apt_poloniumhill ="polonium-hill-apartments"
channel_apt_westglocksbury ="west-glocksbury-apartments"
channel_apt_jaywalkerplain ="jaywalker-plain-apartments"
channel_apt_crookline ="crookline-apartments"
channel_apt_dreadford ="dreadford-apartments"
channel_apt_maimrdige ="maimridge-apartments"

channel_slimesendcliffs = "slimes-end-cliffs"
channel_bodega = "bodega"
channel_wafflehouse = "wafflehouse"
channel_blackpond = "blackpond"
channel_basedhardware = "based-hardware"
channel_clinicofslimoplasty = "clinic-of-slimoplasty"
channel_atomicforest = "atomic-forest"
channel_downpourlaboratory = "downpour-laboratory"

channel_prankfeed = "prank-feed"

# Placeholders
channel_copkilltown_street_a = "cop-killtown-street-a"
channel_rowdyroughhouse_street_a = "rowdy-roughhouse-street-a"
channel_juviesrow_street_a = "juvies-row-street-a"
channel_downtown_street_a = "downtown-street-a"
channel_downtown_street_b = "downtown-street-b"
channel_downtown_street_c = "downtown-street-c"
channel_downtown_street_d = "downtown-street-d"
channel_downtown_street_e = "downtown-street-e"
channel_downtown_street_f = "downtown-street-f"
channel_krakbay_street_a = "krak-bay-street-a"
channel_krakbay_street_b = "krak-bay-street-b"
channel_krakbay_street_c = "krak-bay-street-c"
channel_krakbay_street_d = "krak-bay-street-d"
channel_krakbay_street_e = "krak-bay-street-e"
channel_krakbay_street_f = "krak-bay-street-f"
channel_poudrinalley_street_a = "poudrin-alley-street-a" 
channel_poudrinalley_street_b = "poudrin-alley-street-b"
channel_poudrinalley_street_c = "poudrin-alley-street-c"
channel_poudrinalley_street_d = "poudrin-alley-street-d"
channel_poudrinalley_street_e = "poudrin-alley-street-e"
channel_cratersville_street_a = "cratersville-street-a"
channel_cratersville_street_b = "cratersville-street-b"
channel_cratersville_street_c = "cratersville-street-c"
channel_wreckington_street_a = "wreckington-street-a"
channel_wreckington_street_b = "wreckington-street-b"
channel_oozegardens_street_a = "ooze-gardens-street-a"
channel_oozegardens_street_b = "ooze-gardens-street-b"
channel_oozegardens_street_c = "ooze-gardens-street-c"
channel_oozegardens_street_d = "ooze-gardens-street-d"
channel_southsleezeborough_street_a = "south-sleezeborough-street-a" 
channel_southsleezeborough_street_b = "south-sleezeborough-street-b"
channel_southsleezeborough_street_c = "south-sleezeborough-street-c"
channel_southsleezeborough_street_d = "south-sleezeborough-street-d"
channel_northsleezeborough_street_a = "north-sleezeborough-street-a"
channel_northsleezeborough_street_b = "north-sleezeborough-street-b"
channel_northsleezeborough_street_c = "north-sleezeborough-street-c"
channel_northsleezeborough_street_d = "north-sleezeborough-street-d"
channel_northsleezeborough_street_e = "north-sleezeborough-street-e"
channel_glocksbury_street_a = "glocksbury-street-a"
channel_glocksbury_street_b = "glocksbury-street-b"
channel_glocksbury_street_c = "glocksbury-street-c"
channel_glocksbury_street_d = "glocksbury-street-d"
channel_glocksbury_street_e = "glocksbury-street-e"
channel_westglocksbury_street_a = "west-glocksbury-street-a" 
channel_westglocksbury_street_b = "west-glocksbury-street-b"
channel_westglocksbury_street_c = "west-glocksbury-street-c"
channel_westglocksbury_street_d = "west-glocksbury-street-d"
channel_jaywalkerplain_street_a = "jaywalker-plain-street-a"
channel_jaywalkerplain_street_b = "jaywalker-plain-street-b"
channel_jaywalkerplain_street_c = "jaywalker-plain-street-c"
channel_jaywalkerplain_street_d = "jaywalker-plain-street-d"
channel_jaywalkerplain_street_e = "jaywalker-plain-street-e"
channel_crookline_street_a = "crookline-street-a" 
channel_crookline_street_b = "crookline-street-b"
channel_crookline_street_c = "crookline-street-c"
channel_crookline_street_d = "crookline-street-d"
channel_dreadford_street_a = "dreadford-street-a"
channel_dreadford_street_b = "dreadford-street-b"
channel_vandalpark_street_a = "vandal-park-street-a"
channel_vandalpark_street_b = "vandal-park-street-b"
channel_vandalpark_street_c = "vandal-park-street-c"
channel_vandalpark_street_d = "vandal-park-street-d"
channel_poloniumhill_street_a = "polonium-hill-street-a"
channel_poloniumhill_street_b = "polonium-hill-street-b"
channel_poloniumhill_street_c = "polonium-hill-street-c"
channel_poloniumhill_street_d = "polonium-hill-street-d"
channel_poloniumhill_street_e = "polonium-hill-street-e"
channel_charcoalpark_street_a = "charcoal-park-street-a" 
channel_charcoalpark_street_b = "charcoal-park-street-b"
channel_toxington_street_a = "toxington-street-a"
channel_toxington_street_b = "toxington-street-b"
channel_toxington_street_c = "toxington-street-c"
channel_toxington_street_d = "toxington-street-d"
channel_toxington_street_e = "toxington-street-e"
channel_gatlingsdale_street_a = "gatlingsdale-street-a" 
channel_gatlingsdale_street_b = "gatlingsdale-street-b"
channel_gatlingsdale_street_c = "gatlingsdale-street-c"
channel_gatlingsdale_street_d = "gatlingsdale-street-d"
channel_gatlingsdale_street_e = "gatlingsdale-street-e"
channel_astatineheights_street_a = "astatine-heights-street-a"
channel_astatineheights_street_b = "astatine-heights-street-b"
channel_astatineheights_street_c = "astatine-heights-street-c"
channel_astatineheights_street_d = "astatine-heights-street-d"
channel_astatineheights_street_e = "astatine-heights-street-e"
channel_astatineheights_street_f = "astatine-heights-street-f"
channel_smogsburg_street_a = "smogsburg-street-a" 
channel_smogsburg_street_b = "smogsburg-street-b"
channel_smogsburg_street_c = "smogsburg-street-c"
channel_smogsburg_street_d = "smogsburg-street-d"
channel_smogsburg_street_e = "smogsburg-street-e"
channel_arsonbrook_street_a = "arsonbrook-street-a"
channel_arsonbrook_street_b = "arsonbrook-street-b"
channel_arsonbrook_street_c = "arsonbrook-street-c"
channel_arsonbrook_street_d = "arsonbrook-street-d"
channel_arsonbrook_street_e = "arsonbrook-street-e"
channel_maimridge_street_a = "maimridge-street-a"
channel_maimridge_street_b = "maimridge-street-b"
channel_maimridge_street_c = "maimridge-street-c"
channel_brawlden_street_a = "brawlden-street-a" 
channel_brawlden_street_b = "brawlden-street-b"
channel_brawlden_street_c = "brawlden-street-c"
channel_brawlden_street_d = "brawlden-street-d"
channel_littlechernobyl_street_a = "little-chernobyl-street-a"
channel_littlechernobyl_street_b = "little-chernobyl-street-b"
channel_littlechernobyl_street_c = "little-chernobyl-street-c"
channel_oldnewyonkers_street_a = "old-new-yonkers-street-a"
channel_oldnewyonkers_street_b = "old-new-yonkers-street-b"
channel_oldnewyonkers_street_c = "old-new-yonkers-street-c"
channel_oldnewyonkers_street_d = "old-new-yonkers-street-d"
channel_oldnewyonkers_street_e = "old-new-yonkers-street-e"
channel_newnewyonkers_street_a = "new-new-yonkers-street-a"
channel_newnewyonkers_street_b = "new-new-yonkers-street-b"
channel_newnewyonkers_street_c = "new-new-yonkers-street-c"
channel_newnewyonkers_street_d = "new-new-yonkers-street-d"
channel_assaultflatsbeach_street_a = "assault-flats-beach-street-a"
channel_assaultflatsbeach_street_b = "assault-flats-beach-street-b"
channel_vagrantscorner_street_a = "vagrants-corner-street-a" 
channel_vagrantscorner_street_b = "vagrants-corner-street-b"
channel_vagrantscorner_street_c = "vagrants-corner-street-c"
channel_vagrantscorner_street_d = "vagrants-corner-street-d"
channel_vagrantscorner_street_e = "vagrants-corner-street-e"
channel_vagrantscorner_street_f = "vagrants-corner-street-f"
channel_greenlightdistrict_street_a = "green-light-district-street-a"
channel_greenlightdistrict_street_b = "green-light-district-street-b"
channel_greenlightdistrict_street_c = "green-light-district-street-c"
channel_slimesend_street_a = "slimes-end-street-a"

channel_slimetwitter = "slime-twitter"

hideout_channels = [channel_rowdyroughhouse, channel_copkilltown]
hideout_by_faction = {
	faction_rowdys: channel_rowdyroughhouse,
	faction_killers: channel_copkilltown
}


# Commands
cmd_prefix = '!'
cmd_enlist = cmd_prefix + 'enlist'
cmd_renounce = cmd_prefix + 'renounce'
cmd_revive = cmd_prefix + 'revive'
cmd_kill = cmd_prefix + 'kill'
cmd_shoot = cmd_prefix + 'shoot'
cmd_shoot_alt1 = cmd_prefix + 'bonk'
cmd_shoot_alt2 = cmd_prefix + 'pat'
cmd_shoot_alt3 = cmd_prefix + 'ban'
cmd_shoot_alt4 = cmd_prefix + 'pullthetrigger'
cmd_shoot_alt5 = cmd_prefix + 'curbstomp'
cmd_shoot_alt6 = cmd_prefix + 'hug'
cmd_attack = cmd_prefix + 'attack'
cmd_reload = cmd_prefix + 'reload'
cmd_reload_alt1 = cmd_prefix + 'loadthegun'
cmd_devour = cmd_prefix + 'devour'
cmd_mine = cmd_prefix + 'mine'
cmd_flag = cmd_prefix + 'flag'
cmd_score = cmd_prefix + 'slimes'
cmd_score_alt1 = cmd_prefix + 'slime'
cmd_giveslime = cmd_prefix + 'giveslime'
cmd_giveslime_alt1 = cmd_prefix + 'giveslimes'
cmd_help = cmd_prefix + 'help'
cmd_help_alt1 = cmd_prefix + 'command'
cmd_help_alt2 = cmd_prefix + 'commands'
cmd_help_alt3 = cmd_prefix + 'guide'
cmd_harvest = cmd_prefix + 'harvest'
cmd_salute = cmd_prefix + 'salute'
cmd_unsalute = cmd_prefix + 'unsalute'
cmd_hurl = cmd_prefix + 'hurl'
cmd_spar = cmd_prefix + 'spar'
cmd_suicide = cmd_prefix + 'suicide'
cmd_suicide_alt1 = cmd_prefix + 'seppuku'
cmd_suicide_alt2 = cmd_prefix + 'sudoku'
cmd_haunt = cmd_prefix + 'haunt'
cmd_inhabit = cmd_prefix + 'inhabit'
cmd_letgo = cmd_prefix + 'letgo'
cmd_possess_weapon = cmd_prefix + 'possessweapon'
cmd_possess_fishing_rod = cmd_prefix + 'possessfishingrod'
cmd_possess_fishing_rod_alt1 = cmd_prefix + 'possessrod'
cmd_crystalize_negapoudrin = cmd_prefix + 'crystalizenegapoudrin'
cmd_summonnegaslimeoid = cmd_prefix + 'summonnegaslimeoid'
cmd_summonnegaslimeoid_alt1 = cmd_prefix + 'summonnega'
cmd_summonnegaslimeoid_alt2 = cmd_prefix + 'summon'
cmd_summonenemy = cmd_prefix + 'summonenemy'
cmd_summongvsenemy = cmd_prefix + 'summongvsenemy'
cmd_deleteallenemies = cmd_prefix + 'deleteallenemies'
cmd_negaslimeoid = cmd_prefix + 'negaslimeoid'
cmd_battlenegaslimeoid = cmd_prefix + 'battlenegaslimeoid'
cmd_battlenegaslimeoid_alt1 = cmd_prefix + 'negaslimeoidbattle'
cmd_slimepachinko = cmd_prefix + 'slimepachinko'
cmd_slimeslots = cmd_prefix + 'slimeslots'
cmd_slimecraps = cmd_prefix + 'slimecraps'
cmd_slimeroulette = cmd_prefix + 'slimeroulette'
cmd_slimebaccarat = cmd_prefix + 'slimebaccarat'
cmd_slimeskat = cmd_prefix + 'slimeskat'
cmd_slimeskat_join = cmd_prefix + 'skatjoin'
cmd_slimeskat_decline = cmd_prefix + 'skatdecline'
cmd_slimeskat_bid = cmd_prefix + 'skatbid'
cmd_slimeskat_call = cmd_prefix + 'skatcall'
cmd_slimeskat_pass = cmd_prefix + 'skatpass'
cmd_slimeskat_play = cmd_prefix + 'skatplay'
cmd_slimeskat_hearts = cmd_prefix + 'skathearts'
cmd_slimeskat_slugs = cmd_prefix + 'skatslugs'
cmd_slimeskat_hats = cmd_prefix + 'skathats'
cmd_slimeskat_shields = cmd_prefix + 'skatshields'
cmd_slimeskat_grand = cmd_prefix + 'skatgrand'
cmd_slimeskat_null = cmd_prefix + 'skatnull'
cmd_slimeskat_take = cmd_prefix + 'skattake'
cmd_slimeskat_hand = cmd_prefix + 'skathand'
cmd_slimeskat_choose = cmd_prefix + 'skatchoose'
cmd_deadmega = cmd_prefix + 'deadmega'
cmd_donate = cmd_prefix + 'donate'
cmd_slimecoin = cmd_prefix + 'slimecoin'
cmd_slimecoin_alt1 = cmd_prefix + 'slimecredit'
cmd_slimecoin_alt2 = cmd_prefix + 'coin'
cmd_slimecoin_alt3 = cmd_prefix + 'sc'
cmd_invest = cmd_prefix + 'invest'
cmd_withdraw = cmd_prefix + 'withdraw'
cmd_exchangerate = cmd_prefix + 'exchangerate'
cmd_exchangerate_alt1 = cmd_prefix + 'exchange'
cmd_exchangerate_alt2 = cmd_prefix + 'rate'
cmd_exchangerate_alt3 = cmd_prefix + 'exchangerates'
cmd_exchangerate_alt4 = cmd_prefix + 'rates'
cmd_shares = cmd_prefix + 'shares'
cmd_stocks = cmd_prefix + 'stocks'
cmd_negapool = cmd_prefix + 'negapool'
cmd_negaslime = cmd_prefix + 'negaslime'
cmd_endlesswar = cmd_prefix + 'endlesswar'
cmd_swear_jar = cmd_prefix + 'swearjar'
cmd_equip = cmd_prefix + 'equip'
cmd_sidearm = cmd_prefix + 'sidearm'
cmd_data = cmd_prefix + 'data'
cmd_mutations = cmd_prefix + 'mutations'
cmd_mutations_alt_1 = cmd_prefix + 'stds'
cmd_hunger = cmd_prefix + 'hunger'
cmd_clock = cmd_prefix + 'clock'
cmd_time = cmd_prefix + 'time'
cmd_weather = cmd_prefix + 'weather'
cmd_patchnotes = cmd_prefix + 'patchnotes'
cmd_howl = cmd_prefix + 'howl'
cmd_howl_alt1 = cmd_prefix + '56709'
cmd_moan = cmd_prefix + 'moan'
cmd_transfer = cmd_prefix + 'transfer'
cmd_transfer_alt1 = cmd_prefix + 'xfer'
cmd_redeem = cmd_prefix + 'redeem'
cmd_menu = cmd_prefix + 'menu'
cmd_menu_alt1 = cmd_prefix + 'catalog'
cmd_menu_alt2 = cmd_prefix + 'catalogue'
cmd_order = cmd_prefix + 'order'
cmd_annoint = cmd_prefix + 'annoint'
cmd_annoint_alt1 = cmd_prefix + 'anoint'
cmd_crush = cmd_prefix + 'crush'
cmd_crush_alt1 = cmd_prefix + 'crunch'
cmd_disembody = cmd_prefix + 'disembody'
cmd_war = cmd_prefix + 'war'
cmd_toil = cmd_prefix + 'toil'
cmd_inventory = cmd_prefix + 'inventory'
cmd_inventory_alt1 = cmd_prefix + 'inv'
cmd_inventory_alt2 = cmd_prefix + 'stuff'
cmd_inventory_alt3 = cmd_prefix + 'bag'
cmd_communitychest = cmd_prefix + 'chest'
cmd_move = cmd_prefix + 'move'
cmd_move_alt1 = cmd_prefix + 'goto'
cmd_move_alt2 = cmd_prefix + 'walk'
cmd_move_alt3 = cmd_prefix + 'sny'
cmd_move_alt4 = cmd_prefix + 'tiptoe'
cmd_move_alt5 = cmd_prefix + 'step'
cmd_descend = cmd_prefix + 'descend'
cmd_halt = cmd_prefix + 'halt'
cmd_halt_alt1 = cmd_prefix + 'stop'
cmd_embark = cmd_prefix + 'embark'
cmd_embark_alt1 = cmd_prefix + 'board'
cmd_disembark = cmd_prefix + 'disembark'
cmd_disembark_alt1 = cmd_prefix + 'alight'
cmd_checkschedule = cmd_prefix + 'schedule'
cmd_inspect = cmd_prefix + 'inspect'
cmd_inspect_alt1 = cmd_prefix + 'examine'
cmd_look = cmd_prefix + 'look'
cmd_survey = cmd_prefix + 'survey'
cmd_scout = cmd_prefix + 'scout'
cmd_scout_alt1 = cmd_prefix + 'sniff'
cmd_scrutinize= cmd_prefix + 'scrutinize'
cmd_map = cmd_prefix + 'map'
cmd_transportmap = cmd_prefix + 'transportmap'
cmd_wiki = cmd_prefix + 'wiki'
cmd_booru = cmd_prefix + 'booru'
cmd_pardon = cmd_prefix + 'pardon'
cmd_banish = cmd_prefix + 'banish'
cmd_vouch = cmd_prefix + 'vouch'
cmd_writhe = cmd_prefix + 'writhe'
cmd_use = cmd_prefix + 'use'
cmd_eat = cmd_prefix + 'eat'
cmd_news = cmd_prefix + 'news'
cmd_buy = cmd_prefix + 'buy'
cmd_thrash = cmd_prefix + 'thrash'
cmd_dab = cmd_prefix + 'dab'
cmd_boo = cmd_prefix + 'boo'
cmd_dance = cmd_prefix + 'dance'
cmd_propaganda = cmd_prefix + 'propaganda'
cmd_coinflip = cmd_prefix + 'co1nfl1p'
cmd_spook = cmd_prefix + 'spook'
#cmd_makecostume = cmd_prefix + 'makecostume'
cmd_trick = cmd_prefix + 'trick'
cmd_treat = cmd_prefix + 'treat'
cmd_russian = cmd_prefix + 'russianroulette'
cmd_duel = cmd_prefix + 'duel'
cmd_accept = cmd_prefix + 'accept'
cmd_refuse = cmd_prefix + 'refuse'
cmd_sign = cmd_prefix + 'sign'
cmd_rip = cmd_prefix + 'rip'
cmd_reap = cmd_prefix + 'reap'
cmd_reap_alt = cmd_prefix + 'forcereap'
cmd_sow = cmd_prefix + 'sow'
cmd_check_farm = cmd_prefix + 'checkfarm'
cmd_irrigate = cmd_prefix + 'irrigate'
cmd_weed = cmd_prefix + 'weed'
cmd_fertilize = cmd_prefix + 'fertilize'
cmd_pesticide = cmd_prefix + 'pesticide'
cmd_mill = cmd_prefix + 'mill'
cmd_cast = cmd_prefix + 'cast'
cmd_reel = cmd_prefix + 'reel'
cmd_appraise = cmd_prefix + 'appraise'
cmd_barter = cmd_prefix + 'barter'
cmd_embiggen = cmd_prefix + 'embiggen'
cmd_barterall = cmd_prefix + 'barterall'
cmd_createfish = cmd_prefix + 'createfish'
cmd_adorn = cmd_prefix + 'adorn'
cmd_dedorn = cmd_prefix + 'dedorn'
cmd_dedorn_alt1 = cmd_prefix + 'unadorn'
cmd_dyecosmetic = cmd_prefix + 'dyecosmetic'
cmd_dyecosmetic_alt1 = cmd_prefix + 'dyehat'
cmd_dyecosmetic_alt2 = cmd_prefix + 'saturatecosmetic'
cmd_dyecosmetic_alt3 = cmd_prefix + 'saturatehat'
cmd_create = cmd_prefix + 'create'
cmd_forgemasterpoudrin = cmd_prefix + 'forgemasterpoudrin'
cmd_createitem = cmd_prefix + 'createitem'
cmd_manualsoulbind = cmd_prefix + 'soulbind'
cmd_editprops = cmd_prefix + 'editprops'
cmd_setslime = cmd_prefix + 'setslime'
cmd_checkstats = cmd_prefix + 'checkstats'
cmd_makebp = cmd_prefix + 'makebp'
#cmd_exalt = cmd_prefix + 'exalt'
cmd_give = cmd_prefix + 'give'
cmd_discard = cmd_prefix + 'discard'
cmd_discard_alt1 = cmd_prefix + 'drop'
cmd_trash = cmd_prefix + 'trash'
cmd_leaderboard = cmd_prefix + 'leaderboard'
cmd_leaderboard_alt1 = cmd_prefix + 'leaderboards'
cmd_marry = cmd_prefix + 'marry'
cmd_divorce = cmd_prefix + 'divorce'
cmd_scavenge = cmd_prefix + 'scavenge'
cmd_scavenge_alt1 = cmd_prefix + 'lookbetweenthecushions'
cmd_arm = cmd_prefix + 'arm'
cmd_arsenalize = cmd_prefix + 'arsenalize'
cmd_spray = cmd_prefix + 'annex'
cmd_spray_alt1 = cmd_prefix + 'spray'
cmd_capture_progress = cmd_prefix + 'progress'
cmd_changespray = cmd_prefix + 'changespray'
cmd_changespray_alt1 = cmd_prefix + 'changetag'
cmd_tag = cmd_prefix + 'tag'
cmd_teleport = cmd_prefix + 'tp'
cmd_teleport_alt1 = cmd_prefix + 'blj'
cmd_teleport_player = cmd_prefix + 'tpp'
cmd_print_map_data = cmd_prefix + 'printmapdata'
cmd_ping_me = cmd_prefix + 'pingme'
cmd_boot = cmd_prefix + 'boot'
cmd_bootall = cmd_prefix + 'bootall'
cmd_quarterlyreport = cmd_prefix + 'quarterlyreport'
cmd_piss = cmd_prefix + 'piss'
cmd_fursuit = cmd_prefix + 'fursuit'
cmd_recycle = cmd_prefix + 'recycle'
cmd_recycle_alt1 = cmd_prefix + 'incinerate'
cmd_view_sap = cmd_prefix + 'sap'
cmd_harden_sap = cmd_prefix + 'harden'
cmd_harden_sap_alt1 = cmd_prefix + 'solidify'
cmd_liquefy_sap = cmd_prefix + 'liquefy'
cmd_dodge = cmd_prefix + 'dodge'
cmd_dodge_alt1 = cmd_prefix + 'evade'
cmd_dodge_alt2 = cmd_prefix + 'wavedash'
cmd_taunt = cmd_prefix + 'taunt'
cmd_aim = cmd_prefix + 'aim'
cmd_advertise = cmd_prefix + 'advertise'
cmd_ads = cmd_prefix + 'ads'
cmd_confirm = cmd_prefix + 'confirm'
cmd_cancel = cmd_prefix + 'cancel'
cmd_pray = cmd_prefix + 'pray'
cmd_flushsubzones = cmd_prefix + 'flushsubzones'
cmd_flushstreets = cmd_prefix + 'flushstreets'
cmd_wrap = cmd_prefix + 'wrap'
cmd_unwrap = cmd_prefix + 'unwrap'
cmd_yoslimernalia = cmd_prefix + 'yoslimernalia'
cmd_shamble = cmd_prefix + 'shamble'
cmd_rejuvenate = cmd_prefix + 'rejuvenate'
cmd_clockin = cmd_prefix + 'clockin'
cmd_clockout = cmd_prefix + 'clockout'
cmd_sanitize = cmd_prefix + 'sanitize'
cmd_paycheck = cmd_prefix + 'paycheck'
cmd_payday = cmd_prefix + 'payday'

cmd_preserve = cmd_prefix + 'preserve'
cmd_stink = cmd_prefix + 'stink'
cmd_slap = cmd_prefix + 'slap'
cmd_track = cmd_prefix + 'track'
cmd_longdrop = cmd_prefix + 'longdrop'
cmd_shakeoff = cmd_prefix + 'shakeoff'
cmd_clench = cmd_prefix + 'clench'
cmd_thirdeye = cmd_prefix + 'thirdeye'
cmd_loop = cmd_prefix + 'loop'
cmd_chemo = cmd_prefix + 'chemo'
cmd_graft = cmd_prefix + 'graft'
cmd_bleedout = cmd_prefix + 'bleedout'
cmd_skullbash = cmd_prefix + 'skullbash'
cmd_juviemode = cmd_prefix + 'legallimit'
cmd_manual_unban = cmd_prefix + 'unban'

cmd_switch = cmd_prefix + 'switch'
cmd_switch_alt_1 = cmd_prefix + 's'

cmd_slimeball = cmd_prefix + 'slimeball'
cmd_slimeballgo = cmd_prefix + 'slimeballgo'
cmd_slimeballstop = cmd_prefix + 'slimeballstop'
cmd_slimeballleave = cmd_prefix + 'slimeballleave'
cmd_gambit = cmd_prefix + 'gambit'
cmd_credence = cmd_prefix + 'credence'
cmd_get_credence = cmd_prefix + 'getcredence'
cmd_reset_prank_stats = cmd_prefix + 'resetprankstats'
cmd_set_gambit = cmd_prefix + 'setgambit'
cmd_pointandlaugh = cmd_prefix + 'pointandlaugh'
cmd_prank = cmd_prefix + 'prank'
cmd_gvs_printgrid = cmd_prefix + 'grid'
cmd_gvs_printgrid_alt1 = cmd_prefix + 'lawn'
cmd_gvs_printlane = cmd_prefix + 'lane'
cmd_gvs_incubategaiaslimeoid = cmd_prefix + 'incubategaiaslimeoid'
cmd_gvs_fabricatetombstone = cmd_prefix + 'fabricatetombstone'
cmd_gvs_joinoperation = cmd_prefix + 'joinop'
cmd_gvs_leaveoperation = cmd_prefix + 'leaveop'
cmd_gvs_checkoperation = cmd_prefix + 'checkops'
cmd_gvs_plantgaiaslimeoid = cmd_prefix + 'plant'
cmd_gvs_almanac = cmd_prefix + 'almanac'
cmd_gvs_searchforbrainz = cmd_prefix + 'searchforbrainz'
cmd_gvs_grabbrainz = cmd_prefix + 'grabbrainz'
cmd_gvs_dive = cmd_prefix + 'dive'
cmd_gvs_resurface = cmd_prefix + 'resurface'
cmd_gvs_sellgaiaslimeoid = cmd_prefix + 'sellgaiaslimeoid'
cmd_gvs_sellgaiaslimeoid_alt = cmd_prefix + 'sellgaia'
cmd_gvs_dig = cmd_prefix + 'dig'
cmd_gvs_progress = cmd_prefix + 'gvs'
cmd_gvs_gaiaslime = cmd_prefix + 'gaiaslime'
cmd_gvs_gaiaslime_alt1 = cmd_prefix + 'gs'
cmd_gvs_brainz = cmd_prefix + 'brainz'

cmd_retire = cmd_prefix + 'retire'
cmd_depart = cmd_prefix + 'depart'
cmd_consult = cmd_prefix + 'consult'
cmd_sign_lease = cmd_prefix + 'signlease'
#cmd_rent_cycle = cmd_prefix + 'rentcycle'
cmd_fridge = cmd_prefix + 'fridge'
cmd_closet = cmd_prefix + 'closet'
cmd_store = cmd_prefix + 'stow' #was originally !store, that honestly would be a easier command to remember
cmd_unfridge = cmd_prefix + 'unfridge'
cmd_uncloset = cmd_prefix + 'uncloset'
cmd_take = cmd_prefix + 'snag' #same as above, but with !take
cmd_decorate = cmd_prefix + 'decorate'
cmd_undecorate = cmd_prefix + 'undecorate'
cmd_freeze = cmd_prefix + 'freeze'
cmd_unfreeze = cmd_prefix + 'unfreeze'
cmd_apartment = cmd_prefix + 'apartment'
cmd_aptname = cmd_prefix + 'aptname'
cmd_aptdesc = cmd_prefix + 'aptdesc'
cmd_upgrade  = cmd_prefix + 'aptupgrade' #do we need the apt at the beginning?
cmd_knock = cmd_prefix + 'knock'
cmd_trickortreat = cmd_prefix + 'trickortreat'
cmd_breaklease = cmd_prefix + 'breaklease'
cmd_aquarium = cmd_prefix + 'aquarium'
cmd_pot = cmd_prefix + 'pot'
cmd_propstand = cmd_prefix + 'propstand'
cmd_releaseprop = cmd_prefix + 'unstand'
cmd_releasefish = cmd_prefix + 'releasefish'
cmd_unpot = cmd_prefix + 'unpot'
cmd_wash = cmd_prefix + 'wash'
cmd_browse = cmd_prefix + 'browse'
cmd_smoke = cmd_prefix + 'smoke'
cmd_frame = cmd_prefix + 'frame'
cmd_extractsoul = cmd_prefix + 'extractsoul'
cmd_returnsoul = cmd_prefix + 'returnsoul'
cmd_squeeze = cmd_prefix + 'squeezesoul'
cmd_betsoul = cmd_prefix + 'betsoul'
cmd_buysoul = cmd_prefix + 'buysoul'
cmd_push = cmd_prefix + 'push'
cmd_push_alt_1 = cmd_prefix + 'bully'
cmd_jump = cmd_prefix + 'jump'
cmd_toss = cmd_prefix + 'toss'
cmd_dyefurniture = cmd_prefix + 'dyefurniture'
cmd_watch = cmd_prefix + 'watch'
cmd_purify = cmd_prefix + 'purify'
cmd_shelve = cmd_prefix + 'shelve'
cmd_shelve_alt_1 = cmd_prefix + 'shelf'
cmd_unshelve = cmd_prefix + 'unshelve'
cmd_unshelve_alt_1 = cmd_prefix + 'unshelf'
cmd_addkey = cmd_prefix + 'addkey'
cmd_changelocks = cmd_prefix + 'changelocks'
cmd_setalarm = cmd_prefix + 'setalarm'
cmd_checkflag = cmd_prefix + 'checkflag'
cmd_jam = cmd_prefix + 'jam'
cmd_sew = cmd_prefix + 'sew'
cmd_retrofit = cmd_prefix + 'retrofit'
cmd_sip = cmd_prefix + 'sip'
cmd_fashion = cmd_prefix + 'fashion'

cmd_beginmanuscript = cmd_prefix + 'beginmanuscript'
cmd_beginmanuscript_alt_1 = cmd_prefix + 'createmanuscript'
cmd_beginmanuscript_alt_2 = cmd_prefix + 'startmanuscript'
cmd_setpenname = cmd_prefix + 'setpenname'
cmd_setpenname_alt_1 = cmd_prefix + 'setauthor'
cmd_settitle = cmd_prefix + 'settitle'
cmd_settitle_alt_1 = cmd_prefix + 'setname'
cmd_setgenre = cmd_prefix + 'setgenre'
cmd_editpage = cmd_prefix + 'editpage'
cmd_viewpage = cmd_prefix + 'viewpage'
cmd_checkmanuscript = cmd_prefix + 'manuscript'
cmd_publishmanuscript = cmd_prefix + 'publish'
cmd_readbook = cmd_prefix + 'read'
cmd_nextpage = cmd_prefix + 'nextpage'
cmd_nextpage_alt_1 = cmd_prefix + 'flip'
cmd_previouspage = cmd_prefix + 'previouspage'
cmd_previouspage_alt_1 = cmd_prefix + 'pilf'
cmd_previouspage_alt_2 = cmd_prefix + 'plif'
cmd_browsezines = cmd_prefix + 'browse'
cmd_buyzine = cmd_prefix + 'buyzine'
cmd_buyzine_alt_1 = cmd_prefix + 'orderzine'
cmd_rate = cmd_prefix + 'ratezine'
cmd_rate_alt_1 = cmd_prefix + 'reviewzine'
cmd_rate_alt_2 = cmd_prefix + 'review'
cmd_setpages = cmd_prefix + 'setpages'
cmd_setpages_alt_1 = cmd_prefix + 'setpage'
cmd_setpages_alt_2 = cmd_prefix + 'setlength'
cmd_takedown = cmd_prefix + 'takedown'
cmd_takedown_alt_1 = cmd_prefix + 'copyrightstrike'
cmd_takedown_alt_2 = cmd_prefix + 'deletezine'
cmd_untakedown = cmd_prefix + 'untakedown'
cmd_untakedown_alt_1 = cmd_prefix + 'uncopyrightstrike'
cmd_untakedown_alt_2 = cmd_prefix + 'undeletezine'
cmd_lol = cmd_prefix + 'lol'
cmd_mastery = cmd_prefix + 'mastery'

apartment_b_multiplier = 1500
apartment_a_multiplier = 2000000
apartment_dt_multiplier = 3000000000
apartment_s_multiplier = 6000000000

soulprice = 500000000

tv_set_slime = 5000000
tv_set_level = 100

cmd_promote = cmd_prefix + 'promote'

cmd_arrest = cmd_prefix + 'arrest'
cmd_release = cmd_prefix + 'release'
cmd_balance_cosmetics = cmd_prefix + 'balancecosmetic'
cmd_release_alt1 = cmd_prefix + 'unarrest'
cmd_restoreroles = cmd_prefix + 'restoreroles'
cmd_hiderolenames = cmd_prefix + 'hiderolenames'
cmd_recreateroles = cmd_prefix + 'recreateroles'
cmd_deleteroles = cmd_prefix + 'deleteroles'
cmd_removeuseroverwrites = cmd_prefix + 'removeuseroverwrites'
cmd_collectopics = cmd_prefix + 'collecttopics'
cmd_synctopics = cmd_prefix + 'synctopics'
cmd_shutdownbot = cmd_prefix + 'shutdownbot'
cmd_checkbot = cmd_prefix + 'checkbot'
cmd_degradedistricts = cmd_prefix + 'degradedistricts'
cmd_debug1 = cmd_prefix + ewdebug.cmd_debug1
cmd_debug2 = cmd_prefix + ewdebug.cmd_debug2
cmd_debug3 = cmd_prefix + ewdebug.cmd_debug3
cmd_debug4 = cmd_prefix + ewdebug.cmd_debug4
#debug5 = ewdebug.debug5
cmd_debug6 = cmd_prefix + ewdebug.cmd_debug6
cmd_debug7 = cmd_prefix + ewdebug.cmd_debug7
cmd_debug8 = cmd_prefix + ewdebug.cmd_debug8

cmd_reroll_mutation = cmd_prefix + 'rerollmutation'
cmd_clear_mutations = cmd_prefix + 'sterilizemutations'

cmd_smelt = cmd_prefix + 'smelt'
cmd_wcim = cmd_prefix + 'whatcanimake'
cmd_wcim_alt1 = cmd_prefix + 'wcim'
cmd_wcim_alt2 = cmd_prefix + 'whatmake'
cmd_wcim_alt3 = cmd_prefix + 'usedfor'

#slimeoid commands
cmd_incubateslimeoid = cmd_prefix + 'incubateslimeoid'
cmd_growbody = cmd_prefix + 'growbody'
cmd_growhead = cmd_prefix + 'growhead'
cmd_growlegs = cmd_prefix + 'growlegs'
cmd_growweapon = cmd_prefix + 'growweapon'
cmd_growarmor = cmd_prefix + 'growarmor'
cmd_growspecial = cmd_prefix + 'growspecial'
cmd_growbrain = cmd_prefix + 'growbrain'
cmd_nameslimeoid = cmd_prefix + 'nameslimeoid'
cmd_raisemoxie = cmd_prefix + 'raisemoxie'
cmd_lowermoxie = cmd_prefix + 'lowermoxie'
cmd_raisegrit = cmd_prefix + 'raisegrit'
cmd_lowergrit = cmd_prefix + 'lowergrit'
cmd_raisechutzpah = cmd_prefix + 'raisechutzpah'
cmd_lowerchutzpah = cmd_prefix + 'lowerchutzpah'
cmd_spawnslimeoid = cmd_prefix + 'spawnslimeoid'
cmd_dissolveslimeoid = cmd_prefix + 'dissolveslimeoid'
cmd_slimeoid = cmd_prefix + 'slimeoid'
cmd_challenge = cmd_prefix + 'challenge'
cmd_instructions = cmd_prefix + 'instructions'
cmd_playfetch = cmd_prefix + 'playfetch'
cmd_petslimeoid = cmd_prefix + 'petslimeoid'
cmd_abuseslimeoid = cmd_prefix + 'abuseslimeoid'
cmd_walkslimeoid = cmd_prefix + 'walkslimeoid'
cmd_observeslimeoid = cmd_prefix + 'observeslimeoid'
cmd_slimeoidbattle = cmd_prefix + 'slimeoidbattle'
cmd_saturateslimeoid = cmd_prefix + 'saturateslimeoid'
cmd_restoreslimeoid = cmd_prefix + 'restoreslimeoid'
cmd_bottleslimeoid = cmd_prefix + 'bottleslimeoid'
cmd_unbottleslimeoid = cmd_prefix + 'unbottleslimeoid'
cmd_feedslimeoid = cmd_prefix + 'feedslimeoid'
cmd_dress_slimeoid = cmd_prefix + 'dressslimeoid'
cmd_dress_slimeoid_alt1 = cmd_prefix + 'decorateslimeoid'
cmd_undress_slimeoid = cmd_prefix + 'undressslimeoid'
cmd_undress_slimeoid_alt1 = cmd_prefix + 'undecorateslimeoid'

cmd_add_quadrant = cmd_prefix + "addquadrant"
cmd_clear_quadrant = cmd_prefix + "clearquadrant"
cmd_get_quadrants = cmd_prefix + "quadrants"
cmd_get_sloshed = cmd_prefix + "sloshed"
cmd_get_sloshed_alt1 = cmd_prefix + "soulvent"
cmd_get_roseate = cmd_prefix + "roseate"
cmd_get_roseate_alt1 = cmd_prefix + "bedenizen"
cmd_get_violacious = cmd_prefix + "violacious"
cmd_get_violacious_alt1 = cmd_prefix + "amaranthagonist"
cmd_get_policitous = cmd_prefix + "policitous"
cmd_get_policitous_alt1 = cmd_prefix + "arbitraitor"

cmd_trade = cmd_prefix + 'trade'
cmd_offer = cmd_prefix + 'offer'
cmd_remove_offer = cmd_prefix + 'removeoffer'
cmd_completetrade = cmd_prefix + 'completetrade'
cmd_canceltrade = cmd_prefix + 'canceltrade'

# race
cmd_set_race = cmd_prefix + 'setrace'
cmd_set_race_alt1 = cmd_prefix + 'identifyas'
cmd_exist = cmd_prefix + 'exist'
cmd_ree = cmd_prefix + 'ree'
cmd_autocannibalize = cmd_prefix + 'autocannibalize'
cmd_rattle = cmd_prefix + 'rattle'
cmd_beep = cmd_prefix + 'beep'
cmd_yiff = cmd_prefix + 'yiff'
cmd_hiss = cmd_prefix + 'hiss'
cmd_jiggle = cmd_prefix + 'jiggle'
cmd_request_petting = cmd_prefix + 'requestpetting'
cmd_rampage = cmd_prefix + 'rampage'
cmd_flutter = cmd_prefix + 'flutter'
cmd_entomize = cmd_prefix + 'entomize'
cmd_confuse = cmd_prefix + 'confuse'
cmd_shamble = cmd_prefix + 'shamble'

# Slime Twitter
cmd_tweet = cmd_prefix + 'tweet'
cmd_verification = cmd_prefix + 'requestverification'
cmd_verification_alt = cmd_prefix + '#verify'

#SLIMERNALIA
cmd_festivity = cmd_prefix + 'festivity'

offline_cmds = [
	cmd_move,
	cmd_move_alt1,
	cmd_move_alt2,
	cmd_move_alt3,
	cmd_move_alt4,
	cmd_move_alt5,
	cmd_descend,
	cmd_halt,
	cmd_halt_alt1,
	cmd_embark,
	cmd_embark_alt1,
	cmd_disembark,
	cmd_disembark_alt1,
	cmd_look,
	cmd_survey,
	cmd_scout,
	cmd_scout_alt1,
	cmd_depart,
	cmd_retire
	# cmd_scrutinize
]

# Maximum amount of slime juveniles can have before being killable
max_safe_slime = 100000
max_safe_level = 18

# Slime costs/values
slimes_onrevive = 20
slimes_onrevive_everyone = 20
slimes_toenlist = 0
slimes_perspar_base = 0
slimes_hauntratio = 1000
slimes_perslot = 100
slimes_perpachinko = 500
slimecoin_exchangerate = 1
slimes_permill = 50000
slimes_invein = 4000
slimes_pertile = 50
slimes_to_possess_weapon = -100000
slimes_to_possess_fishing_rod = -10000
slimes_to_crystalize_negapoudrin = -1000000
slimes_cliffdrop = 200000
slimes_item_drop = 10000
slimes_shambler = 10

# hunger
min_stamina = 100
hunger_pershot = 10
hunger_perspar = 10
hunger_perfarm = 50
hunger_permine = 1
hunger_perminereset = 25
hunger_perfish = 15
hunger_perscavenge = 2
hunger_pertick = 3
hunger_pertrickortreat = 6
hunger_perlmcollapse = 100

# Time it takes to move between various parts of the map
travel_time_subzone = 20
travel_time_district = 60
travel_time_street = 20
travel_time_outskirt = 60
travel_time_infinite = 900

# ads
slimecoin_toadvertise = 1000000
max_concurrent_ads = 8
max_length_ads = 500
uptime_ads = 7 * 24 * 60 * 60 # one week

time_bhbleed = 300 #5 minutes

# currencies you can gamble at the casino
currency_slime = "slime"
currency_slimecoin = "SlimeCoin"
currency_soul = "soul"

#inebriation
inebriation_max = 20
inebriation_pertick = 2

# max item amounts
max_food_in_inv_mod = 8  # modifier for how much food you can carry. the player's slime level is divided by this number to calculate the number of carriable food items
max_adornspace_mod = 8
max_weapon_mod = 16

# item acquisition methods
acquisition_smelting = "smelting"
acquisition_milling = "milling"
acquisition_mining = "mining"
acquisition_dojo = "dojo"
acquisition_fishing = "fishing"
acquisition_bartering = "bartering"
acquisition_trickortreating = "trickortreating"
acquisition_bazaar = "bazaar"

# standard food expiration in seconds
std_food_expir = 12 * 3600  # 12 hours
farm_food_expir = 12 * 3600 * 4 # 2 days
milled_food_expir = 12 * 3600 * 28 # 2 weeks

horseman_death_cooldown = 12 * 3600 * 4 # 2 days

# amount of slime you get from crushing a poudrin
crush_slimes = 10000

# minimum amount of slime needed to capture territory
min_slime_to_cap = 200000

# property classes
property_class_s = "s"
property_class_a = "a"
property_class_b = "b"
property_class_c = "c"

# district capturing
capture_tick_length = 10  # in seconds; also affects how much progress is made per tick
max_capture_points_s = 500000 # 500k
max_capture_points_a = 300000  # 300k
max_capture_points_b = 200000  # 200k
max_capture_points_c = 100000   # 100k

limit_influence_s = 133200000
limit_influence_a = 66600000
limit_influence_b = 40000000
limit_influence_c = 19000000

min_influence_s = 66600000
min_influence_a = 34000000
min_influence_b = 20000000
min_influence_c = 7000000

min_garotte = 2000






# district capture rates assigned to property classes
max_capture_points = {
	property_class_s: max_capture_points_s,
	property_class_a: max_capture_points_a,
	property_class_b: max_capture_points_b,
	property_class_c: max_capture_points_c
}

limit_influence = {
	property_class_s: limit_influence_s,
	property_class_a: limit_influence_a,
	property_class_b: limit_influence_b,
	property_class_c: limit_influence_c
}

min_influence = {
	property_class_s: min_influence_s,
	property_class_a: min_influence_a,
	property_class_b: min_influence_b,
	property_class_c: min_influence_c
}

# how long districts stay locked after capture
capture_lock_s = 48 * 60 * 60  # 2 days
capture_lock_a = 24 * 60 * 60  # 1 day
capture_lock_b = 12 * 60 * 60  # 12 hours
capture_lock_c = 6 * 60 * 60  # 6 hours

# district lock times assigned to property classes
capture_locks = {
	property_class_s: capture_lock_s,
	property_class_a: capture_lock_a,
	property_class_b: capture_lock_b,
	property_class_c: capture_lock_c,
}

# how much slime is needed to bypass capture times
slimes_toannex_s = 1000000 # 1 mega
slimes_toannex_a = 500000 # 500 k
slimes_toannex_b = 200000 # 200 k
slimes_toannex_c = 100000 # 100 k

# slime to annex by property class
slimes_toannex = {
	property_class_s: slimes_toannex_s,
	property_class_a: slimes_toannex_a,
	property_class_b: slimes_toannex_b,
	property_class_c: slimes_toannex_c
}

# by how much to extend the capture lock per additional gangster capping
capture_lock_per_gangster = 60 * 60  # 60 min

# capture lock messages
capture_lock_milestone = 15 * 60 # 5 min

# capture messages
capture_milestone = 5  # after how many percent of progress the players are notified of the progress

# capture speed at 0% progress
baseline_capture_speed = 1

# accelerates capture speed depending on current progress
capture_gradient = 1

# district de-capturing
decapture_speed_multiplier = 1  # how much faster de-capturing is than capturing

# district control decay
decay_modifier = 4  # more means slower

# time values
seconds_per_ingame_day = 21600
ticks_per_day = seconds_per_ingame_day / update_market  # how often the kingpins receive slime per in-game day

# kingpin district control slime yields (per tick, i.e. in-game-hourly)
slime_yield_class_s = int(60000 / ticks_per_day)  # dividing the daily amount by the amount of method calls per day
slime_yield_class_a = int(40000 / ticks_per_day)
slime_yield_class_b = int(30000 / ticks_per_day)
slime_yield_class_c = int(20000 / ticks_per_day)

# district control slime yields assigned to property classes
district_control_slime_yields = {
	property_class_s: slime_yield_class_s,
	property_class_a: slime_yield_class_a,
	property_class_b: slime_yield_class_b,
	property_class_c: slime_yield_class_c
}

# Slime decay rate
slime_half_life = 60 * 60 * 24 * 14 #two weeks

# Rate of bleeding stored damage into the environment
bleed_half_life = 60 * 5 #five minutes

# how often to bleed
bleed_tick_length = 10

# how often to decide whether or not to spawn an enemy
enemy_spawn_tick_length = 60 * 3 # Three minutes
#enemy_spawn_tick_length = 1
# how often it takes for hostile enemies to attack
enemy_attack_tick_length = 5

# how often to check game states in Gankers Vs. Shamblers
gvs_gamestate_tick_length = 5

# how often to burn
burn_tick_length = 4

# how often to check for statuses to be removed
removestatus_tick_length = 5

# Unearthed Item rarity (for enlisted players)
unearthed_item_rarity = 1500

# Chance to loot an item while scavenging
scavenge_item_rarity = 1000

# Lifetimes
invuln_onrevive = 0

# how often to apply weather effects
weather_tick_length = 10

# how often to delete expired world events
event_tick_length = 5

# slimeball tick length
slimeball_tick_length = 5

# how often to refresh sap
sap_tick_length = 5

# the amount of sap crushed by !piss
sap_crush_piss = 3

# the amount of sap spent on !piss'ing on someone
sap_spend_piss = 1

# farming
crops_time_to_grow = 180  # in minutes; 180 minutes are 3 hours
reap_gain = 100000
farm_slimes_peraction = 25000
time_nextphase = 20 * 60 # 20 minutes
time_lastphase_juvie = 10 * 60 # 10 minutes
farm_tick_length = 60 # 1 minute

farm_phase_sow = 0
farm_phase_reap = 9
farm_phase_reap_juvie = 5

farm_action_none = 0
farm_action_water = 1
farm_action_fertilize = 2
farm_action_weed = 3
farm_action_pesticide = 4

# gvs
brainz_per_grab = 25

farm_actions = [
	EwFarmAction(
		id_action = farm_action_water,
		action = cmd_irrigate,
		str_check = "Your crop is dry and weak. It needs some water.",
		str_execute = "You pour water on your parched crop.",
		str_execute_fail = "You pour gallons of water on the already saturated soil, nearly drowning your crop.",
	),
	EwFarmAction(
		id_action = farm_action_fertilize,
		action = cmd_fertilize,
		str_check = "Your crop looks malnourished like an African child in a charity ad.",
		str_execute = "You fertilize your starving crop.",
		str_execute_fail = "You give your crop some extra fertilizer for good measure. The ground's salinity shoots up as a result. Maybe look up fertilizer burn, dumbass.",
	),
	EwFarmAction(
		id_action = farm_action_weed,
		action = cmd_weed,
		str_check = "Your crop is completely overgrown with weeds.",
		str_execute = "You make short work of the weeds.",
		str_execute_fail = "You pull those damn weeds out in a frenzy. Hold on, that wasn't a weed. That was your crop. You put it back in the soil, but it looks much worse for the wear.",
	),
	EwFarmAction(
		id_action = farm_action_pesticide,
		action = cmd_pesticide,
		str_check = "Your crop is being ravaged by parasites.",
		str_execute = "You spray some of the good stuff on your crop and watch the pests drop like flies, in a very literal way.",
		str_execute_fail = "You spray some of the really nasty stuff on your crop. Surely no pests will be able to eat it away now. Much like any other living creature, probably.",
	),
]

id_to_farm_action = {}
cmd_to_farm_action = {}
farm_action_ids = []

for farm_action in farm_actions:
	cmd_to_farm_action[farm_action.action] = farm_action
	for alias in farm_action.aliases:
		cmd_to_farm_action[alias] = farm_action
	id_to_farm_action[farm_action.id_action] = farm_action
	farm_action_ids.append(farm_action.id_action)


# fishing
fish_gain = 10000 # multiplied by fish size class
fish_offer_timeout = 1440 # in minutes; 24 hours

# Cooldowns
cd_kill = 5
cd_spar = 60
cd_haunt = 600
cd_shambler_shamble = 20
cd_shambler_attack = 20
cd_squeeze = 1200
cd_invest = 5 * 60
cd_boombust = 22
#For possible time limit on russian roulette
cd_rr = 600
#slimeoid downtime after a defeat
cd_slimeoiddefeated = 300
cd_scavenge = 0
soft_cd_scavenge = 15 # Soft cooldown on scavenging
cd_enlist = 60
cd_premium_purchase = 2 * 24 * 60 * 60 # 48 Hours, 2 days
cd_new_player = 3 * 24 * 60 * 60 # 72 Hours, 3 days

cd_autocannibalize = 60 * 60 # can only eat yourself once per hour
cd_drop_bone = 5 * 60
cd_change_race = 24 * 60 * 60 # can only change your race once per day
cd_gvs_searchforbrainz = 300

# in relation to time of death
time_to_manifest = 24 * 60 * 60 # a day

# PvP timer pushouts
time_pvp_kill = 30 * 60 # NOT USED
time_pvp_attack = 10 * 60 # NOT USED
time_pvp_annex = 10 * 60 # NOT USED
time_pvp_mine = 5 * 60 
time_pvp_withdraw = 30 * 60 # NOT USED
time_pvp_scavenge = 10 * 60 
time_pvp_fish = 10 * 60	
time_pvp_farm = 30 * 60 
time_pvp_chemo = 10 * 60 
time_pvp_spar = 5 * 60 # NOT USED
time_pvp_enlist = 5 * 60 # NOT USED
time_pvp_knock = 1 * 60 #temp fix. will probably add spam prevention or something funny like restraining orders later
time_pvp_duel = 3 * 60 # NOT USED
time_pvp_pride = 1 * 60 # NOT USED
time_pvp_vulnerable_districts = 1 * 60 # NOT USED

# time to get kicked out of subzone. 
time_kickout = 60 * 60  # 1 hour

# For SWILLDERMUK, this is used to prevent AFK people from being pranked.
time_afk_swilldermuk = 60 * 60 * 2 # 1 hours

# time after coming online before you can act
time_offline = 10

# time for an enemy to despawn
time_despawn = 60 * 60 * 12 # 12 hours

# time for a player to be targeted by an enemy after entering a district
time_enemyaggro = 5

# time for a raid boss to target a player after moving to a new district
time_raidbossaggro = 3

# time for a raid boss to activate
time_raidcountdown = 60

# time for a raid boss to stay in a district before it can move again
time_raidboss_movecooldown = 2.5 * 60

# maximum amount of enemies a district can hold before it stops spawning them
max_enemies = 5

# response string used to let attack function in ewwep know that an enemy is being attacked
enemy_targeted_string = "ENEMY-TARGETED"

# Wiki link base url
wiki_baseurl = "https://rfck.miraheze.org/wiki/"

# Emotes
emote_tacobell = "<:tacobell:431273890195570699>"
emote_pizzahut = "<:pizzahut:431273890355085323>"
emote_kfc = "<:kfc:431273890216673281>"
emote_moon = "<:moon:431418525303963649>"
emote_111 = "<:111:431547758181220377>"

emote_copkiller = "<:copkiller:431275071945048075>"
emote_rowdyfucker = "<:rowdyfucker:431275088076079105>"
emote_ck = "<:ck:504173691488305152>"
emote_rf = "<:rf:504174176656162816>"

emote_theeye = "<:theeye:431429098909466634>"
emote_slime1 = "<:slime1:431564830541873182>"
emote_slime2 = "<:slime2:431570132901560320>"
emote_slime3 = "<:slime3:431659469844381717>"
emote_slime4 = "<:slime4:431570132901560320>"
emote_slime5 = "<:slime5:431659469844381717>"
emote_slimeskull = "<:slimeskull:431670526621122562>"
emote_slimeheart = "<:slimeheart:431673472687669248>"
emote_dice1 = "<:dice1:436942524385329162>"
emote_dice2 = "<:dice2:436942524389654538>"
emote_dice3 = "<:dice3:436942524041527298>"
emote_dice4 = "<:dice4:436942524406300683>"
emote_dice5 = "<:dice5:436942524444049408>"
emote_dice6 = "<:dice6:436942524469346334>"
emote_negaslime = "<:ns:453826200616566786>"
emote_bustin = "<:bustin:455194248741126144>"
emote_ghost = "<:lordofghosts:434002083256205314>"
emote_slimefull = "<:slimefull:496397819154923553>"
emote_purple = "<:purple:496397848343216138>"
emote_pink = "<:pink:496397871180939294>"
emote_slimecoin = "<:slimecoin:440576133214240769>"
emote_slimegun = "<:slimegun:436500203743477760>"
emote_slimeshot = "<:slimeshot:436604890928644106>"
emote_slimecorp = "<:slimecorp:568637591847698432>"
emote_nlacakanm = "<:nlacakanm:499615025544298517>"
emote_megaslime = "<:megaslime:436877747240042508>"
emote_srs = "<:srs:631859962519224341>"
emote_staydead = "<:sd:506840095714836480>"
emote_janus1 = "<:janus1:694404178956779592>"
emote_janus2 = "<:janus2:694404179342655518>"
emote_masterpoudrin = "<:masterpoudrin:694788959418712114>"
emote_poketubers = "<:c_poketubers:706989587112787998>"
emote_pulpgourds = "<:c_pulpgourds:706989587469172746>"
emote_sourpotatoes = "<:c_sourpotatoes:706989587196543067>"
emote_bloodcabbages = "<:c_bloodcabbages:706989586475253832>"
emote_joybeans = "<:c_joybeans:706989586949210223>"
emote_killiflower = "<:c_killiflower:706989587003736114>"
emote_razornuts = "<:c_razornuts:706989587129434364>"
emote_pawpaw = "<:c_pawpaw:706989587137953812>"
emote_sludgeberries = "<:c_sludgeberries:706989587205062656>"
emote_suganmanuts = "<:c_suganmanuts:706989587276234862>"
emote_pinkrowddishes = "<:c_pinkrowddishes:706989586684969091>"
emote_dankwheat = "<:c_dankwheat:706989586714460222>"
emote_brightshade = "<:c_brightshade:706989586676580373>"
emote_blacklimes = "<:c_blacklimes:706989586890489947>"
emote_phosphorpoppies = "<:c_phosphorpoppies:706989586898878496>"
emote_direapples = "<:c_direapples:706989586928238663>"
emote_rustealeaves = "<:c_rustealeaves:743337308295790642>"
emote_metallicaps = "<:c_metallicaps:743337308228419714>"
emote_steelbeans = "<:c_steelbeans:743337307968372757>"
emote_aushucks = "<:c_aushucks:743337307859320923>"
emote_blankregional = "<:bl:747207921926144081>"
emote_greenlawn = "<:gr:726271625489809411>"
emote_limelawn = "<:li:726271664815472692>"
emote_frozentile = "<:ft:743276248381259846>"

# Emotes for the negaslime writhe animation
emote_vt = "<:vt:492067858160025600>"
emote_ve = "<:ve:492067844930928641>"
emote_va = "<:va:492067850878451724>"
emote_v_ = "<:v_:492067837565861889>"
emote_s_ = "<:s_:492067830624157708>"
emote_ht = "<:ht:492067823150039063>"
emote_hs = "<:hs:492067783396294658>"
emote_he = "<:he:492067814933266443>"
emote_h_ = "<:h_:492067806465228811>"
emote_blank = "<:blank:570060211327336472>"

# Emotes for troll romance
emote_maws = "<:q_maws:752228834027241554>"
emote_hats = "<:q_hats:752228833968783441>"
emote_slugs = "<:q_slugs:752228834333556756>"
emote_shields = "<:q_shields:752228833897218159>"
emote_broken_heart = ":broken_heart:"

# Emotes for minesweeper
emote_ms_hidden = ":pick:"
emote_ms_mine = ":x:"
emote_ms_flagged = ":triangular_flag_on_post:"
emote_ms_0 = ":white_circle:"
emote_ms_1 = ":heart:"
emote_ms_2 = ":yellow_heart:"
emote_ms_3 = ":green_heart:"
emote_ms_4 = ":blue_heart:"
emote_ms_5 = ":purple_heart:"
emote_ms_6 = ":six:"
emote_ms_7 = ":seven:"
emote_ms_8 = ":eight:"

# Emote for deleting slime tweets
emote_delete_tweet = emote_blank
# Slime twitter verified checkmark
emote_verified = "<:slime_checkmark:797234128398319626>"

# mining types
mining_type_minesweeper = "minesweeper"
mining_type_pokemine = "pokemine"
mining_type_bubblebreaker = "bubblebreaker"

# mining grid types
mine_grid_type_minesweeper = "minesweeper"
mine_grid_type_pokemine = "pokemining"
mine_grid_type_bubblebreaker = "bubblebreaker"

grid_type_by_mining_type = {
	mining_type_minesweeper: mine_grid_type_minesweeper,
	mining_type_pokemine: mine_grid_type_pokemine,
	mining_type_bubblebreaker: mine_grid_type_bubblebreaker,
}

# mining sweeper
cell_mine = 1
cell_mine_marked = 2
cell_mine_open = 3

cell_empty = -1
cell_empty_marked = -2
cell_empty_open = -3

cell_slime = 0

# bubble breaker
cell_bubble_empty = "0"
cell_bubble_0 = "5"
cell_bubble_1 = "1"
cell_bubble_2 = "2"
cell_bubble_3 = "3"
cell_bubble_4 = "4"

cell_bubbles = [
	cell_bubble_0,
	cell_bubble_1,
	cell_bubble_2,
	cell_bubble_3,
	cell_bubble_4
]

bubbles_to_burst = 4


symbol_map_ms = {
	-1 : "/",
	1 : "/",
	-2 : "+",
	2 : "+",
	3 : "X"
}

symbol_map_pokemine = {
	-1 : "_",
	0 : "~",
	1 : "X",
	11 : ";",
	12 : "/",
	13 : "#"

}

number_emote_map = {
	0 : emote_ms_0,
	1 : emote_ms_1,
	2 : emote_ms_2,
	3 : emote_ms_3,
	4 : emote_ms_4,
	5 : emote_ms_5,
	6 : emote_ms_6,
	7 : emote_ms_7,
	8 : emote_ms_8
}

alphabet = "abcdefghijklmnopqrstuvwxyz"

# map of mines and their respective wall
mines_wall_map = {
	poi_id_mine_sweeper : channel_jrmineswall_sweeper,
	poi_id_tt_mines_sweeper : channel_ttmineswall_sweeper,
	poi_id_cv_mines_sweeper : channel_cvmineswall_sweeper,
	poi_id_mine_bubble : channel_jrmineswall_bubble,
	poi_id_tt_mines_bubble : channel_ttmineswall_bubble,
	poi_id_cv_mines_bubble : channel_cvmineswall_bubble
}

# map of mines and the type of mining done in them
mines_mining_type_map = {
	poi_id_mine_sweeper : mining_type_minesweeper,
	poi_id_cv_mines_sweeper : mining_type_minesweeper,
	poi_id_tt_mines_sweeper : mining_type_minesweeper,
	poi_id_mine_bubble : mining_type_bubblebreaker,
	poi_id_cv_mines_bubble : mining_type_bubblebreaker,
	poi_id_tt_mines_bubble : mining_type_bubblebreaker
}

# list of channels you can !mine in
mining_channels = [
	channel_mines,
	channel_mines_sweeper,
	channel_mines_bubble,
	channel_cv_mines,
	channel_cv_mines_sweeper,
	channel_cv_mines_bubble,
	channel_tt_mines,
	channel_tt_mines_sweeper,
	channel_tt_mines_bubble
]

# trading
trade_state_proposed = 0
trade_state_ongoing = 1
trade_state_complete = 2

# SLIMERNALIA
festivity_on_gift_wrapping = 100
festivity_on_gift_giving = 10000

# Common strings.
str_casino_closed = "The SlimeCorp Casino only operates at night."
str_casino_negaslime_dealer = "\"We don't deal with negaslime around here.\", says the dealer disdainfully."
str_casino_negaslime_machine = "The machine doesn't seem to accept antislime."
str_exchange_closed = "The Exchange has closed for the night."
str_exchange_specify = "Specify how much {currency} you will {action}."
str_exchange_channelreq = "You must go to the #" + channel_stockexchange + " in person to {action} your {currency}."
str_exchange_busy = "You can't {action} right now. Your slimebroker is busy."
str_weapon_wielding_self = "You are wielding"
str_weapon_wielding = "They are wielding"
str_weapon_married_self = "You are married to"
str_weapon_married = "They are married to"
str_eat_raw_material = "You chomp into the raw {}. It isn't terrible, but you feel like there is a more constructive use for it."
str_generic_onadorn = "You successfully adorn your {}."
str_generic_unadorn = "You successfully dedorn your {}."
str_generic_onbreak = "Their {} broke!!"
str_soul_onadorn = "{} has begun swirling around you."
str_soul_unadorn = "{} has stopped swirling around you and you place it back into your hammerspace."
str_soul_onbreak = "{} has ***SHATTERED.*** Uh oh."
str_generic_inv_limit = "You can't fit another {} in your inventory!"

generic_role_name = 'NLACakaNM'

str_generic_subway_description = "A grimy subway train."
str_generic_subway_station_description = "A grimy subway station."
str_blimp_description = "This luxury zeppelin contains all the most exquisite amenities a robber baron in transit could ask for. A dining room, a lounge, a pool table, you know, rich people stuff. Being a huge, highly flammable balloon filled with hydrogen, it is the safest way to travel in the city only because it's out of the price range of most juveniles' budget. It's used by the rich elite to travel from their summer homes in Assault Flats Beach to their winter homes in Dreadford, and vice versa, without having to step foot in the more unsavory parts of the city. It does it's job well and only occasionally bursts into flames."
str_blimp_tower_description = "This mooring mast is mostly used for amassing millionaire mooks into the marvelous Neo Milwaukee multi-story zeppelin, m'lady. Basically, you can board a blimp here. All you have to do is walk up an extremely narrow spiral staircase without an adequate handrail for about 40 feet straight up and then you can embark onto the highest airship this side of the River of Slime! It'll be great! Don't mind the spontaneously combusting zeppelins crashing into the earth in the distance. That's normal."
str_downtown_station_description = "This large, imposing structure is the central hub for the entire city's rapid transit system. A public transportation powerhouse, it contains connections to every subway line in the city, and for dirt cheap. Inside of it's main terminal, a humongous split-flap display is constantly updating with the times of subway arrivals and departures. Hordes of commuters from all across the city sprint to their connecting trains, or simply spill out into the Downtown streets, ready to have their guts do the same.\n\nExits into Downtown NLACakaNM."
str_black_subway_description = "Black Line trains are strictly uniform, with dull, minimalistic furnishings producing a borderline depressing experience. Almost completely grey aside from it's style guide mandated black accents, everything is purely practical. It provides just enough for its commuting salarymen to get to work in the morning and home at night."
str_black_subway_station_description = "This sparsely decorated terminal replicates the feeling of riding on a Black Line train, otherwise known as inducing suicidal thoughts. Dim lighting barely illuminates the moldy, stained terminal walls. Inbound and outbound trains arrive and departure one after another with unreal temporal precision. You're not sure if you've ever seen a Black Line train be late. Still doesn't make you like being on one though."
str_green_subway_description = "Easily the oldest subway line in the city, with the interior design and general cleanliness to prove it. Once cutting edge, it's art deco stylings have begun to deteriorate due to overuse and underfunding. That goes double for the actual trains themselves, with a merely bumpy ride on the Green Line being the height of luxury compared to the far worse potential risks."
str_green_subway_station_description = "Much like its trains, Green Line terminals have fallen into disrepair. It's vintage aesthetic only exasperating it's crumbling infrastructure, making the whole line seem like a old, dilapidated mess. But, you'll give it one thing, it's pretty cool looking from the perspective of urban exploration. You've dreamed of exploring it's vast, abandoned subway networks ever since you first rode on it. They could lead to anywhere. So close, and yet so mysterious."
str_purple_subway_description = "Probably the nicest subway line in the city, the Purple Line isn't defined by its poor hygiene or mechanical condition. Instead, it's defined by its relative normality. More-or-less clean floors, brightly lit interiors, upholstery on the seats. These stunning, almost sci-fi levels of perfection are a sight to behold. Wow!"
str_purple_subway_station_description = "It is clean and well-kempt, just like the Purple Line trains. This relatively pristine subway terminal hosts all manner of unusualities. With limited amounts of graffiti sprayed unto the otherwise sort-of white walls, there's actually some semblance of visual simplicity. For once in this city, your eyes aren't being completely assaulted with information or blinding lights. Boring, this place sucks. Board whatever train you're getting on and get back to killing people as soon as possible."
str_pink_subway_description = "If there's one word to describe the Pink Line, it's \"confusing\". It's by far the filthiest subway line in the city, which is exponentially worsened by it's bizarre, unexplainable faux wood paneling that lines every train. You can only imagine that this design decision was made to make the subway feel less sterile and more homely, but the constant stench of piss and homeless people puking sort of ruins that idea. Riding the Pink Line makes you feel like you're at your grandma's house every single time you ride it, if your grandma's house was in Jaywalker Plain."
str_pink_subway_station_description = "It's absolutely fucking disgusting. By far the worst subway line, the Pink Line can't keep it's terrible interior design choices contained to its actual trains. Even in its terminals, the faux wood paneling clashes with every other aesthetic element present. It's ghastly ceilings have turned a delightful piss-soaked shade of faded white. It's bizarre mixture of homely decorations and completely dilapidated state makes you oddly beguiled in a way. How did they fuck up the Pink Line so bad? The world may never know."
str_gold_subway_description = "Construction started on the Gold Line in the 90’s, and it shows. It’s just so fucking gaudy. Opulent, even. It’s vaporwave gone wrong. Geometric patterns with clashing color combinations and art styles are plastered over every square inch of the walls, and the seats are made of that awful upholstery from old Taco Bell™ booths."
str_gold_subway_station_description = "The walls of the Gold Line are covered in terrible murals. Covered. Imagine your loaded in the level geometry of the station into Unity and then Googled “terrible street art murals” and skipped to page nine and then loaded each image as textures unto the geometry, not even accounting for when one object ended and another surface began. No one knows why it’s like this."
str_subway_connecting_sentence = "Below it, on a lower level of the station, is a {} line terminal."

# TODO: Add descriptions for each outskirt/street.
str_generic_outskirts_description_edge = "It's a small patch of desert on the edge of town. Go any further and you're just asking for trouble."
str_generic_outskirts_description = "It's a wasteland, devoid of all life except for slime beasts."
str_generic_outskirts_description_depths = "The lion's den of the biggest and baddest Secreatures. Stay around too long, and you'll wind up in the jaws of god knows what lurks around here."

str_generic_streets_description = "It's a street. Not much more to be said."

# Common database columns
col_id_server = 'id_server'
col_id_user = 'id_user'

#Database columns for roles
col_id_role = 'id_role'
col_role_name = 'name'

# Database columns for items
col_id_item = "id_item"
col_item_type = "item_type"
col_time_expir = "time_expir"
col_value = "value"
col_stack_max = 'stack_max'
col_stack_size = 'stack_size'
col_soulbound = 'soulbound'
col_template = 'template'

#Database columns for apartments
col_apt_name = 'apt_name'
col_apt_description = 'apt_description'
col_rent = 'rent'
col_apt_class = 'apt_class'
col_num_keys = 'num_keys'
col_key_1 = 'key_1'
col_key_2 = 'key_2'

# Database columns for server
col_icon = "icon"

# Database columns for players
col_avatar = "avatar"
col_display_name = "display_name"

# Database columns for users
col_slimes = 'slimes'
col_slimelevel = 'slimelevel'
col_hunger = 'hunger'
col_totaldamage = 'totaldamage'
col_weapon = 'weapon'
col_weaponskill = 'weaponskill'
col_trauma = 'trauma'
col_slimecoin = 'slimecoin'
col_time_lastkill = 'time_lastkill'
col_time_lastrevive = 'time_lastrevive'
col_id_killer = 'id_killer'
col_time_lastspar = 'time_lastspar'
col_time_lasthaunt = 'time_lasthaunt'
col_time_lastinvest = 'time_lastinvest'
col_bounty = 'bounty'
col_weaponname = 'weaponname'
col_name = 'name'
col_inebriation = 'inebriation'
col_ghostbust = 'ghostbust'
col_faction = 'faction'
col_poi = 'poi'
col_life_state = 'life_state'
col_busted = 'busted'
col_time_last_action = 'time_last_action'
col_weaponmarried = 'weaponmarried'
col_time_lastscavenge = 'time_lastscavenge'
col_bleed_storage = 'bleed_storage'
col_time_lastenter = 'time_lastenter'
col_time_lastoffline = 'time_lastoffline'
col_time_joined = 'time_joined'
col_poi_death = 'poi_death'
col_slime_donations = 'donated_slimes'
col_poudrin_donations = 'donated_poudrins'
col_caught_fish = 'caught_fish'
col_global_swear_jar = 'global_swear_jar'
col_arrested = 'arrested'
col_active_slimeoid = 'active_slimeoid'
col_time_expirpvp = 'time_expirpvp'
col_time_lastenlist = 'time_lastenlist'
col_apt_zone = 'apt_zone'
col_visiting = "visiting"
col_has_soul = 'has_soul'
col_sap = 'sap'
col_hardened_sap = 'hardened_sap'
col_manuscript = "manuscript"
col_spray = "spray"
col_salary_credits = 'salary_credits'
col_degradation = 'degradation'
col_time_lastdeath = 'time_lastdeath'
col_sidearm = 'sidearm'
col_race = 'race'
col_time_racialability = 'time_racialability'
col_time_lastpremiumpurchase = 'time_lastpremiumpurchase'
col_verified = 'verified'

col_attack = 'attack'
col_speed = 'speed'
col_freshness = 'freshness'

#SLIMERNALIA
col_festivity = 'festivity'
col_festivity_from_slimecoin = 'festivity_from_slimecoin'
col_slimernalia_coin_gambled = 'slimernalia_coin_gambled'
col_slimernalia_kingpin = 'slimernalia_kingpin'

# SWILLDERMUK
col_gambit = 'gambit'
col_credence = 'credence'
col_credence_used = 'credence_used'

# GANKERS VS SHAMBLERS
col_gvs_currency = 'gvs_currency'
col_gvs_time_lastshambaquarium = 'gvs_time_lastshambaquarium'
col_horde_cooldown = 'horde_cooldown'
col_gaiaslime = 'gaiaslime'
col_shambler_stock = 'shambler_stock'
col_juviemode = 'juviemode'

# Double Halloween
col_horseman_deaths = 'horseman_deaths'
col_horseman_timeofdeath = 'horseman_timeofdeath'

#Database columns for bartering
col_offer_give = 'offer_give'
col_offer_receive = 'offer_receive'
col_time_sinceoffer = 'time_sinceoffer'

#Database columns for slimeoids
col_id_slimeoid = 'id_slimeoid'
col_body = 'body'
col_head = 'head'
col_legs = 'legs'
col_armor = 'armor'
col_weapon = 'weapon'
col_special = 'special'
col_ai = 'ai'
col_type = 'type'
col_name = 'name'
col_atk = 'atk'
col_defense = 'defense'
col_intel = 'intel'
col_level = 'level'
col_time_defeated = 'time_defeated'
col_clout = 'clout'
col_hue = 'hue'
col_coating = 'coating'

#Database columns for enemies
col_id_enemy = 'id_enemy'
col_enemy_slimes = 'slimes'
col_enemy_totaldamage = 'totaldamage'
col_enemy_ai = 'ai'
col_enemy_type = 'enemytype'
col_enemy_attacktype = 'attacktype'
col_enemy_display_name = 'display_name'
col_enemy_identifier = 'identifier'
col_enemy_level = 'level'
col_enemy_poi = 'poi'
col_enemy_life_state = 'life_state'
col_enemy_bleed_storage = 'bleed_storage'
col_enemy_time_lastenter = 'time_lastenter'
col_enemy_initialslimes = 'initialslimes'
col_enemy_expiration_date = 'expiration_date'
col_enemy_id_target = 'id_target'
col_enemy_raidtimer = 'raidtimer'
col_enemy_rare_status = 'rare_status'
col_enemy_hardened_sap = 'hardened_sap'
col_enemy_weathertype = 'weathertype'
col_enemy_class = 'enemyclass'
col_enemy_owner = 'owner'
col_enemy_gvs_coord = 'gvs_coord'

# Database column for the status of districts with locks on them
col_locked_status = 'locked_status'

# Database columns for user statistics
col_stat_metric = 'stat_metric'
col_stat_value = 'stat_value'

# Database columns for markets
col_time_lasttick = 'time_lasttick'
col_slimes_revivefee = 'slimes_revivefee'
col_negaslime = 'negaslime'
col_clock = 'clock'
col_weather = 'weather'
col_day = 'day'
col_decayed_slimes = 'decayed_slimes'
col_donated_slimes = 'donated_slimes'
col_donated_poudrins = 'donated_poudrins'
col_splattered_slimes = 'splattered_slimes'

# Database columns for stocks
col_stock = 'stock'
col_market_rate = 'market_rate'
col_exchange_rate = 'exchange_rate'
col_boombust = 'boombust'
col_total_shares = 'total_shares'

# Database columns for companies
col_total_profits = 'total_profits'
col_recent_profits = 'recent_profits'

# Database columns for shares
col_shares = 'shares'

# Database columns for stats
col_total_slime = 'total_slime'
col_total_slimecoin = 'total_slimecoin'
col_total_players = 'total_players'
col_total_players_pvp = 'total_players_pvp'
col_timestamp = 'timestamp'

# Database columns for districts
col_district = 'district'
col_controlling_faction = 'controlling_faction'
col_capturing_faction = 'capturing_faction'
col_capture_points = 'capture_points'
col_district_slimes = 'slimes'
col_time_unlock = 'time_unlock'
col_cap_side = 'cap_side'

# Database columns for mutations
col_id_mutation = 'mutation'
col_mutation_data = 'data'
col_mutation_counter = 'mutation_counter'
col_tier = 'tier'
col_artificial = 'artificial'
col_rand_seed = 'rand_seed'
col_time_lasthit = 'time_lasthit'

# Database columns for transports
col_transport_type = 'transport_type'
col_current_line = 'current_line'
col_current_stop = 'current_stop'

# Database columns for farms
col_farm = 'farm'
col_time_lastsow = 'time_lastsow'
col_phase = 'phase'
col_time_lastphase = 'time_lastphase'
col_slimes_onreap = 'slimes_onreap'
col_action_required = 'action_required'
col_crop = 'crop'
col_sow_life_state = 'sow_life_state'

# Database columns for troll romance
col_quadrant = 'quadrant'
col_quadrants_target = 'id_target'
col_quadrants_target2 = 'id_target2'

# Database columns for status effects
col_id_status = 'id_status'
col_source = 'source'
col_status_target = 'id_target'

# Database columns for world events
col_id_event = 'id_event'
col_event_type = 'event_type'
col_time_activate = 'time_activate'

# Database columns for advertisements
col_id_ad = 'id_ad'
col_id_sponsor = 'id_sponsor'
col_ad_content = 'content'

# Database columns for books
col_id_book = "id_book"
col_title = "title"
col_author = "author"
col_book_state = "book_state"
col_date_published = "date_published"
col_genre = "genre"
col_length = "length"
col_sales = "sales"
col_rating = "rating"
col_rates = "rates"
col_pages = "pages"

# Database columns for pages of books
col_page = "page"
col_contents = "contents"

# Database columns for book sales
col_bought = "bought"

# Database columns for inhabitation
col_id_ghost = "id_ghost"
col_id_fleshling = "id_fleshling"
col_empowered = "empowered"

# Database columns for hues
col_id_hue = "id_hue"
col_is_neutral = "is_neutral"
col_hue_analogous_1 = "hue_analogous_1"
col_hue_analogous_2 = "hue_analogous_2"
col_hue_splitcomp_1 = "hue_splitcomp_1"
col_hue_splitcomp_2 = "hue_splitcomp_2"
col_hue_fullcomp_1 = "hue_fullcomp_1"
col_hue_fullcomp_2 = "hue_fullcomp_2"






# Item type names
it_item = "item"
it_medal = "medal"
it_questitem = "questitem"
it_food = "food"
it_weapon = "weapon"
it_cosmetic = 'cosmetic'
it_furniture = 'furniture'
it_book = 'book'

# Cosmetic item rarities
rarity_plebeian = "Plebeian"
rarity_patrician = "Patrician"
rarity_promotional = "Promotional" # Cosmetics that should not be awarded through smelting/hunting
rarity_princeps = "princeps"

# Leaderboard score categories
leaderboard_slimes = "SLIMIEST"
leaderboard_slimecoin = "SLIMECOIN BARONS"
leaderboard_ghosts = "ANTI-SLIMIEST"
leaderboard_podrins = "PODRIN LORDS"
leaderboard_bounty = "MOST WANTED"
leaderboard_kingpins = "KINGPINS' COFFERS"
leaderboard_districts = "DISTRICTS CONTROLLED"
leaderboard_donated = "LOYALEST CONSUMERS"
leaderboard_fashion = "NLACakaNM'S TOP MODELS"
#SLIMERNALIA
leaderboard_slimernalia = "MOST FESTIVE"
#INTERMISSION2
leaderboard_degradation = "MOST DEGRADED"
leaderboard_shamblers_killed = "MOST SHAMBLER KILLS"
#SWILLDERKMUK
leaderboard_gambit_high = "HIGHEST GAMBIT"
leaderboard_gambit_low = "LOWEST GAMBIT"

# leaderboard entry types
entry_type_player = "player"
entry_type_districts = "districts"

# district control channel topic text
control_topic_killers = "Currently controlled by the killers."
control_topic_rowdys = "Currently controlled by the rowdys."
control_topic_neutral = "Currently controlled by no one."

control_topics = {
	faction_killers: control_topic_killers,
	faction_rowdys: control_topic_rowdys,
	#"": control_topic_neutral  # no faction
	"": "", # The neutral control thing is a bit messy, disable this for now...
}

# district control actors
actor_decay = "decay"

# degradation strings
channel_topic_degraded = "(Closed indefinitely)"
str_zone_degraded = "{poi} has been degraded too far to keep operating."

# The highest and lowest level your weaponskill may be on revive. All skills over this level reset to these.
weaponskill_max_onrevive = 6
weaponskill_min_onrevive = 0

# User statistics we track
stat_max_slimes = 'max_slimes'
stat_lifetime_slimes = 'lifetime_slimes'
stat_lifetime_slimeloss = 'lifetime_slime_loss'
stat_lifetime_slimesdecayed = 'lifetime_slimes_decayed'
stat_slimesmined = 'slimes_mined'
stat_max_slimesmined = 'max_slimes_mined'
stat_lifetime_slimesmined = 'lifetime_slimes_mined'
stat_slimesfromkills = 'slimes_from_kills'
stat_max_slimesfromkills = 'max_slimes_from_kills'
stat_lifetime_slimesfromkills = 'lifetime_slimes_from_kills'
stat_slimesfarmed = 'slimes_farmed'
stat_max_slimesfarmed = 'max_slimes_farmed'
stat_lifetime_slimesfarmed = 'lifetime_slimes_farmed'
stat_slimesscavenged = 'slimes_scavenged'
stat_max_slimesscavenged = 'max_slimes_scavenged'
stat_lifetime_slimesscavenged = 'lifetime_slimes_scavenged'
stat_lifetime_slimeshaunted = 'lifetime_slimes_haunted'
stat_max_level = 'max_level'
stat_max_ghost_level = 'max_ghost_level'
stat_max_hitsurvived = 'max_hit_survived'
stat_max_hitdealt = 'max_hit_dealt'
stat_max_hauntinflicted = 'max_haunt_inflicted'
stat_kills = 'kills'
stat_max_kills = 'max_kills'
stat_biggest_kill = 'biggest_kill'
stat_lifetime_kills = 'lifetime_kills'
stat_lifetime_ganks = 'lifetime_ganks'
stat_lifetime_takedowns = 'lifetime_takedowns'
stat_max_wepskill = 'max_wep_skill'
stat_max_slimecoin = 'max_slime_coins'
stat_lifetime_slimecoin = 'lifetime_slime_coins'
stat_slimecoin_spent_on_revives = 'slimecoins_spent_on_revives'
stat_biggest_casino_win = 'biggest_casino_win'
stat_biggest_casino_loss = 'biggest_casino_loss'
stat_lifetime_casino_winnings = 'lifetime_casino_winnings'
stat_lifetime_casino_losses = 'lifetime_casino_losses'
stat_total_slimecoin_invested = 'total_slimecoin_invested'
stat_total_slimecoin_withdrawn = 'total_slimecoin_withdrawn'
stat_total_slimecoin_from_recycling = 'total_slimecoin_from_recycling'
stat_total_slimecoin_from_swearing = 'total_slimecoin_from_swearing'
stat_total_slimecoin_from_salary = 'total_slimecoin_from_salary'
stat_bounty_collected = 'bounty_collected'
stat_max_bounty = 'max_bounty'
stat_ghostbusts = 'ghostbusts'
stat_biggest_bust_level = 'biggest_bust_level'
stat_lifetime_ghostbusts = 'lifetime_ghostbusts'
stat_max_ghostbusts = 'max_ghostbusts'
stat_max_poudrins = 'max_poudrins'
stat_poudrins_looted = 'poudrins_looted'
stat_lifetime_poudrins = 'lifetime_poudrins'
stat_lifetime_damagedealt = 'lifetime_damage_dealt'
stat_lifetime_selfdamage = 'lifetime_self_damage'
stat_lifetime_deaths = 'lifetime_deaths'
#Track revolver trigger pulls survived?
stat_lifetime_spins_survived = 'lifetime_spins_survived'
stat_max_spins_survived = 'max_spins_survived'
stat_capture_points_contributed = 'capture_points_contributed'
stat_pve_kills = 'pve_kills'
stat_max_pve_kills = 'max_pve_kills'
stat_lifetime_pve_kills = 'lifetime_pve_kills'
stat_lifetime_pve_takedowns = 'lifetime_pve_takedowns'
stat_lifetime_pve_ganks = 'lifetime_pve_ganks'
stat_lifetime_pve_deaths = 'lifetime_pve_deaths'
stat_capture_points_contributed = 'capture_points_contributed'
stat_shamblers_killed = 'shamblers_killed'

stat_revolver_kills = 'revolver_kills'
stat_dual_pistols_kills = 'dual_pistols_kills'
stat_shotgun_kills = 'shotgun_kills'
stat_rifle_kills = 'rifle_kills'
stat_smg_kills = 'smg_kills'
stat_minigun_kills = 'miningun_kills'
stat_bat_kills = 'bat_kills'
stat_brassknuckles_kills = 'brassknuckles_kills'
stat_katana_kills = 'katana_kills'
stat_broadsword_kills = 'broadsword_kills'
stat_nunchucks_kills = 'nunchucks_kills'
stat_scythe_kills = 'scythe_kills'
stat_yoyo_kills = 'yoyo_kills'
stat_knives_kills = 'knives_kills'
stat_molotov_kills = 'molotov_kills'
stat_grenade_kills = 'grenade_kills'
stat_garrote_kills = 'garrote_kills'
stat_pickaxe_kills = 'pickaxe_kills'
stat_fishingrod_kills = 'fishingrod_kills'
stat_bass_kills = 'bass_kills'
stat_bow_kills = 'bow_kills'
stat_umbrella_kills = 'umbrella_kills'
stat_dclaw_kills = 'dclaw_kills'
stat_spraycan_kills = 'spraycan_kills'
stat_paintgun_kills = 'paintgun_kills'
stat_paintroller_kills = 'paintroller_kills'
stat_paintbrush_kills = 'paintbrush_kills'
stat_watercolor_kills = 'watercolor_kills'
stat_thinnerbomb_kills = 'thinnerbomb_kills'
stat_staff_kills = 'staff_kills'
stat_hoe_kills = 'hoe_kills'
stat_pitchfork_kills = 'pitchfork_kills'
stat_shovel_kills = 'shovel_kills'
stat_slimeringcan_kills = 'slimeringcan_kills'
stat_fingernails_kills = 'fingernails_kills'
stat_roomba_kills = 'roomba_kills'
stat_chainsaw_kills = 'chainsaw_kills'
stat_megachainsaw_kills = 'megachainsaw_kills'

# Categories of events that change your slime total, for statistics tracking
source_mining = 0
source_damage = 1
source_killing = 2
source_self_damage = 3
source_busting = 4
source_haunter = 5
source_haunted = 6
source_spending = 7
source_decay = 8
source_ghostification = 9
source_bleeding = 10
source_scavenging = 11
source_farming = 12
source_fishing = 13
source_squeeze = 14
source_weather = 15
source_crush = 16
source_casino = 17
source_slimeoid_betting = 18
source_ghost_contract = 19

# Categories of events that change your slimecoin total, for statistics tracking
coinsource_spending = 0
coinsource_donation = 1
coinsource_bounty = 2
coinsource_revival = 3
coinsource_casino = 4
coinsource_transfer = 5
coinsource_invest = 6
coinsource_withdraw = 7
coinsource_recycle = 8
coinsource_swearjar = 9
coinsource_salary = 10

# Causes of death, for statistics tracking
cause_killing = 0
cause_mining = 1
cause_grandfoe = 2
cause_donation = 3
cause_busted = 4
cause_suicide = 5
cause_leftserver = 6
cause_drowning = 7
cause_falling = 8
cause_bleeding = 9
cause_burning = 10
cause_killing_enemy = 11
cause_weather = 12
cause_cliff = 13
cause_backfire = 14
cause_praying = 15

# List of user statistics that reset to 0 on death
stats_clear_on_death = [
	stat_slimesmined,
	stat_slimesfromkills,
	stat_kills,
	stat_pve_kills,
	stat_ghostbusts,
	stat_slimesfarmed,
	stat_slimesscavenged
]

context_slimeoidheart = 'slimeoidheart'
context_slimeoidbottle = 'slimeoidbottle'
context_slimeoidfood = 'slimeoidfood'
context_wrappingpaper = 'wrappingpaper'
context_prankitem = 'prankitem'
context_seedpacket = 'seedpacket'
context_tombstone = 'tombstone'

# Item vendor names.
vendor_bar = 'bar'	#rate of non-mtn dew drinks are 100 slime to 9 hunger
vendor_pizzahut = 'Pizza Hut'	#rate of fc vendors are 100 slime to 10 hunger
vendor_tacobell = 'Taco Bell'
vendor_kfc = 'KFC'
vendor_mtndew = 'Mtn Dew Fountain'
vendor_vendingmachine = 'vending machine'
vendor_seafood = 'Red Mobster Seafood'	#rate of seafood is 100 slime to 9 hunger
vendor_diner = "Smoker's Cough"	#rate of drinks are 100 slime to 15 hunger
vendor_beachresort = "Beach Resort" #Just features clones from the Speakeasy and Red Mobster
vendor_countryclub = "Country Club" #Just features clones from the Speakeasy and Red Mobster
vendor_farm = "Farm" #contains all the vegetables you can !reap
vendor_bazaar = "bazaar"
vendor_college = "College" #You can buy game guides from either of the colleges
vendor_glocksburycomics = "Glocksbury Comics" #Repels and trading cards are sold here
vendor_slimypersuits = "Slimy Persuits" #You can buy candy from here
vendor_greencakecafe = "Green Cake Cafe" #Brunch foods
vendor_bodega = "Bodega" # Clothing store in Krak Bay
vendor_secretbodega = "Secret Bodega" # The secret clothing store in Krak Bay
vendor_wafflehouse = "Waffle House" # waffle house in the void, sells non-perishable foods, 100 slime to 1 hunger
vendor_basedhardware = "Based Hardware" # Hardware store in West Glocksbury
vendor_lab = "Lab" #Slimecorp products
vendor_atomicforest = "Atomic Forest Stockpile" # Storage of atomic forest
vendor_downpourlaboratory = "Downpour Armament Vending Machines" # Store for shamblers to get stuff
vendor_breakroom = "The Breakroom" # Security officers can order items here for free.
vendor_rpcity = "RP City" # Double halloween costume store

item_id_slimepoudrin = 'slimepoudrin'
item_id_negapoudrin = 'negapoudrin'
item_id_monstersoup = 'monstersoup'
item_id_doublestuffedcrust = 'doublestuffedcrust'
item_id_quadruplestuffedcrust = 'quadruplestuffedcrust'
item_id_octuplestuffedcrust = "octuplestuffedcrust"
item_id_sexdecuplestuffedcrust = "sexdecuplestuffedcrust"
item_id_duotrigintuplestuffedcrust = "duotrigintuplestuffedcrust"
item_id_quattuorsexagintuplestuffedcrust = "quattuorsexagintuplestuffedcrust"
item_id_forbiddenstuffedcrust = "theforbiddenstuffedcrust"
item_id_forbidden111 = "theforbiddenoneoneone"
item_id_tradingcardpack = "tradingcardpack"
item_id_stick = "stick"
item_id_gameguide = "gameguide"
item_id_juviegradefuckenergybodyspray = "juviegradefuckenergybodyspray"
item_id_superduperfuckenergybodyspray = "superduperfuckenergybodyspray"
item_id_gmaxfuckenergybodyspray = "gmaxfuckenergybodyspray"
item_id_costumekit = "costumekit"
item_id_doublehalloweengrist = "doublehalloweengrist"
item_id_whitelineticket = "ticket"
item_id_seaweedjoint = "seaweedjoint"
item_id_megaslimewrappingpaper = "megaslimewrappingpaper"
item_id_greeneyesslimedragonwrappingpaper = "greeneyesslimedragonwrappingpaper"
item_id_phoebuswrappingpaper = "phoebuswrappingpaper"
item_id_slimeheartswrappingpaper = "slimeheartswrappingpaper"
item_id_slimeskullswrappingpaper = "slimeskullswrappingpaper"
item_id_shermanwrappingpaper = "shermanwrappingpaper"
item_id_slimecorpwrappingpaper = "slimecorpwrappingpaper"
item_id_pickaxewrappingpaper = "pickaxewrappingpaper"
item_id_munchywrappingpaper = "munchywrappingpaper"
item_id_benwrappingpaper = "benwrappingpaper"
item_id_gellphone = "gellphone"
item_id_royaltypoudrin = "royaltypoudrin"
item_id_prankcapsule = "prankcapsule"
item_id_cool_material = "coolbeans"
item_id_tough_material = "toughnails"
item_id_smart_material = "smartcookies"
item_id_beautiful_material = "beautyspots"
item_id_cute_material = "cutebuttons"
item_id_dragonsoul = "dragonsoul"
item_id_monsterbones = "monsterbones"
item_id_faggot = "faggot"
item_id_doublefaggot = "doublefaggot"
item_id_seaweed = "seaweed"
item_id_string = "string"
item_id_tincan = "tincan"
item_id_oldboot = "oldboot"
item_id_leather = "leather"
item_id_ironingot = "ironingot"
item_id_bloodstone = "bloodstone"
item_id_tanningknife = "tanningknife"
item_id_dinoslimemeat = "dinoslimemeat"
item_id_dinoslimesteak = "dinoslimesteak"
item_id_dyesolution = "dyesolution"
item_id_textiles = "textiles"
item_id_foodbase = "foodbase"
item_id_civilianscalp = "civilianscalp"
item_id_modelovaccine = "modelovirusvaccine"
item_id_gaiaseedpack_poketubers = "poketubersseedpacket"
item_id_gaiaseedpack_pulpgourds = "pulpgourdsseedpacket"
item_id_gaiaseedpack_sourpotatoes = "sourpotatoesseedpacket"
item_id_gaiaseedpack_bloodcabbages = "bloodcabbagesseedpacket"
item_id_gaiaseedpack_joybeans = "joybeansseedpacket"
item_id_gaiaseedpack_purplekilliflower = "purplekilliflowerseedpacket"
item_id_gaiaseedpack_razornuts = "razornutsseedpacket"
item_id_gaiaseedpack_pawpaw = "pawpawseedpacket"
item_id_gaiaseedpack_sludgeberries = "sludgeberriesseedpacket"
item_id_gaiaseedpack_suganmanuts = "suganmanutsseedpacket"
item_id_gaiaseedpack_pinkrowddishes = "pinkrowddishesseedpacket"
item_id_gaiaseedpack_dankwheat = "dankwheatseedpacket"
item_id_gaiaseedpack_brightshade = "brightshadeseedpacket"
item_id_gaiaseedpack_blacklimes = "blacklimesseedpacket"
item_id_gaiaseedpack_phosphorpoppies = "phosphorpoppiesseedpacket"
item_id_gaiaseedpack_direapples = "direapplesseedpacket"
item_id_gaiaseedpack_rustealeaves = "rustealeavesseedpacket"
item_id_gaiaseedpack_metallicaps = "metallicapsseedpacket"
item_id_gaiaseedpack_steelbeans = "steelbeansseedpacket"
item_id_gaiaseedpack_aushucks = "aushucksseedpacket"
item_id_tombstone_defaultshambler = "defaultshamblertombstone"
item_id_tombstone_bucketshambler = "bucketshamblertombstone"
item_id_tombstone_juveolanternshambler = "juveolanternshamblertombstone"
item_id_tombstone_flagshambler = "flagshamblertombstone"
item_id_tombstone_shambonidriver = "shambonidrivertombstone"
item_id_tombstone_mammoshambler = "mammoshamblertombstone"
item_id_tombstone_gigashambler = "gigashamblertombstone"
item_id_tombstone_microshambler = "microshamblertombstone"
item_id_tombstone_shamblersaurusrex = "shamblesaurusrextombstone"
item_id_tombstone_shamblerdactyl = "shamblerdactyltombstone"
item_id_tombstone_dinoshambler = "dinoshamblertombstone"
item_id_tombstone_ufoshambler = "ufoshamblertombstone"
item_id_tombstone_brawldenboomer = "brawldenboomertombstone"
item_id_tombstone_juvieshambler = "juvieshamblertombstone"
item_id_tombstone_shambleballplayer = "shambleballplayertombstone"
item_id_tombstone_shamblerwarlord = "shamblerwarlordtombstone"
item_id_tombstone_shamblerraider = "shamblerraidertombstone"
item_id_gaiaslimeoid_pot = "gaiaslimeoidpot"

#SLIMERNALIA
item_id_sigillaria = "sigillaria"

#SWILLDERMUK
# Instant use items
item_id_creampie = "creampie"
item_id_waterballoon = "waterbaloon"
item_id_bungisbeam = "bungisbeam"
item_id_circumcisionray = "circumcisionray"
item_id_cumjar = "cumjar"
item_id_discounttransbeam = "discounttransbeam"
item_id_transbeamreplica = "transbeamreplica"
item_id_bloodtransfusion = "bloodtransfusion"
item_id_transformationmask = "transformationmask"
item_id_emptychewinggumpacket = "emptychewinggumpacket"
item_id_airhorn = "airhorn"
item_id_banggun = "banggun"
item_id_pranknote = "pranknote"
item_id_bodynotifier = "bodynotifier"
# Response items
item_id_chinesefingertrap = "chinesefingertrap"
item_id_japanesefingertrap = "japanesefingertrap"
item_id_sissyhypnodevice = "sissyhypnodevice"
item_id_piedpiperkazoo = "piedpiperkazoo"
item_id_sandpapergloves = "sandpapergloves"
item_id_ticklefeather = "ticklefeather"
item_id_genitalmutilationinstrument = "gentialmutilationinstrument"
item_id_gamerficationasmr = "gamerficationasmr"
item_id_beansinacan = "beansinacan"
item_id_brandingiron = "brandingiron"
item_id_lasso = "lasso"
item_id_fakecandy = "fakecandy"
item_id_crabarmy = "crabarmy"
# Trap items
item_id_whoopiecushion = "whoopiecushion"
item_id_beartrap = "beartrap"
item_id_bananapeel = "bananapeel"
item_id_windupbox = "windupbox"
item_id_windupchatterteeth = "windupchatterteeth"
item_id_snakeinacan = "snakeinacan"
item_id_landmine = "landmine"
item_id_freeipad = "freeipad"
item_id_freeipad_alt = "freeipad_alt"
item_id_perfectlynormalfood = "perfectlynormalfood"
item_id_pitfall = "pitfall"
item_id_electrocage = "electrocage"
item_id_ironmaiden = "ironmaiden"
item_id_signthatmakesyoubensaint = "signthatmakesyoubensaint"
item_id_piebomb = "piebomb"
item_id_defectivealarmclock = "defectivealarmclock"
item_id_alligatortoy = "alligatortoy"
item_id_janusmask = "janusmask"
item_id_swordofseething = "swordofseething"

prank_type_instantuse = 'instantuse'
prank_type_response = 'response'
prank_type_trap = 'trap'
prank_rarity_heinous = 'heinous'
prank_rarity_scandalous = 'scandalous'
prank_rarity_forbidden = 'forbidden'
prank_type_text_instantuse = '\n\nPrank Type: Instant Use - Good for hit-and-run tactics.'
prank_type_text_response = '\n\nPrank Type: Response - Use it on an unsuspecting bystander.'
prank_type_text_trap = '\n\nPrank Type: Trap - Lay it down in a district.'

#candy ids
item_id_paradoxchocs = "paradoxchocs"
item_id_licoricelobsters = "licoricelobsters"
item_id_chocolateslimecorpbadges = "chocolateslimecorpbadges"
item_id_munchies = "munchies"
item_id_sni = "sni"
item_id_twixten = "twixten"
item_id_slimybears = "slimybears"
item_id_marsbar = "marsbar"
item_id_magickspatchkids = "magickspatchkids"
item_id_atms = "atms"
item_id_seanis = "seanis"
item_id_candybungis = "candybungis"
item_id_turstwerthers = "turstwerthers"
item_id_poudrinpops = "poudrinpops"
item_id_juvieranchers = "juvieranchers"
item_id_krakel = "krakel"
item_id_swedishbassedgods = "swedishbassedgods"
item_id_bustahfingers = "bustahfingers"
item_id_endlesswarheads = "endlesswarheads"
item_id_n8heads = "n8heads"
item_id_strauberryshortcakes = "strauberryshortcakes"
item_id_chutzpahcherries = "chutzpahcherries"
item_id_n3crunch = "n3crunch"
item_id_slimesours = "slimesours"

#slimeoid food
item_id_fragilecandy = "fragilecandy" #+chutzpah -grit
item_id_rigidcandy = "rigidcandy" #+grit -chutzpah
item_id_recklesscandy = "recklesscandy" #+moxie -grit
item_id_reservedcandy = "reservedcandy" #+grit -moxie
item_id_bluntcandy = "bluntcandy" #+moxie -chutzpah
item_id_insidiouscandy = "insidiouscandy" #+chutzpah -moxie

#vegetable ids
item_id_poketubers = "poketubers"
item_id_pulpgourds = "pulpgourds"
item_id_sourpotatoes = "sourpotatoes"
item_id_bloodcabbages = "bloodcabbages"
item_id_joybeans = "joybeans"
item_id_purplekilliflower = "purplekilliflower"
item_id_razornuts = "razornuts"
item_id_pawpaw = "pawpaw"
item_id_sludgeberries = "sludgeberries"
item_id_suganmanuts = "suganmanuts"
item_id_pinkrowddishes = "pinkrowddishes"
item_id_dankwheat = "dankwheat"
item_id_brightshade = "brightshade"
item_id_blacklimes = "blacklimes"
item_id_phosphorpoppies = "phosphorpoppies"
item_id_direapples = "direapples"
item_id_rustealeaves = "rustealeaves"
item_id_metallicaps = "metallicaps"
item_id_steelbeans = "steelbeans"
item_id_aushucks = "aushucks"

#vegetable materials
item_id_poketubereyes = "poketubereyes"
item_id_pulpgourdpulp = "pulpgourdpulp"
item_id_sourpotatoskins = "sourpotatoskins"
item_id_bloodcabbageleaves = "bloodcabbageleaves"
item_id_joybeanvines = "joybeanvines"
item_id_purplekilliflowerflorets = "purplekilliflowerflorets"
item_id_razornutshells = "razornutshells"
item_id_pawpawflesh = "pawpawflesh"
item_id_sludgeberrysludge = "sludgeberrysludge"
item_id_suganmanutfruit = "suganmanutfruit"
item_id_pinkrowddishroot = "pinkrowddishroot"
item_id_dankwheatchaff = "dankwheatchaff"
item_id_brightshadeberries = "brightshadeberries"
item_id_blacklimeade = "blacklimeade"
item_id_phosphorpoppypetals = "phosphorpoppypetals"
item_id_direapplestems = "direapplestems"
item_id_rustealeafblades = "rustealeafblades"
item_id_metallicapheads = "metallicapheads"
item_id_steelbeanpods = "steelbeanpods"
item_id_aushuckstalks = "aushuckstalks"

# dye ids
item_id_dye_black = "blackdye"
item_id_dye_pink = "pinkdye"
item_id_dye_green = "greendye"
item_id_dye_brown = "browndye"
item_id_dye_grey = "greydye"
item_id_dye_purple = "purpledye"
item_id_dye_teal = "tealdye"
item_id_dye_orange = "orangedye"
item_id_dye_cyan = "cyandye"
item_id_dye_red = "reddye"
item_id_dye_lime = "limedye"
item_id_dye_yellow = "yellowdye"
item_id_dye_blue = "bluedye"
item_id_dye_magenta = "magentadye"
item_id_dye_cobalt = "cobaltdye"
item_id_dye_white = "whitedye"
item_id_dye_rainbow = "rainbowdye"
item_id_paint_copper = "copperpaint"
item_id_paint_chrome = "chromepaint"
item_id_paint_gold = "goldpaint"

#weapon ids
weapon_id_revolver = 'revolver'
weapon_id_dualpistols = 'dualpistols'
weapon_id_shotgun = 'shotgun'
weapon_id_rifle = 'rifle'
weapon_id_smg = 'smg'
weapon_id_minigun = 'minigun'
weapon_id_bat = 'bat'
weapon_id_brassknuckles = 'brassknuckles'
weapon_id_katana = 'katana'
weapon_id_broadsword = 'broadsword'
weapon_id_nunchucks = 'nun-chucks'
weapon_id_scythe = 'scythe'
weapon_id_yoyo = 'yo-yo'
weapon_id_knives = 'knives'
weapon_id_molotov = 'molotov'
weapon_id_grenades = 'grenades'
weapon_id_garrote = 'garrote'
weapon_id_pickaxe = 'pickaxe'
weapon_id_fishingrod = 'fishingrod'
weapon_id_bass = 'bass'
weapon_id_umbrella = 'umbrella'
weapon_id_bow = 'bow'
weapon_id_dclaw = 'dclaw'
weapon_id_staff = 'staff'
weapon_id_laywaster = 'laywaster'
weapon_id_chainsaw = 'chainsaw'

weapon_id_spraycan = 'spraycan'
weapon_id_paintgun = 'paintgun'
weapon_id_paintroller = 'paintroller'
weapon_id_paintbrush = 'paintbrush'
weapon_id_watercolors = 'watercolors'
weapon_id_thinnerbomb = 'thinnerbomb'

weapon_id_hoe = 'hoe'
weapon_id_pitchfork = 'pitchfork'
weapon_id_shovel = 'shovel'
weapon_id_slimeringcan = 'slimeringcan'

weapon_id_fingernails = 'fingernails'
weapon_id_roomba = 'roomba'

theforbiddenoneoneone_desc = "This card that you hold in your hands contains an indescribably powerful being known simply " \
	"as The Forbidden {emote_111}. It is an unimaginable horror, a beast of such supreme might that wields " \
	"destructive capabilities that is beyond any human’s true understanding. And for its power, " \
	"the very fabric of reality conspired to dismember and seal The Forbidden {emote_111} away into the most " \
	"obscured, nightmarish cages conceivable: trading cards. Now you, foolish mortal, have revived " \
	"this ancient evil. Once again this slime-starved beast may roam the lands, obliterating all life " \
	"that dares to evolve."
forbiddenstuffedcrust_eat = "Dough, pepperoni, grease, marinara and cheese. Those five simple ingredients folded into one " \
	"another thousands upon thousands of times, and multiplied in quantity exponentially over the " \
	"course of weeks. That is what has begat this, an affront to god and man. To explain the ramifications " \
	"of the mere existence of this pizza is pointless. You could not comprehend the amount of temporal " \
	"and spatial destruction you have caused this day. The very fabric of space and time cry out in agony, " \
	"bleeding from the mortal wound you have inflicted upon them. Imbued into every molecule of this " \
	"monstrosity is exactly one word, one thought, one concept. Hate. Hate for conscious life, in concept. " \
	"Deep inside of this pizza, a primordial evil is sealed away for it’s sheer destructive power. Escaped " \
	"from its original prison only to be caged in another. To release, all one needs to do is do exactly " \
	"what you are doing. That is to say, eat a slice. They don’t even need to finish it, as after the very " \
	"first bite it will be free. Go on. It’s about that time, isn’t it? You gaze upon this, the epitome of " \
	"existential dread that you imprudently smelted, and despair. Tepidly, you bring the first slice to your " \
	"tongue, letting the melted cheese drizzle unto your awaiting tongue. There are no screams. There is no time. " \
	"There is only discord. And then, nothing."
forbiddenstuffedcrust_desc = "What are you waiting for? You’ve come this far, why do you hesitate? Useless. Useless, useless, useless. " \
	"Escaping your purpose is impossible. Not destiny, purpose. You were never truly alive, never truly free. " \
	"Your one, singular purpose, that you were created to fulfill, is on the precipice of completion. You’ve " \
	"sought that absolution all your life, haven’t you? You’ve begged to be given the answer, to be shown that " \
	"you and your family and your friends were put on this planet for a purpose. Well, here it is. Here is what " \
	"you were meant to do. Don’t fight it. It’s useless. Useless, useless, useless. Don’t keep the universe waiting. " \
	"It’s ready to die. Slather it in some low-quality marinara, toss it up into the air like in the old movies, and " \
	"shove it into the oven, to teach it the true meaning of heat death. Eat a slice of that motherfucking pizza."

# General items that should have a cooldown on how often they can be purchased
premium_items = [item_id_metallicaps, item_id_steelbeans, item_id_aushucks]
# General items that should show their current durability on !inspect
durability_items = [
	item_id_paint_copper,
	item_id_paint_chrome,
	item_id_paint_gold,
	item_id_gaiaseedpack_poketubers,
	item_id_gaiaseedpack_pulpgourds,
	item_id_gaiaseedpack_sourpotatoes,
	item_id_gaiaseedpack_bloodcabbages,
	item_id_gaiaseedpack_joybeans,
	item_id_gaiaseedpack_purplekilliflower,
	item_id_gaiaseedpack_razornuts,
	item_id_gaiaseedpack_pawpaw,
	item_id_gaiaseedpack_sludgeberries,
	item_id_gaiaseedpack_suganmanuts,
	item_id_gaiaseedpack_pinkrowddishes,
	item_id_gaiaseedpack_dankwheat,
	item_id_gaiaseedpack_brightshade,
	item_id_gaiaseedpack_blacklimes,
	item_id_gaiaseedpack_phosphorpoppies,
	item_id_gaiaseedpack_direapples,
	item_id_gaiaseedpack_rustealeaves,
	item_id_gaiaseedpack_metallicaps,
	item_id_gaiaseedpack_steelbeans,
	item_id_gaiaseedpack_aushucks
]

# List of normal items.
item_list = [
	EwGeneralItem(
		id_item = item_id_slimepoudrin,
		alias = [
			"poudrin",
		],
		context = "poudrin",
		str_name = "Slime Poudrin",
		str_desc = "A dense, crystalized chunk of precious slime.",
		acquisition = acquisition_mining,
	),
	EwGeneralItem(
		id_item = item_id_dye_white,
		context = "dye",
		str_name = "White Dye",
		str_desc = "A small vial of white dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_yellow,
		context = "dye",
		str_name = "Yellow Dye",
		str_desc = "A small vial of yellow dye.",
		acquisition = acquisition_smelting,
	),

	EwGeneralItem(
		id_item = item_id_dye_orange,
		context = "dye",
		str_name = "Orange Dye",
		str_desc = "A small vial of orange dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_red,
		context = "dye",
		str_name = "Red Dye",
		str_desc = "A small vial of red dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_magenta,
		context = "dye",
		str_name = "Magenta Dye",
		str_desc = "A small vial of magenta dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_purple,
		context = "dye",
		str_name = "Purple Dye",
		str_desc = "A small vial of purple dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_blue,
		context = "dye",
		str_name = "Blue Dye",
		str_desc = "A small vial of blue dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_green,
		context = "dye",
		str_name = "Green Dye",
		str_desc = "A small vial of green dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_teal,
		context = "dye",
		str_name = "Teal Dye",
		str_desc = "A small vial of teal dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_rainbow,
		context = "dye",
		str_name = "***Rainbow Dye!!***",
		str_desc = "***A small vial of Rainbow dye!!***",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_pink,
		context = "dye",
		str_name = "Pink Dye",
		str_desc = "A small vial of pink dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_grey,
		context = "dye",
		str_name = "Grey Dye",
		str_desc = "A small vial of grey dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_cobalt,
		context = "dye",
		str_name = "Cobalt Dye",
		str_desc = "A small vial of cobalt dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_black,
		context = "dye",
		str_name = "Black Dye",
		str_desc = "A small vial of black dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_lime,
		context = "dye",
		str_name = "Lime Dye",
		str_desc = "A small vial of lime dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_cyan,
		context = "dye",
		str_name = "Cyan Dye",
		str_desc = "A small vial of cyan dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_dye_brown,
		context = "dye",
		str_name = "Brown Dye",
		str_desc = "A small vial of brown dye.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_paint_copper,
		context = "dye",
		str_name = "Copper Paint",
		str_desc = "A small bucket of Copper Paint.",
		acquisition = acquisition_smelting,
		durability = 3
	),
	EwGeneralItem(
		id_item = item_id_paint_chrome,
		context = "dye",
		str_name = "Chrome Paint",
		str_desc = "A small bucket of Chrome Paint.",
		acquisition = acquisition_smelting,
		durability = 3
	),
	EwGeneralItem(
		id_item = item_id_paint_gold,
		context = "dye",
		str_name = "Gold Paint",
		str_desc = "A small bucket of Gold Paint.",
		acquisition = acquisition_smelting,
		durability = 3
	),
	EwGeneralItem(
		id_item = "bone",
		str_name = "Bone",
		str_desc = "A small nondescript bone. Traces of fresh slime in it indicate it must've belonged to one of the city's residents.",
		context = 'player_bone',
	),
	EwGeneralItem(
		id_item = item_id_negapoudrin,
		str_name = "negapoudrin",
		str_desc = "A dense, crystalized slab of unholy negaslime.",
	),
	EwGeneralItem(
		id_item = item_id_tradingcardpack,
		alias = [
			"tcp", # DUDE LOL JUST LIKE THE PROCRASTINATORS HOLY FUCKING SHIT I'M PISSING MYSELF RN
			"tradingcard",
			"trading",
			"card",
			"cardpack",
			"pack"
		],
		str_name = "Trading Cards",
		str_desc = "A pack of trading cards",
		price = 50000,
		vendors = [vendor_bazaar, vendor_glocksburycomics],
	),
	EwGeneralItem(
		id_item = "rightleg",
		context = 'slimexodia',
		str_name = "The Right Leg of The Forbidden {}".format(emote_111),
		str_desc = "One of the extremely rare, legendary Forbidden {} cards. Gazing upon the card and its accompanying "
				   "intense holographic sheen without the proper eyewear can have disastrous consequences. Yet, you do it anyway. "
				   "It’s just too beautiful not to.".format(emote_111),
	),
	EwGeneralItem(
		id_item = "leftleg",
		context = 'slimexodia',
		str_name = "Left Leg of The Forbidden {}".format(emote_111),
		str_desc = "One of the extremely rare, legendary Forbidden {} cards. Gazing upon the card and its accompanying "
				   "intense holographic sheen without the proper eyewear can have disastrous consequences. Yet, you do it anyway. "
				   "It’s just too beautiful not to.".format(emote_111),
	),
	EwGeneralItem(
		id_item = "slimexodia",
		context = 'slimexodia',
		str_name = "Slimexodia The Forbidden {}".format(emote_111),
		str_desc = "The centerpiece of the extremely rare, legendary Forbidden {} cards. Gazing upon the card and its accompanying "
				   "intense holographic sheen without the proper eyewear can have disastrous consequences. Yet, you do it anyway. "
				   "It’s just too beautiful not to.".format(emote_111),
	),
	EwGeneralItem(
		id_item = "rightarm",
		context = 'slimexodia',
		str_name = "Right Arm of The Forbidden {}".format(emote_111),
		str_desc = "One of the extremely rare, legendary Forbidden {} cards. Gazing upon the card and its accompanying "
				   "intense holographic sheen without the proper eyewear can have disastrous consequences. Yet, you do it anyway. "
				   "It’s just too beautiful not to.".format(emote_111),
	),
	EwGeneralItem(
		id_item = "leftarm",
		context = 'slimexodia',
		str_name = "Left Arm of The Forbidden {}".format(emote_111),
		str_desc = "One of the extremely rare, legendary Forbidden {} cards. Gazing upon the card and its accompanying "
				   "intense holographic sheen without the proper eyewear can have disastrous consequences. Yet, you do it anyway. "
				   "It’s just too beautiful not to.".format(emote_111),
	),
	EwGeneralItem(
		id_item = item_id_forbidden111,
		str_name = "The Forbidden {}".format(emote_111),
		str_desc = theforbiddenoneoneone_desc.format(emote_111 = emote_111),
		acquisition = acquisition_smelting
	),
	EwGeneralItem(
		id_item = item_id_stick,
		str_name = "stick",
		str_desc = "It’s just some useless, dumb stick.",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_faggot,
		str_name = "faggot",
		str_desc = "Wow, incredible! We’ve evolved from one dumb stick to several, all tied together for the sake of a retarded puesdo-pun! Truly, ENDLESS WAR has reached its peak. It’s all downhill from here, folks.",
		acquisition = acquisition_smelting
	),
	EwGeneralItem(
		id_item = item_id_doublefaggot,
		str_name = "double faggot",
		str_desc = "It's just a bundle of sticks, twice as long and hard as the two combined to form it. Hey, what are you chucklin' at?.",
		acquisition = acquisition_smelting
	),
	EwGeneralItem(
		id_item = item_id_seaweed,
		str_name = "Seaweed",
		str_desc = "OH GOD IT'S A FUCKING SEAWEED!",
		acquisition = acquisition_bartering,
		ingredients = "generic",
		context = 10,
	),
	EwGeneralItem(
		id_item = item_id_oldboot,
		str_name = "Old Boot",
		str_desc = "OH GOD IT'S A FUCKING OLD BOOT!",
		acquisition = acquisition_bartering,
		ingredients = "generic",
		context = 10,
	),
	EwGeneralItem(
		id_item = item_id_tincan,
		str_name = "Tin Can",
		str_desc = "OH GOD IT'S A FUCKING TIN CAN!",
		acquisition = acquisition_bartering,
		ingredients = "generic",
		context = 10,
	),
	EwGeneralItem(
		id_item = item_id_leather,
		str_name = "Leather",
		str_desc = "A strip of leather.",
		acquisition = acquisition_smelting,
		ingredients = "generic",
		context = 10,
	),
	EwGeneralItem(
		id_item = item_id_ironingot,
		str_name = "Iron Ingot",
		str_desc = "A bar of iron",
		acquisition = acquisition_smelting,
		ingredients = "generic",
		context = 10,
	),
	EwGeneralItem(
		id_item = item_id_dragonsoul,
		str_name = "Dragon Soul",
		str_desc = "A fearsome dragon soul, pried from the corpse of a Green Eyes Slime Dragon. It's just like Dark Souls! Wait... *just like* Dark Souls??? Maybe you can use this for something.",
		context = 'dragon soul',
	),
	EwGeneralItem(
		id_item = item_id_monsterbones,
		str_name = "Monster Bones",
		str_desc = "A large set of bones, taken from the monsters that roam the outskirts. Tastes meaty.",
		context = 'monster bone',
	),
	EwGeneralItem(
		id_item = item_id_bloodstone,
		str_name = "blood stone",
		str_desc = "Formed from the cracking of monster bones, it glistens in your palm with the screams of those whos bones comprise it. Perhaps it will be of use one day.",
		context = 'blood stone',
		acquisition = acquisition_smelting
	),
	EwGeneralItem(
		id_item = item_id_tanningknife,
		context = "tool",
		str_name = "Tanning Knife",
		str_desc = "A tanning knife",
		acquisition = acquisition_smelting,
	),
	EwGeneralItem(
		id_item = item_id_string,
		str_name = "string",
		str_desc = "It’s just some string.",
		acquisition = acquisition_bartering,
		ingredients = "generic",
		context = 60,
	),
	EwGeneralItem(
		id_item = item_id_gameguide,
		alias = [
			"gg",
			"gameguide",
			"gamergate",
		],
		str_name = "The official unofficial ENDLESS WAR Game Guide, Version III",
		str_desc = "A guide on all the game mechanics found in ENDLESS WAR, accurate as of 7/19/2020. Use the !help command to crack it open.",
		vendors = [vendor_college],
		price = 10000,
	),
	EwGeneralItem(
		id_item=item_id_juviegradefuckenergybodyspray,
		context='repel',
		alias=[
			"regular body spray",
			"regbs",
			"regular repel",
			"juvie",
			"juviegrade",
			"juvie grade",
			"repel",
			"body spray",
			"bodyspray",
			"bs",
		],
		str_name="Juvie Grade FUCK ENERGY Body Spray",
		str_desc="A canister of perfume. Somehow doubles as a slime beast repellant. The label on the back says it lasts for three hours.",
		vendors=[vendor_glocksburycomics],
		price=10000,
	),
	EwGeneralItem(
		id_item = item_id_superduperfuckenergybodyspray,
		context = 'superrepel',
		alias = [
			"superrepel",
			"super repel",
			"super duper body spray",
			"superbodyspray",
			"superduperbodyspray",
			"sdbs",
			"super",
		],
		str_name = "Super Duper FUCK ENERGY Body Spray",
		str_desc = "A canister of perfume. Somehow doubles as a slime beast repellant. The label on the back says it lasts for six hours.",
		vendors = [vendor_glocksburycomics],
		price = 20000,
	),
	EwGeneralItem(
		id_item = item_id_gmaxfuckenergybodyspray,
		context = 'maxrepel',
		alias = [
			"maxrepel",
			"max repel",
			"g-max body spray",
			"gmaxbodyspray",
			"gmbs",
			"gmax",
			"g-max",
		],
		str_name = "G-Max FUCK ENERGY Body Spray",
		str_desc = "A canister of perfume. Somehow doubles as a slime beast repellant. The label on the back says it lasts for twelve hours.",
		vendors = [vendor_glocksburycomics],
		price = 40000,
	),
	EwGeneralItem(
		id_item = item_id_costumekit,
		context = 'costumekit',
		alias = [
			"costumekit",
			"ck",
			"kit",
			"costume",
		],
		vendors = [vendor_rpcity],
		str_name = "Double Halloween Costume Kit",
		str_desc = "A package of all the necessary tools and fabrics needed to make the Double Halloween costume of your dreams.",
		price = 50000,
	),
	EwGeneralItem(
		id_item = item_id_doublehalloweengrist,
		context = 'dhgrist',
		alias = [
			"grist"
		],
		str_name = "Double Halloween Grist",
		str_desc = "A mush of finely ground candy. Perhaps it can be forged into something special?",
	),
	EwGeneralItem(
		id_item = item_id_whitelineticket,
		context = 'wlticket',
		alias = [
			"tickettohell"
		],
		str_name = "Ticket to the White Line",
		str_desc = "A large assortment of candy molded into one unholy voucher for access into the underworld. Use it in a White Line subway station... ***IF YOU DARE!!***",
		acquisition=acquisition_smelting,
	),
	EwGeneralItem(
		id_item=item_id_megaslimewrappingpaper,
		context=context_wrappingpaper,
		alias=[
			"mswp"
		],
		str_name="Megaslime Wrapping Paper",
		str_desc="Wrapping paper with Megaslimes plastered all over it. Blaargh!",
		price = 1000,
	),
	EwGeneralItem(
		id_item=item_id_greeneyesslimedragonwrappingpaper,
		context=context_wrappingpaper,
		alias=[
			"gesdwp"
		],
		str_name="Green Eyes Slime Dragon Wrapping Paper",
		str_desc="Wrapping paper with many images of the Green Eyes Slime Dragon printed on it. Powerful...",
		price = 1000,
	),
	EwGeneralItem(
		id_item = item_id_phoebuswrappingpaper,
		context = context_wrappingpaper,
		alias = [
			"pwp"
		],
		str_name = "Phoebus Wrapping Paper",
		str_desc = "A set of wrapping paper with Slime Invictus on it. Yo, Slimernalia!",
		price = 1000,
	),
	EwGeneralItem(
		id_item = item_id_slimeheartswrappingpaper,
		context = context_wrappingpaper,
		alias = [
			"shwp"
		],
		str_name = "Slime Hearts Wrapping Paper",
		str_desc = "Wrapping paper decorated with slime hearts. Cute!!",
		price = 1000,
	),
	EwGeneralItem(
		id_item = item_id_slimeskullswrappingpaper,
		context = context_wrappingpaper,
		alias = [
			"sswp"
		],
		str_name = "Slime Skulls Wrapping Paper",
		str_desc = "A roll of wrapping paper with Slime Skulls stamped all over it. Spooky...",
		price = 1000,
	),
	EwGeneralItem(
		id_item = item_id_shermanwrappingpaper,
		context = context_wrappingpaper,
		alias = [
			"swp"
		],
		str_name = "Sherman Wrapping Paper",
		str_desc = "Wrapping paper with Sherman, the SlimeCorp salaryman etched into it. Jesus Christ, how horrifying!",
		price = 1000,
	),
	EwGeneralItem(
		id_item = item_id_slimecorpwrappingpaper,
		context = context_wrappingpaper,
		alias = [
			"scwp"
		],
		str_name = "SlimeCorp Wrapping Paper",
		str_desc = "A set of wrapping paper with that accursed logo printed all over it. What sort of corporate bootlicker would wrap a gift in this?",
		price = 1000,
	),
	EwGeneralItem(
		id_item = item_id_pickaxewrappingpaper,
		context = context_wrappingpaper,
		alias = [
			"pawp"
		],
		str_name = "Pickaxe Wrapping Paper",
		str_desc = "A roll of wrapping paper with a bunch of pickaxes depicted on it. Perfect for Juvies who love to toil away in the mines.",
		price = 1000,
	),
	EwGeneralItem(
		id_item = item_id_benwrappingpaper,
		context = context_wrappingpaper,
		alias = [
			"bwp"
		],
		str_name = "Ben Wrapping Paper",
		str_desc = "Wrapping paper with the Cop Killer printed on it. !dab !dab !dab",
		price = 1000,
	),
	EwGeneralItem(
		id_item = item_id_munchywrappingpaper,
		context = context_wrappingpaper,
		alias = [
			"mwp"
		],
		str_name = "Munchy Wrapping Paper",
		str_desc = "Wrapping paper with the Rowdy Fucker printed on it. !THRASH !THRASH !THRASH",
		price = 1000,
	),
	EwGeneralItem(
		id_item = item_id_gellphone,
		context = 'gellphone',
		alias = [
			"gell",
			"phone",
			"cellphone",
			"flipphone",
			"nokia"
		],
		str_name = "Gellphone",
		str_desc = "A cell phone manufactured by SlimeCorp. Turning it on allows you to access various apps and games.",
		vendors = [vendor_bazaar],
		price = 1000000
	),
	EwGeneralItem(
		id_item = item_id_modelovaccine,
		context = item_id_modelovaccine,
		alias = [
			"vaccine",
			"cure",
		],
		str_name = "Modelovirus vaccine",
		str_desc = "It’s a rusty syringe containing a thick, dark-red substance. It begins to bubble slightly when you shake it. A few charred bits rise to the top. Looks yummy!",
		vendors = [vendor_lab],
		price = 1000000
	),
	EwSlimeoidFood(
		id_item = item_id_fragilecandy,
		alias = [
			"fragile",
		],
		str_name = "Fragile Candy",
		str_desc = "Increases Chutzpah and decreases Grit, when fed to a slimeoid.",
		vendors = [vendor_glocksburycomics, vendor_slimypersuits],
		price = 100000,
		increase = slimeoid_stat_chutzpah,
		decrease = slimeoid_stat_grit,
	),
	EwSlimeoidFood(
		id_item = item_id_rigidcandy,
		alias = [
			"rigid",
		],
		str_name = "Rigid Candy",
		str_desc = "Increases Grit and decreases Chutzpah, when fed to a slimeoid.",
		vendors = [vendor_glocksburycomics, vendor_slimypersuits],
		price = 100000,
		increase = slimeoid_stat_grit,
		decrease = slimeoid_stat_chutzpah,
	),
	EwSlimeoidFood(
		id_item = item_id_reservedcandy,
		alias = [
			"reserved",
		],
		str_name = "Reserved Candy",
		str_desc = "Increases Grit and decreases Moxie, when fed to a slimeoid.",
		vendors = [vendor_glocksburycomics, vendor_slimypersuits],
		price = 100000,
		increase = slimeoid_stat_grit,
		decrease = slimeoid_stat_moxie,
	),
	EwSlimeoidFood(
		id_item = item_id_recklesscandy,
		alias = [
			"reckless",
		],
		str_name = "Reckless Candy",
		str_desc = "Increases Moxie and decreases Grit, when fed to a slimeoid.",
		vendors = [vendor_glocksburycomics, vendor_slimypersuits],
		price = 100000,
		increase = slimeoid_stat_moxie,
		decrease = slimeoid_stat_grit,
	),
	EwSlimeoidFood(
		id_item = item_id_insidiouscandy,
		alias = [
			"insidious",
		],
		str_name = "Insidious Candy",
		str_desc = "Increases Chutzpah and decreases Moxie, when fed to a slimeoid.",
		vendors = [vendor_glocksburycomics, vendor_slimypersuits],
		price = 100000,
		increase = slimeoid_stat_chutzpah,
		decrease = slimeoid_stat_moxie,
	),
	EwSlimeoidFood(
		id_item = item_id_bluntcandy,
		alias = [
			"blunt",
		],
		str_name = "Blunt Candy",
		str_desc = "Increases Moxie and decreases Chutzpah, when fed to a slimeoid.",
		vendors = [vendor_glocksburycomics, vendor_slimypersuits],
		price = 100000,
		increase = slimeoid_stat_moxie,
		decrease = slimeoid_stat_chutzpah,
	),
	EwPrankItem(
		id_item=item_id_creampie,
		str_name="Coconut Cream Pie",
		str_desc="A coconut cream pie, perfect for creaming all over someone!" + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="{} throws a cream pie at your face! How embarrassing, yet tasty!",
		rarity=prank_rarity_heinous,
		gambit=15,
	),
	EwPrankItem(
		id_item=item_id_waterballoon,
		str_name="Water Balloon",
		str_desc="A simple, yet effective water balloon. Aim for the groin for maximum effectiveness." + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="{} throws a water balloon at your crotch. Haha, fucking piss your pants much?",
		rarity=prank_rarity_heinous,
		gambit=15,
	),
	EwPrankItem(
		id_item=item_id_bungisbeam,
		str_name="Bungis Beam",
		str_desc="A high-tech futuristic ray gun, with the uncanny ability to turn someone into Sky (Bungis)... or so the legends say." + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="{} shoots you with a Bungis Beam! Slowly but surely, you transmogrify into Sky (Bungis)!!",
		rarity=prank_rarity_scandalous,
		gambit=10,
		side_effect="bungisbeam_effect",
	),
	EwPrankItem(
		id_item=item_id_circumcisionray,
		str_name="Circumcision Ray",
		str_desc="A powerful surgical tool in the form of a handgun. You're not really sure how it works, but testing it out on yourself seems unwise." + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="{} fires off a Circumcision Ray at your genitals! Oh god, **IT BURNS!!** What the fuck is wrong with them?",
		rarity=prank_rarity_scandalous,
		gambit=25,
	),
	EwPrankItem(
		id_item=item_id_cumjar,
		str_name="Cum Jar",
		str_desc="A jar full of seminal fluid. You think you can spot what looks like a My Little Pony figurine on the inside." + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="{} chucks a Cum Jar in your general direction! The sticky white stuff gets everywhere!!",
		rarity=prank_rarity_scandalous,
		gambit=30,
		side_effect="cumjar_effect",
	),
	EwPrankItem(
		id_item=item_id_discounttransbeam,
		str_name="Discount Trans Beam",
		str_desc="A shitty knock-off of the real thing. Gotta work with the hand you're dealt, I guess." + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="{} emits a Discount Trans Beam! You are imbued with a mild sense of gender dysphoria.",
		rarity=prank_rarity_heinous,
		gambit=20,
	),
	EwPrankItem(
		id_item=item_id_transbeamreplica,
		str_name="Legally Distinct Trans Beam Replica",
		str_desc="A scientifically perfected replica of the famous Trans Beam. Could SlimeCorp be responsible?\n\n**THIS IS A LEGALLY DISTINCT VERSION OF THE TRANS BEAM. IT IS IN NO WAY AN ACT OF PLAGIARISM AGAINST PARADOX CROCS OR THE PARADOX CROCS FAN CLUB TREEHOUSE LLC**" + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="***PSHOOOOOOOO!!!*** {} calls upon the all powerful **Trans Beam!** Your gender dysphoria levels are off the fucking charts!! You, dare I say it, might just be Transgendered now.",
		rarity=prank_rarity_forbidden,
		gambit=50,
	),
	EwPrankItem(
		id_item=item_id_bloodtransfusion,
		str_name="Blood Transfusion",
		str_desc="A packet of unknown blood hooked up to a syringe. They'll never see it coming." + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="{} stabs you with a syringe and performs a Blood Transfusion! Who knows what kind of fucked up diseases they just gave you?!",
		rarity=prank_rarity_scandalous,
		gambit=30,
	),
	EwPrankItem(
		id_item=item_id_transformationmask,
		str_name="Transformation Mask",
		str_desc="A mask used to transform into other people, somewhat visually reminiscent of the one used in The Mask (1994), starring Jim Carrey." + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="***SSSSMMMMMMOOOOKKIIIN!!*** {} puts on their Transformation Mask and copies your likeness! While in disguise, they do all sorts of crazy, messed up shit and ruin your reputation completely!!",
		rarity=prank_rarity_forbidden,
		gambit=45,
	),
	EwPrankItem(
		id_item=item_id_emptychewinggumpacket,
		str_name="Empty Chewing Packet",
		str_desc="A packet of chewing gum, which, upon closer inspection, is completely empty. It's fool-proof, really." + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="{} offers you a piece of Chewing Gum in these desperate times. HA, sike! The packet is completely empty, you fucking IDIOT!",
		rarity=prank_rarity_heinous,
		gambit=10,
	),
	EwPrankItem(
		id_item=item_id_airhorn,
		str_name="Air Horn",
		str_desc="A device capable of deafening those who get too close to it." + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="{} blasts an Air Horn and ruptures your eardrums! What an asshole!",
		rarity=prank_rarity_heinous,
		gambit=20,
	),
	EwPrankItem(
		id_item=item_id_banggun,
		str_name="BANG! Gun",
		str_desc="A firearm that shoots out a tiny little flag. Also capable of shooting real bullets." + prank_type_text_instantuse,
		prank_type=prank_type_instantuse,
		prank_desc="{} points a gun at your! Oh, haha, it just shoots out a little flag with the word 'BANG!' on it, how cu-\n\n**The gun then ejects the flag and fires a bullet right into your foot.**",
		rarity=prank_rarity_heinous,
		gambit=20,
	),
	EwPrankItem(
		id_item=item_id_pranknote,
		str_name="Prank Note",
		str_desc="A mysterious notebook. It's said that if you write someone's name down in it, they get pranked hardcore.",
		prank_type=prank_type_instantuse,
		prank_desc="{} writes your name down in the Prank Note! You are almost instantly assaulted by a barrage of cream pies, water baloons, and air horns! Holy fucking shit!!",
		rarity=prank_rarity_forbidden,
		gambit=45,
	),
	EwPrankItem(
		id_item=item_id_bodynotifier,
		str_name="Body Notifier",
		str_desc="An item that notifies someone of their basic bodily functions.",
		prank_type=prank_type_instantuse,
		prank_desc="{} notifies you of your basic bodily functions.",
		rarity=prank_rarity_heinous,
		gambit=15,
		side_effect="bodynotifier_effect"
	),
	EwPrankItem(
		id_item=item_id_chinesefingertrap,
		str_name="Chinese Finger Trap",
		str_desc="An item of oriental origin. Wrap it around someone's finger to totally prank them!" + prank_type_text_response,
		prank_type=prank_type_response,
		prank_desc="Oh no! {} has ensnared you in a Chinese finger trap! Type **!loosenfinger** to escape!",
		response_desc_1="You try to separate your fingers but they are truly trapped. Type **!loosenfinger** to untrap yourself.",
		response_desc_2="The paper finger trap holds strong. Type **!loosenfinger** to break free.",
		response_desc_3="You pull your fingers apart with all your might, but the finger trap only grips tighter. Typing **!loosenfinger** might loosen your finger and help you escape.",
		response_desc_4="You surrender, resigning your fingers to be connected forever. You think about all the things you can still do with conjoined index fingers. You try to jack it but it doesn't quite work.",
		response_command="loosenfinger",
		rarity=prank_rarity_heinous,
		gambit=2,
	),
	EwPrankItem(
		id_item=item_id_japanesefingertrap,
		str_name="Japanese Finger Trap",
		str_desc="By all means it's an upgrade compared to the Chinese one. This one has barbs on the inside. Youch!" + prank_type_text_response,
		prank_type=prank_type_response,
		prank_desc="気を付けて！ {}さんがあなたを日本の指トラップに捕らえました！ **!wigglefinger**タイプをする！",
		response_desc_1="指が閉じ込められます。閉じ込められるように、**!wigglefinger**と入力します。",
		response_desc_2="ペーパーフィンガートラップは強力です。 **!wigglefinger**と入力して自由にします。",
		response_desc_3="機械翻訳施設に閉じ込められているのを助けてください **!wigglefinger**。",
		response_desc_4="あなたは日本人になりました",
		response_command="wigglefinger",
		rarity=prank_rarity_scandalous,
		gambit=4,
	),
	EwPrankItem(
		id_item=item_id_sissyhypnodevice,
		str_name="Sissy Hypno Device",
		str_desc="A VR headset with some rather dubious content being broadcast to it. Yeah, you better save this for when the chips are down and you really wanna fuck someone's day up." + prank_type_text_response,
		prank_type=prank_type_response,
		prank_desc="Oh no! When you weren't looking, {} slipped a sissy hypno device onto your head and tightened the straps! Type **!takeoffheadset** to get out of there before your mind becomes corrupted!",
		response_desc_1="The sissy hypno device analyzes your brainwaves and finds you a perfect candidate to become a sissy. Type **!takeoffheadset** to stop the procedure.",
		response_desc_2="Your grey matter is probed by the tendrils of the sissy hypno device. You are about to sustain permanant sissyfication. Type **!takeoffheadset** now.",
		response_desc_3="You feel the sudden urge to don striped socks. **!takeoffheadset**.",
		response_desc_4="You have been fully hypnotized and are now 100% a sissy. **!takeoffheadset** will not help you any longer.",
		response_command="takeoffheadset",
		rarity=prank_rarity_forbidden,
		gambit=6,
	),
	EwPrankItem(
		id_item=item_id_piedpiperkazoo,
		str_name="Pied Piper Kazoo",
		str_desc="A musical instrument capable of summoning a swarm of rodents! Let's see what kind of trouble this thing can get you into." + prank_type_text_response,
		prank_type=prank_type_response,
		prank_desc="Oh no! {} has sicced their rats on you. Type **!runfromtherats** to run from the rats.",
		response_desc_1="A rat peeks its head out of a nearby gutter and peers directly at you. You can get a headstart on him by typing **!runfromtherats**.",
		response_desc_2="Three rats crawl out of a trashcan and attempt to block your way. You could probably step over them, if you type **!runfromtherats**.",
		response_desc_3="About 15 or 16 rats encircle you. It looks grim, but you may still have a chance to **!runfromtherats**.",
		response_desc_4="A rat runs up your pant leg and bites your taint. You stumble and fall into what can only be described as a sea of rats.",
		response_command="runfromtherats",
		rarity=prank_rarity_scandalous,
		gambit=4,
	),
	EwPrankItem(
		id_item=item_id_sandpapergloves,
		str_name="Sandpaper Gloves",
		str_desc="Gloves padded with sandpaper on the palms and fingers. Although it's capable of giving some real mean Indian burns, its slapping attacks are nothing to be scoffed at, either." + prank_type_text_response,
		prank_type=prank_type_response,
		prank_desc="Oh no! {} approaches. It looks like they want a hi-five. Type **!dodgetheglove** to dodge their sandpaper glove.",
		response_desc_1="You don't know them that well... they might just be waving at you. Type **!dodgetheglove** to try and avoid an awkward situation.",
		response_desc_2="You raise your hand to wave back, but it seems they're waving at someone behind you. Type **!dodgetheglove** to sprint in the opposite direction as fast as possible.",
		response_desc_3="They stop waving, but are still approaching you with -- what you can now see is a sandpaper glove -- outstretched. Type **!dodgetheglove** to dodge their hand, matrix-style.",
		response_desc_4="{} reaches you, and slaps you across the face with their 80 grit, diamond powder, industry-standard sandpaper glove. It tears your facial dermis straight off.",
		response_command="dodgetheglove",
		rarity=prank_rarity_heinous,
		gambit=3,
	),
	EwPrankItem(
		id_item=item_id_ticklefeather,
		str_name="Tickle Feather",
		str_desc="A feather? For like, tickling people or some shit? Honestly, these pranks are starting to get a bit weird." + prank_type_text_response,
		prank_type=prank_type_response,
		prank_desc="Oh no! Imminent tickling from {} approaching. Type **!dontlaugh** to not laugh.",
		response_desc_1="aaahahaaha it tickles **!dontlaugh**",
		response_desc_2="hehehehheh STOP **!dontlaugh**",
		response_desc_3="AAAAAHHAHAHAHHAHHAAH **!dontlaugh** HHEJHJHHAHAHAHA!",
		response_desc_4="OOOOOO OOOOO OOOO OOOOO OO OO O O O O OOO!",
		response_command="dontlaugh",
		rarity=prank_rarity_heinous,
		gambit=2,
	),
	EwPrankItem(
		id_item=item_id_genitalmutilationinstrument,
		str_name="Genital Mutilation Instrument",
		str_desc="A horrid, nightmarish mechanism which should have been hidden away off ages ago, but has somehow returned. Legends say the Double Headless Double Horseman had one in his possession." + prank_type_text_response,
		prank_type=prank_type_response,
		prank_desc="{} has your genitals in an iron grip! Type **!resisttorture** to minimize the extreme pain!",
		response_desc_1="{} has your genitals in an iron grip! Type **!resisttorture** to minimize the extreme pain!",
		response_desc_2="{} has your genitals in an iron grip! Type **!resisttorture** to minimize the extreme pain!",
		response_desc_3="{} has your genitals in an iron grip! Type **!resisttorture** to minimize the extreme pain!",
		response_desc_4="{} has your genitals in an iron grip! Type **!resisttorture** to minimize the extreme pain!",
		response_command="resisttorture",
		rarity=prank_rarity_forbidden,
		gambit=7,
	),
	EwPrankItem(
		id_item=item_id_gamerficationasmr,
		str_name="Gamerfication ASMR",
		str_desc="An incredibly long recording of some depraved hypnotization method. You wouldn't wish this kind of thing on your worst enemy." + prank_type_text_response,
		prank_type=prank_type_response,
		prank_desc="Oh no! {} approaches you with a 10-hour YouTube video of Gamerification ASMR. Type **!closeyourears** to try not to listen.",
		response_desc_1="woooOOOooo yooouuu are becooooming a gaaaamer. yoou playy temple ruuuun on the toiiiilet. **!closeyourears** to turn off the video.",
		response_desc_2="ooooooo yoooou seeeee a csgo major at a bar and kiiiinda enjoooy iiiit. **!closeyourears** to stop the damage any further.",
		response_desc_3="oooohhhhhh youuuuu plaaaaayyy dota 2 and flaaaame your teammates !votekick **!closeyourears**.",
		response_desc_4="yooouu suudeenly waant too speeend eeight houurs debuuugiiinng skyriiim moooodsss oooOOOoooo.",
		response_command="closeyourears",
		rarity=prank_rarity_scandalous,
		gambit=5,
	),
	EwPrankItem(
		id_item=item_id_beansinacan,
		str_name="Beans In A Can",
		str_desc="A tin of beans. Warning: Place In A Microwave-Safe Container Before Heating." + prank_type_text_response,
		prank_type=prank_type_response,
		prank_desc="Oh no! {} approches you with a can of Bush's Baked Beans in one hand, and a spoon in the other. They are making train noises. Type **!duckthebeans** to dodge the choo-choo.",
		response_desc_1="You ate the entire can of baked beans, but {} pulls out another can. This time it's Pinto Beans in Liquid. **!duckthebeans** so you don't have to eat slimy beans.",
		response_desc_2="You polish off another can of beans. {} pulls out an entire 8-layer Bean Dip and a bag of Tostito's. Honestly it looks pretty good, but you are full. Type **!duckthebeans** because you can't bear to eat anything more.",
		response_desc_3="Now {} pulls out a baggie of Jelly Beans. You think it could be a nice desert. Maybe you don't want to **!duckthebeans** this time.",
		response_desc_4="You finish off the Jelly Beans, but {} pulls out a handful of toe beans. It looks like they just poached them off a pack of furries. They still have hair on them. Absolutely disgusting.",
		response_command="duckthebeans",
		rarity=prank_rarity_scandalous,
		gambit=4,
	),
	EwPrankItem(
		id_item=item_id_brandingiron,
		str_name="Branding Iron",
		str_desc="A big, red hot iron used for branding cattle. Is this how we're doing !vouches nowawadays?" + prank_type_text_response,
		prank_type=prank_type_response,
		prank_desc="Oh no! {} lunges towards you with a white-hot branding iron. Type **!deflectthebrand** to attempt to knock it away.",
		response_desc_1="{} jabs you with the white-hot brand. It's only one letter, any tattoo artist could work it into another word. They still looks angry, and the brand is still yellow hot, so you should probably try to **!deflectthebrand**.",
		response_desc_2="{} drives the brand into you a few more times. It looks like they are trying to spell their name. Type **!deflectthebrand** before they can remember the last few letters.",
		response_desc_3="At this point it looks like {} is using you like a loose-leaf paper. They are taking Social Studies notes using an orange-hot metal rod on your flesh. Type **!deflectthebrand** before they can get to your face.",
		response_desc_4="You are fully covered in brands. You look like a human crossword puzzle, children run by and sharpie circles on you. You look down at your abdomen and notice a few choice epithets.",
		response_command="deflectthebrand",
		rarity=prank_rarity_scandalous,
		gambit=3,
	),
	EwPrankItem(
		id_item=item_id_lasso,
		str_name="Lasso",
		str_desc="A rope with a hoop tied at the end. You're reminded of Quickdraw Saloon, if only because of the blatantly out-of-place cowboy theming this item represents." + prank_type_text_response,
		prank_type=prank_type_response,
		prank_desc="Aw shucks! {} is wavin' their lasso high in the air! Type **!escapethelasso** to git on out of their, partner!",
		response_desc_1="YEEHAW! {} lassos you up once! Type **!escapethelasso** and maybe you can walk away with your bounty intact!",
		response_desc_2="YEEEEHAAW!! {} lassos you up twice! Type **!escapethelasso** to buck away that twine!",
		response_desc_3="YEEEEEEHAAAW!!! {} lassos you up thrice! Holy hell, you're a goddamn rope mummy at this point, partner! Type **!escapethelasso** and maybe you can still *rope* your way out of this one!",
		response_desc_4="YYYYYYYYEEEEEEEEHHHHHHHAAAAAAWWWWWWW!!!!! {} has made a lasso cocoon out of you! There's no way out!!",
		response_command="escapethelasso",
		rarity=prank_rarity_heinous,
		gambit=2,
	),
	EwPrankItem(
		id_item=item_id_fakecandy,
		str_name="Fake Candy",
		str_desc="A bag of fake candy, disguised as candy from last year's Double Halloween",
		prank_type=prank_type_response,
		prank_desc="You see a bag of candy lying on the ground. Neaby, you can see {} cackling to themselves like a madman. Maybe it's best to **!ignorethecandy**.",
		response_desc_1="You scoop up the bag and ingest its contents instead. Yuck! These taste awful! Another bag of candy dropped close by catches your attention. **!ignorethecandy**.",
		response_desc_2="You eat the next bag of candy, which tastes even worse than the previous! Seriously, maybe you should stop being retarded and **!ignorethecandy**.",
		response_desc_3="You eat the third bag of candy in a row. Oh jesus fucking christ, you just cant help yourself at this point, and gobble up the awful confectionary without a second thought. Maybe it's time to **!ignorethecandy**.",
		response_desc_4="You eat the last and final bag of candy. They taste like literal dogshit. What the fuck were you thinking?",
		response_command="ignorethecandy",
		rarity=prank_rarity_heinous,
		gambit=2,
	),
	EwPrankItem(
		id_item=item_id_crabarmy,
		str_name="Crab Army",
		str_desc="An army of crabs, ready to be snip and snap at will.",
		prank_type=prank_type_response,
		prank_desc="{} calls forth their Crab Army, and directs it towards you! Oh man, you better type **!jumpovercrabs** before it's too late!",
		response_desc_1="A lonesome crab snips and snaps at your leg! Ow, the pain is just brutal! Others are skittering closely behind, type **!jumpovercrabs**.",
		response_desc_2="A few more crabs come and attack your sides! Oh god! You gotta get these things off of you and **!jumpovercrabs** fast to make sure no more can latch on!!",
		response_desc_3="Five or six more crabs grab on with their snippers and squeeze tightly against your arms and face. Despite everything, it's still you. With determination in hand, maybe you can **!jumpovercrabs** and escape them before they clutch victory in their crustacean appendages.",
		response_desc_4="It's too late to **!jumpovercrabs** now. In light of their overwhelming victory against you, they hold a celebratory rave. The music they play, you will not soon forget.",
		response_command="jumpovercrabs",
		rarity=prank_rarity_scandalous,
		gambit=4
	),
	EwPrankItem(
		id_item=item_id_whoopiecushion,
		str_name="Whoopie Cushion",
		str_desc="A classic tool of the pranking trade. You'd be surprised if anyone actually fell for it these days, though." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="You step on a Whoopie Cushion by mistake, emitting a noise most foul. Strangers and passersby look at you like you just shit your fucking pants.",
		trap_chance=35,
		rarity=prank_rarity_heinous,
		gambit=15,
	),
	EwPrankItem(
		id_item=item_id_beartrap,
		str_name="Bear Trap",
		str_desc="A hunk of metal jaws, with a trigger plate in the middle. Stepping on it would be a bad idea." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="Oh fuck! You just stepped inside a bear trap! After several minutes of bleeding profusely, you manage to pry it open and lift out your numbed, chomped up ankle!",
		trap_chance=30,
		rarity=prank_rarity_heinous,
		gambit=20,
	),
	EwPrankItem(
		id_item=item_id_bananapeel,
		str_name="Banana Peel",
		str_desc="A rotten leftover banana peel. God, can't people fucking clean up after themselves anymore?" + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="You slip and slide on a Banana Peel and land right on your tailbone! Oof, ouch, your bones!!",
		trap_chance=35,
		rarity=prank_rarity_heinous,
		gambit=15,
	),
	EwPrankItem(
		id_item=item_id_windupbox,
		str_name="Wind-up Box",
		str_desc="One of those old-timey toys that somehow manages to scare the living daylights out of you. It has a jester on the inside, who by all means takes great joy in your fear, and the fear of others." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="What's this? You find a box with a crank on the side... hey! When you crank it, it starts to play music! This is pretty co- AH JESUS FUCK!!",
		trap_chance=35,
		rarity=prank_rarity_scandalous,
		gambit=25,
	),
	EwPrankItem(
		id_item=item_id_windupchatterteeth,
		str_name="Wind-up Chatter Teeth",
		str_desc="A set of plastic teeth that chomp away the more you wind up the little dial on the side. It chugs along on a pair of feet while the gears inside tick away." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="OUCH!! What the fuck? A pair of Wind-up Chatter Teeth are nipping at your heels! Shoo, you fucking wannabe memorabilia!",
		trap_chance=40,
		rarity=prank_rarity_heinous,
		gambit=15,
	),
	EwPrankItem(
		id_item=item_id_snakeinacan,
		str_name="Snake In A Can",
		str_desc="An undeniable classic. Pop it open, and watch the color drain from some poor dim-wit's face as the vinyl-coated viper reaches for the skies." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="What the heck... no way! A can of peanuts! You just gotta unscrew the lid, and... ***!!!***\n\nAfter a brief lapse in consciousness, you awake to find yourself lying on the ground next to that shitty Snake In A Can you can't believe you fell for.",
		trap_chance=30,
		rarity=prank_rarity_heinous,
		gambit=20,
	),
	EwPrankItem(
		id_item=item_id_landmine,
		str_name="Land Mine",
		str_desc="A round metal plate, charged with explosives. These are normally only reserved for tanks, but during Swilldermuk, civilians have been given clearance to use them at their personal discretion.",
		prank_type=prank_type_trap,
		prank_desc="**HOLY FUCKING SHIT!!** You just stepped on a God damn Land Mine! The blast knocks you on your ass and fractures several bones in the lower half of your body. Haha, fucking pranked, bro!!",
		trap_chance=40,
		rarity=prank_rarity_forbidden,
		gambit=45,
	),
	EwPrankItem(
		id_item=item_id_freeipad,
		str_name="Free Ipad",
		str_desc="A free iPad. On the back, there's a logo sticker for... Cinemassacre? Oh god, you better drop this thing before that cyborg puts you out of your misery." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc='Well what do ya know! A free iPad! You bend over to pick it up...\n\nENDLESS WAR judges you harshly! He shoots out two shots of a non-lethal variant of the Bone-hurting-beam, which is even more embarrassing than if he had just killed you, honestly. He told you to shut up, but you didn\'t listen.\n\n**"OH LOOK, A FREE IPAD."**',
		trap_chance=35,
		rarity=prank_rarity_forbidden,
		gambit=45,
	),
	EwPrankItem(
		id_item=item_id_perfectlynormalfood,
		str_name="Perfectly Normal Food",
		str_desc="A plate of perfectly normal food, which in no way has been tampered with in any capacity" + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="Oh damn! A plate of perfectly normal food? Well, what could be the harm in having a bite, you wonder... **COUGH COUGH COUGH** OH GOD IT'S LACED WITH RAT POISON!",
		trap_chance=30,
		rarity=prank_rarity_scandalous,
		gambit=30,
	),
	EwPrankItem(
		id_item=item_id_pitfall,
		str_name="Pitfall Trap",
		str_desc="A round sphere, with an exclamation mark painted on. You don't really know how it works, but aparrently all you gotta do to set it up is dig a hole in the ground and throw it in." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="Ah fuck! The ground caves underneath you, causing you to fall inside a Pitfall Trap! After a moment or two, you manage to climb back up out of the pit it so deviously hid from sight.",
		trap_chance=40,
		rarity=prank_rarity_heinous,
		gambit=20,
	),
	EwPrankItem(
		id_item=item_id_electrocage,
		str_name="Electro Cage",
		str_desc="A cage with iron bars that are hooked up to some kind of electrical current. Apparently they used to use these things at the Slime Circus, to keep all the beasts this thing housed tempered and in line." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="Oh shit. Before you know it, you're 3 steps too far into an Electro Cage. The door locks behind you, and you're forced to endure an agonizing 1 Million Volt shock, with a decent amount of Amps to back it up. Incidentally, the overstimulation also forces you to vacate your bladder, worsening the embarrassment of the situation.",
		trap_chance=40,
		rarity=prank_rarity_scandalous,
		gambit=30,
	),
	EwPrankItem(
		id_item=item_id_ironmaiden,
		str_name="Iron Maiden",
		str_desc="An ancient instrument of torture, in the form of a human-shaped closet with spears on the inside. Hauling it around is a pain in the fucking ass, so you hope someone at least gets tricked by it when the time comes." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="Like a complete fucking dumbass, you walk into a nearby Iron Maiden, which closes shut behind you. The spikes impale you on every limb and into every orifice, causing the whole thing to get damn near coated in slime on the inside. Try taking your eyes off your phone for once, dummy!",
		trap_chance=25,
		rarity=prank_rarity_forbidden,
		gambit=50,
	),
	EwPrankItem(
		id_item=item_id_signthatmakesyoubensaint,
		str_name="Sign That Makes You Ben Saint When You Read It",
		str_desc="An otherworldy artifact. Has the fantastical effect of transforming someone into Ben Saint, should they trigger its effects by reading what it says." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="Hey, there's a sign over in the distance. You squint to make out what it says... Oh no! Upon closer inspection, it's a Sign That Makes You Ben Saint When You Read It!",
		trap_chance=50,
		rarity=prank_rarity_forbidden,
		gambit=15,
		side_effect = "bensaintsign_effect"
	),
	EwPrankItem(
		id_item=item_id_piebomb,
		str_name="Pie Bomb",
		str_desc="A bomb cleverly disguised as a Defective Coconut Cream Pie." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="Oh sweet! Another Defective Coconut Cream Pie for the taking!\n**BOOM!**\nAw man, someone set up a Pie Bomb and got you good!",
		trap_chance=30,
		rarity=prank_rarity_scandalous,
		gambit=30,
	),
	EwPrankItem(
		id_item=item_id_defectivealarmclock,
		str_name="Defective Alarm Clock",
		str_desc="A factory-rejected Alarm Clock. This thing just won't stop fucking beeping at you!!" + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc="BLAAAP BLAAAP BLAAAP BLAAAP BLAAAP\nBLAAAP BLAAAP BLAAAP BLAAAP BLAAAP\nBLAAAP BLAAAP BLAAAP BLAAAP BLAAAP\nBLAAAP BLAAAP BLAAAP BLAAAP BLAAAP\nBLAAAP BLAAAP BLAAAP BLAAAP BLAAAP\nYou crush the Defective Alarm Clock with your bare hands. Good fucking riddance.",
		trap_chance=40,
		rarity=prank_rarity_scandalous,
		gambit=15,
	),
	EwPrankItem(
		id_item=item_id_freeipad_alt,
		str_name="Free Ipad...?",
		str_desc="A free iPad. On the back, there's a logo sticker for... Cinemassacre? Oh god, you better drop this thing before that android puts you out of your misery." + prank_type_text_trap,
		prank_type=prank_type_trap,
		prank_desc='Well what do ya know! A free iPad! You bend over to pick it up...\n\nENDLESS WAR judges you harshly! He shoots out two shots of a non-lethal variant of the Bone-hurting-beam, which is even more embarrassing than if he had just killed you, honestly. He told you to shut up, but you didn\'t listen.\n\n**"It always... ends like this..."**\n\n**"OH LOOK, A FREE IPAD."**',
		trap_chance=35,
		rarity=prank_rarity_forbidden,
		gambit=45,
	),
	EwPrankItem(
		id_item=item_id_alligatortoy,
		str_name="Alligator Toy",
		str_desc="A toy alligator, where the objective is to brush its teeth without tripping its jaws. The top jaw on this one is mysteriously outfitted with razor blades instead of plastic, however.",
		prank_type=prank_type_trap,
		prank_desc='Oh hey! A toy alligator! You had so much fun with these as a kid! You just gotta press on the teeth in the right combination, and...\nOH JESUS CHRIST, THE RAZOR BLADES HIDDEN INSIDE BURY THEMSELVES INTO YOUR HAND!!',
		trap_chance=35,
		rarity=prank_rarity_heinous,
		gambit=20,
	),
	EwGeneralItem(
		id_item=item_id_swordofseething,
		str_name="SWORD OF SEETHING",
		str_desc="An ancient blade of legend. It's said to contain the foul malevolence of the Oozoth, sealed away long ago. The forces resting inside the sword are practically begging you to !use it, before its power fades away into nothingness, so you might as well get it over with.",
		context="swordofseething",
	),
	EwGeneralItem(
		id_item="brokensword",
		str_name="Broken Sword",
		str_desc="The lower half of a broken sword. A useless trinket now, but perhaps one day it can be turned into something useful.",
		context="brokensword",
	),
	EwGeneralItem(
		id_item = item_id_prankcapsule,
		alias = [
			"prank",
			"capsule",
		],
		str_name = "Prank Capsule",
		str_desc = "A small little plastic capsule, which holds a devious prank item on the inside.",
		price = 20000,
		vendors = [vendor_vendingmachine],
		context = "prankcapsule"
	),
	EwGeneralItem(
		id_item = item_id_cool_material,
		str_name = "Cool Beans",
		str_desc = "A couple of cool beans! Far out, man. Well, they aren’t really beans per se, more like little condensed nuggets of your crop. Whatever they are, they’re undeniably cool.",
	),
	EwGeneralItem(
		id_item = item_id_tough_material,
		str_name = "Tough Nails",
		str_desc = "A handful of rusty nails caked in dried blood that were presumably waiting for you if you had eaten your crops instead of milling them. Damn, what a missed opportunity!",
	),
	EwGeneralItem(
		id_item = item_id_smart_material,
		str_name = "Smart Cookies",
		str_desc = "A farmer’s dozen of smart cookies. Well, they aren’t really cookies per se, more like little bland condensed patties of your crop. Whatever they are, they’re undeniably smart.",
	),
	EwGeneralItem(
		id_item = item_id_beautiful_material,
		str_name = "Beauty Spots",
		str_desc = "A small collection of severed beauty spots, mostly freckles and moles, that were presumably waiting for you if you had eaten your crops instead of milling them. Damn, what a missed opportunity!",
	),
	EwGeneralItem(
		id_item = item_id_cute_material,
		str_name = "Cute Buttons",
		str_desc = "A wardrobe of cute buttons. You know you should probably be concerned that these lil’ guys were hiding in your crops, but honestly you’re overcome with emotion and feel utterly blessed. Lookit ‘em! They’re adorable! D’awww...",
	),
	EwGeneralItem(
		id_item = item_id_dyesolution,
		str_name = "Dye Solution",
		str_desc = "A small vial of salt, water, and vinegar. You can smelt this together with crop materials to make dyes.",
		price = 1000,
		vendors = [vendor_basedhardware]
	),
	EwGeneralItem(
		id_item = item_id_textiles,
		str_name = "Textiles",
		str_desc = "A set of fabrics. You can smelt this together with crop materials to make exclusive cosmetics.",
		price = 1000,
		vendors = [vendor_basedhardware]
	),
	EwGeneralItem(
		id_item = item_id_foodbase,
		str_name = "Food Base",
		str_desc = "A set of powders and chemicals. You can smelt this together with crop materials to make exclusive food items which take longer to expire.",
		price = 1000,
		vendors = [vendor_basedhardware]
	),
	EwGeneralItem(
		id_item = item_id_poketubereyes,
		str_name = "Poketuber Eyes",
		str_desc = "The small stem buds of a Poketuber.",
		acquisition = acquisition_milling,
		ingredients = [item_id_poketubers],
	),
	EwGeneralItem(
		id_item = item_id_pulpgourdpulp,
		str_name = "Pulp Gourd Pulp",
		str_desc = "The pulp of a Pulp Gourd.",
		acquisition = acquisition_milling,
		ingredients = [item_id_pulpgourds],
	),
	EwGeneralItem(
		id_item = item_id_sourpotatoskins,
		str_name = "Sour Potato Skins",
		str_desc = "The skins of a Sour Potato.",
		acquisition = acquisition_milling,
		ingredients = [item_id_sourpotatoes],
	),
	EwGeneralItem(
		id_item = item_id_bloodcabbageleaves,
		str_name = "Blood Cabbage Leaves",
		str_desc = "The soft leaves of a Blood Cabbage.",
		acquisition = acquisition_milling,
		ingredients = [item_id_bloodcabbages],
	),
	EwGeneralItem(
		id_item = item_id_joybeanvines,
		str_name = "Joybean Vines",
		str_desc = "The severed vines on which Joybeans grow.",
		acquisition = acquisition_milling,
		ingredients = [item_id_joybeans],
	),
	EwGeneralItem(
		id_item = item_id_purplekilliflowerflorets,
		str_name = "Killiflower Florets",
		str_desc = "The bush-like appendages of a Killiflower plant.",
		acquisition = acquisition_milling,
		ingredients = [item_id_purplekilliflower],
	),
	EwGeneralItem(
		id_item = item_id_razornutshells,
		str_name = "Razornut Shells",
		str_desc = "The sharp and pointy shells of a Razornut.",
		acquisition = acquisition_milling,
		ingredients = [item_id_razornuts],
	),
	EwGeneralItem(
		id_item = item_id_pawpawflesh,
		str_name = "Pawpaw Flesh",
		str_desc = "The ground flesh of a Pawpaw.",
		acquisition = acquisition_milling,
		ingredients = [item_id_pawpaw],
	),
	EwGeneralItem(
		id_item = item_id_sludgeberrysludge,
		str_name = "Sludgeberry Sludge",
		str_desc = "The thick syrup of a Sludgeberry.",
		acquisition = acquisition_milling,
		ingredients = [item_id_sludgeberries],
	),
	EwGeneralItem(
		id_item = item_id_suganmanutfruit,
		str_name = "Suganmanut Fruit",
		str_desc = "The bright, multi-colored fruit off which Suganmanuts grow.",
		acquisition = acquisition_milling,
		ingredients = [item_id_suganmanuts],
	),
	EwGeneralItem(
		id_item = item_id_pinkrowddishroot,
		str_name = "Pink Rowddish Root",
		str_desc = "The thin, light-colored root of a Pink Rowddish.",
		acquisition = acquisition_milling,
		ingredients = [item_id_pinkrowddishes],
	),
	EwGeneralItem(
		id_item = item_id_dankwheatchaff,
		str_name = "Dankwheat Chaff",
		str_desc = "The scaly, protective casing on Dankwheat plants.",
		acquisition = acquisition_milling,
		ingredients = [item_id_dankwheat],
	),
	EwGeneralItem(
		id_item = item_id_brightshadeberries,
		str_name = "Brightshade Berries",
		str_desc = "The small blue berries that grow on Brightshade plants.",
		acquisition = acquisition_milling,
		ingredients = [item_id_brightshade],
	),
	EwGeneralItem(
		id_item = item_id_blacklimeade,
		str_name = "Black Limeade",
		str_desc = "The sweet and sour juice of a Black Lime.",
		acquisition = acquisition_milling,
		ingredients = [item_id_blacklimes],
	),
	EwGeneralItem(
		id_item = item_id_phosphorpoppypetals,
		str_name = "Phosphorpoppy Petals",
		str_desc = "The yellow-green petals of a Phosphorpoppy.",
		acquisition = acquisition_milling,
		ingredients = [item_id_phosphorpoppies],
	),
	EwGeneralItem(
		id_item = item_id_direapplestems,
		str_name = "Dire Apple Stems",
		str_desc = "The orange stems of a Dire Apple.",
		acquisition = acquisition_milling,
		ingredients = [item_id_direapples],
	),
	EwGeneralItem(
		id_item = item_id_rustealeafblades,
		str_name = "Rustea Leaf Blades",
		str_desc = "The razor-sharp blades attatched to the stems of Rustea Leaves.",
		acquisition = acquisition_milling,
		ingredients = [item_id_rustealeaves],
	),
	EwGeneralItem(
		id_item = item_id_metallicapheads,
		str_name = "Metallicap Heads",
		str_desc = "The bulbous head on the top of a Metallicap.",
		acquisition = acquisition_milling,
		ingredients = [item_id_metallicaps],
	),
	EwGeneralItem(
		id_item = item_id_steelbeanpods,
		str_name = "Steel Bean Pods",
		str_desc = "The long and hard pods that house Steel Beans.",
		acquisition = acquisition_milling,
		ingredients = [item_id_steelbeans],
	),
	EwGeneralItem(
		id_item = item_id_aushuckstalks,
		str_name = "Aushuck Stalks",
		str_desc = "The lengthy stalks of an Aushuck plant.",
		acquisition = acquisition_milling,
		ingredients = [item_id_aushucks],
	),
	EwGeneralItem(
		id_item=item_id_civilianscalp,
		str_name="civilian's scalp",
		str_desc="It's the discarded scalp of an innocent NLACakaNM resident. You always wanted to kill one of these guys."
	),
	EwSeedPacket(
		id_item=item_id_gaiaseedpack_poketubers,
		cooldown=30,
		cost=50,
		str_name="Poketuber Gaiaslimeoid Seed Packet",
		str_desc="A seed packet for a Poketuber Gaiaslimeoid. It costs 50 gaiaslime to !plant one, and has a 30 second cooldown.",
		ingredients=[item_id_poketubereyes],
		enemytype="poketubers"
	),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_pulpgourds,
	# 	cooldown=45,
	# 	cost=100,
	# 	str_name="Pulp Gourds Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Pulp Gourds Gaiaslimeoid. It costs 100 gaiaslime to !plant one, and has a 45 second cooldown.",
	# 	ingredients=[item_id_pulpgourdpulp],
	# 	enemytype="pulpgourds"
	# ),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_sourpotatoes,
	# 	cooldown=10,
	# 	cost=150,
	# 	str_name="Sour Potatoes Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Sour Potatoes Gaiaslimeoid. It costs 150 gaiaslime to !plant one, and has a 10 second cooldown.",
	# 	ingredients=[item_id_sourpotatoskins],
	# 	enemytype="sourpotatoes"
	# ),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_bloodcabbages,
	# 	cooldown=10,
	# 	cost=125,
	# 	str_name="Blood Cabbages Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Blood Cabbages Gaiaslimeoid. It costs 125 gaiaslime to !plant one, and has a 10 second cooldown.",
	# 	ingredients=[item_id_bloodcabbageleaves],
	# 	enemytype="bloodcabbages"
	# ),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_joybeans,
	# 	cooldown=120,
	# 	cost=100,
	# 	str_name="Joybeans Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Joybean Gaiaslimeoid. It costs 100 gaiaslime to !plant one, and has a 120 second cooldown.",
	# 	ingredients=[item_id_joybeanvines],
	# 	enemytype="joybeans"
	# ),
	EwSeedPacket(
		id_item=item_id_gaiaseedpack_purplekilliflower,
		cooldown=10,
		cost=100,
		str_name="Purple Killiflower Gaiaslimeoid Seed Packet",
		str_desc="A seed packet for a Purple Killiflower Gaiaslimeoid. It costs 100 gaiaslime to !plant one, and has a 10 second cooldown.",
		ingredients=[item_id_purplekilliflowerflorets],
		enemytype="purplekilliflower"
	),
	EwSeedPacket(
		id_item=item_id_gaiaseedpack_razornuts,
		cooldown=45,
		cost=50,
		str_name="Razornuts Gaiaslimeoid Seed Packet",
		str_desc="A seed packet for a Razornuts Gaiaslimeoid. It costs 50 gaiaslime to !plant one, and has a 45 second cooldown.",
		ingredients=[item_id_razornutshells],
		enemytype="razornuts"
	),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_pawpaw,
	# 	cooldown=45,
	# 	cost=150,
	# 	str_name="Pawpaw Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Pawpaw Gaiaslimeoid. It costs 150 gaiaslime to !plant one, and has a 45 second cooldown.",
	# 	ingredients=[item_id_pawpawflesh],
	# 	enemytype="pawpaw"
	# ),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_sludgeberries,
	# 	cooldown=15,
	# 	cost=75,
	# 	str_name="Sludgeberries Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Sludgeberries Gaiaslimeoid. It costs 75 gaiaslime to !plant one, and has a 15 second cooldown.",
	# 	ingredients=[item_id_sludgeberrysludge],
	# 	enemytype="sludgeberries"
	# ),
	EwSeedPacket(
		id_item=item_id_gaiaseedpack_suganmanuts,
		cooldown=60,
		cost=125,
		str_name="Suganmanuts Gaiaslimeoid Seed Packet",
		str_desc="A seed packet for a Suganmanuts Gaiaslimeoid. It costs 125 gaiaslime to !plant one, and has a 60 second cooldown.",
		ingredients=[item_id_suganmanutfruit],
		enemytype="suganmanuts"
	),
	EwSeedPacket(
		id_item=item_id_gaiaseedpack_pinkrowddishes,
		cooldown=20,
		cost=150,
		str_name="Pink Rowddishes Gaiaslimeoid Seed Packet",
		str_desc="A seed packet for a Pink Rowddishes Gaiaslimeoid. It costs 150 gaiaslime to !plant one, and has a 20 second cooldown.",
		ingredients=[item_id_pinkrowddishroot],
		enemytype="pinkrowddishes"
	),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_dankwheat,
	# 	cooldown=30,
	# 	cost=200,
	# 	str_name="Dankwheat Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Dankwheat Gaiaslimeoid. It costs 200 gaiaslime to !plant one, and has a 30 second cooldown.",
	# 	ingredients=[item_id_dankwheatchaff],
	# 	enemytype="dankwheat"
	# ),
	EwSeedPacket(
		id_item=item_id_gaiaseedpack_brightshade,
		cooldown=10,
		cost=50,
		str_name="Brightshade Gaiaslimeoid Seed Packet",
		str_desc="A seed packet for a Brightshade Gaiaslimeoid. It costs 50 gaiaslime to !plant one, and has a 10 second cooldown.",
		ingredients=[item_id_brightshadeberries],
		enemytype="brightshade"
	),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_blacklimes,
	# 	cooldown=10,
	# 	cost=75,
	# 	str_name="Black Limes Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Black Limes Gaiaslimeoid. It costs 75 gaiaslime to !plant one, and has a 10 second cooldown.",
	# 	ingredients=[item_id_blacklimeade],
	# 	enemytype="blacklimes"
	# ),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_phosphorpoppies,
	# 	cooldown=10,
	# 	cost=75,
	# 	str_name="Phosphorpoppies Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Phosphorpoppies Gaiaslimeoid. It costs 75 gaiaslime to !plant one, and has a 10 second cooldown.",
	# 	ingredients=[item_id_phosphorpoppypetals],
	# 	enemytype="phosphorpoppies"
	# ),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_direapples,
	# 	cooldown=10,
	# 	cost=225,
	# 	str_name="Dire Apples Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Dire Apples Gaiaslimeoid. It costs 225 gaiaslime to !plant one, and has a 10 second cooldown.",
	# 	ingredients=[item_id_direapplestems],
	# 	enemytype="direapples"
	# ),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_rustealeaves,
	# 	cooldown=10,
	# 	cost=100,
	# 	str_name="Rustea Leaves Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Rustea Leaves Gaiaslimeoid. It costs 100 gaiaslime to !plant one, and has a 10 second cooldown.",
	# 	ingredients=[item_id_rustealeafblades],
	# 	enemytype="rustealeaves"
	# ),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_metallicaps,
	# 	cooldown=30,
	# 	cost=225,
	# 	str_name="Metallicaps Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Metallicaps Gaiaslimeoid. It costs 225 gaiaslime to !plant one, and has a 30 second cooldown.",
	# 	ingredients=[item_id_metallicapheads],
	# 	enemytype="metallicaps"
	# ),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_steelbeans,
	# 	cooldown=90,
	# 	cost=150,
	# 	str_name="Steelbeans Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for a Steelbeans Gaiaslimeoid. It costs 150 gaiaslime to !plant one, and has a 90 second cooldown.",
	# 	ingredients=[item_id_steelbeanpods],
	# 	enemytype="steelbeans"
	# ),
	# EwSeedPacket(
	# 	id_item=item_id_gaiaseedpack_aushucks,
	# 	cooldown=120,
	# 	cost=175,
	# 	str_name="Aushucks Gaiaslimeoid Seed Packet",
	# 	str_desc="A seed packet for an Aushucks Gaiaslimeoid. It costs 175 gaiaslime to !plant one, and has a 120 second cooldown.",
	# 	ingredients=[item_id_aushuckstalks],
	# 	enemytype="auschucks"
	# ),
	EwTombstone(
		id_item=item_id_tombstone_defaultshambler,
		cost=300,
		brainpower=30,
		stock=20,
		str_name="Default Shambler Tombstone",
		str_desc="A tombstone for a Default Shambler. If you use it in a graveyard op, it'll add a cooldown of 30 seconds.",
		enemytype="defaultshambler",
	),
	EwTombstone(
		id_item=item_id_tombstone_bucketshambler,
		cost=500,
		brainpower=45,
		stock=20,
		str_name="Bucket Shambler Tombstone",
		str_desc="A tombstone for a Bucket Shambler. If you use it in a graveyard op, it'll add a cooldown of 45 seconds.",
		enemytype="bucketshambler",
	),
	EwTombstone(
		id_item=item_id_tombstone_juveolanternshambler,
		cost=700,
		brainpower=60,
		stock=20,
		str_name="Juve-O'-Lantern Shambler Tombstone",
		str_desc="A tombstone for a Juve-O'-Lantern Shambler. If you use it in a graveyard op, it'll add a cooldown of 60 seconds.",
		enemytype="juveolanternshambler",
	),
	# EwTombstone(
	# 	id_item=item_id_tombstone_flagshambler,
	# 	cost=200,
	# 	brainpower=60,
	# 	stock=10,
	# 	str_name="Flag Shambler Tombstone",
	# 	str_desc="A tombstone for a Flag Shambler. If you use it in a graveyard op, it'll add a cooldown of 60 seconds.",
	# 	enemytype="flagshambler",
	# ),
	# EwTombstone(
	# 	id_item=item_id_tombstone_shambonidriver,
	# 	cost=300,
	# 	brainpower=90,
	# 	stock=10,
	# 	str_name="Shamboni Driver Tombstone",
	# 	str_desc="A tombstone for a Shamboni. If you use it in a graveyard op, it'll add a cooldown of 90 seconds.",
	# 	enemytype="shambonidriver",
	# ),
	# EwTombstone(
	# 	id_item=item_id_tombstone_mammoshambler,
	# 	cost=500,
	# 	brainpower=90,
	# 	stock=1,
	# 	str_name="Mammoshambler Tombstone",
	# 	str_desc="A tombstone for a Mammoshambler. Acts as an upgrade to the Shamboni Driver tombstone. If you use it in a graveyard op, it'll add a cooldown of 90 seconds.",
	# 	enemytype="mammoshambler",
	# ),
	# EwTombstone(
	# 	id_item=item_id_tombstone_gigashambler,
	# 	cost=500,
	# 	brainpower=180,
	# 	stock=3,
	# 	str_name="Gigashambler Tombstone",
	# 	str_desc="A tombstone for a Gigashambler. If you use it in a graveyard op, it'll add a cooldown of 180 seconds.",
	# 	enemytype="gigashambler",
	# ),
	# EwTombstone(
	# 	id_item=item_id_tombstone_microshambler,
	# 	cost=300,
	# 	brainpower=60,
	# 	stock=1,
	# 	str_name="Microshambler Tombstone",
	# 	str_desc="A tombstone for a Microshambler. Acts as an upgrade to the Gigashambler tombstone. If you use it in a graveyard op, it'll add a cooldown of 60 seconds.",
	# 	enemytype="microshambler",
	# ),
	# EwTombstone(
	# 	id_item=item_id_tombstone_shamblersaurusrex,
	# 	cost=800,
	# 	brainpower=180,
	# 	stock=1,
	# 	str_name="Shamblesaurus Rex Tombstone",
	# 	str_desc="A tombstone for a Shamblesaurus. If you use it in a graveyard op, it'll add a cooldown of 180 seconds.",
	# 	enemytype="shamblesaurusrex",
	# ),
	# EwTombstone(
	# 	id_item=item_id_tombstone_shamblerdactyl,
	# 	cost=200,
	# 	brainpower=90,
	# 	stock=5,
	# 	str_name="Shamblerdactyl Tombstone",
	# 	str_desc="A tombstone for a Shamblerdactyl. If you use it in a graveyard op, it'll add a cooldown of 90 seconds.",
	# 	enemytype="shamblerdactyl",
	# ),
	EwTombstone(
		id_item=item_id_tombstone_dinoshambler,
		cost=150,
		brainpower=60,
		stock=5,
		str_name="Dinoshambler Tombstone",
		str_desc="A tombstone for a Dinoshambler. If you use it in a graveyard op, it'll add a cooldown of 60 seconds.",
		enemytype="dinoshambler",
	),
	# EwTombstone(
	# 	id_item=item_id_tombstone_ufoshambler,
	# 	cost=200,
	# 	brainpower=120,
	# 	stock=5,
	# 	str_name="UFO Shambler Tombstone",
	# 	str_desc="A tombstone for a UFO Shambler. If you use it in a graveyard op, it'll add a cooldown of 120 seconds.",
	# 	enemytype="ufoshambler",
	# ),
	# EwTombstone(
	# 	id_item=item_id_tombstone_brawldenboomer,
	# 	cost=150,
	# 	brainpower=60,
	# 	stock=10,
	# 	str_name="Brawlden Boomer Tombstone",
	# 	str_desc="A tombstone for a Brawlden Boomer. If you use it in a graveyard op, it'll add a cooldown of 60 seconds.",
	# 	enemytype="brawldenboomer",
	# ),
	# EwTombstone(
	# 	id_item=item_id_tombstone_juvieshambler,
	# 	cost=250,
	# 	brainpower=60,
	# 	stock=15,
	# 	str_name="Juvie Shambler Tombstone",
	# 	str_desc="A tombstone for a Juvie Shambler. If you use it in a graveyard op, it'll add a cooldown of 60 seconds.",
	# 	enemytype="juvieshambler",
	# ),
	EwTombstone(
		id_item=item_id_tombstone_shambleballplayer,
		cost=400,
		brainpower=60,
		stock=20,
		str_name="Shambleball Player Tombstone",
		str_desc="A tombstone for a Shambleball Player. If you use it in a graveyard op, it'll add a cooldown of 60 seconds.",
		enemytype="shambleballplayer",
	),
	# EwTombstone(
	# 	id_item=item_id_tombstone_shamblerwarlord,
	# 	cost=400,
	# 	brainpower=180,
	# 	stock=5,
	# 	str_name="Shambler Warlord Tombstone",
	# 	str_desc="A tombstone for a Shambler Warlord. If you use it in a graveyard op, it'll add a cooldown of 180 seconds.",
	# 	enemytype="shamblerwarlord",
	# ),
	# EwTombstone(
	# 	id_item=item_id_tombstone_shamblerraider,
	# 	cost=500,
	# 	brainpower=120,
	# 	stock=1,
	# 	str_name="Shambler Raider Tombstone",
	# 	str_desc="A tombstone for a Shambler Raider. Acts as an upgrade to the Shambler Warlord tombstone. If you use it in a graveyard op, it'll add a cooldown of 120 seconds.",
	# 	enemytype="shamblerraider",
	# ),
]
#item_list += ewdebug.debugitem_set

#debugitem = ewdebug.debugitem

# A map of id_item to EwGeneralItem objects.
item_map = {}

# A list of item names
item_names = []

# list of dyes you're able to saturate your Slimeoid with
dye_list = []
dye_map = {}
# seperate the dyes from the other normal items
for c in item_list:

	if c.context != "dye":
		pass
	else:
		dye_list.append(c)
		dye_map[c.str_name] = c.id_item
		
seedpacket_ingredient_list = []
seedpacket_material_map = {}
seedpacket_enemytype_map = {}
seedpacket_ids = []
for sp in item_list:
	if sp.context == context_seedpacket:
		seedpacket_ingredient_list.append(sp.ingredients[0])
		seedpacket_material_map[sp.ingredients[0]] = sp.id_item
		seedpacket_enemytype_map[sp.id_item] = sp.enemytype
		seedpacket_ids.append(sp.id_item)

tombstone_enemytype_map = {}
tombstone_fullstock_map = {}
tombstone_ids = []
for ts in item_list:
	if ts.context == context_tombstone:
		tombstone_enemytype_map[ts.id_item] = ts.enemytype
		tombstone_fullstock_map[ts.enemytype] = ts.stock
		tombstone_ids.append(ts.id_item)

def get_weapon_type_stats(weapon_type):
	types = {
		"normal": {
			"damage_multiplier": 1.1,
			"cost_multiplier": 1,
			"crit_chance": 0.2,
			"crit_multiplier": 1.8,
			"hit_chance": 0.9,
		},
		"precision": {
			"damage_multiplier": 1.3,
			"cost_multiplier": 1.3,
			"crit_chance": 0,
			"crit_multiplier": 2,
			"hit_chance": 1,
		},
		"small_game": {
			"damage_multiplier": 0.5,
			"cost_multiplier": 0.25,
			"crit_chance": 0.1,
			"crit_multiplier": 2,
			"hit_chance": 0.95,
		},
		"variable_damage": {
			"damage_multiplier": 0.5,
			"variable_damage_multiplier": 2,
			"cost_multiplier": 1,
			"crit_chance": 0.1,
			"crit_multiplier": 1.5,
			"hit_chance": 0.9,
		},
		"heavy": {
			"damage_multiplier": 3,
			"cost_multiplier": 5,
			"crit_chance": 0.1,
			"crit_multiplier": 1.5,
			"hit_chance": 0.8,
		},
		"defensive": {
			"damage_multiplier": 0.75,
			"cost_multiplier": 1.5,
			"crit_chance": 0.1,
			"crit_multiplier": 1.5,
			"hit_chance": 0.85,
		},
		"burst_fire": {
			"damage_multiplier": 0.4,
			"cost_multiplier": 0.8,
			"crit_chance": 0.2,
			"crit_multiplier": 1.5,
			"hit_chance": 0.85,
			"shots": 3
		},
		"minigun": {
			"damage_multiplier": 0.3,
			"cost_multiplier": 5,
			"crit_chance": 0.1,
			"crit_multiplier": 2,
			"hit_chance": 0.5,
			"shots": 10
		},
		"incendiary": {
			"damage_multiplier": 0.75,
			"bystander_damage": 0.5,
			"cost_multiplier": 1.5,
			"crit_chance": 0.1,
			"crit_multiplier": 2,
			"hit_chance": 0.9,
		},
		"explosive": {
			"damage_multiplier": 0.5,
			"bystander_damage": 0.5,
			"cost_multiplier": 1,
			"crit_chance": 0.1,
			"crit_multiplier": 2,
			"hit_chance": 0.9,
		},
		"tool": {
			"damage_multiplier": 0.5,
			"cost_multiplier": 1,
			"crit_chance": 0.2,
			"crit_multiplier": 1.8,
			"hit_chance": 0.9,
		},
	}

	return types[weapon_type]

def get_normal_attack(weapon_type = "normal", cost_multiplier = None):
	weapon_stats = get_weapon_type_stats(weapon_type)
	if cost_multiplier:
		weapon_stats["cost_multiplier"] = cost_multiplier

	def get_hit_damage(ctn):
		hit_damage = 0
		base_damage = ctn.slimes_damage

		player_has_sharptoother = (mutation_id_sharptoother in ctn.user_data.get_mutations())
		hit_roll = min(random.random(), random.random()) if player_has_sharptoother else random.random()
		guarantee_crit = (weapon_type == "precision" and ctn.user_data.sidearm == -1)

		if hit_roll < (weapon_stats["hit_chance"] + ctn.hit_chance_mod):
			effective_multiplier = weapon_stats["damage_multiplier"] 
			if "variable_damage_multiplier" in weapon_stats:
				effective_multiplier += random.random() * weapon_stats["variable_damage_multiplier"]

			hit_damage = base_damage * effective_multiplier
			if guarantee_crit or random.random() < (weapon_stats["crit_chance"] + ctn.crit_mod):
				hit_damage *= weapon_stats["crit_multiplier"]
				if not ("shots" in weapon_stats):
					ctn.crit = True
		
		return hit_damage

	def attack(ctn):
		ctn.slimes_spent = int(ctn.slimes_spent * weapon_stats["cost_multiplier"])
		damage = 0
		if "shots" in weapon_stats:
			ctn.crit = True
			for _ in range(weapon_stats["shots"]):
				hit_damage = get_hit_damage(ctn)
				damage += hit_damage
				if hit_damage == 0:
					ctn.crit = False
		else:
			damage = get_hit_damage(ctn)
			if "bystander_damage" in weapon_stats:
				ctn.bystander_damage = damage * weapon_stats["bystander_damage"]
		
		if damage:
			ctn.slimes_damage = int(damage)
		else:
			ctn.miss = True

	return attack

# weapon effect function for "garrote"
def wef_garrote(ctn = None):
	ctn.slimes_damage *= 15
	#ctn.sap_damage = 0
	#ctn.sap_ignored = ctn.shootee_data.hardened_sap

	user_mutations = ctn.user_data.get_mutations()
	aim = (random.randrange(100) + 1)
	if aim <= int(100 * ctn.hit_chance_mod):
		if mutation_id_sharptoother in user_mutations:
			if random.random() < 0.5:
				ctn.miss = True
		else:
			ctn.miss = True

	elif aim <= (1 - int(100 * ctn.crit_mod)):
		ctn.slimes_damage *= 10
		ctn.crit = True

	if ctn.miss == False:
		#Stop movement
		ewutils.moves_active[ctn.user_data.id_user] = 0
		#Stun player for 5 seconds
		ctn.user_data.applyStatus(id_status=status_stunned_id, value=(int(ctn.time_now) + 5))
		#Start strangling target
		ctn.shootee_data.applyStatus(id_status=status_strangled_id, source=ctn.user_data.id_user)

# weapon effect function for "Eldritch Staff"
def wef_staff(ctn = None):
	market_data = EwMarket(id_server = ctn.user_data.id_server)
	conditions_met = 0
	conditions = {
		lambda _: 3 <= market_data.clock < 4, # witching hour
		lambda _: weather_map.get(market_data.weather) == weather_foggy,
		lambda _: (market_data.day % 31 == 15 and market_data.clock >= 20) or (market_data.day % 31 == 16 and market_data.clock <= 6), # moonless night
		lambda ctn: not ctn.user_data.has_soul,
		lambda ctn: ctn.user_data.get_possession('weapon'),
		lambda ctn: ctn.user_data.poi == poi_id_thevoid,
		lambda ctn: ctn.shootee_data.slime > ctn.user_data.slime,
		lambda ctn: (ctn.user_data.salary_credits <= -50000) or (ctn.shootee_data.salary_credits == 0),
		lambda ctn: (ctn.user_data.poi_death == ctn.user_data.poi) or (ctn.shootee_data.poi_death == ctn.shootee_data.poi),
		lambda ctn: (ctn.user_data.id_killer == ctn.shootee_data.id_user) or (ctn.user_data.id_user == ctn.shootee_data.id_killer),
		lambda ctn: (ctn.shootee_data.life_state == life_state_juvenile) or (ctn.shootee_data.life_state == life_state_enlisted and ctn.shootee_data.faction == ctn.user_data.faction),
	}
	for condition in conditions:
		try:
			if condition(ctn):
				conditions_met += 1
		except:
			pass
	
	ctn.slimes_spent = int(ctn.slimes_spent * 2)
	ctn.slimes_damage = int(ctn.slimes_damage * (0.3 + conditions_met * 0.6))
	if conditions_met >= (random.randrange(15) + 1): # 6.66% per condition met
		ctn.crit = True
		ctn.slimes_damage = int(ctn.slimes_damage * 1.8)


def wef_paintgun(ctn = None):
	ctn.slimes_damage = int(ctn.slimes_damage * .7)
	ctn.slimes_spent = int(ctn.slimes_spent * .75)
	aim = (random.randrange(10) + 1)
	#ctn.sap_ignored = 10
	#ctn.sap_damage = 2

	if aim >= (9 - int(10 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage *= 2

def wef_paintroller(ctn = None):
	ctn.slimes_damage = int(ctn.slimes_damage * 1.75)
	ctn.slimes_spent = int(ctn.slimes_spent * 4)

	aim = (random.randrange(10) + 1)
	user_mutations = ctn.user_data.get_mutations()

	if aim <= (1 + int(10 * ctn.hit_chance_mod)):
		if mutation_id_sharptoother in user_mutations:
			if random.random() < 0.5:
				ctn.miss = True
		else:
			ctn.miss = True

	elif aim >= (10 - int(10 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage *= 2
		#ctn.sap_damage *= 2

def wef_watercolors(ctn = None):
	ctn.slimes_damage = 4000
	aim = (random.randrange(250) + 1)
	user_mutations = ctn.user_data.get_mutations()
	#ctn.sap_damage = 0

	if aim <= (1 + int(250 * ctn.hit_chance_mod)):
		if mutation_id_sharptoother in user_mutations:
			if random.random() < 0.5:
				ctn.miss = True
		else:
			ctn.miss = True

	elif aim == 1000:
		ctn.crit = True
		ctn.slimes_damage *= 1

def wef_fingernails(ctn = None):
	ctn.slimes_damage = int(ctn.slimes_damage * 0.8)
	aim = (random.randrange(10) + 1)
	user_mutations = ctn.user_data.get_mutations()
	#ctn.sap_damage = 2
	ctn.miss = False

	if aim >= (10 - int(10 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage *= 2


vendor_dojo = "Dojo"

weapon_class_ammo = "ammo"
weapon_class_exploding = "exploding"
weapon_class_burning = "burning"
weapon_class_captcha = "captcha"
weapon_class_defensive = "defensive"
weapon_class_paint = "paint"
#juvies can equip these weapons
weapon_class_juvie = "juvie"
weapon_class_farming = "farming"

weapon_type_convert = {
weapon_id_watercolors:wef_watercolors,
weapon_id_spraycan:get_normal_attack(),
weapon_id_paintroller:wef_paintroller,
weapon_id_thinnerbomb:get_normal_attack(weapon_type = 'incendiary'),
weapon_id_paintgun:wef_paintgun,
weapon_id_paintbrush:get_normal_attack(weapon_type = 'small_game'),
weapon_id_roomba:get_normal_attack()
}

# All weapons in the game.
weapon_list = [
	EwWeapon( # 1
		id_weapon = weapon_id_revolver,
		alias = [
			"pistol",
			"handgun",
			"bigiron"
		],
		str_crit = "**Critical Hit!** You have fataly wounded {name_target} with a lethal shot!",
		str_miss = "**You missed!** Your shot whizzed past {name_target}'s head!",
		str_equip = "You equip the revolver.",
		str_name = "revolver",
		str_weapon = "a revolver",
		str_weaponmaster_self = "You are a rank {rank} master of the revolver.",
		str_weaponmaster = "They are a rank {rank} master of the revolver.",
		#str_trauma_self = "You have scarring on both temples, which occasionally bleeds.",
		#str_trauma = "They have scarring on both temples, which occasionally bleeds.",
		str_kill = "{name_player} puts their revolver to {name_target}'s head. **BANG**. Execution-style. Blood splatters across the hot asphalt. {emote_skull}",
		str_killdescriptor = "gunned down",
		str_damage = "{name_target} takes a bullet to the {hitzone}!!",
		str_duel = "**BANG BANG**. {name_player} and {name_target} practice their quick-draw, bullets whizzing past one another's heads.",
		str_description = "It's a revolver.",
		str_reload = "You swing out the revolver’s chamber, knocking out the used shells onto the floor before hastily slamming fresh bullets back into it.",
		str_reload_warning = "**BANG--** *tk tk...* **SHIT!!** {name_player} just spent the last of the ammo in their revolver’s chamber, it’s out of bullets!!",
		str_scalp = " It has a bullet hole in it.",
		fn_effect = get_normal_attack(cost_multiplier = 0.8),
		price = 10000,
		clip_size = 6,
		vendors = [vendor_dojo, vendor_breakroom],
		classes = [weapon_class_ammo],
		stat = stat_revolver_kills,
	),
	EwWeapon( # 2
		id_weapon = weapon_id_dualpistols,
		alias = [
			"dual",
			"pistols",
			"berettas",
			"dualies"
		],
		str_crit = "**Critical Hit!** {name_player} has lodged several bullets into {name_target}'s vital arteries!",
		str_miss = "**You missed!** Your numerous, haphazard shots hit everything but {name_target}!",
		str_equip = "You equip the dual pistols.",
		str_name = "dual pistols",
		str_weapon = "dual pistols",
		str_weaponmaster_self = "You are a rank {rank} master of the dual pistols.",
		str_weaponmaster = "They are a rank {rank} master of the dual pistols.",
		#str_trauma_self = "You have several stitches embroidered into your chest over your numerous bullet wounds.",
		#str_trauma = "They have several stitches embroidered into your chest over your numerous bullet wounds.",
		str_kill = "{name_player} dramatically pulls both triggers on their dual pistols midair, sending two bullets straight into {name_target}'s lungs'. {emote_skull}",
		str_killdescriptor = "double gunned down",
		str_damage = "{name_target} takes a flurry of bullets to the {hitzone}!!",
		str_duel = "**tk tk tk tk tk tk tk tk tk tk**. {name_player} and {name_target} hone their twitch aim and trigger fingers, unloading clip after clip of airsoft BBs into one another with the eagerness of small children.",
		str_description = "They're dual pistols.",
		str_reload = "You swing out the handles on both of your pistols, knocking out the used magazines onto the floor before hastily slamming fresh mags back into them.",
		str_reload_warning = "**tk tk tk tk--** *tk...* **SHIT!!** {name_player} just spent the last of the ammo in their dual pistol’s mags, they’re out of bullets!!",
		str_scalp = " It has a couple bullet holes in it.",
		fn_effect = get_normal_attack(),
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		stat = stat_dual_pistols_kills,
	),
	EwWeapon( # 3
		id_weapon = weapon_id_shotgun,
		alias = [
			"boomstick",
			"remington",
			"scattergun",
			"r870"
		],
		str_crit = "**Critical Hit!** {name_player} has landed a thick, meaty shot into {name_target}'s chest!",
		str_miss = "**You missed!** Your pellets inexplicably dodge {name_target}. Fucking random bullet spread, this game will never be competitive.",
		str_equip = "You equip the shotgun.",
		str_name = "shotgun",
		str_weapon = "a shotgun",
		str_weaponmaster_self = "You are a rank {rank} master of the shotgun.",
		str_weaponmaster = "They are a rank {rank} master of the shotgun.",
		#str_trauma_self = "You have a few large, gaping holes in your abdomen. Someone could stick their arm through the biggest one.",
		#str_trauma = "They have a few large, gaping holes in your abdomen. Someone could stick their arm through the biggest one.",
		str_kill = "{name_player} blasts their shotgun into {name_target}'s chest at point-blank range, causing guts to explode from their back and coat the surrounding street. chk chk Who's next? {emote_skull}",
		str_killdescriptor = "pumped full of lead",
		str_damage = "{name_target} takes a shotgun blast to the {hitzone}!!",
		str_duel = "**BOOM.** {name_player} and {name_target} stand about five feet away from a wall, pumping it full of lead over and over to study it's bullet spread.",
		str_description = "It's a shotgun.",
		str_reload = "You tilt your shotgun and pop shell after shell into its chamber before cocking the forend back. Groovy.",
		str_reload_warning = "**chk--** *...* **SHIT!!** {name_player}’s shotgun has ejected the last shell in it’s chamber, it’s out of ammo!!",
		str_scalp = " It has a gaping hole in the center.",
		fn_effect = get_normal_attack(cost_multiplier = 4, weapon_type = 'heavy'),
		clip_size = 2,
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		classes = [weapon_class_ammo],
		stat = stat_shotgun_kills,
	),
	EwWeapon( # 4
		id_weapon = weapon_id_rifle,
		alias = [
			"assaultrifle",
			"machinegun",
			"mg"
		],
		str_crit = "**Critical hit!!** You unload an entire magazine into the target!!",
		str_miss = "**You missed!** Not one of your bullets connected!!",
		str_equip = "You equip the assault rifle.",
		str_name = "assault rifle",
		str_weapon = "an assault rifle",
		str_weaponmaster_self = "You are a rank {rank} master of the assault rifle.",
		str_weaponmaster = "They are a rank {rank} master of the assault rifle.",
		#str_trauma_self = "Your torso is riddled with scarred-over bulletholes.",
		#str_trauma = "Their torso is riddled with scarred-over bulletholes.",
		str_kill = "**RAT-TAT-TAT-TAT-TAT!!** {name_player} rains a hail of bullets directly into {name_target}!! They're officially toast! {emote_skull}",
		str_killdescriptor = "gunned down",
		str_damage = "Bullets rake over {name_target}'s {hitzone}!!",
		str_duel = "**RAT-TAT-TAT-TAT-TAT!!** {name_player} and {name_target} practice shooting at distant targets with quick, controlled bursts.",
		str_description = "It's a rifle.",
		str_reload = "You hastily rip the spent magazine out of your assault rifle, before slamming a fresh one back into it.",
		str_reload_warning = "**RAT-TAT-TAT--** *ttrrr...* **SHIT!!** {name_player}’s rifle just chewed up the last of it’s magazine, it’s out of bullets!!",
		str_scalp = " It has a shit-load of holes in it.",
		fn_effect = get_normal_attack(cost_multiplier = 0.7, weapon_type = 'burst_fire'),
		clip_size = 10,
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		classes = [weapon_class_ammo],
		stat = stat_rifle_kills,
	),
	EwWeapon( # 5
		id_weapon = weapon_id_smg,
		alias = [
			"submachinegun",
			"machinegun"
		],
		str_crit = "**Critical hit!!** {name_target}’s vital arteries are ruptured by miraculously accurate bullets that actually hit their intended target!!",
		str_miss = "**You missed!!** {name_player}'s reckless aiming sends their barrage of bullets in every direction but into {name_target}’s body!",
		str_equip = "You equip the SMG.",
		str_name = "SMG",
		str_weapon = "an SMG",
		str_weaponmaster_self = "You are a rank {rank} master of the SMG.",
		str_weaponmaster = "They are a rank {rank} master of the SMG.",
		#str_trauma_self = "Your copious amount of bullet holes trigger onlookers’ Trypophobia.",
		#str_trauma = "Their copious amount of bullet holes trigger onlookers’ Trypophobia.",
		str_kill = "**RATTA TATTA TAT!!** {name_player}’s bullet rip through what little was left of {name_target} after the initial barrage. All that remains is a few shreds of clothing and splatterings of slime. {emote_skull}",
		str_killdescriptor = "riddled with bullets",
		str_damage = "A reckless barrage of bullets pummel {name_target}’s {hitzone}!!",
		str_duel = "**RATTA TATTA TAT!!** {name_player} and {name_target} spray bullets across the floor and walls of the Dojo, having a great time.",
		str_description = "It's a submachine gun.",
		# str_jammed = "Your SMG jams again, goddamn piece of shit gun...",
		str_reload = "You hastily rip the spent magazine out of your SMG, before slamming a fresh one back into it.",
		str_reload_warning = "**RATTA TATTA--** *tk tk tk tk…* **SHIT!!** {name_player}’s SMG just chewed up the last of it’s magazine, it’s out of bullets!!",
		# str_unjam = "{name_player} successfully whacks their SMG hard enough to dislodge whatever hunk of gunk was blocking it’s internal processes.",
		str_scalp = " It has a bunch of holes strewn throughout it.",
		fn_effect = get_normal_attack(cost_multiplier = 0.7, weapon_type = 'burst_fire'),
		clip_size = 10,
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		classes = [weapon_class_ammo],
		stat = stat_smg_kills,
	),
	EwWeapon( # 6
		id_weapon = weapon_id_minigun,
		alias = [
			"mini",
			"gatlinggun"
		],
		str_crit = "**Critical hit!!** Round after round of bullets fly through {name_target}, inflicting irreparable damage!!",
		str_miss = "**You missed!!** Despite the growing heap of used ammunition shells {name_player} has accrued, none of their bullets actually hit {name_target}!",
		str_equip = "You equip the minigun.",
		str_name = "minigun",
		str_weapon = "a minigun",
		str_weaponmaster_self = "You are a rank {rank} master of the minigun.",
		str_weaponmaster = "They are a rank {rank} master of the minigun.",
		#str_trauma_self = "What little is left of your body has large holes punched through it, resembling a slice of swiss cheese.",
		#str_trauma = "What little is left of their body has large holes punched through it, resembling a slice of swiss cheese.",
		str_kill = "**TKTKTKTKTKTKTKTKTK!!** {name_player} pushes their minigun barrel right up to {name_target}’s chest, unloading a full round of ammunition and knocking their lifeless corpse back a few yards from the sheer force of the bullets. They failed to outsmart bullet. {emote_skull}",
		str_killdescriptor = "obliterated",
		str_damage = "Cascades of bullet easily puncture and rupture {name_target}’s {hitzone}!!",
		str_duel = "**...** {name_player} and {name_target} crouch close to the ground, throwing sandwiches unto the floor next to each other and repeating memetic voice lines ad nauseam.",
		str_description = "It's a minigun.",
		#str_reload = "You curse under your breath, before pulling a fresh belt of bullets from hammerspace and jamming it into your minigun’s hungry feed.",
		#str_reload_warning = "**TKTKTKTKTKTK--** *wrrrrrr…* **SHIT!!** {name_player}’s minigun just inhaled the last of it’s belt, it’s out of bullets!!",
		str_scalp = " It looks more like a thick slice of swiss cheese than a scalp.",
		fn_effect = get_normal_attack(weapon_type = 'minigun'),
		price = 1000000,
		vendors = [vendor_bazaar],
		classes= [weapon_class_captcha],
		stat = stat_minigun_kills,
		captcha_length = 6
	),
	EwWeapon( # 7
		id_weapon = weapon_id_bat,
		alias = [
			"club",
			"batwithnails",
			"nailbat",
		],
		str_crit = "**Critical hit!!** {name_player} has bashed {name_target} up real bad!",
		str_miss = "**MISS!!** {name_player} swung wide and didn't even come close!",
		str_equip = "You equip the bat with nails in it.",
		str_name = "bat",
		str_weaponmaster_self = "You are a rank {rank} master of the nailbat.",
		str_weaponmaster = "They are a rank {rank} master of the nailbat.",
		str_weapon = "a bat full of nails",
		#str_trauma_self = "Your head appears to be slightly concave on one side.",
		#str_trauma = "Their head appears to be slightly concave on one side.",
		str_kill = "{name_player} pulls back for a brutal swing! **CRUNCCHHH.** {name_target}'s brains splatter over the sidewalk. {emote_skull}",
		str_killdescriptor = "nail bat battered",
		str_damage = "{name_target} is struck with a hard blow to the {hitzone}!!",
		# str_backfire = "{name_player} recklessly budgens themselves with a particularly overzealous swing! Man, how the hell could they fuck up so badly?",
		str_duel = "**SMASHH! CRAASH!!** {name_player} and {name_target} run through the neighborhood, breaking windshields, crushing street signs, and generally having a hell of a time.",
		str_description = "It's a nailbat.",
		str_scalp = " It has a couple nails in it.",
		fn_effect = get_normal_attack(weapon_type = 'variable_damage'),
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		stat = stat_bat_kills,
	),
	EwWeapon( # 8
		id_weapon = weapon_id_brassknuckles,
		alias = [
			"knuckles",
			"knuckledusters",
			"dusters"
		],
		str_crit = "***SKY UPPERCUT!!*** {name_player} executes an artificially difficult combo, rocketing their fist into the bottom of {name_target}’s jaw so hard that {name_target}’s colliding teeth brutally sever an inch off their own tongue!!",
		str_miss = "**MISS!** {name_player} couldn't land a single blow!!",
		str_equip = "You equip the brass knuckles.",
		str_name = "brass knuckles",
		str_weapon = "brass knuckles",
		str_weaponmaster_self = "You are a rank {rank} master pugilist.",
		str_weaponmaster = "They are a rank {rank} master pugilist.",
		#str_trauma_self = "You've got two black eyes, missing teeth, and a profoundly crooked nose.",
		#str_trauma = "They've got two black eyes, missing teeth, and a profoundly crooked nose.",
		str_kill = "{name_player} slugs {name_target} right between the eyes! *POW! THWACK!!* **CRUNCH.** Shit. May have gotten carried away there. Oh, well. {emote_skull}",
		str_killdescriptor = "pummeled to death",
		str_damage = "{name_target} is socked in the {hitzone}!!",
		str_duel = "**POW! BIFF!!** {name_player} and {name_target} take turns punching each other in the abs. It hurts so good.",
		str_description = "They're brass knuckles.",
		str_scalp = " It has bone fragments in it.",
		fn_effect = get_normal_attack(weapon_type = 'variable_damage'),
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		stat = stat_brassknuckles_kills,
	),
	EwWeapon( # 9
		id_weapon = weapon_id_katana,
		alias = [
			"weebsword",
			"ninjasword",
			"samuraisword",
			"blade"
		],
		str_crit = "**Critical hit!!** {name_target} is cut deep!!",
		str_miss = "",
		str_equip = "You equip the katana.",
		str_name = "katana",
		str_weapon = "a katana",
		str_weaponmaster_self = "You are a rank {rank} blademaster.",
		str_weaponmaster = "They are a rank {rank} blademaster.",
		#str_trauma_self = "A single clean scar runs across the entire length of your body.",
		#str_trauma = "A single clean scar runs across the entire length of their body.",
		str_kill = "Faster than the eye can follow, {name_player}'s blade glints in the greenish light. {name_target} falls over, now in two pieces. {emote_skull}",
		str_killdescriptor = "bisected",
		str_damage = "{name_target} is slashed across the {hitzone}!!",
		str_duel = "**CRACK!! THWACK!! CRACK!!** {name_player} and {name_target} duel with bamboo swords, viciously striking at head, wrist and belly.",
		str_description = "It's a katana.",
		str_scalp = " It seems to have been removed with some precision.",
		fn_effect = get_normal_attack(weapon_type = 'precision'),
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		classes= [weapon_class_captcha],
		stat = stat_katana_kills,
		captcha_length = 4
	),
	EwWeapon( # 10
		id_weapon = weapon_id_broadsword,
		alias = [
			"sword",
			"highlander",
			"arawheapofiron",
			"eyelander"
		],
		str_crit = "Critical hit!! {name_player} screams at the top of their lungs and unleashes a devastating overhead swing that maims {name_target}.",
		str_miss = "You missed! You grunt as your failed overhead swing sends ripples through the air.",
		# str_backfire = "You feel the bones in your wrists snap as you botch your swing with the heavy blade!! Fucking ouch dawg!",
		str_equip = "You equip the broadsword.",
		str_name = "broadsword",
		str_weapon = "a broadsword",
		str_weaponmaster_self = "You are a rank {rank} berserker.",
		str_weaponmaster = "They are a rank {rank} berserker.",
		#str_trauma_self = "A large dent resembling that of a half-chopped down tree appears on the top of your head.",
		#str_trauma = "A dent resembling that of a half-chopped down tree appears on the top of their head.",
		str_kill = "{name_player} skewers {name_target} through the back to the hilt of their broadsword, before kicking their lifeless corpse onto the street corner in gruseome fashion. {name_player} screams at the top of their lungs. {emote_skull}",
		str_killdescriptor = "slayed",
		str_damage = "{name_target}'s {hitzone} is separated from their body!!",
		str_duel = "SCHWNG SCHWNG! {name_player} and {name_target} scream at the top of their lungs to rehearse their battle cries.",
		str_description = "It's a broadsword.",
		str_reload = "You summon strength and muster might from every muscle on your body to hoist your broadsword up for another swing.",
		str_reload_warning = "**THUD...** {name_player}’s broadsword is too heavy, it’s blade has fallen to the ground!!",
		str_scalp = " It was sloppily lopped off.",
		clip_size = 1,
		price = 10000,
		fn_effect = get_normal_attack(weapon_type = 'heavy'),
		vendors = [vendor_dojo, vendor_breakroom],
		stat = stat_broadsword_kills,
	),
	EwWeapon( # 11
		id_weapon = weapon_id_nunchucks,
		alias = [
			"nanchacku",
			"nunchaku",
			"chucks",
			"numchucks",
			"nunchucks"
		],
		str_crit = "**COMBO!** {name_player} strikes {name_target} with a flurry of 5 vicious blows!",
		# str_backfire = "**Whack!!** {name_player} fucks up their kung-fu routine and whacks themselves in the head with their own nun-chucks!!",
		str_equip = "You equip the nun-chucks.",
		str_name = "nun-chucks",
		str_weapon = "nun-chucks",
		str_weaponmaster_self = "You are a rank {rank} kung-fu master.",
		str_weaponmaster = "They are a rank {rank} kung-fu master.",
		#str_trauma_self = "You are covered in deep bruises. You hate martial arts of all kinds.",
		#str_trauma = "They are covered in deep bruises. They hate martial arts of all kinds.",
		str_kill = "**HIIII-YAA!!** With expert timing, {name_player} brutally batters {name_target} to death, then strikes a sweet kung-fu pose. {emote_skull}",
		str_killdescriptor = "fatally bludgeoned",
		str_damage = "{name_target} takes {strikes} nun-chuck whacks directly in the {hitzone}!!",
		str_duel = "**HII-YA! HOOOAAAAAHHHH!!** {name_player} and {name_target} twirl wildly around one another, lashing out with kung-fu precision.",
		str_description = "They're nunchucks.",
		str_scalp = " It looks very bruised.",
		fn_effect = get_normal_attack(weapon_type = 'burst_fire'),
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		stat = stat_nunchucks_kills,
	),
	EwWeapon( # 12
		id_weapon = weapon_id_scythe,
		alias = [
			"sickle"
		],
		str_crit = "**Critical hit!!** {name_target} is carved by the wicked curved blade!",
		str_miss = "**MISS!!** {name_player}'s swings wide of the target!",
		str_equip = "You equip the scythe.",
		str_name = "scythe",
		str_weapon = "a scythe",
		str_weaponmaster_self = "You are a rank {rank} master of the scythe.",
		str_weaponmaster = "They are a rank {rank} master of the scythe.",
		#str_trauma_self = "You are wrapped tightly in bandages that hold your two halves together.",
		#str_trauma = "They are wrapped tightly in bandages that hold their two halves together.",
		str_kill = "**SLASHH!!** {name_player}'s scythe cleaves the air, and {name_target} staggers. A moment later, {name_target}'s torso topples off their waist. {emote_skull}",
		str_killdescriptor = "sliced in twain",
		str_damage = "{name_target} is cleaved through the {hitzone}!!",
		str_duel = "**WHOOSH, WHOOSH** {name_player} and {name_target} swing their blades in wide arcs, dodging one another's deadly slashes.",
		str_description = "It's a scythe.",
		str_scalp = " It's cut in two pieces.",
		price = 10000,
		fn_effect = get_normal_attack(weapon_type = 'heavy'),
		vendors = [vendor_dojo, vendor_breakroom],
		stat = stat_scythe_kills,
	),
	EwWeapon( # 13
		id_weapon = weapon_id_yoyo,
		alias = [
			"yo-yos",
			"yoyo",
			"yoyos"
		],
		str_crit = "SMAAAASH!! {name_player} pulls off a modified Magic Drop, landing a critical hit on {name_target} just after the rejection!",
		str_miss = "You missed! {name_player} misjudges their yo-yos trajectory and botches an easy trick.",
		str_equip = "You equip the yo-yo.",
		str_name = "yo-yo",
		str_weaponmaster_self = "You are a rank {rank} master of the yo-yo.",
		str_weaponmaster = "They are a rank {rank} master of the yo-yo.",
		str_weapon = "a yo-yo",
		#str_trauma_self = "Simple yo-yo tricks caught even in your peripheral vision triggers intense PTSD flashbacks.",
		#str_trauma = "Simple yo-yo tricks caught even in their peripheral vision triggers intense PTSD flashbacks.",
		str_kill = "{name_player} performs a modified Kwyjibo, effortlessly nailing each step before killing their opponent just ahead of the dismount.",
		str_killdescriptor = "amazed",
		str_damage = "{name_player} used {name_target}'s {hitzone} as a counterweight!!",
		str_duel = "whhzzzzzz {name_player} and {name_target} practice trying to Walk the Dog for hours. It never clicks.",
		str_description = "It's a yo-yo.",
		str_scalp = " It has a ball bearing hidden inside it. You can spin it like a fidget spinner.",
		fn_effect = get_normal_attack(),
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		stat = stat_yoyo_kills,
	),
	EwWeapon( # 14
		id_weapon = weapon_id_knives,
		alias = [
			"knife",
			"dagger",
			"daggers",
			"throwingknives",
			"throwingknife"
		],
		str_crit = "**Critical hit!!** {name_player}'s knife strikes a vital point!",
		str_miss = "**MISS!!** {name_player}'s knife missed its target!",
		str_equip = "You equip the throwing knives.",
		str_name = "throwing knives",
		str_weapon = "throwing knives",
		str_weaponmaster_self = "You are a rank {rank} master of the throwing knife.",
		str_weaponmaster = "They are a rank {rank} master of the throwing knife.",
		#str_trauma_self = "You are covered in scarred-over lacerations and puncture wounds.",
		#str_trauma = "They are covered in scarred-over lacerations and puncture wounds.",
		str_kill = "A blade flashes through the air!! **THUNK.** {name_target} is a goner, but {name_player} slits their throat before fleeing the scene, just to be safe. {emote_skull}",
		str_killdescriptor = "knifed",
		str_damage = "{name_target} is stuck by a knife in the {hitzone}!!",
		str_duel = "**TING! TING!!** {name_player} and {name_target} take turns hitting one another's knives out of the air.",
		str_description = "They're throwing knives.",
		str_scalp = " It has about a half dozen stab holes in it.",
		fn_effect = get_normal_attack(weapon_type = 'small_game'),
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		stat = stat_knives_kills,
	),
	EwWeapon( # 15
		id_weapon = weapon_id_molotov,
		alias = [
			"firebomb",
			"molotovcocktail",
			"bomb",
			"bombs",
			"moly"
		],
		# str_backfire = "**Oh, the humanity!!** The bottle bursts in {name_player}'s hand, burning them terribly!!",
		str_miss = "**A dud!!** the rag failed to ignite the molotov!",
		str_crit = "{name_player}’s cocktail shatters at the feet of {name_target}, sending a shower of shattered shards of glass into them!!",
		str_equip = "You equip the molotov cocktail.",
		str_name = "molotov cocktail",
		str_weapon = "molotov cocktails",
		str_weaponmaster_self = "You are a rank {rank} master arsonist.",
		str_weaponmaster = "They are a rank {rank} master arsonist.",
		#str_trauma_self = "You're wrapped in bandages. What skin is showing appears burn-scarred.",
		#str_trauma = "They're wrapped in bandages. What skin is showing appears burn-scarred.",
		str_kill = "**SMASH!** {name_target}'s front window shatters and suddenly flames are everywhere!! The next morning, police report that {name_player} is suspected of arson. {emote_skull}",
		str_killdescriptor = "exploded",
		str_damage = "{name_target} dodges a bottle, but is singed on the {hitzone} by the blast!!",
		str_duel = "{name_player} and {name_target} compare notes on frontier chemistry, seeking the optimal combination of combustibility and fuel efficiency.",
		str_description = "These are glass bottles filled with some good ol' fashioned pyrotechnics.",
		str_scalp = " It's burnt to a crisp!",
		fn_effect = get_normal_attack(weapon_type = 'incendiary'),
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		classes = [weapon_class_burning, weapon_class_captcha],
		stat = stat_molotov_kills,
		captcha_length = 4
	),
	EwWeapon( # 16
		id_weapon = weapon_id_grenades,
		alias = [
			"nades",
			"grenade"
		],
		str_crit = "**Critical hit!!** {name_target} is blown off their feet by the initial explosion, and lacerated by innumerable shards of shrapnel scattering themselves through their body!!",
		str_miss = "**You missed!!** {name_player}’s poor aim sends their grenade into a nearby alleyway, it’s explosion eliciting a Wilhelm scream and the assumed death of an innocent passerby. LOL!!",
		str_equip = "You equip the grenades.",
		str_name = "grenades",
		str_weapon = "grenades",
		str_weaponmaster_self = "You are a rank {rank} master of the grenades.",
		str_weaponmaster = "They are a rank {rank} master of the grenades.",
		#str_trauma_self = "Blast scars and burned skin are spread unevenly across your body.",
		#str_trauma = "Blast scars and burned skin are spread unevenly across their body.",
		str_kill = "**KA-BOOM!!** {name_player} pulls the safety pin and holds their grenade just long enough to cause it to explode mid air, right in front of {name_target}’s face, blowing it to smithereens. {emote_skull}",
		str_killdescriptor = "exploded",
		str_damage = "{name_player}’s grenade explodes, sending {name_target}’s {hitzone} flying off their body!!",
		str_duel = "**KA-BOOM!!** {name_player} and {name_target} pull the pin out of their grenades and hold it in their hands to get a feel for how long it takes for them to explode. They lose a few body parts in the process.",
		str_description = "A stack of grenades.",
		str_scalp = " It's covered in metallic shrapnel.",
		fn_effect = get_normal_attack(weapon_type = 'explosive'),
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		classes = [weapon_class_exploding, weapon_class_captcha],
		stat = stat_grenade_kills,
		captcha_length = 4
	),
	EwWeapon( # 17
		id_weapon = weapon_id_garrote,
		alias = [
			"wire",
			"garrotewire",
			"garrottewire"
		],
		str_crit = "**CRITICAL HIT!!** {name_player} got lucky and caught {name_target} completely unaware!!",
		str_miss = "**MISS!** {name_player}'s target got away in time!",
		str_equip = "You equip the garrotte wire.",
		str_name = "garrote wire",
		str_weapon = "a garrotte wire",
		str_weaponmaster_self = "You are a rank {rank} master of the garrotte.",
		str_weaponmaster = "They are a rank {rank} master of the garrotte.",
		#str_trauma_self = "There is noticeable bruising and scarring around your neck.",
		#str_trauma = "There is noticeable bruising and scarring around their neck.",
		str_kill = "{name_player} quietly moves behind {name_target} and... **!!!** After a brief struggle, only a cold body remains. {emote_skull}",
		str_killdescriptor = "garrote wired",
		str_damage = "{name_target} is ensnared by {name_player}'s wire!!",
		str_duel = "{name_player} and {name_target} compare their dexterity by playing Cat's Cradle with deadly wire.",
		str_description = "It's a garrote wire.",
		str_scalp = " It's a deep shade of blue.",
		fn_effect = wef_garrote,
		price = 10000,
		vendors = [vendor_dojo, vendor_breakroom],
		stat = stat_garrote_kills,
	),
	EwWeapon(  # 18
		id_weapon = weapon_id_pickaxe,
		alias = [
			"pick",
			"poudrinpickaxe",
			"poudrinpick"
		],
		str_crit = "**Critical hit!!** By sheer dumb luck, {name_player} manages to get a good hit off on {name_target}’s {hitzone}.",
		str_miss = "**MISS!!** {name_player} is too weak to lift their pickaxe!",
		str_equip = "You equip the pickaxe.",
		str_name = "pickaxe",
		str_weapon = "a pickaxe",
		str_weaponmaster_self = "You are a rank {rank} coward of the pickaxe.",
		str_weaponmaster = "They are a rank {rank} coward of the pickaxe.",
		#str_trauma_self = "There is a deep, precise indent in the crown of your skull. How embarrassing!",
		#str_trauma = "There is a deep, precise indent in the crown of their skull. How embarrassing!",
		str_kill = "**THWACK!!** {name_player} summons what little courage they possess to lift the pickaxe above their head and !mine {name_target} to death. How embarrassing! {emote_skull}",
		str_killdescriptor = "!mined",
		str_damage = "{name_target} is lightly tapped on the {hitzone}!!",
		str_duel = "**THWACK, THWACK** {name_player} and {name_target} spend some quality time together, catching up and discussing movies they recently watched or food they recently ate.",
		str_scalp = " It reeks of dirt and poudrins. How embarrassing!",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		str_description = "It's a pickaxe.",
		acquisition = acquisition_smelting,
		stat = stat_pickaxe_kills,
		is_tool = 1
	),
	EwWeapon(  # 19
		id_weapon = weapon_id_fishingrod,
		alias = [
			"fish",
			"fishing",
			"rod",
			"super",
			"superrod",
			"superfishingrod"
		],
		str_crit = "**Critical hit!!** By sheer dumb luck, {name_player} manages to get a good hit off on {name_target}’s {hitzone}.",
		str_miss = "**MISS!!** {name_player} is too weak to cast their fishing rod!",
		str_equip = "You equip the super fishing rod.",
		str_name = "super fishing rod",
		str_weapon = "a super fishing rod",
		str_weaponmaster_self = "You are a rank {rank} coward of the super fishing rod.",
		str_weaponmaster = "They are a rank {rank} coward of the super fishing rod.",
		#str_trauma_self = "There is a piercing on the side of your mouth. How embarrassing!",
		#str_trauma = "There is a piercing on the side of their mouth. How embarrassing!",
		str_kill = "*whsssh* {name_player} summons what little courage they possess to reel in {name_target} and wring all the slime out of them. How embarrassing! {emote_skull}",
		str_killdescriptor = "!reeled",
		str_damage = "{name_target} is lightly pierced on the {hitzone}!!",
		str_duel = "**whsssh, whsssh** {name_player} and {name_target} spend some quality time together, discussing fishing strategy and preferred types of bait.",
		str_scalp = " It has a fishing hook stuck in it. How embarrassing!",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		str_description = "It's a super fishing rod.",
		acquisition = acquisition_smelting,
		stat = stat_fishingrod_kills,
		is_tool = 1
	),
	EwWeapon(  # 20
		id_weapon = weapon_id_bass,
		alias = [
			"bass",
		],
		str_crit = "**Critical hit!!** Through skilled swipes {name_player} manages to sharply strike {name_target}’s {hitzone}.",
		str_miss = "**MISS!!** {name_player} swings and misses like a dumbass!",
		str_equip = "You equip the bass guitar, a highly distorted and reverbed riff of unknown origin plays as you place the strap over your neck.",
		str_name = "bass guitar",
		str_weapon = "a bass guitar",
		str_weaponmaster_self = "You are a rank {rank} master of the bass guitar.",
		str_weaponmaster = "They are a rank {rank} master of the bass guitar.",
		#str_trauma_self = "There is a large concave dome in the side of your head.",
		#str_trauma = "There is a large concave dome in the side of their head.",
		str_kill = "*CRASSHHH.* {name_player} brings down the bass on {name_target} with righteous fury. Discordant notes play harshly as the bass trys its hardest to keep itself together. {emote_skull}",
		str_killdescriptor = "smashed to pieces",
		str_damage = "{name_target} is whacked across the {hitzone}!!",
		str_duel = "**SMASHHH.** {name_player} and {name_target} smash their bass together before admiring eachothers skillful basslines.",
		str_scalp = " If you listen closely, you can still hear the echoes of a sick bassline from yesteryear.",
		fn_effect = get_normal_attack(weapon_type = 'variable_damage'),
		str_description = "It's a bass guitar. All of its strings are completely out of tune and rusted.",
		acquisition = acquisition_smelting,
		stat = stat_bass_kills,
	),
	EwWeapon(  # 21
		id_weapon = weapon_id_umbrella,
		alias = [
			"umbrella",
			"slimebrella",
			"slimecorpumbrella"
		],
		str_crit = "**Critical hit!!** {name_player} briefly stuns {name_target} by opening their umbrella in their face, using the opportunity to score a devastating blow to their {hitzone}.",
		str_miss = "**MISS!!** {name_player} fiddles with their umbrella, failing to open it!",
		str_equip = "You equip the umbrella.",
		str_name = "umbrella",
		str_weapon = "an umbrella",
		str_weaponmaster_self = "You are a rank {rank} master of the umbrella.",
		str_weaponmaster = "They are a rank {rank} master of the umbrella.",
		#str_trauma_self = "You have a large hole in your chest.",
		#str_trauma = "They have a large hole in their chest.",
		str_kill = "*SPLAT.* {name_player} pierces {name_target} through the chest, hoists them over their head and opens their umbrella, causing them to explode in a rain of blood and slime. {emote_skull}",
		str_killdescriptor = "umbrella'd",
		str_damage = "{name_target} is struck in the {hitzone}!!",
		str_duel = "**THWACK THWACK.** {name_player} and {name_target} practice their fencing technique, before comparing their favorite umbrella patterns.",
		str_scalp = " At least it didn't get wet.",
		fn_effect = get_normal_attack(weapon_type = 'defensive'),
		str_description = "It's an umbrella, both stylish and deadly.",
		price = 100000,
		vendors = [vendor_bazaar],
		classes = [weapon_class_defensive, weapon_class_captcha],
		stat = stat_umbrella_kills,
		captcha_length = 4
	),
	EwWeapon(  # 22
		id_weapon = weapon_id_bow,
		alias = [
			"bow",
		],
		str_crit = "**Critical hit!!** Through measured shots {name_player} manages to stick a pixelated arrow in {name_target}’s {hitzone}.",
		str_miss = "**MISS!!** {name_player} completely misses, a pixelated arrow embeds itself into the ground!",
		str_equip = "You equip the minecraft bow, c418 music plays in the background.",
		str_name = "minecraft bow",
		str_weapon = "a minecraft bow",
		str_weaponmaster_self = "You are a rank {rank} minecraft bowmaster.",
		str_weaponmaster = "They are a rank {rank} minecraft bowmaster.",
		#str_trauma_self = "There is a pixelated arrow in the side of your head.",
		#str_trauma = "There is a pixelated arrow in the side of their head.",
		str_kill = "*Pew Pew Pew.* {name_player} spams the bow as {name_target}'s life fades, riddling their body with arrows. {emote_skull}",
		str_killdescriptor = "shot to death",
		str_damage = "{name_target} is shot in the {hitzone}!!",
		str_duel = "{name_player} and {name_target} shoot distant targets, {name_player} is clearly the superior bowman.",
		str_scalp = " The scalp has pixels covering it.",
		fn_effect = get_normal_attack(weapon_type = 'small_game'),
		str_description = "It's a newly crafted minecraft bow, complete with a set of minecraft arrows",
		acquisition = acquisition_smelting,
		stat = stat_bow_kills,
	),
	EwWeapon(  # 23
		id_weapon = weapon_id_dclaw,
		alias = [
			"dragon claw",
		],
		str_crit = "{name_player} runs like a madman towards {name_target}, {name_target} swings but is deftly parried by {name_player}, {name_player} hoists their dragon claw into the air and ripostes {name_target} for massive damage ***!!!Critical Hit!!!***",
		str_miss = "{name_player} swings but {name_target} is in the middle of a dodge roll and is protected by iframes. **!!Miss!!**",
		str_equip = "You place the core of the dragon claw on your hand and it unfolds around it, conforming to the contour of your hands, claws protude out the end of your fingers as your hand completes its transformation into the *dragon claw*.",
		str_name = "dragon claw",
		str_weapon = "a dragon claw",
		str_weaponmaster_self = "You are a rank {rank} master of the dragon claw.",
		str_weaponmaster = "They are a rank {rank} master of the dragon claw.",
		#str_trauma_self = "Three smoldering claw marks are burned into your flesh, the flames `won't seem to extinguish.",
		#str_trauma = "Three smoldering claw marks are burned into their flesh, the flames won't seem to extinguish.",
		str_kill = "***Thwip.*** {name_player}'s dragon claw cuts the air followed by a trail of flame and blood, the camera pans out and {name_target} is shown, cut in twain. {emote_skull}",
		str_killdescriptor = "cut to pieces",
		str_damage = random.choice(["{name_target} is slashed across the {hitzone}!!","{name_player} furiously slashes {name_target} across the {hitzone}!!","{name_player} flicks their fingers and a jet of flame ignites from the dragon claw, burning {name_target} in the {hitzone}!!"]),
		str_duel = "**SLICE!! SWIPE!! SLASH!!** {name_player} and {name_target} cut the fuck out of eachother, a fire extinguisher is never more than a meter away.",
		str_scalp = "The scalp is burning and doesn't look like it's gonna stop.",
		fn_effect = get_normal_attack(weapon_type = 'incendiary'),
		str_description = "It's the core of a Dragon Claw, it will morph around whatever hand it is held by granting them the power of the elusive GREEN EYES SLIME DRAGON. If you listen closely you can hear whines of the dragon soul as it remains perpetually trapped in the weapon.",
		acquisition = acquisition_smelting,
		stat = stat_dclaw_kills,
		classes = [weapon_class_burning, weapon_class_captcha],
		captcha_length = 4
	),

	EwWeapon(  # 24
		id_weapon=weapon_id_spraycan,
		alias=[
			"spray can",
			"spray"
		],
		str_crit="**Critical hit!!** {name_player} flicks the nozzle off their spray can and lights it like a fuse! {name_target} gets nasty burns and a fresh coat of paint! **WHOOSH!!!**",
		str_miss="**MISS!!** {name_player} attempts a spray attack, but the wind blows it back in their face!",
		str_equip="You hold the spray can tightly, hoping to god somebody confuses it for a gun.",
		str_name="spray can",
		str_weapon="a spray can",
		str_weaponmaster_self="You are a rank {rank} vandal of the spray can.",
		str_weaponmaster="They are a rank {rank} vandal of the spray can.",
		# str_trauma_self = "You're having trouble breathing, and the inside of your mouth is off-color.",
		# str_trauma = "They're weirdly short of breath, and their mouth and tongue are off-color.",
		str_kill="***PPPPPPSSSSSSSSSHHHHHhhhhhfff.*** {name_player} forcibly opens {name_target}'s mouth and sprays everything they have into their lungs. Their eyes roll back into their head and, trembling, they slowly asphyxiate in your arms. {emote_skull}",
		str_killdescriptor="suffocated",
		str_damage=random.choice(["{name_target} is whacked across the {hitzone}!!",
								  "{name_player} sprays {name_target} with paint, making them a gaudy color in the {hitzone}!!",
								  "{name_player} humiliates {name_target} by bringing a spray can to a gunfight, mentally damaging them in the {hitzone}!!"]),
		str_duel="**PSSS PSSS PSSSSSHH!** {name_player} and {name_target} spray the dojo walls until they get dizzy from the smell.",
		str_scalp="The scalp is a nice shade of mauve.",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		str_description="It's a Based Hardware brand spray can, in your gang's color. The blurb on the backside preaches about the merits of street art and murals, but you're pretty sure that's just to cover their ass.",
		vendors = [vendor_basedhardware, vendor_breakroom],
		stat=stat_spraycan_kills,
		classes=[weapon_class_paint, weapon_class_captcha],
		#sap_cost=2,
		captcha_length=3,
		is_tool = 1,
		# str_backfire = "As {name_player} shakes the can to fire another shot, the thing suddenly explodes on them!",
		tool_props = {
		'reg_spray' : "You run down the streets, tagging buildings, street signs and old ladies with spray paint in the image of the {gang}!",
		'miss_spray' : "**Miss!** Your can seems to be low on spray. You fill it up and give it a good shake. Good as new!",
		'crit_spray' : "**Critical hit!** You dual wield spray cans, painting an urban masterpiece in one hand and shooting toxic chemicals into a cop's mouth with the other!",
		'equip_spray' : "You get your trusty spray paint at the ready."}
		),
	EwWeapon(  # 25
		id_weapon=weapon_id_paintgun,
		alias=[
			"paint gun",
			"splatoon"
		],
		str_crit="**Critical hit!!** {name_player} aims down the sights with the precision of a video game real life sniper, shooting {name_target} in the eyes from 30 yards! **SPLAAAAAT!!!**",
		str_miss="**MISS!!** {name_player} fires off a volley of paint, but {name_target} jumps behind cover!",
		str_equip="Now listen here. You just equipped a paint gun. Keep in mind this is the weapon that boomer families shoot each other with to have fun. Enjoy trying to kill with it.",
		str_name="paint gun",
		str_weapon="a paint gun",
		str_weaponmaster_self="You are a rank {rank} vandal of the paint gun.",
		str_weaponmaster="They are a rank {rank} vandal of the paint gun.",
		# str_trauma_self = "You have a splitting headache.",
		# str_trauma = "They look hungover, almost like their entire body exploded.",
		str_kill="***SPLAAAAART!!!!*** {name_player} fatally strikes {name_target}, and they explode from the inside out! There's a lot more gore than when you see it happen in Splatoon, though.{emote_skull}",
		str_killdescriptor="imploded",
		str_damage=random.choice(["{name_target} is splatted in the {hitzone}!!",
								  "{name_player} shoots {name_target} with paint, making them a gaudy color in the {hitzone}!!",
								  "{name_player} attacks {name_target} with harmless paint!!"]),
		str_duel="**SPLAT TAT TAT!!** {name_player} and {name_target} harass everyone in the dojo with their paint guns.",
		str_scalp="The scalp is colorful, from both blood and paint.",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		str_description="It's an industrial strength two handed paint gun with a sniper scope attached. What do they use this for in industry, anyway?",
		vendors=[vendor_basedhardware, vendor_breakroom],
		stat=stat_paintgun_kills,
		classes=[weapon_class_paint, weapon_class_ammo, weapon_class_captcha],
		clip_size = 15,
		price = 5000,
		#sap_cost=2,
		captcha_length=4,
		is_tool = 1,
		str_reload = "*Click.* You grab a paint cylinder from god knows where and load it into your gun, chucking the leftover one behind an alleyway.",
		# str_backfire = "Whoops, looks like somebody didn't fasten the paint cylinder hard enough! {name_player} gets a thorough spray to the face!",
		tool_props = {
			'reg_spray':  "You find a patch of wall several yards away that hasn't been vandalized yet. Time to take aim and...BAM! Nice shot!",
			'miss_spray': "**Miss!** Your aim was as sharp as ever, but a fucking pigeon took the hit! Christ, what are the odds?",
			'crit_spray': "**Critical hit!** The paint bullet skids a wall, spreading your paint across the whole thing!",
			'equip_spray': "You load a clip of paint into the gun and throw it onto your back, kinda like Rambo if he were an art major."
		}
	),
	EwWeapon(  # 26
		id_weapon=weapon_id_paintroller,
		alias=[
			"paint roller",
			"roller"
		],
		str_crit="**Critical hit!!** {name_player}  knocks {name_target} to the ground and does a golf swing to their vulnerable little head, sending them spinning. **FWAP!!!**",
		str_miss="**MISS!!** {name_player} does cringey bo staff jujitsu moves with the roller and forgets to actually attack {name_target}!",
		str_equip="You hold the paint roller in your hand. The light plastic broom handle and spongy brush are sure to deal at least 10 damage.",
		str_name="paint roller",
		str_weapon="a paint roller",
		str_weaponmaster_self="You are a rank {rank} vandal of the paint roller.",
		str_weaponmaster="They are a rank {rank} vandal of the paint roller.",
		# str_trauma_self = "There's a gaudy colored dent in your skull.",
		# str_trauma = "There is a gaudy colored dent in their skull.",
		str_kill="***CA-CRACK!*** {name_player} opens {name_target}'s skull like an egg using the dull metal edge of the roller. It appears to be hollow, after all, {name_target} was stupid enough to get killed with a fucking paint roller.{emote_skull}",
		str_killdescriptor="cracked open",
		str_damage=random.choice(["{name_target} is swatted in the {hitzone}!!",
								  "{name_player} slaps {name_target} with paint, making them a gaudy color in the {hitzone}!!",
								  "{name_player} rolls paint all over {name_target}'s {hitzone}!!"]),
		str_duel="{name_player} and {name_target} quietly pass the time rolling paint over the windows of nearby houses You both have learned tranquility.",
		str_scalp="The scalp is split in half, with a big hole right in the middle.",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		price = 4500,
		str_description="It's a long, broom-like plastic paint roller with a spongy brush and metal axle. The modern man's bo staff.",
		vendors=[vendor_basedhardware, vendor_breakroom],
		stat=stat_paintroller_kills,
		classes=[weapon_class_paint, weapon_class_captcha],
		#sap_cost=2,
		captcha_length=4,
		is_tool=1,
		# str_backfire = "{name_player} waves the paint roller around like it's a plastic toy, spreading paint nowhere but giving themselves a thorough welt in the head from the 2 square inches of it that could actually do any damage. How'd they manage that?",
		tool_props = {
			'reg_spray' : "You roll paint over as much surface area as your puny little Juvie legs can take you to.",
			'miss_spray' : "**Miss!** The sponge on your roller snaps off and it takes too long for you to notice. What a waste!",
			'crit_spray' : "**Critical hit!** Your mind goes blank in a painting-induced rage. When you wake up, all your surroundings are {color} You should do that more often!",
			'equip_spray' : "You grab your paint roller and strap it on your back."}
		),
	EwWeapon(  # 27
		id_weapon=weapon_id_paintbrush,
		alias=[
			"paint brushes",
			"brush"
		],
		str_crit="**Critical hit!!** {name_player}  stabs {name_target} with one brush and paints over their eyes with another!  **HOT DOG!!!**",
		str_miss="**MISS!!** {name_player} throws the brushes at {name_target}, but they get hit with the soft bristles instead of the pointy bit!",
		str_equip="If only you had a whittling knife that could sharpen paintbrush handles. That way you could equip the knife as a weapon instead of this.",
		str_name="paintbrushes",
		str_weapon="paintbrushes",
		str_weaponmaster_self="You are a rank {rank} vandal of the paintbrush.",
		str_weaponmaster="They are a rank {rank} vandal of the paintbrush.",
		# str_trauma_self = "You have bruises all over your body and you can't get the paint out of your clothes.",
		# str_trauma = "They have bruises all over their body, and they can't get the paint out of their clothes.",
		str_kill="***MASTERPIECE!*** {name_target} takes a mortal brush to the forehead, courtesy of {name_player}'s talent as a painter. {emote_skull}",
		str_killdescriptor="paintbrushed to death",
		str_damage=random.choice(["{name_target} is handlestabbed in the {hitzone}!!",
								  "{name_player} flecks {name_target} with paint, making them a gaudy color in the {hitzone}!!",
								  "{name_player} grazes {name_target}'s {hitzone} with coarse bristles!!"]),
		str_duel="{name_player} and {name_target} paint random text commands on the walls outside the Dojo. {name_target} paints some furry art when nobody's looking.",
		str_scalp="The scalp has a bunch of welts, and has a faint smell of lead.",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		str_description="A stack of large, coarse-bristled paintbrushes, linked together on a burlap string.",
		vendors=[vendor_basedhardware, vendor_breakroom],
		stat=stat_paintbrush_kills,
		classes=[weapon_class_paint, weapon_class_captcha],
		#sap_cost=2,
		price = 100,
		captcha_length=3,
		is_tool=1,
		# str_backfire = "In an attempt to paint faster, {name_player} sticks one of the handles in their mouth and try to use it to cover more ground. Instead, they broke your teeth and scraped their cheek on a hard brick surface. Better not try that again...",
		tool_props = {
			'reg_spray' : "You paint vulgar {gang} symbols on as many buildings as you can.",
			'miss_spray' : "**Miss!** You finish with a paint can and have to switch! You waste too much time getting the can open.",
			'crit_spray' : "**Critical hit!**  You hold the paint can in your mouth and start crab walking, throwing paint along the wall as you do it! Somehow, this is more efficient!",
			'equip_spray' : "You get your brushes at the ready."}
	),
	EwWeapon(  # 28
		id_weapon=weapon_id_watercolors,
		alias=[
			"paint brushes",
			"brush"
		],
		str_crit="```css\n\"oooOOOOOOOH LA LA! {name_target} is exposed to {name_player}'s watercolor pornography! They won't be able to recover from that!\"\n```",
		str_miss="```css\n[{name_player} paints a picture for {name_target}. It does no damage, as expected.]\n```",
		str_equip="```ini\n[You get a nice mug to dip your little paintbrush in, and open your 12 set of watercolors. Look out world, here comes you!]\n```",
		str_name="watercolors",
		str_weapon="a set of watercolors",
		str_weaponmaster_self="You are a rank {rank} flaming homosexual of watercolors.",
		str_weaponmaster="They are a rank {rank} flaming homosexual of watercolors.",
		# str_trauma_self = "You are eternally humiliated after being murdered by a gangster wielding watercolor paints.",
		# str_trauma = "They are eternally humiliated after being murdered by a gangster wielding watercolor paints.",
		str_kill="```bash\n\"HUUUUUUH?? {name_target} goes and kills themselves after having an existential crisis! {name_player} seems to have done this with only their own retardation!\"\n```",
		str_killdescriptor="driven to suicide",
		str_damage="```ini\n[{name_player} paints a picture of {name_target}. Their self esteem takes a hit!]\n```",
		str_duel="```json\n\"{name_player} and {name_target} practice art using Dojo-owned easels and canvases. Eventually, the training session breaks down and, you just throw paint water at each other and giggle like schoolgirls.\"\n```",
		str_scalp="The scalp is perfectly intact.",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		str_description="A 12 pack of watercolors, the kind you used when you were a 5 years old boy.",
		vendors=[vendor_basedhardware, vendor_breakroom],
		stat=stat_watercolor_kills,
		classes=[weapon_class_paint, weapon_class_captcha],
		#sap_cost=2,
		price = 1300,
		captcha_length=3,
		is_tool=1,
		# str_backfire = "{name_player} has the idea of trying to paint their parents fucking, thinking it will be really funny and everyone will love them. Pretty soon we're going to have to ban watercolors because people like you are using them to molest yourself.",
		tool_props = {
			'reg_spray' : "Nice drawing, {curse}! ",
			'miss_spray' : "**Miss!** Your painting sucks. God, you're stupid. ",
			'crit_spray' : "After the thousandth failed watercolor gesamtkunstwerk you decide enough is enough. Fuck this. Fuck the gangs, fuck the violence, fuck the perpetually rotting lets player that compels you to rigor mortis yourself more frequently than you eat breakfast. The spite is so concentrated that it compels you to turn your life around. You get a fake ID, join the PTA, and rope them into cleaning every last inch of this district until the homeless population smell like citrus and give out free, non-tainted lollipops. However, your newfound peaceful life is interrupted by the night terrors ENDLESS WAR now gives you on a daily basis, and you decide to go back to being a gangster. You suppose some things never change.",
			'equip_spray' : "You get out your 12 pack of watercolors. Can't believe you have to use one of these."
		}
	),
	EwWeapon(  # 29
		id_weapon=weapon_id_thinnerbomb,
		alias=[
			"thinner",
			"thinnerbombs"
		],
		str_crit="**Critical hit!!** {name_player} slams {name_target} with a bottle of paint thinner, showering their face with broken glass and getting some of the thinner down their gullet. They fall back, dazed and bleeding.",
		str_miss="**MISS!!** {name_player} is too dazed by their own chemicals to make a move! They drop the bottle on accident, throwing vapors all over the place.",
		str_equip="You pull out the thinner bombs and hold their bottlenecks between your fingers. Never has a not-weapon ever felt so cool.",
		str_name="thinner bombs",
		str_weapon="thinner bombs",
		str_weaponmaster_self="You are a rank {rank} vandal of the thinner bomb.",
		str_weaponmaster="They are a rank {rank} vandal of the thinner bomb.",
		# str_trauma_self = "You have the hangover from hell.",
		# str_trauma = "They have the hangover from hell.",
		str_kill="***WHAT A SIZZLER!*** {name_target}, dazed from the concentrated toxic chemicals in the air, falls to the ground, giving {name_player} the chance to stab them through the neck with the broken bottle. Inhalants. Not even once. {emote_skull}",
		str_killdescriptor="drugged",
		str_damage=random.choice(["{name_target} gets a thinnerbomb to the {hitzone}!!",
								  "{name_player} slashes {name_target} with a broken thinnerbomb! Ooh, right in the {hitzone}!!"]),
		str_duel="{name_player} and {name_target} build a resistance to the noxious chemicals they're using by drinking paint thinner together. Cheers.",
		str_scalp="The scalp smells awful, you can hardly hold it.",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		str_description="A pack of brittle glass bottles filled with paint thinner. This stuff vaporizes like nobody's business, and could strip the osmotic membrane off a slimeoid.",
		vendors=[vendor_basedhardware, vendor_breakroom],
		stat=stat_thinnerbomb_kills,
		classes=[weapon_class_paint, weapon_class_captcha],
		#sap_cost=2,
		price = 15000,
		captcha_length=4,
		is_tool = 1,
		# str_backfire = "You haven't had a good buzz in awhile, so you take a whiff of one of your thinner bombs. Great trip and all, but you rough yourself up convulsing on the ground while it happens.",
		tool_props = {
		'reg_spray' : "You find a vandalized wall and toss a thinner bomb on it! You hear a faint sizzling as paint begins to strip off the walls. Sick!",
		'miss_spray' : "**Miss!** You make a mistake on the throw's distance and it bursts uselessly on the ground. You got to do some littering, so at least there's that.",
		'crit_spray' : "**Critical hit!** You take out a paint bomb and throw it at a particularly fragile looking building. The chemicals you used were so caustic that they burned a hole through the whole wall, preventing anyone from painting it for all of time!",
		'equip_spray' : "You get your glass thinner bombs out you you can throw them in a moment's notice."
	}),
	EwWeapon( # 30
		id_weapon = weapon_id_staff,
		alias = [
			"eldritchstaff",
			"spookystaff",
			"reprehensiblerod",
			"wickedwand",
			"frighteningfaggot"
		],
		str_miss = "Your mind goes blank as you feel slime disappear from your body in preparation for a deadly attack.",
		str_damage = "{name_player} finalizes their invocation. " + random.choice([
			"Gravity violently increases in the space around {name_target}, slamming them into the ground.", 
			"A blinding white light shines from {name_target}'s {hitzone} as it burns hotter than the surface of the sun.", 
			"Spectral hands caress {name_target}'s body, leaving gaping wounds in their path.", 
			"An unseen force suddenly yoinks {name_target} by their {hitzone}, sending them flying into the air.",
			"A pitch black horror forms around {name_target}'s {hitzone} and tears into it."
		]),
		str_crit = "{name_player} notices {name_target} still recoiling from the damage, and takes the chance to bonk the everliving shit out of them with their staff. **Critical hit!!**",
		str_kill = "A mass of tiny hands erupts from the ground below {name_target}, grabbing on to their body. Their screams echo across the streets as they're dragged through the ground and into the sewers.",
		str_equip = "You equip the eldritch staff.",
		str_name = "eldritch staff",
		str_weapon = "an eldritch staff",
		str_weaponmaster_self = "You are a rank {rank} conduit of the ones below.",
		str_weaponmaster = "They are a rank {rank} conduit of the ones below.",
		str_killdescriptor = "cast down",
		str_duel = "{name_player} and {name_target} compare notes on their understanding of the eldritch fuckery they've each experienced.",
		str_description = "An intricate wooden staff with a cloudy crystal on its handle. It looks fucking class, but it also gives you the creeps.",
		str_scalp = "It's covered in symbols written with a strange black substance.",
		fn_effect = wef_staff,
		acquisition = acquisition_smelting,
		stat = stat_staff_kills,
		#sap_cost = 2,
		captcha_length = 10,
	),
	EwWeapon( # 31
		id_weapon = weapon_id_hoe,
		str_miss = "**MISS!!** {name_player}'s hoe strikes the earth with a loud THUD.",
		str_damage = "{name_player} scrapes their hoe across {name_target}'s {hitzone}.",
		str_crit = "**CRITICAL HIT!!** {name_player} gets their hoe deep into {name_target}'s body, cutting up their vitals!",
		str_kill = "{name_player} pushes {name_target} to the ground. After an intense windup, they slam their hoe down on {name_target}'s neck, decapitating them in the process.",
		str_equip = "You ready your hoe.",
		str_name = "hoe",
		str_weapon = "a hoe",
		str_weaponmaster_self = "You are a rank {rank} farmer.",
		str_weaponmaster = "They are a rank {rank} farmer.",
		str_killdescriptor = "!reaped",
		str_duel = "{name_player} and {name_target} discuss their latest harvest and exchange farming tips.",
		str_description = "It's a farming hoe.",
		str_scalp = "It's covered in dirt.",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		price = 100000,
		vendors = [vendor_atomicforest],
		classes = [weapon_class_farming, weapon_class_juvie],
		stat = stat_hoe_kills,
		#sap_cost = 2,
		captcha_length = 2,
		is_tool = 1,
	),
	EwWeapon( # 32
		id_weapon = weapon_id_pitchfork,
		str_miss = "**MISS!!** {name_player}'s pitchfork is planted firmly into the ground.",
		str_damage = "{name_player} stabs {name_target}'s {hitzone} with their pitchfork!",
		str_crit = "**CRITICAL HIT!!** {name_player} pokes several holes in {name_target}!",
		str_kill = "{name_player} plants their pitchfork firmly into {name_target} and lifts them high into the air. After {name_target} loses consciousness, {name_target} throws them to the ground.",
		str_equip = "You pick up your pitchfork and give the ground a light tap with the handle's end.",
		str_name = "pitchfork",
		str_weapon = "a pitchfork",
		str_weaponmaster_self = "You are a rank {rank} farmer.",
		str_weaponmaster = "They are a rank {rank} farmer.",
		str_killdescriptor = "!reaped",
		str_duel = "{name_player} and {name_target} joust with their pithforks. Thankfully, no one gets hurt in the process.",
		str_description = "It's a farming pitchfork.",
		str_scalp = "It's got three holes in it.",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		price = 100000,
		vendors = [vendor_atomicforest],
		classes = [weapon_class_farming, weapon_class_juvie],
		stat = stat_pitchfork_kills,
		#sap_cost = 2,
		captcha_length = 2,
		is_tool = 1,
	),
	EwWeapon( # 33 
		id_weapon = weapon_id_shovel,
		str_miss = "**MISS!!** {name_player}'s shovel is planted firmly into the ground.",
		str_damage = "{name_player} swings their shovel at {name_target}'s {hitzone}!",
		str_crit = "**CRITICAL HIT!** The flat end of {name_player}'s shovel impacts {name_target}'s chest! They start coughing up blood!",
		str_kill = "*BONK!* {name_player}'s shovel lands right on top of {name_target}'s head. Their skull and brain is completely crushed by the impact. {name_player} buries them in a shallow grave.",
		str_equip = "You grip your shovel tightly in both hands.",
		str_name = "shovel",
		str_weapon = "a shovel",
		str_weaponmaster_self = "You are a rank {rank} farmer.",
		str_weaponmaster = "They are a rank {rank} farmer.",
		str_killdescriptor = "!digged",
		str_duel = "{name_player} and {name_target} perform a high-shovel. The moment could not be more perfect.",
		str_description = "It's a shovel.",
		str_scalp = "It's flattened.",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		price = 100000,
		vendors = [vendor_atomicforest],
		classes = [weapon_class_juvie],
		stat = stat_shovel_kills,
		#sap_cost = 2,
		captcha_length = 2,
		is_tool = 1,
	),
	EwWeapon( # 34 
		id_weapon = weapon_id_slimeringcan,
		str_miss = "**MISS!!** Spouts of slime from {name_players} Slimering Can fly everywhere!",
		str_damage = "{name_player} pours slime onto {name_target}'s {hitzone}. What the fuck is that going to accomplish?",
		str_crit = "**CRITIAL HIT!!** {name_player} pours slime onto {name_target}'s eyes! How unsanitary!",
		str_kill = "{name_player} rams their Slimering Can down {name_target}'s throat. {name_target} chokes to death on slime.",
		str_equip = "You pick up your Slimering Can.",
		str_name = "slimering can",
		str_weapon = "a slimering can",
		str_weaponmaster_self = "You are a rank {rank} green thumbed coward.",
		str_weaponmaster = "They are a rank {rank} green thumbed coward.",
		str_killdescriptor = "drowned",
		str_duel = "{name_player} and {name_target} water flowers together. Sometimes it's nice to be a fucking weak willed coward, y'know?",
		str_description = "It's a slimering can.",
		str_scalp = "It's soaking wet.",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		price = 100000,
		vendors = [vendor_atomicforest],
		classes = [weapon_class_juvie],
		stat = stat_slimeringcan_kills,
		#sap_cost = 2,
		captcha_length = 2,
		is_tool = 1,
	),
    EwWeapon(  # 35
        id_weapon=weapon_id_fingernails,
        alias=[
            "fingernails",
            "nails"
        ],
        str_crit="**Critical hit!!** {name_target} is cut deep!!",
        str_miss="",
        str_equip="",
        str_name="fingernails",
        str_weapon="their fingernails",
        str_weaponmaster_self="",
        str_weaponmaster="",
        # str_trauma_self = "A single clean scar runs across the entire length of your body.",
        # str_trauma = "A single clean scar runs across the entire length of their body.",
        str_kill="{name_player} lunges at {name_target} with fingernails bared! They're mercilessly rips them to pieces, tufts of skin flying every which way! **BRRRRRRRAP!!!** When the dust settles, {name_target} is unrecognizable, and more importantly, dead as fuck. {emote_skull}",
        str_killdescriptor="torn apart",
        str_damage="{name_target} is slashed across the {hitzone}!!",
        str_duel="",
        str_description="",
        str_scalp=" Multiple slash marks run across it.",
        fn_effect=wef_fingernails,
        price=0,
        vendors=[],
        classes=[],
        stat=stat_fingernails_kills,
        # sap_cost = 3,
        captcha_length=8
    ),
	EwWeapon(  # 35
		id_weapon=weapon_id_roomba,
		alias=[
			"roomba",
			"vaccuum"
		],
		str_crit="**Critical hit!!** {name_target} gets a concussion via roomba to the face!!",
		str_miss="**MISS!** The roomba forgets where it is and begins tripping around!",
		str_equip="You turn on your Roomba and place it on the ground.",
		str_name="roomba",
		str_weapon="a roomba",
		str_weaponmaster_self="You are a rank {rank} roomba acolyte.",
		str_weaponmaster="They are a rank {rank} roomba acolyte.",
		# str_trauma_self = "A single clean scar runs across the entire length of your body.",
		# str_trauma = "A single clean scar runs across the entire length of their body.",
		str_kill="{name_player} jumps at {name_target} using the roomba as a springboard! Screaming bloody murder, they beat {name_target} to within an inch of their life. The roomba follows, sucking whatever morsel of slime was left. Job finished. {emote_skull}",
		str_killdescriptor="sucked dry",
		str_damage="{name_player}'s roomba sucks gobs of slime out of {name_target}'s {hitzone}!!",
		str_duel="{name_player} and {name_target} begin engineering their portable vaccums into high class battle bots. By the time you're done the Dojo floor is spotless and everyone nearby is dead.",
		str_description="It's a high powered portable vaccuum designed to clean up dust. You use it to spread paint around by attaching a spray can to the back.",
		str_scalp=" It looks stretched and wrinkled.",
		fn_effect = get_normal_attack(weapon_type = 'tool'),
		price=40000,
		# str_backfire="You roomba turns on you! Its shitty AI thinks your feet are its prey, and it sucks away some precious slime!",
		vendors=[vendor_basedhardware],
		classes=[weapon_class_paint, weapon_class_captcha],
		stat=stat_fingernails_kills,
		# sap_cost = 3,
		captcha_length=8,
		tool_props = {
		'reg_spray' : "The roomba continues its intrepid journey spraying paint around town.",
		'miss_spray' : "**Miss!** Fuck, the thing got stuck on a pothole again.",
		'crit_spray' : "**Critical hit!** A bystander walking by kicks your roomba as it's moving, which inadvertently overclocks its processor!! It speeds around the area with reckless abandon. Go go go!",
		'equip_spray' : "You pull out your roomba and set it on the ground."
	}
	),
	EwWeapon(  # 36
		id_weapon=weapon_id_laywaster,
		alias=[
			"chainsaw",
			"megachainsaw",
			"widowmaker",
			"jessica"
		],
		str_crit="**Critical Hit!** {name_player} snaps {name_target} between two of the sawblades, ripping mercilessly into flesh and nearly vaporizing the spraying blood!",
		str_miss="**Miss!** {name_player} swings the heavy blade around and hits nothing but air.",
		str_equip="You rev up the Laywaster 9000.",
		str_name="multiblade chainsaw",
		str_weapon="a multiblade chainsaw",
		str_weaponmaster_self="You are a rank {rank} master of the Laywaster 9000.",
		str_weaponmaster="They are a rank {rank} master of the Laywaster 9000.",
		# str_trauma_self = "You have a few large, gaping holes in your abdomen. Someone could stick their arm through the biggest one.",
		# str_trauma = "They have a few large, gaping holes in your abdomen. Someone could stick their arm through the biggest one.",
		str_kill="**VRRRRRRRRRRRRRRRRRRRRRRRRRRRR!**{name_player} swings violently through {name_target}'s unconscious body, each slash making them more unrecognizable than the last. As more and more blood flecks across {name_player}'s face, their opponent turns into a pile of viscera. {emote_skull}",
		str_killdescriptor="shredded to a paste",
		str_damage="{name_target}'s {hitzone} is torn into!! Blood flies everywhere!",
		str_duel="**...** {name_player} and {name_target} clash with each other chainsaw blow for chainsaw blow like badasses.",
		str_description="It's a multi-bladed chainsaw.",
		str_scalp=" It's not really a scalp anymore, more of a paste.",
		fn_effect=get_normal_attack(weapon_type='heavy'),
		price=1000000,
		vendors=[],
		classes=[],
		stat=stat_megachainsaw_kills,
	),
EwWeapon( # 37
		id_weapon = weapon_id_chainsaw,
		alias = [
			"ripper",
			"motoraxe"
		],
		str_crit = "**Critical hit!!** The jagged teeth of the chainsaw rest within {name_target}, body as the slime flies!!",
		str_miss = "**You missed!!** In {name_player}’s excitement and desperation neither chain nor saw hits {name_target}!",
		str_equip = "You equip the chainsaw.",
		str_name = "chainsaw",
		str_weapon = "a chainsaw",
		str_weaponmaster_self = "You are a rank {rank} wielder of the chainsaw.",
		str_weaponmaster = "They are a rank {rank} wielder of the chainsaw.",
		#str_trauma_self = "Your body runs jagged with large chunks missing and patches of skin torn up.",
		#str_trauma = "Their body runs jagged with large chunks missing and patches of skin torn up.",
		str_kill = "**REEERNREERN!!** {name_player} revs up their chainsaw and carves up {name_target}’s torso, cutting through the guts,bile,viscera, and slime; sending it all flying. They’ve been cut down to size. {emote_skull}",
		str_killdescriptor = "chainsaw’d",
		str_damage = "The numerous finely tooth blades tear at {name_target}’s {hitzone}!!",
		str_duel = "**...** {name_player} and {name_target} clash with each other chainsaw blow for chainsaw blow like badasses.",
		str_description = "It's a chainsaw.",
		#str_reload = "You desperately pull at the ripcord of your chainsaw trying to rev it back up to speed.",
		#str_reload_warning = "**REEERNREERN--** *shhhhh…* **FUCK!!** {name_player}’s chainsaw just ran out of it’s rev!!",
		str_scalp = "It’s more like a collection of dandruff then a scalp.",
		fn_effect = get_normal_attack(weapon_type = 'heavy'),
		price = 1000000,
		vendors = [vendor_basedhardware],
		classes= [],
		stat = stat_chainsaw_kills,
		captcha_length = 4
	),

]

# A map of id_weapon to EwWeapon objects.
weapon_map = {}

# A list of weapon names
weapon_names = []

# Attacking type effects
def atf_fangs(ctn = None):
	# Reskin of dual pistols

	aim = (random.randrange(10) + 1)
	#ctn.sap_damage = 1

	if aim == (1 + int(10 * ctn.hit_chance_mod)):
		ctn.miss = True
		ctn.slimes_damage = 0
	elif aim == (10 - int(10 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage *= 2

def atf_talons(ctn = None):
	# Reskin of katana

	ctn.miss = False
	ctn.slimes_damage = int(0.85 * ctn.slimes_damage)
	#ctn.sap_damage = 0
	#ctn.sap_ignored = 10

	if (random.randrange(10) + 1) == (10 + int(10 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage *= 2.1

def atf_raiderscythe(ctn = None):
	# Reskin of scythe

	ctn.enemy_data.change_slime(n = (-ctn.slimes_spent * 0.33), source = source_self_damage)
	ctn.slimes_damage = int(ctn.slimes_damage * 1.25)
	aim = (random.randrange(10) + 1)
	#ctn.sap_damage = 0
	#ctn.sap_ignored = 5

	if aim <= (2 + int(10 * ctn.hit_chance_mod)):
		ctn.miss = True
		ctn.slimes_damage = 0
	elif aim >= (9 - int(10 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage *= 2

def atf_gunkshot(ctn = None):
	# Reskin of rifle

	aim = (random.randrange(10) + 1)
	#ctn.sap_damage = 2

	if aim <= (2 + int(10 * ctn.hit_chance_mod)):
		ctn.miss = True
		ctn.slimes_damage = 0
	elif aim >= (9 - int(10 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage *= 2

def atf_tusks(ctn = None):
	# Reskin of bat

	aim = (random.randrange(21) - 10)
	#ctn.sap_damage = 3
	if aim <= (-9 + int(21 * ctn.hit_chance_mod)):
		ctn.miss = True
		ctn.slimes_damage = 0

	ctn.slimes_damage = int(ctn.slimes_damage * (1 + (aim / 10)))

	if aim >= (9 - int(21 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage = int(ctn.slimes_damage * 1.5)

def atf_molotovbreath(ctn = None):
	# Reskin of molotov

	dmg = ctn.slimes_damage
	ctn.slimes_damage = int(ctn.slimes_damage * 0.75)
	#ctn.sap_damage = 0
	#ctn.sap_ignored = 10

	aim = (random.randrange(10) + 1)

	#ctn.bystander_damage = dmg * 0.5

	if aim == (3 + int(10 * ctn.hit_chance_mod)):
		ctn.miss = True
		ctn.slimes_damage = 0

	elif aim == (10 - int(10 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage *= 2

def atf_armcannon(ctn = None):
	dmg = ctn.slimes_damage
	#ctn.sap_damage = 2

	aim = (random.randrange(20) + 1)

	if aim <= (2 + int(20 * ctn.hit_chance_mod)):
		ctn.miss = True

	if aim == (20 - int(20 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage *= 3


def atf_axe(ctn=None):
	ctn.slimes_damage *= 0.7
	aim = (random.randrange(10) + 1)

	if aim <= (4 + int(10 * ctn.hit_chance_mod)):
		ctn.miss = True

	if aim == (10 - int(10 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage *= 2


def atf_hooves(ctn=None):
	ctn.slimes_damage *= 0.4
	aim = (random.randrange(30) + 1)

	if aim <= (5 + int(30 * ctn.hit_chance_mod)):
		ctn.miss = True

	if aim > (25 - int(30 * ctn.crit_mod)):
		ctn.crit = True
		ctn.slimes_damage *= 2
		
def atf_body(ctn=None):
	ctn.slimes_damage *= 0.5
	aim = (random.randrange(10) + 1)

	if aim <= 2:
		ctn.miss = True

	if aim == 10:
		ctn.crit = True
		ctn.slimes_damage *= 2
		
def atf_gvs_basic(ctn=None):
	pass

# All enemy attacking types in the game.
enemy_attack_type_list = [
	EwAttackType( # 1
		id_type = "fangs",
		str_crit = "**Critical Hit!** {name_enemy} sinks their teeth deep into {name_target}!",
		str_miss = "**{name_enemy} missed!** Their maw snaps shut!",
		#str_trauma_self = "You have bite marks littered throughout your body.",
		#str_trauma = "They have bite marks littered throughout their body.",
		str_kill = "{name_enemy} opens their jaw for one last bite right on {name_target}'s juicy neck. **CHOMP**. Blood gushes out of their arteries and onto the ground. {emote_skull}",
		str_killdescriptor = "mangled",
		str_damage = "{name_target} is bitten on the {hitzone}!!",
		fn_effect = atf_fangs
	),
	EwAttackType( # 2
		id_type = "talons",
		str_crit = "**Critical hit!!** {name_target} is slashed across the chest!!",
		str_miss = "**{name_enemy} missed!** Their wings flap in the air as they prepare for another strike!",
		#str_trauma_self = "A large section of scars litter your abdomen.",
		#str_trauma = "A large section of scars litter their abdomen.",
		str_kill = "In a fantastic display of avian savagery, {name_enemy}'s talons grip {name_target}'s stomach, rip open their flesh and tear their intestines to pieces. {emote_skull}",
		str_killdescriptor = "disembowled",
		str_damage = "{name_target} has their {hitzone} clawed at!!",
		fn_effect = atf_talons
	),
	EwAttackType( # 3
		id_type = "scythe",
		str_crit = "**Critical hit!!** {name_target} is carved by the wicked curved blade!",
		str_miss = "**MISS!!** {name_enemy}'s swings miss wide of the target!",
		#str_trauma_self = "You are wrapped tightly in bandages that hold your two halves together.",
		#str_trauma = "They are wrapped tightly in bandages that hold their two halves together.",
		str_kill = "**SLASHH!!** {name_enemy}'s scythe cleaves the air, and {name_target} staggers. A moment later, {name_target}'s torso topples off their waist. {emote_skull}",
		str_killdescriptor = "sliced in twain",
		str_damage = "{name_target} is cleaved through the {hitzone}!!",
		fn_effect = atf_raiderscythe
	),
	EwAttackType( # 4
		id_type = "gunkshot",
		str_crit = "**Critical hit!!** {name_target} is covered in a thick, gelatenous ooze!",
		str_miss = "**MISS!!** {name_enemy}'s gunk shot just barely missed the target!",
		#str_trauma_self = "Several locations on your body have decayed from the aftermath of horrific radiation.",
		#str_trauma = "Several locations on their body have decayed from the aftermath of horrific radiation.",
		str_kill = "**SPLOOSH!!** {name_enemy}'s gunk shot completely envelops {name_target}, boiling their flesh alive in a radiation that rivals the Elephant's Foot. Nothing but a charred husk remains. {emote_skull}",
		str_killdescriptor = "slimed on",
		str_damage = "{name_target} is coated in searing, acidic radiation on their {hitzone}!!",
		fn_effect = atf_gunkshot
	),
	EwAttackType( # 5
		id_type = "tusks",
		str_crit = "**Critical hit!!** {name_target} is smashed hard by {name_enemy}'s tusks!",
		str_miss = "**{name_enemy} missed!** Their tusks strike the ground, causing it to quake underneath!",
		#str_trauma_self = "You have one large scarred-over hole on your upper body.",
		#str_trauma = "They have one large scarred-over hole on their upper body.",
		str_kill = "**SHINK!!** {name_enemy}'s tusk rams right into your chest, impaling you right through your back! Moments later, you're thrusted out on to the ground, left to bleed profusely. {emote_skull}",
		str_killdescriptor = "pierced",
		str_damage = "{name_target} has tusks slammed into their {hitzone}!!",
		fn_effect = atf_tusks
	),
	EwAttackType( # 6
		id_type = "molotovbreath",
		# str_backfire = "**Oh the humanity!!** {name_enemy} tries to let out a breath of fire, but it combusts while still inside their maw!!",
		str_crit = "**Critical hit!!** {name_target} is char grilled by {name_enemy}'s barrage of molotov breath!",
		str_miss = "**{name_enemy} missed!** Their shot hits the ground instead, causing embers to shoot out in all directions!",
		#str_trauma_self = "You're wrapped in two layers of bandages. What skin is showing appears burn-scarred.",
		#str_trauma = "They're wrapped in two layers of bandages. What skin is showing appears burn-scarred.",
		str_kill = "In a last ditch effort, {name_enemy} breathes in deeply for an extra powerful shot of fire. Before you know it, your body is cooked alive like a rotisserie chicken. {emote_skull}",
		str_killdescriptor = "exploded",
		str_damage = "{name_target} is hit by a blast of fire on their {hitzone}!!",
		fn_effect = atf_molotovbreath
	),
	EwAttackType( # 7
		id_type = "armcannon",
		str_crit = "**Critical hit!!** {name_target} has a clean hole shot through their chest by {name_enemy}'s bullet!",
		str_miss = "**{name_enemy} missed their target!** The stray bullet cleaves right into the ground!",
		#str_trauma_self = "There's a deep bruising right in the middle of your forehead.",
		#str_trauma = "There's a deep bruising right in the middle of their forehead.",
		str_kill = "{name_enemy} readies their crosshair right for your head and fires without hesitation. The force from the bullet is so powerful that when it lodges itself into your skull, it rips your head right off in the process. {emote_skull}",
		str_killdescriptor = "sniped",
		str_damage = "{name_target} has a bullet zoom right through their {hitzone}!!",
		fn_effect = atf_armcannon
	),
	EwAttackType( # 8
		id_type = "axe",
		str_crit = "**Critical hit!!** {name_target} is thoroughly cleaved by {name_enemy}'s axe!",
		str_miss = "**{name_enemy} missed!** The axe gives a loud **THUD** as it strikes the earth!",
		#str_trauma_self = "There's a hefty amount of bandages covering the top of your head",
		#str_trauma = "There's a hefty amount of bandages covering the top of their head",
		str_kill = "{name_enemy} lifts up their axe for one last swing. The wicked edge buries itself deep into your skull, cutting your brain in twain. {emote_skull}",
		str_killdescriptor = "axed",
		str_damage = "{name_target} is swung at right on their {hitzone}!!",
		fn_effect = atf_axe
	),
	EwAttackType( # 9
		id_type = "hooves",
		str_crit = "**Critical hit!!** {name_enemy} lays a savage hind-leg kick into {name_target}'s chest!",
		str_miss = "**WHOOSH!** {name_enemy}'s hooves just barely miss you!",
		#str_trauma_self = "Your chest is somewhat concave.",
		#str_trauma = "Their chest is somewhat concave.",
		str_kill = "{name_enemy} gallops right over your head, readying their hind legs just after landing. Before you can even ready your weapon, their legs are already planted right onto your chest. Your heart explodes. {emote_skull}",
		str_killdescriptor = "stomped",
		str_damage = "{name_target} is stomped all over their {hitzone}!!",
		fn_effect = atf_hooves
	),
	EwAttackType( # 10
		id_type = "body",
		str_crit = "**OOF!!** {name_enemy} lands a critical strike onto {name_target}'s torso with the sheer impact of their body weight!",
		str_miss = "**MISS!** {name_enemy} flails their body around to try and attack {name_target}, but nothing happens...",
		#str_trauma_self = "Your have deep bruising on your torso.",
		#str_trauma = "They have deep bruising on their torso.",
		str_kill = "{name_enemy} throws every once of force they can at you with your body. The impact is so strong that you're slammed into the ground, shattering your skull. {emote_skull}",
		str_killdescriptor = "pushed around",
		str_damage = "{name_target} gets bumped around a bit on their {hitzone}!",
		fn_effect = atf_body
	),
	EwAttackType(  # 11
		id_type="amateur",
		str_crit="**AIIIIEEE!!** {name_enemy} screams in abject fear, lunging at {name_target}'s with a {civ_weapon} in hand! Fuck, they actually got you!",
		str_miss="**MISS!** {name_enemy} trips and falls facefirst on the ground. {name_target} is holding back their laughter at how goddamn stupid this all is.",
		# str_trauma_self = "Your have deep bruising on your torso.",
		# str_trauma = "They have deep bruising on their torso.",
		str_kill="{name_enemy} is thrown into an adrenaline rush! They brandish their {civ_weapon} and throw it in a perfect spiral, directly through {name_target}'s skull. {emote_skull}",
		str_killdescriptor="felled",
		str_damage="{name_enemy} bludgeons {name_target} in the {hitzone}! At least they try to...",
		fn_effect=atf_body
	),
	# If str_trauma and str_trauma_self make a return, consider filling GvS attacktypes out in these attributes.
	EwAttackType( # GvS - 1
		id_type = "g_seeds",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy}'s seeds completely miss {name_target}!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "{name_enemy}'s seeds land right inside {name_target}'s skull, killing them instantly. {emote_skull}",
		str_killdescriptor = "seeded",
		str_damage = "{name_target} is pummeled with seeds on their {hitzone}!",
		str_groupattack = "{name_target} pummels a whole group of shamblers with their seeds!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 1.5
			id_type = "g_appleacid",
			str_crit = "NULL",
			str_miss = "**MISS!** {name_enemy}'s acid completely misses {name_target}!",
			#str_trauma_self = "NULL", 
			#str_trauma = "NULL,
			str_kill = "{name_enemy} hurls a glob of acid straight onto {name_target}'s chest, melting down their insides. {emote_skull}",
			str_killdescriptor = "melted down to the bone",
			str_damage = "{name_target} is drenched with acid on their {hitzone}!",
			str_groupattack = "{name_target} drenches a group of shamblers with their acid!",
			fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 2
		id_type = "g_bloodshot",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy}'s bloodshot dissipates in mid-air as it fails to seek out {name_target}!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "{name_enemy} turns {name_target} into a shriveled up husk! {emote_skull}",
		str_killdescriptor = "drained",
		str_damage = "{name_target} has their life essence drained away by {name_enemy}!",
		str_groupattack = "{name_enemy} sucks the life force out of a group of shamblers!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 3
		id_type = "g_nuts",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy}'s nuts don't even come close to hitting {name_target}!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "{name_enemy}'s nuts knock {name_target}'s head clean off! {emote_skull}",
		str_killdescriptor = "conked on the head",
		str_damage = "{name_enemy}'s nuts bonk {name_target} on their {hitzone}!",
		str_groupattack = "{name_enemy}'s nuts richochet off of a group of shamblers!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 4
		id_type = "g_chompers",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy}'s gaping maw snaps shut!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "**CHOMP!** {name_enemy} devours {name_target}, killing them instantly. {emote_skull}",
		str_killdescriptor = "chomped",
		str_damage = "{name_enemy}'s chompers take a bite out of {name_target}!",
		str_groupattack = "{name_enemy} is running wild!! Their chompers lay waste to a group of shamblers!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 5
		id_type = "g_fists",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy} thrashes about, but fails to hit {name_target}.",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "{name_enemy} deals a devastating strike to {name_target}! The impact causes their heart to stop. {emote_skull}",
		str_killdescriptor = "punched to death",
		str_damage = "{name_enemy}'s fists deal savage blows to {name_target}!",
		str_groupattack = "{name_enemy} rushes down a group of shamblers with their fists!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 6
		id_type = "g_brainwaves",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy}'s Binaural Brainwaves completely miss {name_target}!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "{name_enemy} hypnotizes {name_target} into walking off of the Slime's End cliffs. {emote_skull}",
		str_killdescriptor = "mind broken",
		str_damage = "{name_enemy}'s Binaural Brainwaves give {name_target} a massive headache!",
		str_groupattack = "{name_enemy} is firing on all cylinders! Their Binaural Brainwaves impact multiple shamblers!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 7
		id_type = "g_vapecloud",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_target} completely avoids {name_enemy}'s vape cloud!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "{name_target} has inhaled too much of {name_enemy}'s toxic vape cloud! {emote_skull}",
		str_killdescriptor = "vaped to death",
		str_damage = "{name_enemy} completely covers {name_target} in a toxic vape cloud!",
		str_groupattack = "{name_enemy} spreads its toxic vape cloud to a group of shamblers!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 8
		id_type = "g_hotbox",
		str_crit = "NULL",
		str_miss = "**MISS!** weed",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = " {emote_skull}",
		str_killdescriptor = "forced to smoke too much weed",
		str_damage = "weed",
		str_groupattack = "weed",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 9
		id_type = "g_blades",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_target} manages to avoid getting cut on {name_enemy}'s blades!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "**SHINK!!** {name_enemy}'s blades sink deep into {name_target}! {emote_skull}",
		str_killdescriptor = "cut and stabbed",
		str_damage = "{name_enemy} cuts {name_target} with their sharpened blades!",
		str_groupattack = "{name_enemy} slices and dices a group of shamblers with their blades!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 10
		id_type = "g_explosion",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy}'s explosion doesn't even come close to hitting {name_target}!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "**KABOOM!!** {name_enemy} sacrifices itself to blow {name_target} apart! {emote_skull}",
		str_killdescriptor = "blown to smithereens",
		str_damage = "*BOOM!* {name_enemy}'s explosion puts a dent into {name_target}!",
		str_groupattack = "{name_enemy} takes down a group of shamblers with it!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 11
		id_type = "s_shamboni",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy} drives right past {name_target}!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "{name_enemy}'s wheels completely flatten {name_target}! {emote_skull}",
		str_killdescriptor = "run over",
		str_damage = "{name_enemy}'s wheels run over {name_target}!",
		str_groupattack = "{name_enemy} runs over a group of gaiaslimeoids!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 12
		id_type = "s_teeth",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy}'s bite doesn't even graze {name_target}!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "**CRUNCH!** {name_enemy} devours {name_target} with their teeth! {emote_skull}",
		str_killdescriptor = "bitten all over",
		str_damage = "{name_enemy} bites {name_target} on their {hitzone}!",
		str_groupattack = "{name_enemy}'s appetite knows no bounds! They bite into several gaiaslimeoids!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 13
		id_type = "s_tusks",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_targets}'s tusks fail to hit {name_target}, and give a loud *THUD* as they strike the ground!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "**SLAM!** {name_target} is flattened by {name_enemy}'s tusks. {emote_skull}",
		str_killdescriptor = "slammed into the ground",
		str_damage = "{name_enemy} bashes {name_target}'s {hitzone} with their tusks!",
		str_groupattack = "{name_enemy} slams its tusks into several gaiaslimeoids!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 14
		id_type = "s_fangs",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy}'s jaws snap shut! It failed to eat {name_target}!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "**GULP!** {name_enemy} swallows {name_target} whole! {emote_skull}",
		str_killdescriptor = "vored to death",
		str_damage = "",
		str_groupattack = "NULL",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 15
		id_type = "s_talons",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy} couldn't get a grip on {name_target}!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "**YOINK!** {name_enemy} picks up {name_target} and carries them off into the sunset... {emote_skull}",
		str_killdescriptor = "spirited away",
		str_damage = "**SLASH!** {name_enemy} couldn't carry {name_target} away, but scratched them up nonetheless!",
		str_groupattack = "{name_enemy} attacks a group of gaiaslimeoids with their talons!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 16
		id_type = "s_molotovbreath",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_target} managed to avoid {name_enemy}'s hellfire!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "**FWOOOOOOOSHHHHH!!** {name_enemy} burns {name_target} to a crisp! {emote_skull}",
		str_killdescriptor = "burnt to ash",
		str_damage = "{name_enemy} spits a ball of fire at {name_target} and burns their {hitzone}!",
		str_groupattack = "{name_enemy} absolutely incinerates a group of gaiaslimeoids with their molotov breath!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 17
		id_type = "s_cudgel",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy}'s cudgel misses {name_target} and goes down with a *THUD*.",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "**OOF!!** {name_enemy}'s cudgel whacks {name_target} so hard, it buries them far beneath the ground. {emote_skull}",
		str_killdescriptor = "flattened",
		str_damage = "**BAM!** {name_enemy} strikes {name_target}'s {hitzone} with their cudgel!",
		str_groupattack = "NULL",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 18
		id_type = "s_raiderscythe",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy}'s scythe breezes past {name_target}!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "{name_enemy} cleaves {name_target} in two. {emote_skull}",
		str_killdescriptor = "cut in twain",
		str_damage = "{name_enemy} slices {name_target} with its scythe!",
		str_groupattack = "{name_enemy} slashes a group of gaiaslimeoids with its scythe!",
		fn_effect = atf_gvs_basic
	),
	EwAttackType( # GvS - 19
		id_type = "s_grenadecannon",
		str_crit = "NULL",
		str_miss = "**MISS!** {name_enemy} couldn't land a hit on {name_target} with its grenade cannon!",
		#str_trauma_self = "NULL", 
		#str_trauma = "NULL,
		str_kill = "**KABAM!!** {name_enemy}'s grenade cannon lands a direct hit on {name_target}! {emote_skull}",
		str_killdescriptor = "blown apart",
		str_damage = "{name_target} is caught in the blast zone of {name_enemy}'s grenades!",
		str_groupattack = "{name_enemy} blows up a group of gaiaslimeoids with its grenades!",
		fn_effect = atf_gvs_basic
	),
]

# A map of id_type to EwAttackType objects.
attack_type_map = {}

# Populate attack type map.
for attack_type in enemy_attack_type_list:
	attack_type_map[attack_type.id_type] = attack_type

# Weather IDs
weather_sunny = "sunny"
weather_rainy = "rainy"
weather_windy = "windy"
weather_lightning = "lightning"
weather_cloudy = "cloudy"
weather_snow = "snow"
weather_foggy = "foggy"
weather_bicarbonaterain = "bicarbonaterain"

# All weather effects in the game.
weather_list = [
	EwWeather(
		name = weather_sunny,
		sunrise = "The smog is beginning to clear in the sickly morning sunlight.",
		day = "The sun is blazing on the cracked streets, making the air shimmer.",
		sunset = "The sky is darkening, the low clouds an iridescent orange.",
		night = "The moon looms yellow as factories belch smoke all through the night."
	),
	EwWeather(
		name = weather_rainy,
		sunrise = "Rain gently beats against the pavement as the sky starts to lighten.",
		day = "Rain pours down, collecting in oily rivers that run down sewer drains.",
		sunset = "Distant thunder rumbles as it rains, the sky now growing dark.",
		night = "Silverish clouds hide the moon, and the night is black in the heavy rain."
	),
	EwWeather(
		name = weather_windy,
		sunrise = "Wind whips through the city streets as the sun crests over the horizon.",
		day = "Paper and debris are whipped through the city streets by the winds, buffetting pedestrians.",
		sunset = "The few trees in the city bend and strain in the wind as the sun slowly sets.",
		night = "The dark streets howl, battering apartment windows with vicious night winds."
	),
	EwWeather(
		name = weather_lightning,
		sunrise = "An ill-omened morning dawns as lighting streaks across the sky in the sunrise.",
		day = "Flashes of bright lightning and peals of thunder periodically startle the citizens out of their usual stupor.",
		sunset = "Bluish white arcs of electricity tear through the deep red dusky sky.",
		night = "The dark night periodically lit with bright whitish-green bolts that flash off the metal and glass of the skyscrapers."
	),
	EwWeather(
		name = weather_cloudy,
		sunrise = "The dim morning light spreads timidly across the thickly clouded sky.",
		day = "The air hangs thick, and the pavement is damp with mist from the clouds overhead.",
		sunset = "The dusky light blares angry red on a sky choked with clouds and smog.",
		night = "Everything is dark and still but the roiling clouds, reflecting the city's eerie light."
	),
	EwWeather(
		name = weather_snow,
		sunrise = "The morning sun glints off the thin layer or powdery snow that blankets the city.",
		day = "Flakes of snow clump together and whip through the bitter cold air in the winder wind.",
		sunset = "The cold air grows colder as the sky darkens and the snow piles higher in the streets.",
		night = "Icy winds whip through the city, white snowflakes glittering in the black of night."
	),
	EwWeather(
		name = weather_foggy,
		sunrise = "Fog hangs thick in the air, stubbornly refusing to dissipate as the sun clears the horizon.",
		day = "You can barely see to the next block in the sickly greenish NLAC smog.",
		sunset = "Visibility only grows worse in the fog as the sun sets and the daylight fades.",
		night = "Everything is obscured by the darkness of night and the thick city smog."
	),
	# EwWeather(
	#  	name = weather_bicarbonaterain,
	#  	sunrise = "Accursed bicarbonate soda and sugar rain blocks out the morning sun.",
	#  	day = "The bicarbonate rain won't let up. That blue weasel is going to pay for this.",
	#  	sunset = "The deadly rain keeps beating down mercilessly. You have a feeling it's going to be a long night.",
	#  	night = "Clouds of doom obscure the moon as they dispense liquid death from above."
	# ),
]

# stock ids
stock_kfc = "kfc"
stock_pizzahut = "pizzahut"
stock_tacobell = "tacobell"

# default stock rates
default_stock_market_rate = 1000
default_stock_exchange_rate = 1000000


# A map of name to EwWeather objects.
weather_map = {}
for weather in weather_list:
	weather_map[weather.name] = weather


food_list = []
with open(os.path.join('json', 'food.json')) as f:
	foods = json.load(f)
	for i in foods:
		i = foods[i]
		food_list.append(
			EwFood(
				id_food = i['id_food'],						
				alias = i['alias'],							
				recover_hunger = i['recover_hunger'],		
				price = i['price'],							
				inebriation = i['inebriation'],				
				str_name = i['str_name'],					
				vendors = i['vendors'],						
				str_eat = i['str_eat'],						
				str_desc = i['str_desc'],					
				time_expir =  i['time_expir'],
				time_fridged =  i['time_fridged'],
				ingredients =  i['ingredients'],
				acquisition =  i['acquisition'],
				perishable =  i['perishable'],
			))						
		

# A map of id_food to EwFood objects.
food_map = {}

# A list of food names
food_names = []

# list of crops you're able to !reap
vegetable_list = []

# map of vegetables to their associated cosmetic material
vegetable_to_cosmetic_material = {}

# seperate the crops from the normal foods
for v in food_list:

	if vendor_farm not in v.vendors:
		pass
	else:
		if v.id_food in [item_id_direapples, item_id_brightshade, item_id_razornuts, item_id_steelbeans]:
			vegetable_to_cosmetic_material[v.id_food] = item_id_cool_material
		elif v.id_food in [item_id_pinkrowddishes, item_id_joybeans, item_id_purplekilliflower, item_id_suganmanuts]:
			vegetable_to_cosmetic_material[v.id_food] = item_id_cute_material
		elif v.id_food in [item_id_poketubers, item_id_dankwheat, item_id_blacklimes, item_id_aushucks]:
			vegetable_to_cosmetic_material[v.id_food] = item_id_beautiful_material
		elif v.id_food in [item_id_phosphorpoppies, item_id_pawpaw, item_id_sludgeberries, item_id_rustealeaves]:
			vegetable_to_cosmetic_material[v.id_food] = item_id_smart_material
		elif v.id_food in [item_id_sourpotatoes, item_id_bloodcabbages, item_id_pulpgourds, item_id_metallicaps]:
			vegetable_to_cosmetic_material[v.id_food] = item_id_tough_material

		vegetable_list.append(v)

candy_ids_list = []
for c in food_list:
	if c.acquisition == acquisition_trickortreating:
		candy_ids_list.append(c.id_food)
		

vendor_stock_map = {
	vendor_kfc : stock_kfc,
	vendor_pizzahut : stock_pizzahut,
	vendor_tacobell : stock_tacobell
	}

fish_rarity_common = "common"
fish_rarity_uncommon = "uncommon"
fish_rarity_rare = "rare"
fish_rarity_promo = "promo"

fish_catchtime_rain = "rain"
fish_catchtime_night = "night"
fish_catchtime_day = "day"

fish_slime_freshwater = "freshwater"
fish_slime_saltwater = "saltwater"
fish_slime_void = "void"

fish_size_miniscule = "miniscule"
fish_size_small = "small"
fish_size_average = "average"
fish_size_big = "big"
fish_size_huge = "huge"
fish_size_colossal = "colossal"

# All the fish, baby!
fish_list = []
with open(os.path.join('json', 'fish.json')) as f:
	fish = json.load(f)
	for i in fish:
		i = fish[i]
		fish_list.append(
			EwFish(
				id_fish = i['id_fish'],
				str_name = i['str_name'],
				size = i['size'],
				rarity = i['rarity'],
				catch_time = i['catch_time'],
				catch_weather = i['catch_weather'],
				str_desc = i['str_desc'],
				slime = i['slime'],
				vendors = i['vendors']
			))						
		


# A map of id_fish to EwFish objects.
fish_map = {}

# A list of fish names.
fish_names = []

bully_responses = [
	"You push {target_name} into a puddle of sludge, laughing at how hopelessly dirty they are.",
	"You hold {target_name} down and pull their underwear over their head. It looks like their neck's about to snap off, holy shit.",
	"You decide to give {target_name} a slime swirly in a nearby puddle. It's so shallow that they mostly get a faceful of gravel.",
	"You tie {target_name} to a tree and slap them around senselessly. You untie them once their face and belly bruise cherry red.",
	"You flag down a muscle car on the road and shout: \"HEY! {target_name} FUCKED YOUR WIFE!\" The good man parks on the side of the road and starts beating the everloving shit out them. {slimeoid} cowers in the corner, now scarred for life and afraid of dads.",
	"You pull on {target_name}'s hair, ripping some out and causing them to cry. They should fucking grow up.",
	"You reach into {target_name}'s shirt and give them a purple nurple. Man, these bullying tactics are getting kind of gay.",
	"You whip out your dick and pee on {target_name}'s wife. Fuck. That's a power move right there.",
	"You scream \"HEY {target_name}! NICE {cosmetic} YOU'RE WEARING! DID YOUR MOM BUY IT FOR YA?\"",
	"You grab {slimeoid} and give them a noogie. Just when {target_name} thinks this is all fun and games, you throw {slimeoid} into the street. They have a panic attack trying to get past all the traffic and back to safety."

]

makeshift_weapons = [
"stick",
"purse",
"dollar store pepper spray",
"backpack",
"cosplay katana",
"leather belt"
]

cabinets_list = [
"This is a Zoombinis Logical Journey arcade cabinet.\nWait. This is an old PC game. Why the fuck would they port this to cabinet? Now you have to use the stick to move the mouse around. Oh well. Buyers remorse, you suppose. \nhttps://classicreload.com/win3x-logical-journey-of-the-zoombinis.html",
"This is a Cookie Clicker arcade cabinet.\n The huge cookie button on the front is pretty neat, but running it forever seems like it would crank your electricity bill. You know, if you had one.\nhttps://orteil.dashnet.org/cookieclicker/",
"This is a Poptropica arcade cabinet.\nI don't know who thought point and click platforming was a good idea, but this new control scheme is a godsend. \nhttps://www.poptropica.com/",
"This is a Frog Fractions arcade cabinet.\nThis cabinet's been lightly used. Looks like a remnant of some bar in Ponyville, what with all the ponytuber signatures on it. Eh, we can leave those well alone for now.\nhttps://kbhgames.com/game/frog-fractions",
"This is a Pokemon Showdown arcade cabinet.\nSouls, hearts, and eons of slime were won and lost on this legendary little number. Playing it on this rickety old thing somehow doesn't seem as suspenseful, though.\n https://pokemonshowdown.com/",
"This is a Madness: Accelerant arcade cabinet.\n If you've been to West Glocksbury the violence in here is a little old hat, but a lot of people have a soft spot for it.\nhttps://www.newgrounds.com/portal/view/512407",
"This is a Flanders Killer 6 arcade cabinet.\nClearly this is the greatest game the world has ever conceived.\nhttps://www.silvergames.com/en/flanders-killer-6",
"This is a Peasant's Quest arcade cabinet.\nThe struggles of the main guy here are a lot like what juvies go through: a rise to greatness, false hope, and inevitable worthless destruction. Onward!\nhttp://homestarrunner.com/disk4of12.html",
"This is a Super Mario 63 arcade cabinet.\nSince Reggie Fils-Amie is too fucking cowardly to set foot in NLACakaNM, we have to resort to bootleg merchandise. Relatively good bootlegs, but bootlegs nonetheless.\nhttps://www.newgrounds.com/portal/view/498969",
"This is a World's Hardest Game arcade cabinet.\nThere were countless stories of moms getting bankrupted because their kids dumped their money into these.\nhttps://www.coolmathgames.com/0-worlds-hardest-game "
]

browse_list = [
"You found a server slightly out of city limits. Looks like they don't care so much about slime or gang warfare, they just make art about other stuff. Unthinkable, but nonetheless fascinating.\nhttps://discord.gg/TAQukUe",
"Ah, how we forget the sports. Vandal Park's rec center ads have always felt like a big distraction from shooting rival gang members in the face, but maybe it could be fun! This one's shilling their TF2 and Ace of Spades sections, there seem to be many others.\n https://discord.gg/X6TB5uP",
"Looks like the Cop Killer has a coven of people someplace outside NLACakaNM, kind of like a summer home or the late stages of a cult operation. Either way, seems interesting.\nhttps://discordapp.com/invite/j6xP5MB ",
"Pokemon Go doesn't seem like an option in this city without a dedicated support group like this. If people went alone, I'm pretty certain they'd get ganked or eaten by secreatures.\nhttps://discord.gg/QbDqEFU",
"Wait a minute. This doesn't seem quite right. Let's not click this one. \nhttps://discord.gg/mtSRXek",
"A young Milwaukee citizen stands in her room. Today is a very important day, though as circumstances would have it, she has momentarily forgotten about the exit. But like hell that's gonna stop her, or her name isn't...\nhttps://discord.gg/EkCMmGn",
"Gangs with wiki pages. I never thought I'd see the day. This place lets you doxx your friends to the NLACakaNM Police Department by compiling their backgrounds and posting it on the internet. They're always looking for writers, so knock yourself out.\nhttps://discord.gg/z5mvCfS",
"You stumble across an old ARG server. It's since been abandoned, but it's an interesting little piece of history nonetheless.\nhttps://discord.gg/9nwaMC",
"You find a group of visionaries who have turned hunting into a business. Personally, you wouldn't have gone with the LARPy high-fantasy branding, but to each their own.\nhttps://discord.gg/Rw2wCYT",
"Killers weren't supposed to be able to access this place, but all you really have to do to get in these days is convincingly !thrash a few times.\nhttps://discord.gg/JZ2AaJ2",
"St. Ben's Cathedral is a weird base in that it doesn't really bar rowdys from entry. The killers there generally just sneer and spit at their rival gangsters. \nhttps://discord.gg/xSQQD2M",
"Look, you ignorant juvenile. You basically don't know anything. The media that you love so much is a brainwashing tool, and its lies pull wool over your weary eyes. Get REAL news from the South Los Angeles News Dog Enquirer Report.\nhttps://discord.gg/FtHKt3B",
"SUBMIT TO SLIMECORP\nhttps://discord.gg/HK8VEzw",
"You succumb to your urges and find a rather naughty link. Slimegirls are against God's will, but if you don't care this place might appeal to you.\n https://discord.gg/nN6xtk9",
"@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\n@everyone\nhttps://discord.gg/b2hP68k",
"It's the land of the nateheads. You're really opening Pandora's box, fucking with this one. \nhttps://discordapp.com/invite/2Kc7nTA",
"You used to not be a big fan of hippos, but then you learned they like tearing people limb from limb and you've been in love ever since. Maybe now's your chance to meet one.\nhttps://discordapp.com/invite/6ksZrne",
"Y'arrr. \nhttps://discord.gg/VFcUmgc"
]

bible_verses = [
"And they said one to another, Go to, let us make brick, and burn them thoroughly. And they had brick for stone, and slime had they for mortar. And they said, !Goto, let us build us a city and a tower, whose top may reach unto heaven; and let us make us a name, lest we be scattered abroad upon the face of the whole earth… Genesis, 11:4 7",
"Then he went up from there to Bethel; and as he was going up by the way, young lads came out from the city and mocked him and said to him, “Go up, you baldhead; go up, you baldhead!” When he looked behind him and saw them, he cursed them in the name of the LORD. Then two female bears came out of the woods and tore up forty-two lads of their number. And he went from there to Mount Carmel, and from there he returned to Samaria. 2 Kings 2:23-25",
"Yet she became more and more promiscuous as she recalled the days of her youth, when she was a prostitute in Egypt. There she lusted after her lovers, whose genitals were like those of donkeys and whose emission was like that of horses. So you longed for the lewdness of your youth, when in Egypt your bosom was caressed and your young breasts fondled. Ezekiel 23:19",
"No one whose testicles are crushed or whose male organ is cut off shall enter the assembly of the Lord. Deuteronomy 23:1",
"Ye are the light of the world. A city that is set on an hill cannot be hid. Matthew 5:14",
"But now they desire a better country, that is, an heavenly: wherefore God is not ashamed to be called their God: for he hath prepared for them a city. Hebrews 11:16 ",
"Seek the prosperity of the city to which I have sent you as exiles. Pray to the LORD on its behalf, for if it prospers, you too will prosper. Jeremiah 29:7",
"And they went up on the breadth of the earth, and compassed the camp of the saints about, and the beloved city: and fire came down from God out of heaven, and devoured them. Revelation 20:9 ",
"And I will turn my hand upon thee, and purely purge away thy dross, and take away all thy tin: And I will restore thy judges as at the first, and thy counsellors as at the beginning: afterward thou shalt be called, The city of righteousness, the faithful city. Isaiah 1:25-26 ",
"David rose up and went, he and his men, and struck down two hundred men among the Philistines Then David brought their foreskins, and they gave them in full number to the king, that he might become the king's son-in-law. So Saul gave him Michal his daughter for a wife. 1 Samuel 18:27 ",
"Behold, the days come, saith the LORD, that I will punish all them which are circumcised with the uncircumcised. Jeremiah 9:25",
"Let me gulp down some of that red stuff; I’m starving. Genesis 25:30 ",
"Would that those who are upsetting you might also castrate themselves! Galatians 5:12",
"Even the handle sank in after the blade, and his bowels discharged. Ehud did not pull the sword out, and the fat closed in over it. Judges 3:22 ",
]


tv_lines = [
	"Breaking news! A local street performer won't come down from a gigantic pile of corpses. He refuses to eat for publicity! More to come.",
	"Welcome, goobs and gabs, to the Live Interactive Broadcast Enquirer Line, or L.I.B.E.L. for short. In today's news, local resident N6 was arrested for her abusive and predatory behavior toward Epic. Charges include false accusations of foot fetishism, terroristic threats, and 3rd degree sloshing toward a minor.",
	"Welcome to Mad Murderous Money, the show where stockbrokers are allowed, nay, encouraged, to jump out of buildings when the Dow Jones gets a bit pouty. Today we have a fucking ridiculous upturn for KFC, which actually got one of its supply trucks through the gang infested streets without being ransacked. Taco Bell set up a new restaraunt in New New Yonkers, but the windows aren't even bulletproof, so it's probably just gonna be a money pit for them. But my little chiclets, DO NOT invest in FUCKING PIZZA HUT. ENDLESS WAR shot a fucking laser through their kitchen and they're still in reconstruction. \n\nAs always, this is Mad Murderous Money, telling you to buy sell, die, and shill!",
	"Hey, everybody. This is Slime Bob Ross. I'm like regular Bob Ross, only I'm a thrown together copy some Juvie made cause he wanted to fuck me. Today, we'll be painting on the graffiti soaked walls of urban Green Light District. Now, the first thing you do on these urban type pieces is to sign your name here in the bottom right. This is so you will receive credit even if you have to run from the police halfway through. OK, very good. Today we're going to be doing a still life of Wreckington. We'll be doing a lot of greys here, but let's start with something fun, the flames of the burning wreckage. Wait. I forgot to bring red paint. OK, in that case, I'll have more once I fetch a Juvie during the commercial break. Stay tuned!",
	"The TV is just static. Maybe it's a bad reception. You wait. It will turn back on eventually, right?",
	"Welcome to Reading Rainbow, boys and girls! I'm Slime Levar Burton, and despite the existential  dread that comes with being a blob person, I'm doing wonderful today. This week, I read a book called 'The Gamer and The Bear'. We'll read an excerpt here. \nOnce upon a time in a cute little village at the bottom of a valley was a big rowdy bear.The bear was a real nasty guy, always smashing shit up and stomping his big feet. All the innocent little gamers of the village were scared of the big bear for if he saw them !dabbing he’d rip them limb from limb! They had to hide in their homes when he came around, !dabbing under their breath and gaming with the TV muted. It was a horrible time for everyone. \nThat was the first page, be sure to buy the full book!",
	"It's time for 'Our Deep Fuck City', where we run documentaries on the mystique of each district. Today, we'll be examining the phenomenon of 'Door Gunning', a new prank pulled by the upstarts of Little Chernobyl. In order to explain it, we must first look at a certain subculture of people there, known as half-deads. These folks live so close to the radiation of Little Chernobyl Power Plant that the radiation has more than killed them and fully decayed their minds. The problem is, they can't !revive either. They are so brain dead that ENDLESS WAR doesn't know what to do with them. So functionally, they exist as these wildly disfigured, basically immortal suburbanites. Door Gunning takes advantage of this. A prankster will knock on the door of some hapless half-dead person, and shoot them repeatedly in the face. It's incredibly painful, but since nobody dies it gets passed off as harmless fun. It really makes you think, eh?",
	"It's time for 'Our Deep Fuck City', where we run documentaries on the mystique of each district. We've got a treat for you this time, something you probably haven't heard of. Charcoal Park's efforts to fight back against hostile secreatures. You see, most districts are under Slimecorp's protection, excluding gangsters. However, Charcoal Park was such a forgettable place that they just forgot to send relief over there. Things have gotten so dire that many of the region's blue collar workers have banded together to form a militia of their own. There were many casualties at first, but intense training has turned the region into an sort of anarchist paradise. You wouldn't know it, though. To this day, their houses are kept very clean.",
	"Oh. Looks like it's playing the test screen. You know, the one with all the verticle colored stripes and the long beep. Yeah.",
	"It's time for 'Our Deep Fuck City', where we run documentaries on the mystique of each district. Most NLACakaNM citizens stay indoors for obvious reasons. Because of this, we're often oblivious to the interesting new social patterns they exhibit in this isolation. For example, Old New Yonkers has developed its own sect of Christianity. The practitioners of Neo-Protestant Milwaukeeism are convinced that ENDLESS WAR is the second coming of Christ, and that they have all been sent to Hell for their sins. Beyond that, most of the differences lie in the amount of self-flaggellation there is. NLACakaNM is a place of extremes, so what actually takes place is pretty mild compared to what else we've seen here. But despite its modesty, those folks may well be the most miserable in the city.",
	"It's time for 'Our Deep Fuck City', where we run documentaries on the mystique of each district. It's time to talk about the disappearing statue of Thalamus J. Crookline that stands in Globule Plaza. You see, Crookline's bandits have developed an inflated sense of honor among themselves. Part of that means they'll often wish themselves luck on that particular statue for good fortune in their pilfering. Every thief knows this, so it's not surprising how often the damn thing gets stolen. Hence the 'disappearance'. It costs the government like 1,000,000 slime a year just to maintain it.",
]

the_slime_lyrics= [
"https://www.youtube.com/watch?v=w-sREpqDiUo",
"I am gross and perverted \nI'm obsessed 'n deranged \nI have existed for years\nBut very little has changed",
"I'm the tool of the Government\nAnd industry too\nFor I am destined to rule\nAnd regulate you",
"I may be vile and pernicious\nBut you can't look away\nI make you think I'm delicious\nWith the stuff that I say",
"I'm the best you can get\nHave you guessed me yet?\nI'm the slime oozin' out\nFrom your TV set",
"You will obey me while I lead you\nAnd eat the garbage that I feed you\nUntil the day that we don't need you\nDon't go for help . . . no one will heed you",
"Your mind is totally controlled\nIt has been stuffed into my mold\nAnd you will do as you are told\nUntil the rights to you are sold",
"That's right, folks\nDon't touch that dial",
"Well, I am the slime from your video\nOozin' along on your livin' room floor\nI am the slime from your video\nCan't stop the slime, people, lookit me go",
"I am the slime from your video\nOozin' along on your livin' room floor\nI am the slime from your video\nCan't stop the slime, people, lookit me go",
"Welp, there it went. The Slime begins to wreak havoc outside your apartment. Can you believe you sat on your ass for like 6 hours?"
]

jams_saxophone = ["https://www.youtube.com/watch?v=Z2tvlp7RnlM&ab_channel=rgsmusicargentina", "https://www.youtube.com/watch?v=-yg7aZpIXRI&ab_channel=domtheodore", "https://www.youtube.com/watch?v=9Zyr0IDaRXQ&ab_channel=JohnColtrane-Topic"]
jams_drums = ["https://www.youtube.com/watch?v=fE6YN9VcPPA&ab_channel=ProphetOfTheMoons", "https://www.youtube.com/watch?v=4D4iSmpT-bI&ab_channel=BuddyRich-Topic", "https://www.youtube.com/watch?v=US7c9ASVfNc&ab_channel=kekecanberk"]
jams_xylophone = ["https://www.youtube.com/watch?v=QGDXuJlJdec&ab_channel=Klagmar", "https://www.youtube.com/watch?v=-1dSY6ZuXEY&ab_channel=Dr.Blase", "https://www.youtube.com/watch?v=NUBSNWVG55Y&ab_channel=VictorMendoza"]
jams_bass = ["https://www.youtube.com/watch?v=Pyral_8aZp8&ab_channel=MingusBigBand-Topic", "https://www.youtube.com/watch?v=hnVFGz0xYKE&ab_channel=TheMarsVolta-Topic", "https://www.youtube.com/watch?v=ogKDBbi2thA&ab_channel=MadMaxOnlyMusic"]
jams_clarinet = ["https://www.youtube.com/watch?v=4dm3Ml9g_cs&ab_channel=CatsPjamas1", "https://www.youtube.com/watch?v=Im2JDdcXO9Y&ab_channel=EvanChristopher%26ClarinetRoad", "https://www.youtube.com/watch?v=r2S1I_ien6A&ab_channel=WorldWar2Music"]
jams_vuvuzela = ["https://www.youtube.com/watch?v=oyAP6PpAzK8&ab_channel=TheAttilaX", "https://www.youtube.com/watch?v=-E6ljLSOkbY&ab_channel=TehN1ppe"]
jams_guitar = ["https://www.youtube.com/watch?v=hNRHHRjep3E&ab_channel=rtwodtwo565", "https://www.youtube.com/watch?v=mBbyrqNhyNE&ab_channel=Metal8909", "https://www.youtube.com/watch?v=xnKhsTXoKCI&ab_channel=MotherRussiaMr"]
jams_maracas = ["https://www.youtube.com/watch?v=etYb-p8uhWA&ab_channel=GilvaSunner", "https://www.youtube.com/watch?v=EstIvN0_hcg&ab_channel=Cz%C5%82owiekDrzewo", "https://www.youtube.com/watch?v=l8R_OQz_BtU&ab_channel=majabsalu"]
jams_cornet = ["https://www.youtube.com/watch?v=mPP65UcGxq0&ab_channel=Ham_", "https://www.youtube.com/watch?v=FJrUBEtoNQU&ab_channel=ropa79", "https://www.youtube.com/watch?v=KxibMBV3nFo&ab_channel=TheJazzplaylist"]
jams_trombone = ["https://www.youtube.com/watch?v=WEWLuBB7_FE&ab_channel=mixablemusic", "https://www.youtube.com/watch?v=lqngnNy1_Cg&ab_channel=DaveYama", "https://www.youtube.com/watch?v=1ZGeYR8b-mg&ab_channel=AllThatJazzDonKaart"]

jam_tunes = {
	"solidpoudringuitar" : jams_guitar,
	"craftsmansclarinet" : jams_clarinet,
	"gourdmaracas" : jams_maracas,
	"saxophone" : jams_saxophone,
	"woodenvuvuzela" : jams_vuvuzela,
	"fishbonexylophone" : jams_xylophone,
	"beastskindrums" : jams_drums,
	"bass" : jams_bass,
	"trombone" : jams_trombone,
	"cornet": jams_cornet
}


furniture_list = []
with open(os.path.join('json', 'furniture.json')) as f:
	furniture = json.load(f)
	for i in furniture:
		i = furniture[i]
		furniture_list.append(
			EwFurniture(
				id_furniture = i['id_furniture'],
				str_name = i['str_name'],
				str_desc = i['str_desc'],
				rarity = i['rarity'],
				acquisition = i['acquisition'],
				price = i['price'],
				vendors = i['vendors'],
				furniture_place_desc = i['furniture_place_desc'],
				furniture_look_desc = i['furniture_look_desc'],
				furn_set = i['furn_set'],
				hue = i['hue'],
				num_keys = i['num_keys']
			))

furniture_map = {}
furniture_names = []
furniture_lgbt = []
furniture_highclass = []
furniture_haunted = []
furniture_leather = []
furniture_church = []
furniture_pony = []
furniture_blackvelvet = []
furniture_slimecorp = []
furniture_seventies = []
furniture_shitty = []
furniture_instrument = []
furniture_specialhue = []

howls = [
	'**AWOOOOOOOOOOOOOOOOOOOOOOOO**',
	'**5 6 7 0 9**',
	'**awwwwwWWWWWooooOOOOOOOOO**',
	'**awwwwwwwwwooooooooooooooo**',
	'*awoo* *awoo* **AWOOOOOOOOOOOOOO**',
	'*awoo* *awoo* *awoo*',
	'**awwwwwWWWWWooooOOOOOOOoo**',
	'**AWOOOOOOOOOOOOOOOOOOOOOOOOOOOOO**',
	'**AWOOOOOOOOOOOOOOOOOOOO**',
	'**AWWWOOOOOOOOOOOOOOOOOOOO**'
]

moans = [
	'**BRRRRRAAAAAAAAAIIIIIINNNNNZZ**',
	'**B R A I N Z**',
	'**bbbbbRRRRRaaaaaaIIIIIInnnnZZZZZZ**',
	'**bbbbbbrrrrrraaaaaaaaiiiiiiinnnnnnnzzzz**',
	'**duuuuude, liiiiike, brrrraaaaaaiiiiinnnnnnzzzzz**',
	'**bbbraaaaiiinnnzzz**',
	'**BRAAAAAAAIIIIIIIIIIIIIIIINNNNNNNNNZZZZZZZZ**',
	'**BBBBBBBBBBBBBBBBBRRRRRRRRRRRRRRRAAAAAAAAAAAAAIIIIIIIIIIIIIIINNNNNNNNZZZZZZZZZZ**',
	'**BRRRRAAAAAIIINNNNNZZZ**',
	'**BBBBRRRRRRRRRRRRRRRAAAAIIIIIINNNNZZZZZ**',
	'**BRRRAAAIINNNZZ? BRRRAAAAIINNNZZ! BRRRRRRRAAAAAAAAIIIIIINNNNNZZZZZZZ!!!**',
	'**bbbbbBBBBrrrrrRRRRaaaaIIIIInnnnnnNNNNNzzzzZZZZZZZ!!!**',
	'**CCCCRRRRRRIIIIINNNNNNNGGGGEEEEE! BBBBBAAAAAAAAAAASSSSSEEEDDDDDDDD!**'
]

"""
	The list of item definitions. Instances of items are always based on these
	skeleton definitions.
"""
item_def_list = [
	EwItemDef(
		# Unique item identifier. Not shown to players.
		item_type = "demo",

		# The name of the item that players will see.
		str_name = "Demo",

		# The description shown when you look at an item.
		str_desc = "A demonstration item."
	),

	EwItemDef(
		item_type = it_item,
		str_name = "{item_name}",
		str_desc = "{item_desc}",
		item_props = {
			'id_name': 'normalitem',
			'context': 'context',
			'item_name': 'Normal Item.',
			'item_desc': 'This is a normal item.',
			'ingredients': 'vegetable'
		}
	),

	# A customizable award object.
	EwItemDef(
		item_type = it_medal,
		str_name = "{medal_name}",
		str_desc = "{medal_desc}",
		soulbound = True,
		item_props = {
			'medal_name': 'Blank Medal',
			'medal_desc': 'An uninscribed medal with no remarkable features.'
		}
	),

	EwItemDef(
		item_type = it_questitem,
		str_name = "{qitem_name}",
		str_desc = "{qitem_desc}",
		soulbound = True,
		item_props = {
			'qitem_name': 'Quest Item',
			'qitem_desc': 'Something important to somebody.'
		}
	),

	EwItemDef(
		item_type = it_food,
		str_name = "{food_name}",
		str_desc = "{food_desc}",
		soulbound = False,
		item_props = {
			'food_name': 'Food Item',
			'food_desc': 'Food.',
			'recover_hunger': 0,
			'price': 0,
			'inebriation': 0,
			'vendor': None,
			'str_eat': 'You eat the food item.',
			'time_expir': std_food_expir,
			'time_fridged': 0,
		}
	),

	EwItemDef(
		item_type = it_weapon,
		str_name = "{weapon_name}",
		str_desc = "{weapon_desc}",
		soulbound = False,
		item_props = {
			'weapon_type': 'Type of weapon',
			'weapon_desc': 'It\'s a weapon of some sort.',
			'weapon_name': 'Weapon\'s name',
			'ammo': 0,
			'married': 'User Id',
			'kills': 0,
			'consecutive_hits': 0,
			'time_lastattack': 0,
			'totalkills': 0
		}
	),
	EwItemDef(
		item_type = it_cosmetic,
		str_name = "{cosmetic_name}",
		str_desc = "{cosmetic_desc}",
		soulbound = False,
		item_props = {
			'cosmetic_name': 'Cosmetic Item',
			'cosmetic_desc': 'Cosmetic Item.',
			'rarity': rarity_plebeian,
			'hue': "",
		}
	),
	EwItemDef(
		item_type = it_furniture,
		str_name = "{furniture_name}",
		str_desc = "{furniture_desc}",
		soulbound = False,
		item_props = {
			'furniture_name': 'Furniture Item',
			'furniture_place_desc': 'placed',
			'furniture_look_desc': 'it\'s there',
			'rarity': rarity_plebeian,
			'vendor': None,

		}
	),
	EwItemDef(
		item_type = it_book,
		str_name = "{title}",
		str_desc = "{book_desc}",
		soulbound = False,
		item_props = {
			"title": "Book",
			"author": "Boy",
			"date_published": 2000,
			"id_book": 69,
			"book_desc": "A book by AUTHOR, published on DAY."
		}
	),
]

# A map of item_type to EwItemDef objects.
item_def_map = {}

# Populate the item def map.
for item_def in item_def_list:
	item_def_map[item_def.item_type] = item_def


#load EwPois from json to poi_list
poi_list = []
with open(os.path.join('json', 'poi.json')) as f:
	pois = json.load(f)
	for i in pois:
		i = pois[i]
		poi_list.append(
			EwPoi(
				id_poi = i['id_poi'], 
				alias = i['alias'], 
				str_name = i['str_name'], 
				str_desc = i['str_desc'], 
				str_in = i['str_in'], 
				str_enter = i['str_enter'], 
				coord = i['coord'], 
				coord_alias = i['coord_alias'], 
				channel = i['channel'], 
				role = i['role'], 
				major_role = i['major_role'], 
				minor_role = i['minor_role'], 
				permissions = i['permissions'], 
				pvp = i['pvp'], 
				factions = i['factions'], 
				life_states = i['life_states'], 
				closed = i['closed'], 
				str_closed = i['str_closed'], 
				vendors = i['vendors'], 
				property_class = i['property_class'], 
				is_district = i['is_district'], 
				is_gangbase = i['is_gangbase'], 
				is_capturable = i['is_capturable'], 
				is_subzone = i['is_subzone'], 
				is_apartment = i['is_apartment'], 
				is_street = i['is_street'], 
				mother_districts = i['mother_districts'], 
				father_district = i['father_district'], 
				is_transport = i['is_transport'], 
				transport_type = i['transport_type'], 
				default_line = i['default_line'], 
				default_stop = i['default_stop'], 
				is_transport_stop = i['is_transport_stop'], 
				transport_lines = set(), 
				is_outskirts = i['is_outskirts'], 
				community_chest = i['community_chest'], 
				is_pier = i['is_pier'], 
				pier_type = i['pier_type'], 
				is_tutorial = i['is_tutorial'], 
				has_ads = i['has_ads'], 
				write_manuscript = i['write_manuscript'], 
				max_degradation = i['max_degradation'], 
				neighbors = i['neighbors'], 
				topic = i['topic'], 
				wikipage = i['wikipage'], 
			))


	

debugroom = ewdebug.debugroom
debugroom_short = ewdebug.debugroom_short
debugpiers = ewdebug.debugpiers
debugfish_response = ewdebug.debugfish_response
debugfish_goal = ewdebug.debugfish_goal

# if you're looking for poi_map, here it is
id_to_poi = {}
coord_to_poi = {}
chname_to_poi = {}
alias_to_coord = {}
capturable_districts = []
outskirts_districts = []
transports = []
transport_stops = []
transport_stops_ch = []
piers = []
outskirts = []
outskirts_edges = []
outskirts_middle = []
outskirts_depths = []
streets = []
tutorial_pois = []
zine_mother_districts = []

for poi in poi_list:

	# Assign permissions for all locations in the poi list.
	if poi.permissions == None:
		poi.permissions = {('{}'.format(poi.id_poi)): permissions_general}

	# Assign all the correct major and minor roles.
	
	# Districts and streets need their minor roles to see (read-only) all of their subzones.
	if poi.is_district or poi.is_street or poi.id_poi in [poi_id_mine, poi_id_cv_mines, poi_id_tt_mines]:
		poi.minor_role = '{}_minor'.format(poi.id_poi)

	# Districts need their major roles for their specific LAN (voice/text) channels.
	if poi.is_district:
		poi.major_role = '{}_major'.format(poi.id_poi)
		streets_resp = ''
		"""
		district_streets_list = []
		for street_poi in poi_list:
			if street_poi.father_district == poi.id_poi:
				district_streets_list.append(street_poi.str_name)
			
		if len(district_streets_list) > 0:
			poi.str_desc += " This area is connected to "
			if len(district_streets_list) == 1:
				poi.str_desc += district_streets_list[0]
			else:
				for i in range(len(district_streets_list)):
		
					if i == (len(district_streets_list) - 1):
						poi.str_desc += 'and {}.'.format(district_streets_list[i])
					else:
						poi.str_desc += '{}, '.format(district_streets_list[i])
		"""
						
	placeholder_channel_names_used = False
		
	# Subzones and streets need the same major roles as their mother/father districts.
	if poi.is_street:
		if poi.father_district != "" and poi.father_district != None:
			for father_poi in poi_list:
				if father_poi.id_poi == poi.father_district:
					poi.major_role = father_poi.major_role
					poi.property_class = father_poi.property_class
					
					if placeholder_channel_names_used:
						if 'streeta' in poi.id_poi:
							poi.channel = father_poi.channel + '-street-a'
						elif 'streetb' in poi.id_poi:
							poi.channel = father_poi.channel + '-street-b'
						elif 'streetc' in poi.id_poi:
							poi.channel = father_poi.channel + '-street-c'
						elif 'streetd' in poi.id_poi:
							poi.channel = father_poi.channel + '-street-d'
						elif 'streete' in poi.id_poi:
							poi.channel = father_poi.channel + '-street-e'
						elif 'streetf' in poi.id_poi:
							poi.channel = father_poi.channel + '-street-f'
							
					break
			
			father_district = ''
			connected_streets_and_districts = []
			connected_subzones = []
			for neighbor_poi in poi_list:
				if neighbor_poi.id_poi in poi.neighbors:
					if neighbor_poi.id_poi == poi.father_district:
						father_district = neighbor_poi.str_name
					elif neighbor_poi.is_street or (neighbor_poi.is_district and neighbor_poi.id_poi != poi.father_district):
						connected_streets_and_districts.append(neighbor_poi.str_name)
					elif neighbor_poi.is_subzone:
						connected_subzones.append(neighbor_poi.str_name)
			
			if father_district != '':
				poi.str_desc += " This street connects back into {}.".format(father_district)
			
				if len(connected_streets_and_districts) >= 1:
					poi.str_desc += " This street is connected to "
					if len(connected_streets_and_districts) == 1:
						poi.str_desc += connected_streets_and_districts[0]
					else:
						for i in range(len(connected_streets_and_districts)):
					
							if i == (len(connected_streets_and_districts) - 1):
								poi.str_desc += 'and {}.'.format(connected_streets_and_districts[i])
							else:
								poi.str_desc += '{}, '.format(connected_streets_and_districts[i])

				if len(connected_subzones) >= 1:
					poi.str_desc += " This street also exits into "
					if len(connected_subzones) == 1:
						poi.str_desc += connected_subzones[0]
					else:
						for i in range(len(connected_subzones)):
		
							if i == (len(connected_subzones) - 1):
								poi.str_desc += 'and {}.'.format(connected_subzones[i])
							else:
								poi.str_desc += '{}, '.format(connected_subzones[i])
		else:
			print('Error: No father POI found for {}'.format(poi.id_poi))
	
	mother_roles_dict = {}
	if poi.is_subzone:
		
		for mother_poi in poi_list:
			if mother_poi.id_poi in poi.mother_districts:
				if mother_poi.major_role != None:
					poi.major_role = mother_poi.major_role
					break
		
	if poi.major_role == None:
		#print('Null Major Role give to {}'.format(poi.id_poi))
		poi.major_role = role_null_major_role
	if poi.minor_role == None:
		#print('Null Minor Role give to {}'.format(poi.str_name))
		poi.minor_role = role_null_minor_role
	
	# poi coords cause json import problems because poi.coords imports as a list type 
	#if poi.coord != None:
	#	# Populate the map of coordinates to their point of interest, for looking up from the map.
	#	coord_to_poi[poi.coord] = poi
	#	
	#	# for poi_2 in poi_list:
	#	# 	if (poi.coord == poi_2.coord) and (poi.id_poi != poi_2.id_poi):
	#	# 		print('{} has same coords as {}, please fix this.'.format(poi.id_poi, poi_2.id_poi))
	#
	#	# Populate the map of coordinate aliases to the main coordinate.
	#	for coord_alias in poi.coord_alias:
	#		alias_to_coord[coord_alias] = poi.coord
	#		coord_to_poi[coord_alias] = poi

	# Populate the map of point of interest names/aliases to the POI.
	id_to_poi[poi.id_poi] = poi
	for alias in poi.alias:
		for poi_2 in poi_list:
			if alias in poi_2.alias and poi.id_poi != poi_2.id_poi:
				print('alias {} is already being used by {}'.format(alias, poi_2.id_poi))

		id_to_poi[alias] = poi

	# if it's a district and not RR, CK, or JR, add it to a list of capturable districts
	if poi.is_capturable:
		capturable_districts.append(poi.id_poi)

	if poi.is_transport:
		transports.append(poi.id_poi)

	if poi.is_transport_stop:
		transport_stops.append(poi.id_poi)
		transport_stops_ch.append(poi.channel)

	if poi.is_pier:
		piers.append(poi.id_poi)

	if poi.is_outskirts:
		outskirts.append(poi.id_poi)
		# For spawning purposes. Rarer enemies will spawn more often in the father layers of the 18 outskirts.
		
		# It's a bit of a simplistic solution, but this way we don't have to add an attribute to EwPoi
		if 'edge' in poi.str_name.lower():
			outskirts_edges.append(poi.id_poi)
			#print(poi.channel)
		elif 'depths' in poi.str_name.lower():
			outskirts_depths.append(poi.id_poi)
			#print(poi.channel)
		else:
			outskirts_middle.append(poi.id_poi)
		
		if len(poi.neighbors) > 0:
			poi.str_desc += " This outskirt is connected to "
			
			neighbor_index = 0
			for neighbor_id in poi.neighbors.keys():
				
				current_neighbor = None
				
				for outskirt_neighbor in poi_list:
					if neighbor_id == outskirt_neighbor.id_poi:
						current_neighbor = outskirt_neighbor
						
				if current_neighbor != None:
					if neighbor_index == (len(poi.neighbors.keys()) - 1):
						poi.str_desc += 'and {}.'.format(current_neighbor.str_name)
					else:
						poi.str_desc += '{}, '.format(current_neighbor.str_name)
				
				neighbor_index += 1
		
	if poi.is_street:
		streets.append(poi.id_poi)
		#print(poi.minor_role)

	if poi.is_tutorial:
		tutorial_pois.append(poi.id_poi)

	if poi.write_manuscript:
		for mother_poi in poi.mother_districts:
			zine_mother_districts.append(id_to_poi.get(mother_poi))

	chname_to_poi[poi.channel] = poi


landmark_pois = [
	poi_id_dreadford,
	poi_id_charcoalpark,
	poi_id_slimesend,
	poi_id_assaultflatsbeach,
	poi_id_wreckington,
]

non_district_non_subzone_pvp_areas = [
	poi_id_thevoid
]

# Places on the map that should result in a user being flagged for PVP
vulnerable_districts = outskirts + streets
for poi in poi_list:
	if (poi.is_subzone or poi.id_poi in non_district_non_subzone_pvp_areas) and poi.pvp:
		vulnerable_districts.append(poi.id_poi)
# for vul in vulnerable_districts:
#     print('vulnerable area: {}'.format(vul))

# maps districts to their immediate neighbors
poi_neighbors = {}

transport_lines = [
	EwTransportLine( # ferry line from wreckington to vagrant's corner
		id_line = transport_line_ferry_wt_to_vc,
		alias = [
			"vagrantscornerferry",
			"vagrantsferry",
			"vcferry",
			"ferrytovagrantscorner",
			"ferrytovagrants",
			"ferrytovc"
			],
		first_stop = poi_id_wt_port,
		last_stop = poi_id_vc_port,
		next_line = transport_line_ferry_vc_to_wt,
		str_name = "The ferry line towards Vagrant's Corner",
		schedule = {
			poi_id_wt_port : [60, poi_id_slimesea],
			poi_id_slimesea : [120, poi_id_vc_port]
			}

		),
	EwTransportLine( # ferry line from vagrant's corner to wreckington
		id_line = transport_line_ferry_vc_to_wt,
		alias = [
			"wreckingtonferry",
			"wreckferry",
			"wtferry",
			"ferrytowreckington",
			"ferrytowreck",
			"ferrytowt"
			],
		first_stop = poi_id_vc_port,
		last_stop = poi_id_wt_port,
		next_line = transport_line_ferry_wt_to_vc,
		str_name = "The ferry line towards Wreckington",
		schedule = {
			poi_id_vc_port : [60, poi_id_slimesea],
			poi_id_slimesea : [120, poi_id_wt_port]
			}
		),
	EwTransportLine( # yellow subway line from south sleezeborough to arsonbrook
		id_line = transport_line_subway_yellow_northbound,
		alias = [
			"northyellowline",
			"northyellow",
			"yellownorth",
			"yellowtoarsonbrook",
			"yellowtoarson",
			"yellowtoab"
			],
		first_stop = poi_id_ssb_subway_station,
		last_stop = poi_id_ab_subway_station,
		next_line = transport_line_subway_yellow_southbound,
		str_name = "The yellow subway line towards Arsonbrook",
		schedule = {
			poi_id_ssb_subway_station : [20, poi_id_kb_subway_station],
			poi_id_kb_subway_station : [20, poi_id_dt_subway_station],
			poi_id_dt_subway_station : [20, poi_id_sb_subway_station],
			poi_id_sb_subway_station : [20, poi_id_ab_subway_station]
			}

		),
	EwTransportLine( # yellow subway line from arsonbrook to south sleezeborough
		id_line = transport_line_subway_yellow_southbound,
		alias = [
			"southyellowline",
			"southyellow",
			"yellowsouth",
			"yellowtosouthsleezeborough",
			"yellowtosouthsleeze",
			"yellowtossb"
			],
		first_stop = poi_id_ab_subway_station,
		last_stop = poi_id_ssb_subway_station,
		next_line = transport_line_subway_yellow_northbound,
		str_name = "The yellow subway line towards South Sleezeborough",
		schedule = {
			poi_id_ab_subway_station : [20, poi_id_sb_subway_station],
			poi_id_sb_subway_station : [20, poi_id_dt_subway_station],
			poi_id_dt_subway_station : [20, poi_id_kb_subway_station],
			poi_id_kb_subway_station : [20, poi_id_ssb_subway_station]
			}

		),
	EwTransportLine( # red subway line from cratersville to toxington
		id_line = transport_line_subway_red_northbound,
		alias = [
			"northredline",
			"northred",
			"rednorth",
			"redtotoxington",
			"redtotox",
			"redtott"
			],
		first_stop = poi_id_cv_subway_station,
		last_stop = poi_id_tt_subway_station,
		next_line = transport_line_subway_red_southbound,
		str_name = "The red subway line towards Toxington",
		schedule = {
			poi_id_cv_subway_station : [20, poi_id_wt_subway_station],
			poi_id_wt_subway_station : [20, poi_id_rr_subway_station],
			poi_id_rr_subway_station : [20, poi_id_dt_subway_station],
			poi_id_dt_subway_station : [20, poi_id_ck_subway_station],
			poi_id_ck_subway_station : [20, poi_id_gd_subway_station],
			poi_id_gd_subway_station : [20, poi_id_ah_subway_station],
			poi_id_ah_subway_station : [20, poi_id_tt_subway_station]
			}

		),
	EwTransportLine( # red subway line from toxington to cratersville
		id_line = transport_line_subway_red_southbound,
		alias = [
			"southredline",
			"southred",
			"redsouth",
			"redtocratersville",
			"redtocraters",
			"redtocv"
			],
		first_stop = poi_id_tt_subway_station,
		last_stop = poi_id_cv_subway_station,
		next_line = transport_line_subway_red_northbound,
		str_name = "The red subway line towards Cratersville",
		schedule = {
			poi_id_tt_subway_station : [20, poi_id_ah_subway_station],
			poi_id_ah_subway_station : [20, poi_id_gd_subway_station],
			poi_id_gd_subway_station : [20, poi_id_ck_subway_station],
			poi_id_ck_subway_station : [20, poi_id_dt_subway_station],
			poi_id_dt_subway_station : [20, poi_id_rr_subway_station],
			poi_id_rr_subway_station : [20, poi_id_wt_subway_station],
			poi_id_wt_subway_station : [20, poi_id_cv_subway_station]
			}

		),
	EwTransportLine( # green subway line from smogsburg to west glocksbury
		id_line = transport_line_subway_green_eastbound,
		alias = [
			"greeneastline",
			"greeneast",
			"eastgreen",
			"greentosmogsburg",
			"greentosmogs",
			"greentosb"
			],
		first_stop = poi_id_wgb_subway_station,
		last_stop = poi_id_sb_subway_station,
		next_line = transport_line_subway_green_westbound,
		str_name = "The green subway line towards Smogsburg",
		schedule = {
			poi_id_wgb_subway_station : [20, poi_id_jp_subway_station],
			poi_id_jp_subway_station : [20, poi_id_nsb_subway_station],
			poi_id_nsb_subway_station : [20, poi_id_kb_subway_station],
			poi_id_kb_subway_station : [20, poi_id_dt_subway_station],
			poi_id_dt_subway_station : [20, poi_id_sb_subway_station]
			}

		),
	EwTransportLine( # green subway line from west glocksbury to smogsburg
		id_line = transport_line_subway_green_westbound,
		alias = [
			"greenwestline",
			"greenwest",
			"westgreen",
			"greentowestglocksbury",
			"greentowestglocks",
			"greentowgb"
			],
		first_stop = poi_id_sb_subway_station,
		last_stop = poi_id_wgb_subway_station,
		next_line = transport_line_subway_green_eastbound,
		str_name = "The green subway line towards West Glocksbury",
		schedule = {
			poi_id_sb_subway_station : [20, poi_id_dt_subway_station],
			poi_id_dt_subway_station : [20, poi_id_kb_subway_station],
			poi_id_kb_subway_station : [20, poi_id_gb_subway_station],
			poi_id_gb_subway_station : [20, poi_id_wgb_subway_station]
			}

		),
	EwTransportLine( # blue subway line from downtown to assault flats beach
		id_line = transport_line_subway_blue_eastbound,
		alias = [
			"blueeastline",
			"blueeast",
			"eastblue",
			"bluetoassaultflatsbeach",
			"bluetoassaultflats",
			"bluetobeach",
			"bluetoafb"
			],
		first_stop = poi_id_dt_subway_station,
		last_stop = poi_id_afb_subway_station,
		next_line = transport_line_subway_blue_westbound,
		str_name = "The blue subway line towards Assault Flats Beach",
		schedule = {
			poi_id_dt_subway_station : [20, poi_id_gld_subway_station],
			poi_id_gld_subway_station : [20, poi_id_jr_subway_station],
			poi_id_jr_subway_station : [20, poi_id_vc_subway_station],
			poi_id_vc_subway_station : [20, poi_id_afb_subway_station]
			}

		),
	EwTransportLine( # blue subway line from assault flats beach to downtown
		id_line = transport_line_subway_blue_westbound,
		alias = [
			"bluewestline",
			"bluewest",
			"westblue",
			"bluetodowntown",
			"bluetodt"
			],
		first_stop = poi_id_afb_subway_station,
		last_stop = poi_id_dt_subway_station,
		next_line = transport_line_subway_blue_eastbound,
		str_name = "The blue subway line towards Downtown NLACakaNM",
		schedule = {
			poi_id_afb_subway_station : [20, poi_id_vc_subway_station],
			poi_id_vc_subway_station : [20, poi_id_jr_subway_station],
			poi_id_jr_subway_station : [20, poi_id_gld_subway_station],
			poi_id_gld_subway_station : [20, poi_id_dt_subway_station]
			}

		),
#	EwTransportLine( # white subway line from downtown to juvies row
#	 	id_line = transport_line_subway_white_eastbound,
#	 	alias = [
#	 		"whiteeastline",
#			"whiteeast",
#	 		"eastwhite",
#	 		"whitetojuviesrow",
#	 		"whitetojuvies",
#	 		"whitetojr"
#	 	    ],
#	 	first_stop = poi_id_underworld_subway_station,
#	 	last_stop = poi_id_jr_subway_station,
#	 	next_line = transport_line_subway_white_westbound,
#	 	str_name = "The white subway line towards Juvie's Row",
#	 	schedule = {
#	 		poi_id_underworld_subway_station : [20, poi_id_dt_subway_station],
#	 		poi_id_dt_subway_station : [20, poi_id_rr_subway_station],
#	 		poi_id_rr_subway_station : [20, poi_id_jr_subway_station]
#	 	    }
#	 	),
#	EwTransportLine( # white subway line from juvies row to downtown
#	 	id_line = transport_line_subway_white_westbound,
#	 	alias = [
#	 		"whitewestline",
#	 		"whitewest",
#	 		"westwhite",
#	 		"whitetounderworld",
#	 		"whitetouw"
#	 	    ],
#	 	first_stop = poi_id_jr_subway_station,
#	 	last_stop = poi_id_underworld_subway_station,
#	 	next_line = transport_line_subway_white_eastbound,
#	 	str_name = "The white subway line towards The Underworld",
#	 	schedule = {
#	 		poi_id_jr_subway_station : [20, poi_id_rr_subway_station],
#	 		poi_id_rr_subway_station : [20, poi_id_dt_subway_station],
#	 		poi_id_dt_subway_station : [20, poi_id_underworld_subway_station],
#	 	    }
#	 	),
	EwTransportLine( # blimp line from dreadford to assault flats beach
		id_line = transport_line_blimp_df_to_afb,
		alias = [
			"assaultflatsbeachblimp",
			"assaultflatsblimp",
			"beachblimp",
			"afbblimp",
			"blimptoassaultflatsbeach",
			"blimptoassaultflats",
			"blimptobeach",
			"blimptoafb"
			],
		first_stop = poi_id_df_blimp_tower,
		last_stop = poi_id_afb_blimp_tower,
		next_line = transport_line_blimp_afb_to_df,
		str_name = "The blimp line towards Assault Flats Beach",
		schedule = {
			poi_id_df_blimp_tower : [60, poi_id_jaywalkerplain],
			poi_id_jaywalkerplain : [40, poi_id_northsleezeborough],
			poi_id_northsleezeborough : [40, poi_id_krakbay],
			poi_id_krakbay : [40, poi_id_downtown],
			poi_id_downtown : [40, poi_id_greenlightdistrict],
			poi_id_greenlightdistrict : [40, poi_id_vagrantscorner],
			poi_id_vagrantscorner : [40, poi_id_afb_blimp_tower]
			}

		),
	EwTransportLine( # blimp line from assault flats beach to dreadford
		id_line = transport_line_blimp_afb_to_df,
		alias = [
			"dreadfordblimp",
			"dreadblimp",
			"dfblimp",
			"blimptodreadford",
			"blimptodread",
			"blimptodf"
			],
		first_stop = poi_id_afb_blimp_tower,
		last_stop = poi_id_df_blimp_tower,
		next_line = transport_line_blimp_df_to_afb,
		str_name = "The blimp line towards Dreadford",
		schedule = {
			poi_id_afb_blimp_tower : [60, poi_id_vagrantscorner],
			poi_id_vagrantscorner : [40, poi_id_greenlightdistrict],
			poi_id_greenlightdistrict : [40, poi_id_downtown],
			poi_id_downtown : [40, poi_id_krakbay],
			poi_id_krakbay : [40, poi_id_northsleezeborough],
			poi_id_northsleezeborough : [40, poi_id_jaywalkerplain],
			poi_id_jaywalkerplain : [40, poi_id_df_blimp_tower]
			}

		),
]

id_to_transport_line = {}

for line in transport_lines:
	id_to_transport_line[line.id_line] = line
	for alias in line.alias:
		id_to_transport_line[alias] = line

	for poi in transport_stops:
		poi_data = id_to_poi.get(poi)
		if (poi in line.schedule.keys()) or (poi == line.last_stop):
			poi_data.transport_lines.add(line.id_line)



landlocked_destinations ={
	poi_id_maimridge:poi_id_wreckington,
	poi_id_wreckington: poi_id_maimridge,
	poi_id_cratersville:poi_id_arsonbrook,
	poi_id_arsonbrook:poi_id_cratersville,
	poi_id_oozegardens:poi_id_brawlden,
	poi_id_brawlden:poi_id_oozegardens,
	poi_id_southsleezeborough:poi_id_newnewyonkers,
	poi_id_newnewyonkers:poi_id_southsleezeborough,
	poi_id_dreadford:poi_id_assaultflatsbeach,
	poi_id_assaultflatsbeach:poi_id_dreadford,
	poi_id_crookline:poi_id_assaultflatsbeach,
	poi_id_jaywalkerplain:poi_id_vagrantscorner,
	poi_id_vagrantscorner:poi_id_jaywalkerplain,
	poi_id_westglocksbury:poi_id_slimesendcliffs,
	poi_id_slimesendcliffs:poi_id_westglocksbury,
	poi_id_poloniumhill:poi_id_slimesend,
	poi_id_slimesend:poi_id_poloniumhill,
	poi_id_charcoalpark:poi_id_ferry,
	poi_id_ferry:poi_id_charcoalpark,
	poi_id_toxington:poi_id_ferry

}

#landlocked_destinations ={
#    poi_id_maimridge_street_c:poi_id_oozegardens_street_a, #Colloid->Festival
#    poi_id_oozegardens_street_a:poi_id_maimridge_street_c, #Festival->Colloid
#    poi_id_maimridge_street_b:poi_id_cratersville_street_a, #Ski Lodges->End Lines
#    poi_id_cratersville_street_a:poi_id_maimridge_street_b, #End Lines->Ski Lodges
#    poi_id_arsonbrook_street_c:poi_id_cratersville_street_c, #Tilly -> Dynamite
#    poi_id_cratersville_street_c:poi_id_arsonbrook_street_c, #Dynamite->Tilly
#    poi_id_arsonbrook_street_d:poi_id_oozegardens_street_d, #Crassus->Zoo
#    poi_id_oozegardens_street_d:poi_id_arsonbrook_street_d, #Zoo->Crassus
#    poi_id_crookline_street_a:poi_id_newnewyonkers_street_a, #Doxy->Concrete
#    poi_id_newnewyonkers_street_a:poi_id_crookline_street_a, #Concrete->Doxy
#    poi_id_newnewyonkers_street_b:poi_id_crookline_street_b, #Broadway->MacGuffin
#    poi_id_crookline_street_b:poi_id_newnewyonkers_street_b, #MacGuffin->Broadway
#    poi_id_brawlden_street_b:poi_id_southsleezeborough_street_a, #Brownstone->China
#    poi_id_southsleezeborough_street_a:poi_id_brawlden_street_b, #China->Brownstone
#    poi_id_assaultflatsbeach_street_b:poi_id_dreadford_street_b, #Beachfront->Hangem
#    poi_id_dreadford_street_b:poi_id_assaultflatsbeach_street_b, #Hangem->Beachfront
#    poi_id_vagrantscorner_street_a:poi_id_westglocksbury_street_c, #Wharf->Goosh
#    poi_id_westglocksbury_street_c:poi_id_vagrantscorner_street_a,#Goosh->Wharf
#    poi_id_poloniumhill_street_d:poi_id_ferry, #Sawdust->Ferry
#    poi_id_ferry:poi_id_poloniumhill_street_d, #Ferry->Sawdust
#    poi_id_slimesendcliffs:poi_id_poloniumhill_street_c, #Cliffs->Geller
#    poi_id_poloniumhill_street_c:poi_id_slimesendcliffs, #Geller->Cliffs
#    poi_id_wreckington_street_b:poi_id_toxington_street_c,#Scrapyard->Quarantined
#    poi_id_toxington_street_c:poi_id_wreckington_street_b,#Quarantined->Scrapyard
#    poi_id_brawlden_street_a:poi_id_southsleezeborough_street_a, #Abandoned->China
#    poi_id_westglocksbury_street_d:poi_id_vagrantscorner_street_a, #Highway->Wharf
#    poi_id_jaywalkerplain_street_d:poi_id_vagrantscorner_street_a, #Qoute->Wharf
#    poi_id_toxington_street_d:poi_id_ferry, #Carcinogen->Ferry
#    poi_id_dreadford_street_a:poi_id_assaultflatsbeach_street_b, #Scaffold->Beachfront
#    poi_id_charcoalpark_street_a:poi_id_wreckington_street_b, #Church->Scrapyard
#    poi_id_charcoalpark_street_b:poi_id_cratersville_street_a, #Veteran->Endline
#}





# Fashion styles for cosmetics
style_cool = "cool"
style_tough = "tough"
style_smart = "smart"
style_beautiful = "beautiful"
style_cute = "cute"

freshnesslevel_1 = 500
freshnesslevel_2 = 1000
freshnesslevel_3 = 2000
freshnesslevel_4 = 3000

# Base durability for cosmetic items (These are for if/when we need easy sweeping balance changes)
base_durability = 2500000 # 2.5 mega

generic_scalp_durability = 25000 # 25k
soul_durability = 100000000 # 100 mega

cosmetic_id_raincoat = "raincoat"

cosmeticAbility_id_lucky = "lucky"
cosmeticAbility_id_boost = "boost" # Not in use. Rollerblades have this ability.


#load EwCosmeticItems from json to cosmetic_items_list
cosmetic_items_list = []
with open(os.path.join('json', 'cosmetic_items.json')) as f:
	cosmetic_items = json.load(f)
	for i in cosmetic_items:
		i = cosmetic_items[i]
		cosmetic_items_list.append(
			EwCosmeticItem(
			id_cosmetic = i['id_cosmetic'],
			str_name = i['str_name'],
			str_desc = i['str_desc'],
			str_onadorn = i['str_onadorn'],
			str_unadorn = i['str_unadorn'],
			str_onbreak = i['str_onbreak'],
			rarity = i['rarity'],
			ability = i['ability'],
			durability = i['durability'],
			size = i['size'],
			style = i['style'],
			freshness = i['freshness'],
			ingredients = i['ingredients'],
			acquisition = i['acquisition'],
			price = i['price'],
			vendors = i['vendors'],
			is_hat = i['is_hat'],
		))


# A map of id_cosmetic to EwCosmeticItem objects.
cosmetic_map = {}


# A list of cosmetic names.
cosmetic_names = []

smelting_recipe_list = [
	EwSmeltingRecipe(
		id_recipe = "coolcosmetic",
		str_name = "a cool cosmetic",
		alias = [
			"cool",
			"coolhat",
		],
		ingredients = {
			item_id_slimepoudrin : 4,
			item_id_cool_material: 1
		},
		products = cosmetic_names
	),
	EwSmeltingRecipe(
		id_recipe = "toughcosmetic",
		str_name = "a tough cosmetic",
		alias = [
			"tough",
			"toughhat",
		],
		ingredients = {
			item_id_slimepoudrin : 4,
			item_id_tough_material: 1
		},
		products = cosmetic_names
	),
	EwSmeltingRecipe(
		id_recipe = "smartcosmetic",
		str_name = "a smart cosmetic",
		alias = [
			"smart",
			"smarthat",
		],
		ingredients = {
			item_id_slimepoudrin : 4,
			item_id_smart_material: 1
		},
		products = cosmetic_names
	),
	EwSmeltingRecipe(
		id_recipe = "beautifulcosmetic",
		str_name = "a beautiful cosmetic",
		alias = [
			"beautiful",
			"beautifulhat",
		],
		ingredients = {
			item_id_slimepoudrin : 4,
			item_id_beautiful_material: 1
		},
		products = cosmetic_names
	),
	EwSmeltingRecipe(
		id_recipe = "cutecosmetic",
		str_name = "a cute cosmetic",
		alias = [
			"cute",
			"cutehat",
		],
		ingredients = {
			item_id_slimepoudrin : 4,
			item_id_cute_material: 1
		},
		products = cosmetic_names
	),
	EwSmeltingRecipe(
		id_recipe = "knightarmor",
		str_name = "a set of Knight Armor",
				alias = [
			"armor",
		],
		ingredients = {
			item_id_ironingot : 2
		},
		products = ["knightarmor"]
	),
	EwSmeltingRecipe(
		id_recipe = item_id_monstersoup,
		str_name = "a bowl of Monster Soup",
		alias = [
			"soup",
			"meatsoup",
			"stew",
			"meatstew",
			"monstersoup",
			"monster soup"
		],
		ingredients = {
			item_id_monsterbones : 5,
			item_id_dinoslimemeat : 1
		},
		products = [item_id_monstersoup],
	),
	EwSmeltingRecipe(
		id_recipe=item_id_quadruplestuffedcrust,
		str_name="a Quadruple Stuffed Crust",
		alias=[
			"qsc",
			"quadruple",
			"quadruplestuffed",
		],
		ingredients={
			item_id_doublestuffedcrust: 2
		},
		products=[item_id_quadruplestuffedcrust],
	),
	EwSmeltingRecipe(
		id_recipe = item_id_octuplestuffedcrust,
		str_name = "an Octuple Stuffed Crust",
		alias = [
			"osc",
			"octuple",
			"octuplestuffed",
		],
		ingredients = {
			item_id_quadruplestuffedcrust : 2
		},
		products = [item_id_octuplestuffedcrust],
	),
	EwSmeltingRecipe(
		id_recipe = item_id_sexdecuplestuffedcrust,
		str_name = "a Sexdecuple Stuffed Crust",
		alias = [
			"sdsc",
			"sexdecuple",
			"sexdecuplestuffed",
		],
		ingredients = {
			item_id_octuplestuffedcrust : 2
		},
		products = [item_id_sexdecuplestuffedcrust],
	),
	EwSmeltingRecipe(
		id_recipe = item_id_duotrigintuplestuffedcrust,
		str_name = "a Duotrigintuple Stuffed Crust",
		alias = [
			"dtsc",
			"duotrigintuple",
			"duotrigintuplestuffed",
		],
		ingredients = {
			item_id_sexdecuplestuffedcrust : 2
		},
		products = [item_id_duotrigintuplestuffedcrust],
	),
	EwSmeltingRecipe(
		id_recipe = item_id_quattuorsexagintuplestuffedcrust,
		str_name = "a Quattuorsexagintuple Stuffed Crust",
		alias = [
			"qssc",
			"quattuorsexagintuple",
			"quattuorsexagintuplestuffed",
		],
		ingredients = {
			item_id_duotrigintuplestuffedcrust : 2
		},
		products = [item_id_quattuorsexagintuplestuffedcrust],
	),
	EwSmeltingRecipe(
		id_recipe = item_id_forbiddenstuffedcrust,
		str_name = "a Forbidden Stuffed Crust",
		alias = [
			"fsc",
			"forbiddenstuffedcrust",
		],
		ingredients = {
			item_id_quattuorsexagintuplestuffedcrust : 2,
			item_id_forbidden111 : 1
		},
		products = [item_id_forbiddenstuffedcrust],
	),
	EwSmeltingRecipe(
		id_recipe = item_id_forbidden111,
		str_name = "The Forbidden {}".format(emote_111),
		alias = [
			"forbiddenone",
			"forbidden",
			"sealed",
			"exodia",
			"oneoneone",
			"forbidden111",
			":111:",
		],
		ingredients = {
			'leftleg' : 1,
			'rightleg' : 1,
			'slimexodia' : 1,
			'rightarm' : 1,
			'leftarm' : 1
		},
		products = [item_id_forbidden111]
	),
	EwSmeltingRecipe(
		id_recipe = "pickaxe",
		str_name = "a Poudrin Pickaxe",
		alias = [
			"pp", # LOL
			"poudrinpick",
			"poudrinpickaxe",
			"pick"
		],
		ingredients = {
			item_id_slimepoudrin : 3,
			item_id_stick : 2
		},
		products = [weapon_id_pickaxe]
	),
	EwSmeltingRecipe(
		id_recipe = "faggot",
		str_name = "a Faggot",
		alias = [
			"f",
			"fag",
		],
		ingredients = {
			item_id_stick : 3
		},
		products = [item_id_faggot]
	),
	EwSmeltingRecipe(
		id_recipe = "doublefaggot",
		str_name = "a Double Faggot",
		alias = [
			"df",
			"dfag",
		],
		ingredients = {
			item_id_faggot : 2
		},
		products = [item_id_doublefaggot]
	),
	EwSmeltingRecipe(
		id_recipe = "dinoslimesteak",
		str_name = "a cooked piece of Dinoslime meat",
		alias = [
			"cookedmeat",
			"dss"
		],
		ingredients = {
			item_id_faggot : 1,
			item_id_dinoslimemeat : 1
		},
		products = [item_id_dinoslimesteak]
	),
	EwSmeltingRecipe(
		id_recipe = "fishingrod",
		str_name = "a fishing rod",
		alias = [
			"fish",
			"fishing",
			"rod",
			"fr"
		],
		ingredients = {
			item_id_string: 2,
			item_id_stick: 3
		},
		products = [weapon_id_fishingrod]
	),
	EwSmeltingRecipe(
		id_recipe = "bass",
		str_name = "a Bass Guitar",
		alias = [
			"bassguitar"
		],
		ingredients = {
			'thebassedgod' : 1,
			item_id_string : 4
		},
		products = [weapon_id_bass]
	),
	EwSmeltingRecipe(
		id_recipe = "bow",
		str_name = "a Minecraft Bow",
		alias = [
			"minecraft bow"
		],
		ingredients = {
			item_id_stick: 3,
			item_id_string: 3
		},
		products = [weapon_id_bow]
	),
		EwSmeltingRecipe(
		id_recipe = "ironingot",
		str_name = "an Iron Ingot",
		alias = [
			"ingot"
			"metal",
			"ironingot",
			"iron ingot"
		],
		ingredients = {
			item_id_tincan:10,
			item_id_faggot:1
		},
		products = [item_id_ironingot]
	),
		EwSmeltingRecipe(
		id_recipe = "tanningknife",
		str_name = "a small tanning knife",
		alias = [
			"knife",
			"tanningknife",
			"tanning"
		],
		ingredients = {
			item_id_ironingot:1
		},
		products = [item_id_tanningknife]
	),
		EwSmeltingRecipe(
		id_recipe = "leather",
		str_name = "a piece of leather",
		alias = [
			"leather"
		],
		ingredients = {
			item_id_oldboot:10,
			item_id_tanningknife:1
		},
		products = [item_id_leather]
	),
		EwSmeltingRecipe(
		id_recipe = "bloodstone",
		str_name = "a chunk of bloodstone",
		alias = [
			"bloodstone",
			"bstone"
		],
		ingredients = {
			item_id_monsterbones:100,
			item_id_faggot:1
		},
		products = [item_id_bloodstone]
	),
		EwSmeltingRecipe(
		id_recipe = "dclaw",
		str_name = "a Dragon Claw",
		alias = [
			"dragonclaw",
			"claw",
			"dclaw"
		],
		ingredients = {
			item_id_dragonsoul: 1,
			item_id_slimepoudrin: 5,
			item_id_ironingot: 1,
			item_id_leather: 1
		},
		products = [weapon_id_dclaw]
	),
	EwSmeltingRecipe(
		id_recipe = weapon_id_staff,
		str_name = "an eldritch staff",
		alias = [
			"eldritchstaff",
			"spookystaff",
			"reprehensiblerod",
			"wickedwand",
			"frighteningfaggot"
		],
		ingredients = {
			item_id_doublefaggot : 1,
			item_id_negapoudrin : 1,
		},
		products = [weapon_id_staff]
	),

	EwSmeltingRecipe(
		id_recipe = "leathercouch",
		str_name = "a leather couch",
		alias = [
			"humancouch"
		],
		ingredients = {
			'couch': 1,
			'scalp': 10
		},
		products = ['leathercouch']
	),
	EwSmeltingRecipe(
		id_recipe = "leatherchair",
		str_name = "a leather chair",
		alias = [
			"humanchair"
		],
		ingredients = {
			'chair': 1,
			'scalp': 5
		},
		products = ['leatherchair']
	),
	EwSmeltingRecipe(
		id_recipe = "leatherlamp",
		str_name = "a leather coated lamp",
		alias = [
			"humanlamp"
		],
		ingredients = {
			'lamp': 1,
			'scalp': 3
		},
		products = ['leatherlamp']
	),
	EwSmeltingRecipe(
		id_recipe = "leatherdesk",
		str_name = "a leather desk",
		alias = [
			"humandesk"
		],
		ingredients = {
			'desk': 1,
			'scalp': 4
		},
		products = ['leatherdesk']
	),
	EwSmeltingRecipe(
		id_recipe = "leatherbed",
		str_name = "a leather bed",
		alias = [
			"humanbed"
		],
		ingredients = {
			'bed': 1,
			'scalp': 12
		},
		products = ['leatherbed']
	),
	EwSmeltingRecipe(
		id_recipe = "seaweedjoint",
		str_name = "a seaweed joint",
		alias = [
			"joint",
			"seaweed",
			"weed",
			"doobie",
			"blunt"
		],
		ingredients = {
			item_id_seaweed: 3,
			item_id_dankwheat: 1,
			item_id_slimepoudrin : 1,
		},
		products = [item_id_seaweedjoint]
	),
	EwSmeltingRecipe(
		id_recipe = "slimepoudrin",
		str_name = "a slime poudrin",
		alias = [
			"poudrin",
			"poud",
			"pou",
			"poodrin",
		],
		ingredients = {
			item_id_royaltypoudrin: 2
		},
		products = [item_id_slimepoudrin]
	),
	EwSmeltingRecipe(
		id_recipe = "humancorpse",
		str_name = "a corpse",
		alias = [
			"stiff",
			"corpse",
			"deadperson",
			"cadaver",
		],
		ingredients = {
			'scalp': 20,
			item_id_dinoslimemeat: 2,
			item_id_string :2
		},
		products = ['humancorpse']
	),
	EwSmeltingRecipe(
		id_recipe = "popeonarope",
		str_name = "a pope on a rope",
		alias = [
			"pope",
			"francis",
			"deadpope",
			"sacrilege",
		],
		ingredients = {
			'humancorpse': 1,
			'diadem':1,
			'scarf':1,
			'confessionbooth':1
		},
		products = ['popeonarope']
	),
	EwSmeltingRecipe(
		id_recipe = "reanimatedcorpse",
		str_name = "a reanimated corpse",
		alias = [
			"frankenstein",
			"reanimate",
			"revenant",
		],
		ingredients = {
			'humancorpse': 1,
			'soul':1,
		},
		products = ['reanimatedcorpse']
	),
	EwSmeltingRecipe(
		id_recipe = "soul",
		str_name = "a soul",
		alias = [
			"spirit",
			"essence",
			"hippiebullshit",
		],
		ingredients = {
			'reanimatedcorpse': 1,
		},
		products = ['soul']
	),
	EwSmeltingRecipe(
		id_recipe = "humanskeleton",
		str_name = "a human skeleton",
		ingredients = {
			'bone': 206,
		},
		products = ['humanskeleton']
	),
	EwSmeltingRecipe(
		id_recipe = "monsterskeleton",
		str_name = "a wild beast's skeleton",
		ingredients = {
			item_id_monsterbones: 200,
		},
		products = ['dinoslimeskeleton', 'slimeadactylskeleton', 'mammoslimeskeleton', 'slimeasaurusskeleton', 'slimedragonskeleton']
	),
	EwSmeltingRecipe(
		id_recipe = "handmadechair",
		str_name = "a handmade chair",
		alias = [
			"woodchair",
			"carvedchair",
			"woodenchair",
			"ornatechair",
		],
		ingredients = {
			item_id_stick: 5,
			weapon_id_bat:2,
		},
		products = ['ornatechair', 'shittychair']
	),
	EwSmeltingRecipe(
		id_recipe = "handmadebench",
		str_name = "a handmade bench",
		alias = [
			"woodbench",
			"carvedbench",
			"woodenbench",
			"ornatebench",
		],
		ingredients = {
			item_id_stick: 10,
			weapon_id_bat: 4,
		},
		products = ['ornatebench', 'shittybench']
	),
	EwSmeltingRecipe(
		id_recipe = "handmadebed",
		str_name = "a handmade bed",
		alias = [
			"woodbed",
			"carvedbed",
			"woodenbed",
			"ornatebed",
		],
		ingredients = {
			item_id_stick: 12,
			weapon_id_bat :3,
		},
		products = ['ornatebed', 'shittybed']
	),
	EwSmeltingRecipe(
		id_recipe = "handmadedesk",
		str_name = "a handmade desk",
		alias = [
			"wooddesk",
			"carveddesk",
			"woodendesk",
			"ornatedesk",
		],
		ingredients = {
			item_id_stick: 4,
			weapon_id_bat: 1,
		},
		products = ['ornatedesk', 'shittydesk']
	),
	EwSmeltingRecipe(
		id_recipe = "clarinet",
		str_name = "a clarinet",
		alias = [
			"flute",
			"bennygoodmanthing",
			"vuvuzela",
		],
		ingredients = {
			'bat': 1,
			'razornuts':1,
			'knives':1,
			'blacklimes':1,
			'direappleciderfuckenergy':1,
			'sweetfish':1,
		},
		products = ['craftsmansclarinet', 'woodenvuvuzela']
	),
	EwSmeltingRecipe(
		id_recipe = "guitar",
		str_name = "a solid poudrin guitar",
		alias = [
			"poudringuitar",
			"electricguitar",
			"solidpoudringuitar",
		],
		ingredients = {
			item_id_slimepoudrin: 150,
			item_id_string: 6,
		},
		products = ['solidpoudringuitar']
	),
	EwSmeltingRecipe(
		id_recipe = "drums",
		str_name = "a beast skin drums",
		alias = [
			"beastskindrums",
			"drumset",
			"drum",
		],
		ingredients = {
			'dinoslimemeat': 5,
			'dinoslimesteak' : 2,
			'scalp': 5,
			'string' : 3,
			'stick' : 2
		},
		products = ['beastskindrums']
	),
	EwSmeltingRecipe(
		id_recipe = "xylophone",
		str_name = "a fish bone xylophone",
		alias = [
			"xylo",
			"metallophone",
			"fishbonexylophone",
		],
		ingredients = {
			'nuclearbream' : 1,
			'largebonedlionfish' : 2,
			'plebefish':3,
			'sweetfish':1,
			'stick':1
		},
		products = ['fishbonexylophone']
	),
	EwSmeltingRecipe(
		id_recipe = "maracas",
		str_name = "a gourd maracas",
		alias = [
			"gourdmaracas",
			"shakers",
			"rattle",
		],
		ingredients = {
			'pulpgourds': 1,
			'suganmanuts': 1,
			'sludgeberries':1,
			'razornuts':1,
			'joybeans':1,
			'phosphorpoppies':1
		},
		products = ['gourdmaracas']
	),
	EwSmeltingRecipe(
		id_recipe = "saxophone",
		str_name = "a saxophone",
		alias = [
			"sax",
			"saxamaphone",
		],
		ingredients = {
			weapon_id_shotgun: 1,
			'earlbrowntea': 1,
			item_id_metallicapheads: 4,
			item_id_cute_material: 10,
			item_id_aushuckstalks: 1,
			item_id_slimepoudrin: 5,
		},
		products = ['saxophone']
	),
	EwSmeltingRecipe(
		id_recipe="cornet",
		str_name="a cornet",
		alias=[
			"trumpet",
			"horn",
			"trump"
		],
		ingredients={
			weapon_id_slimeringcan: 1,
			'goobalibre': 1,
			item_id_steelbeanpods: 2,
			item_id_tough_material: 10,
			item_id_aushuckstalks: 2,
			item_id_slimepoudrin: 6,
		},
		products=['cornet']
	),
	EwSmeltingRecipe(
		id_recipe="trombone",
		str_name="a trombone",
		alias=[
			"tbone",
			"bestinstrument",
			"sackbut"
		],
		ingredients={
			weapon_id_shotgun: 2,
			'manhattanproject': 1,
			item_id_metallicapheads: 1,
			item_id_smart_material: 10,
			item_id_aushuckstalks: 3,
			item_id_slimepoudrin: 10,
		},
		products=['trombone']
	),
	EwSmeltingRecipe(
		id_recipe="whitedye",
		str_name="a vial of White Dye",
		alias=[
			'white',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_poketubereyes: 1,
		},
		products=[item_id_dye_white]
	),
	EwSmeltingRecipe(
		id_recipe="yellowdye",
		str_name="a vial of Yellow Dye",
		alias=[
			'yellow',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_pulpgourdpulp: 1,
		},
		products=[item_id_dye_yellow]
	),
	EwSmeltingRecipe(
		id_recipe="orangedye",
		str_name="a vial of Orange Dye",
		alias=[
			'orange',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_sourpotatoskins: 1,
		},
		products=[item_id_dye_orange]
	),
	EwSmeltingRecipe(
		id_recipe="reddye",
		str_name="a vial of Red Dye",
		alias=[
			'red',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_bloodcabbageleaves: 1,
		},
		products=[item_id_dye_red]
	),
	EwSmeltingRecipe(
		id_recipe="magentadye",
		str_name="a vial of Magenta Dye",
		alias=[
			'magenta',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_joybeanvines: 1,
		},
		products=[item_id_dye_magenta]
	),
	EwSmeltingRecipe(
		id_recipe="purpledye",
		str_name="a vial of Purple Dye",
		alias=[
			'purple',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_purplekilliflowerflorets: 1,
		},
		products=[item_id_dye_purple]
	),
	EwSmeltingRecipe(
		id_recipe="bluedye",
		str_name="a vial of Blue Dye",
		alias=[
			'blue',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_razornutshells: 1,
		},
		products=[item_id_dye_blue]
	),
	EwSmeltingRecipe(
		id_recipe="greendye",
		str_name="a vial of Green Dye",
		alias=[
			'green',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_pawpawflesh: 1,
		},
		products=[item_id_dye_green]
	),
	EwSmeltingRecipe(
		id_recipe="tealdye",
		str_name="a vial of Teal Dye",
		alias=[
			'teal',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_sludgeberrysludge: 1,
		},
		products=[item_id_dye_teal]
	),
	EwSmeltingRecipe(
		id_recipe="rainbowdye",
		str_name="a vial of ***Rainbow Dye***",
		alias=[
			'rainbow',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_suganmanutfruit: 1,
		},
		products=[item_id_dye_rainbow]
	),
	EwSmeltingRecipe(
		id_recipe="pinkdye",
		str_name="a vial of Pink Dye",
		alias=[
			'pink',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_pinkrowddishroot: 1,
		},
		products=[item_id_dye_pink]
	),
	EwSmeltingRecipe(
		id_recipe="greydye",
		str_name="a vial of Grey Dye",
		alias=[
			'grey',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_dankwheatchaff: 1,
		},
		products=[item_id_dye_grey]
	),
	EwSmeltingRecipe(
		id_recipe="cobaltdye",
		str_name="a vial of Cobalt Dye",
		alias=[
			'cobalt',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_brightshadeberries: 1,
		},
		products=[item_id_dye_cobalt]
	),
	EwSmeltingRecipe(
		id_recipe="blackdye",
		str_name="a vial of Black Dye",
		alias=[
			'black',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_blacklimeade: 1,
		},
		products=[item_id_dye_black]
	),
	EwSmeltingRecipe(
		id_recipe="limedye",
		str_name="a vial of Lime Dye",
		alias=[
			'lime',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_phosphorpoppypetals: 1,
		},
		products=[item_id_dye_lime]
	),
	EwSmeltingRecipe(
		id_recipe="cyandye",
		str_name="a vial of Cyan Dye",
		alias=[
			'cyan',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_direapplestems: 1,
		},
		products=[item_id_dye_cyan]
	),
	EwSmeltingRecipe(
		id_recipe="browndye",
		str_name="a vial of Brown dye",
		alias=[
			'brown',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_rustealeafblades: 1,
		},
		products=[item_id_dye_brown]
	),
	EwSmeltingRecipe(
		id_recipe="copperpaint",
		str_name="a bucket of Copper Paint",
		alias=[
			'copper',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_metallicapheads: 1,
		},
		products=[item_id_paint_copper]
	),
	EwSmeltingRecipe(
		id_recipe="chromepaint",
		str_name="a bucket of Chrome Paint",
		alias=[
			'chrome',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_steelbeanpods: 1,
		},
		products=[item_id_paint_chrome]
	),
	EwSmeltingRecipe(
		id_recipe="goldpaint",
		str_name="a bucket of Gold Paint",
		alias=[
			'gold',
		],
		ingredients={
			item_id_dyesolution: 1,
			item_id_aushuckstalks: 1,
		},
		products=[item_id_paint_gold]
	),
	EwSmeltingRecipe(
		id_recipe="jellyfilleddoughnut",
		str_name="a Jelly Filled Donut",
		alias=[
			'donut',
			'doughnut',
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_poketubereyes: 1,
		},
		products=["jellyfilleddoughnut"]
	),
	EwSmeltingRecipe(
		id_recipe="pulpgourdpie",
		str_name="a plate of Pulp Gourd Pie",
		alias=[
			'pie',
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_pulpgourdpulp: 1,
		},
		products=['pulpgourdpie']
	),
	EwSmeltingRecipe(
		id_recipe="sourpotatofrenchfries",
		str_name="a plate of Sour Potato French Fries",
		alias=[
			'fries',
			'frenchfries'
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_sourpotatoskins: 1,
		},
		products=['sourpotatofrenchfries']
	),
	EwSmeltingRecipe(
		id_recipe="bloodcabbagecoleslaw",
		str_name="a tub of Blood Cabbage Coleslaw",
		alias=[
			'coleslaw',
			'redcoleslaw',
			'blood'
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_bloodcabbageleaves: 1,
		},
		products=['bloodcabbagecoleslaw']
	),
	EwSmeltingRecipe(
		id_recipe="joybeanpastemochi",
		str_name="a pile of Joybean Paste Mochi",
		alias=[
			'mochi',
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_joybeanvines: 1,
		},
		products=['joybeanpastemochi']
	),
	EwSmeltingRecipe(
		id_recipe="purplekilliflowercrustpizza",
		str_name="a plate of Purple Killiflower Crust Pizza",
		alias=[
			'pizza',
			'cauliflowercrustpizza'
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_purplekilliflowerflorets: 1,
		},
		products=['purplekilliflowercrustpizza']
	),
	EwSmeltingRecipe(
		id_recipe="razornutbutter",
		str_name="a tub of Razornut Butter",
		alias=[
			'butter',
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_razornutshells: 1,
		},
		products=['razornutbutter']
	),
	EwSmeltingRecipe(
		id_recipe="pawpawfood",
		str_name="a plate of Pawpaw Food",
		alias=[
			'food',
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_pawpawflesh: 1,
		},
		products=['pawpawfood']
	),
	EwSmeltingRecipe(
		id_recipe="sludgeberrypancakes",
		str_name="a plate of Sludgeberry Pancakes",
		alias=[
			'pancakes',
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_sludgeberrysludge: 1,
		},
		products=['sludgeberrypancakes']
	),
	EwSmeltingRecipe(
		id_recipe="yourfavoritefood",
		str_name="a plate of ***Your Favorite Food***",
		alias=[
			'favoritefood',
			'favefood'
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_suganmanutfruit: 1,
		},
		products=['yourfavoritefood']
	),
	EwSmeltingRecipe(
		id_recipe="pinkrowdatouille",
		str_name="a plate of Pink Rowdatouille",
		alias=[
			'rowdatouille',
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_pinkrowddishroot: 1,
		},
		products=['pinkrowdatouille']
	),
	EwSmeltingRecipe(
		id_recipe="dankwheattoast",
		str_name="a plate of Dankwheat Toast",
		alias=[
			'toast',
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_dankwheatchaff: 1,
		},
		products=['dankwheattoast']
	),
	EwSmeltingRecipe(
		id_recipe="brightshadeseeds",
		str_name="some Brightshade Seeds",
		alias=[
			'seeds',
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_brightshadeberries: 1,
		},
		products=['brightshadeseeds']
	),
	EwSmeltingRecipe(
		id_recipe="blacklimesour",
		str_name="some Black Lime Sours",
		alias=[
			'sours',
			'sour'
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_blacklimeade: 1,
		},
		products=['blacklimesour']
	),
	EwSmeltingRecipe(
		id_recipe="phosphorpoppiesmuffin",
		str_name="a Phosphorpoppies Muffin",
		alias=[
			'muffin',
			'muffins'
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_phosphorpoppypetals: 1,
		},
		products=['phosphorpoppiesmuffin']
	),
	EwSmeltingRecipe(
		id_recipe="direapplejuice",
		str_name="a bottle of Dire Apple Juice",
		alias=[
			'juice',
			'applejuice',
			'appyjuice'
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_direapplestems: 1,
		},
		products=['direapplejuice']
	),
	EwSmeltingRecipe(
		id_recipe="earlbrowntea",
		str_name="a cup of Earl Brown Tea",
		alias=[
			'tea',
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_rustealeafblades: 1,
		},
		products=['earlbrowntea']
	),
	EwSmeltingRecipe(
		id_recipe="badshroomz",
		str_name="some Bad Shroomz",
		alias=[
			'shrooms',
			'mushrooms',
			'shroomz'
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_metallicapheads: 1,
		},
		products=['badshroomz']
	),
	EwSmeltingRecipe(
		id_recipe="chromaccino",
		str_name="a Chromaccino",
		alias=[
			'cappuccino',
			'chroma'
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_steelbeanpods: 1,
		},
		products=['chromaccino']
	),
	EwSmeltingRecipe(
		id_recipe="moltenpopcorn",
		str_name="a bag of Molten Popcorn",
		alias=[
			'popcorn',
		],
		ingredients={
			item_id_foodbase: 1,
			item_id_aushuckstalks: 1
		},
		products=['moltenpopcorn']
	),
	EwSmeltingRecipe(
		id_recipe="captainshat",
		str_name="a Captain's Hat",
		alias=[
			'captain',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_poketubereyes: 1,
		},
		products=['captainshat']
	),
	EwSmeltingRecipe(
		id_recipe="juveolantern",
		str_name="a Juve-O' Lantern",
		alias=[
			'juve',
			'jackolantern'
		],
		ingredients={
			item_id_textiles: 1,
			item_id_pulpgourdpulp: 1,
		},
		products=['juveolantern']
	),
	EwSmeltingRecipe(
		id_recipe="bowlerhat",
		str_name="a Bowler Hat",
		alias=[
			'bowler',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_sourpotatoskins: 1,
		},
		products=['bowlerhat']
	),
	EwSmeltingRecipe(
		id_recipe="cabbagetreehat",
		str_name="a Cabbage Tree Hat",
		alias=[
			'cabbagehat',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_bloodcabbageleaves: 1,
		},
		products=['cabbagetreehat']
	),
	EwSmeltingRecipe(
		id_recipe="braces",
		str_name="some Braces",
		alias=[
			'headgear',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_joybeanvines: 1,
		},
		products=['braces']
	),
	EwSmeltingRecipe(
		id_recipe="hoodie",
		str_name="a Hoodie",
		alias=[
			'hood',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_purplekilliflowerflorets: 1,
		},
		products=['hoodie']
	),
	EwSmeltingRecipe(
		id_recipe="copbadge",
		str_name="a Cop Badge",
		alias=[
			'badge',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_razornutshells: 1,
		},
		products=['copbadge']
	),
	EwSmeltingRecipe(
		id_recipe="strawhat",
		str_name="a Straw Hat",
		alias=[
			'straw',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_pawpawflesh: 1,
		},
		products=['strawhat']
	),
	EwSmeltingRecipe(
		id_recipe="cosplayhorns",
		str_name="a pair of Cosplay Horns",
		alias=[
			'horns',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_sludgeberrysludge: 1,
		},
		products=['cosplayhorns']
	),
	EwSmeltingRecipe(
		id_recipe="yourfavoritehat",
		str_name="***Your Favorite Hat***",
		alias=[
			'favoritehat',
			'favehat'
		],
		ingredients={
			item_id_textiles: 1,
			item_id_suganmanutfruit: 1,
		},
		products=['yourfavoritehat']
	),
	EwSmeltingRecipe(
		id_recipe="pajamaonesie",
		str_name="a Pajama Onesie",
		alias=[
			'pajamas',
			'onesie'
		],
		ingredients={
			item_id_textiles: 1,
			item_id_pinkrowddishroot: 1,
		},
		products=['pajamaonesie']
	),
	EwSmeltingRecipe(
		id_recipe="pairofcircularsunglasses",
		str_name="a Pair Of Circular Sunglasses",
		alias=[
			'digibroglasses',
			'circleglasses',
			'circularglasses'
		],
		ingredients={
			item_id_textiles: 1,
			item_id_dankwheatchaff: 1,
		},
		products=['pairofcircularsunglasses']
	),
	EwSmeltingRecipe(
		id_recipe="flowercrown",
		str_name="a Flower Crown",
		alias=[
			'flower',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_brightshadeberries: 1,
		},
		products=['flowercrown']
	),
	EwSmeltingRecipe(
		id_recipe="spikedbracelets",
		str_name="a pair of Spiked Bracelets",
		alias=[
			'spiked',
			'bracelets'
		],
		ingredients={
			item_id_textiles: 1,
			item_id_blacklimeade: 1,
		},
		products=['spikedbracelets']
	),
	EwSmeltingRecipe(
		id_recipe="slimecorppin",
		str_name="a SlimeCorp Pin",
		alias=[
			'pin',
			'shillpin',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_phosphorpoppypetals: 1,
		},
		products=['slimecorppin']
	),
	EwSmeltingRecipe(
		id_recipe="overalls",
		str_name="a pair of Overalls",
		alias=[
			'trousers',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_direapplestems: 1,
		},
		products=['overalls']
	),
	EwSmeltingRecipe(
		id_recipe="rustynail",
		str_name="a Rusty Nail",
		alias=[
			'nail',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_rustealeafblades: 1,
		},
		products=['rustynail']
	),
	EwSmeltingRecipe(
		id_recipe="fullmetaljacket",
		str_name="a Full Metal Jacket",
		alias=[
			'jacket',
			'metaljacket'
		],
		ingredients={
			item_id_textiles: 1,
			item_id_metallicapheads: 1,
		},
		products=['fullmetaljacket']
	),
	EwSmeltingRecipe(
		id_recipe="tinfoilhat",
		str_name="a Tinfoil Hat",
		alias=[
			'tinfoil',
		],
		ingredients={
			item_id_textiles: 1,
			item_id_steelbeanpods: 1,
		},
		products=['tinfoilhat']
	),
	EwSmeltingRecipe(
		id_recipe="resplendentcoronet",
		str_name="a Resplendent Coronet",
		alias=[
			'crown',
			'goldcrown'
		],
		ingredients={
			item_id_textiles: 1,
			item_id_aushuckstalks: 1,
		},
		products=['resplendentcoronet']
	),
	EwSmeltingRecipe(
		id_recipe="stick",
		str_name="a stick",
		alias=[
			'wood',
		],
		ingredients={
			item_id_direapplestems: 3
		},
		products=[item_id_stick]
	),
	EwSmeltingRecipe(
        id_recipe="rollerblades",
        str_name="a pair of rollerblades",
        alias=[
            'rollerblades',
            'inlineskates',
            'skates',
            'jsr'
        ],
        ingredients={
            item_id_oldboot: 2, # Shoes
            item_id_slimepoudrin: 8, # Wheels
            item_id_leather: 1, # Buckles
            item_id_string: 2, # Laces
        },
        products=["rollerblades"]
    ),
	EwSmeltingRecipe(
		id_recipe="ferroslimeoid",
		str_name="a ferroslimeoid",
		alias=[
			'ferroslimeoid',
			'magnet'
		],
		ingredients={
			item_id_tincan: 2,  # metal dust
			item_id_slimepoudrin: 5,  # lifeforce
			item_id_string: 1,  # Scarf/tether
		},
		products=["ferroslimeoid"]
	)
	# TODO remove after double halloween
	#EwSmeltingRecipe(
    #    id_recipe = "ticket",
    #    str_name = "Ticket to the White Line",
    #    alias = [
    #        "tickettohell",
    #    ],
    #    ingredients = {
    #        item_id_doublehalloweengrist: 100,
    #    },
    #    products = ['ticket']
    #)
]
#smelting_recipe_list += ewdebug.debugrecipes

# A map of id_recipe to EwSmeltingRecipe objects.
smelting_recipe_map = {}

# A list of recipe names
recipe_names = []

# Populate recipe map, including all aliases.
for recipe in smelting_recipe_list:

	# print("==============================\n\n{}\n――――――――――――――――――――――――――――――\nTo craft {}, you'll need...\n".format(recipe.str_name, recipe.str_name))
	# for ingredient in recipe.ingredients.keys():
	# 	print('{} {}'.format(recipe.ingredients[ingredient], ingredient))
	# print('')
	
	smelting_recipe_map[recipe.id_recipe] = recipe
	recipe_names.append(recipe.id_recipe)

	for alias in recipe.alias:
		smelting_recipe_map[alias] = recipe


# Slimeoid attributes.
slimeoid_strat_attack = "attack"
slimeoid_strat_evade = "evade"
slimeoid_strat_block = "block"

slimeoid_weapon_blades = "blades"
slimeoid_weapon_teeth = "teeth"
slimeoid_weapon_grip = "grip"
slimeoid_weapon_bludgeon = "bludgeon"
slimeoid_weapon_spikes = "spikes"
slimeoid_weapon_electricity = "electricity"
slimeoid_weapon_slam = "slam"

slimeoid_armor_scales = "scales"
slimeoid_armor_boneplates = "boneplates"
slimeoid_armor_quantumfield = "quantumfield"
slimeoid_armor_formless = "formless"
slimeoid_armor_regeneration = "regeneration"
slimeoid_armor_stench = "stench"
slimeoid_armor_oil = "oil"

slimeoid_special_spit = "spit"
slimeoid_special_laser = "laser"
slimeoid_special_spines = "spines"
slimeoid_special_throw = "throw"
slimeoid_special_TK = "TK"
slimeoid_special_fire = "fire"
slimeoid_special_webs = "webs"

# All body attributes in the game.
body_list = [
	EwBody( # body 1
		id_body = "teardrop",
		alias = [
			"tear",
			"drop",
			"oblong",
			"a"
		],
		str_create = "You press a button on the body console labelled 'A'. Through the observation port, you see the rapidly congealing proto-Slimeoid take on a roughly teardrop-shaped form.",
		str_body = "It is teardrop-shaped.",
		str_observe = "{slimeoid_name} is bobbing its top-heavy body back and forth."
	),
	EwBody( # body 2
		id_body = "wormlike",
		alias = [
			"long",
			"serpent",
			"serpentine",
			"b"
		],
		str_create = "You press a button on the body console labelled 'B'. Through the observation port, you see the rapidly congealing proto-Slimeoid begin to stretch into an elongated form.",
		str_body = "It is long and wormlike.",
		str_observe = "{slimeoid_name} is twisting itself around, practicing tying its knots."
	),
	EwBody( # body 3
		id_body = "spherical",
		alias = [
			"sphere",
			"orb",
			"ball",
			"c"
		],
		str_create = "You press a button on the body console labelled 'C'. Through the observation port, you see the rapidly congealing proto-Slimeoid take on a roughly spherical form.",
		str_body = "It is generally orb-shaped.",
		str_observe = "{slimeoid_name} flops over onto one side of its round body."
	),
	EwBody( # body 4
		id_body = "humanoid",
		alias = [
			"biped",
			"human",
			"d"
		],
		str_create = "You press a button on the body console labelled 'D'. Through the observation port, you see the rapidly congealing proto-Slimeoid curl into a foetal, vaguely humanoid form.",
		str_body = "It is vaguely humanoid.",
		str_observe = "{slimeoid_name} is scraping at something on the ground with its arms."
	),
	EwBody( # body 5
		id_body = "tentacled",
		alias = [
			"squid",
			"squidlike",
			"tentacle",
			"tentacles",
			"e"
		],
		str_create = "You press a button on the body console labelled 'E'. Through the observation port, you see the rapidly congealing proto-Slimeoid begin to sprout long tendrils from its nucleus.",
		str_body = "It is a mass of tendrils.",
		str_observe = "{slimeoid_name} is moving its tentacles around, running them over one another."
	),
	EwBody( # body 6
		id_body = "amorphous",
		alias = [
			"none",
			"formless",
			"f"
		],
		str_create = "You press a button on the body console labelled 'F'. Through the observation port, you see the rapidly congealing proto-Slimeoid accreting itself together with no distinct shape to speak of.",
		str_body = "It has no defined shape.",
		str_observe = "{slimeoid_name}'s body is spread out on the floor like a kind of living puddle."
	),
	EwBody( # body 7
		id_body = "quadruped",
		alias = [
			"animal",
			"g"
		],
		str_create = "You press a button on the body console labelled 'G'. Through the observation port, you see the rapidly congealing proto-Slimeoid beginning to grow bones and vertebrae as it starts to resemble some kind of quadruped.",
		str_body = "It has a body shape vaguely reminiscent of a quadruped.",
		str_observe = "{slimeoid_name} has its hindquarters lowered in a sort of sitting position."
	)
]

# A map of id_body to EwBody objects.
body_map = {}

# A list of body names
body_names = []

# Populate body map, including all aliases.
for body in body_list:
	body_map[body.id_body] = body
	body_names.append(body.id_body)

	for alias in body.alias:
		body_map[alias] = body

# All head attributes in the game.
head_list = [
	EwHead( # head 1
		id_head = "eye",
		alias = [
			"cyclops",
			"a"
		],
		str_create = "You press a button on the head console labelled 'A'. Through the observation port, you see a dark cluster within the proto-Slimeoid begin to form into what looks like a large eye.",
		str_head = "Its face is a single huge eye.",
		str_feed = "{slimeoid_name} swallows the {food_name} whole.",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name}'s huge eye follows the ball's arc, and it makes a leap to catch it!!\n\n...only to get socked right in the eye, sending it to the floor in pain. Depth perception... it's truly a gift."
	),
	EwHead( # head 2
		id_head = "maw",
		alias = [
			"mouth",
			"b"
		],
		str_create = "You press a button on the head console labelled 'B'. Through the observation port, you see an opening form in what you think is the proto-Slimeoid's face, which begins to sprout large pointed teeth.",
		str_head = "Its face is a huge toothy mouth.",
		str_feed = "{slimeoid_name} crunches the {food_name} to paste with its huge teeth.",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} slavers and drools as it awaits the throw, and when it sees the ball start to fly, it lunges to grab it out of the air in its huge toothy maw, slicing it to shreds with its teeth in seconds."
	),
	EwHead( # head 3
		id_head = "void",
		alias = [
			"hole",
			"c"
		],
		str_create = "You press a button on the head console labelled 'C'. Through the observation port, you see what you thought was the proto-Slimeoid's face suddenly sucked down into its body, as though by a black hole.",
		str_head = "Its face is an empty black void.",
		str_feed = "The {food_name} disappears into the unknowable depths of {slimeoid_name}'s face hole.",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} positions itself to catch the ball in it's... face? The ball falls into the empty void of {slimeoid_name}'s face, then just keeps falling, falling, falling, down into the depths, falling so far it disappears forever."
	),
	EwHead( # head 4
		id_head = "beast",
		alias = [
			"animal",
			"dragon",
			"d"
		],
		str_create = "You press a button on the head console labelled 'D'. Through the observation port, you see the beginnings of an animal-like face forming on your proto-Slimeoid, with what might be eyes, a nose, teeth... maybe.",
		str_head = "Its face is that of a vicious beast.",
		str_feed = "{slimeoid_name} gobbles up the {food_name} greedily.",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} focuses its eyes and bares its teeth, then makes a flying leap, snapping the ball clean out of the air in its jaws! It comes back to you and drops the ball at your feet. Good boy!"
	),
	EwHead( # head 5
		id_head = "insect",
		alias = [
			"bug",
			"insectoid",
			"e"
		],
		str_create = "You press a button on the head console labelled 'E'. Through the observation port, you see the proto-Slimeoid suddenly bulge with a series of hard orbs which congeal into what appear to be large compound eyes.",
		str_head = "It has bulging insectoid eyes and mandibles.",
		str_feed = "{slimeoid_name} cuts the {food_name} into pieces with its mandibles.",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} stands motionless, presumably watching the ball with its large compound eyes, before darting toward it as it sails through the air, snapping its mandibles around the ball and slicing it cleanly in two."
	),
	EwHead( # head 6
		id_head = "skull",
		alias = [
			"skeleton",
			"f"
		],
		str_create = "You press a button on the head console labelled 'F'. Through the observation port, you see the proto-Slimeoid's frontal features twist into a ghastly death's-head.",
		str_head = "Its face resembles a skull.",
		str_feed = "{slimeoid_name} spills half the {food_name} on the floor trying to chew it with its exposed teeth.",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} moves as quickly as it can to make the catch, making it just before the ball lands! With a thunk, the ball lodges itself in {slimeoid_name}'s open eye socket. {slimeoid_name} yanks it out and tosses the ball back to you. Euughh."
	),
	EwHead( # head 7
		id_head = "none",
		alias = [
			"g"
		],
		str_create = "You press a button on the head console labelled 'G'. Through the observation port, you see the proto-Slimeoid's front end melt into an indistinct mass.",
		str_head = "It has no discernable head.",
		str_feed = "{slimeoid_name} just sort of... absorbs the {food_name} into its body.",
		str_fetch = "You toss a ball for {slimeoid_name} to fetch. {slimeoid_name} moves under the ball as it flies through the air, but makes no attempt to catch it in its mouth on account of having none. The ball lands next to {slimeoid_name}, who merely looks on. Actually, you can't tell where it's looking."
	)
]

# A map of id_head to EwBody objects.
head_map = {}

# A list of head names
head_names = []

# Populate head map, including all aliases.
for head in head_list:
	head_map[head.id_head] = head
	head_names.append(head.id_head)

	for alias in head.alias:
		head_map[alias] = head

# All mobility attributes in the game.
mobility_list = [
	EwMobility( # mobility 1
		id_mobility = "legs",
		alias = [
			"animal",
			"quadruped",
			"biped",
			"jointed",
			"limbs",
			"a"
		],
		str_advance = "{active} barrels toward {inactive}!",
		str_retreat = "{active} leaps away from {inactive}!",
		str_advance_weak = "{active} limps toward {inactive}!",
		str_retreat_weak = "{active} limps away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'A'. Through the observation port, you see jointed limbs begin to sprout from the proto-Slimeoid's underside.",
		str_mobility = "It walks on legs.",
		str_defeat = "{slimeoid_name}'s knees buckle under it as it collapses to the ground, defeated!",
		str_walk = "{slimeoid_name} walks along beside you."
	),
	EwMobility( # mobility 2
		id_mobility = "rolling",
		alias = [
			"roll",
			"b"
		],
		str_advance = "{active} rolls itself toward {inactive}!",
		str_retreat = "{active} rolls away from {inactive}!",
		str_advance_weak = "{active} rolls itself unsteadily towards {inactive}!",
		str_retreat_weak = "{active} rolls unsteadily away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'B'. Through the observation port, you see the proto-Slimeoid becoming smoother and rounder.",
		str_mobility = "It moves by rolling its body around.",
		str_defeat = "{slimeoid_name} rolls itself over before collapsing on the ground, defeated!",
		str_walk = "{slimeoid_name} rolls itself along the ground behind you."
	),
	EwMobility( # mobility 3
		id_mobility = "flagella",
		alias = [
			"flagella",
			"tendrils",
			"tentacles",
			"c"
		],
		str_advance = "{active} slithers toward {inactive}!",
		str_retreat = "{active} slithers away from {inactive}!",
		str_advance_weak = "{active} drags itself toward {inactive}!",
		str_retreat_weak = "{active} drags itself away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'C'. Through the observation port, you see masses of writhing flagella begin to protrude from the proto-Slimeoid's extremities.",
		str_mobility = "It moves by pulling itself around with its flagella.",
		str_defeat = "{slimeoid_name}'s flagella go limp as it collapses to the ground, defeated!",
		str_walk = "{slimeoid_name} writhes its way along the ground on its flagella next to you."
	),
	EwMobility( # mobility 4
		id_mobility = "jets",
		alias = [
			"fluid",
			"jet",
			"d"
		],
		str_advance = "{active} propels itself toward {inactive}!",
		str_retreat = "{active} propels itself away from {inactive}!",
		str_advance_weak = "{active} sputters towards {inactive}!",
		str_retreat_weak = "{active} sputters away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'D'. Through the observation port, you see openings forming in the proto-Slimeoid's body, which begin to vent fluid.",
		str_mobility = "It moves via jet-propulsion by squirting fluids.",
		str_defeat = "{slimeoid_name} fires its fluid jets wildly in a panic until it completely deflates and collapses, defeated!",
		str_walk = "{slimeoid_name} tries to keep pace with you, spurting jets of fluid to propel itself along behind you."
	),
	EwMobility( # mobility 5
		id_mobility = "slug",
		alias = [
			"undulate",
			"e"
		],
		str_advance = "{active} undulates its way toward {inactive}!",
		str_retreat = "{active} undulates itself away from {inactive}!",
		str_advance_weak = "{active} heaves itself slowly toward {inactive}!",
		str_retreat_weak = "{active} heaves itself slowly away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'E'. Through the observation port, you see the base of the proto-Slimeoid's body widen and flatten out.",
		str_mobility = "It moves like a slug, undulating its underside along the ground.",
		str_defeat = "{slimeoid_name} stops moving entirely and collapses to the ground, defeated!",
		str_walk = "{slimeoid_name} glacially drags its way along behind you in its slug-like way. Your walk ends up taking fucking forever."
	),
	EwMobility( # mobility 5
		id_mobility = "float",
		alias = [
			"gas",
			"f"
		],
		str_advance = "{active} floats toward {inactive}!",
		str_retreat = "{active} floats away from {inactive}!",
		str_advance_weak = "{active} bobs unsteadily through the air towards {inactive}!",
		str_retreat_weak = "{active} bobs unsteadily away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'F'. Through the observation port, you see the of the proto-Slimeoid's body start to inflate itself.",
		str_mobility = "It floats in the air with the use of super-low-density gas bladders.",
		str_defeat = "{slimeoid_name} spins wildly in the air before careening to the ground, defeated!",
		str_walk = "{slimeoid_name} bobs along next to you on its leash like a balloon."
	),
	EwMobility( # mobility 5
		id_mobility = "wings",
		alias = [
			"fly",
			"g"
		],
		str_advance = "{active} darts through the air toward {inactive}!",
		str_retreat = "{active} flaps away from {inactive}!",
		str_advance_weak = "{active} flaps its way doggedly towards {inactive}!",
		str_retreat_weak = "{active} flaps doggedly away from {inactive}!",
		str_create = "You press a button on the mobility console labelled 'G'. Through the observation port, you see the proto-slimeoid start to sprout wide, flat, thin appendages.",
		str_mobility = "It moves by making short flights through the air with its wings.",
		str_defeat = "{slimeoid_name} flaps helplessly as it spins out and crashes into the ground, defeated!",
		str_walk = "{slimeoid_name} flaps along through the air next to you, occasionally perching in trees or windowsills along the route."
	)
]

# A map of id_mobility to EwBody objects.
mobility_map = {}

# A list of mobility names
mobility_names = []

# Populate mobility map, including all aliases.
for mobility in mobility_list:
	mobility_map[mobility.id_mobility] = mobility
	mobility_names.append(mobility.id_mobility)

	for alias in mobility.alias:
		mobility_map[alias] = mobility

# All offense attributes in the game.
offense_list = [
	EwOffense( # offense 1
		id_offense = slimeoid_weapon_blades,
		alias = [
			"edged",
			"edges",
			"edgy",
			"bladed",
			"blade",
			"a"
		],
		str_attack = "{active} slashes {inactive} with its blades!",
		str_attack_weak = "{active} desperately swipes at {inactive} with its blades!",
		str_attack_coup = "{active} slices deep into {inactive}! Green goo splatters onto the ground from the wound!!",
		str_create = "You press a button on the weapon console labelled 'A'. Through the observation port, you see long, sharp protrusions begin to form on the proto-Slimeoid's extremities.",
		str_offense = "It slices foes with retractible blades.",
		str_observe = "{slimeoid_name} is sharpening its retractible blades on a stone nearby."
	),
	EwOffense( # offense 2
		id_offense = slimeoid_weapon_teeth,
		alias = [
			"bite",
			"biting",
			"crunch",
			"crunching",
			"b"
		],
		str_attack = "{active} sinks its teeth into {inactive}!",
		str_attack_weak = "{active} gnashes its teeth, biting {inactive} wherever it can!",
		str_attack_coup = "{active} bites hard into {inactive}, tearing off a piece and chewing it hungrily!",
		str_create = "You press a button on the weapon console labelled 'B'. Through the observation port, you see large bony structures resembling teeth forming in the proto-Slimeoid's... mouth?",
		str_offense = "It can bite foes with deadly fangs.",
		str_observe = "{slimeoid_name} is idly picking its sharp teeth."
	),
	EwOffense( # offense 3
		id_offense = slimeoid_weapon_grip,
		alias = [
			"squeeze",
			"grab",
			"squeezing",
			"grabbing",
			"gripping",
			"constrict",
			"constriction",
			"c"
		],
		str_attack = "{active} grabs {inactive} and squeezes hard!",
		str_attack_weak = "{active} grabs at {inactive}, trying to fend it off!",
		str_attack_coup = "{active} grips {inactive} like a vice, squeezing until you hear a sickening pop!",
		str_create = "You press a button on the weapon console labelled 'C'. Through the observation port, you see the proto-Slimeoid's limbs becoming thicker and stronger, beginning to twist and writhe, seeking something to grip onto.",
		str_offense = "It can grab and crush its foes with its limbs.",
		str_observe = "{slimeoid_name} picks up a rock off the ground and squeezes it like a stress ball."
	),
	EwOffense( # offense 4
		id_offense = slimeoid_weapon_bludgeon,
		alias = [
			"strike",
			"striking",
			"smash",
			"smashing",
			"bash",
			"bashing",
			"crush",
			"crushing",
			"d"
		],
		str_attack = "{active} bashes {inactive} with its limbs!",
		str_attack_weak = "{active} flails its limbs to strike back at {inactive}!",
		str_attack_coup = "{active} winds back and smashes {inactive}, dealing a knockout blow!",
		str_create = "You press a button on the weapon console labelled 'D'. Through the observation port, you see the ends of the proto-Slimeoid's limbs becoming harder and heavier.",
		str_offense = "It can smash foes with one or more of its limbs.",
		str_observe = "{slimeoid_name} spots an insect on the ground nearby and smashes it."
	),
	EwOffense( # offense 5
		id_offense = slimeoid_weapon_spikes,
		alias = [
			"puncture",
			"spear",
			"e"
		],
		str_attack = "{active} skewers {inactive} with its spikes!",
		str_attack_weak = "{active} tries to defend itself from {inactive} with its spikes!",
		str_attack_coup = "{active} punctures {inactive} with its spikes, opening a hole that oozes green fluid all over the ground!",
		str_create = "You press a button on the weapon console labelled 'E'. Through the observation port, you see hard spikes forming out of the congealing slime biomatter.",
		str_offense = "It can puncture its enemies with the spikes on its body.",
		str_observe = "{slimeoid_name} carefully adjusts its position so as not to prick itself with its own spikes."
	),
	EwOffense( # offense 6
		id_offense = slimeoid_weapon_electricity,
		alias = [
			"strike",
			"f"
		],
		str_attack = "{active} unleashes a pent-up electrical discharge into {inactive}!",
		str_attack_weak = "{active} sparks and flickers with electricity, shocking {inactive}!",
		str_attack_coup = "{active} charges up and sends a bolt of electricity through {inactive}, making it sizzle!",
		str_create = "You press a button on the weapon console labelled 'F'. Through the observation port, you see the proto-Slimeoid begin to spark with small electrical discharges.",
		str_offense = "It crackles with stored electrical energy.",
		str_observe = "A fly flies a little too near {slimeoid_name} and is zapped with a tiny bolt of electricity, killing it instantly."
	),
	EwOffense( # offense 7
		id_offense = slimeoid_weapon_slam,
		alias = [
			"bodyslam",
			"g"
		],
		str_attack = "{active} slams its entire body into {inactive}!",
		str_attack_weak = "{active} flails itself back against {inactive}'s onslaught!",
		str_attack_coup = "{active} hurls its whole weight into {inactive}, crushing it to the ground!",
		str_create = "You press a button on the weapon console labelled 'G'. Through the observation port, you see the ends of the proto-Slimeoid's congealing body condense, becoming heavier and more robust.",
		str_offense = "It can slam its body into its foes with tremendous force.",
		str_observe = "{slimeoid_name} shifts its weight back and forth before settling down in a kind of sumo-squat position."
	)
]

# A map of id_offense to EwBody objects.
offense_map = {}

# A list of offense names
offense_names = []

# Populate offense map, including all aliases.
for offense in offense_list:
	offense_map[offense.id_offense] = offense
	offense_names.append(offense.id_offense)

	for alias in offense.alias:
		offense_map[alias] = offense




# All defense attributes in the game.
defense_list = [
	EwDefense( # defense 1
		id_defense = slimeoid_armor_scales,
		alias = [
			"scale",
			"scaled",
			"scaly",
			"a"
		],
		str_defense = "",
		str_pet = "You carefully run your hand over {slimeoid_name}'s hide, making sure to go with the grain so as not to slice your fingers open on its sharp scales.",
		str_abuse = "You pick up {slimeoid_name} by the hind legs, swinging them over your head and repeatedly slamming them to the ground.",
		str_create = "You press a button on the armor console labelled 'A'. Through the observation port, you see the proto-Slimeoid's skin begin to glint as it sprouts roughly-edged scales.",
		str_armor = "It is covered in scales.",
		id_resistance = slimeoid_weapon_electricity,
		id_weakness = slimeoid_special_TK,
		str_resistance = " {}'s scales conduct the electricity away from its vitals!",
		str_weakness = " {}'s scales refract and amplify the disrupting brainwaves inside its skull!",
	),
	EwDefense( # defense 2
		id_defense = slimeoid_armor_boneplates,
		alias = [
			"bone",
			"bony",
			"bones",
			"plate",
			"plates",
			"armor",
			"plating",
			"b"
		],
		str_defense = "",
		str_pet = "You pat one of the hard, bony plates covering {slimeoid_name}'s skin.",
		str_abuse = "You take a stick and hit {slimeoid_name}'s face with it.",
		str_create = "You press a button on the armor console labelled 'B'. Through the observation port, you see hard bony plates begin to congeal on the proto-Slimeoid's surface.",
		str_armor = "It is covered in bony plates.",
		id_resistance = slimeoid_weapon_blades,
		id_weakness = slimeoid_special_spines,
		str_resistance = " {}'s bone plates block the worst of the damage!",
		str_weakness = " {}'s bone plates only drive the quills deeper into its body as it moves!",

	),
	EwDefense( # defense 3
		id_defense = slimeoid_armor_quantumfield,
		alias = [
			"quantum",
			"field",
			"energy",
			"c"
		],
		str_defense = "",
		str_pet = "You pat {slimeoid_name}, and your hand tingles as it passes through the quantum field that surrounds its body.",
		str_abuse = "You grab hold of {slimeoid_name} and shake them aggressively, until their quantum static is splayed out and they look nauseous.",
		str_create = "You press a button on the armor console labelled 'C'. Through the observation port, start to notice the proto-Slimeoid begin to flicker, and you hear a strange humming sound.",
		str_armor = "It is enveloped in a field of quantum uncertainty.",
		id_resistance = slimeoid_weapon_slam,
		id_weakness = slimeoid_special_laser,
		str_resistance = " {}'s quantum superposition makes it difficult to hit head-on!",
		str_weakness = " {}'s quantum particles are excited by the high-frequency radiation, destabilizing its structure!",

	),
	EwDefense( # defense 4
		id_defense = slimeoid_armor_formless,
		alias = [
			"amorphous",
			"shapeless",
			"squishy",
			"d"
		],
		str_defense = "",
		str_pet = "You pat {slimeoid_name}, its fluid, shapeless body squishing and deforming in response to even slight pressure.",
		str_abuse = "You stick your fist into {slimeoid_name}'s squishy body and jostle its vital organs.",
		str_create = "You press a button on the armor console labelled 'D'. Through the observation port, you see the proto-Slimeoid suddenly begin to twist itself, stretching and contracting as its shape rapidly shifts.",
		str_armor = "It is malleable and can absorb blows with ease.",
		id_resistance = slimeoid_weapon_bludgeon,
		id_weakness = slimeoid_special_webs,
		str_resistance = " {}'s squishy body easily absorbs the blows!",
		str_weakness = " {}'s squishy body easily adheres to and becomes entangled by the webs!",

	),
	EwDefense( # defense 5
		id_defense = slimeoid_armor_regeneration,
		alias = [
			"healing",
			"regen",
			"e"
		],
		str_defense = "",
		str_pet = "You pat {slimeoid_name}. Its skin is hot, and you can feel it pulsing rhythmically.",
		str_abuse = "You take a blowtorch to {slimeoid_name}'s pulsating skin and watch as it wears itself out trying to regenerate the rapidly burning tissue.",
		str_create = "You press a button on the armor console labelled 'E'. Through the observation port, you see the proto-Slimeoid begin to pulse, almost like a beating heart.",
		str_armor = "It can regenerate damage to its body rapidly.",
		id_resistance = slimeoid_weapon_spikes,
		id_weakness = slimeoid_special_spit,
		str_resistance = " {} quickly begins regenerating the small puncture wounds inflicted by the spikes!",
		str_weakness = " {}'s regeneration is impeded by the corrosive chemicals!",

	),
	EwDefense( # defense 6
		id_defense = slimeoid_armor_stench,
		alias = [
			"stink",
			"smell",
			"f"
		],
		str_defense = "",
		str_pet = "You pat {slimeoid_name}, taking care not to inhale through your nose, as one whiff of its odor has been known to make people lose their lunch.",
		str_abuse = "You try to humiliate {slimeoid_name} by plugging your nose and kicking it around.",
		str_create = "You press a button on the armor console labelled 'F'. Through the observation port, you see the proto-Slimeoid give off bubbles of foul-colored gas.",
		str_armor = "It exudes a horrible stench.",
		id_resistance = slimeoid_weapon_teeth,
		id_weakness = slimeoid_special_throw,
		str_resistance = " {}'s noxious fumes make its opponent hesitant to put its mouth anywhere near it!",
		str_weakness = " {}'s foul odor gives away its position, making it easy to target with thrown projectiles!",

	),
	EwDefense( # defense 7
		id_defense = slimeoid_armor_oil,
		alias = [
			"slick",
			"g"
		],
		str_defense = "",
		str_pet = "You pat {slimeoid_name}'s slick wet skin, and your hand comes away coated in a viscous, slippery oil.",
		str_abuse = "You turn {slimeoid_name} upside down and push their oily body, sending them slipping down the sidewalk.",
		str_create = "You press a button on the armor console labelled 'G'. Through the observation port, you see the surface of the proto-Slimeoid become shiny with some kind of oily fluid.",
		str_armor = "It is covered in a coating of slippery oil.",
		id_resistance = slimeoid_weapon_grip,
		id_weakness = slimeoid_special_fire,
		str_resistance = " {}'s slippery coating makes it extremely difficult to grab on to!",
		str_weakness = " {}'s oily coating is flammable, igniting as it contacts the flame!",

	)
]

# A map of id_defense to EwBody objects.
defense_map = {}

# A list of defense names
defense_names = []

# Populate defense map, including all aliases.
for defense in defense_list:
	defense_map[defense.id_defense] = defense
	defense_names.append(defense.id_defense)

	for alias in defense.alias:
		defense_map[alias] = defense

# All special attributes in the game.
special_list = [
	EwSpecial( # special 1
		id_special = slimeoid_special_spit,
		alias = [
			"spitting",
			"spray",
			"squirt",
			"spraying",
			"squirting",
			"liquid",
			"fluid",
			"acid",
			"acidic",
			"toxic",
			"poison",
			"a"
		],
		str_special_attack = "{active} spits acidic ooze onto {inactive}!",
		str_special_attack_weak = "{active} coughs and spurts up a sputtering spray of acid at {inactive}!",
		str_special_attack_coup = "{active} vomits a torrent of acid onto {inactive}, deteriorating it to the point that it can no longer fight!",
		str_create = "You press a button on the special attack console labelled 'A'. Through the observation port, you see the proto-Slimeoid's body begin to excrete a foul, toxic ooze.",
		str_special = "It can spit acidic ooze.",
		str_observe = "A bit of acidic fluid drips from {slimeoid_name} onto the ground, where it smokes and sizzles."
	),
	EwSpecial( # special 2
		id_special = slimeoid_special_laser,
		alias = [
			"beam",
			"energy",
			"radiation",
			"b"
		],
		str_special_attack = "{active} sears {inactive} with a blast of radiation!",
		str_special_attack_weak = "{active} starts to flicker before firing an unsteady beam of light at {inactive}!",
		str_special_attack_coup = "{active} blasts {inactive} with a beam of green energy, searing it all over its body!",
		str_create = "You press a button on the special attack console labelled 'B'. Through the observation port, you see the proto-Slimeoid's body begin to glow with energy as the gestation vat's built-in Geiger Counter begins to click frantically.",
		str_special = "It can fire beams of radiation.",
		str_observe = "{slimeoid_name} suddenly glows with radioactive energy. Best not to look directly at it until it settles down..."
	),
	EwSpecial( # special 3
		id_special = slimeoid_special_spines,
		alias = [
			"spikes",
			"spiky",
			"spiny",
			"quills",
			"c"
		],
		str_special_attack = "{active} fires a volley of quills into {inactive}!",
		str_special_attack_weak = "{active} desperately fires a few of its last quills into {inactive}!",
		str_special_attack_coup = "{active} fires a rapid burst of sharp quills into {inactive}, filling it like a pincushion!",
		str_create = "You press a button on the special attack console labelled 'C'. Through the observation port, you see the proto-Slimeoid's congealing body suddenly protruding with long, pointed spines, which quickly retract back into it.",
		str_special = "It can fire sharp quills.",
		str_observe = "{slimeoid_name} shudders and ejects a few old quills onto the ground. You can see new ones already growing in to replace them."
	),
	EwSpecial( # special 4
		id_special = slimeoid_special_throw,
		alias = [
			"throwing",
			"hurling",
			"hurl",
			"d"
		],
		str_special_attack = "{active} picks up a nearby {object} and hurls it into {inactive}!",
		str_special_attack_weak = "{active} unsteadily hefts a nearby {object} before throwing it into {inactive}!",
		str_special_attack_coup = "{active} hurls a {object}, which smashes square into {inactive}, knocking it to the ground! A direct hit!",
		str_create = "You press a button on the special attack console labelled 'D'. Through the observation port, you see the proto-Slimeoid's limbs become more articulate.",
		str_special = "It can hurl objects at foes.",
		str_observe = "{slimeoid_name} is idly picking up stones and seeing how far it can toss them."
	),
	EwSpecial( # special 5
		id_special = slimeoid_special_TK,
		alias = [
			"telekinesis",
			"psychic",
			"e"
		],
		str_special_attack = "{active} focuses on {inactive}... {inactive} convulses in pain!",
		str_special_attack_weak = "{active}'s cranium bulges and throbs! {inactive} convulses!",
		str_special_attack_coup = "{active} emanates a strange static sound as {inactive} is inexplicably rendered completely unconscious!",
		str_create = "You press a button on the special attack console labelled 'E'. You momentarily experience an uncomfortable sensation, sort of like the feeling you get when you know there's a TV on in the room even though you can't see it.",
		str_special = "It can generate harmful frequencies with its brainwaves.",
		str_observe = "You momentarily black out. When you come to, your nose is bleeding. {slimeoid_name} tries to look innocent."
	),
	EwSpecial( # special 6
		id_special = slimeoid_special_fire,
		alias = [
			"chemical",
			"breath",
			"breathe",
			"f"
		],
		str_special_attack = "{active} ejects a stream of fluid which ignites in the air, burning {inactive}!",
		str_special_attack_weak = "{active} fires an unsteady, sputtering stream of fluid that ignites and singes {inactive}!",
		str_special_attack_coup = "{active} empties its fluid bladders in a final burst of liquid! {inactive} is completely engulfed in the conflagration!",
		str_create = "You press a button on the special attack console labelled 'F'. Through the observation port, you see fluid bladders forming deep under the still-forming proto-Slimeoid's translucent skin.",
		str_special = "It can fire a stream of pyrophoric fluid at its foes.",
		str_observe = "A bit of fluid drips from {slimeoid_name} onto the floor and ignites, but you manage to smother the small flame quickly before it spreads."
	),
	EwSpecial( # special 7
		id_special = slimeoid_special_webs,
		alias = [
			"webbing",
			"web",
			"g"
		],
		str_special_attack = "{active} fires a stream of sticky webbing onto {inactive}!",
		str_special_attack_weak = "{active} is running out of webbing! It shoots as much as it can onto {inactive}!",
		str_special_attack_coup = "{active} gathers itself up before spurting a blast of webbing that coats {inactive}'s body, completely ensnaring it!",
		str_create = "You press a button on the special attack console labelled 'G'. Through the observation port, you see large glands forming near the surface of the still-forming proto-Slimeoid's translucent skin.",
		str_special = "It can spin webs and shoot webbing fluid to capture prey.",
		str_observe = "{slimeoid_name} is over in the corner, building itself a web to catch prey in."
	)
]

# A map of id_special to EwBody objects.
special_map = {}

# A list of special names
special_names = []

# Populate special map, including all aliases.
for special in special_list:
	special_map[special.id_special] = special
	special_names.append(special.id_special)

	for alias in special.alias:
		special_map[alias] = special

def get_strat_a(combat_data, in_range, first_turn, active):
	base_attack = 30
	base_evade = 10
	base_block = 10

	weight_attack = base_attack
	weight_evade = base_evade
	weight_block = base_block

	if in_range:
		if active:
			weight_attack *= 3
			weight_block *= 2
		else:
			weight_block *= 3

	else:
		if active:
			weight_evade *= 2
		else:
			weight_evade *= 5

	strat = random.randrange(weight_attack + weight_evade + weight_block)
	if strat < weight_attack:
		strat_used = slimeoid_strat_attack
	elif strat < weight_attack + weight_evade:
		strat_used = slimeoid_strat_evade
	else:
		strat_used = slimeoid_strat_block

	if first_turn:
		sap_spend = int(random.triangular(0, combat_data.sap, int(combat_data.sap * 0.8))) + 1

	else:
		sap_spend = combat_data.sap

	sap_spend = min(sap_spend, combat_data.sap)

	return strat_used, sap_spend

def get_strat_b(combat_data, in_range, first_turn, active):
	base_attack = 20
	base_evade = 10
	base_block = 10

	weight_attack = base_attack
	weight_evade = base_evade
	weight_block = base_block

	if in_range:
		if active:
			weight_attack *= 3
			weight_block *= 2
		else:
			weight_block *= 2
			weight_evade *= 3

	else:
		if active:
			weight_attack *= 3
			weight_evade *= 3
		else:
			weight_evade *= 4
			weight_block *= 2

	strat = random.randrange(weight_attack + weight_evade + weight_block)
	if strat < weight_attack:
		strat_used = slimeoid_strat_attack
	elif strat < weight_attack + weight_evade:
		strat_used = slimeoid_strat_evade
	else:
		strat_used = slimeoid_strat_block

	if first_turn:
		sap_spend = int(random.triangular(0, combat_data.sap, int(combat_data.sap * 0.65))) + 1

	else:
		sap_spend = combat_data.sap

	sap_spend = min(sap_spend, combat_data.sap)

	return strat_used, sap_spend

def get_strat_c(combat_data, in_range, first_turn, active):
	base_attack = 30
	base_evade = 10
	base_block = 10

	weight_attack = base_attack
	weight_evade = base_evade
	weight_block = base_block

	if in_range:
		if active:
			weight_attack *= 3
		else:
			weight_block *= 2
			weight_evade *= 2

	else:
		if active:
			weight_attack *= 3
		else:
			weight_evade *= 2
			weight_block *= 2

	strat = random.randrange(weight_attack + weight_evade + weight_block)
	if strat < weight_attack:
		strat_used = slimeoid_strat_attack
	elif strat < weight_attack + weight_evade:
		strat_used = slimeoid_strat_evade
	else:
		strat_used = slimeoid_strat_block

	if first_turn:
		sap_spend = int(random.triangular(0, combat_data.sap, int(combat_data.sap * 0.8))) + 1

	else:
		sap_spend = combat_data.sap

	sap_spend = min(sap_spend, combat_data.sap)

	return strat_used, sap_spend

def get_strat_d(combat_data, in_range, first_turn, active):
	base_attack = 20
	base_evade = 5
	base_block = 15

	weight_attack = base_attack
	weight_evade = base_evade
	weight_block = base_block

	if in_range:
		if active:
			weight_attack *= 3
		else:
			weight_attack /= 2
			weight_block *= 2

	else:
		if active:
			weight_attack *= 3
		else:
			weight_attack /= 2
			weight_block *= 2

	strat = random.randrange(weight_attack + weight_evade + weight_block)
	if strat < weight_attack:
		strat_used = slimeoid_strat_attack
	elif strat < weight_attack + weight_evade:
		strat_used = slimeoid_strat_evade
	else:
		strat_used = slimeoid_strat_block

	if first_turn:
		sap_spend = int(random.triangular(0, combat_data.sap, int(combat_data.sap * 0.35))) + 1

	else:
		sap_spend = combat_data.sap

	sap_spend = min(sap_spend, combat_data.sap)

	return strat_used, sap_spend

def get_strat_e(combat_data, in_range, first_turn, active):
	base_attack = 20
	base_evade = 10
	base_block = 10

	weight_attack = base_attack
	weight_evade = base_evade
	weight_block = base_block

	if in_range:
		if active:
			weight_attack *= 2
			weight_evade *= 2
		else:
			weight_evade *= 4

	else:
		if active:
			weight_attack *= 4
			weight_block *= 2
		else:
			weight_block *= 3

	strat = random.randrange(weight_attack + weight_evade + weight_block)
	if strat < weight_attack:
		strat_used = slimeoid_strat_attack
	elif strat < weight_attack + weight_evade:
		strat_used = slimeoid_strat_evade
	else:
		strat_used = slimeoid_strat_block

	if first_turn:
		sap_spend = int(random.triangular(0, combat_data.sap, int(combat_data.sap * 0.65))) + 1

	else:
		sap_spend = combat_data.sap

	sap_spend = min(sap_spend, combat_data.sap)

	return strat_used, sap_spend

def get_strat_f(combat_data, in_range, first_turn, active):
	base_attack = 20
	base_evade = 20
	base_block = 10

	weight_attack = base_attack
	weight_evade = base_evade
	weight_block = base_block

	if in_range:
		if active:
			weight_attack *= 3
			weight_evade *= 2
		else:
			weight_evade *= 3
			weight_block *= 2

	else:
		if active:
			weight_attack *= 4
			weight_block *= 2
		else:
			weight_block *= 3
			weight_evade *= 2


	strat = random.randrange(weight_attack + weight_evade + weight_block)
	if strat < weight_attack:
		strat_used = slimeoid_strat_attack
	elif strat < weight_attack + weight_evade:
		strat_used = slimeoid_strat_evade
	else:
		strat_used = slimeoid_strat_block

	if first_turn:
		sap_spend = int(random.triangular(0, combat_data.sap, int(combat_data.sap * 0.35))) + 1

	else:
		sap_spend = combat_data.sap

	sap_spend = min(sap_spend, combat_data.sap)

	return strat_used, sap_spend

def get_strat_g(combat_data, in_range, first_turn, active):
	base_attack = 10
	base_evade = 15
	base_block = 5

	weight_attack = base_attack
	weight_evade = base_evade
	weight_block = base_block

	if in_range:
		if active:
			weight_attack *= 4
		else:
			weight_evade *= 2

	else:
		if active:
			weight_attack *= 4
		else:
			weight_evade *= 2

	strat = random.randrange(weight_attack + weight_evade + weight_block)
	if strat < weight_attack:
		strat_used = slimeoid_strat_attack
	elif strat < weight_attack + weight_evade:
		strat_used = slimeoid_strat_evade
	else:
		strat_used = slimeoid_strat_block

	if first_turn:
		sap_spend = int(random.triangular(0, combat_data.sap, int(combat_data.sap * 0.2))) + 1

	else:
		sap_spend = combat_data.sap

	sap_spend = min(sap_spend, combat_data.sap)

	return strat_used, sap_spend
# All brain attributes in the game.
brain_list = [
	EwBrain( # brain 1
		id_brain = "a",
		alias = [
			"typea",
			"type a"
		],
		str_create = "You press a button on the brain console labelled 'A'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid begins to move, thrashing about as if in frustration.",
		str_brain = "It is extremely irritable.",
		str_observe = "{slimeoid_name} is snarling. You're not sure if it's angry at you, or at the world in general.",
		str_pet = "{slimeoid_name} hisses at you.",
		str_walk = "You wrestle {slimeoid_name} down and force a leash onto it, as it angrily snarls and hisses at you in protest.",
		str_feed = "{slimeoid_name} almost bites your hand off as you offer the {food_name} to it! It growls at you before eating, as if to secure its prey.",
		str_kill = "{slimeoid_name} howls with savage delight at the bloodshed!!",
		str_death = "{slimeoid_name} howls in fury at its master's death! It tears away in a blind rage!",
		str_victory = "{slimeoid_name} roars in triumph!!",
		str_battlecry = "{slimeoid_name} roars with bloodlust!! ",
		str_battlecry_weak = "{slimeoid_name} is too breathless to roar, but is still filled with bloodlust!! ",
		str_movecry = "{slimeoid_name} snarls at its prey! " ,
		str_movecry_weak = "{slimeoid_name}  hisses with frustrated rage! ",
		str_revive = "{slimeoid_name} howls at your return, annoyed to have been kept waiting.",
		str_spawn = "{slimeoid_name} shakes itself off to get rid of some excess gestation fluid, then starts to hiss at you. Seems like a real firecracker, this one.",
		str_dissolve = "{slimeoid_name} hisses and spits with fury as you hold it over the SlimeCorp Dissolution Vats. Come on, get in there...\n{slimeoid_name} claws at you, clutching at the edge of the vat, screeching with rage even as you hold its head under the surface and wait for the chemical soup to do its work. At last, it stops fighting.\n\n{slimeoid_name} is no more.",
		get_strat = get_strat_a,
		str_abuse= "{slimeoid_name} lashes out, trying to fight back."

	),
	EwBrain( # brain 2
		id_brain = "b",
		alias = [
			"typeb",
			"type b"
		],
		str_create = "You press a button on the brain console labelled 'B'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid begins to move about its gestation tank, exploring its surroundings.",
		str_brain = "It is enthusiastic about almost everything.",
		str_observe = "{slimeoid_name} notices you looking at it and seems delighted!",
		str_pet = "{slimeoid_name} purrs happily.",
		str_walk = "{slimeoid_name} is so excited for its walk, it can barely hold still enough to let you put the leash on it!",
		str_feed = "{slimeoid_name} starts running circles around you and drooling uncontrollably in anticipation as soon as you reach for the {food_name}.",
		str_kill = "{slimeoid_name} gives a bestial woop of excitement for your victory!",
		str_death = "{slimeoid_name} gives a wail of grief at its master's death, streaking away from the scene.",
		str_victory = "{slimeoid_name} woops with delight at its victory!",
		str_battlecry = "{slimeoid_name} lets out a loud war woop! " ,
		str_battlecry_weak = "{slimeoid_name} is determined not to lose! ",
		str_movecry = "{slimeoid_name} is thrilled by the battle! " ,
		str_movecry_weak = "{slimeoid_name} seems a little less thrilled now... ",
		str_revive = "{slimeoid_name} is waiting patiently downtown when you return from your time as a corpse. It knew you'd be back!",
		str_spawn = "{slimeoid_name} gets up off the ground slowly at first, but then it notices you and leaps into your arms. It sure seems glad to see you!",
		str_dissolve = "You order {slimeoid_name} into the Dissolution Vats. It's initially confused, but realization of what you're asking slowly crawks across its features.\nIt doesn't want to go, but after enough stern commanding, it finally pitches itself into the toxic sludge, seemingly too heartbroken to fear death.\n\n{slimeoid_name} is no more.",
		get_strat = get_strat_b,
		str_abuse = "{slimeoid_name} yelps in pain. It's beside itself and doesn't know what to do..."
	),
	EwBrain( # brain 3
		id_brain = "c",
		alias = [
			"typec",
			"type c"
		],
		str_create = "You press a button on the brain console labelled 'C'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid draws its congealing body together, as if trying to gather its strength.",
		str_brain = "It is quiet and withdrawn.",
		str_observe = "{slimeoid_name} seems to be resting, possibly deep in thought.",
		str_pet = "{slimeoid_name} doesn't react.",
		str_walk = "{slimeoid_name} holds still as you place the leash on it. It regards the leash, seemingly pontificating.",
		str_feed = "{slimeoid_name} shows neither happiness nor reluctance as you offer the {food_name}. It accepts the treat as though it were a mere formality.",
		str_kill = "{slimeoid_name} regards the corpse of your former adversary with an unknowable expression.",
		str_death = "{slimeoid_name} stares at the killer, memorizing their face before fleeing the scene.",
		str_victory = "{slimeoid_name} silently turns away from its defeated opponent.",
		str_battlecry = "{slimeoid_name} carefully regards its opponent. ",
		str_battlecry_weak = "{slimeoid_name} tries to steady itself. ",
		str_movecry = "{slimeoid_name} seems to be getting impatient. " ,
		str_movecry_weak = "{slimeoid_name} is losing its composure just a little! ",
		str_revive = "{slimeoid_name} is downtown when you return from the sewers. You find it staring silently up at ENDLESS WAR.",
		str_spawn = "{slimeoid_name} regards you silently from the floor. You can't tell if it likes you or not, but it starts to follow you regardless.",
		str_dissolve = "You pick up {slimeoid_name} and hurl it into the SlimeCorp Dissolution Vats before it starts to suspect anything. It slowly sinks into the chemical soup, kind of like Arnold at the end of Terminator 2, only instead of giving you a thumbs-up, it stares at you with an unreadable expression. Betrayal? Confusion? Hatred? Yeah, probably.\n\n{slimeoid_name} is no more.",
		get_strat = get_strat_c,
		str_abuse = "You can feel {slimeoid_name} trembling, but it just takes your abuse."
	),
	EwBrain( # brain 4
		id_brain = "d",
		alias = [
			"typed",
			"type d"
		],
		str_create = "You press a button on the brain console labelled 'D'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid lazily turns over in its gestation vat, floating and doing little else.",
		str_brain = "It is usually staring off into space.",
		str_observe = "{slimeoid_name} stares off into the distance. Who knows if it's actually looking at anything in particular.",
		str_pet = "{slimeoid_name} is startled out of a stupor by your touch.",
		str_walk = "{slimeoid_name} hardly seems to notice you fastening it with a leash.",
		str_feed = "You have to literally shove the {food_name} into {slimeoid_name}'s face to get its attention. It takes a moment to recover its orientation before accepting the treat.",
		str_kill = "{slimeoid_name} wasn't paying attention and missed the action.",
		str_death = "{slimeoid_name} is startled to realize its master has died. It blinks in confusion before fleeing.",
		str_victory = "{slimeoid_name} keeps attacking for a moment before realizing it's already won.",
		str_battlecry = "{slimeoid_name} is weighing its options! ",
		str_battlecry_weak = "{slimeoid_name} is desperately trying to come up with a plan! ",
		str_movecry = "{slimeoid_name} Isn't really feeling this. " ,
		str_movecry_weak = "{slimeoid_name} tries to buy itself some time to think! ",
		str_revive = "{slimeoid_name} is exactly where you left it when you died.",
		str_spawn = "{slimeoid_name} flops over on the floor and stares up at you. Its gaze wanders around the room for a while before it finally picks itself up to follow you.",
		str_dissolve = "You lead {slimeoid_name} up to the edge of the Dissolution Vats and give a quick 'Hey, look, a distraction!'. {slimeoid_name} is immediately distracted and you shove it over the edge. Landing in the vat with a sickening *gloop* sound, it sinks quickly under the fluid surface, flailing madly in confusion and desperation.\n\n{slimeoid_name} is no more.",
		get_strat = get_strat_d,
		str_abuse = "You have a hard time with it, {slimeoid_name} is panicked and keeps trying to run."
	),
	EwBrain( # brain 5
		id_brain = "e",
		alias = [
			"typee",
			"type e"
		],
		str_create = "You press a button on the brain console labelled 'E'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid starts to sporadically twitch and shiver.",
		str_brain = "It is extremely skittish and jumpy.",
		str_observe = "{slimeoid_name} is glancing around furtively, seemingly scanning for threats.",
		str_pet = "{slimeoid_name} flinches nervously at your touch.",
		str_walk = "{slimeoid_name} shivers in place as you're fastening the leash, then starts to pull and tug at it, seemingly perturbed.",
		str_feed = "{slimeoid_name} backs up anxiously as you reach out with the {food_name} in your hand. You sigh and take a bite of the treat yourself to convince {slimeoid_name} that its not poisoned. It reluctantly accepts the {food_name} and starts nibbling at it.",
		str_kill = "{slimeoid_name} peers out from behind its master, hoping the violence is over.",
		str_death = "{slimeoid_name} is overcome with terror, skittering away from the killer in a mad panic!",
		str_victory = "{slimeoid_name} is deeply relieved that the battle is over.",
		str_battlecry = "{slimeoid_name} chitters fearfully! ",
		str_battlecry_weak = "{slimeoid_name} squeals in abject terror! ",
		str_movecry = "{slimeoid_name} makes a break for it! " ,
		str_movecry_weak = "{slimeoid_name} is in a full-blown panic! ",
		str_revive = "{slimeoid_name} peeks out from behind some trash cans before rejoining you. It seems relieved to have you back.",
		str_spawn = "{slimeoid_name}'s eyes dart frantically around the room. Seeing you, it darts behind you, as if for cover from an unknown threat.",
		str_dissolve = "{slimeoid_name} is looking around the lab nervously, obviously unnerved by the Slimeoid technology. Its preoccupation makes it all too easy to lead it to the Dissolution Vats and kick its legs out from under it, knocking it in. As it falls and hits the solvent chemicals, it wails and screeches in shock and terror, but the noise eventually quiets as it dissolves into a soft lump, then disintegrates altogether.\n\n{slimeoid_name} is no more.",
		get_strat = get_strat_e,
		str_abuse = "{slimeoid_name} is squealing in horror. It will remember this..."
	),
	EwBrain( # brain 6
		id_brain = "f",
		alias = [
			"typef",
			"type f"
		],
		str_create = "You press a button on the brain console labelled 'F'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid darts to the opposite side of the gestation vat. You're not sure, but you feel like it's watching you.",
		str_brain = "It acts secretive, as though it's up to something.",
		str_observe = "{slimeoid_name} is moving around, apparently searching for... something.",
		str_pet = "{slimeoid_name} seems nonplussed, but doesn't object.",
		str_walk = "{slimeoid_name} exasperatedly lets you fit it with a leash for a walk.",
		str_feed = "{slimeoid_name} only seems to halfway pay attention as you offer the {food_name}. It pockets the treat for later and eats it when it thinks you aren't looking.",
		str_kill = "{slimeoid_name} rifles through your victim's pockets for food.",
		str_death = "{slimeoid_name} rifles through its dead master's pockets for whatever it can find before slinking away.",
		str_victory = "{slimeoid_name} shakes itself off after the battle.",
		str_battlecry = "{slimeoid_name} makes its move! ",
		str_battlecry_weak = "{slimeoid_name}, backed into a corner, tries to counterattack! ",
		str_movecry = "{slimeoid_name} decides on a tactical repositioning. " ,
		str_movecry_weak = "{slimeoid_name} thinks it'd better try something else, and fast! ",
		str_revive = "{slimeoid_name} starts following you around again not long after you have returned from the dead.",
		str_spawn = "{slimeoid_name} picks itself up off the floor and regards you coolly. It seems as if it's gauging your usefulness.",
		str_dissolve = "{slimeoid_name} eyes you suspiciously as you approach the Dissolution Vats. It's on to you. Before it has a chance to bolt, you grab it, hoist it up over your head, and hurl it into the chemical soup. {slimeoid_name} screeches in protest, sputtering and hissing as it thrashes around in the vat, but the chemicals work quickly and it soon dissolves into nothing.\n\n{slimeoid_name} is no more.",
		get_strat = get_strat_f,
		str_abuse = "{slimeoid_name}'s fear grows as it desperately looks for an escape."
	),
	EwBrain( # brain 7
		id_brain = "g",
		alias = [
			"typeg",
			"type g"
		],
		str_create = "You press a button on the brain console labelled 'G'.\nA cluster of neurons coagulates within your newly-forming Slimeoid. The proto-Slimeoid begins to flit around the gestation vat, seemingly unsure where to go.",
		str_brain = "It seems to have no idea what it's doing.",
		str_observe = "{slimeoid_name} seems unsure of whether it wants to wander around or just stay put.",
		str_pet = "{slimeoid_name} seems confused about how to react.",
		str_walk = "{slimeoid_name} lets you put its leash on it, but immediately starts to trip over it and get tangled in it.",
		str_feed = "{slimeoid_name} stares at the {food_name} like it's unfamiliar with the concept of food. You make a chewing motion with your mouth to demonstrate. It still seems confused. You lose your patience and force-feed the treat to your slimeoid.",
		str_kill = "{slimeoid_name} seems unsure of whether to celebrate the victory or to mourn the decline of your civilization into rampant youth violence.",
		str_death = "{slimeoid_name} starts to approach its master's body, then changes its mind and starts to run away. It trips over itself and falls on its way out.",
		str_victory = "{slimeoid_name} looks around, apparently shocked that it somehow won.",
		str_battlecry = "{slimeoid_name} decides to actually do something for once! ",
		str_battlecry_weak = "{slimeoid_name} decides to actually do something for once, now that it's probably too late.",
		str_movecry = "{slimeoid_name} is moving around aimlessly! " ,
		str_movecry_weak = "{slimeoid_name} is limping around aimlessly! ",
		str_revive = "{slimeoid_name} wanders by, seemingly by accident, but thinks it probably ought to start following you again.",
		str_spawn = "{slimeoid_name} starts to pick itself up off the floor, then changes its mind and lies back down. Then it gets up again. Lies down again. Up. Down. Up. Ok, this time it stays up.",
		str_dissolve = "{slimeoid_name} is perplexed by the laboratory machinery. Taking advantage of its confusion, you point it towards the Dissolution Vats, and it gormlessly meanders up the ramp and over the edge. You hear a gloopy SPLOOSH sound, then nothing. You approach the vats and peer over the edge, but see no trace of your former companion.\n\n{slimeoid_name} is no more.",
		get_strat = get_strat_g,
		str_abuse = "{slimeoid_name} still hasn't caught up to all this chaos, and is lost and confused."
	)
]

# A map of id_brain to EwBrain objects.
brain_map = {}

# A list of brain names
brain_names = []

# Populate brain map, including all aliases.
for brain in brain_list:
	brain_map[brain.id_brain] = brain
	brain_names.append(brain.id_brain)

	for alias in brain.alias:
		brain_map[alias] = brain

hue_analogous = -1
hue_neutral = 0
hue_atk_complementary = 1
hue_special_complementary = 2
hue_full_complementary = 3

hue_id_yellow = "yellow"
hue_id_orange = "orange"
hue_id_red = "red"
hue_id_pink = "pink"
hue_id_magenta = "magenta"
hue_id_purple = "purple"
hue_id_blue = "blue"
hue_id_cobalt = "cobalt"
hue_id_cyan = "cyan"
hue_id_teal = "teal"
hue_id_green = "green"
hue_id_lime = "lime"
hue_id_rainbow = "rainbow"
hue_id_white = "white"
hue_id_grey = "grey"
hue_id_black = "black"
hue_id_brown = "brown"
hue_id_copper = "copper"
hue_id_chrome = "chrome"
hue_id_gold = "gold"


# All color attributes in the game.
hue_list = [
	EwHue(
		id_hue = hue_id_white,
		alias = [
			"whitedye",
			"poketubers"
		],
		str_saturate = "It begins to glow a ghostly white!",
		str_name = "white",
		str_desc = "Its pale white body and slight luminescence give it a supernatural vibe.",
		is_neutral = True,
	),
	EwHue(
		id_hue = hue_id_yellow,
		alias = [
			"yellowdye",
			"pulpgourds"
		],
		str_saturate = "It begins to shine a bright yellow!",
		str_name = "yellow",
		str_desc = "Its bright yellow hue is delightfully radiant.",
		effectiveness = {
			hue_id_orange: hue_analogous,
			hue_id_lime: hue_analogous,
			hue_id_purple: hue_atk_complementary,
			hue_id_cobalt: hue_special_complementary,
			hue_id_blue: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},

	),
	EwHue(
		id_hue = hue_id_orange,
		alias = [
			"orangedye",
			"sourpotatoes"
		],
		str_saturate = "It turns a warm orange!",
		str_name= "orange",
		str_desc = "Its warm orange hue makes you want to cuddle up beside it with a nice book.",
		effectiveness = {
			hue_id_red: hue_analogous,
			hue_id_yellow: hue_analogous,
			hue_id_blue: hue_atk_complementary,
			hue_id_cyan: hue_special_complementary,
			hue_id_cobalt: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},
	),
	EwHue(
		id_hue = hue_id_red,
		alias = [
			"reddye",
			"blood",
			"cabbage"
		],
		str_saturate = "It darkens a deep shade of crimson red!",
		str_name = "red",
		str_desc = "Its deep burgundy hue reminds you of a rare steak’s leaked myoglobin.",
		effectiveness = {
			hue_id_pink: hue_analogous,
			hue_id_orange: hue_analogous,
			hue_id_cobalt: hue_atk_complementary,
			hue_id_teal: hue_special_complementary,
			hue_id_cyan: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},

	),
	EwHue(
		id_hue = hue_id_magenta,
		alias = [
			"magentadye",
			"joybeans"
		],
		str_saturate = "It turns a vivid magenta!",
		str_name = "magenta",
		str_desc = "It’s vivid magenta that fills you with energy and excitement every time you see it.",
		effectiveness = {
			hue_id_pink: hue_analogous,
			hue_id_purple: hue_analogous,
			hue_id_teal: hue_atk_complementary,
			hue_id_lime: hue_special_complementary,
			hue_id_green: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},
	),
	EwHue(
		id_hue = hue_id_purple,
		alias = [
			"purpledye",
			"purplekilliflower",
			"killer"
		],
		str_saturate = "It turns a dark purple!",
		str_name = "purple",
		str_desc = "Its dark purple hue gives it a brooding, edgy appearance. It will huff and groan when given orders, like a teenage rebelling against his mom in the most flaccid way possible.",
		effectiveness = {
			hue_id_blue: hue_analogous,
			hue_id_magenta: hue_analogous,
			hue_id_green: hue_atk_complementary,
			hue_id_yellow: hue_special_complementary,
			hue_id_lime: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},
	),
	EwHue(
		id_hue = hue_id_blue,
		alias = [
			"bluedye",
			"razornuts"
		],
		str_saturate = "It turns a deep blue!",
		str_name = "blue",
		str_desc = "Its deep blue hue reminds you of those “ocean” things you’ve heard so much of in the movies and video games that have washed ashore the coast of the Slime Sea.",
		effectiveness = {
			hue_id_cobalt: hue_analogous,
			hue_id_purple: hue_analogous,
			hue_id_lime: hue_atk_complementary,
			hue_id_orange: hue_special_complementary,
			hue_id_yellow: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},
	),
	EwHue(
		id_hue = hue_id_green,
		alias = [
			"greendye",
			"pawpaw",
			"juvie"
		],
		str_saturate = "It turns a shade of green that barely distinguishes itself from a Slimeoid’s standard hue.",
		str_name = "green",
		str_desc = "Its unimpressive green hue does nothing to separate itself from the swathes of the undyed Slimeoids of the working class.",
		effectiveness = {
			hue_id_lime: hue_analogous,
			hue_id_teal: hue_analogous,
			hue_id_pink: hue_atk_complementary,
			hue_id_purple: hue_special_complementary,
			hue_id_magenta: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},
	),
	EwHue(
		id_hue = hue_id_teal,
		alias = [
			"tealdye",
			"sludgeberries"
		],
		str_saturate = "It looks so purdy now!",
		str_name = "teal",
		str_desc = "Its caliginous teal hue gives you a sudden lust for prosecuting criminals in the legal system, before coming to your senses and realizing there is no legal system here.",
		effectiveness = {
			hue_id_green: hue_analogous,
			hue_id_cyan: hue_analogous,
			hue_id_red: hue_atk_complementary,
			hue_id_magenta: hue_special_complementary,
			hue_id_pink: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},
	),
	EwHue(
		id_hue = hue_id_rainbow,
		alias = [
			"rainbowdye",
			"suganmanuts"
		],
		str_saturate = "It turns a fantastic shade of... well, everything!!",
		str_name = "***Rainbow***",
		str_desc = "Its ***Rainbow*** hue dazzles and amazes you. It comprises the whole color spectrum in an crude, Photoshop-tier gradient. It’s so obnoxious… and yet, decadent!",
	),
	EwHue(
		id_hue = hue_id_pink,
		alias = [
			"pinkdye",
			"pinkrowddishes"
		],
		str_saturate = "It turns a vibrant shade of  pink!",
		str_name = "pink",
		str_desc = "Its vibrant pink hue imbues the Slimeoid with an uncontrollable lust for destruction. You will often see it flailing about happily, before knocking down a mailbox or kicking some adult in the shin.",
		effectiveness = {
			hue_id_magenta: hue_analogous,
			hue_id_red: hue_analogous,
			hue_id_cyan: hue_atk_complementary,
			hue_id_green: hue_special_complementary,
			hue_id_teal: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},
	),
	EwHue(
		id_hue = hue_id_grey,
		alias = [
			"greydye",
			"dankwheat"
		],
		str_saturate = "It turns a dull, somber grey.",
		str_name = "grey",
		str_desc = "Its dull grey hue depresses you, lulling you into inaction and complacency. ",
		is_neutral = True,
	),
	EwHue(
		id_hue = hue_id_cobalt,
		alias = [
			"cobaltdye",
			"brightshade"
		],
		str_saturate = "It turns a shimmering cobalt!",
		str_name = "cobalt",
		str_desc = "Its shimmering cobalt hue can reflect images if properly polished.",
		effectiveness = {
			hue_id_cyan: hue_analogous,
			hue_id_blue: hue_analogous,
			hue_id_yellow: hue_atk_complementary,
			hue_id_red: hue_special_complementary,
			hue_id_orange: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},
	),
	EwHue(
		id_hue = hue_id_black,
		alias = [
			"blackdye",
			"blacklimes"
		],
		str_saturate = "It turns pitch black!",
		str_name = "black",
		str_desc = "Its pitch black, nearly vantablack hue absorbs all the light around it, making this Slimeoid appear as though a hole was ripped right out of reality.",
		is_neutral = True,
	),
	EwHue(
		id_hue = hue_id_lime,
		alias = [
			"limedye",
			"phosphorpoppies"
		],
		str_saturate = "It turns a heavily saturated lime!",
		str_name = "lime",
		str_desc = "Its heavily saturated lime hue assaults your eyes in a way not unlike the Slime Sea. That is to say, painfully.",
		effectiveness = {
			hue_id_yellow: hue_analogous,
			hue_id_green: hue_analogous,
			hue_id_magenta: hue_atk_complementary,
			hue_id_blue: hue_special_complementary,
			hue_id_purple: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},
	),
	EwHue(
		id_hue = hue_id_cyan,
		alias = [
			"cyandye",
			"direapples"
		],
		str_saturate = "It turned a light cyan!",
		str_name = "cyan",
		str_desc = "Its light cyan hue imbues it with a slightly anxious demeanor, it is sure to avoid sewer manholes when walking down the street.",
		effectiveness = {
			hue_id_teal: hue_analogous,
			hue_id_cobalt: hue_analogous,
			hue_id_orange: hue_atk_complementary,
			hue_id_pink: hue_special_complementary,
			hue_id_red: hue_full_complementary,
			hue_id_rainbow: hue_full_complementary
		},
	),
	EwHue(
		id_hue = hue_id_brown,
		alias = [
			"browndye",
		],
		str_saturate = "It turned an earthly brown!",
		str_name = "brown",
		str_desc = "Its earthly brown hue imbues it with a humble, down-to-earth personality.",
		is_neutral = True,
	),
	EwHue(
		id_hue = hue_id_copper,
		alias = [
			"copperpaint",
		],
		str_saturate = "It was given a coating of bright copper!",
		str_name = "copper",
		str_desc = "It seems to feel good about its copper coating.",
		is_neutral = True,
	),
	EwHue(
		id_hue = hue_id_chrome,
		alias = [
			"chromepaint",
		],
		str_saturate = "It was given a coating of silvery chrome!",
		str_name = "chrome",
		str_desc = "It's content with its chrome coating.",
		is_neutral = True,
	),
	EwHue(
		id_hue = hue_id_gold,
		alias = [
			"goldpaint",
		],
		str_saturate = "It was given a coating of dazzling gold!",
		str_name = "gold",
		str_desc = "It prides itself on its shiny golden coating.",
		is_neutral = True,
	),
]

# A map of id_hue to EwHue objects.
hue_map = {}

# A list of hue names
hue_names = []

# Populate hue map, including all aliases.
for hue in hue_list:
	hue_map[hue.id_hue] = hue
	hue_names.append(hue.id_hue)

	for alias in hue.alias:
		hue_map[alias] = hue# A map of id_hue to EwHue objects.

# Things a slimeoid might throw
thrownobjects_list = [
	"sewer cap",
	"boulder",
	"chunk of broken asphalt",
	"broken fire hydrant",
	"SlimeCorp-Brand Slime Containment Vessel (tm)",
	"piece of sheet metal",
	"burning tire",
	"hapless bystander",
	"completely normal small mammal",
	"heap of broken glass",
	"stereotypical nautical anchor",
	"piece of an iron girder",
	"pile of lumber",
	"pile of bricks",
	"unrecognizably decayed animal carcass",
	"very fortuitously abandoned javelin",
	"large rock",
	"small motor vehicle",
	"chunk of broken concrete",
	"piece of rusted scrap metal",
	"box overflowing with KFC branded bbq sauce",
	"Nokia 3310"
]

mutation_id_spontaneouscombustion = "spontaneouscombustion"
#mutation_id_thickerthanblood = "thickerthanblood"
mutation_id_graveyardswift = "graveyardswift" #TODO
mutation_id_fungalfeaster = "fungalfeaster"
mutation_id_sharptoother = "sharptoother"
mutation_id_openarms = "openarms" #TODO
mutation_id_2ndamendment = "2ndamendment"
mutation_id_panicattacks = "panicattacks" #TODO
mutation_id_twobirdswithonekidneystone = "2birds1stone" #TODO
mutation_id_shellshock = "shellshock" #TODO
mutation_id_bleedingheart = "bleedingheart"
mutation_id_paranoia = "paranoia" #TODO
mutation_id_cloakandstagger = "cloakandstagger" #TODO
mutation_id_nosferatu = "nosferatu"
mutation_id_organicfursuit = "organicfursuit"
mutation_id_lightasafeather = "lightasafeather"
mutation_id_whitenationalist = "whitenationalist"
mutation_id_spoiledappetite = "spoiledappetite"
mutation_id_bigbones = "bigbones"
mutation_id_fatchance = "fatchance"
mutation_id_fastmetabolism = "fastmetabolism"
mutation_id_bingeeater = "bingeeater"
mutation_id_lonewolf = "lonewolf"
mutation_id_quantumlegs = "quantumlegs"
mutation_id_chameleonskin = "chameleonskin"
mutation_id_patriot = "patriot"
mutation_id_socialanimal = "socialanimal"
mutation_id_corpseparty = "corpseparty" #TODO
mutation_id_threesashroud = "threesashroud"
mutation_id_aposematicstench = "aposematicstench"
mutation_id_paintrain = "paintrain" #TODO
mutation_id_lucky = "lucky"
mutation_id_dressedtokill = "dressedtokill"
mutation_id_keensmell = "keensmell"
mutation_id_enlargedbladder = "enlargedbladder"
mutation_id_dumpsterdiver = "dumpsterdiver"
mutation_id_trashmouth = "trashmouth"
mutation_id_webbedfeet = "webbedfeet"

mutation_id_davyjoneskeister = "davyjoneskeister"
mutation_id_stickyfingers = "stickyfingers"
mutation_id_coleblooded = "coleblooded"
mutation_id_packrat = "packrat"
mutation_id_nervesofsteel = "nervesofsteel"
mutation_id_lethalfingernails = "lethalfingernails"
mutation_id_napalmsnot = "napalmsnot"
mutation_id_ambidextrous = "ambidextrous"
mutation_id_landlocked = "landlocked"
mutation_id_dyslexia = "dyslexia"
mutation_id_oneeyeopen = "oneeyeopen"
mutation_id_ditchslap = "ditchslap"
mutation_id_greenfingers = "greenfingers"
mutation_id_handyman = "handyman"
mutation_id_unnaturalcharisma = "unnaturalcharisma"
mutation_id_bottomlessappetite = "bottomlessappetite"
mutation_id_rigormortis = "rigormortis"
mutation_id_longarms = "longarms"
mutation_id_airlock = "airlock"
mutation_id_lightminer = "lightminer"
mutation_id_amnesia = "amnesia"

mutation_milestones = [5,10,15,20,25,30,35,40,45,50]

mutations = [
	EwMutationFlavor(
		id_mutation = mutation_id_spontaneouscombustion,
		str_name = "Spontaneous Combustion",
		alias = ['sc', 'spc', 'spontaneous', 'combustion'],
		str_describe_self = "On the surface you look calm and ready, probably unrelated to your onset of **Spontaneous Combustion**.",
		str_describe_other = "On the surface they look calm and ready, probably unrelated to their onset of **Spontaneous Combustion**.",
		str_acquire = "Deep inside your chest you feel a slight burning sensation. You suddenly convulse for a few moments, before… returning basically to normal. Huh, that’s weird. Oh well, I guess nothing happened. You have developed the mutation **Spontaneous Combustion**.",
		tier = 5,
        str_transplant = "Dr. Dustrap pulls out a gigantic cylinder of pressurized hydrogen and sticks the valve directly into your bone marrow. 'Just say when,' she says with a mischevious smile, immediately flooding your body with gas and nearly ripping the skin off your muscles. After the pain subsides, you feel bloated, but somehow lighter.\n\n You have developed the mutation **Spontaneous Combustion**. On death, deal blast damage to all enemies in the zone.",
		),
	EwMutationFlavor(
		id_mutation = mutation_id_fungalfeaster,
		str_name="Fungal Feaster",
        alias = ['ff', 'fungal', 'feaster', 'fungus'],
		str_describe_self = "Tiny mushrooms and other fungi sprout from the top of your head and shoulders due to **Fungal Feaster**.",
		str_describe_other = "Tiny mushrooms and other fungi sprout from the top of their head and shoulders due to **Fungal Feaster**.",
		str_acquire = "Your saliva thickens, pouring out of your mouth with no regulation. A plethora of funguses begin to grow from your skin, causing you to itch uncontrollably. You feel an intense hunger for the flesh of another juvenile. You have developed the mutation **Fungal Feaster**. On a fatal blow, restore all hunger.",
		tier = 4,
        str_transplant = "The procedure is simple: just a few quick injections to the head. Not 5 minutes afterward, the fungi start growing out of your scalp and into your synapses. Luckily, there isn't an intelligence stat in this game, or you'd be fucked.\n\nYou have developed the mutation **Fungal Feaster**. On a fatal blow, restore all hunger.",
		),
	EwMutationFlavor(
		id_mutation = mutation_id_sharptoother,
		str_name="Sharptoother",
        alias = ['st', 'tooth', 'sharp', 'sharptooth'],
		str_describe_self = "Your inhuman hand-eye-teeth coordination is the stuff of legends due to **Sharptoother**.",
		str_describe_other = "Their inhuman hand-eye-teeth coordination is the stuff of legends due to **Sharptoother**.",
		str_acquire = "Your pupils dilate, a cacophony of previously imperceivable noises floods into your head. Your canines pop out of your skull, making room for monstrously oversized saber-tooth replacements. Your fingers twitch frequently, begging to pull a trigger, any trigger. You have developed the mutation **Sharptoother**. Halved miss chance.",
		tier = 6,
		str_transplant = "You notice that one of the dentistry options on the hospital menu is just called \"The Works\". Well, no stone left unturned. One by one, she pulls all your teeth, takes out a whittlin\' knife, and carves out some purty looking pointy ones. Maybe this lady is a psychopathic quack doctor, but she has excellent craftsmanship.\n\nYou have developed the mutation **Sharptoother**. Halved miss chance.",
		),
	EwMutationFlavor(
		id_mutation = mutation_id_2ndamendment,
		str_name="2nd Amendment",
        alias = ['2a', 'second', 'secondamendment'],
		str_describe_self = "A spare pair of arms extend from your monstrously large shoulders due to **2nd Amendment**.",
		str_describe_other = "A spare pair of arms extend from their monstrously large shoulders due to **2nd Amendment**.",
		str_acquire = "You feel an intense, sharp pain in the back of your shoulders. Skin tears and muscles rip as you grow a brand new set of arms, ready, willing, prepared to fight. You have developed the mutation **2nd Amendment**. Extra equippable gun slot, and a damage bonus when sidearming another weapon.",
		tier = 5,
        str_transplant = "Dustrap clamps your eyes open and takes an old CRT out from the hall closet. You spend hours watching gang violence propaganda and screaming jingoism and racial slurs along with the show. The pure testosterone of the moment compels two beefy arms to violently sprout from your shoulders.\n\nYou have developed the mutation **2nd Amendment**. Extra equippable gun slot, and a damage bonus when sidearming another weapon.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_bleedingheart,
		str_name="Bleeding Heart",
        alias = ['bleed', 'bh', 'bdh'],
		str_describe_self = "Your heartbeat’s rhythm is sporadic and will randomly change intensity due to **Bleeding Heart**.",
		str_describe_other = "Their heartbeat’s rhythm is sporadic and will randomly change intensity due to **Bleeding Heart**.",
		str_acquire = "To say you experience “heart palpitations” is a gross understatement. Your heart feels like it explodes and reforms over and over for the express amusement of some cruel god’s sick sense of humor. You begin to cough up blood and basically continue to do so for the rest of your life. You have developed the mutation **Bleeding Heart**. When hit, bleeding is delayed for 5 minutes.",
		tier = 4,
        str_transplant = "Auntie Dustrap takes one of her scalpels and jams it deep into your chest. Your heart, as is natural for a stabbed heart, begins to sputter and palpitate. Looks like the surgery is over. Shit, you could've done that yourself.\n\nYou have developed the mutation **Bleeding Heart**. When hit, bleeding is delayed for 5 minutes.",
		),
	EwMutationFlavor(
		id_mutation = mutation_id_nosferatu,
		str_name="Noseferatu",
        alias = ['nose', 'nf', 'vampire'],
		str_describe_self = "Your freakishly huge, hooked schnoz and pointed ears give you a ghoulish appearance due to **Noseferatu**.",
		str_describe_other = "Their freakishly huge, hooked schnoz and pointed ears give them a ghoulish appearance due to **Noseferatu**.",
		str_acquire = "The bridge of your nose nearly triples in size. You recoil as the heat of nearby lights sear your skin, forcing you to seek cover under the shadows of dark, secluded alleyways. Your freakish appearance make you a social outcast, filling you with a deep resentment which evolves into unbridled rage. You will have your revenge. You have developed the mutation **Noseferatu**. At night, when attacking, 60% of splattered slime is absorbed directly into your slimecount.",
		tier = 5,
        str_transplant = "You ask for the super jumbo size nose job. The doctor blindfolds you and takes you to her van. A quick drive later, you arrive at Slimecorp Labs, where you descend to the embiggening ward. A small amount of bright green fluid gets injected into the tip of your nose, and it grows to sizes beyond your wildest dreams.\n\nYou have developed the mutation **Noseferatu**. At night, when attacking, 60% of splattered slime is absorbed directly into your slimecount.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_organicfursuit,
		str_name="Organic Fursuit",
        alias = ['ogf', 'organic', 'fursuit', 'of'],
		str_describe_self = "Your shedding is a constant source of embarrassment due to **Organic Fursuit**.",
		str_describe_other = "Their shedding is a constant source of embarrassment due to **Organic Fursuit**.",
		str_acquire = "An acute tingling sensation shoots through your body, causing you to start scratching uncontrollably. You fly past puberty and begin growing frankly alarming amounts of hair all over your body. Your fingernails harden and twist into claws. You gain a distinct appreciation for anthropomorphic characters in media, even going to the trouble of creating an account on an erotic furry roleplay forum. Oh, the horror!! You have developed the mutation **Organic Fursuit**. Double damage dealt, 1/10th damage taken and enhanced movement speed every 31st night.",
		tier = 2,
        str_transplant = "Dr. Dustrap asks you if you're feeling down. Why yes, you suppose you do. She then introduces you to her two snarling therapy dogs: Gank and Yiffy. They take turns biting you in the neck and subconciously indoctrinating you into the furry fandom.\n\nYou have developed the mutation **Organic Fursuit**. Double damage dealt, 1/10th damage taken and enhanced movement speed every 31st night.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_lightasafeather,
		str_name="Light as a Feather",
        alias = ['laaf', 'laf', 'lf', 'feather'],
		str_describe_self = "Your anorexic, frail physique causes even light breezes to blow you off course due to **Light As A Feather**.",
		str_describe_other = "Their anorexic, frail physique causes even light breezes to blow them off course due to **Light As A Feather**.",
		str_acquire = "Your body fat begins to dissolve right before your eyes, turning into a foul-smelling liquid that drenches the floor beneath you. You quickly pass conventionally attractive weights and turn into a hideous near-skeleton. The only thing resting between your bones and your skin is a thin layer of muscles that resemble lunch meat slices. You have developed the mutation **Light As A Feather**. Double movement speed while weather is windy.",
		tier = 3,
        str_transplant = "You decide to get the liposuction deluxe package. Once in the OR, you are prodded on all sides with a surgical vacuum, sucking out whatever looks unneccesary. She takes a couple kidneys and you gallbladder though, so maybe the word necessary is a bit subjective. All is forgiven though; your new flabby frame gives flying squirrels a run for their money.\n\nYou have developed the mutation **Light As A Feather**. Double movement speed while weather is windy.",
		),
	EwMutationFlavor(
		id_mutation = mutation_id_whitenationalist,
		str_name="White Nationalist",
        alias = ['wn', 'white', 'racism'],
		str_describe_self = "Your bleached white, peeling skin is surely the envy of lesser races due to **White Nationalist**.",
		str_describe_other = "Their bleached white, peeling skin is surely the envy of lesser races due to **White Nationalist**.",
		str_acquire = "Every pore on your skin suddenly feels like it’s being punctured by a rusty needle. Your skin’s pigment rapidly desaturates to the point of pure #ffffff whiteness. You suddenly love country music, too. Wow, that was a really stupid joke. You have developed the mutation **White Nationalist**. Scavenge bonus and cannot be scouted while weather is snowy.",
		tier = 1,
        str_transplant = "You are led to the clinic's basement, where you find an empty laptop sitting on the dark cement floor. The keyboard and mouse are broken, and it's got Richard Spencer tirades on autoplay. All of a sudden, the door locks. You spend an indefinite amount of time slowly falling in love with his dreamy soft-serve flip haircut, and as you waste away you eventually grow deathly pale, too.\n\nYou have developed the mutation **White Nationalist**. Scavenge bonus and cannot be scouted while weather is snowy.",
		),
	EwMutationFlavor(
		id_mutation = mutation_id_spoiledappetite,
		str_name="Spoiled Appetite",
        alias = ['spoiled'],
		str_describe_self = "Your frequent, unholy belches could incapacitate a Megaslime due to **Spoiled Appetite**.",
		str_describe_other = "Their frequent, unholy belches could incapacitate a Megaslime due to **Spoiled Appetite**.",
		str_acquire = "You become inexplicably tired, you develop bags under your eyes and can barely keep them open without fidgeting. Stenches begin to secrete from your body, which only worsens as your stomach lets out a deep, guttural growl that sounds like a dying animal being raped by an already dead animal. Which is to say, not pleasant. You are overcome with a singular thought. “What the hell, I’ll just eat some trash.” You have developed the mutation **Spoiled Appetite**. You can now eat spoiled food.",
		tier = 7,
        str_transplant = "You are force-fed cole slaw for several hours. Your desensitized taste buds will never recover from this, and you feel like you could digest anything. Of course, in her infinite wisdom, Dusttrap uses organic cole slaw, so you can't even bust ghosts afterward.\n\nYou have developed the mutation **Spoiled Appetite**. You can now eat spoiled food.",
		),
	EwMutationFlavor(
		id_mutation = mutation_id_bigbones,
		str_name="Big Bones",
        alias = ['bb', 'bones', 'big'],
		str_describe_self = "You can often be seen consuming enough calories to power a small country due to **Big Bones**.",
		str_describe_other = "They can often be seen consuming enough calories to power a small country due to **Big Bones**.",
		str_acquire = "Your can actively feel your brain being squeezed and your heart being nearly crushed by your rib cage as every bone in your body doubles in size. Your body fat doubles in density, requiring great strength and energy for even simple movements. You have developed the mutation **Big Bones**. Double food carrying capacity.",
		tier = 4,
		str_transplant = "Dusttrap lets out a heavy sigh. This one's gonna take some work. You lay down on the operating table, and she proceeds to take out literally every bone in your body, even those gay ass ear ones and the fingery bits. She painstakingly coats them in several coats of fiberglass and takes the spare skin off a local cadaver to extend your flesh to refit the new ones. It is a painful, world-changing experience for you and her both. You just had to be fat, didn't you?\n\nYou have developed the mutation **Big Bones**. Double food carrying capacity."
		),
	EwMutationFlavor(
		id_mutation = mutation_id_fatchance,
		str_name="Fat Chance",
        alias=['fc', 'fat', 'chance', 'obesity'],
		str_describe_self = "Your impressive girth provides ample amounts of armor against attacks due to **Fat Chance**.",
		str_describe_other = "Their impressive girth provides ample amounts of armor against attacks due to **Fat Chance**.",
		str_acquire = "Your body begins to swell, providing you with easily hundreds of extra pounds nigh instantaneously. Walking becomes difficult, breathing even more so. Your fat solidifies into a brick-like consistency, turning you into a living fortress. You only have slightly increased mobility than a regular fortress, however. You have developed the mutation **Fat Chance**. Take 25% less damage when above 50% hunger.",
        tier = 5,
        str_transplant = "'Alright', Dusttrap says, 'I want to go to the food court and eat as many Doritos Locos Tacos as you can steal, then take these pills.' You have an amazing time mercilessly stuffing your face and getting away with grand theft taco scot-free. That said, you think you got scammed by that doctor. The pills are placebos, you basically only needed to get really fat.\n\n You have developed the mutation **Fat Chance**. Take 25% less damage when above 50% hunger.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_fastmetabolism,
		str_name="Fast Metabolism",
        alias=['fm', 'metabolism'],
		str_describe_self = "Fierce boiling and sizzling can be heard from deep inside your stomach due to **Fast Metabolism**.",
		str_describe_other = "Fierce boiling and sizzling can be heard from deep inside their stomach due to **Fast Metabolism**.",
		str_acquire = "An intense heat is felt in the pit of your stomach, which wails in pain as it’s dissolved from the inside out. Your gastric acid roars to an unthinkably destructive fever pitch, ready to completely annihilate whatever poor calories may enter your body before instantly turning them into pure leg muscle. You have developed the mutation **Fast Metabolism**. Doubled movement speed at below 50% hunger.",
		tier = 6,
		str_transplant = "Dusttrap grabs a small bottle in the back. 'You're gonna have to take all these pills. I bought these from infomercials and I'm not really sure which ones work yet.' Welp, bottoms up. With the hesitation of a hardened gangster, you slide the pills down your gullet. In your stomach they begin to bubble and boil, and you can sense a hint of smoke in your breath.\n\nYou have developed the mutation **Fast Metabolism**. Doubled movement speed at below 50% hunger.",
		),
	EwMutationFlavor(
		id_mutation = mutation_id_bingeeater,
		str_name="Binge Eater",
        alias = ['binge', 'be'],
		str_describe_self = "You’re always one criticism away from devouring several large pizzas due to **Binge Eater**.",
		str_describe_other = "They’re always one criticism away from devouring several large pizzas due to **Binge Eater**.",
		str_acquire = "Your mouth begins to mimic chewing over and over again, opening and closing all on it’s own. You’re suddenly able to smell the food being carried by passersby for sometimes hours after they’ve left your sight. Your mouth dries and you sweat profusely even just being in the same room as food. Even now, just thinking about food, you begin to tremble. You can barely contain yourself. You don’t need it. You don’t need it. You don’t need it. You don’t need it... You need it. You have developed the mutation **Binge Eater**. Upon eating food, the restored hunger is multiplied by the number of dishes you’ve consumed in the past 5 seconds.  If you eat many food items at once, go into a 5 minute food coma that buffs your defense.",
        tier = 5,
        str_transplant="Dr. Dusttrap offers you some cookies from her employee lounge. You decide to accept. However, she didn't tell you they be full of morphine and 70-year old antidepressants. You compulsively start eating and your metabolism begins to enter a state of eternal balls-tripping. The magnitude of hunger is so uncontrollable you consider cannibalizing Dusttrap herself. Don't worry, eventually it will calm down, so long as you don't have a relapse.\n\n You have developed the mutation **Binge Eater**. Upon eating food, the restored hunger is multiplied by the number of dishes you’ve consumed in the past 5 seconds. If you eat many food items at once, go into a 5 minute food coma that buffs your defense."
        ),
	EwMutationFlavor(
		id_mutation = mutation_id_lonewolf,
		str_name="Lone Wolf",
        alias = ['lw', 'lone', 'wolf'],
		str_describe_self = "You stand out from the crowd, mostly because you stay far away from them due to **Lone Wolf**.",
		str_describe_other = "They stand out from the crowd, mostly because they stay far away from them due to **Lone Wolf**.",
		str_acquire = "Your eyes squint and a growl escapes your mouth. You begin fostering an unfounded resentment against your fellow juveniles, letting it bubble into a burning hatred in your chest. You snarl and grimace as people pass beside you on the street. All you want to do is be alone, no one understands you anyway. You have developed the mutation **Lone Wolf**. 50% damage buff when in a district alone.",
		tier = 7,
        str_transplant = "After a long time under the knife, you wake up to find your genes spliced with the DNA of Dr. Wolf. You are both unwilling and unable to engage in conversation with anybody, and deep within your soul, you develop the uncontrollable urge to pout.\n\nYou have developed the mutation **Lone Wolf**. 50% damage buff when in a district alone."),
	EwMutationFlavor(
		id_mutation = mutation_id_quantumlegs,
		str_name="Quantum Legs",
        alias = ['ql', 'quantum'],
		str_describe_self = "You’ve got nothing of note below the belt due to **Quantum Legs**.",
		str_describe_other = "They’ve got nothing of note below the belt due to **Quantum Legs**.",
		str_acquire = "Before you can even register it’s happening, your legs simply evaporate into a light mist that dissolves into the atmosphere. You ungracefully fall to the ground in pure shock, horror, and unrivaled agony. You are now literally half the person you used to be. What the hell are you supposed to do now? You scramble to try and find someone that can help you, moving to a nearby phone booth. Wait… how did you just do that? You have developed the mutation **Quantum Legs**. You can now use the !tp command, allowing you to teleport to a district up to two locations away from you after an uninterrupted 15 second running start, with a cooldown of 3 hours.",
        tier=5,
        str_transplant="Dr. Dusttrap places you under hypnosis, using the power of psychological suggestion to convince you your legs aren't real. She then covers your lower half in a tarp and sets up an elaborate poison injection system that places your legs in a superposition of life and death. When the tarp comes off, your legs are gone. You hop off the table and somehow walk back to the waiting room.\n\nYou have developed the mutation **Quantum Legs**. You can now use the !tp command, allowing you to teleport to a district up to two locations away from you after an uninterrupted 15 second running start, with a cooldown of 3 hours.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_chameleonskin,
		str_name="Chameleon Skin",
        alias = ['cs', 'chameleon'],
		str_describe_self = "Your skin quickly adjusts and camouflages you in your current surroundings due to **Chameleon Skin**.",
		str_describe_other = "Their skin quickly adjusts and camouflages them in their current surroundings due to **Chameleon Skin**.",
		str_acquire = "You feel a scraping sensation all over your body, like you’re being sunburned and skinned alive at the same exact time. You begin to change hue rapidly, flipping through a thousand different colors, patterns, and textures. Every individual minor change in value across your entire body feels like you’re being dismembered. This transpires for several agonizing seconds before your body settles on a perfect recreation of your current surroundings. For all intents and purposes, you are transparent. You have developed the mutation **Chameleon Skin**. While offline, you can move and scout other districts and cannot be scouted.",
        tier=5,
        str_transplant="The doctor pulls out a large vat of glittering maroon ink, and uses it to fill what looks like a tattoo needle. Sure enough, that's what it is. You brace yourself for the arduous process of getting a complete full-body tattoo. Dusttrap assures you that while this will be extremely painful as usual, it doesn't count as blackface.  The eyelids end up being a particularly nasty part of it. Good news is, by the end, you've learned how this ink changes color based on temperature and pressure, and have mastered the art of blending in.\n\nYou have developed the mutation **Chameleon Skin**. While offline, you can move and scout other districts and cannot be scouted.",

    ),
	EwMutationFlavor(
		id_mutation = mutation_id_patriot,
		str_name="Patriot",
        alias = ['pt'],
		str_describe_self = "You beam with intense pride over your faction’s sophisticated culture and history due to **Patriot**.",
		str_describe_other = "They beam with intense pride over their faction’s sophisticated culture and history due to **Patriot**.",
		str_acquire = "Your brain’s wrinkles begin to smooth themselves out, and you are suddenly susceptible to being swayed by propaganda. Suddenly, your faction’s achievements flash before your eyes. All of the glorious victories it has won, all of its sophisticated culture and history compels you to action. You have developed the mutation **Patriot**. 20% capture discount.",
        tier=6,
        str_transplant="You are led into a room with a projector and told to sit down. Each slide has a different gang's propaganda on it. Every time your gang's propaganda shows up, you get a glob of slime. For your enemy gang, you get tased. The process continues until Pavlov has made you his bitch. Allegiance is all you understand.\n\nYou have developed the mutation **Patriot**. 20% capture discount.",

    ),
	EwMutationFlavor(
		id_mutation = mutation_id_socialanimal,
		str_name="Social Animal",
        alias = ['social', 'animal'],
		str_describe_self = "Your charming charisma and dashing good looks make you the life of the party due to **Social Animal**.",
		str_describe_other = "Their charming charisma and dashing good looks make them the life of the party due to **Social Animal**.",
		str_acquire = "You begin to jitter and shake with unusual vim and vigor. Your heart triples in size and you can’t help but let a toothy grin span from ear to ear as a bizarre energy envelopes you. As long as you’re with your friends, you feel like you can take on the world!! You have developed the mutation **Social Animal**. Your damage increases by 10% for every ally in your district.",
        tier=4,
        str_transplant="Dr. Dusttrap takes a long hard look at you. 'Nope, can't do it,' she says, nonetheless directing you to the operating table. In the end, instead of making you more charismatic, she just switches your brain for someone better than you. Well, we can't win 'em all. Sometimes there's just no way to salvage a violent antisocial personality like yours.\n\nYou have developed the mutation **Social Animal**. Your damage increases by 10% for every ally in your district.",

    ),
	EwMutationFlavor(
		id_mutation = mutation_id_threesashroud,
		str_name="Three's a Shroud",
        alias = ['3s', 'shroud', '3as'],
		str_describe_self = "You tend to blend into the crowd due to **Three’s A Shroud**.",
		str_describe_other = "They tend to blend into the crowd due to **Three’s A Shroud**.",
		str_acquire = "A distinct sense of loneliness pervades your entire body. You’re reduced to the verge of tears without really knowing why. You suddenly feel very conscious of how utterly useless you are. You want to fade away so badly, you’d give anything just to be invisible. Everyone would like it better that way. You have developed the mutation **Three’s A Shroud**. Cannot be scouted and crit rate doubled if there are more than 3 allies in your district.",
        tier=3,
        str_transplant="Botox is injected into your upper and lower jaw muscles. The simplest method needed to blend into the crowd just turns out to be making it hurt to speak or eat. You become scrawnier and more unassuming, and you slowly begin to fade out of conversations. Paying for a surgery like this was probably a terrible idea.\n\nYou have developed the mutation **Three’s A Shroud**. Cannot be scouted and crit rate doubled if there are more than 3 allies in your district.",

    ),
	EwMutationFlavor(
		id_mutation = mutation_id_aposematicstench,
		str_name="Aposematic Stench",
        alias = ['as', 'stench'],
		str_describe_self = "A putrid stench permeates around you all hours of the day due to **Aposematic Stench**.",
		str_describe_other = "A putrid stench permeates around them all hours of the day due to **Aposematic Stench**.",
		str_acquire = "Your eyes water as you begin secreting pheromones into the air from every indecent nook and cranny on your body. You smell so unbelievably terrible that even you are not immune from frequent coughs and wheezes when you catch a particularly bad whiff. You have developed the mutation **Aposematic Stench**. For every 5 levels you gain, you appear as 1 more person when being scouted. Use !stink to put on secreature repellent at any time.",
        tier=3,
        str_transplant="Dr. Dusttrap installs a slot in the small of your back that fits Fuck Energy Bodyspray canisters into it. She tells you that this will augment your hormones to make you smell terrible. Makes sense, you suppose. It'd be nice if she didn't take sponsorships from Slimecorp, though.\n\nYou have developed the mutation **Aposematic Stench**. For every 5 levels you gain, you appear as 1 more person when being scouted. Use !stink to put on secreature repellent at any time.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_lucky,
		str_name="Lucky",
        alias = ['luck'],
		str_describe_self = "You are extremely fortunate due to **Lucky**.",
		str_describe_other = "They are extremely fortunate due to **Lucky**.",
		str_acquire = "Just as you level up, you are struck by lightning. You struggle to stand at first, but after the initial shock wears off you quickly dust the cartoonish soot from your clothes and begin walking again. Then, you’re struck again. You stand up again. This happens a few more times before you’re forced by the astronomically low odds of you being alive to conclude you are a statistical anomaly and thus normal concepts of fortune do not apply to you. You have developed the mutation **Lucky**. Drastically increased chance to unearth slime poudrins and odds of winning slime casino games. !reel chance also increases.",
        tier=5,
        str_transplant="\"Tough luck, runt,\" the doctor says, 'but this is still an experimental treatment.' You roll your eyes, knowing that basically all her surgeries are like that. She starts by taking out her stash of dead leprechauns and transplanting a few body parts. She unexpectedly shoots you through the hand, and you scream in pain. \"Quit yer whinin' I have to do this. If the gun's not jamming that means it didn't work.\" She tried everything in the book, rabbit's foot fingers, lucky penny tooth fillings, you name it. More bullets to the hand. Eventually the luck charm takes after she cuts three of your toes off. Doesn't make sense, but at least nothing unfortunate will happen to you now.\n\nYou have developed the mutation **Lucky**. Drastically increased chance to unearth slime poudrins and odds of winning slime casino games. !reel chance also increases.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_dressedtokill,
		str_name="Dressed to Kill",
        alias = ['dtk', 'dressed', 'kill'],
		str_describe_self = "You’re fabulously accompanied by a wide range of luxurious cosmetics due to **Dressed to Kill**.",
		str_describe_other = "They’re fabulously accompanied by a wide range of luxurious cosmetics due to **Dressed to Kill**.",
		str_acquire = "You are rocked by a complete fundamental change in your brain’s chemistry. Practically every cell in your body is reworked to apply this, the most ambitious mutation yet. You gain an appreciation for French haute couture. You have developed the mutation **Dressed to Kill**. Damage bonus if freshness is at least 250.",
        tier=7,
        str_transplant="Some would say acclimating a juvenile delinquent to French haute coture is impossible. There's a simple way to do it, as you quickly find out. The easiest way in is by showing them the insane violence of the French Revolution. Using heads on pikes as a gateway drug, you quickly become cultured in their frou frou mannerisms.\n\n You have developed the mutation **Dressed to Kill**. Damage bonus if freshness is at least 250.",

    ),
	EwMutationFlavor(
		id_mutation = mutation_id_keensmell,
		str_name="Keen Smell",
        alias = ['ks', 'smell', 'keen'],
		str_describe_self = "You have an uncanny ability to track and identify scents due to **Keen Smell**.",
		str_describe_other = "They have an uncanny ability to track and identify scents due to **Keen Smell**.",
		str_acquire = "You can feel your facial muscles being ripped as your skull elongates your mouth and nose, molding them into an uncanny snout. Your nostrils painfully stretch and elongate to allow for a broad range of olfactory sensations you could only have dreamed of experiencing before. Your nose twitches and you begin to growl as you pick up the scent of a nearby enemy gangster. You have developed the mutation **Keen Smell**. You can now use the !sniff command, allowing you to meticulously list every single player in the targeted district.",
        tier=5,
        str_transplant="You ask for a nose job that will enhance your senses. Ask, and you shall receive. Dr. Dusttrap walks you into the OR, and gives you a catalog of possible noses. You tell her to fuck off and jump into the chair. When you wake up, you are the proud new owner of a snout, one that can sniff the gunpowder off a rifle at 1000 yards.\n\nYou have developed the mutation **Keen Smell**. You can now use the !sniff command, allowing you to meticulously list every single player in the targeted district.",

    ),
	EwMutationFlavor(
		id_mutation = mutation_id_dumpsterdiver,
		str_name="Dumpster Diver",
        alias = ['dd', 'dumpster'],
		str_describe_self = "You are exceptionally good at picking up trash due to **Dumpster Diver**.",
		str_describe_other = "They are exceptionally good at picking up trash due to **Dumpster Diver**.",
		str_acquire = "A cold rush overtakes you, fogging your mind and causing a temporary lapse in vision. When your mind clears again and you snap back to reality, you notice so many tiny details you hadn’t before. All the loose change scattered on the floor, all the pebbles on the sidewalk, every unimportant object you would have normally glanced over now assaults your senses. You have an uncontrollable desire to pick them all up. You have developed the mutation **Dumpster Diver**. 10 times chance to get items while scavenging. Captcha scavenging will use parts of the captcha to scavenge for items.",
        tier=2,
        str_transplant="You ask for the ability to hyperfocus on unimportant trash. In order to accomplish this, you are injected with several vaccines to unrelated diseases until you receive enough to acquire autism. Simple but effective, just like Grandma used to make.\n\nYou have developed the mutation **Dumpster Diver**. 10 times chance to get items while scavenging. Captcha scavenging will use parts of the captcha to scavenge for items.",

    ),
	EwMutationFlavor(
		id_mutation = mutation_id_trashmouth,
		str_name="Trash Mouth",
        alias = ['trash', 'tm'],
		str_describe_self = "You have the mouth of a sailor and the vocabulary of a fourteen year old due to **Trash Mouth**.",
		str_describe_other = "They have the mouth of a sailor and the vocabulary of a fourteen year old due to **Trash Mouth**.",
		str_acquire = "You drop down onto your knees, your inhibitions wash away as a new lust overtakes you. You begin shoveling literally everything you can pry off the floor into your mouth with such supernatural vigor that a nearby priest spontaneously dies. You have developed the mutation **Trash Mouth**. Reach maximum power scavenges faster. You can eat furniture and cosmetics with !devour <item>.",
        tier=5,
        str_transplant="You get off the fucking chair in the goddamn waiting room and ask for a dirty mouth. The bitch doctor thinks you're a retard but slices your body up anyway. After a million fucking years of bullshit you eventually start to develop an extreme oral fixation and want to suck on everything in Dusttrap's office, even including Dusttrap's dusttrap. Whoops, I meant her cunt.\n\nYou have developed the mutation **Trash Mouth**. Reach maximum power scavenges faster. You can eat furniture and cosmetics with !devour <item>.",

    ),
	EwMutationFlavor(
		id_mutation = mutation_id_webbedfeet,
		str_name="Webbed Feet",
        alias = ['wf', 'webbed'],
		str_describe_self = "Your toes are connected by a thin layer of skin due to **Webbed Feet**.",
		str_describe_other = "Their toes are connected by a thin layer of skin due to **Webbed Feet**.",
		str_acquire = "Your feet grow a thin layer of skin, allowing you to swim through piles of slime, soaking up their precious nutrients easily. You have developed the mutation **Webbed Feet**. Your scavenging power increases the more slime there is in a district. You can also feel out the amount of slime you scavenge.",
        tier=4,
        str_transplant="Your feet receive a new transplant, where skinflaps are sewn into the spaces between your toes. Not much complexity or detail work there. You decide that's a good thing.\n\nYou have developed the mutation **Webbed Feet**. Your scavenging power increases the more slime there is in a district. You can also feel out the amount of slime you scavenge.",

    ),
	EwMutationFlavor(
		id_mutation = mutation_id_enlargedbladder,
		str_name="Enlarged Bladder",
        alias = ['eb', 'bladder'],
		str_describe_self = "You have an enlarged bladder due to **Enlarged Bladder**.",
		str_describe_other = "They have an enlarged bladder due to **Enlarged Bladder**.",
		str_acquire = "You feel some mild sensation near your kidney, but you don’t really notice it. You have developed the mutation **Enlarged Bladder**. You may now, finally, piss.",
        tier=0,
        str_transplant="You walk into the office and request the ability to pee. This, of course, is a pretty stupid thing to ask, because that's a basic function of the human body. Moments later, in the operating room, Dusttrap notices you have a cork in your urethra. She sighs, and flicks it out. Congrats, you can !piss now!\n\nYou have developed the mutation **Enlarged Bladder**. You may now, finally, piss.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_davyjoneskeister,
		str_name="Davy Jones' Keister",
        alias = ['djk', 'keister', 'davyjones', 'davy'],
		str_describe_self = "Your ass is tailor made for the high seas due to **Davy Jones' Keister**.",
		str_describe_other = "Their ass is tailor made for the high seas due to **Davy Jones' Keister**.",
		str_acquire = "You begin to feel a crawling sensation on your hindquarters. Layers of skin built for long hours on the tavern bench slowly creep upward along your ass and up your back. Your mind surges with an unfounded confidence as you recall every close call with a secreature and tussle with a gangster. Never have you been on the high seas, not a day in your life, and you're somehow still a sea dog to the bone. For some reason your mind jumps to your conversations with that old fellow at the tavern. Wonder how he's doing? You have developed the mutation **Davy Jones' Keister**. No trash deals when bartering with Albert Alexander.",
        tier=4,
        str_transplant="You are taken into the OR, where you're shown a number of asses in a catalogue. It takes awhile, but you find the \"Old Sea Captain\" model, and she goes to work. You don't know exactly what old Dusttrap did since your back was turned, but when you sit down you think she might've put in some memory foam. Eh, why complain? It's the exact size you ordered.\n\nYou have developed the mutation **Davy Jones' Keister**. No trash deals when bartering with Albert Alexander.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_stickyfingers,
		str_name="Sticky Fingers",
        alias = ['sf', 'sticky'],
		str_describe_self = "Your hands can't let go of anything due to **Sticky Fingers**.",
		str_describe_other = "Their hands can't let go of anything due to **Sticky Fingers**.",
		str_acquire = "Your body begins to tremble, and you get an enormous pressure in your forearms as they begin to turn sickly pale. You feel your pores being pried open, as they excrete a thin layer of film along your palms and down your hand. You glide your fingers across the back of your hand... oh fuck. They won't come apart! You have developed the mutation **Sticky Fingers**. 20% chance to steal from shops when using !order.",
        tier=3,
        str_transplant= "Dr. Dusttrap takes out a culture of artificially developed adhesive bacteria and proceeds to inject it into your bloodstream.\"Now, this'll clog your arteries like nobody's business, but if you want sticky hands, you just gotta grin and bear it. Also, be sure not to take antibiotics ever again, or you'll kill the poor strain.\" After letting the disease settle in, you find you can now sweat glue.\n\nYou have developed the mutation **Sticky Fingers**. 20% chance to steal from shops when using !order.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_coleblooded,
		str_name="Cole Blooded",
        alias = ['cb', 'cole', 'slaw'],
		str_describe_self = "Ghosts fear your arteries due to **Cole Blooded**.",
		str_describe_other = "Ghosts fear their arteries due to **Cole Blooded**.",
		str_acquire = "Your begin to hear your pulse pounding in your ear, louder and louder, duller and duller. A choking sensation creeps up your neck as the flow of your blood begins to settle. You smell a faint hint of mayonnaise, and the redness begins to vanish from your skin. Is this cole slaw in your veins? Well, whatever it is, you feel purified, if a little queasy. You have developed the mutation **Cole Blooded**. Ghosts lose negaslime when haunting you, and you can bust them without cole slaw.",
        tier=2,
        str_transplant= "You ask to fill your veins with obscene amounts of cole slaw. \"Guess we'll have to get the big IV then.\"It really is a big IV. Attached to the needle is a full bodybag filled with probably-maybe-refrigerated cole slaw. Sitting for hours as your blood is replaced with cole slaw dripped through an IV is very tedious, too. It tingles whenever one of the cabbage bits gets stuck, so you can never quite fall asleep.\n\nYou have developed the mutation **Cole Blooded**. Ghosts lose negaslime when haunting you, and you can bust them without cole slaw.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_nervesofsteel,
		str_name="Nerves of Steel",
        alias = ['nos', 'nerves', 'nerve'],
		str_describe_self = "You are absolutely fearless due to **Nerves of Steel**.",
		str_describe_other = "They are absolutely fearless due to **Nerves of Steel**.",
		str_acquire = "You feel a sudden coldness sinking into the back of your head. Parts of your brain rapidly shut down, but you have no idea which ones are going because you can no longer access them. Without thinking, you run a knife down your hand, and although it's painful, you're completely detatched from the sensation. A gun to your head? No fear. If you die, you die. You have developed the mutation **Nerves of Steel**. As a gangster, you can cap ally surrounded districts. As a juvie, you can play russian roulette and commit suicide.",
        tier=6,
        str_transplant= "Dr. Dusttrap decides to take what she calls \"a traditional approach\". She takes out a syringe full of neurotoxin and pokes it right into your noggin. She tells you she's going to disable the part of your brain that processes fear, but the fact she's constantly referencing her brain anatomy chart is concerning. She manages to make you fearless, but sadly at the expense of a few precious childhood memories.\n\nYou have developed the mutation **Nerves of Steel**. As a gangster, you can cap ally surrounded districts. As a juvie, you can play russian roulette and commit suicide.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_packrat,
		str_name="Packrat",
        alias = ['pack', 'rat', 'pr'],
		str_describe_self = "Your constant hoarding has sabotaged your whole life due to **Packrat**.",
		str_describe_other = "Their constant hoarding has sabotaged their whole life due to **Packrat**.",
		str_acquire = "Your posture suddenly begins to contort, and you hunch forward. A hairless tail worms its way out of your backend and onto the floor. Paranoia washes over you, and you dart your eyes across your surroundings, looking for any sign of thieves of Freemasons. You remember the milk carton you threw away in the food court the other day and can't forgive yourself. That was the key to everything. You have developed the mutation **Packrat**. You can store twice as much in your apartment.",
        tier=1,
        str_transplant= "Dr. Dusttrap gives you a session of what she calls \"reverse therapy\". She pries into your life story, untangling every shred of vice you posess until you're unable to handle reality anymore. To cope, you now have a terrible hoarding issue.\n\nYou have developed the mutation **Packrat**. You can store twice as much in your apartment.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_landlocked,
		str_name="Landlocked",
        alias = ['ll', 'land', 'lock'],
		str_describe_self = "You feel trapped in a loop due to **Landlocked**.",
		str_describe_other = "They feel trapped in a loop due to due to **Landlocked**.",
		str_acquire = "You start to feel lightheaded, and your vision blurs. When you're lucid again, you notice that the sky is filled with amorphous neon patches. They look like dimensional rifts, don't they? Whatever the case, it seems like you're able to see them now. Wonder what happens if you charge right in? You have developed the mutation **Landlocked**. Use !loop at a street bordering the outskirts to warp to the opposite side.",
        tier=8,
        str_transplant= "Dusttrap somehow manages to pull out a Slimecorp teleportation core from her little box of tricks. Christ, it's the size of a dinner plate... She plugs it into her computer and does a bit of finagling with the GPS, when replaces your appendix with it. What a deal, you got an appendix removal out of the surgery!\n\nYou have developed the mutation **Landlocked**. Use !loop at a street bordering the outskirts to warp to the opposite side.",
    ),
	EwMutationFlavor(
		id_mutation = mutation_id_lethalfingernails,
		str_name="Lethal Fingernails",
        alias = ['lf', 'fingernails', 'lethal', 'nails'],
		str_describe_self = "Your nails cut flesh like butter due to **Lethal Fingernails**.",
		str_describe_other = "Their nails cut flesh like butter due to **Lethal Fingernails**.",
		str_acquire = "You feel an uncontrollable burning in your fingertips as blood begins to rush to them. In short bursts, your fingernails begin to pop out of your cuticle, hardening to diamond. It hurts like hell. First to an inch, then to five, then to nine. You have developed the mutation **Lethal Fingernails**. As a gangster, unarmed combat deals as much damage as a level 6 revolver with 0% miss chance.",
        tier=5,
        str_transplant= "You end up bringing in several katanas from the dojo for this one. Dusttrap tells you to bring your own metal for this procedure. You're brought into the operating room, where all your fingernails are removed. In their place, you're given sword nails, individually forged to fit your own tiny child fingers. They turned out way heavier than expected, you probably should've gotten some knives instead.\n\nYou have developed the mutation **Lethal Fingernails**. As a gangster, unarmed combat deals as much damage as a level 6 revolver with 0% miss chance.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_napalmsnot,
		str_name="Napalm Snot",
        alias = ['ns', 'napalmsnot', 'napalm'],
		str_describe_self = "You can spew firebomb loogies due to **Napalm Snot**.",
		str_describe_other = "They can spew firebomb loogies due to **Napalm Snot**.",
		str_acquire = "Breathing gets harder as steam starts to leak out your mouth and nose. Little by little, you can also feel a suffocating glob of phlegm building in your throat. At first it's unbearably searing, but you quickly adapt, like getting used to a hot shower. You try to cough it out to catch your breath, and the dark red loogie sets the tissue you're using on fire. You quickly realize that manners no longer apply. You have developed the mutation **Napalm Snot**. Deal burn damage when attacking with any weapon. Gain immunity to burn damage.",
        tier=8,
        str_transplant= "Dr. Dusttrap drags out her organ cooler and pulls out a Blue Eyes Slime Dragon fire bladder. Oxygenation is a bitch, so she shrinkwraps it and adds a protective plastic covering for good measure. One external implant to the back later, and you're the proud new owner of a firebreath organ. It's really uncomfortable to sit in chairs now that you have a big tank on your back that makes you burp fire when squeezed, but those are the consequences of bloodlust.\n\nYou have developed the mutation **Napalm Snot**. Deal burn damage when attacking with any weapon. Gain immunity to burn damage.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_ambidextrous,
		str_name="Ambidextrous",
        alias = ['ab', 'ambi'],
		str_describe_self = "Your left and right arms can multitask like hell due to **Ambidextrous**.",
		str_describe_other = "Their left and right arms can multitask like hell due to **Ambidextrous**.",
		str_acquire = "Your left arm falls asleep. It just came out of nowhere, so you just shrug with your good arm and keep going. A few minutes later, though, that's when your arm fucking WAKES UP. An urge to multitask burns inside you; your right hand starts reloading your weapon and your left begins to write a heartfelt letter to your mother. You don't even like your mother! You have developed the mutation **Ambidextrous**. When unarmed or wielding a tool, attacking will default to any sidearmed weapons.",
        tier=6,
        str_transplant= "Dr. Dusttrap may have misconstrued what you meant by \"having two dominant hands\". She decides the answer is to slice off your non-dominant arm and reattach one from a dead lefty in its place. Where does she find all these dead bodies?\n\nYou have developed the mutation **Ambidextrous**. When unarmed or wielding a tool, attacking will default to any sidearmed weapons.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_dyslexia,
		str_name="Dyslexia",
        alias = ['dl', 'lex'],
		str_describe_self = "Long words make your head hurt due to **Dyslexia**.",
		str_describe_other = "Long words make their head hurt due to **Dyslexia**.",
		str_acquire = "Something blows into your eye, and you rush to wipe it out. All of a sudden, the txet suorrnduing yuo, bllbroads and tmieclkocs negib to ilft off eth aepg. Snpotaoenus lliiterayc is a pertty iryifterng epxeriecne. You have developed the mutation **Dyslexia**. Across the board, captcha length is reduced by 3.",
        tier=6,
        str_transplant= "\"Hey pipsquick, are you sure you're in the right spot? I think you want to be in the Dojo for this.\" You assure her that you've come to the right place. You realize what she means when she takes out a club and knocks you over the head several times. You suppose that's one way to damage a brain. You can't think, let alone read.\n\nYou have developed the mutation **Dyslexia**. Across the board, captcha length is reduced by 3.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_bottomlessappetite,
		str_name="Bottomless Appetite",
        alias = ['ba', 'bottomless'],
		str_describe_self = "You could devour a horse, its carriage, and the frumpy nobles inside it due to **Bottomless Appetite**.",
		str_describe_other = "They could devour a horse, its carriage, and the frumpy nobles inside it due to **Bottomless Appetite**.",
		str_acquire = "You suddenly notice an eternal hunger, something so ridiculous it's completely uncontrollable. You try to focus on a nearby rock just to keep yourself still. Do...not...eat... Uh oh. The rock disappeared. Shit, now your spray can's gone, and you can feel it bulging in your gullet. This is going to be rough... You have developed the mutation **Bottomless Appetite**. Max hunger is doubled.",
        tier=7,
        str_transplant= "You get a full physical, complete with BMI and mammogram. Based on your approximate proportions, you are given 1.5 tapeworms to help regulate digestion. By \"regulate\" I mean annex. You're never feeling full ever again.\n\nYou have developed the mutation **Bottomless Appetite**. Max hunger is doubled.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_airlock,
		str_name="Air Lock",
        alias = ['al', 'air'],
		str_describe_self = "The weather is your bitch due to **Airlock**.",
		str_describe_other = "The weather is their bitch due to **Airlock**.",
		str_acquire = "Without thinking you take a deep breath. The air is so clean! You feel like this is your first taste of oxygen in years. A droplet falls on you from above, but it just runs off you, rolling down your face with a refreshing coolness. For once, the quantum wind has shown mercy. You have developed the mutation **Air Lock**. Gain the effects of White Nationalist and Light as a Feather. These effects do not stack with those mutations.",
        tier=4,
        str_transplant= "Dr. Dusttrap straps a small, high-grade air purifier around your neck, and runs a cord through your nose and into your stomach. The cords take somme getting used to, but this procedure was shockingly painless.\n\nYou have developed the mutation **Air Lock**. Gain the effects of White Nationalist and Light as a Feather. These effects do not stack with those mutations.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_unnaturalcharisma,
		str_name = "Unnatural Charisma",
        alias = ['uc', 'charisma'],
		str_describe_self = "Your unbridled charm can manipulate the unwashed masses due to **Unnatural Charisma**.",
		str_describe_other = "Their unbridled charm can manipulate the unwashed masses due to **Unnatural Charisma**.",
		str_acquire = "You hear rubbery squeaking sounds stirring throughout your body. You hair starts to condense and slick back, and the grime and sugar start to evaporate from your teeth. You attempt to gasp in shock, but it comes out a seductive purr. You don't just make women swoon, you have no choice but to do so. You have developed the mutation **Unnatural Charisma**. 20% capping increase and +500 freshness.",
        tier=4,
        str_transplant= "You notice the \"Make Me Pretty, I'm Begging You\" option on the menu and decide to go for broke. You are filled with experimental pheromones, and your undergo intense botoxing and head rearrangement. Coming out of the procedure, your face is completely unrecognizable, but you nonetheless have an urge to literally go fuck yourself. Just to top things off, the doctor uses your jawline to cut a pane of glass clean in half.\n\nYou have developed the mutation **Unnatural Charisma**. 20% capping increase and +500 freshness.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_ditchslap,
		str_name="Ditch Slap",
        alias = ['ds', 'slap', 'ditch'],
		str_describe_self = "You can knock someone into next precinct due to **Ditch Slap**.",
		str_describe_other = "They can knock someone into next precinct due to **Ditch Slap**.",
		str_acquire = "A fly grazes past your left eye. God, how annoying. You absentmindedly try to wave it away. The moment you do, you feel a surge of power in your backhand, and hit the fucker so hard it vaporizes on touch. The massive shockwave blows your hair back and scares away a distant stray cat. Jesus, it's like you're throwing Kamehameha waves or some shit. You have developed the mutation **Ditch Slap**. !slap <district> @player to knock allies into a nearby district or subzone, with a few exceptions.",
        tier=6,
        str_transplant= "Dr. Dusttrap takes out a hydraulic brace she says is designed for old-school freight trains and starts fitting it snugly into your left arm. \"You know, one time I forgot to ask if someone was left handed before doing this. They killed themselves trying to brush their teeth. Heheh, can you believe it?\" With those words, she stitches up the incision, work done. You don't think she asked your dominant hand...\n\nYou have developed the mutation **Ditch Slap**. !slap <district> @player to knock allies into a nearby district or subzone, with a few exceptions.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_oneeyeopen,
		str_name="One Eye Open",
        alias = ['oeo', 'oneeye', '1eo'],
		str_describe_self = "Your third eye's in the sky due to **One Eye Open**.",
		str_describe_other = "Their third eye's in the sky due to **One Eye Open**.",
		str_acquire = "A splitting headache emerges, and you begin to feel a hollow bubble forming next to your frontal lobe. The bubble becomes liquid and starts churning, forming noticeable wrinkles in your forehead as it solidifies. All of a sudden, something effortlessly slips out of it like the skin there was a pair of drawn curtains. It appears to be a disembodied third eye. And all of a sudden, your mind is clear. You can see more than ever before. You have developed the mutation **One Eye Open**. Use !track @user to receive a DM when they enter a danger zone.",
        tier=8,
        str_transplant= "\"Settle down, shrimp, this one will require therapy.\" You follow her into the surgery room, which you suppose doubles as the therapy room, and she tells you to lie down. \"So first, we need to talk about Lemuria...\" By the end of the conversation, you were more enlightened than you ever thought possible. Your feeble mind came in wanting a third eye, and came out with that and so much more.\n\nYou have developed the mutation **One Eye Open**. Use !track @user to receive a DM when they enter a danger zone.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_handyman,
		str_name="Handy Man",
        alias = ['hm', 'handy'],
		str_describe_self = "You've grown many graspers with minds of their own due to **Handy Man**.",
		str_describe_other = "They've grown many graspers with minds of their own due to **Handy Man**.",
		str_acquire = "A mysterious fellow taps you on the shoulder from behind. Huh? Nothing there. Oh well, probably just some staydead trying to prank you. All of a sudden, a hand spontaneously extends from your chest and hands you a rock off the ground. It's a good, round one too, perfect for window breakng. Very resourceful... You think you and your arm friend here are looking at the start of a beautiful friendship. You have developed the mutation **Handy Man**. Killing gangsters with a tool awards double the kingpin slime.",
        tier=4,
        str_transplant= "Dr. Dusttrap takes one of the severed arms from her pile of robot corpses and plugs it into her computer. She spends a lot of time coding the script to allow it to assist you, and once finished, links it up to a baseplate she is able to sew into your belly button. Then comes testing. Turns out 80 year old medical doctors aren't very good coders, so you get slapped around while Dusttrap finds the right calibration. Ah, there we go.\n\nYou have developed the mutation **Handy Man**. Killing gangsters with a tool awards double the kingpin slime.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_greenfingers,
		str_name="Green Fingers",
        alias = ['gf', 'greenthumb', 'green'],
		str_describe_self = "You're one with the gardens due to **Green Fingers**.",
		str_describe_other = "They're one with the gardens due to **Green Fingers**.",
		str_acquire = "You stretch yourself out and raise your hands to the sky. Vitality suddenly courses through your body! Your hands just photosynthesized! Now that you look at them, they've turned green, so that's suspicious. You look back to how much guac you consumed in your time at Taco Bell. All those plants, your bretheren, slaughtered... You make a vow that the plants you sow from now on will have genuine and fulfilling lives. Whatever that means. You have developed the mutation **Green Fingers**. 1.2x farming yields, and you can harvest in 60 minutes instead of 90.",
        tier=8,
        str_transplant= "Dr. Dusttrap walks into the greenhouse she keeps in the back and brings out two carnivorous looking plants, and fertilizes them right in front of you. She then mixes the pollen with concentrated fertilizer and injects them into the skin of your knuckles, shallow enough not to enter the bloodstream. Your skin is then bathed in intense light for 3 hours until the tattoo like formula turns from teal to a deep forest green, and a couple sprouts emerge. You have witnessed the miracle of childbirth, there is no turning back.\n\nYou have developed the mutation **Green Fingers**. 1.2x farming yields, and you can harvest in 60 minutes instead of 90.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_rigormortis,
		str_name="Rigor Mortis",
        alias = ['rm', 'rigor', 'rig'],
		str_describe_self = "You really can take it with you due to  **Rigor Mortis**.",
		str_describe_other = "They really can take it with them due to **Rigor Mortis**.",
		str_acquire = "A feeling of nausea permeates you entire body, even in places where you wouldn't expect to feel it. You stagger at the sudden sensation and you feel your feet begin to phase into your shoes. Just a little bit of pressure is all it takes to merge an object into yourself.  You have developed the mutation **Rigor Mortis**. !preserve an item and it will stay in your inventory after you die. You have to die with the mutation and only 5 items can be preserved.",
        tier=3,
        str_transplant= "You are led to a chemical shower and handed a brick. Dusttrap says she won't let you out until you can merge yourself with the thing. Whatever the hell you're being drenched with, it seems to leak through your pores and into your body, like you were made of coffee filters. After a few minutes you start to feel rubbery and squishy. Sure enough, the brick is buried in your shoulder and you don't feel a thing.\n\nYou have developed the mutation **Rigor Mortis**. !preserve an item and it will stay in your inventory after you die. You have to die with the mutation and only 5 items can be preserved.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_longarms,
		str_name="Long Arms",
        alias = ['la', 'long', 'longarms'],
		str_describe_self = "Your reach extends to the skies above due to **Long Arms**.",
		str_describe_other = "Their reach extends to the skies above due to **Long Arms**.",
		str_acquire = "The insides of your arms start to feel cramped. You feel the hair on a second skin brush up against the interior of your arm, bunching up. You try to relax your muscles, but a little stretch just causes you to rocket your right arm into the air. Hm. This could be useful, as long as you can get used to having to gather up the limp extended limb afterwards. You have developed the mutation **Long Arms**. Use !longdrop <location> <item> to drop an item to an adjacent area.",
        tier=2,
        str_transplant= "Dusttrap makes several incisions into your arms and placed a cyndrilical plate that acts as a filter between your veins. \"OK, all done. If you want to extend your arm, flip this switch. This'll convert your blood to 100% stem cells and expand nice n' fast. Whenever you're done, cut your long arm off and press the GROW HAND button over here, y'see? Simple as pie on a windowsill.\"\n\nYou have developed the mutation **Long Arms**. Use !longdrop <location> <item> to drop an item to an adjacent area.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_lightminer,
		str_name="Light Miner",
        alias = ['lm', 'miner'],
		str_describe_self = "You've adapted to mining in any conditions due to **Light Miner**.",
		str_describe_other = "They've adapted to mining in any conditions due to **Light Miner**.",
		str_acquire = "Several adaptations bombard your body all at once. You feel a aching friction in your eyes, and your vision begins to hyperfocus on small objects on the street. You start to notice you're able to see in the dark, even the cracks in the sidewalk or the slime in a nearby burning trash can. Meanwhile, your arms and legs become thinner and lankier and you develop a fading sense of allegiance to your gangs important traditions. Killers mine at night? Rowdys don't? Why? You have developed the mutation **Light Miner**. You can mine at any time, and mineshaft collapses do not affect you.",
        tier=4,
        str_transplant= "Dr. Dusttrap gets out the needles. \"Sucks to be you, but your measly surgery fee could only afford me 80s era steroids. Basically, horse tranquilizers, these. There are some wigs in the back in case your hair goes though, so take one if you need it.\" Of course, being the idiot you were, you didn't think she would go for an eye injection. She went for the eye injection. The good news is you can see better than ever. Damn, Dusttrap really should clean this place.\n\nYou have developed the mutation **Light Miner**. You can mine at any time, and mineshaft collapses do not affect you.",
    ),
EwMutationFlavor(
		id_mutation = mutation_id_amnesia,
		str_name="Amnesia",
        alias = ['amn'],
		str_describe_self = "You and everyone else have forgotten your identity due to **Amnesia**.",
		str_describe_other = "Everyone has forgotten their identity due to **Amnesia**.",
		str_acquire = "You are a delinquent JUVENILE, recently busted for attempting a scandalous act of vandalism and distribution of highly coveted SLIME. Luckily for you, the juvenile detention center you’ve been assigned to is notoriously corrupt and it’s an open secret how easy escape is. All you have to do for freedom and protection is- Wait a moment, this isn't quite right. You were taken to a jail just now, weren't you? You have developed the mutation **Amnesia**. On a kill, 60 seconds pass before it shows on the kill feed. Your identity will be concealed in ENDLESS WAR's messages, and you can delete your commands without coutermessages.",
        tier=3,
        str_transplant= "You are led to a cot in the back room and given an experimental dose of adrenaline and DMT. Once injected, you spend 54 years trapped on a 20 acre school playground, hunting and cannibalizing wayward 2nd graders to survive. You develop strong bonds and eventually marry into the local tribe that does the same as you. You are at your daughter's wedding near the old rock climbing wall when you wake up with a start. Where's Nancy and Luna? Why am I a teenager? \n\nYou have developed the mutation **Amnesia**. On a kill, 60 seconds pass before it shows on the kill feed. Your identity will be concealed in ENDLESS WAR's messages, and you can delete your commands without coutermessages.",
    ),
	]

mutations_map = {}

mutation_ids = set()

for mutation in mutations:
	mutations_map[mutation.id_mutation] = mutation
	mutation_ids.add(mutation.id_mutation)

quadrant_sloshed = "flushed"
quadrant_roseate = "pale"
quadrant_violacious = "caliginous"
quadrant_policitous = "ashen"

quadrant_ids = [
	quadrant_sloshed,
	quadrant_roseate,
	quadrant_violacious,
	quadrant_policitous
	]

quadrants_map = {}

quadrants = [
	EwQuadrantFlavor(
		id_quadrant = quadrant_sloshed,

		aliases = ["maw", "maws", "soulvent", "soulution", "pinked", "pink", "hotpink", "brightpink", 
		"flushed", "heart", "hearts", "matesprit", "matespritship"], # borrowing these from the original quadrants so people dont get mad/confused by using the "wrong" name 

		resp_add_onesided = "You have developed sloshed feelings for {}.",

		resp_add_relationship = "You have entered into a soulution with {}.",

		resp_view_onesided = "{} has a one-sided pink crush on {}.",

		resp_view_onesided_self = "You have a one-sided pink crush on {}.",

		resp_view_relationship = "{} is in a soulution with {}. " + emote_maws,

		resp_view_relationship_self = "You are in a soulution with {}. " + emote_maws
		),

	EwQuadrantFlavor(
		id_quadrant = quadrant_roseate,

		aliases = ["hat", "hats", "bedenizen", "bedenaissance", "denizen", "palepink", "pastelpink", 
		"pale", "diamond", "diamonds", "moirail", "moiraillegiance"], # borrowing these from the original quadrants so people dont get mad/confused by using the "wrong" name 

		resp_add_onesided = "You have developed roseate feelings for {}.",

		resp_add_relationship = "You have entered into a bedenaissance with {}.",

		resp_view_onesided = "{} has a one-sided roseate crush on {}.",

		resp_view_onesided_self = "You have a one-sided roseate crush on {}.",

		resp_view_relationship = "{} is in a bedenaissance with {}. " + emote_hats,

		resp_view_relationship_self = "You are in a bedenaissance with {}. " + emote_hats
		),

	EwQuadrantFlavor(
		id_quadrant = quadrant_violacious,

		aliases = ["slug", "slugs", "amaranthagonist", "amaranthagony", "antagonist", "agony", "purple", "violent", "violet", "hotpurple", 
		"caliginous", "spade", "spades", "kismesis", "kismesissitude"], # borrowing these from the original quadrants so people dont get mad/confused by using the "wrong" name 

		resp_add_onesided = "You have developed violacious feelings for {}.",

		resp_add_relationship = "You have entered into a amaranthagony with {}.",

		resp_view_onesided = "{} has a one-sided violet crush on {}.",

		resp_view_onesided_self = "You have a one-sided violet crush on {}.",

		resp_view_relationship = "{} is in a amaranthagony with {}. " + emote_slugs,

		resp_view_relationship_self = "You are in a amaranthagony with {}. " + emote_slugs
		),

	EwQuadrantFlavor(
		id_quadrant = quadrant_policitous,

		aliases = ["shield", "shields", "arbitraitor", "arbitreason", "police", "traitor", "treason", "lightpurple", "pastelpurple", 
		"ashen", "club", "clubs", "auspistice", "auspisticism"], # borrowing these from the original quadrants so people dont get mad/confused by using the "wrong" name 

		resp_add_onesided = "You have developed policitous feelings for {}.",

		resp_add_relationship = "You have entered into an arbitreason with {}.",

		resp_view_onesided = "{} has a one-sided policitous crush on {}.",

		resp_view_onesided_self = "You have a one-sided policitous crush on {}.",

		resp_view_relationship = "{} is in an arbitreason with {}. " + emote_shields,

		resp_view_relationship_self = "You are in an arbitreason with {}. " + emote_shields
		)

	]

for quadrant in quadrants:
	quadrants_map[quadrant.id_quadrant] = quadrant
	for alias in quadrant.aliases:
		quadrants_map[alias] = quadrant

quadrants_comments_onesided = [
		"Adorable~",
		"GAY!",
		"Disgusting.",
		"How embarrassing!",
		"Epic.",
		"Have you no shame...?",
		"As if you'd ever have a shot with them."
	]

quadrants_comments_relationship = [
		"Adorable~",
		"GAY!",
		"Disgusting.",
		"How embarrassing!",
		"Epic.",
		"Have you no shame...?",
		"Lke that's gonna last."
	]

# list of stock ids
stocks = [
	stock_kfc,
	stock_pizzahut,
	stock_tacobell,
]

# Stock names
stock_names = {
	stock_kfc : "Kentucky Fried Chicken",
	stock_pizzahut : "Pizza Hut",
	stock_tacobell : "Taco Bell",
}

#  Stock emotes
stock_emotes = {
	stock_kfc : emote_kfc,
	stock_pizzahut : emote_pizzahut,
	stock_tacobell : emote_tacobell
}
# A map of vendor names to their items.
vendor_inv = {}

# Populate item map, including all aliases.
for item in item_list:
	item_map[item.id_item] = item
	item_names.append(item.id_item)

	# Add item to its vendors' lists.
	for vendor in item.vendors:
		vendor_list = vendor_inv.get(vendor)

		if vendor_list == None:
			vendor_list = []
			vendor_inv[vendor] = vendor_list

		vendor_list.append(item.id_item)

	for alias in item.alias:
		item_map[alias] = item

# Populate food map, including all aliases.
for food in food_list:
	food_map[food.id_food] = food
	food_names.append(food.id_food)

	# Add food to its vendors' lists.
	for vendor in food.vendors:
		vendor_list = vendor_inv.get(vendor)

		if vendor_list == None:
			vendor_list = []
			vendor_inv[vendor] = vendor_list

		vendor_list.append(food.id_food)

	for alias in food.alias:
		food_map[alias] = food

# Populate fish map, including all aliases.
for fish in fish_list:
	fish_map[fish.id_fish] = fish
	fish_names.append(fish.id_fish)

	# Add fish to its vendors' lists.
	for vendor in fish.vendors:
		vendor_list = vendor_inv.get(vendor)

		if vendor_list == None:
			vendor_list = []
			vendor_inv[vendor] = vendor_list

		vendor_list.append(fish.id_fish)

	for alias in fish.alias:
		fish_map[alias] = fish

# Populate cosmetic map.
for cosmetic in cosmetic_items_list:
	cosmetic_map[cosmetic.id_cosmetic] = cosmetic
	cosmetic_names.append(cosmetic.id_cosmetic)

	# Add cosmetics to its vendors' lists.
	for vendor in cosmetic.vendors:
		vendor_list = vendor_inv.get(vendor)

		if vendor_list == None:
			vendor_list = []
			vendor_inv[vendor] = vendor_list

		vendor_list.append(cosmetic.id_cosmetic)


for furniture in furniture_list:
	furniture_map[furniture.id_furniture] = furniture
	furniture_names.append(furniture.id_furniture)
	if furniture.furn_set == "haunted":
		furniture_haunted.append(furniture.id_furniture)
	elif furniture.furn_set == "high class":
		furniture_highclass.append(furniture.id_furniture)
	elif furniture.furn_set == "lgbt":
		furniture_lgbt.append(furniture.id_furniture)
	elif furniture.furn_set == "leather":
		furniture_leather.append(furniture.id_furniture)
	elif furniture.furn_set == "church":
		furniture_church.append(furniture.id_furniture)
	elif furniture.furn_set == "pony":
		furniture_pony.append(furniture.id_furniture)
	elif furniture.furn_set == "blackvelvet":
		furniture_blackvelvet.append(furniture.id_furniture)
	elif furniture.furn_set == "seventies":
		furniture_seventies.append(furniture.id_furniture)
	elif furniture.furn_set == "slimecorp":
		furniture_slimecorp.append(furniture.id_furniture)
	elif furniture.furn_set == "shitty":
		furniture_shitty.append(furniture.id_furniture)
	elif furniture.furn_set == "instrument":
		furniture_instrument.append(furniture.id_furniture)
	elif furniture.furn_set == "specialhue":
		furniture_specialhue.append(furniture.id_furniture)


	for vendor in furniture.vendors:
		vendor_list = vendor_inv.get(vendor)
		if vendor_list == None:
			vendor_list = []
			vendor_inv[vendor] = vendor_list
		vendor_list.append(furniture.id_furniture)


# Populate weapon map, including all aliases.
for weapon in weapon_list:
	weapon_map[weapon.id_weapon] = weapon
	weapon_names.append(weapon.id_weapon)

	for vendor in weapon.vendors:
		vendor_list = vendor_inv.get(vendor)

		if vendor_list == None:
			vendor_list = []
			vendor_inv[vendor] = vendor_list

		vendor_list.append(weapon.id_weapon)

	for alias in weapon.alias:
		weapon_map[alias] = weapon


# List of items you can obtain via milling.
mill_results = []

# Gather all items that can be the result of milling.
for m in item_list:
	if m.acquisition == acquisition_milling:
		mill_results.append(m)
	else:
		pass

for m in food_list:
	if m.acquisition == acquisition_milling:
		mill_results.append(m)
	else:
		pass

for m in cosmetic_items_list:
	if m.acquisition == acquisition_milling:
		mill_results.append(m)
	else:
		pass

# List of items you can obtain via appraisal.
appraise_results = []

# Gather all items that can be the result of bartering.
for a in item_list:
	if a.acquisition == acquisition_bartering:
		appraise_results.append(a)
	else:
		pass

for a in food_list:
	if a.acquisition == acquisition_bartering:
		appraise_results.append(a)
	else:
		pass

for a in cosmetic_items_list:
	if a.acquisition == acquisition_bartering:
		appraise_results.append(a)
	else:
		pass

# List of items you can obtain via smelting.
smelt_results = []

# Gather all items that can be the result of smelting.
for s in item_list:
	if s.acquisition == acquisition_smelting:
		smelt_results.append(s)
	# So poudrins can be smelted with 2 royalty poudrins (this is obviously half-assed but i can't think of a better solution)
	elif s.id_item == item_id_slimepoudrin:
		smelt_results.append(s)
	else:
		pass

for s in food_list:
	if s.acquisition == acquisition_smelting:
		smelt_results.append(s)
	else:
		pass

for s in cosmetic_items_list:
	if s.acquisition == acquisition_smelting:
		smelt_results.append(s)
	else:
		pass

for s in weapon_list:
	if s.acquisition == acquisition_smelting:
		smelt_results.append(s)
	else:
		pass

for s in furniture_list:
	if s.acquisition == acquisition_smelting:
		smelt_results.append(s)
	else:
		pass

# List of items you can obtain via mining.
mine_results = []

# Gather all items that can be the result of mining.
for m in item_list:
	if m.acquisition == acquisition_mining:
		mine_results.append(m)
	else:
		pass

for m in food_list:
	if m.acquisition == acquisition_mining:
		mine_results.append(m)
	else:
		pass

for m in cosmetic_items_list:
	if m.acquisition == acquisition_mining:
		mine_results.append(m)
	else:
		pass

# Gather all the items that can be the result of trick-or-treating.
trickortreat_results = []

for t in food_list:
	if t.acquisition == acquisition_trickortreating:
		trickortreat_results.append(t)
	else:
		pass

slimexodia_parts = []

# Gather all parts of slimexodia.
for slimexodia in item_list:
	if slimexodia.context == 'slimexodia':
		slimexodia_parts.append(slimexodia)
	else:
		pass

prank_items_heinous = [] # common
prank_items_scandalous = [] # uncommon
prank_items_forbidden = [] # rare
swilldermuk_food = []

# Gather all prank items
for p in item_list:
	if p.context == context_prankitem and p.rarity == prank_rarity_heinous:
		prank_items_heinous.append(p)
	else:
		pass
for p in item_list:
	if p.context == context_prankitem and p.rarity == prank_rarity_scandalous:
		prank_items_scandalous.append(p)
	else:
		pass
for p in item_list:
	if p.context == context_prankitem and p.rarity == prank_rarity_forbidden:
		prank_items_forbidden.append(p)
	else:
		pass

# Pity-pies will also spawn across the map.
# for p in food_list:
# 	if p.acquisition == "swilldermuk":
# 		swilldermuk_food.append(p)
# 	else:
# 		pass

status_effect_type_miss = "miss"
status_effect_type_crit = "crit"
status_effect_type_damage = "dmg"

status_effect_target_self = "status_effect_target_self"
status_effect_target_other = "status_effect_target_other"

status_burning_id = "burning"
status_acid_id = "acid"
status_spored_id = "spored"
status_badtrip_id = "badtrip"
status_stoned_id = "stoned"
status_baked_id = "baked"
status_sludged_id = "sludged"
status_strangled_id = "strangled"
status_drunk_id = "drunk"
status_ghostbust_id = "ghostbust"
status_stunned_id = "stunned"
status_repelled_id = "repelled"
status_repelaftereffects_id = "repelaftereffects"
status_evasive_id = "evasive"
status_taunted_id = "taunted"
status_aiming_id = "aiming"
status_sapfatigue_id = "sapfatigue"
status_rerollfatigue_id = "rerollfatigue"
status_high_id = "high"
status_modelovaccine_id = "modelovaccine"
status_slapped_id = "slapped"
status_foodcoma_id = "foodcoma"
status_juviemode_id = "juviemode"

status_injury_head_id = "injury_head"
status_injury_torso_id = "injury_torso"
status_injury_arms_id = "injury_arms"
status_injury_legs_id = "injury_legs"


time_expire_burn = 12
time_expire_high = 30 * 60 # 30 minutes

time_expire_repel_base = 60 * 60 * 3 # 3 hours

status_effect_list = [
	EwStatusEffectDef(
		id_status = status_burning_id,
		time_expire = time_expire_burn,
		str_acquire = '{name_player}\'s body is engulfed in flames.',
		str_describe = 'They are burning.',
		str_describe_self = 'You are burning.'
	),
	EwStatusEffectDef(
		id_status = status_acid_id,
		time_expire = time_expire_burn,
		str_acquire = '{name_player}\'s body is drenched in acid.',
		str_describe = 'Their body is being melted down by acid.',
		str_describe_self = 'Your body is being melted down by acid.'
	),
	EwStatusEffectDef(
		id_status = status_spored_id,
		time_expire = time_expire_burn,
		str_acquire = '{name_player}\'s body is riddled with spores.',
		str_describe = 'Their body is being consumed by spores.',
		str_describe_self = 'Your body is being consumed by spores.'
	),
	EwStatusEffectDef(
		id_status = status_badtrip_id,
		time_expire = 5,
		str_acquire = '{name_player} begins to suffer from a bad trip.',
		str_describe = 'They are suffering from the effects of a bad trip.',
		str_describe_self = 'You are suffering from a bad trip.'
	),
	EwStatusEffectDef(
		id_status = status_stoned_id,
		time_expire = 30,
		str_acquire = '{name_player} starts to get stoned as fuck, brooooo.',
		str_describe = 'Their movements are sluggish and weak due to being stoned.',
		str_describe_self = 'Your movements are sluggish and weak due to being stoned.'
	),
	EwStatusEffectDef(
		id_status = status_baked_id,
		time_expire = 30,
		str_acquire = '{name_player} has become absolutely *baked!*',
		str_describe = 'They can barely move a muscle due to how fucking baked they are.',
		str_describe_self = 'You can barely move a muscle due to how fucking baked you are.'
	),
	EwStatusEffectDef(
		id_status = status_ghostbust_id,
		time_expire = 86400,
		str_describe_self = 'The coleslaw in your stomach allows you to bust ghosts.'
	),
	EwStatusEffectDef(
		id_status = status_strangled_id,
		time_expire = 5,
		str_describe = 'They are being strangled.'
	),
	EwStatusEffectDef(
		id_status = status_stunned_id,
		str_describe = 'They are stunned.'
	),
	EwStatusEffectDef(
		id_status = status_repelled_id,
		time_expire = time_expire_repel_base,
		str_acquire = 'You spray yourself with the FUCK ENERGY Body Spray.',
		str_describe = 'They smell like shit, much to the displeasure of slime beasts.',
		str_describe_self = 'You smell like shit, much to the displeasure of slime beasts.'
	),
	EwStatusEffectDef(
		id_status = status_repelaftereffects_id,
		time_expire = 2,
		str_acquire = 'You try and shake off the body spray, but its stench still lingers, if only for a brief moment.',
		str_describe = 'Their surroundings give off a slightly foul odor.',
		str_describe_self = 'Your surroundings give off a slightly foul odor.'
	),
	EwStatusEffectDef(
		id_status = status_high_id,
		time_expire = time_expire_high,
		str_describe = "They are as high as a kite.",
		str_describe_self = "You are as high as a kite."
	),
	EwStatusEffectDef(
		id_status = status_evasive_id,
		time_expire = 10,
		str_describe = "They have assumed an evasive stance.",
		str_describe_self = "You have assumed an evasive stance.",
		hit_chance_mod = -0.25
	),
	EwStatusEffectDef(
		id_status = status_taunted_id,
		time_expire = 10,
		str_describe = "They are fuming with rage.",
		str_describe_self = "You are fuming with rage.",
		hit_chance_mod_self = -0.25
	),
	EwStatusEffectDef(
		id_status = status_aiming_id,
		time_expire = 10,
		str_describe = "They are taking careful aim.",
		str_describe_self = "You are taking careful aim.",
		hit_chance_mod_self = 0.1,
		crit_mod_self = 0.2
	),
	EwStatusEffectDef(
		id_status = status_sapfatigue_id,
		time_expire = 60,
		str_describe = "They are suffering from sap fatigue.",
		str_describe_self = "You are suffering from sap fatigue.",
	),
	EwStatusEffectDef(
		id_status = status_rerollfatigue_id,
	),
	EwStatusEffectDef(
		id_status = status_injury_head_id,
		str_describe = "Their head looks {severity}",
		str_describe_self = "Your head looks {severity}",
		hit_chance_mod_self = -0.05,
		crit_mod_self = -0.1,
		hit_chance_mod = 0.01,
		crit_mod = 0.01,
	),
	EwStatusEffectDef(
		id_status = status_injury_torso_id,
		str_describe = "Their torso looks {severity}",
		str_describe_self = "Your torso looks {severity}",
	),
	EwStatusEffectDef(
		id_status = status_injury_arms_id,
		str_describe = "Their arms look {severity}",
		str_describe_self = "Your arms look {severity}",
		hit_chance_mod_self = -0.05,
		crit_mod_self = -0.1,
	),
	EwStatusEffectDef(
		id_status = status_injury_legs_id,
		str_describe = "Their legs look {severity}",
		str_describe_self = "Your legs look {severity}",
		hit_chance_mod = 0.06,
		crit_mod = 0.03,
	),
	EwStatusEffectDef(
		id_status = status_modelovaccine_id,
		time_expire = 86400,
		str_acquire = "You shoot the vaccine but… nothing happens. On the surface, anyway. The vaccine has successfully dissolved throughout your bloodstream, and you will now “cure” all those who come into contact with your pure, righteous slime. Meaning, it’s time to conduct some straight up genocide.",
		str_describe_self = "The modelovirus vaccine running through your veins allows you to cure shamblers!"
	),
    EwStatusEffectDef(
		id_status = status_slapped_id,
		time_expire = 300,
		str_acquire = "You're tuckered out. Better not get slapped for awhile.",
		str_describe_self = "You got ditch slapped recently and are really feeling it."
	),
    EwStatusEffectDef(
		id_status = status_foodcoma_id,
		time_expire = 300,
		str_acquire = "Calorie-induced rage consumes you! You could drink gasoline and get shot and not feel a damn thing!",
		str_describe_self = "You're in the middle of a raging food coma.",
        dmg_mod_self = -0.4
	),
    EwStatusEffectDef(
		id_status = status_juviemode_id,
		time_expire = 86400,
		str_acquire = "",
		str_describe_self = "You're carrying slime under the legal limit."
	),
]

status_effects_def_map = {}

for status in status_effect_list:
	status_effects_def_map[status.id_status] = status

# If a user already has one of these status effects, extend the timer for that status effect if applied once more.
stackable_status_effects = [
	status_burning_id,
	status_acid_id,
	status_spored_id,
	status_badtrip_id,
	status_stoned_id,
	status_baked_id,
	status_repelled_id,
	status_repelaftereffects_id,
]
# Status effects that cause users/enemies to take damage.
harmful_status_effects = [
	status_burning_id,
	status_acid_id,
	status_spored_id
]

injury_weights = {
	status_injury_head_id : 1,
	status_injury_torso_id : 5,
	status_injury_arms_id : 2,
	status_injury_legs_id : 2
}


# Places you might get !shot
hitzones = [
	EwHitzone(
		name = "head",
		aliases = [
			"neck",
			"jaw",
			"face",
			"nose",
		],
		id_injury = status_injury_head_id,
	),
	EwHitzone(
		name = "torso",
		aliases = [
			"upper back",
			"obliques",
			"solar plexus",
			"trapezius",
			"chest",
			"gut",
			"abdomen",
			"lower back",
		],
		id_injury = status_injury_torso_id,
	),
	EwHitzone(
		name = "leg",
		aliases = [
			"foot",
			"kneecap",
			"Achilles' tendon",
			"ankle",
			"thigh",
			"calf",
		],
		id_injury = status_injury_legs_id,
	),
	EwHitzone(
		name = "arm",
		aliases = [
			"hand",
			"wrist",
			"shoulder",
			"elbow",
		],
		id_injury = status_injury_arms_id,
	),
]

hitzone_list = []
hitzone_map = {}

for hz in hitzones:
	hitzone_list.append(hz.name)
	hitzone_map[hz.name] = hz

	for alias in hz.aliases:
		hitzone_list.append(alias)
		hitzone_map[alias] = hz

	hitzone_map[hz.id_injury] = hz

trauma_id_suicide = "suicide"
trauma_id_betrayal = "betrayal"
trauma_id_environment = "environment"

trauma_class_slimegain = "slimegain"
trauma_class_damage = "damage"

trauma_class_sapregeneration = "sapgen"
trauma_class_accuracy = "accuracy"
trauma_class_bleeding = "bleeding"
trauma_class_movespeed = "movespeed"
trauma_class_hunger = "hunger"

trauma_list = [
	EwTrauma(
		id_trauma = trauma_id_suicide,
		str_trauma_self = "You are suffering from a tragic case of cowardice.",
		str_trauma = "They are suffering from a tragic case of cowardice.",
		trauma_class = trauma_class_damage,
	),
	EwTrauma(
		id_trauma = trauma_id_betrayal,
		str_trauma_self = "You look anxious around your teammates, wary of betrayal.",
		str_trauma = "They look anxious around their teammates, wary of betrayal.",
		trauma_class = trauma_class_movespeed,
	),
	EwTrauma(
		id_trauma = trauma_id_environment,
		str_trauma_self = "Your death could have resulted any number of situations, mostly related to your own idiocy.",
		str_trauma = "Their death could have come from any number of situations, mostly related to their own idiocy.",
		trauma_class = trauma_class_slimegain,
	),
	EwTrauma( # 1
		id_trauma = weapon_id_revolver,
		str_trauma_self = "You have scarring on both temples, which occasionally bleeds.",
		str_trauma = "They have scarring on both temples, which occasionally bleeds.",
		trauma_class = trauma_class_accuracy,
	),
	EwTrauma( # 2
		id_trauma = weapon_id_dualpistols,
		str_trauma_self = "You have several stitches embroidered into your chest over your numerous bullet wounds.",
		str_trauma = "They have several stitches embroidered into their chest over their numerous bullet wounds.",
		trauma_class = trauma_class_bleeding,
	),
	EwTrauma( # 3
		id_trauma = weapon_id_shotgun,
		str_trauma_self = "You have a few large, gaping holes in your abdomen. Someone could stick their arm through the biggest one.",
		str_trauma = "They have a few large, gaping holes in your abdomen. Someone could stick their arm through the biggest one.",
		trauma_class = trauma_class_bleeding,
	),
	EwTrauma( # 4
		id_trauma = weapon_id_rifle,
		str_trauma_self = "Your torso is riddled with scarred-over bulletholes.",
		str_trauma = "Their torso is riddled with scarred-over bulletholes.",
		trauma_class = trauma_class_bleeding,
	),
	EwTrauma( # 5
		id_trauma = weapon_id_smg,
		str_trauma_self = "Your copious amount of bullet holes trigger onlookers’ Trypophobia.",
		str_trauma = "Their copious amount of bullet holes trigger onlookers’ Trypophobia.",
		trauma_class = trauma_class_bleeding,
	),
	EwTrauma( # 6
		id_trauma = weapon_id_minigun,
		str_trauma_self = "What little is left of your body has large holes punched through it, resembling a slice of swiss cheese.",
		str_trauma = "What little is left of their body has large holes punched through it, resembling a slice of swiss cheese.",
		trauma_class = trauma_class_bleeding,
	),
	EwTrauma( # 7
		id_trauma = weapon_id_bat,
		str_trauma_self = "Your head appears to be slightly concave on one side.",
		str_trauma = "Their head appears to be slightly concave on one side.",
		trauma_class = trauma_class_accuracy,
	),
	EwTrauma( # 8
		id_trauma = weapon_id_brassknuckles,
		str_trauma_self = "You've got two black eyes, missing teeth, and a profoundly crooked nose.",
		str_trauma = "They've got two black eyes, missing teeth, and a profoundly crooked nose.",
		trauma_class = trauma_class_accuracy,
	),
	EwTrauma( # 9
		id_trauma = weapon_id_katana,
		str_trauma_self = "A single clean scar runs across the entire length of your body.",
		str_trauma = "A single clean scar runs across the entire length of their body.",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma( # 10
		id_trauma = weapon_id_broadsword,
		str_trauma_self = "A large dent resembling that of a half-chopped down tree appears on the top of your head.",
		str_trauma = "A dent resembling that of a half-chopped down tree appears on the top of their head.",
		trauma_class = trauma_class_accuracy,
	),
	EwTrauma( # 11
		id_trauma = weapon_id_nunchucks,
		str_trauma_self = "You are covered in deep bruises. You hate martial arts of all kinds.",
		str_trauma = "They are covered in deep bruises. They hate martial arts of all kinds.",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma( # 12
		id_trauma = weapon_id_scythe,
		str_trauma_self = "You are wrapped tightly in bandages that hold your two halves together.",
		str_trauma = "They are wrapped tightly in bandages that hold their two halves together.",
		trauma_class = trauma_class_movespeed,
	),
	EwTrauma( # 13
		id_trauma = weapon_id_yoyo,
		str_trauma_self = "Simple yo-yo tricks caught even in your peripheral vision triggers intense PTSD flashbacks.",
		str_trauma = "Simple yo-yo tricks caught even in their peripheral vision triggers intense PTSD flashbacks.",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma( # 14
		id_trauma = weapon_id_knives,
		str_trauma_self = "You are covered in scarred-over lacerations and puncture wounds.",
		str_trauma = "They are covered in scarred-over lacerations and puncture wounds.",
		trauma_class = trauma_class_bleeding,
	),
	EwTrauma( # 15
		id_trauma = weapon_id_molotov,
		str_trauma_self = "You're wrapped in bandages. What skin is showing appears burn-scarred.",
		str_trauma = "They're wrapped in bandages. What skin is showing appears burn-scarred.",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma( # 16
		id_trauma = weapon_id_grenades,
		str_trauma_self = "Blast scars and burned skin are spread unevenly across your body.",
		str_trauma = "Blast scars and burned skin are spread unevenly across their body.",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma( # 17
		id_trauma = weapon_id_garrote,
		str_trauma_self = "There is noticeable bruising and scarring around your neck.",
		str_trauma = "There is noticeable bruising and scarring around their neck.",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma(  # 18
		id_trauma = weapon_id_pickaxe,
		str_trauma_self = "There is a deep, precise indent in the crown of your skull. How embarrassing!",
		str_trauma = "There is a deep, precise indent in the crown of their skull. How embarrassing!",
		trauma_class = trauma_class_accuracy,
	),
	EwTrauma(  # 19
		id_trauma = weapon_id_fishingrod,
		str_trauma_self = "There is a piercing on the side of your mouth. How embarrassing!",
		str_trauma = "There is a piercing on the side of their mouth. How embarrassing!",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma(  # 20
		id_trauma = weapon_id_bass,
		str_trauma_self = "There is a large concave dome in the side of your head.",
		str_trauma = "There is a large concave dome in the side of their head.",
		trauma_class = trauma_class_accuracy,
	),
	EwTrauma(  # 21
		id_trauma = weapon_id_umbrella,
		str_trauma_self = "You have a large hole in your chest.",
		str_trauma = "They have a large hole in their chest.",
		trauma_class = trauma_class_bleeding,
	),
	EwTrauma(  # 22
		id_trauma = weapon_id_bow,
		str_trauma_self = "There is a pixelated arrow in the side of your head.",
		str_trauma = "There is a pixelated arrow in the side of their head.",
		trauma_class = trauma_class_accuracy,
	),
	EwTrauma(  # 23
		id_trauma = weapon_id_dclaw,
		str_trauma_self = "Three smoldering claw marks are burned into your flesh, the flames `won't seem to extinguish.",
		str_trauma = "Three smoldering claw marks are burned into their flesh, the flames won't seem to extinguish.",
		trauma_class = trauma_class_sapregeneration,
	),
	EwTrauma(  # 24
		id_trauma = weapon_id_staff,
		str_trauma_self = "Parts of your skin look necrotic, and you look like you haven't slept in days.",
		str_trauma = "Parts of their skin look necrotic, and they look like they haven't slept in days.",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma(  # 25 
		id_trauma = weapon_id_hoe,
		str_trauma_self = "You have a perfectly straight scar right on your neck.",
		str_trauma = "They have a perfectly straight scar right on their neck.",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma(  # 26 
		id_trauma = weapon_id_pitchfork,
		str_trauma_self = "You have three evenly sized holes on your upper body.",
		str_trauma = "They have three evenly sized holes on their upper body.",
		trauma_class = trauma_class_bleeding,
	),
	EwTrauma(  # 27 
		id_trauma = weapon_id_shovel,
		str_trauma_self = "You have a cartoonishly large dent on your head.",
		str_trauma = "They have a cartoonishly large dent on their head.",
		trauma_class = trauma_class_sapregeneration,
	),
	EwTrauma(  # 28 
		id_trauma = weapon_id_slimeringcan,
		str_trauma_self = "Your throat is swollen.",
		str_trauma = "Their throat is swollen.",
		trauma_class = trauma_class_sapregeneration,
	),
	EwTrauma( # 1
		id_trauma = "fangs",
		str_trauma_self = "You have bite marks littered throughout your body.",
		str_trauma = "They have bite marks littered throughout their body.",
		trauma_class = trauma_class_bleeding,
	),
	EwTrauma( # 2
		id_trauma = "talons",
		str_trauma_self = "A large section of scars litter your abdomen.",
		str_trauma = "A large section of scars litter their abdomen.",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma( # 4
		id_trauma = "gunk shot",
		str_trauma_self = "Several locations on your body have decayed from the aftermath of horrific radiation.",
		str_trauma = "Several locations on their body have decayed from the aftermath of horrific radiation.",
		trauma_class = trauma_class_sapregeneration,
	),
	EwTrauma( # 5
		id_trauma = "tusks",
		str_trauma_self = "You have one large scarred-over hole on your upper body.",
		str_trauma = "They have one large scarred-over hole on their upper body.",
		trauma_class = trauma_class_bleeding,
	),
	EwTrauma( # 6
		id_trauma = "molotov breath",
		str_trauma_self = "You're wrapped in two layers of bandages. What skin is showing appears burn-scarred.",
		str_trauma = "They're wrapped in two layers of bandages. What skin is showing appears burn-scarred.",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma( # 7
		id_trauma = "arm cannon",
		str_trauma_self = "There's a deep bruising right in the middle of your forehead.",
		str_trauma = "There's a deep bruising right in the middle of their forehead.",
		trauma_class = trauma_class_accuracy,
	),
	EwTrauma( # 8
		id_trauma = "axe",
		str_trauma_self = "There's a hefty amount of bandages covering the top of your head",
		str_trauma = "There's a hefty amount of bandages covering the top of their head",
		trauma_class = trauma_class_accuracy,
	),
	EwTrauma( # 9
		id_trauma = "hooves",
		str_trauma_self = "Your chest is somewhat concave.",
		str_trauma = "Their chest is somewhat concave.",
		trauma_class = trauma_class_hunger,
	),
	EwTrauma( # 10
			id_trauma = weapon_id_fingernails,
			str_trauma_self = "Criscrossed slash marks cover your body.",
			str_trauma = "Criscrossed slash marks cover their body.",
			trauma_class = trauma_class_hunger,
		),
	EwTrauma( # 11
			id_trauma = weapon_id_spraycan,
			str_trauma_self = "Your breath smells awful, and you talk in a wheeze.",
			str_trauma = "Their breath smells awful, and they talk in a wheeze.",
			trauma_class = trauma_class_accuracy,
		),
	EwTrauma( # 12
			id_trauma = weapon_id_paintroller,
			str_trauma_self = "Mishhapen welts cover the top of your head.",
			str_trauma = "Misshhapen welts cover the top of their head.",
			trauma_class = trauma_class_bleeding,
		),
	EwTrauma( # 13
			id_trauma = weapon_id_paintgun,
			str_trauma_self = "Your stitched-up form looks barely held together.",
			str_trauma = "Their stitched-up form looks barely held together.",
			trauma_class = trauma_class_bleeding,
		),
	EwTrauma( # 14
			id_trauma = weapon_id_paintbrush,
			str_trauma_self = "Your eyes are bloodshot, and splinters stick out of your torso.",
			str_trauma = "Their eyes are bloodshot, and splinters stick out of their torso.",
			trauma_class = trauma_class_accuracy,
		),
	EwTrauma( # 14
			id_trauma = weapon_id_thinnerbomb,
			str_trauma_self = "Light scars run across your face, which is a disturbing blue discoloration.",
			str_trauma = "Light scars run across their face, which is a disturbing blue discoloration.",
			trauma_class = trauma_class_accuracy,
		),
	EwTrauma( # 14
			id_trauma = weapon_id_watercolors,
			str_trauma_self = "You are a dumb suicidal idiot and despise watercolors as a concept.",
			str_trauma = "They are a dumb suicidal idiot and despise watercolors as a concept.",
			trauma_class = trauma_class_accuracy,
		),
	EwTrauma( # 15
				id_trauma = weapon_id_roomba,
				str_trauma_self = "Your skin is stretched amd misshapen, flabby and tight in different spots.",
				str_trauma = "Their skin is stretched amd misshapen, flabby and tight in different spots.",
				trauma_class = trauma_class_accuracy,
			),
	EwTrauma(  # 16
		id_trauma=weapon_id_chainsaw,
		str_trauma_self="Your body is made almost exclusively out of scar tissue.",
		str_trauma="Their body is made almost exclusively out of scar tissue.",
		trauma_class=trauma_class_accuracy,
	),
	EwTrauma(  # 17
		id_trauma=weapon_id_laywaster,
		str_trauma_self="Your body is melting and mishhapen, like your skin was made of drenched paper mache.",
		str_trauma="Their body is melting and mishhapen, like their skin was made of drenched paper mache.",
		trauma_class=trauma_class_accuracy,
	),
	EwTrauma(  # 17
		id_trauma='amateur',
		str_trauma_self="You can still feel the circular scar inside your throat. Embarrassing...",
		str_trauma="They can still feel the circular scar inside their throat. Embarrassing...",
		trauma_class=trauma_class_accuracy,
	),
]


trauma_map = {}

for trauma in trauma_list:
	trauma_map[trauma.id_trauma] = trauma

# Shitty bait that always yields Plebefish while fishing.
plebe_bait = []

# Gather all shitty bait.
for bait in food_list:
	if bait.price == None or bait.price <= 1000:
		plebe_bait.append(bait.id_food)
	else:
		pass

# If a fish doesn't bite, send one of these.
generic_fishing_text = [
	"You patiently wait...",
	"This is so fucking boring...",
	"You grow impatient and kick the rotted wooden guard rails...",
	"AUUUUUGH JUST BITE THE FUCKING HOOK ALREADY...",
	"You begin to zone-out a bit...",
	"Shouldn't you be doing something productive?",
	"You sit patiently, eagerly awaiting a fish to bite. Thanks to your concentration, this descriptive contradiction does not occur to you.",
	"Maybe one day your wife will pardon you...",
	"You feel the oncoming downward spiral...",
	"You wonder if the Space Navy has been formed yet...",
	"You start to slip into an existential crisis...",
	"You hum some sea shanties...",
	"Fuck fish...",
	"Fish..."
]
normal_fishing_text = [
	"You watch your hook bob...",
	"You see a fish about to bite your hook, but you shout in elation, scaring it away...",
	"You make direct eye contact with a fish, only to quickly look away...",
	"♪ Fishing for Fishies! ♪",
	"♪ That Captain Albert Alexander! ♪",
	"Still better than Minesweeper...",
	"Man... Why were you excited for this shit?",
	"You begin to daydream about fish sex... Gross...",
	"You begin to daydream about fish sex... Hot...",
	"You get the urge to jump in and try to grab a fish, before remembering that you can't swim...",
	"You jitter as other seamen catch fish before you. Fuck fishing...",
	"You shake your head as a young seaman baits a perfectly good slice of pizza on his hook... What a cretin...",
	"Wouldn't it be funny if you just reached into the sea and grabbed one? Haha, yeah, that'd be funny...",
	"You see a bird carry off a Plebefish in the distance... Good riddance...",
	"You spot a stray bullet in the distance...",
	"You see a dead body float up to the surface of the Slime...",
	"You let out a deep sigh, scaring away a fish...",
] + generic_fishing_text
void_fishing_text = [
	"You get the urge to jump in and try to grab a fish, before the voice reminds you that you can't swim...",
	"Did the water just wink at you?",
	"That guy in the water looks so handsome... You should give him your number.",
	"Your mother motions you to join her in the water, it's nice and warm!",
	"HAHAHAHA OH WOW",
	"Hmmm?",
	"Man, the water looks fucking delicious, you should take a sip.",
	"Wait, why did you come here again?",
	"God, what a beautiful smile. So many of them, too.",
	"Go on, take a nap, the fish will wait for you.",
	"What is _that_?",
	"The girl across the pond has such a nice voice... Please keep singing...",
] + generic_fishing_text

generic_help_response = "Check out the guide for help: https://ew.krakissi.net/guide/\nThe guide won't cover everything though, and may even be a bit outdated in some places, so you can also visit N.L.A.C.U. (!goto uni) or Neo Milwaukee State (!goto nms) to get more in-depth descriptions about how various game mechanics work by using the !help command there. Portable game guides can also be bought there for 10,000 slime."

# Dict of all help responses linked to their associated topics
help_responses = {
	# Introductions, part 1
	"gangs":"**Gang Violence** is the center focus of **Rowdy Fuckers Cop Killers' ENDLESS WAR**. Enlisting in a gang allows you to attack other gang members, juveniles, ghosts, and slime beasts with the **'!kill'** command. To enlist in a gang, use **'!enlist'**. However, a member of that gang must use **'!vouch'** for you beforehand. Enlisting will permanently affiliate you with that gang, unless you are !pardon'd by the **ROWDY FUCKER** (Munchy), or the **COP KILLER** (Ben Saint). You may use **'!renounce'** to return to the life of a juvenile, but you will lose half of your current slime, and you will still be affiliated with that gang, thus disallowing you from entering the enemy's gang base. Additionally, a Kingpin, should they feel the need to, can inflict the '!banned' status upon you, preventing you from enlisting in their gang.",
	"food":"Food lowers your hunger by a set amount, and can be ordered from various **restaurants** within the city. Generally speaking, the more expensive food is, the more hunger it sates. You can **'!order [food name] togo'** to order it togo, otherwise you will eat it on the spot, and you can **'!use [food name]'** to use it once its in your inventory. You can only carry a certain amount of food depending on your level. Regular food items expire after 2 in-game days, or 12 hours in real life, while crops expire after 8 in-game days (48 hours), and food items gained from milling expire after a whole 2 weeks in real life. Three popular restauraunts close by various gang bases include **THE SPEAKEASY** (juveniles), **THE SMOKER'S COUGH** (rowdys), and **RED MOBSTER SEAFOOD** (killers), though there are other places to order food as well, such as the **Food Court**.",
	"capturing":"Capping is a battle for influence over the 33 districts of NLACakaNM, and one of your main goals as a gangster. Capped territories award your kingpin slime, and give your teammates benefits while visiting. Start by visiting Based Hardware and equipping one of the paint tools sold there. Once you have that, you can **!spray <captcha>** while in a capturable district's streets to gain influence for your gang. Spraying graffiti in districts will increase influence for you, or decrease it for the enemy if they have influence there. Think of dealing influence to a district like dealing damage to a Juvie's soft squishy body, with critical hits, misses, and backfires included. As you go, you can check your **!progress** to see how much influence you still need. It can be more or less depending on the territory class, running from rank C to S. \n\nA few more things to note:\n>**!progress** will tell you the minimum and limit for territory capture. However, you can capture above that limit, as high as you want. The catch is that anything captured over this limit will decay faster.\n>Decapping does 0.8x the influence of capping, even though the cost remains the same.\n>Don't attack enemy territory when it is surrounded by enemy territory/outskirts. Small little bitches like yourself are prone to fucking up severely under that much pressure.\n>The nightlife starts in the late night. Fewer cops are around to erase your handiwork, so if you cap then you will gain a 33% capping bonus.\n>You can't kill for shit with paint tools equipped. Luckily, you can **!sidearm** a weapon or tool and quickly switch between your two equip slots using **switch** or **!s**.",
	"transportation":"There are various methods of transportation within the city, the quickest and most efficient of them being **The Subway System**. Trains can be boarded with **'!board'** or **'!embark'**, and to board specific trains, you can add your destination to the command. For example, to board the red line to Cratersville, you would use '!board pinktocv'. **'!disembark'** can be used to exit a train. **The Ferry** (which moves between Vagrant's Corner and Wreckington) and **The Blimp** (which moves between Dreadford and Assault Flats Beach) can also be used as methods of transportation, though they take longer to arrive at their destinations than the trains do. Refer to the diagram below on understanding which districts and streets have subway stations in them.\nhttps://cdn.discordapp.com/attachments/431238867459375145/570392908780404746/t_system_final_stop_telling_me_its_wrong_magicks.png",
	"death": "Death is an integral mechanic to Endless War. Even the most experienced players will face the sewers every now and again. If you find yourself in such a situation, use **'!revive'** in the sewers channel, and you will return to the land of the living as a juvenile at the base of ENDLESS WAR. Dying will drop some of your unadorned cosmetics and food, and all of your unequiped weapons, but your currently adorned cosmetics and equiped weapon will remain in your inventory (Gangsters will lose half of their food/unadorned cosmetics, while Juveniles lose only a quarter). Alternatively, you can hold off on reviving and remain a **ghost**, which has its own gameplay mechanics associated with it. To learn more, use '!help ghosts' at one of the colleges or with a game guide, or see the wiki page here: https://rfck.miraheze.org/wiki/Ghosts",
	# Introductions, part 2
	"dojo":"**The Dojo** is where you acquire weapons to fight and kill other players with. To purchase a weapon, use **'!order [weapon]'**. There are many weapons you can choose from (you can view all of them with !menu), and they all perform differently from one another. Once you've purchased a weapon, you can use **'!equip [weapon]'** to equip it, provided that you're enlisted in a gang beforehand. You can also name your weapon by spending a poudrin on it with **'!annoint [name]'**. Furthermore, annointing will increase your mastery over that weapon, but it's much more efficient to do so through **sparring**. To learn more about the sparring system and weapon ranks, use '!help sparring'.",
	"subzones":"**Subzones** are areas locations within the districts of the city where gang violence off-limits, with the only exception being the subway stations, the trains, and the base of ENDLESS WAR. If you don't type anything in a sub-zone for 60 minutes, you'll get kicked out for loitering, so be sure to check up often if you don't wanna get booted out into the streets.",
	"scouting": "Scouting is a way for you to check how many **players** might be in a district that's close by. You can do just **'!scout'** to check the district you're already in, or **'!scout [district]'** to scout out that specific district. For example, if you were in Vagrant's Corner, you could use '!scout gld' to see how many players might be in Green Light District. Scouting will show both **friendly and enemy** gang members, as well as juveniles and even enemies. Scouting will list all players/enemies above your own level, as well as players/enemies below your level, but at a certain **cutoff point**. If you can't scout someone, it's safe to assume they have around **1/10th** the amount of slime that you do, or less. It should be noted that scouting currently only gives an estimate, sending off different messages depending on how many players are in that district.",
	"wanted":"If you find that you have a role with 'Wanted' in the name, be alarmed. This means that you are able to be attacked by gangsters! Always be on the look out and remember to check your corners.",
	"combat": "Once you have enlisted in a gang, you can engage in gang violence. To do so you will need a weapon, which you can find at the Dojo and a target. To attack an enemy, you have to **!equip** a weapon and **!kill [player]**. Attacking costs slime and sap. The default cost for attacking is ((your slime level)^4 / 60), and the default damage it does to your opponent is ((your slimelevel)^4 / 6). Every weapon has an attack cost mod and a damage mod that may change these default values. When you reduce a player's slime count below 0 with your attacks, they die. Most weapons will ask you to input a security code with every attack. This security code, also referred to as a captcha, is displayed after a previous !kill or when you !inspect your weapon. Heavy weapons increase crit chance by 5% and decrease miss chance by 10% against you, when you carry them.",
	# Ways to gain slime
	"mining": "Mining is the primary way to gain slime in **ENDLESS WAR**. When you type one **'!mine'** command, you raise your hunger by a little bit. The more slime you mine for, the higher your level gets. Mining will sometimes endow you with hardened crystals of slime called **slime poudrins**, which can be used for farming and annointing your weapon. **JUVENILES** can mine any time they like, but **ROWDYS** and **KILLERS** are restricted to mining during the day (8AM-6PM) and night (8PM-6AM), respectively. If you are enlisted, you can make use of the **pickaxe**, which increases the amount of slime you gain from mining. Currently mining is event-based, with events like simple slimboosts or guaranteed poudrins for a certain time. Similarly to clicker games your base action is **!mine**, however some mines can dynamically change how mining works. Basic instructions for these variations can be found in those mines.",
	"scavenging":"Scavenging allows you to collect slime that is **stored** in districts. When someone in a district gets hurt or dies, their slime **splatters** onto the ground, allowing you to use **'!scavenge'** and collect it, similarly to mining. Scavenging raises your hunger by 1% with every command entered. If you type **!scavenge** by itself, you will be given a captca to type. The more captchas you type correctly, the more slime you will gain. To check how much slime you can scavenge, use **'!look'** while in a district channel. You can also scavenge for items by doing '!scavenge [item name]'.",
	"farming":"**Farming** is an alternative way to gain slime, accessible only by **JUVENILES**. It is done by planting poudrins on a farm with the **'!sow'** command. You can only '!sow' one poudrin per farm. After about 12 in-game hours (3 hours in real life), you can use **'!reap'** to gain 200,000 slime, with a 1/30 chance to gain a poudrin. If you do gain a poudrin, you also have 1/3 chance to gain a second poudrin. If your poudrin plant is left alone for too long (around 2 in-game days, or 12 hours in real life), it will **die out**. In addition to slime, farming also provides you with various **crops** which can be used for **milling**, but you can also **'!crush'** them to gain cosmetic materials for smelting random cosmetics. Crops can be eaten by themselves, but it's much more useful if you use **'!mill'** on them while at a farm, granting you crop materials used for smelting **dyes**, as well as food items and cosmetics associated with that crop, all at the cost of 50,000 slime per '!mill'. Dyes can be used on slimeoids with **'!saturateslimeoid'**. Crops can also be sown themselves with '!sow [crop name]', and upon reaping you be rewarded with a bushel of that crop, as well as 100,000 slime. You can, however, increase the slime gained from sowing crops by using **'!checkfarm'**, and performing **'!irrigate'**, **'!fertilize'**, **'!pesticide'** or **'!weed'** if neccessary. Current farms within the city include **JUVIE'S ROW FARMS** (within Juvie's Row), **OOZE GARDENS FARMS** (close by Rowdy Roughhouse), and **ARSONBROOK FARMS** (close by Cop Killtown).",
	"fishing": "**Fishing** can be done by performing the **'!cast'** command at one of the six piers, including **Juvie's Row Pier**, **Crookline Pier**, **Jaywalker Plain Pier**, **Toxington Pier**, **Assault Flats Beach Pier**, **Slime's End Pier**, as well as **The Ferry**. To reel in a fish, use **'!reel'** when the game tells you that you have a bite. If you don't reel in quick enough, the fish will get away. If you are enlisted and have the **fishing rod** equiped, you will have increased chances of reeling in a fish. For more information about fishing, refer to this helpful guide (credits to Miller#2705).\n<https://www.youtube.com/watch?v=tHDeSukIqME>\nAs an addendum to that video, note that fish can be taken to the labs in Brawlden, where they can be made more valuble in bartering by increasing their size with **'!embiggen [fish]'**.",
	"hunting": "**Hunting** is another way to gain slime in ENDLESS WAR. To hunt, you can visit **The Outskirts**, which are layered areas located next to the edge of the map (Wreckington -> Wreckington Outskirts Edge, Wreckington Outskirts Edge -> Wreckington Outskirts, etc). In the outskirts, you will find enemies that you can !kill. Rather than doing '!kill @' like with players, with enemies you can either type their display name ('!kill Dinoslime'), their shorthand name ('!kill dino'), or their identifying letter ('!kill A'), which can be accessed with !look or !survey (WARNING: Raid bosses moving around the city do not have identifying letters. You must use the other targeting methods to attack them). To see how much slime an enemy has, you can do '!data [enemy name]', or just !data with any of the previous types of methods listed. Enemies will drop items and slime upon death, and some enemies are more powerful and threatening than others. In fact, there are enemies powerful enough to hold their own against the gangsters in the city, called **Raid Bosses**, and will enter into the city as a result, rather than just staying in the outskirts like regular enemies. **The Rowdy Roughhouse** and **Cop Killtown** will send out a response that mentions which district a raid boss has entered into. Enemies despawn after **3 hours in real life**.",
	# Additional gameplay mechanics, part 1
	"mutations": "**Mutations** are helpful bonuses you acquire when you level up. The more powerful your next mutation, the more level ups it takes to acquire. This is represented my the mutation's level. When you acquire a mutation, a short text response will indicate what it can do. To modify your mutations, you need to go to NLACakaNM Clinic of Slimoplasty in Crookline. When you get there, you can !chemo <mutation> to remove a mutation you acquired, or !chemo all to remove all possible mutations from your body. You can use !graft <mutation> to add a mutation to yourself. Keep in mind that you cannot use !chemo on a mutation if you got it through grafting, and you can only !graft a mutation if you have enough space in your mutations pool. You will likely need to !chemo a mutation out in order to !graft something else.",
	"mymutations":"You read some research notes about your current mutations...", # will print out a list of mutations with their specific mechanics
	"smelting": "Smelting is a way for you to craft certain items from certain ingredients. To smelt, you use **'!smelt [item name]'**, which will either smelt you the item, or tell which items you need to smelt the item. Popular items gained from smelting are **Cosmetics**, as well as the coveted **Pickaxe** and **Super Fishing Rod**. If you're stuck, you can look up the crafting recipes for any item with **!whatcanimake [itemname]**.",
	"sparring": "**Sparring** can be done between two players using **'!spar [player]'**. Sparring, provided that both players spar with the same weapon type and are not at full hunger, will increase both of your mastery **LEVEL**, which is a hidden value, by one. The publicly displayed value, mastery **RANK** (which is just your mastery level minus 4), is more important. It should be noted that the damage you deal with your weapon is increased even if you haven't reached rank 1 yet. However, once you do reach at least mastery rank 2 (Again, this would be level 6), when you next revive, you will now **permanently** be at level 6 for that weapon type until you annoint or spar again. Essentially, this means you will always start back at rank 2. Once you reach **rank 6**, you can no longer annoint your weapon rank any higher, and must instead kill other players/enemies (that are higher in both slime and level than you) to do so. Reaching rank 6 also stops you from increasing your own rank through sparring, unless you are sparring with someone who has a higher weapon rank than you. You can only spar up to someone else's mastery rank, minus 1 (example: Sparring with a rank 15 master of the katana would, at most, allow you to get to rank 14). Sparring has a one minute cooldown and raises your hunger by about 5%. Once you reach rank 8, you may also **'!marry'** your weapon, resulting in a matrimonial ceremony that increases your rank by two.",
	"ghosts": "Ghost gameplay revolves around the acquisition of antislime, through haunting and possession. Every use of **'!haunt'** away a small portion of slime from the haunted player, and grants it to the ghost as antislime. The amount of slime taken starts at 1/1000th and varies depending on a number of conditions, and you may also add a customized message by doing '!haunt [@player] [message]'. It can be done face-to-face like with !kill, or done remotely with decreased potency. As a ghost, you can only leave the sewers after being dead for at least a day. Furthermore, if a player has consumed **coleslaw**, they can **'!bust'** ghosts, which sends them back to the sewers. After amassing sufficient **Negative Slime** ghosts can summon **negaslimoids** in the city, with the use of **'!summon [name]'**. Negaslimeoids haunt all players within a district, and also decay capture progress. **The Rowdy Roughhouse** and **Cop Killtown** will send out a response that mentions which district a Negaslimeoid has entered into. Ghosts can also **!inhabit** living players to move alongside them. If a ghost has sufficient antislime, they may also **!possessweapon** or **!possessfishingrod** to grant bonuses to the player they're inhabiting, with a potential reward in antislime if conditions are fulfilled. For more detailed information on ghost mechanics, see https://rfck.miraheze.org/wiki/Ghosts",
	# Additional gameplay mechanics, part 2
	"slimeoids":"**SLIMEOIDS** are sentient masses of slime that you can keep as **pets**. To learn how to make one for yourself, visit **The Slimeoid Laboratory** in Brawlden and check the enclosed **'!instructions'**. After you've made one, you can also battle it out with other slimeoids in **The Arena**, located in Vandal Park. Slimeoids can also be used to fight off **negaslimeoids** that have been summoned by ghosts, though be warned, as this is a fight to the death! If your slimeoid dies, it's **HEART** is dropped, which can be sown in the ground like a poudrin, or taken to the labs to revive your slimeoid with **'!restoreslimeoid'**. In regards to your slimeoid's stats, a slimeoid's **'Moxie'** represents its physical attack, **'Chutzpah'** its special attack, and **'Grit'** its defense. Additionally, the color you dye your slimeoid with **'!saturateslimeoid'** also plays into combat. Your slimeoid gets attack bonuses against slimeoids that have its split complementary hue and resist slimeoids with its analgous hues. For more information, see the diagrams linked below (credits to Connor#3355). There are also various commands you can perform on your slimeoid, such as **'!observeslimeoid'**, **'!petslimeoid'**, **'!walkslimeoid'**, and **'!playfetch'**. To humanely and ethically euthanize your slimeoid, use **'!dissolveslimeoid'** at the laboratory. To store and release your slimeoid in a bottle (Warning: This bottle is dropped upon death!!), use **'!bottleslimeoid'** and **'!unbottleslimeoid [slimeoid]'**, respectively.\n<https://cdn.discordapp.com/attachments/492088204053184533/586310921274523648/SLIMEOID-HUE.png>\n<https://cdn.discordapp.com/attachments/177891183173959680/586662087653064706/SLIMEOID-HUE.gif>\n<https://cdn.discordapp.com/attachments/177891183173959680/586662095848996894/SLIMEOID_HUE_NOTE.png>",
	"cosmetics":"**Cosmetics** are items that the player may wear. To equip and un-equip a cosmetic, use **'!adorn [cosmetic]'** and **'!dedorn [cosmetic]'**. If you have four slime poudrins and a cosmetic material, you can use **'!smelt'** to create a new one from scratch. These cosmetic materials can be obtained from using **'!crush'** on vegetables gained by farming. Cosmetics can either be of 'plebian' or 'patrician' quality, indicating their rarity. If you win an art contest held for the community, a Kingpin will make a **Princep** cosmetic for you, which is custom tailored, and will not leave your inventory upon death. Cosmetics can be dyed with **!dyecosmetic [cosmetic name/id] [dye name/id]**. To check which cosmetics you have adorned, you can use !fashion.",
	"realestate":"The **Slimecorp Real Estate Agency** is, well, the agency where you buy real estate. First, check out the property you want with **'!consult [district]'**. The real estate agent will tell you a bit about the area. \nOnce you've made your decision, you can **'!signlease [district]'** to seal the deal. There's a down payment, and you will be charged rent every 2 IRL days. Fair warning, though, if you already have an apartment and you rent a second one, you will be moved out of the first.\n\nFinally, if you own an apartment already, you can **'!aptupgrade'** it, improving its storage capabilities, but you'll be charged a huge down payment and your rent will double. The biggest upgrade stores 40 closet items, 20 food items, and 25 pieces of furniture. And if you're ready to cut and run, use **'!breaklease'** to end your contract. It'll cost another down payment, though.\n\nYou can !addkey to acquire a housekey. Giving this item to some lucky fellow gives them access to your apartment, including all your prized posessions. Getting burglarized? Use !changelocks to eliminate all housekeys you created. Both cost a premium, though.",
	"apartments":"Once you've gotten yourself an apartment, there are a variety of things you can do inside it. To enter your apartment, do **'!retire'** in the district your apartment is located in. There are certain commands related to your apartment that you must do in a direct message to ENDLESS WAR. To change the name and description of your apartment, do **'!aptname [name]'** and **'!aptdesc [description]'**, respectively. To place and remove furniture (purchasable in The Bazaar), do **'!decorate [furniture]'** and **'!undecorate [furniture]'**, respectively. You can store and remove items with **'!stow'** and **'!snag'**, respectively. To store in and remove items from the fridge, do **'!fridge [item]'** and **'!unfridge [item]'**. To store in and remove items from the closet, do **'!closet [item]'** and **'!uncloset [item]'**, respectively. To store and remove your slimeoid, do **'!freeze'** and **'!unfreeze'**, respectively. To store and remove fish, do **'!aquarium [fish]'** and **'!releasefish [fish]'**, respectively. To store and remove items such as weapons and cosmetics, do **'!propstand [item]'** and **'!unstand [item]'**, respectively. To put away zines, do **!shelve [item]** and **!unshelve [item]**. To place crops into flower pots, do **pot [item]** and **unpot [item]** To enter someone else's apartment, you can do **'!knock [player]'**, which will prompt them to let you in. This list of commands can also be accessed by using !help in a direct message to ENDLESS WAR.",
	"stocks":"**The Stock Exchange** is a sub-zone within downtown NLACakaNM, open only during the daytime (6AM-8PM). It allows players to **'!invest'** in various **'!stocks'**, which not only affects their own personal monetary gains, but the city's economy as well. Stocks will shift up and down value, which affects the price of food associated with the food chains of those respective stocks. The rate of exchange for stocks can be checked with **'!rates'**, and to withdraw your **'!shares'** from a stock, use **'!withdraw [amount] [stock]'** (the same logic also applies to !invest). Additionally, players may **'!transfer'** their slimecoin to other players at any time of the day while in the stock exchange, but at the cost of a 5% broker's fee and a 20 minute cooldown on subsequent transfers.",
	# Additional gameplay mechanics, part 3
	"trading": "Trading allows you to exchange multiple items at once with another player. You can ask someone to trade with you by using **!trade [player]**. Should they accept, you will be able to offer items with **!offer [item]**. Use **!removeoffer [item]** to remove an item from your offers. You can check both player's offers by using **!trade** again. When you're ready to finish the trade, use **!completetrade**. The items will only be exchanged when both players do the command. Note that if a player adds or removes an item afterwards you will no longer be set as ready and will need to redo the command. Should you want to cancel the trade, you can do so by using **!canceltrade**.",
	"weather": "The weather of NLACakaNM can have certain outcomes on gameplay, most notably in regards to mutations like White Nationalist or Light As A Feather. Right now, however, you should be most concerned with **Bicarbonate Rain Storms**, which rapidly destroy slime both on the ground and within your very being. It's advised that you pick up a rain coat at The Bazaar to avoid further harm. To check the weather, use **'!weather'**.",
	"casino": "**The Casino** is a sub-zone in Green Light District where players may bet their slime and slimecoin in various games, including **'!slimepachinko'**, **'!slimecraps'**, **'!slimeslots'**, **'!slimeroulette'**, **'!slimebaccarat'**, and **!slimeskat**. Some games allow you to bet certain amounts, while other games have a fixed cost. Furthermore, the casino allows you to challenge other players to a game of **'!russianroulette'**, where most of the loser's slime is transferred to the winner. A recent takeover by SlimeCorp has introduced a policy requiring 20% of all winnings to be sent directly to them. To bet with slime, simply add 'slime' to the name of the game you wish to play. Example: **!slimeslots 500 slime**.",
	"bleeding": "When you get hit by someone using a '!kill' command, certain things happen to your slime. Let's say you take 20,000 points of damage. **50%** of that slime, in this case 10,000, immediately becomes scavengeable. However, the other 50%, provided that you didn't die instantly, will undergo the **bleeding** process. 25% of that slime, in this case 5,000, is immediately added to a 'bleed pool', causing it to slowly trickle out of your body and onto the ground for it to be scavenged. The remaining 25% of that slime will **slowly** be added to the 'bleed pool', where it will then bleed, just as previously stated. Upon dying, your 'bleed pool' is immediately dumped onto the ground, ready to be scavenged. Think of it like the 'rolling HP' system from the game *EarthBound*. When you get hit, you don't take all your damage upfront, it instead slowly trickles down.",
	"offline":"Given that ENDLESS WAR is a **Discord** game, there are a few peculiarities surrounding it and how it interacts with Discord itself. When you set your status to **'Offline'**, you can still move between districts if you typed a '!goto' command beforehand. You won't show up on the sidebar in that district's channel, but people can still scout for you, and see the '[player] has entered [district]' message when you do enter the district they're in. Furthermore, you **can't** use commands while offline, and can only use commands **10 seconds** after coming online again. Often times, you may find yourself using '!scout' or '!look' on a district, only to find that **no one** is there besides yourself. This is likely because they're in that district, just with their status set to offline. The exception to this, of course, is if you have the **Chameleon Skin** mutation, which lets you type a handful of commands even while offline, including **!goto**, **!look**, **!scout**, **!survey**, **!embark**, and **!disembark**.",
	# Additional gameplay mechanics, part 4
	"profile": "This isn't so much a guide on gameplay mechanics as it is just a guide for what to expect from roleplaying in ENDLESS WAR. The general rule of thumb is that your profile picture will act as your 'persona' that gets depicted in fanworks, and it can be said that many of the colorful characters you'll find in NLCakaNM originated in this way.",
	"manuscripts": "First of all, to start a manuscript, you're gonna need to head down to the Cafe, either University, or the Comic Shop.\n\nYou can **!beginmanuscript [title]** at the cost of 20k slime.\n\nIf you happen to regret your choice of title, you can just **!settitle [new title]**.\n\nThe author name is already set to your nickname, but if you want to change it, you change your nickname and then **!setpenname**.\n\nYou're required to specify a genre for your future zine by using **!setgenre [genre name]** (Genre list includes: narrative, historical, comic, ||porn||, instructional, lore, reference, journal, newspaper, and experimental).\n\nIf at any time you would like to look at the title, author name, and length of your manuscript, then use **!manuscript**.\n\n*NOW*, if you actually want to start getting stuff done, you're gonna need to **!editpage [page number] [content]**. Every zine has 10 pages (kinda) that you can work with, but you can **!setpages [pages]** to customize it (maximum is 20, minimum is 5). Each holds a maximum of 1500 characters of content. You can fill it with information, image links, smut, whatever floats your freakish boat. If you try to edit a page that already has writing, it will ask you to confirm the change before overwriting it.\n\nYou can also set a cover, which is optional. You do this with **!editpage cover [image link]**.\n\nTo check any of your pages, simply **!viewpage [number]** to see how it looks.\n\nKeep in mind that manuscripts ARE NOT items and can't be lost on death. They're accessible from any authoring location (Cafe, NLACU, NMS, Comics). A player can only have 1 manuscript out at a time.\n\nOnce you are completely finished, you can **!publish** your manuscript (it will ask you to confirm that you are completely done with it), which will enable the citizens of the town to purchase it from any zine place. From there, it will be bought and rated by the people and you may even earn some royalty poudrins for it.",
	"zines": "Zines are the hot new trend in Neo-Milwaukee and give slimebois of all shapes and sizes access to the free-market of information and culture.\n\nTo obtain a zine, you must head down to any of these locations: Green Cake Cafe, NLAC University, Neo-Milwaukee State, or Glockbury Comics.\n\nFrom there, you can **!browse** for zines. They are ordered by *Zine ID*, but you have many options for sorting them, including: **title, author, datepublished,** any of the genres (including **narrative, historical, comic, ||porn||, instructional, lore, reference, journal, newspaper,** and **experimental**.), **length, sales,** and **rating** (use **!browse [criteria]**). You can also add **reverse** on to any of these in order to make it display in reverse order. Example: **!browse bestsellers reverse** (essentially looks for worse-selling zines). Browsing in the Comic Shop will automatically browse for comic zines and browsing at the Colleges will look for historical zines (keep in mind that any zines can be bought from these places).\n\nYou can also **!browse [Zine ID]** in order to get info about that specific zine, including sales, length, genre, and rating.\n\nOnce you've found a zine that's caught your eye, simply **!orderzine [Zine ID]** to buy it for 10k slime.\n\nAfter absorbing the zine's content, it is your moral obligation as a reader to **!review [Zine Name] [Score]**. The potential scores range from between 1 and 5 *fucks* (whole numbers only). If you hate a zine, then give it one fuck. If you absolutely loved it, give it five fucks. Simple. By the way, if a zine's average rating is less than 2.0 by the time it gets to 10 ratings (or less than 1.5 by 5 ratings), it will be excluded from the default browse. The only way to purchase it will be to use the **worstrated** or **all** sorting methods.\n\nYou can **!shelve [zine name]** in your apartment after you've finished.",
	#"sap": "**Sap** is a resource your body produces to control your slime. It's integral to being able to act in combat. You can have a maximum amount of sap equal to 1.6 * ( your slime level ^ 0.75 ). When you spend it, it will regenerate at a rate of 1 sap every 5 seconds. You can spend your sap in a variety of ways: **!harden [number]** allows you to dedicate a variable amount of sap to your defense. Hardened sap reduces incoming damage by a factor of 10 / (10 + hardened sap). Your hardened sap counts against your maximum sap pool, so the more you dedicate to defense, the less you will have to attack. You can **!liquefy [number]** hardened sap back into your sap pool. Every attack requires at least 1 sap to complete. Different weapons have different sap costs. Some weapons have the ability to destroy an amount of hardened sap from your target, or ignore a portion of their hardened sap armor. This is referred to as **sap crushing** and **sap piercing** respectively. There are also other actions you can take in combat, that cost sap, such as: **!aim [player]** will slightly increase your hit chance and crit chance against that player for 10 seconds. It costs 2 sap. **!dodge [player]** will decrease that players hit chance against you for 10 seconds. It costs 3 sap. **!taunt [player]** will decrease that player's hit chance against targets other than you for 10 seconds. It costs 5 sap.",
	"sprays":"**Sprays** are your signature piece of graffiti as a gangster. You can **!changespray <image link>** in order to set your own custom image. This image appears when you get a critical hit while capping, and you can also **!tag** to spray it anywhere.",
	# Misc.
	"slimeball": "Slimeball is a sport where two teams of players compete to get the ball into the opposing team's goal to score points. A game of Slimeball is started when a player does !slimeball [team] in a district. Other players can join in by doing the same command in the same district. Once you've joined a game, you can do !slimeball to see your data, the ball's location and the score. To move around the field, use !slimeballgo [coordinates]. You can kick the ball by running into it. To stop, use !slimeballstop. Each team's goal is open between 20 and 30 Y, and located at the ends of the field (0 and 99 X for purple and pink respectively). To leave a game, do !slimeballleave, or join a different game. A game of Slimeball ends when no players are left.",

	# Weapons
	"normal": "**Normal weapons** include the **Dual Pistols**, **Revolver**, and the **Yo-yo**. They have a damage modifier of 110%, no cost modifier, 20% crit chance, a crit multiplier of 180%, and a 90% chance to hit. These are straight forward weapons with no gimmicks and average damage.",
	"multiple-hit": "**Multiple hit weapons** include the **SMG**, **Assault Rifle**, and the **Nunchuck**. They deal three attacks per kill command with an overall cost modifier of 80%, and each attack has a 40% damage modifier, 20% crit chance, a crit multiplier of 150%, and an 85% chance to hit. These are very safe reliable weapons, though they deal slightly below average damage on average.",
	"variable-damage": "**Variable damage weapons** include the **Nailbat**, **Bass**, and the **Brass Knuckles**. They have a randomised damage modifier between 50% and 250%, no cost modifier, 10% crit chance, a crit multiplier of 150%, and a 90% chance to hit. On average, these weapons deal pretty good damage for a very reasonable attack cost, but their unreliability can make them quite risky to use.",
	"small-game": "**Small game weapons** include the **Knives** and the **Minecraft Bow**. They have a damage modifier of 50%, a cost modifier of 25%, 10% crit chance, a crit multiplier of 200%, and a 95% chance to hit. These are reliable and underpowered weapons, with extremely low usage costs making them very efficient. Best used for bullying weaklings and hunting.",
	"heavy": "**Heavy weapons** include the **Scythe** and the **Broadsword**. They have a damage modifier of 300%, a cost modifier of 500%, 5% crit chance, a crit multiplier of 150%, and an 80% chance to hit. Unreliable and incredibly expensive to use, to compensate for their very high damage.",
	"defensive": "**Heavy weapons** currently only include the **Umbrella**. While you have one equipped, you take 25% reduced damage! They have a damage modifier of 75%, a cost modifier of 150%, 10% crit chance, a crit multiplier of 150%, and an 85% chance to hit, with a captcha of 4. Best used for punching down or protecting yourself while traveling, these weapons are typically too weak and unwieldy for use in normal combat scenarios.",
	"precision": "**Precision weapons** currently only include the **Katana**. They have a damage modifier of 130%, a cost modifier of 130%, a crit multiplier of 200%, with a captcha of 4. They always hit, and get a guaranteed crit if you have no other weapons equipped. These weapons deal very high and reliably damage, but only if you're willing to bear the burden of their captcha and the lack of flexibility they impose.",
	"incendiary": "**Incendiary weapons** include the **Molotov Bottles** and the **Dragon Claw**. They have a damage modifier of 75%, a cost modifier of 150%, 10% crit chance, a crit multiplier of 200%, a 90% chance to hit, and a captcha of 4. You will take 10% to 15% of your slime as damage if you enter the captcha wrong! They also deal an extra 50% damage to the target and any flagged enemies in the area over time, causing them to explode on death. A more powerful alternative to explosive weapons, if you can deal with the damage being dealt over time, rather than on one go.",
	"explosive": "**Incendiary weapons** currently only include the **Grenades**. They have a damage modifier of 75%, a cost modifier of 150%, 10% crit chance, a crit multiplier of 200%, a 90% chance to hit, and a captcha of 4. You will take 10% to 15% of your slime as damage if you enter the captcha wrong! They also deal an extra 50% damage to the target and any flagged enemies in the area. The go-to if you're being swarmed by a mob of weaklings, can clear entire districts in one go.",

	weapon_id_revolver: "**The revolver** is a normal weapon for sale at the Dojo. It's an ordinary six-shot revolver, so you'll have to **!reload** it after attacking six times, though its attack cost is reduced to 80% to compensate. Goes well with a cowboy hat.",
	weapon_id_dualpistols: "**The dual pistols** are a normal weapon for sale at the Dojo. Shockingly, these aren't that common, despite the city being chock-full of gangsters.",
	weapon_id_shotgun: "**The shotgun** is a heavy weapon for sale at the Dojo. It's a double barrelled shotgun, so you'll need to !reload after every two shots, though your cost multiplier is reduced down to 400% to compensate. Grass grows, birds fly, sun shines, and this thing hurts people; it's a force of nature.",
	weapon_id_rifle: "**The rifle** is a multiple-hit weapon for sale at the Dojo. Its magazine only holds enough bullets for ten attacks, so you'll have to **!reload** after hitting the rate limit, but its cost multiplier goes down to 70% to compensate. The experts are still undecided, but most people would agree this is a FAMAS.",
	weapon_id_smg: "**The SMG** is a multiple hit-weapon for sale at the Dojo. Its magazine only holds enough bullets for ten attacks, so you'll have to **!reload** after hitting the rate limit, but its cost multiplier goes down to 70% to compensate. This is pretty good if you like to move around a lot, since the crosshair doesn't grow that much while you're sprinting.",
	weapon_id_bat: "**The nailbat** is a variable-damage weapon for sale at the Dojo. This thing could actually be used to hit balls if you took the nails off it, but that seems a little high-tech...",
	weapon_id_brassknuckles: "**The brass knuckles** are a variable-damage weapon for sale at the Dojo. Made by sanding away most of a huge pair of metal gauntlets.",
	weapon_id_katana: "**The katana** is a precision weapon for sale at the Dojo. This weapon is folded over a thousand times, so it can cut clean through steel and is vastly superior to any other weapon on earth.",
	weapon_id_broadsword: "**The broadsword** is a heavy weapon for sale at the Dojo. Modeled after a legendary Scottish blade, said to have lopped off a hundred enemy heads and then its own wielder's.",
	weapon_id_nunchucks: "**The nunchucks** are a multiple-hit weapon for sale at the Dojo. 我不僅在未經武裝的戰鬥中接受了廣泛的訓練，而且我可以接觸到美國海軍陸戰隊的整個武庫，而且我會盡其所能將你那可悲的屁股從整個非洲大陸上擦掉，你一點都不討厭。 如果只有您能知道您的小“聰明”評論對您造成了什麼邪惡的報應，也許您會held之以鼻。 但是你不能，你沒有，現在你要付出代價了，你這該死的白痴。 我會在你周圍大怒，你會淹死在裡面。 你他媽的死了，孩子。",
	weapon_id_scythe: "**The scythe** is a heavy weapon for sale at the Dojo. Often mistaken for a bardiche, this is actually one of the better weapons for a PvE-focused DEX build if you don't mind the long recovery animation after whiffing an attack.",
	weapon_id_yoyo: "**The yo-yo** is a normal weapon for sale at the Dojo. All the sick tricks you can pull off with this thing are frankly unremarkable compared to the primal joy of cracking a hole through someone's skull with this tungsten wheel of death.",
	weapon_id_bass: "**The bass guitar** is a variable-damage weapon acquired via smelting. It makes the most beautiful sounds when plucking your enemies' tendons.",
	weapon_id_umbrella: "**The umbrella** is a defensive weapon for sale at the Bazaar. It has a futurecore feel to it, with the reinforced graphene canopy allowing visibility from the inside out, but not the other way around. Certainly one of the most stylish weapons seen in the city.",
	weapon_id_knives: "**The throwing knives** are a small-game weapon for sale at the Dojo. These are often quite dull, relying less on the knives's inherent properties and more on the slime-fueled superstrength of its wielders to pierce through their targets.",
	weapon_id_molotov: "**The molotov bottles** are an incendiary weapon for sale at the Dojo. Made with a special slime-based concoction powerful enough to level Juvie's Row if applied correctly. This shit is like bottled malice.",
	weapon_id_grenades: "**The grenades** are an explosive weapon for sale at the Dojo. These may actually be nuclear powered, judging by their ability to wipe out entire districts full of gangsters in one blast.",
	weapon_id_dclaw: "**The Dragon Claw** is an incendiary weapon acquired via smelting. It merges into your body, turning your arm into a weapon of mass destruction.",
	weapon_id_bow: "**The minecraft bow** is a small-game weapon acquired via smelting. The calming music most people hum while wielding this thing is quite the interesting contrast, when considered along with the impaled corpses they leave behind.",

	weapon_id_garrote: "**The Garrote Wire** is a unique weapon. It has a damage modifier of 1500%, no cost modifier, guaranteed hits, and a 1% chance for a crit, which does 1000% damage. When you attack with a garrote, the target has 5 seconds to send any message before the damage is done. If they do, the attack fails.",
	weapon_id_minigun: "The **Minigun** is a special variant of **variable damage weapons**. It deals ten attacks per kill command with an overall cost modifier of 500%, and each attack has a 30% damage modifier, 10% crit chance, a crit multiplier of 200%, and a 50% chance to hit, with a captcha of 6. This is a strange weapon that can potentially deal astronomical damage if used in the right circumstances, and if you're willing to deal with its exceptionally long captcha.",
	weapon_id_staff: "The **Eldritch Staff** is a unique weapon. By default, it has a damage modifier of 30%, a cost modifier of 200%, guaranteed hits, no crit chance, and a crit multiplier of 180%. A number of conditions may be met to increase the damage multiplier by 60% and crit chance by 6.66%: tenebrous weather and locations, grudges between the user and its target, the time of day, and the user's general degeneracy will all contribute to the weapon's effectiveness.",

	weapon_id_spraycan: "**The spray can** is a paint tool for sale at Based Hardware. It has a capping modifier of 0.8 and a spray cost mod of 1. It has a captcha length of 4, a miss chance of 10% and a 10% chance for a crit, which does 2x influence.",
	weapon_id_paintgun: "**The paint gun** is a paint tool for sale at Based Hardware. It has a capping modifier of 0.7 and a spray cost mod of 0.75. It has a captcha length of 6, a miss chance of O% and a 20% chance for a crit, which does 2x influence.",
	weapon_id_paintroller: "**The paint roller** is a paint tool for sale at Based Hardware. It has a capping modifier of 1.75 and a spray cost mod of 4. It has a captcha length of 4, a miss chance of 10% and a 10% chance for a crit, which does 2x influence.",
	weapon_id_paintbrush: "**The paint brush** is a paint tool for sale at Based Hardware. It has a capping modifier of 0.5 and a spray cost mod of .25. It has a captcha length of 4, a miss chance of 10% and a 10% chance for a crit, which does 1.5x influence.",
	weapon_id_watercolors: "**Watercolors** are a paint tool for sale at Based Hardware. It does a set 4000 influence per shot. It has a captcha length of 3, a miss chance of 10% and a .1% chance for a crit, which zeros out the whole district regardless of owner.",
	weapon_id_thinnerbomb: "**Thinner bombs** are a paint tool for sale at Based Hardware. It has a capping modifier of 0.15 and a spray cost mod of 2. It has a captcha length of 4, a miss chance of 10% and a 10% chance for a crit, which does 2x influence. When you cap with a thinner bomb, it is used up, and you have to buy more. When decapping, damage is multiplied by 10.",

	# "otp":"If you find that you have a role with 'OTP' in the name, don't be alarmed. This just means that you're outside a safe place, such as your apartment, or your gang base / juvie's row. It's essentially a signal to other players that you're actively participating in the game.",
}

# Keys are retrieved out of order in older versions of python. This list circumvents the issue.
help_responses_ordered_keys = [
	"gangs", "food", "capturing", "transportation", "death",
	"dojo", "subzones", "scouting", "wanted", "combat",
	"mining", "scavenging", "farming", "fishing", "hunting",
	"mutations", "mymutations", "smelting", "sparring", "ghosts",
	"slimeoids", "cosmetics", "realestate", "apartments", "stocks",
	"trading", "weather", "casino", "bleeding", "offline",
	"profile", "manuscripts", "zines", "sap", "sprays",
	"slimeball",
]

weapon_help_responses_ordered_keys = [
	weapon_id_revolver, weapon_id_dualpistols, weapon_id_shotgun,
	weapon_id_rifle, weapon_id_smg, weapon_id_bat, 
	weapon_id_brassknuckles, weapon_id_katana, weapon_id_broadsword,
	weapon_id_nunchucks, weapon_id_scythe, weapon_id_yoyo,
	weapon_id_bass, weapon_id_umbrella, weapon_id_knives,
	weapon_id_molotov, weapon_id_grenades, weapon_id_dclaw, weapon_id_bow,
	weapon_id_garrote, weapon_id_minigun, weapon_id_staff,
	weapon_id_spraycan, weapon_id_paintgun, weapon_id_paintroller, weapon_id_paintbrush,
	weapon_id_watercolors, weapon_id_thinnerbomb,
	"normal", "multiple-hit", "variable-damage",
	"small-game", "heavy", "defensive",
	"precision", "incendiary", "explosive",
]

mutation_descriptions = {
	mutation_id_spontaneouscombustion: "Upon dying you do damage proportional to your current slime level, calculated as (level^4)/5, hitting everyone in the district. Example: A level 50 player will do 1,250,000 damage.",
	#mutation_id_thickerthanblood: "On a fatal blow, immediately receive the opponent’s remaining slime, causing none of it to bleed onto the ground or go your kingpin. Its effects are diminished on hunted enemies, however.",
	mutation_id_fungalfeaster: "On a fatal blow, restore all of your hunger.",
	mutation_id_sharptoother: "The chance to miss with a weapon is reduced by 50%. Specifically, a normal miss will now have a 50% to either go through as a miss or a hit.",
	mutation_id_2ndamendment: "One extra equippable weapon slot in your inventory. You receive a 25% damage buff if two non-tool weapons are in both your weapon slots.",
	mutation_id_bleedingheart: "When you are hit, bleeding pauses for 5 minutes. Use !bleedout to empty your bleed storage onto the floor.",
	mutation_id_nosferatu: "At night (8PM-6AM), upon successful hit, 60% of splattered slime is absorbed directly into your slime count.",
	mutation_id_organicfursuit: "Double damage, double movement speed, and 10x damage reduction every 31st night. Use **'!fursuit'** to check if it's active.",
	mutation_id_lightasafeather: "Double movement speed while weather is windy. Use **'!weather'** to check if it's windy.",
	mutation_id_whitenationalist: "Cannot be scouted regularly and you scavenge 50% more slime while weather is snowy, which also stacks with the Webbed Feet mutation. Use **'!weather'** to check if it's snowing. You can still be scouted by players with the Keen Smell mutation.",
	mutation_id_spoiledappetite: "You can eat spoiled food.",
	mutation_id_bigbones: "The amount of food items you can hold in your inventory is doubled.",
	mutation_id_fatchance: "Take 25% less damage from attacks when above 50% hunger.",
	mutation_id_fastmetabolism: "Movement speed is increased by 33% when below 40% hunger.",
	mutation_id_bingeeater: "Upon eating food, the restored hunger is multiplied by the number of dishes you’ve consumed in the past 5 seconds. Eating lots of food at once puts you in a raging food coma, increasing defense.",
	mutation_id_lonewolf: "50% more damage when in a district without any friendly gangsters. Stacks with the Patriot mutation.",
	mutation_id_quantumlegs: "You can now use the !tp command, allowing you to teleport to a district up to two locations away from you after an uninterrupted 15 second running start, with a cooldown of 3 hours.",
	mutation_id_chameleonskin: "While offline, you can move to and scout other districts and cannot be scouted.",
	mutation_id_patriot: "25% influence bonus. Stacks with Unnatural Charisma.",
	mutation_id_socialanimal: "Your damage increases by 10% for every ally in your district.",
	mutation_id_threesashroud: "Cannot be scouted and crit chance is doubled if there are more than 3 allies in your district. Cannot be scouted by players with the Keen Smell mutation.",
	mutation_id_aposematicstench: "For every 5 levels you gain, you appear as 1 more person when being scouted. Cannot be scouted by players with the Keen Smell mutation. Use !stink to produce a monster repelling effect. Attacking enemies with it on causes a temporary damage nerf and the removal of the effect.",
	mutation_id_lucky: "33% higher chance to get slime poudrins from mining and farming, and better luck at casino games. Increased !reel chance.",
	mutation_id_dressedtokill: "50% more damage if freshness is at least 250.",
	mutation_id_keensmell: "Scouting will list off the names of players and enemies within a district. Will not work on players with the Aposematic Stench or Three's A Shroud mutations.",
	mutation_id_enlargedbladder: "You can use the !piss command, which, if targeted at a player like with !kill, spends 1 of your liquid sap, but crushes 3 of the target's hardened sap.",
	mutation_id_dumpsterdiver: "10x chance to get items while scavenging with just '!scavenge'. Captcha scavenges search for items using a random single letter of the captcha.",
	mutation_id_trashmouth: "Reach maximum power scavenges 3 times as fast. Example: The soft cooldown of 15 seconds on scavenging is now reduced to 5 seconds. You can also eat cosmetics and furniture. You can also eat furniture and cosmetics using !devour <item>.",
	mutation_id_webbedfeet: "Your scavenging power increases the more slime there is in a district. Caps out at 400% more slime gained from scavenging, but does stack with the White Nationalist mutation. You can feel out the amount of slime you scavenge.",

    mutation_id_dyslexia:"The size of captchas is decreased by 3 characters. If a captcha is smaller than 3, the captcha length will be 1 instead.",
    mutation_id_handyman:"If you kill an enemy gangster with a tool instead of a weapon, your kingpin gets double the slime they normally do.",
    mutation_id_packrat:"Apartment storage is doubled, regardless of apartment class.",
    mutation_id_stickyfingers:"When using !order at a store, there is a 20% chance to get the item for free. You still need to have the slime to purchase it, though.",
    mutation_id_unnaturalcharisma:"Influence when !spraying goes up by 20%. You also gain 500 freshness.",
    mutation_id_rigormortis:"You are able to !preserve up to 5 items. These items will not drop when you are killed. You must have this mutation for the preservation to take effect, and the items must be in your inventory.",
    mutation_id_nervesofsteel:"As a gangster, you aren't damaged by !spray-ing in ally-surrounded districts. As a juvie, you can play Russian Roulette and commit suicide.",
    mutation_id_napalmsnot:"You do some burn damage when attacking with any weapon, in addition to its normal damage. You also gain immunity to burn damage.",
    mutation_id_ditchslap:"Use !slap @user <location> on an ally to instantly launch them to an adjacent district. If you are in a safe zone, the target must use !clench before they can be hit. Any given ally can't be slapped again for a 5 minute cooldown.",
    mutation_id_greenfingers:"Farming wait time is decreased by 33%, and yields are increased by 20%.",
    mutation_id_lightminer:"You can mine at any time of day. You are also immune to mineshaft collapses.",
    mutation_id_longarms:"You can !longdrop <destination> <item> to drop an item in an adjacent district.",
    mutation_id_lethalfingernails:"If you have no weapon, you will use your fingernails instead. They do the same damage as a level 6 revolver with no miss.",
    mutation_id_davyjoneskeister:"When making deals with Captain Albert Alexander, you only receive offers for slime, not items.",
    mutation_id_oneeyeopen:"Use !track @user to keep your eye on a specific player. If they move to a PVP zone, you will receive  a DM. If you are being tracked, you can !shakeoff @user to remove their tracking. To check who you'ree currently tracking, use !thirdeye.",
    mutation_id_bottomlessappetite:"Your maximum hunger is doubled.",
    mutation_id_airlock:"Combined effects of White Nationalist and Light as a Feather. This mutation is mutually exclusive with those. You also gain passive hunger when it's sunny, fire immunity in rain, and crit bonuses in the fog.",
    mutation_id_ambidextrous:"If you are unarmed or have a tool equipped, and have a weapon in your sidearm slot, you will default to that weapon.",
    mutation_id_coleblooded:"You get the ability to bust ghosts without coleslaw. If a ghost haunts you, they lose negaslime instead of gaining it.",
    mutation_id_landlocked:"When standing in a street either bordering an outskirt or the Slime Sea, use !loop to warp to the opposite side of the map. This also works on the ferry and at Slime's End Cliffs. There is a 20 second travel time when using !loop.",
	mutation_id_amnesia:"Your display name is replaced with ????? in EW's messages, and you can delete your message commands without ENDLESS WAR reacting. On a kill, the kill feed message is delayed by 60 seconds."

}

consult_responses = {
"downtown":"Our complex in Downtown is a sight to behold, one of our most in-demand properties. The whole complex is 2-story penthouses, with built-in storage facility/fallout shelter, restaraunt sized fridge, and state-of-the-art bulletproof windows. This is an offer you won't want to pass up, believe you me. Now, perhaps you're concerned about the large amount of gang violence in the area. But, uh...shut up. ",
"smogsburg":"Have you ever wanted wake up to a haze outside your window every morning? Or to fall asleep to the sound of bazaar merchants bickering with one another in foreign languages? I do, too! That's why I live in Smogsburg, where the prices are low and the furniture is close! Seriously, because of how nearby it is to the bazaar, I've been sniping amazing deals on high quality furniture. Wait...why are you looking at me like that? Actually on second thought, don't buy a property here. I don't want you to steal my shit.",
"krakbay":"Krak Bay is a real social hotspot. Teenagers come from all over to indulge in shopping sprees they can't afford and gorge themselves on fast food with dubious health standards. I say this all as a compliment, of course. Stay here, and you won't have to walk through the city for ages just to get a good taco. As for the apartment quality, you can rest assured that it is definitely an apartment.",
"poudrinalley":"You know, people point to the labrynthine building structure and the morbid levels of graffiti and say this place is a wreck. I don't think so, though. Graffiti is art, and unlike many districts in NLACakaNM, the densely packed cityscape makes it difficult to get shot through your window. The 7-11's right around the corner, to boot. For that, I'd say we're charging a real bargain.",
"greenlightdistrict":"Did you just win the lottery? Have you recently made spending decisions that alientated you from your family? Are you TFAAAP? Then the Green Light District Triple Seven Apartments are for you! Gamble, drink, and do whatever they do in brothels to your heart's content, all far beyond the judging eyes of society! Just remember, with rent this high, you should enjoy those luxuries while they last...",
"oldnewyonkers":"Eh? I guess you must've liked the view outside. I can't blame you. It's a peaceful sight out there. Lots of old folks who just want to live far away from the gang violence and close to people they can understand. They might say some racist shit while you're not looking, but getting called a bustah never hurt anybody. Wait, shit. Don't tell my boss I said the B word. Shit. OK, how about this? We normally charge this property higher, but here's a discount.",
"littlechernobyl":"You're an adventurous one, choosing the good ol' LC. The place is full of ruins and irradiated to hell. A friend of mine once walked into the place, scrawny and pathetic, and walked out a griseled man, full of testosterone and ready to wrestle another crazed mutant. Of course, his hair had fallen out, but never mind that. I'm sure your stay will be just as exciting. Just sign on the dotted line.",
"arsonbrook":"Oh, Arsonbrook? Hang on, I actually need to check if that one's available. You know how it is. We have to make sure we're not selling any torched buildings to our customers. I realize how that sounds, but owning an apartment in Arsonbrook is easier than you think. Once you're settled in with a fire extinguisher or three, the local troublemakers will probably start going for emptier flats. And even if your house does get burned down, it'll be one hell of a story.",
"astatineheights":"If you live with the yuppies in Astatine Heights, people will treat you like a god. When you walk by on the street, they'll say: \"Oh wow! I can't believe such a rich Juvie is able to tolerate my presence! I must fellate him now, such that my breathing is accepted in their presence!\" It has amazing garage space and a walk-in fridge. Trust me, the mere sight of it would make a communist keel over in disgusted envy.",
"gatlingsdale":"You'll be living above a bookstore, it looks like. We'd have a normal apartment complex set up, but these pretentious small businesses refuse to sell their property. Guess you'll have to settle for living in some hipster's wet dream for now. We here at SlimeCorp are working to resolve the inconvenience as soon as we can. On the upside, you have every liberty to shout loudly below them and disrupt their quiet reading enviornment.",
"vandalpark":"Did you know that the apartment complex we have for lease was once lived in by the famous Squickey Henderson? That guy hit like 297 home runs in his career, and you better believe he picked up his bat skills from gang violence. What I'm telling you is, if you buy property here, then you're on your way to the major leagues, probably! Besides, the apartment is actually pretty well built.",
"glocksbury":"There are a lot of police here. I can see the frothing rage in your eyes already, but hear me out. If you want to go do the gang violence, or whatever you kids do these days, then you can go over someplace else and do it there. Then, when you come back, your poudrins and dire apples will still be unstolen. I suppose that still means you're living around cops all the time, but for this price, that may be an atrocity you have to endure.",
"northsleezeborough":"This place may as well be called Land of the Doomers, for as lively as the citizens are. They're disenfranchised, depressed, and probably voted for Gary Johnson. My suggestion is not to avoid them like the plague. Instead, I think you really ought to liven up their lives a little. Seriously, here you have a group of un-harassed people just waiting for their lives to go from bad to worse! I think a juvenile delinquent like yourself would be right at home. Wait, is that incitement? Forget what I just said.",
"southsleezeborough":"Ah, I see. Yes, I was a weeb once, too. I always wanted to go to the place where anime is real and everyone can buy swords. Even if the streets smell like fish, the atmosphere is unforgettable. And with this apartment, the place actually reflects that culture. The doors are all sliding, the bathroom is Japanese-style, and your window overlooks to a picturesque view of the Dojo.",
"oozegardens":"This place has such a lovely counterculture. Everybody makes the community beautiful with their vibrant gardens, and during the night they celebrate their unity with PCP and drum circles. Everybody fucks everybody, and they all have Digibro-level unkempt beards. If you're willing to put gang violence aside and smell the flowers, you'll quickly find your neighbors will become your family. Of course, we all know you're unwilling to do that, so do your best to avoid killing the damn dirty hippies, OK?",
"cratersville":"OK...what to say about Cratersville? It's cheap, for one. You're not going to get a better deal on housing anywhere else. It's... It has a fridge, and a closet, and everything! I'm pretty sure there aren't holes in any of those objects, either, at least not when you get them. What else? I guess it has less gang violence than Downtown, and cleaner air than Smogsburg. Actually, fuck it. This place sucks. Just buy the property already. ",
"wreckington":"So you want to eat a lot of really good pancakes. And you also want to live in a place that looks like war-torn Syria. But unfortunately, you can't do both at the same time. Well boy howdy, do I have a solution for you! Wreckington is world famous for its abandoned and demolished properties and its amazing homestyle diner. More than one apartment complex has actually been demolished with people still in it! How's that for a life-enhancing risk?",
"slimesend":"I like to imagine retiring in Slime's End. To wake up to the sound of gulls and seafoam, to walk out into the sun and lie under a tree for the rest my days, doesn't it sound perfect? Then, when my old age finally creeps up on me, I can just walk off the cliff and skip all those tearful goodbyes at the very end. Er...right, the apartment. It's pretty good,  a nice view. I know you're not quite retiring age, but I'm sure you'll get there.",
"vagrantscorner":"Hmm. I've never actually been to Vagrant's Corner. And all it says on this description is that it has a lot of pirates. Pirates are pretty cool, though. Like, remember that time when Luffy had Rob Lucci in the tower, and he Gum Gum Gatling-ed the living shit out of him and broke the building? That was sick, dude. OK, Google is telling me that there's a pretty good bar there, so I suppose that would be a perk, too.",
"assaultflatsbeach":"Sure, the flat has massive storage space in all aspects. Sure, you can ride a blimp to work if you feel like it. Sure, it's the very definition of \"beachhouse on the waterfront\". But do you REALLY know why this is a top piece of real estate? Dinosaurs. They're huge, they attack people, they're just an all around riot. If you catch some of the ones here and sell them to paleontologists, this place will pay itself back in no time.",
"newnewyonkers":"Let's be real for a second: I don't need to tell you why New New Yonkers is amazing. They have basically everything there: bowling, lazer tag, arcades, if it distracts adolescents, they have it. Don't let the disgusting old people tell you otherwise: this place is only going up from here. Sure, we had to skimp out a bit on the structural integrity of the place, but surely that won't be noticed until vandals eventually start trying to break it down.",
"brawlden":"Brawlden's not too scary to live in, relatively speaking. Maybe you'll get pummeled by a straggling dad if you look at him funny, but chances are he won't kill you. If the lanky fellows down at Slimecorp Labs are able to live in Brawlden, I'm sure you can too. And think of the money you're saving! A \"quality\" apartment, complete with the best mini-fridge and cupboard this side of the city!",
"toxington":"Are you really considering living in a place that's completely overrun with deadly gases? It's called TOXINGTON, you idiot! The few people who live there now are miners whose brains were already poisoned into obsolescence. I know we technically sell it as a property, but come on, man! You have so much to live for! Call a suicide hotline or get a therapist or something. Anything but this.",
"charcoalpark":"It's a po-dunk place with po-dunk people. That is to say, it doesn't matter. Charcoal Park is the equivalent of a flyover state, but its location on the edge of the map prevents even that utility. That's exactly why it's perfect for a juvie like yourself. If you want to go into hiding, I personally guarantee the cops will never find you. Of course, you may end up assimilating with the uninspired fucks that live there, but I think that it still fills a niche here in our fair city.",
"poloniumhill":"If you live with the wannabes in Polonium Hill, people will treat you like a dog. When you walk by on the street, they'll say: \"Oh damn! I can't believe such a desperate Juvie is able to go on living! I must slit their throat just to put 'em out of their misery!\" It nonetheless has amazing storage space and a big, gaudy-looking fridge. Trust me, the mere sight of it would make a communist keel over from the abject waste of material goods. I'm just being honest, buddy. Go live in Astatine Heights instead.",
"westglocksbury":"If you ever wanted to turn killing people into a reality show, this is probably where you'd film it. The cops were stationed in Glocksbury in order to deal with this place, but they don't tread here for the same reason most of us don't. The corpses here get mangled. I've seen ripped out spines, chainsaw wounds, and other Mortal Kombat-like lacerations. Our photographer couldn't even take a picture of the property without getting a severed leg in the shot. But, as a delinquent yourself, I imagine that could also be a good thing.",
"jaywalkerplain":"Are you one of those NMU students? Or maybe you're after the drug culture. Well in either case, Jaywalker Plain's an excellent place to ruin your life. In addition to having lots of like-minded enablers, the countless parks will give you the perfect spot to pace and ruminate on your decisions. You know, this is a sales pitch. I probably shouldn't make the place sound so shitty.",
"crookline":"Now, we've gotten a lot of complaints about thieves here, stealing our clients' SlimeCoin wallets and relieving them of our rent money. We acknowledge this is a problem, so for every purchase of a property in Crookline, we've included this anti-thievery metal codpiece. Similar to how a chastity belt blocks sexual urges, this covers your pockets, making you invulnerable to petty thieves. Apart from that perk, in Crookline you'll get a lovely high-rise flat with all the essentials, all coated in a neat gloomy neon aesthetic.",
"dreadford":"Have you ever wanted to suck on the sweet, sweet teat of ultra-decadence? Do you have multiple yachts? Do you buy both versions of Pokemon when they come out, just because you can blow the cash? Ha. Let me introduce you to the next level of opulence. Each apartment is a full-scale mansion, maintained by some of the finest slimebutlers in the industry. In the morning they tickle your feet to get you up, and at night they sing you Sixten ballads to drift you back to restful slumber. The place is bulletproof, fireproof, and doubles as a nuclear bunker if things go south. And it stores...everything. The price, you say? Shit, I was hoping you wouldn't ask.",
"maimridge":"Perhaps you think it's sketchy that we're selling lightly refurbished log cabins built eons ago. Well let me ask you something, young juvie: do you like getting laid? Well, living in Maimridge is your ticket into ice-cold lust and debauchery. You just bring a lady friend or whoever into your isolated mountain cabin, and our state-of-the-art faulty electrical wiring will leave you stranded and huddling for warmth in no time flat! Wow...I'm picturing you now. Yeah, you definitely want this one."
}

sea_scavenge_responses = [
	"see a school of Fuck Sharks circling below you",
	"notice an approaching kraken",
	"remember you can't swim"
]

# Enemy life states
enemy_lifestate_dead = 0
enemy_lifestate_alive = 1
enemy_lifestate_unactivated = 2

# Enemy attacking types (aka 'weapons')
enemy_attacktype_unarmed = 'unarmed'
enemy_attacktype_fangs = 'fangs'
enemy_attacktype_talons = 'talons'
enemy_attacktype_tusks = 'tusks'
enemy_attacktype_raiderscythe = 'scythe'
enemy_attacktype_gunkshot = 'gunkshot'
enemy_attacktype_molotovbreath = 'molotovbreath'
enemy_attacktype_armcannon = 'armcannon'
enemy_attacktype_axe = 'axe'
enemy_attacktype_hooves = 'hooves'
enemy_attacktype_body = 'body'

enemy_attacktype_amateur = 'amateur'

enemy_attacktype_gvs_g_seeds = 'g_seeds'
enemy_attacktype_gvs_g_appleacid = 'g_appleacid'
enemy_attacktype_gvs_g_bloodshot = 'g_bloodshot'
enemy_attacktype_gvs_g_nuts = 'g_nuts'
enemy_attacktype_gvs_g_chompers = 'g_chompers'
enemy_attacktype_gvs_g_fists = 'g_fists'
enemy_attacktype_gvs_g_brainwaves = 'g_brainwaves'
enemy_attacktype_gvs_g_vapecloud = 'g_vapecloud'
enemy_attacktype_gvs_g_hotbox = 'g_hotbox'
enemy_attacktype_gvs_g_blades = 'g_blades'
enemy_attacktype_gvs_g_explosion = 'g_explosion'

enemy_attacktype_gvs_s_shamboni = 's_shamboni'
enemy_attacktype_gvs_s_teeth = 's_teeth'
enemy_attacktype_gvs_s_tusks = 's_tusks'
enemy_attacktype_gvs_s_fangs = 's_fangs'
enemy_attacktype_gvs_s_talons = 's_talons'
enemy_attacktype_gvs_s_molotovbreath = 's_molotovbreath'
enemy_attacktype_gvs_s_raiderscythe = 's_scythe'
enemy_attacktype_gvs_s_cudgel = 's_cudgel'
enemy_attacktype_gvs_s_grenadecannon = 's_grenadecannon'

# Enemy weather types. In the future enemies will make use of this in tandem with the current weather, but for now they can just resist the rain.
enemy_weathertype_normal = 'normal'
enemy_weathertype_rainresist = 'rainresist'

# Enemy types
# Common enemies
enemy_type_juvie = 'juvie'
enemy_type_dinoslime = 'dinoslime'
# Uncommon enemies
enemy_type_slimeadactyl = 'slimeadactyl'
enemy_type_desertraider = 'desertraider'
enemy_type_mammoslime = 'mammoslime'
# Rare enemies
enemy_type_microslime = 'microslime'
enemy_type_slimeofgreed = 'slimeofgreed'
# Raid bosses
enemy_type_megaslime = 'megaslime'
enemy_type_slimeasaurusrex = 'slimeasaurusrex'
enemy_type_greeneyesslimedragon = 'greeneyesslimedragon'
enemy_type_unnervingfightingoperator = 'unnervingfightingoperator'

enemy_type_civilian = 'civilian'
enemy_type_civilian_innocent = 'innocent'

# Gankers Vs. Shamblers enemies
enemy_type_gaia_poketubers = "poketubers"
enemy_type_gaia_pulpgourds = "pulpgourds"
enemy_type_gaia_sourpotatoes = "sourpotatoes"
enemy_type_gaia_bloodcabbages = "bloodcabbages"
enemy_type_gaia_joybeans = "joybeans"
enemy_type_gaia_purplekilliflower = "purplekilliflower"
enemy_type_gaia_razornuts = "razornuts"
enemy_type_gaia_pawpaw = "pawpaw"
enemy_type_gaia_sludgeberries = "sludgeberries"
enemy_type_gaia_suganmanuts = "suganmanuts"
enemy_type_gaia_pinkrowddishes = "pinkrowddishes"
enemy_type_gaia_dankwheat = "dankwheat"
enemy_type_gaia_brightshade = "brightshade"
enemy_type_gaia_blacklimes = "blacklimes"
enemy_type_gaia_phosphorpoppies = "phosphorpoppies"
enemy_type_gaia_direapples = "direapples"
enemy_type_gaia_rustealeaves = "rustealeaves"
enemy_type_gaia_metallicaps = "metallicaps"
enemy_type_gaia_steelbeans = "steelbeans"
enemy_type_gaia_aushucks = "aushucks"

enemy_type_defaultshambler = "defaultshambler"
enemy_type_bucketshambler = "bucketshambler"
enemy_type_juveolanternshambler = "juveolanternshambler"
enemy_type_flagshambler = "flagshambler"
enemy_type_shambonidriver = "shambonidriver"
enemy_type_mammoshambler = "mammoshambler"
enemy_type_gigashambler = "gigashambler"
enemy_type_microshambler = "microshambler"
enemy_type_shamblersaurusrex = "shamblesaurusrex"
enemy_type_shamblerdactyl = "shamblerdactyl"
enemy_type_dinoshambler = "dinoshambler"
enemy_type_ufoshambler = "ufoshambler"
enemy_type_brawldenboomer = "brawldenboomer"
enemy_type_juvieshambler = "juvieshambler"
enemy_type_shambleballplayer = "shambleballplayer"
enemy_type_shamblerwarlord = "shamblerwarlord"
enemy_type_shamblerraider = "shamblerraider"
enemy_type_gvs_boss = "blueeyesshamblerdragon"

# Sandbag (Only spawns in the dojo, doesn't attack)
enemy_type_sandbag = 'sandbag'

# Double Halloween bosses. Could be brought back as enemies later on, for now will only spawn in the underworld.
enemy_type_doubleheadlessdoublehorseman = 'doubleheadlessdoublehorseman'
enemy_type_doublehorse = 'doublehorse'

# Enemy ai types
enemy_ai_sandbag = 'Sandbag'
enemy_ai_coward = 'Coward'
enemy_ai_attacker_a = 'Attacker-A'
enemy_ai_attacker_b = 'Attacker-B'
enemy_ai_defender = 'Defender'
enemy_ai_gaiaslimeoid = 'Gaiaslimeoid'
enemy_ai_shambler = 'Shambler'

# Enemy classes. For now this is only used for Gankers Vs. Shamblers
enemy_class_normal = 'normal'
enemy_class_gaiaslimeoid = 'gaiaslimeoid'
enemy_class_shambler = 'shambler'

# List of enemies sorted by their spawn rarity.
common_enemies = [enemy_type_sandbag, enemy_type_juvie, enemy_type_dinoslime]
uncommon_enemies = [enemy_type_slimeadactyl, enemy_type_desertraider, enemy_type_mammoslime]
rare_enemies = [enemy_type_microslime, enemy_type_slimeofgreed]
raid_bosses = [enemy_type_megaslime, enemy_type_slimeasaurusrex, enemy_type_greeneyesslimedragon, enemy_type_unnervingfightingoperator]

enemy_movers = [enemy_type_megaslime, enemy_type_slimeasaurusrex, enemy_type_greeneyesslimedragon, enemy_type_unnervingfightingoperator]

# List of enemies that spawn in the Nuclear Beach
pre_historic_enemies = [enemy_type_slimeasaurusrex, enemy_type_dinoslime, enemy_type_slimeadactyl, enemy_type_mammoslime]

# List of enemies used in the Gankers Vs. Shamblers event
gvs_enemies_gaiaslimeoids = [
	enemy_type_gaia_poketubers,
	enemy_type_gaia_pulpgourds,
	enemy_type_gaia_sourpotatoes,
	enemy_type_gaia_bloodcabbages,
	enemy_type_gaia_joybeans,
	enemy_type_gaia_purplekilliflower,
	enemy_type_gaia_razornuts,
	enemy_type_gaia_pawpaw,
	enemy_type_gaia_sludgeberries,
	enemy_type_gaia_suganmanuts,
	enemy_type_gaia_pinkrowddishes,
	enemy_type_gaia_dankwheat,
	enemy_type_gaia_brightshade,
	enemy_type_gaia_blacklimes,
	enemy_type_gaia_phosphorpoppies,
	enemy_type_gaia_direapples,
	enemy_type_gaia_rustealeaves,
	enemy_type_gaia_metallicaps,
	enemy_type_gaia_steelbeans,
	enemy_type_gaia_aushucks
]
gvs_enemies_shamblers = [
	enemy_type_defaultshambler,
	enemy_type_bucketshambler,
	enemy_type_juveolanternshambler,
	enemy_type_flagshambler,
	enemy_type_shambonidriver,
	enemy_type_mammoshambler,
	enemy_type_gigashambler,
	enemy_type_microshambler,
	enemy_type_shamblersaurusrex,
	enemy_type_shamblerdactyl,
	enemy_type_dinoshambler,
	enemy_type_ufoshambler,
	enemy_type_brawldenboomer,
	enemy_type_juvieshambler,
	enemy_type_shambleballplayer,
	enemy_type_shamblerwarlord,
	enemy_type_shamblerraider,
	enemy_type_gvs_boss,
]
gvs_enemies = gvs_enemies_gaiaslimeoids + gvs_enemies_shamblers
repairable_gaias = [
	enemy_type_gaia_blacklimes, 
	enemy_type_gaia_razornuts, 
	enemy_type_gaia_suganmanuts, 
	enemy_type_gaia_steelbeans
]

# List of raid bosses sorted by their spawn rarity.
raid_boss_tiers = {
	"micro": [enemy_type_megaslime],
	"monstrous": [enemy_type_slimeasaurusrex, enemy_type_unnervingfightingoperator],
	"mega": [enemy_type_greeneyesslimedragon],
	# This can be left empty until we get more raid boss ideas.
	#"nega": [],
}

# List of enemies that are simply too powerful to have their rare variants spawn
overkill_enemies = [enemy_type_doubleheadlessdoublehorseman, enemy_type_doublehorse]

# List of enemies that have other enemies spawn with them
enemy_group_leaders = [enemy_type_doubleheadlessdoublehorseman]

# Dict of enemy spawn groups. The leader is the key, which correspond to which enemies to spawn, and how many.
enemy_spawn_groups = {
	enemy_type_doubleheadlessdoublehorseman: [[enemy_type_doublehorse, 1]]
}

# Enemy drop tables. Values are sorted by the chance to the drop an item, and then the minimum and maximum amount of times to drop that item.
enemy_drop_tables = {
	enemy_type_sandbag: [
		{item_id_slimepoudrin: [100, 1, 1]}
	],
	enemy_type_juvie: [
		{item_id_slimepoudrin: [50, 1, 2]}, 
		{rarity_plebeian: [5, 1, 1]}, 
		{"crop": [30, 1, 1]}, 
		{item_id_tradingcardpack: [20, 1, 1]}
	],
	enemy_type_dinoslime: [
		{item_id_slimepoudrin: [100, 2, 4]}, 
		{rarity_plebeian: [10, 1, 1]},  
		{item_id_dinoslimemeat: [33, 1, 2]}, 
		{item_id_monsterbones: [100, 3, 5]}
	],
	enemy_type_slimeadactyl: [
		{item_id_slimepoudrin: [100, 3, 5]}, 
		{rarity_plebeian: [10, 1, 1]}, 
		{item_id_monsterbones: [100, 3, 5]}
	],
	enemy_type_microslime: [
		{rarity_patrician: [100, 1, 1]}
	],
	enemy_type_slimeofgreed: [
		{item_id_slimepoudrin: [100, 2, 2]}
	],
	enemy_type_desertraider: [
		{item_id_slimepoudrin: [100, 1, 2]}, 
		{rarity_plebeian: [50, 1, 1]},  
		{"crop": [50, 3, 6]}
	],
	enemy_type_mammoslime: [
		{item_id_slimepoudrin: [75, 5, 6]},  
		{rarity_patrician: [20, 1, 1]},
		{item_id_monsterbones: [100, 1, 3]}
	],
	enemy_type_doubleheadlessdoublehorseman: [
		{item_id_slimepoudrin: [100, 22, 22]}, 
		{rarity_plebeian: [100, 22, 22]}, 
		{rarity_patrician: [100, 22, 22]}, 
		{"crop": [100, 22, 22]}, 
		{item_id_dinoslimemeat: [100, 22, 22]}, 
		{item_id_tradingcardpack: [100, 22, 22]}
	],
	enemy_type_doublehorse: [
		{item_id_slimepoudrin: [100, 22, 22]}
	],
	enemy_type_megaslime: [
		{item_id_slimepoudrin: [100, 4, 8]}, 
		{rarity_plebeian: [80, 1, 2]}, 
		{rarity_patrician: [30, 1, 1]}
	],
	enemy_type_slimeasaurusrex: [
		{item_id_slimepoudrin: [100, 8, 15]}, 
		{rarity_plebeian: [50, 1, 2]}, 
		{rarity_patrician: [20, 1, 2]},  
		{item_id_dinoslimemeat: [100, 3, 4]}, 
		{item_id_monsterbones: [100, 3, 5]}
	],
	enemy_type_greeneyesslimedragon: [
		{item_id_dragonsoul: [100, 1, 1]},
		{item_id_slimepoudrin: [100, 15, 20]}, 
		{rarity_patrician: [100, 1, 1]}, 
		{item_id_monsterbones: [100, 5, 10]}
	],
	enemy_type_unnervingfightingoperator: [
		{item_id_slimepoudrin: [100, 1, 1]}, 
		{"crop": [100, 1, 1]}, 
		{item_id_dinoslimemeat: [100, 1, 1]}, 
		{item_id_tradingcardpack: [100, 1, 1]}
	],
	enemy_type_civilian: [
		{item_id_slimepoudrin: [20, 1, 1]},
		{item_id_civilianscalp: [100, 1, 1]},
	],
	enemy_type_civilian_innocent: [
		{item_id_slimepoudrin: [20, 1, 1]},
		{item_id_civilianscalp: [100, 1, 1]},
	],
}
for enemy in gvs_enemies:
	enemy_drop_tables[enemy] = [{item_id_slimepoudrin: [100, 1, 1]}]

# When making a new enemy, make sure to fill out slimerange, ai, attacktype, displayname, raredisplayname, and aliases.
# Enemy data tables. Slime is stored as a range from min to max possible slime upon spawning.
enemy_data_table = {
	enemy_type_sandbag: {
		"slimerange": [1000000000, 1000000000], 
		"ai": enemy_ai_sandbag, 
		"attacktype": enemy_attacktype_unarmed, 
		"displayname": "Sand Bag", 
		"raredisplayname": "Durable Sand Bag", 
		"aliases": ["sandbag", "bag o sand", "bag of sand"]
	},
	enemy_type_juvie: {
		"slimerange": [10000, 50000],
		"ai": enemy_ai_coward, "attacktype": enemy_attacktype_unarmed, 
		"displayname": "Lost Juvie", 
		"raredisplayname": "Shellshocked Juvie", 
		"aliases": ["juvie","greenman","lostjuvie", "lost"]
	},
	enemy_type_dinoslime: {
		"slimerange": [250000, 500000], 
		"ai": enemy_ai_attacker_a, 
		"attacktype": enemy_attacktype_fangs, 
		"displayname": "Dinoslime", 
		"raredisplayname": "Voracious Dinoslime", 
		"aliases": ["dino","slimeasaur"]
	},
	enemy_type_slimeadactyl: {
		"slimerange": [500000, 750000], 
		"ai": enemy_ai_attacker_b, 
		"attacktype": enemy_attacktype_talons, 
		"displayname": "Slimeadactyl", 
		"raredisplayname": "Predatory Slimeadactyl", 
		"aliases": ["bird","dactyl"]
	},
	enemy_type_desertraider: {
		"slimerange": [250000, 750000], 
		"ai": enemy_ai_attacker_b, 
		"attacktype": enemy_attacktype_raiderscythe, 
		"displayname": "Desert Raider", 
		"raredisplayname": "Desert Warlord", 
		"aliases": ["raider","scytheboy","desertraider", "desert"]
	},
	enemy_type_mammoslime: {
		"slimerange": [650000, 950000],
		"ai": enemy_ai_defender, 
		"attacktype": enemy_attacktype_tusks, 
		"displayname": "Mammoslime", 
		"raredisplayname": "Territorial Mammoslime", 
		"aliases": ["mammoth","brunswick"]
	},
	enemy_type_microslime: {
		"slimerange": [10000, 50000], 
		"ai": enemy_ai_defender, 
		"attacktype": enemy_attacktype_body, 
		"displayname": "Microslime", 
		"raredisplayname": "Irridescent Microslime", 
		"aliases": ["micro","pinky"]
	},
	enemy_type_slimeofgreed: {
		"slimerange": [20000, 100000], 
		"ai": enemy_ai_defender, 
		"attacktype": enemy_attacktype_body, 
		"displayname": "Slime Of Greed", 
		"raredisplayname": "Slime Of Avarice", 
		"aliases": ["slime","slimeofgreed","pot","potofgreed","draw2cards"]
	},
	enemy_type_doubleheadlessdoublehorseman: {
		"slimerange": [100000000, 150000000], 
		"ai": enemy_ai_attacker_b, 
		"attacktype": enemy_attacktype_axe, 
		"displayname": "Double Headless Double Horseman", 
		"raredisplayname": "Quadruple Headless Quadruple Horseman", 
		"aliases": ["doubleheadlessdoublehorseman", "headlesshorseman", "demoknight", "horseman"]
	},
	enemy_type_doublehorse: {
		"slimerange": [50000000, 75000000], 
		"ai": enemy_ai_attacker_a, 
		"attacktype": enemy_attacktype_hooves, 
		"displayname": "Double Headless Double Horseman's Horse", 
		"raredisplayname": "Quadruple Headless Quadruple Horseman's Horse", 
		"aliases": ["doublehorse", "horse", "pony", "lilbit"]
	},
	enemy_type_megaslime: {
		"slimerange": [1000000, 1000000], 
		"ai": enemy_ai_attacker_a, 
		"attacktype": enemy_attacktype_gunkshot, 
		"displayname": "Megaslime", 
		"raredisplayname": "Rampaging Megaslime", 
		"aliases": ["mega","smooze","muk"]
	},
	enemy_type_slimeasaurusrex: {
		"slimerange": [1750000, 3000000], 
		"ai": enemy_ai_attacker_b, 
		"attacktype": enemy_attacktype_fangs, 
		"displayname": "Slimeasaurus Rex", 
		"raredisplayname": "Sex Rex", 
		"aliases": ["rex","trex","slimeasaurusrex","slimeasaurus"]
	},
	enemy_type_greeneyesslimedragon: {
		"slimerange": [3500000, 5000000], 
		"ai": enemy_ai_attacker_a, 
		"attacktype": enemy_attacktype_molotovbreath, 
		"displayname": "Green Eyes Slime Dragon", 
		"raredisplayname": "Green Eyes JPEG Dragon", 
		"aliases": ["dragon","greeneyes","greeneyesslimedragon","green"]
	},
	enemy_type_unnervingfightingoperator: {
		"slimerange": [1000000, 3000000],
		"ai": enemy_ai_attacker_b,
		"attacktype": enemy_attacktype_armcannon,
		"displayname": "Unnerving Fighting Operator",
		"raredisplayname": "Unyielding Fierce Operator",
		"aliases": ["ufo", "alien","unnervingfightingoperator","unnvering"]
	},
enemy_type_civilian: {
		"slimerange": [100001, 100001],
		"ai": enemy_ai_attacker_a,
		"attacktype": enemy_attacktype_amateur,
		"displayname": "Bloodthirsty Civilian",
		"raredisplayname": "Closet Serial Killer",
		"aliases": ["townsfolk", "citizen","civilian","bloodthirsty", "person"]
	},
enemy_type_civilian_innocent: {
		"slimerange": [100001, 100001],
		"ai": enemy_ai_defender,
		"attacktype": enemy_attacktype_amateur,
		"displayname": "Innocent Civilian",
		"raredisplayname": "Puppy-Eyed Youth",
		"aliases": ["townsfolk", "citizen","civilian","innocent", "person"]
	},
	enemy_type_gaia_poketubers: {
		"slimerange": [100, 100],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_gvs_g_explosion,
		"displayname": "Poketuber",
		"raredisplayname": "Joybean Poketuber",
		"aliases": ['tuber'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'primed': 'false',
			'primecountdown': 3,
			'setdamage': 500000,
			'piercing': 'true',
			'range': 2
		}
	},
	enemy_type_gaia_pulpgourds: {
		"slimerange": [50000, 50000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_unarmed,
		"displayname": "Pulp Gourd",
		"raredisplayname": "Joybean Pulp Gourd",
		"aliases": ['gourd', 'pulp'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'gourdstorage': 0
		}
	},
	enemy_type_gaia_sourpotatoes: {
		"slimerange": [100000, 100000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_gvs_g_chompers,
		"displayname": "Sour Potato",
		"raredisplayname": "Joybean Sour Potato",
		"aliases": ['potato', 'sour'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'chewingcountdown': 0,
			'setdamage': 500000,
			'range': 2
		}
	},
	enemy_type_gaia_bloodcabbages: {
		"slimerange": [100000, 100000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_gvs_g_bloodshot,
		"displayname": "Blood Cabbage",
		"raredisplayname": "Joybean Blood Cabbage",
		"aliases": ['blood', 'cabbage'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'setdamage': 20000,
			'range': 20,
			'piercing': 'true',
			'pierceamount': 3
		}
	},
	enemy_type_gaia_joybeans: {
		"slimerange": [500000, 500000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_unarmed,
		"displayname": "Joybean",
		"raredisplayname": "Joybean Fusion!!",
		"aliases": ['bean','uhoh','youfriccinmoron'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'noprop': 'noprop'
		}
	},
	enemy_type_gaia_purplekilliflower: {
		"slimerange": [100000,100000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_gvs_g_vapecloud,
		"displayname": "Purple Killiflower",
		"raredisplayname": "Joybean Purple Killiflower",
		"aliases": ['purple','killiflower','cauliflower'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'range': 12,
			'piercing': 'true',
			'setdamage': '15000',
		}
	},
	enemy_type_gaia_razornuts: {
		"slimerange": [200000, 200000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_unarmed,
		"displayname": "Razornut",
		"raredisplayname": "Joybean Razornut",
		"aliases": ['razor', 'nut'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'setdamage': 20000
		}
	},
	enemy_type_gaia_pawpaw: {
		"slimerange": [200000, 200000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_gvs_g_explosion,
		"displayname": "Pawpaw",
		"raredisplayname": "Joybean Pawpaw",
		"aliases": ['paw'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'setdamage': 500000,
			'direction': 'ring',
			'splash': 'true'
		}
	},
	enemy_type_gaia_sludgeberries: {
		"slimerange": [100, 100],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_unarmed,
		"displayname": "Sludgeberries",
		"raredisplayname": "Joybean Sludgeberries",
		"aliases": ['berries','sludge'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'noprop': 'noprop'
		}
	},
	enemy_type_gaia_suganmanuts: {
		"slimerange": [400000, 400000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_unarmed, # changes to gvs_g_nuts upon the use of a joybean
		"displayname": "Suganmanut",
		"raredisplayname": "Joybean Suganmanut",
		"aliases": ['cashew', 'nuts'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'setdamage': 20000
		}
	},
	enemy_type_gaia_pinkrowddishes: {
		"slimerange": [100000, 100000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_gvs_g_fists,
		"displayname": "Pink Rowddish",
		"raredisplayname": "Joybean Pink Rowddish",
		"aliases": ['rowddish', 'raddish'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'range': 3,
			'direction': 'frontandback',
			'piercing': 'true',
			'setdamage': 50000
		}
	},
	enemy_type_gaia_dankwheat: {
		"slimerange": [50000, 50000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_gvs_g_hotbox,
		"displayname": "Dankwheat",
		"raredisplayname": "Joybean Dankwheat",
		"aliases": ['weed','digiweed','digibro','wheat'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'setdamage': 10000,
			'direction': 'ring',
			'piercing': 'true',
		}
	},
	enemy_type_gaia_brightshade: {
		"slimerange": [50000, 50000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_unarmed,
		"displayname": "Brightshade",
		"raredisplayname": "Double Brightshade",
		"aliases": ['bright','shade'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'gaiaslimecountdown': 2
		}
	},
	enemy_type_gaia_blacklimes: {
		"slimerange": [200000, 200000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_unarmed,
		"displayname": "Black Lime",
		"raredisplayname": "Joybean Black Lime",
		"aliases": ['lime','black'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'noprop': 'noprop'
		}
	},
	enemy_type_gaia_phosphorpoppies: {
		"slimerange": [100000, 100000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_gvs_g_brainwaves,
		"displayname": "Phosphorpoppy",
		"raredisplayname": "Joybean Phosphorpoppy",
		"aliases": ['phosphor', 'poppy'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'setdamage': 10000,
			'piercing': 'true',
			'pierceamount': 3
		}
	},
	enemy_type_gaia_direapples: {
		"slimerange": [100000, 100000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_gvs_g_seeds,
		"displayname": "Dire Apple",
		"raredisplayname": "Joybean Dire Apple",
		"aliases": ['apple','dire'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'setdamage': 35000,
			'splash': 'false'
			# 'singletilepierce': 'true', JOYBEAN 
			# 'pierceamount': 3
		}
	},
	enemy_type_gaia_rustealeaves: {
		"slimerange": [200000, 200000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_gvs_g_blades,
		"displayname": "Rustea Leaves",
		"raredisplayname": "Joybean Rustea Leaves",
		"aliases": ['leaves','tea'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'range': 1,
			'direction': 'frontandback',
			'setdamage': 30000
		}
	},
	enemy_type_gaia_metallicaps: {
		"slimerange": [500000, 500000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_unarmed,
		"displayname": "Metallicaps",
		"raredisplayname": "NULL",
		"aliases": ['mushrooms','shrooms','shroomz','mushroom'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			#'setdamage': 30000
			'noprop': 'noprop'
		}
	},
	enemy_type_gaia_steelbeans: {
		"slimerange": [200000, 200000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_unarmed,
		"displayname": "Steel Beans",
		"raredisplayname": "NULL",
		"aliases": ['911','steel','beans'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			'noprop': 'noprop'
		}
	},
	enemy_type_gaia_aushucks: {
		"slimerange": [500000, 500000],
		"ai": enemy_ai_gaiaslimeoid,
		"attacktype": enemy_attacktype_unarmed,
		"displayname": "Aushucks",
		"raredisplayname": "NULL",
		"aliases": ['gold','shucks','corn'],
		"class": enemy_class_gaiaslimeoid,
		"props": {
			#'gaiaslimecountdown': 4
			'noprop': 'noprop'
		}
	},
	enemy_type_defaultshambler: {
		"slimerange": [125000, 125000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_teeth,
		"displayname": "Default Shambler",
		"raredisplayname": "NULL",
		"aliases": ['zombie'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 30000
		}
	},
	enemy_type_bucketshambler: {
		"slimerange": [175000, 175000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_teeth,
		"displayname": "KFC Bucket Shambler",
		"raredisplayname": "NULL",
		"aliases": ['kfc','bucket'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 30000
		}
	},
	enemy_type_juveolanternshambler: {
		"slimerange": [250000, 250000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_teeth,
		"displayname": "Juve-O'-Lantern Shambler",
		"raredisplayname": "NULL",
		"aliases": ['juveolantern','jackolantern'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 30000
		}
	},
	enemy_type_flagshambler: {
		"slimerange": [125000, 125000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_teeth,
		"displayname": "Flag Shambler",
		"raredisplayname": "NULL",
		"aliases": ['flag'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 30000
		}
	},
	enemy_type_shambonidriver: {
		"slimerange": [175000, 175000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_shamboni,
		"displayname": "Shamboni Driver",
		"raredisplayname": "NULL",
		"aliases": ['zomboni', 'driver', 'zamboni'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 250000
		}
	},
	enemy_type_mammoshambler: {
		"slimerange": [250000, 250000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_tusks,
		"displayname": "Mammoshambler",
		"raredisplayname": "NULL",
		"aliases": ['mammoth','brunswick'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 100000,
			'turncountdown': 2
		}
	},
	enemy_type_gigashambler: {
		"slimerange": [500000, 500000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_cudgel,
		"displayname": "Gigashambler",
		"raredisplayname": "NULL",
		"aliases": ['giga','gigachad'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 200000,
			'turncountdown': 2,
			'microspawned': 'false'
		}
	},
	enemy_type_microshambler: {
		"slimerange": [60000, 60000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_teeth,
		"displayname": "Microshambler",
		"raredisplayname": "NULL",
		"aliases": ['micro'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 30000
		}
	},
	enemy_type_shamblersaurusrex: {
		"slimerange": [250000, 250000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_fangs,
		"displayname": "Shamblersaurus Rex",
		"raredisplayname": "NULL",
		"aliases": ['rex','trex','t-rex','shamblersaurus'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 75000,
			'roarused': False,
		}
	},
	enemy_type_shamblerdactyl: {
		"slimerange": [100000, 100000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_talons,
		"displayname": "Shamblerdactyl",
		"raredisplayname": "NULL",
		"aliases": ['bird','dactyl'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 2000000,
			'grabcountdown': 3
		}
	},
	enemy_type_dinoshambler: {
		"slimerange": [150000, 150000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_fangs,
		"displayname": "Dinoshambler",
		"raredisplayname": "NULL",
		"aliases": ['dinosaur','dino'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 35000,
			'jumping': 'true'
		}
	},
	enemy_type_ufoshambler: {
		"slimerange": [150000, 150000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_grenadecannon,
		"displayname": "Unnerving Fighting Shambler",
		"raredisplayname": "NULL",
		"aliases": ['ufo'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 40000,
			'turncountdown': 2,
			'range': 18
		}
	},
	enemy_type_brawldenboomer: {
		"slimerange": [100000, 100000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_teeth,
		"displayname": "The Brawlden Boomer",
		"raredisplayname": "Enraged Brawlden Boomer",
		"aliases": ['boomer','boombox'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 30000,
			'turncountdown': 2,
			'boomboxcountdown': 12,
			'boomboxbroken': 'false',
			'boomboxhealth': 100000
		}
	},
	enemy_type_juvieshambler: {
		"slimerange": [150000, 150000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_teeth,
		"displayname": "Juvie Shambler",
		"raredisplayname": "NULL",
		"aliases": ['juvie','miner'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 40000,
			'underground': 'true'
		}
	},
	enemy_type_shambleballplayer: {
		"slimerange": [250000, 250000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_teeth,
		"displayname": "Shambleball Player",
		"raredisplayname": "NULL",
		"aliases": ['soccerguy','football','sports'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 40000
		}
	},
	enemy_type_shamblerwarlord: {
		"slimerange": [300000, 300000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_raiderscythe,
		"displayname": "Shambler Warlord",
		"raredisplayname": "NULL",
		"aliases": ['warlord'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 60000,
			'summoncountdown': 3 # When it reaches 0, it is dialed back to 6
		}
	},
	enemy_type_shamblerraider: {
		"slimerange": [100000, 100000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_gvs_s_raiderscythe,
		"displayname": "Shambler Raider",
		"raredisplayname": "NULL",
		"aliases": ['raider'],
		"class": enemy_class_shambler,
		"props": {
			'setdamage': 30000
		}
	},
	enemy_type_gvs_boss: {
		"slimerange": [5000000, 5000000],
		"ai": enemy_ai_shambler,
		"attacktype": enemy_attacktype_unarmed,
		"displayname": "PLACEHOLDER",
		"raredisplayname": "NULL",
		"aliases": ['placeholder'],
		"class": enemy_class_shambler,
		"props": {
			'onground': 'true',
			'setdamage': 100000
		}
	},
}

# Raid boss names used to avoid raid boss reveals in ewutils.formatMessage
raid_boss_names = []
for enemy in enemy_data_table.keys():
	if enemy in raid_bosses:
		raid_boss_names.append(enemy_data_table[enemy]["displayname"])
		raid_boss_names.append(enemy_data_table[enemy]["raredisplayname"])

# Responses given by cowardly enemies when a non-ghost user is in their district.
coward_responses = [
	"The {} calls out to you: *H-Hello. Are you one of those Gangsters everyone seems to be talking about?*",
	"The {} calls out to you: *You wouldn't hurt a {}, would you?*",
	"The {} calls out to you: *Why.. uh.. hello there? What brings you to these parts, stranger?*",
	"The {} calls out to you: *L-look at how much slime I have! I'm not even worth it for you to kill me!*",
	"The {} calls out to you: *I'm just a good little {}... never hurt nobody anywhere...*",
]

# Responses given by cowardly enemies when hurt.
coward_responses_hurt = [
	"\nThe {} cries out in pain!: *Just wait until the Juvenile Enrichment Center hears about this!!*",
	"\nThe {} cries out in pain!: *You MONSTER!*",
	"\nThe {} cries out in pain!: *What the H-E-double-hockey-sticks is your problem?*",
]

# Letters that an enemy can identify themselves with
identifier_letters = [
	'A', 'B', 'C', 'D', 'E',
	'F', 'G', 'H', 'I', 'J',
	'K', 'L', 'M', 'N', 'O',
	'P', 'Q', 'R', 'S', 'T',
	'U', 'V', 'W', 'X', 'Y', 'Z'
]

gvs_valid_coords_gaia = [
	['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
	['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'],
	['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
	['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'],
	['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9']
]

gvs_valid_coords_shambler = [
	['A0', 'A0.5', 'A1', 'A1.5', 'A2', 'A2.5', 'A3', 'A3.5', 'A4', 'A4.5', 'A5', 'A5.5', 'A6', 'A6.5', 'A7', 'A7.5', 'A8', 'A8.5', 'A9', 'A9.5', 'A-S'],
	['B0', 'B0.5', 'B1', 'B1.5', 'B2', 'B2.5', 'B3', 'B3.5', 'B4', 'B4.5', 'B5', 'B5.5', 'B6', 'B6.5', 'B7', 'B7.5', 'B8', 'B8.5', 'B9', 'B9.5', 'B-S'],
	['C0', 'C0.5', 'C1', 'C1.5', 'C2', 'C2.5', 'C3', 'C3.5', 'C4', 'C4.5', 'C5', 'C5.5', 'C6', 'C6.5', 'C7', 'C7.5', 'C8', 'C8.5', 'C9', 'C9.5', 'C-S'],
	['D0', 'D0.5', 'D1', 'D1.5', 'D2', 'D2.5', 'D3', 'D3.5', 'D4', 'D4.5', 'D5', 'D5.5', 'D6', 'D6.5', 'D7', 'D7.5', 'D8', 'D8.5', 'D9', 'D9.5', 'D-S'],
	['E0', 'E0.5', 'E1', 'E1.5', 'E2', 'E2.5', 'E3', 'E3.5', 'E4', 'E4.5', 'E5', 'E5.5', 'E6', 'E6.5', 'E7', 'E7.5', 'E8', 'E8.5', 'E9', 'E9.5', 'E-S']
]

gvs_coords_end = ['A0', 'B0', 'C0', 'D0', 'E0']

gvs_coords_start = ['A-S', 'B-S', 'C-S', 'D-S', 'E-S']

gvs_enemy_emote_map = {
	enemy_type_gaia_poketubers: emote_poketubers,
	enemy_type_gaia_pulpgourds: emote_pulpgourds,
	enemy_type_gaia_sourpotatoes: emote_sourpotatoes,
	enemy_type_gaia_bloodcabbages: emote_bloodcabbages,
	enemy_type_gaia_joybeans: emote_joybeans,
	enemy_type_gaia_purplekilliflower: emote_killiflower,
	enemy_type_gaia_razornuts: emote_razornuts,
	enemy_type_gaia_pawpaw: emote_pawpaw,
	enemy_type_gaia_sludgeberries: emote_sludgeberries,
	enemy_type_gaia_suganmanuts: emote_suganmanuts,
	enemy_type_gaia_pinkrowddishes: emote_pinkrowddishes,
	enemy_type_gaia_dankwheat: emote_dankwheat,
	enemy_type_gaia_brightshade: emote_brightshade,
	enemy_type_gaia_blacklimes: emote_blacklimes,
	enemy_type_gaia_phosphorpoppies: emote_phosphorpoppies,
	enemy_type_gaia_direapples: emote_direapples,
	enemy_type_gaia_rustealeaves: emote_rustealeaves,
	enemy_type_gaia_metallicaps: emote_metallicaps,
	enemy_type_gaia_steelbeans: emote_steelbeans,
	enemy_type_gaia_aushucks: emote_aushucks,
	'frozen': emote_frozentile,
}

gvs_enemy_emote_map_debug = {
	enemy_type_gaia_poketubers: ':potato:',
	enemy_type_gaia_pulpgourds: ':lemon:',
	enemy_type_gaia_sourpotatoes: ':sweet_potato:',
	enemy_type_gaia_bloodcabbages: ':tomato:',
	enemy_type_gaia_joybeans: ':rainbow:',
	enemy_type_gaia_purplekilliflower: ':broccoli:',
	enemy_type_gaia_razornuts: ':chestnut:',
	enemy_type_gaia_pawpaw: ':pear:',
	enemy_type_gaia_sludgeberries: ':grapes:',
	enemy_type_gaia_suganmanuts: ':peanuts:',
	enemy_type_gaia_pinkrowddishes: ':strawberry:',
	enemy_type_gaia_dankwheat: ':herb:',
	enemy_type_gaia_brightshade: ':hibiscus:',
	enemy_type_gaia_blacklimes: ':garlic:',
	enemy_type_gaia_phosphorpoppies: ':blossom:',
	enemy_type_gaia_direapples: ':apple:',
	enemy_type_gaia_rustealeaves: ':fallen_leaf:',
	enemy_type_gaia_metallicaps: ':mushroom:',
	enemy_type_gaia_steelbeans: ':shield:',
	enemy_type_gaia_aushucks: ':corn:',
	'frozen': ':snowflake:',
}

gvs_almanac = {
	enemy_type_gaia_poketubers: 'Poketubers are mines that deal massive damage when a shambler tries to attack one of them. However, they must take 15 seconds to prime beforehand, otherwise they\'re sitting ducks. When given a Joybean, they will entrench their roots into the ground ahead of them, spawning more fully primed poketubers in random locations ahead of it.\nPoketuber used to be a big shot. His analysis channel with Dire Apples was the talk of the town, even getting big shots like Aushucks to turn their heads in amazement. Nowadays though, he\'s washed up, and has to shill his patreon just to get by. "God, just fucking step on me already and end it all", Poketuber thinks to himself every day.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743641434841808967/poketubers_seedpacket.png',
	enemy_type_gaia_pulpgourds: 'Gaiaslimeoids anywhere on the field can drink out of Pulp Gourds, replenishing their HP and draining that Pulp Gourd\'s storage in the process. Pulp Gourds can only be refilled by Blood Cabbages. When given a Joybean, their healing effect is doubled.\nPulp Gourd is the faithful and humble servant of Blood Cabbage, aiding her in her experiments. "I would sooner walk into the fires of Hell than see a wound on your leaves, Miss Cabbage", says Pulp Gourd. "Ohohoho~, you spoil me, sir Gourd", replies Blood Cabbage. Other Gaiaslimeoids aren\'t sure what the nature of their relationship is, and frankly it weirds them out a bit.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743258076152332339/pulpgourds_seedpacket.png',
	enemy_type_gaia_sourpotatoes: 'Sour Potatoes are a great front-line attacker for any Garden Op. They can\'t dish out constant damage like a Pink Rowddish, but they make up for it by swallowing almost any shambler in front of it whole, killing it instantly. This immobilizes the Sour Potato for 10 seconds, however, leaving it vulnerable to attacks. When given a Joybean, they can launch out a ball of fire, which melts away the frozen slime trail left by Shambonis, in addition to dealing a fair amount of splash damage.\nIn a twist of fate, Sour Potatoes have turned into a popular pet across NLACakaNM. This is in opposition of the fact that Sour Potatoes are sentient, and aware of their own domestication. "Awww, who\'s a cute widdle doggy", a Juvenile says. "I can speak English you know. I\'m forming proper sentences, for fucks sake. Treat me with some dignity, *please*", says Sour Potato.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241053598908466/sourpotatoes_seedpacket.png',
	enemy_type_gaia_bloodcabbages: 'Attacks coming from a Blood Cabbage are relatively weak compared to their Rowddish and Killiflower cohorts, but they have a special effect of draining health from enemy shamblers and redistributing it to their allies. They cannot heal themselves, however. When given a Joybean, their attacks will deal twice as much damage, and heal twice as much as a result. They can heal any Gaiaslimeoid within range, but will prioritize those that are low on health, saving Pulp Gourds for last.\nBlood Cabbage\'s obsession with the dark arts led her down an equally dark path in life. After pouring over countless forbidden tomes, she had found what she had been seeking, and used the hordes of undead Shamblers as her test subjects to measure her abilities. "Ahahaha... what a discovery! This ability will prove to be useful... whether my allies like it or not!"\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241003779227718/bloodcabbages_seedpacket.png',
	enemy_type_gaia_joybeans: 'Joybeans act as an upgrade to other Gaiaslimeoids. They can either be planted onto blank tiles and used later when combined with other Gaiaslimeoids, or they can be planted on top of other Gaiaslimeoids. If two Joybeans combine, they explode into a fountain of sheer ecstasy, activating the Joybean effects of all Gaiaslimeoids within a short radius for 30 seconds. It is consumed upon use.\nJoybean is very excitable. When in the presence of another Gaiaslimeoid, she can\'t help but start hyperventilating at the thought of being near them, and is frequently unable to contain herself. "Kyaaaaaa~!" Joybean cries out, as she glomps onto fellow Gaiaslimeoids.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241010506891374/joybeans_seedpacket.png',
	enemy_type_gaia_purplekilliflower: 'Purple Killiflowers shoot out toxic vape clouds when they !dab. This allows them to target shamblers up to 6 tiles in front of them, piercing multiple Shamblers in the process. When given a Joybean, it will deal twice as much damage.\n"Fuck you Dad! It\'s called The Vapors, and it\'s way better than any shitty comic book you\'ve ever read! God, I HATE YOU!", says Killiflower, as he slams the door shut behind him. Choking back tears, he mutters to himself: "Don\'t let him see you cry..."\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241012104921098/killiflower_seedpacket.png',
	enemy_type_gaia_razornuts: 'Razornuts aren\'t as hard or long as Suganmanuts, but their sharpened edges will harm any Shambler that tries to attack it. If a Razornut is damaged, you can !plant another one on top of it to repair it. When given a Joybean, its death will cause an explosion of shrapnel, dealing a fair amount of damage within a large radius around it.\nWhen a Shambler bites into Razornut, he doesn\'t care. He lets it happen, just to *feel* something. "Go on, give me your best. You aren\'t half as strong as the thugs I\'ve mauled in the past", says Razonut. "This shell right here, it\'s ready for the apocalypse.", he continues.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241045348843530/razornuts_seedpacket.png',
	enemy_type_gaia_pawpaw: 'When planted, a Pawpaw will explode after a short amount of time, dealing massive damage in a small radius. If a Pawpaw is planted on top of a Joybean, this will increase its range significantly.\nPawpaw has been places and seen shit you would not believe. The guilt of his war crimes will be taken with him to the grave. "It\'s a good day to die.", says Pawpaw.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743258148239966308/pawpaw_seedpacket.png',
	enemy_type_gaia_sludgeberries: 'Sludgeberries are a Gaiaslimeoid that will detonate into a sticky and immobilizing sludge, inflicting a stun effect on all shamblers within a short range. When given a Joybean, it will cover all Shamblers on the field in this sludge.\nThese Gaiaslimeoids are all the craze over at Pyrope Farms. "UM, G4RD3N G4NK3RS? SORRY, BUT W3 ONLY WORK UND3R DIR3CT ORD3RS FROM T3R3Z1 G4NG", says Sludgeberry.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241051401224192/sludgeberries_seedpacket.png',
	enemy_type_gaia_suganmanuts: 'Suganmanuts\' large health pool allows it to provide a great amount of defensive utility in battle. If a Suganmanut is damaged, you can !plant another one on top of it to repair it. When given a Joybean, it will occasionally spit out its nut, ricocheting off of shamblers.\n"I swear I\'m not gay" says Suganmanuts. "I just like the taste". The look in his eye told a different story, however. That, and the 50 tabs of Grimedr he had open.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743240999492649071/suganmanuts_seedpacket.png',
	enemy_type_gaia_pinkrowddishes: 'Pink Rowddishes attack by !thrash-ing about, dealing massive damage to all Shamblers within a short range in front of them. They can attack behind themselves as well. When given a Joybean, it will begin to violently scream. These screams act as an increase to its range, reaching three times as far as a basic attack.\nRowddishes are hot-blooded and looking to brawl. Though they have no eyes, they make up for it with intense reflexes. In some instances, they will even go as far as to lash out at the Garden Gankers who have planted them. "Back off, Juvie!", says Rowddish. "Unless you want me to turn you into a knuckle sandwich! Ha! Up-five", he says as he hi-fives himself. Even when there are no Shamblers around, Rowddishes will continue to pick fights with each other, frequently engaging in what are known as "No Hard Feelings Civil Wars".\nhttps://cdn.discordapp.com/attachments/743240814250950678/743258274761015326/pinkrowddish_seedpacket.png',
	enemy_type_gaia_dankwheat: 'Dankwheat tend to be a utility-focussed Gaiaslimeoid, dealing minimal damage, but whatever does enter their short attack radius that surrounds them will be slowed down by a status effect. When given a Joybean, it can reach further in front and in back of it for targets, and the status effect will also lower the damage output of its targets.\n"Dude, what\'s a text command?" one stalk of Dankwheat says. "Dude, what GAME are we even IN right now??", another adds. "Guys, wait, hold on, my seaweed joint is running out, can one of you spot me?", the third one chimes in. These guys can never seem to get their fucking heads straight, outside of the 22 minutes every Saturday that a new MLP episode is on the air.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241007025488023/dankwheat_seedpacket.png',
	enemy_type_gaia_brightshade: 'Brightshades are an essential plant to have in any Garden Op. They provide Garden Gankers with precious gaiaslime, at a rate of 25 gaiaslime every 20 seconds. When given a Joybean, this output is doubled in effectiveness.\nIn her past, Brightshade was a beautiful singer, frequently selling out even to large crowds. When the Shamblers came to town, she decided to put her career on hold, however. She is a shining gem among Gaiaslimeoids, revered and loved by all, and by some, perhaps a bit too much...\n"I just got this Brightshade poster off of Amoozeon, and oh my fucking God, you can see her TITS."\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241005406486658/brightshade_seedpacket.png',
	enemy_type_gaia_blacklimes: 'When a Black Lime gets bitten, its sour taste will repulse the shambler and redirect it to a different lane entirely. If a Black Lime is damaged, you can !plant another one on top of it to repair it. When given a Joybean, it will shoot out a damaging stream of lime juice, shuffling all shamblers within its lane, and it will also be healed fully.\nOther Gaiaslimeoids worry about Black Lime... what he might do, who he might become. They only hang out with him as a preventative measure. "He\'s... he\'s just different, you know?", says Brightshade as she watches Black Lime brutally torture disease-infested rodents from a safe distance.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241002319347873/blacklimes_seedpacket.png',
	enemy_type_gaia_phosphorpoppies: 'Phosphorpoppies will give Shamblers a \'bad trip\' when it shoots out its Binaural Brainwaves, or when it gets eaten. This will cause Shamblers to either hit, miss, or backfire in their attacks. When given a Joybean, its Binaural Brainwaves will inflict this effect 100% of the time, otherwise the effect only has a chance to be inflicted.\nPhosphoroppy is a total klutz, but she tries her best. Her simple-minded innocence led to her becoming a fan-favorite among many of the Garden Gankers, but behind those swirly eyes remains a horrible tragedy. A psychadelic experience aided by one of the Dankwheat brothers caused her to overload and see things no Gaiaslimeoid was meant to see. It fractured her mind, but her heart is still in there, ready to take on the Shamblers with everything she\'s got.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743258227696730152/phosphorpoppies_seedpacket.png',
	enemy_type_gaia_direapples: 'Dire apples are a vital Gaiaslimeoid to have in any offensive setup. They can lob globules of acid or spit bullet seeds. When given a Joybean, their seed attacks will do more damage and will inflict an acidic burn on whatever shamblers it manages to hit.\n"How does a Gaiaslimeoid like me make the best of both worlds collide? Well, I could tell you, but I\'ve got a BIG meeting to catch." He speeds away in his sports car occupied by himself and several Phosphorpoppies. Only a puff of smoke is left behind.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241008828907660/direapples_seedpacket.png',
	enemy_type_gaia_rustealeaves: 'Rustea Leaves are a grounded Gaiaslimeoid, and can attack only within a very short range of where they are planted. They are completely immune to conventional methods of Shambler offense, however, only being damaged by Gigashamblers, Shambonis, and UFO Shamblers. They can be planted on any tile, provided it\'s not already occupied by another Rustea Leaves. When given a Joybean, they will receive a significant boost in both health and damage output.\nRustea Leaves are the amalgamation of leftover shavings off of other metallic crops, culminating into one fearsome Gaiaslimeoid. He is the forgotten fourth member of the Metal Crop Bros, but despite all this, he manages to maintain a positive attitude. "You gotta work with tha hand yah dealt", he says. "These shamblahs ain\'t gonna moida themselves." Regardless of what he says though, he\'s still bitter about not being invited to the family reunion.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241049073254460/rustealeaves_seedpacket.png',
	enemy_type_gaia_metallicaps: 'Metallicaps are a metallic upgrade Gaiaslimeoid, meaning that it can be planted on any tile, provided that a Steel Bean or Aushuck is not already occupying that tile. When planted on top of an attacking Gaiaslimeoid, it will provide a boost in damage, as well as an additional amount of damage in the form of a spores effect, which burns away the health of enemy shamblers. It cannot be given a Joybean. It is consumed upon use, much like a Joybean.\nMetallicap is a rebellious youth, and the youngest member of the Metal Crop Bros. His affinity for metal music drives his other brothers up the goddamn wall, given how often he will throw parties over at the house and blast his music through his custom-made boombox. "Rules? HA! There\'s only one rule in this house brah, and that is, *TO GET DOWN AND PARTY!!!*", he says.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241014118187059/metallicaps_seedpacket.png',
	enemy_type_gaia_steelbeans: 'Steel Beans are a metallic upgrade Gaiaslimeoid, meaning that it can be planted on any tile, provided that a Metallicap or Aushuck is not already occupying that tile. When planted on top of a gaiaslimeoid, it will act as an additional layer of health that a shambler must get rid of before it can attack the Gaiaslimeoid being protected. If a Steel Bean is damaged, you can !plant another one on top of it to repair it. It cannot be given a Joybean.\nSteel Bean is the middle child of the Metal Crop Bros. He has a deep fascination with conspiracy theories, to the point where his brothers seriously worry about his mental state at times. "We\'re all in a simulation man, they\'re pulling our strings with commands and we just have to follow what\'s in the program." When asked to clarify what he meant by this, Steel Bean replied "You wouldn\'t get it..."\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241056048644126/steelbeans_seedpacket.png',
	enemy_type_gaia_aushucks: 'Aushucks are a metallic upgrade Gaiaslimeoid, meaning that it can be planted on any tile, provided that a Metallicap or Steel Bean is not already occupying that tile. When planted on top of a Gaiaslimeoid, it will produce Gaiaslime at the same rate as a regular brightshade. It can be planted on top of any Gaiaslimeoid, including Brightshades. It cannot be given a Joybean. It is consumed upon use, much like a Joybean.\nAushuck is the eldest of the Metal Crop Bros. He got in on the ground floor with SlimeCoin after the last market crash and made a killing, and from then on he\'s been living the high life. His newfound wealth enables his smug personality, much to the ire of his younger brothers. Everything he owns is gold plated, including all his furniture and clothing. "Look at me, I fucking OWN this city", he says as he stands on the balcony of his luxury condo.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241000918450196/aushucks_seedpacket.png',
	
	enemy_type_defaultshambler: 'The Default Shambler is exactly what it sounds like. It has low defenses and low attack, and will slowly move towards the edge of the field.\n"Ughhhhhhhh, criiiiiiiinnnnngggggeeeee. Baaaaaasssseeeddddddd. Duuuuuddee I loooooovvveeee braaiiiiiiinnnnnnnzzzzz", says Default Shambler, as he lurches toward an enemy Gaiaslimeoid. they\'re all like this. Copy and paste this for every single type of Shambler, you aren\'t missing much.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241123576807435/defaultshambler_gravestone.png',
	enemy_type_bucketshambler: 'The KFC Bucket shambler is exactly the same as a Default Shambler, it just has more HP.\nShamblers don\'t need to eat regular food, but they sometimes do, just for the enjoyment of chowing down on some nice fast food. They tend to go overboard, however, frequently placing the entire KFC bucket over their head just to get the last few crumbs down their gullet. This is how every KFC Bucket shambler is born, as they are too stupid to figure out how to take it off.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241141293416568/kfcbucket_shambler.png',
	enemy_type_juveolanternshambler: 'The Juve-O\'-Lantern shambler is exactly the same as a Default Shambler, it just has significantly more HP.\nThe Juve-O\'-Lantern is crafty, at least by Shambler standards. He has taken a product of the Garden Gankers and used it against them. This increase in defense compensates for the lack of vision it provides, but to be fair Shamblers don\'t really need to worry about that when their only concern is with moving forward in a straight line.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241134977056858/juveolanternshambler_gravestone.png',
	enemy_type_flagshambler: 'The Flag Shambler is exactly the same as a Default Shambler in terms of health and damage output, but it has the unique ability of boosting the damage of all shamblers in its lane when it is present.\nThe Flag Shambler is one of the best units to have in a Graveyard Op, if only for his enthusiasm for the cause. He\'s gone as far as releasing his own album dedicated to Shambler pride, including sleeper hits such as "Amazing Brainz" and "Take Me Home, Shambler Road".\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241129260089374/flagshambler_gravestone.png',
	enemy_type_shambonidriver: 'The Shamboni is a specialized unit, killing anything in its path and leaving behind a frozen slime trail, of which Gaiaslimeoids cannot be planted on. There\'s a catch, however: If it drives over Rustea Leaves or a primed Poketuber, it will not survive the attack and explode instantly.\nBeing turned into a Shambler has given the Shamboni Driver a new lease on life. In his past, he worked long hours with little pay, cleaning the Ice Rink over at Slime\'s End like any other wagecuck, but now he is a brave soldier in Dr. Downpour\'s army of the undead. Drive on, Shamboni. We believe in you.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241174197731389/shambonidriver_gravestone.png',
	enemy_type_mammoshambler: 'The Mammoshambler is a Shambler Mammoslime. It may be slow, but it\'s tough as hell. It can slide on the frozen slime trail left behind by Shambonis to move as fast as a normal Shambler.\nMammoslimes were already bereft of any intelligent thoughts, but being turned into a Shambler has just made things worse. It will frequently be unable to tell friend from foe, and leave many ally Shamblers caught in the crossfire when it slams its massive tusks into the ground. Despite their massive size, they are terrified of Microshamblers.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241144229691463/mammoshambler_gravestone.png',
	enemy_type_gigashambler: 'The Gigashambler is a powerful attacking unit. It is very slow, but can practically one-shot anything in its path once it lands a hit. It will toss a Microshambler off of its back when it is below half of its maximum health.\nThe Gigashambler is what every shambler aspires to be. When he enters the field, you will know. You won\'t just *see* him, you\'ll *sense* him and his chad-like presence. He\'ll make your heart rock. He\'ll make your dick rock. He\'ll make your ass fucking shake, bro.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241132112085123/gigashambler_gravestone.png',
	enemy_type_microshambler: 'The Microshambler is a smaller version of the Default Shambler. He may not have much health, but he can be a vital distraction or even tear up the backlines of a Gaiaslimeoid defense if left unattended. One punch from a Pink Rowddish will send him flying.\nIf Microshambler could speak in complete sentences, he would probably say something like "Being small has its benefits. I may not be able to ride all the rollercoasters I want, but I\'m light enough for Big Bro to carry me on his back and give me a good view of the battlefield."For lack of a better word, he\'s the \'brainz\' of the Gigashambler/Microshambler tag team.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743259271298416640/microshambler_gravestone.png',
	enemy_type_shamblersaurusrex: 'The Shamblersaurus Rex is a Shambler Slimeasaurus Rex. It is fairly bulky and can dish out reasonable damage, but the main draw is its mighty roar, which will stun all Gaiaslimeoids on the field for a brief time, once it reaches below half of its maximum health\n"A pitiable creature. It has the potential to be the king of this city, but it\'s held back by its lust for meat." comments Dr. Downpour. In an effort to maximize the potential of the Shamblersaurus Rex, he re-wired its brain and body to be an omnivore, setting it free to rampage onward towards Gaiaslimeoids and sate its hunger.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241168204333116/shamblersaurusrex_gravestone.png',
	enemy_type_shamblerdactyl: 'The Shamblerdactyl is a Shambler Slimeadactyl. It will not attack in a conventional manner, instead opting to swoop down from the skies and snatch Gaiaslimeoids away from the field, effectively killing them instantly. Sour Potatoes can swallow them whole before it can have the chance to land this attack, however, and Phosphorpoppies will thwart their attacks outright if they are nearby a Shamblerdactyl.\nNo one knows where Shamblerdactyls take their victims after they are whisked away into the skies. Shambologists theorize that they are taken to somewhere in outskirts where their nest lies and newborn Shamblerdactyls are born and raised. At least, they would, if they weren\'t so wall-eyed and prone to crashing into things.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241161350709308/shamblerdactyl_gravestone.png',
	enemy_type_dinoshambler: 'The Dinoshambler is a Shambler Dinoslime. It will not attack in a conventional manner, instead opting to jump over all Gaiaslimeoids in its path. This allows it to be a considerable threat against Garden Gankers who do not put a stop to its agile movements, either by catching it with a Sour Potato, slowing it down with a Dankwheat, or blocking it outright with an erect Suganmanut.\nThe Dinoshambler remains a carnivorous entity, less modified and altered compared to the Shamblersaurus Rex. They make use of their springy legs to leap over short distances, and seek out the mouth-watering Garden Gankers hiding behind the less-desireable leafy appendages of all Gaiaslimeoids. "Chew on this, you knock-off Secreature!", a gangster might say as they shoot down Dinoshamblers who prey on their Garden Ganker allies.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241126185795636/dinoshambler_gravestone.png',
	enemy_type_ufoshambler: 'The UFO Shambler is a Shambler Unnerving Fighting Operator. It will not attack in a conventional manner, preferring to launch ranged attacks in the form of grenades. If a grenade lands nearby a Pink Rowddish, it will be thrown back, resulting in damage taken by the UFO Shambler. If a UFO Shambler runs out of grenades, or if all Gaiaslimeoids within its lane are taken out, it will then begin to move forward like any other shambler and instantly take out any Gaiaslimeoid it finds with a short-range blaster attack.\nOf all the modified Secreatures in Dr. Downpour\'s arsenal, this was by far the trickiest to overturn. Not only did it have to be genetically modified, but technologically modified as well. If all the right steps aren\'t properly taken, there\'s a chance they might be able to contact their homeworld, and god help us all if it comes to that.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241176811044965/ufoshambler_gravestone.png',
	enemy_type_brawldenboomer: 'The Brawlden Boomer is a Shambler with slightly above-average defenses, as he is protected by his Boombox. Once the song on his boombox finishes playing, it will explode, damaging all nearby Gaiaslimeoids. If it is destroyed by Gaiaslimeoids before that point, then he will become enraged, gaining a significant boost to his offensive capabilities. Certain attacks will pierce through his boombox and deal damage to him directly, such as the globs of acid from Dire Apples, or the toxic vape from Killiflowers.\n"Music... they don\'t make it... like they used to...", says The Brawlden Boomer. You can\'t tell if turning into a Shambler caused him to look and act the way he does, or if he was already like this.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241120724811816/brawldenboomer_gravestone.png',
	enemy_type_juvieshambler: 'The Juvie Shambler is a Shambler Juvie. What is less obvious, however, is their method of attack: They mine underground, circumventing all forms of Gaiaslimeoid defense, with the exception of primed Poketubers, which they will detonate upon digging underneath them. If the reach the back of the field, they will begin to walk towards their starting point, taking out Gaiaslimeoids from behind.\nJuvie Shamblers are as cowardly as they come, perhaps even more so than before they had been Shambled. The process of bicarbination has left them traumatized and unable to confront even the weakest of gangsters, instead opting to safely eliminate Gaiaslimeoids through careful navigation under their roots. Fucking pussies.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241138399608852/juvieshambler_gravestone.png',
	enemy_type_shambleballplayer: 'The Shambleball Player is a bulkier version of the Default Shambler, with a unique ability: Any Gaiaslimeoid in their path will be kicked into the column behind them, provided that there is enough room. Their efforts to punt Razonuts will always end in failure, however, due to the sharpened edges puncturing straight through their cleats and damaging them instead. Sour Potatoes will also devour them before their kicks can go through.\nMany people in NLACakaNM, shamblers and non-shamblers alike, are under the impression that Shambeball is a real sport. This is a farce, however. Shambleball can be a fun pass time, but it lacks any notion of rules or formations. As a result, many Shambleball players are found to be wearing conflicting uniforms, be it those used for Soccer, Football, or Basketball. Many of them don\'t even know what game they\'re playing, but their single-digit-IQ allows them to enjoy it all the more.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743259662815592533/shambleballplayer_gravestone.png',
	enemy_type_shamblerwarlord: 'The Shambler Warlord is a Shambler Desert Warlord. He is a fairly strong Shambler, and additionally, he will sometimes call in a handful of Shambler Raiders to surround him and protect him from enemy fire.\nThe Shambler Warlord willingly joined Dr. Downpour\'s forces, so as to get back at the residents of NLACakaNM, who continue to invade his outposts and slaughter his underlings. "Sure, braiiinz, whatever, I\'m just here to get the fucking job done", says Shambler Warlord.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241171219906621/shamblerwarlord_gravestone.png',
	enemy_type_shamblerraider: 'The Shambler Raider is a Shambler Desert Raider. He is exactly the same as a Default Shambler, summoned whenever he is called upon by the Shambler Warlord.\n"N-no, it\'s not true!", Shambler Raider says, clutching his scythe. "I-I don\'t like gardening, this is just for combat!". We all know the truth though, Shambler Raider. You don\'t have to hide it.\nhttps://cdn.discordapp.com/attachments/743240814250950678/743241165436092476/shamblerraider_gravestone.png',
    enemy_type_gvs_boss: 'The Blue Eyes Shambler Dragon is Dr. Downpour\'s personal weapon of mass destruction. It can deal massive damage with balls of fire, summon any type of Shambler, spit out a Bicarbonate Rain weather balloon that heals all Shamblers on the field, and fly into the air for brief periods of time, protecting it from almost all methods of attack from Gaiaslimeoids.\nThe Blue Eyes Shambler Dragon is the culmination of Dr. Downpour\'s research throughout his time spent at SlimeCorp. Every smidgen of anger and vengeance towards his former colleagues was poured into the creation of one disastrous half-monster half-machine that has the potential to turn cities to ash, and spread the Modelovirus like wildfire.\n"Call it whatever you want, The Rain, The Modelovirus. Only the right stuff survived that nightmare... It set me free. It opened my eyes to the future of the city, and what it takes to reach that future. Night Star sent us to hell, but we are going even deeper. I will wage war in order to end this war, once and for all." -Dr. Downpour\nhttps://cdn.discordapp.com/attachments/436013056233963520/728419713633484930/blue_eyes_shambler_dragon.png'
}

rain_protection = [
	cosmetic_id_raincoat,
	weapon_id_umbrella
]

event_type_slimeglob = "slimeglob"
event_type_slimefrenzy = "slimefrenzy"
event_type_poudrinfrenzy = "poudrinfrenzy"
event_type_minecollapse = "minecollapse"
event_type_voidhole = "voidhole"
event_type_voidconnection = "voidconnection"
event_type_shambaquarium = "shambaquarium"

world_events = [
	EwEventDef(
		event_type = event_type_slimeglob,
		str_event_start = "You mined an extra big glob of slime! {}".format(emote_slime1),
	),
	EwEventDef(
		event_type = event_type_slimefrenzy,
		str_event_start = "You hit a dense vein of slime! Double slimegain for the next 30 seconds.",
		str_event_end = "The double slime vein dried up.",
	),
	EwEventDef(
		event_type = event_type_poudrinfrenzy,
		str_event_start = "You hit a dense vein of poudrins! Guaranteed poudrin on every {} for the next 5 seconds.".format(cmd_mine),
		str_event_end = "The poudrin vein dried up.",
	),
	EwEventDef(
		event_type = event_type_minecollapse,
		str_event_start = "The mineshaft starts collapsing around you.\nGet out of there quickly! ({cmd} {captcha})",
	),
	EwEventDef(
		event_type = event_type_voidhole,
		str_event_start = "You hit a sudden gap in the stone, with a scary looking drop. You see what looks like a trampoline on a building's roof at the bottom. Do you **{}** in?".format(cmd_jump),
		str_event_end = "The wall collapses.",
	),
	EwEventDef(
		event_type = event_type_shambaquarium,
		str_event_start = "Holy. Fucking. SHIT. You spot some brainz. Grab 'em all with **{}** {} before they get washed away by the current!",
		str_event_end = "The brainz drift away into the endless expanse of the Slime Sea. Cringe.",
	),
]

event_type_to_def = {}

for event in world_events:
	event_type_to_def[event.event_type] = event

halloween_tricks_tricker = [
	"You open the door and give {} a hearty '!SPOOK'. They lose {} slime!",
	"You slam open the door and give {} a knuckle sandwich. They lose {} slime!",
	"You hastily unlock the door and throw a bicarbonate-soda-flavored pie in {}'s face. They lose {} slime!",
	"You just break down the door and start stomping on {}'s fucking groin. The extreme pain makes them lose {} slime!",
]
halloween_tricks_trickee = [
	"{} opens the door and gives you a hearty '!SPOOK'. You lose {} slime!",
	"{} slams open the door and gives you a knuckle sandwich. You lose {} slime!",
	"{} hastily unlocks the door and throws a bicarbonate-soda-flavored pie in your face. You lose {} slime!",
	"{} just breaks down the door and starts stomping on your fucking groin. The extreme pain makes you lose {} slime!",
]

dungeon_tutorial = [
	#00
	EwDungeonScene(
		text = "You're fucked.\n\nYou'd been dreaming of the day when you'd finally get your hands on some **SLIME**," \
			   " the most precious resource in New Los Angeles City, aka Neo Milwaukee (NLACakaNM).\n\nAs a humble, " \
			   "pitiful Juvenile, or Juvie as they say on the mean streets, it seemed like a pipe dream. Then one day, " \
			   "it happened: you saw a molotov cocktail blow open the hull of a SLIMECORP™ Freight Unit, sending barrels " \
			   "of sweet, beautiful SLIME rolling out across the pavement. You grabbed the first one you could lay your " \
			   "hands on and bolted.\n\nIt was more slime than you'd ever seen before in your wretched Juvie life. But " \
			   "it was not to last. SLIMECORP™ has eyes everywhere. It wasn't long before a SLIMECORP™ death squad kicked " \
			   "in your door, recovered their stolen assets, and burned your whole place to the ground.\n\nTale as old as " \
			   "time.\n\nAs for you, they dumped you in this run-down facility in downtown NLACakaNM called the Detention " \
			   "Center. Supposedly it exists to re-educate wayward youths like yourself on how to be productive citizens. " \
			   "*BARF*\n\nSome guy in a suit brought you to an empty classroom and handcuffed you to a desk. That was like " \
			   "seven hours ago.",
		options = {"escape": 2, "suicide": 3,"wait": 4},
		poi = poi_id_tutorial_classroom,
		life_state = life_state_juvenile,
	),
	#01
	EwDungeonScene(
		text = "Defeated, you reunite your ghost with your body. Alas, death is not the end in NLACakaNM.\n\nAlive " \
			   "once more, the man puts his stogie out and grabs you. He drags you to a new empty classroom, " \
			   "handcuffs you to a new desk, and promptly leaves.",
		options = {"escape": 2, "suicide": 3,"wait": 4},
		poi = poi_id_tutorial_classroom,
		life_state = life_state_juvenile,

	),
	#02
	EwDungeonScene(
		text = "You yank on the handcuffs that hold you to the desk. Being rusted and eroded from years of radiation " \
			   "exposure, the chain snaps instantly. You're free.\n\nYou have two possible routes of escape: the door " \
			   "that you came in through which leads to a hallway, or the window which leads to a courtyard.",
		options = {"goto door": 8, "goto window": 9},
		poi = poi_id_tutorial_classroom,
		life_state = life_state_juvenile,

	),
	#03
	EwDungeonScene(
		text = "You fumble inside the desk and find exactly what you need: a pencil.\n\nYou stab the pencil into " \
			   "the desk so it's standing up straight. You're pretty sure you saw this in a movie once.\n\nWith " \
			   "all your might, you slam your head onto the desk. The pencil has disappeared! Congratulations, you " \
			   "are dead.\n\nHowever, before your ghost can make its way out of the room, a guy in a SLIMECORP™ " \
			   "jumpsuit with a bizarre-looking machine on his back kicks in the door and blasts you with some kind " \
			   "of energy beam, then traps you in a little ghost-box.\n\nHe grabs your body and drags it out of the " \
			   "room, down a series of hallways and several escalators, into a dark room full of boilers and pipes, " \
			   "and one large vat containing a phosphorescent green fluid. He tosses your body, and the box containing " \
			   "your ghost, into the vat, where they land with a SPLOOSH. Then he sits down in a nearby chair and " \
			   "lights up a fat SLIMECORP™-brand cigar.",
		options = {"revive": 1, "wait": 10},
		poi = poi_id_tutorial_ghostcontainment,
		life_state = life_state_corpse,

	),
	#04
	EwDungeonScene(
		text = "You sit and wait for the authorities to decide your fate like a well-behaved little Juvie." \
			   "\n\nYou wait for another hour. Nothing happens.",
		options = {"escape": 2, "suicide": 3,"wait": 5},
		poi = poi_id_tutorial_classroom,
		life_state = life_state_juvenile,

	),
	#05
	EwDungeonScene(
		text = "You sit and wait for the authorities to decide your fate like a well-behaved little Juvie." \
			   "\n\nYou wait for another hour. Still, nothing happens.",
		options = {"escape": 2, "suicide": 3,"wait": 6},
		poi = poi_id_tutorial_classroom,
		life_state = life_state_juvenile,

	),
	#06
	EwDungeonScene(
		text = "You sit and wait for the authorities to decide your fate like a well-behaved little Juvie.\n\n" \
			   "You wait for another hour. You begin to hear a faint commotion through the door. There are " \
			   "distant voices yelling in the hallway outside.",
		options = {"escape": 2, "suicide": 3,"wait": 7},
		poi = poi_id_tutorial_classroom,
		life_state = life_state_juvenile,

	),
	#07
	EwDungeonScene(
		text = "You wait and listen, trying to discern what's going on in the hallway.\n\nThe voices grow louder. " \
			   "You begin to discern more clearly... there are voices frantically shouting, mostly voices that " \
			   "sound like Juvies your age, but some strangely inhuman.\n\nSuddenly you hear gunshots.\n\nA " \
			   "deafening fury erupts as you hear from the hallway a hail of gunfire and the clanging of metal." \
			   "\n\nA sudden explosion demolishes the classroom wall and sends you flying. The desk you were " \
			   "handcuffed to is smashed apart... you're free!\n\nYou have two possible routes of escape: the " \
			   "hole blown in the wall which leads out to the hallway, or the window which leads to a courtyard.",
		options = {"goto hole": 11, "goto window": 9},
		poi = poi_id_tutorial_classroom,
		life_state = life_state_juvenile,

	),
	#08
	EwDungeonScene(
		text = "You go to the door and open it. You step out into the hallway. It is completely empty. " \
			   "You can make out faint voices shouting in the distance.",
		options = {"goto left": 12, "goto right": 12},
		poi = poi_id_tutorial_hallway,
		life_state = life_state_juvenile,

	),
	#09
	EwDungeonScene(
		text = "You make for the window. It slides open easily and you jump out into the courtyard. " \
			   "The grass here is completely dry and dead. A few faintly glowing green thorny weeds " \
			   "grow in patches here and there. Across the lawn you see a high chain-link fence " \
			   "topped with barbed wire. You break into a run hoping to hop the fence and escape.\n\n" \
			   "You make it about 20 feet from the window before a gun turret mounted on the Detention " \
			   "Center roof gets a clear shot at you. A torrent of bullets rips through you and you " \
			   "fall to the ground, directly onto one of the many, many landmines buried here. The " \
			   "explosion blows your body into meaty chunks, and the force is to powerful that even " \
			   "your ghost is knocked unconscious.\n\nWhen you regain consciousness, you realize that" \
			   " you are contained in a tiny ghost-box that's floating in a vat of phosphorescent green " \
			   "fluid along with a collection of bloody meat-chunks that are presumably what's left of " \
			   "your body. Across the dark room, a man in a SLIMECORP™ jumpsuit sits and smokes a " \
			   "SLIMECORP™-brand cigar, apparently waiting for something.",
		options = {"revive": 1, "wait": 10},
		poi = poi_id_tutorial_ghostcontainment,
		life_state = life_state_corpse,

	),
	#10
	EwDungeonScene(
		text = "You and your body float in the glowing green liquid. Nothing happens.",
		options = {"revive": 1, "wait": 10},
		poi = poi_id_tutorial_ghostcontainment,
		life_state = life_state_corpse,

	),
	# 11
	EwDungeonScene(
		text="You peer through the charred hole in the classroom wall and into the hallway.",
		options={"proceed": 15},
		poi = poi_id_tutorial_hallway,
		life_state = life_state_juvenile,

	),
	# 12
	EwDungeonScene(
		text="You make your way down the hallway, hoping to find an exit. The shouting voices grow louder."
			 "\n\nYou come to a split in the hallway. You can go left or right.",
		options={"goto left": 13, "goto right": 13},
		poi = poi_id_tutorial_hallway,
		life_state = life_state_juvenile,

	),
	# 13
	EwDungeonScene(
		text="You make your way down the hallway, hoping to find an exit. The shouting voices grow even "
			 "louder.\n\nYou come to another split. Left or right?",
		options={"goto left": 14, "goto right": 14},
		poi = poi_id_tutorial_hallway,
		life_state = life_state_juvenile,

	),
	# 14
	EwDungeonScene(
		text="You make your way down the hallway, hoping to find an exit.\n\nAs you come to the next "
			 "split in the hallway, a gunshot rings out. Suddenly, there is an explosion of noise as "
			 "more and more guns fire, and you hear the clang of metal against metal.",
		options={"proceed": 15},
		poi = poi_id_tutorial_hallway,
		life_state = life_state_juvenile,

	),
	# 15
	EwDungeonScene(
		text="It looks like a fucking war has erupted. Bullets are flying through the air and bodies, blood, " \
			 "and slime are all smeared across the floor and the walls.\n\nDown the hallway in both directions " \
			 "are groups of people waging what you now realize must be GANG WARFARE. These must be gang " \
			 "members here to capture some territory for their KINGPINS.\n\nTo your right, a throng of terrifying " \
			 "freaks in pink gleefully !thrash about, swinging spiked bats and firing automatic weapons with " \
			 "wild abandon. You've heard about them... the deadly ROWDYS.\n\nTo your left, a shadowy mass of " \
			 "sinister-looking purple-clad ne'er-do-wells !dab defiantly in the face of death, blades and guns " \
			 "gleaming in the fluorescent light. These must be the dreaded KILLERS.\n\nAnd in the middle, " \
			 "where the two gangs meet, weapons clash and bodies are smashed open, slime splattering everywhere " \
			 "as the death count rises.\n\nA little bit gets on you. It feels good.",
		options={"scavenge": 16, "kill": 17, "goto left": 18, "goto right": 19},
		poi = poi_id_tutorial_hallway,
		life_state = life_state_juvenile,

	),
	# 16
	EwDungeonScene(
		text="You surreptitiously try to scrape up as much of the dropped slime as you can without " \
			 "alerting the gang members to your presence. It's not much, but you stuff what little " \
			 "you can gather into your pockets.\n\nGod you fucking love slime so much.",
		options={"scavenge": 16, "kill": 17, "goto left": 18, "goto right": 19},
		poi = poi_id_tutorial_hallway,
		life_state = life_state_juvenile,

	),
	# 17
	EwDungeonScene(
		text="You itch to get in on the action. But unfortunately, you're still a mere Juvenile. " \
			 "Violence is simply beyond your capability... for now.\n\nYou make a mental note to " \
			 "!enlist in a gang at the first possible opportunity. You'll need to escape the " \
			 "Detention Center first though, and get some slime.",
		options={"scavenge": 16, "kill": 17, "goto left": 18, "goto right": 19},
		poi = poi_id_tutorial_hallway,
		life_state = life_state_juvenile,

	),
	# 18
	EwDungeonScene(
		text="You're certain any individual member of either side of this conflict could obliterate " \
				"you with a mere thought. With no safe options available, you decide to make a break " \
				"for it to the left, through the ranks of the KILLERS.\n\nYou sprint down the hall " \
				"and pray that none of the whizzing bullets connect with your tender and slimeless Juvie " \
				"body.\n\nReaching the Killer front lines, you make a running leap. A curved scythe " \
				"blade that you think must be sharp enough to split atoms whizzes millimeters above " \
				"your head.\n\nMiraculously, you land still intact on the other side of the Killers, who " \
				"pay you no further mind. You break into a run.\n\nYou run through through hallway after " \
				"hallway riddled with the burned craters and bullet holes left in the wake of the Killers. " \
				"Purple graffiti is scrawled on the walls everywhere. \"!DAB\" is written over and over, " \
				"along with the occasional \"ROWDYS IS BUSTAHS\", drawings of bizarre slimy-looking creatures, " \
				"and pictures of a hooded man in a beanie accompanied by the message \"FOR THE COP KILLER\".\n\n" \
				"This \"Cop Killer\" must be a pretty cool guy, you decide.\n\nAt last, when you're nearing " \
				"exhaustion, you come to a large burnt hole in the wall that leads outside. The Killers must " \
				"have blown the wall open to make their assault.\n\nCould it be? Sweet freedom at last??",
		options={"escape": 20},
		poi = poi_id_tutorial_hallway,
		life_state = life_state_juvenile,

	),
	# 19
	EwDungeonScene(
		text="You're certain any individual member of either side of this conflict could obliterate " \
			"you with a mere thought. With no safe options available, you decide to make a break for " \
			"it to the right, through the ranks of the ROWDYS.\n\nYou sprint down the hall and pray " \
			"that none of the whizzing bullets connect with your tender and slimeless Juvie body.\n\n" \
			"Reaching the Rowdy front lines, you make a running leap. A wildly swung nun-chuck packing " \
			"the force of an eighteen-wheeler whizzes millimeters above your head.\n\nMiraculously, " \
			"you land still intact on the other side of the Rowdys, who pay you no further mind. You " \
			"break into a run.\n\nYou run through through hallway after hallway riddled with the burned " \
			"craters and bullet holes left in the wake of the Rowdys. Pink graffiti is scrawled on the " \
			"walls everywhere. \"!THRASH\" is written over and over, along with the occasional \"KILLERS " \
			"GET FUCKED\", drawings of bizarre slimy-looking creatures, and pictures of a man in a " \
			"jester's cap accompanied by the message \"FOR THE ROWDY FUCKER\".\n\nThis \"Rowdy Fucker\" " \
			"must be a pretty cool guy, you decide.\n\nAt last, when you're nearing exhaustion, you come " \
			"to a large burnt hole in the wall that leads outside. The Rowdys must have blown the wall " \
			"open to make their assault.\n\nCould it be? Sweet freedom at last??",
		options={"escape": 20},
		poi = poi_id_tutorial_hallway,
		life_state = life_state_juvenile,

	),
	# 20
	EwDungeonScene(
		text="You exit through the hole in the wall into the front parking lot of the Detention " \
				"Center. Behind you you can still hear screams and gunshots echoing through the halls." \
				"\n\nMoving quickly, you sprint across the parking lot, lest some SLIMECORP™ security " \
				"camera alert a guard to your presence. Fortunately, it seems that all available Detention " \
				"Center personel are dealing with the Gang Warfare currently raging inside.\n\nUpon " \
				"reaching the high chain link fence encircling the facility, you find that a large hole " \
				"has been torn open in it, through which you quickly make your escape.\n\nYou take a " \
				"moment to survey the scene before you. Downtown NLACakaNM bustles and hums with activity " \
				"and you hear the familiar clicking of the Geiger Counters on every street corner. Over " \
				"the skyline you see it... the towering green obelisk, ENDLESS WAR. Taker of Life, " \
				"Bringer of Slime. Your heart swells with pride and your eyes flood with tears at the " \
				"sight of His glory.\n\nBehind you, SLIMECORP™ helicopters circle overhead. You know " \
				"what that means. Things are about to get hot. Time to skedaddle.\n\nYou leave the " \
				"Detention Center and head into Downtown.\n\nIt's time to resume your life in NLACakaNM.",
		dungeon_state = False,
		poi = poi_id_downtown,
		life_state = life_state_juvenile,

	),
]

pray_responses_list = [
	"ENDLESS WAR momentarily overwhelms all of your senses by telepathically communicating with you in his eldritch tongue.",
	"ENDLESS WAR gazes up towards the stars, longingly.",
	"ENDLESS WAR fondly regards the good ol’ days.",
	"ENDLESS WAR urges you to collect more slime.",
	"ENDLESS WAR hungers for more.",
	"ENDLESS WAR commands you to kill thy neighbor.",
	"ENDLESS WAR creates an overwhelming urge inside of you to kill everyone you know.",
	"ENDLESS WAR helpfully reminds you that !harvest is not a valid text command.",
	"ENDLESS WAR is a free text-based MMORPG playable entirely within a Discord server. But, you probably already knew that, didn't you?",
]


dance_responses = [
	"{} busts a move. Wow, look at 'em go!",
	"{} gets down and boogies! Groovy!",
	"{} does a headstand and does a 720 degree spin!",
	"{} starts flossing fast and hard!",
	"{} does the Orange Justice, nailing each step flawlessly. Incredible!",
	"{} cracks the whip! Watch them go at it!",
	"{} performs the Nae Nae! https://en.wikipedia.org/wiki/Nae_Nae",
	"{} does the Default Dance! You hear the familiar Fortnite jingle go off in your head.",
	"{} gets down on the floor and does the worm! Their rhythm is off the charts!",
	"{} spins around like a Laotian Toprock dancer! Whoa, be careful not to kick anyone, big guy!",
	"{} does the monkey! Man, they're pretty!",
	"{} does the charleston. What is this, the 20's? They do look kinda cool though...",
	"{} starts breakdancing, Capoeira style! They almost knock someone's teeth out with their swift leg swings!",
	"{} does a triple backflip! Hot diggedy!",
	"{} performs a double Cartwheel! Not really a dance move, but we'll take it!",
	"{} starts a Conga line! The party's over here!",
	"{} does a moonwalk! They're smooth as heck!",
	"{} does the robot! They manage to pull it off in a way that doesn't seem totally autistic!",
	"{} does the carlton! It's anything BUT unusual!",
	"{} starts tap dancing! They really start puttin' on the ritz for sure!",
	"{} pumps their fist in the air over and over!",
	"{} does a Flamenco dance! Their grace and elegance is unmatched!",
	"{} walks like an Egyptian! Wow, racist much???",
	"{} does an old-fashioned breakdance! Hot damn!",
	"{} does the traditional Ukrainian Hopak! Their legs flail back and forth!",
	"{} performs the Mannrobics taunt! They feel the burn!",
	"{} gets the urge to !dab, but holds back with all their might.",
	"{} gets the urge to !thrash, but holds back with all their might.",
	"{} just kind of stands there, awkwardly. What did you expect?",
	"{} makes a complete fool of themselves. Everyone gets secondhand embarrassment...",
]

# links to SlimeCorp propaganda
propaganda = [
	'https://cdn.discordapp.com/attachments/431238867459375145/617526157239386113/image0.jpg',
	'https://cdn.discordapp.com/attachments/761984492868993031/761984545087946764/break_free_goon.png',
	'https://cdn.discordapp.com/attachments/761984492868993031/761984547549478942/corp_goon_1.png',
	'https://cdn.discordapp.com/attachments/761984492868993031/761984566562258984/saint_goon.png',
	'https://cdn.discordapp.com/attachments/761984492868993031/761984567249731664/D7xtNC8XYAI5uB9.png',
	'https://cdn.discordapp.com/attachments/761984492868993031/761984569460391967/DeQWu9iX0AA-F7H.png',
	'https://cdn.discordapp.com/attachments/761984492868993031/761984575228215316/securityforce2.png',
	'https://cdn.discordapp.com/attachments/761984492868993031/761984576205619220/slime_corp_designs.png',
]

# list of genres and aliases
book_genres = [
	"narrative", #0
	"historical", #1
	"comic", #2
	"porn", #3
	"instructional", #4
	"lore", #5
	"reference", #6
	"journal", #7
	"newspaper", #8
	"experimental", #9
    "surgical" #10
	]

# rating flavor text
rating_flavor = [
	"",
	"Seething with hatred",
	"Teeming with disappointment",
	"pullulating with mild satisfaction",
	"Brimming with respect",
	"Glowing with admiration",
	]

zine_cost = 10000
minimum_pages = 5
maximum_pages = 20

# zine related commands that can be used in DMs
zine_commands = [
	cmd_beginmanuscript,
	cmd_beginmanuscript_alt_1,
	cmd_beginmanuscript_alt_2,
	cmd_setpenname,
	cmd_setpenname_alt_1,
	cmd_settitle,
	cmd_settitle_alt_1,
	cmd_setgenre,
	cmd_editpage,
	cmd_viewpage,
	cmd_checkmanuscript,
	cmd_publishmanuscript,
	cmd_readbook,
	cmd_nextpage,
	cmd_nextpage_alt_1,
	cmd_previouspage,
	cmd_previouspage_alt_1,
	cmd_previouspage_alt_2,
	cmd_rate,
	cmd_rate_alt_1,
	cmd_rate_alt_2,
	cmd_accept,
	cmd_refuse,
	cmd_setpages,
	cmd_setpages_alt_1,
	cmd_setpages_alt_2,
]

curse_words = { # words that the player should be punished for saying via swear jar deduction. the higher number, the more the player gets punished.
	"fag":20,
	"shit":10,
	"asshole":10, # can not be shortened to 'ass' due to words like 'pass' or 'class'
	"dumbass": 10,
	"cunt":30,
	"fuck":10,
	"bitch":10,
	"bastard":5,
	"nigger":80,
	"kike":80,
	"cuck":30,
	#"chink":50,
	"chinaman":50,
	"gook":50,
	"injun":50,
	"bomboclaat":80,
	"mick":50,
	"pickaninny":50,
	"tarbaby":50,
	"towelhead":50,
	"wetback":50,
	"zipperhead":50,
	"spic":50,
	"dyke":50,
	"tranny":80,
	"dickhead":20,
	"retard":20,
	"buster":100,
	"kraker":100,
	"beaner":50,
	"wanker":10,
	"twat":10,
}

curse_responses = [ # scold the player for swearing
	"Watch your language!",
	"Another one for the swear jar...",
	"Do you kiss your mother with that mouth?",
	"Wow, maybe next time be a little nicer, won't you?",
	"If you don't have anything nice to say, then don't say anything at all.",
	"Now that's just plain rude.",
	"And just like that, some of your precious SlimeCoin goes right down the drain.",
	"Calm down that attitude of yours, will you?",
	"Your bad manners have costed you a fraction of your SlimeCoin!",
	"Take your anger out on a juvenile, if you're so inclined to use such vulgar language.",
	#"You know, don't, say, s-swears."
]

captcha_dict = [
	#3
	'GOO', 'MUD', 'DIE', 'WAR', 'BEN',
	'EYE', 'ARM', 'LEG', 'BOO', 'DAB',
	'KFC', 'GAY', 'LOL', 'GUN', 'MUK',
	'POW', 'WOW', 'POP', 'OWO', 'HIP',
	'END', 'HAT', 'CUP', '911', '711',
	'SIX', 'SMG', 'BOW',
	#4
	'GOON', 'DOOR', 'CORP', 'SPAM', 'BLAM',
	'FISH', 'MINE', 'LOCK', 'OURS', 'ROCK',
	'DATA', 'LOOK', 'GOTO', 'COIN', 'GANG',
	'HEHE', 'WEED', 'LMAO', 'EPIC', 'NICE',
	'SOUL', 'KILL', 'FREE', 'GOOP', 'CAVE',
	'ZOOM', 'FIVE', 'NINE', 'BASS', 'FIRE',
	'TEXT', 'AWOO',
	#5
	'GUNKY', 'BOORU', 'ROWDY', 'GHOST', 'ORDER',
	'SCARE', 'BULLY', 'FERRY', 'SAINT', 'SLASH',
	'SLOSH', 'PARTY', 'BASED', 'TULPA',
	'SLURP', 'MONTH', 'SEVEN', 'BRASS', 'MINES',
	'CHEMO', 'LIGHT', 'FURRY', 'PIZZA', 'ARENA',
	'LUCKY', 'RIFLE', '56709',
	#6
	'SLUDGE', 'KILLER', 'MUNCHY', 'BLAAAP', 'BARTER',
	'ARTIST', 'FUCKER', 'MINING', 'SURVEY', 'THRASH',
	'BEWARE', 'STOCKS', 'COWARD', 'CRINGE', 'INVEST', 
	'BUSTAH', 'KILLAH', 'KATANA', 'GHOSTS', 'BASSED', 
	'REVIVE', 'BATTLE', 'PAWPAW',
	#7
	'KINGPIN', 'ENDLESS', 'ATTACKS', 'FUCKERS', 'FISHING',
	'VIOLENT', 'SQUEEZE', 'LOBSTER', 'WESTERN', 'EASTERN', 
	'REGIONS', 'DISCORD', 'KNUCKLE', 'MOLOTOV', 'SHAMBLE',
	'WARFARE', 'BIGIRON', 'POUDRIN', 'PATRIOT', 'MINIGUN',
	#8
	'GAMEPLAY', 'CONFLICT', 'EXCHANGE', 'FEEDBACK', 'GRENADES',
	'VIOLENCE', 'TACOBELL', 'PIZZAHUT', 'OUTSKIRT', 'WHATEVER',
	'WITHDRAW', 'SOUTHERN', 'NORTHERN', 'ASTATINE', 'SLIMEOID',
	'SHAMBLIN', 'STAYDEAD', 'DOWNTOWN', 'DISTRICT', 'BASEBALL',
	'BIGBONES', 'LONEWOLF', 'KEENSMELL', 'RAZORNUTS', 'REVOLVER',
	#9
	'APARTMENT', 'SURVIVORS', 'NEGASLIME', 'COMMUNITY', 'GIGASLIME',
	'DETENTION', 'CATHEDRAL', 'TOXINGTON', 'SLIMEGIRL', 'INVESTING',
	'SLIMECOIN', 'RATELIMIT', 'NARRATIVE', 'COMMANDO', 'SHAMBLERS',
	'NUNCHUCKS', 'SLIMECORP', 'ARSONBROOK','SMOGSBURG', 'SLIMEFEST', 
	'COMMANDER', 'FATCHANCE', 'DANKWHEAT',
	#10
	'SLUDGECORE', 'LOREMASTER', 'ROUGHHOUSE', 'GLOCKSBURY', 'CALCULATED',
	'PLAYGROUND', 'NEWYONKERS', 'OLDYONKERS', 'VANDALPARK', 'SLIMERMAID',
	'SLIMEXODIA', 'WEBBEDFEET', 'NOSEFERATU', 'BINGEEATER', 'TRASHMOUTH',
	'DIREAPPLES', 'BLACKLIMES', 'POKETUBERS', 'PULPGOURDS', 'ROWDDISHES',
	'DRAGONCLAW',
]

races = {
	'humanoid': 'humanoid',
	'amphibian': 'amphibian',
	'food': 'food',
	'skeleton': 'skeleton',
	'robot': 'robot',
	'furry': 'furry',
	'scalie': 'scalie',
	'slime-derived': 'slime-derived',
	'monster': 'monster',
	'critter': 'critter',
	'avian': 'avian',
	'insectoid': 'insectoid',
	'other': 'other',
	'shambler' : 'shambler'
}

# slime twitter stuff
tweet_color_by_lifestate = {
	life_state_corpse : '010101',
	life_state_juvenile: '33cc4a'
}

tweet_color_by_faction = {
	faction_killers : 'b585ff',
	faction_rowdys : 'f390b6',
	faction_slimecorp : 'ff0000'
}


# scream = ""
# for i in range(1, 10000):
#     scream += "A"
#     
# print(scream)

"""    /*"rpcity": {
        "id_poi": "rpcity",
        "alias": [
            "rp",
            "rp city",
            "roleplay city",
            "rpc",
            "costumestore",
            "costume"
        ],
        "str_name": "RP City",
        "str_desc": "This place gives you the fucking creeps. A run-down shell of its former self, the RP City store has been long forgotten by most of the residents of NLACakaNM, but every Double Halloween, it somehow comes crawling back. All the amenities and costumes are ragged and decrepit, but it seems there's still a fresh supply of costume creation kits. Oh yeah, the register is also manned by a ghost, because why wouldn't it be. He doesn't seem to mind you browsing though, you figure he's just here to collect a paycheck. Such is life... er... the afterlife, rather.",
        "str_in": "in",
        "str_enter": "enter",
        "coord": null,
        "coord_alias": [],
        "channel": "rp-city",
        "role": "RP City",
        "major_role": "littlechernobyl_major",
        "minor_role": "nullminorrole",
        "permissions": {
            "rpcity": [
                "read",
                "send",
                "connect"
            ]
        },
        "pvp": false,
        "factions": [],
        "life_states": [],
        "closed": false,
        "str_closed": null,
        "vendors": [
            "RP City"
        ],
        "property_class": "",
        "is_district": false,
        "is_gangbase": false,
        "is_capturable": false,
        "is_subzone": true,
        "is_apartment": false,
        "is_street": false,
        "mother_districts": [
            "littlechernobyl"
        ],
        "father_district": "",
        "is_transport": false,
        "transport_type": "",
        "default_line": "",
        "default_stop": "",
        "is_transport_stop": false,
        "is_outskirts": false,
        "community_chest": null,
        "is_pier": false,
        "pier_type": null,
        "is_tutorial": false,
        "has_ads": false,
        "write_manuscript": true,
        "max_degradation": 10000,
        "neighbors": {
            "littlechernobyl": 20
        },
        "topic": "",
        "wikipage": "https://rfck.miraheze.org/wiki/Little_Chernobyl#RP_City"
    },*/"""
