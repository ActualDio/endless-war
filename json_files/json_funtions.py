import json
import os
import string
index = 0
ITEM_ID = {

    "acquisition_smelting" : "smelting",
    "acquisition_milling" : "milling",
    "acquisition_mining" : "mining",
    "acquisition_dojo" : "dojo",
    "acquisition_fishing" : "fishing",
    "acquisition_bartering" : "bartering",
    "acquisition_trickortreating" : "trickortreating",
    "acquisition_bazaar" : "bazaar",

    "context_slimeoidheart": 'slimeoidheart',
    "context_slimeoidbottle": 'slimeoidbottle',
    "context_slimeoidfood": 'slimeoidfood',
    "context_wrappingpaper": 'wrappingpaper',
    "context_prankitem": 'prankitem',
    "context_seedpacket": 'seedpacket',
    "context_tombstone": 'tombstone',

    # Item vendor names.
    "vendor_bar": 'bar',  # rate of non-mtn dew drinks are 100 slime to 9 hunger,
    "vendor_pizzahut": 'Pizza Hut',  # rate of fc vendors are 100 slime to 10 hunger,
    "vendor_tacobell": 'Taco Bell',
    "vendor_kfc": 'KFC',
    "vendor_mtndew": 'Mtn Dew Fountain',
    "vendor_vendingmachine": 'vending machine',
    # rate of seafood is 100 slime to 9 hunger
    "vendor_seafood": 'Red Mobster Seafood',
    "vendor_diner": "Smoker's Cough",  # rate of drinks are 100 slime to 15 hunger,
    # Just features clones from the Speakeasy and Red Mobster
    "vendor_beachresort": "Beach Resort",
    # Just features clones from the Speakeasy and Red Mobster
    "vendor_countryclub": "Country Club",
    "vendor_farm": "Farm",  # contains all the vegetables you can !reap,
    "vendor_bazaar": "bazaar",
    "vendor_college": "College",  # You can buy game guides from either of the colleges,
    # Repels and trading cards are sold here
    "vendor_glocksburycomics": "Glocksbury Comics",
    "vendor_slimypersuits": "Slimy Persuits",  # You can buy candy from here,
    "vendor_greencakecafe": "Green Cake Cafe",  # Brunch foods,
    "vendor_bodega": "Bodega",  # Clothing store in Krak Bay,
    # The secret clothing store in Krak Bay,
    "vendor_secretbodega": "Secret Bodega",
    # waffle house in the void, sells non-perishable foods, 100 slime to 1 hunger
    "vendor_wafflehouse": "Waffle House",
    "vendor_basedhardware": "Based Hardware",  # Hardware store in West Glocksbury,
    "vendor_lab": "Lab",  # Slimecorp "products",
    "vendor_atomicforest": "Atomic Forest Stockpile",  # Storage of atomic forest,
    # Store for shamblers to get stuff
    "vendor_downpourlaboratory": "Downpour Armament Vending Machines",
    # Security officers can order items here for free.
    "vendor_breakroom": "The Breakroom",
    "vendor_rpcity": "RP City",  # Double halloween costume store,

    "item_id_slimepoudrin": 'slimepoudrin',
    "item_id_negapoudrin": 'negapoudrin',
    "item_id_monstersoup": 'monstersoup',
    "item_id_doublestuffedcrust": 'doublestuffedcrust',
    "item_id_quadruplestuffedcrust": 'quadruplestuffedcrust',
    "item_id_octuplestuffedcrust": "octuplestuffedcrust",
    "item_id_sexdecuplestuffedcrust": "sexdecuplestuffedcrust",
    "item_id_duotrigintuplestuffedcrust": "duotrigintuplestuffedcrust",
    "item_id_quattuorsexagintuplestuffedcrust": "quattuorsexagintuplestuffedcrust",
    "item_id_forbiddenstuffedcrust": "theforbiddenstuffedcrust",
    "item_id_forbidden111": "theforbiddenoneoneone",
    "item_id_tradingcardpack": "tradingcardpack",
    "item_id_stick": "stick",
    "item_id_gameguide": "gameguide",
    "item_id_juviegradefuckenergybodyspray": "juviegradefuckenergybodyspray",
    "item_id_superduperfuckenergybodyspray": "superduperfuckenergybodyspray",
    "item_id_gmaxfuckenergybodyspray": "gmaxfuckenergybodyspray",
    "item_id_costumekit": "costumekit",
    "item_id_doublehalloweengrist": "doublehalloweengrist",
    "item_id_whitelineticket": "ticket",
    "item_id_seaweedjoint": "seaweedjoint",
    "item_id_megaslimewrappingpaper": "megaslimewrappingpaper",
    "item_id_greeneyesslimedragonwrappingpaper": "greeneyesslimedragonwrappingpaper",
    "item_id_phoebuswrappingpaper": "phoebuswrappingpaper",
    "item_id_slimeheartswrappingpaper": "slimeheartswrappingpaper",
    "item_id_slimeskullswrappingpaper": "slimeskullswrappingpaper",
    "item_id_shermanwrappingpaper": "shermanwrappingpaper",
    "item_id_slimecorpwrappingpaper": "slimecorpwrappingpaper",
    "item_id_pickaxewrappingpaper": "pickaxewrappingpaper",
    "item_id_munchywrappingpaper": "munchywrappingpaper",
    "item_id_benwrappingpaper": "benwrappingpaper",
    "item_id_gellphone": "gellphone",
    "item_id_royaltypoudrin": "royaltypoudrin",
    "item_id_prankcapsule": "prankcapsule",
    "item_id_cool_material": "coolbeans",
    "item_id_tough_material": "toughnails",
    "item_id_smart_material": "smartcookies",
    "item_id_beautiful_material": "beautyspots",
    "item_id_cute_material": "cutebuttons",
    "item_id_dragonsoul": "dragonsoul",
    "item_id_monsterbones": "monsterbones",
    "item_id_faggot": "faggot",
    "item_id_doublefaggot": "doublefaggot",
    "item_id_seaweed": "seaweed",
    "item_id_string": "string",
    "item_id_tincan": "tincan",
    "item_id_oldboot": "oldboot",
    "item_id_leather": "leather",
    "item_id_ironingot": "ironingot",
    "item_id_bloodstone": "bloodstone",
    "item_id_tanningknife": "tanningknife",
    "item_id_dinoslimemeat": "dinoslimemeat",
    "item_id_dinoslimesteak": "dinoslimesteak",
    "item_id_dyesolution": "dyesolution",
    "item_id_textiles": "textiles",
    "item_id_foodbase": "foodbase",
    "item_id_civilianscalp": "civilianscalp",
    "item_id_modelovaccine": "modelovirusvaccine",
    "item_id_gaiaseedpack_poketubers": "poketubersseedpacket",
    "item_id_gaiaseedpack_pulpgourds": "pulpgourdsseedpacket",
    "item_id_gaiaseedpack_sourpotatoes": "sourpotatoesseedpacket",
    "item_id_gaiaseedpack_bloodcabbages": "bloodcabbagesseedpacket",
    "item_id_gaiaseedpack_joybeans": "joybeansseedpacket",
    "item_id_gaiaseedpack_purplekilliflower": "purplekilliflowerseedpacket",
    "item_id_gaiaseedpack_razornuts": "razornutsseedpacket",
    "item_id_gaiaseedpack_pawpaw": "pawpawseedpacket",
    "item_id_gaiaseedpack_sludgeberries": "sludgeberriesseedpacket",
    "item_id_gaiaseedpack_suganmanuts": "suganmanutsseedpacket",
    "item_id_gaiaseedpack_pinkrowddishes": "pinkrowddishesseedpacket",
    "item_id_gaiaseedpack_dankwheat": "dankwheatseedpacket",
    "item_id_gaiaseedpack_brightshade": "brightshadeseedpacket",
    "item_id_gaiaseedpack_blacklimes": "blacklimesseedpacket",
    "item_id_gaiaseedpack_phosphorpoppies": "phosphorpoppiesseedpacket",
    "item_id_gaiaseedpack_direapples": "direapplesseedpacket",
    "item_id_gaiaseedpack_rustealeaves": "rustealeavesseedpacket",
    "item_id_gaiaseedpack_metallicaps": "metallicapsseedpacket",
    "item_id_gaiaseedpack_steelbeans": "steelbeansseedpacket",
    "item_id_gaiaseedpack_aushucks": "aushucksseedpacket",
    "item_id_tombstone_defaultshambler": "defaultshamblertombstone",
    "item_id_tombstone_bucketshambler": "bucketshamblertombstone",
    "item_id_tombstone_juveolanternshambler": "juveolanternshamblertombstone",
    "item_id_tombstone_flagshambler": "flagshamblertombstone",
    "item_id_tombstone_shambonidriver": "shambonidrivertombstone",
    "item_id_tombstone_mammoshambler": "mammoshamblertombstone",
    "item_id_tombstone_gigashambler": "gigashamblertombstone",
    "item_id_tombstone_microshambler": "microshamblertombstone",
    "item_id_tombstone_shamblersaurusrex": "shamblesaurusrextombstone",
    "item_id_tombstone_shamblerdactyl": "shamblerdactyltombstone",
    "item_id_tombstone_dinoshambler": "dinoshamblertombstone",
    "item_id_tombstone_ufoshambler": "ufoshamblertombstone",
    "item_id_tombstone_brawldenboomer": "brawldenboomertombstone",
    "item_id_tombstone_juvieshambler": "juvieshamblertombstone",
    "item_id_tombstone_shambleballplayer": "shambleballplayertombstone",
    "item_id_tombstone_shamblerwarlord": "shamblerwarlordtombstone",
    "item_id_tombstone_shamblerraider": "shamblerraidertombstone",
    "item_id_gaiaslimeoid_pot": "gaiaslimeoidpot",

    # SLIMERNALIA
    "item_id_sigillaria": "sigillaria",

    # SWILLDERMUK
    # Instant use items
    "item_id_creampie": "creampie",
    "item_id_waterballoon": "waterbaloon",
    "item_id_bungisbeam": "bungisbeam",
    "item_id_circumcisionray": "circumcisionray",
    "item_id_cumjar": "cumjar",
    "item_id_discounttransbeam": "discounttransbeam",
    "item_id_transbeamreplica": "transbeamreplica",
    "item_id_bloodtransfusion": "bloodtransfusion",
    "item_id_transformationmask": "transformationmask",
    "item_id_emptychewinggumpacket": "emptychewinggumpacket",
    "item_id_airhorn": "airhorn",
    "item_id_banggun": "banggun",
    "item_id_pranknote": "pranknote",
    "item_id_bodynotifier": "bodynotifier",
    # Response items
    "item_id_chinesefingertrap": "chinesefingertrap",
    "item_id_japanesefingertrap": "japanesefingertrap",
    "item_id_sissyhypnodevice": "sissyhypnodevice",
    "item_id_piedpiperkazoo": "piedpiperkazoo",
    "item_id_sandpapergloves": "sandpapergloves",
    "item_id_ticklefeather": "ticklefeather",
    "item_id_genitalmutilationinstrument": "gentialmutilationinstrument",
    "item_id_gamerficationasmr": "gamerficationasmr",
    "item_id_beansinacan": "beansinacan",
    "item_id_brandingiron": "brandingiron",
    "item_id_lasso": "lasso",
    "item_id_fakecandy": "fakecandy",
    "item_id_crabarmy": "crabarmy",
    # Trap items
    "item_id_whoopiecushion": "whoopiecushion",
    "item_id_beartrap": "beartrap",
    "item_id_bananapeel": "bananapeel",
    "item_id_windupbox": "windupbox",
    "item_id_windupchatterteeth": "windupchatterteeth",
    "item_id_snakeinacan": "snakeinacan",
    "item_id_landmine": "landmine",
    "item_id_freeipad": "freeipad",
    "item_id_freeipad_alt": "freeipad_alt",
    "item_id_perfectlynormalfood": "perfectlynormalfood",
    "item_id_pitfall": "pitfall",
    "item_id_electrocage": "electrocage",
    "item_id_ironmaiden": "ironmaiden",
    "item_id_signthatmakesyoubensaint": "signthatmakesyoubensaint",
    "item_id_piebomb": "piebomb",
    "item_id_defectivealarmclock": "defectivealarmclock",
    "item_id_alligatortoy": "alligatortoy",
    "item_id_janusmask": "janusmask",
    "item_id_swordofseething": "swordofseething",

    "prank_type_instantuse": 'instantuse',
    "prank_type_response": 'response',
    "prank_type_trap": 'trap',
    "prank_rarity_heinous": 'heinous',
    "prank_rarity_scandalous": 'scandalous',
    "prank_rarity_forbidden": 'forbidden',
    "prank_type_text_instantuse": '\\n\\nPrank Type: Instant Use - Good for hit-and-run tactics.',
    "prank_type_text_response": '\\n\\nPrank Type: Response - Use it on an unsuspecting bystander.',
    "prank_type_text_trap": '\\n\\nPrank Type: Trap - Lay it down in a district.',

    # candy ids
    "item_id_paradoxchocs": "paradoxchocs",
    "item_id_licoricelobsters": "licoricelobsters",
    "item_id_chocolateslimecorpbadges": "chocolateslimecorpbadges",
    "item_id_munchies": "munchies",
    "item_id_sni": "sni",
    "item_id_twixten": "twixten",
    "item_id_slimybears": "slimybears",
    "item_id_marsbar": "marsbar",
    "item_id_magickspatchkids": "magickspatchkids",
    "item_id_atms": "atms",
    "item_id_seanis": "seanis",
    "item_id_candybungis": "candybungis",
    "item_id_turstwerthers": "turstwerthers",
    "item_id_poudrinpops": "poudrinpops",
    "item_id_juvieranchers": "juvieranchers",
    "item_id_krakel": "krakel",
    "item_id_swedishbassedgods": "swedishbassedgods",
    "item_id_bustahfingers": "bustahfingers",
    "item_id_endlesswarheads": "endlesswarheads",
    "item_id_n8heads": "n8heads",
    "item_id_strauberryshortcakes": "strauberryshortcakes",
    "item_id_chutzpahcherries": "chutzpahcherries",
    "item_id_n3crunch": "n3crunch",
    "item_id_slimesours": "slimesours",

    # slimeoid food
    "item_id_fragilecandy": "fragilecandy",  # +chutzpah -grit,
    "item_id_rigidcandy": "rigidcandy",  # +grit -chutzpah,
    "item_id_recklesscandy": "recklesscandy",  # +moxie -grit,
    "item_id_reservedcandy": "reservedcandy",  # +grit -moxie,
    "item_id_bluntcandy": "bluntcandy",  # +moxie -chutzpah,
    "item_id_insidiouscandy": "insidiouscandy",  # +chutzpah -moxie,

    # vegetable ids
    "item_id_poketubers": "poketubers",
    "item_id_pulpgourds": "pulpgourds",
    "item_id_sourpotatoes": "sourpotatoes",
    "item_id_bloodcabbages": "bloodcabbages",
    "item_id_joybeans": "joybeans",
    "item_id_purplekilliflower": "purplekilliflower",
    "item_id_razornuts": "razornuts",
    "item_id_pawpaw": "pawpaw",
    "item_id_sludgeberries": "sludgeberries",
    "item_id_suganmanuts": "suganmanuts",
    "item_id_pinkrowddishes": "pinkrowddishes",
    "item_id_dankwheat": "dankwheat",
    "item_id_brightshade": "brightshade",
    "item_id_blacklimes": "blacklimes",
    "item_id_phosphorpoppies": "phosphorpoppies",
    "item_id_direapples": "direapples",
    "item_id_rustealeaves": "rustealeaves",
    "item_id_metallicaps": "metallicaps",
    "item_id_steelbeans": "steelbeans",
    "item_id_aushucks": "aushucks",

    # vegetable materials
    "item_id_poketubereyes": "poketubereyes",
    "item_id_pulpgourdpulp": "pulpgourdpulp",
    "item_id_sourpotatoskins": "sourpotatoskins",
    "item_id_bloodcabbageleaves": "bloodcabbageleaves",
    "item_id_joybeanvines": "joybeanvines",
    "item_id_purplekilliflowerflorets": "purplekilliflowerflorets",
    "item_id_razornutshells": "razornutshells",
    "item_id_pawpawflesh": "pawpawflesh",
    "item_id_sludgeberrysludge": "sludgeberrysludge",
    "item_id_suganmanutfruit": "suganmanutfruit",
    "item_id_pinkrowddishroot": "pinkrowddishroot",
    "item_id_dankwheatchaff": "dankwheatchaff",
    "item_id_brightshadeberries": "brightshadeberries",
    "item_id_blacklimeade": "blacklimeade",
    "item_id_phosphorpoppypetals": "phosphorpoppypetals",
    "item_id_direapplestems": "direapplestems",
    "item_id_rustealeafblades": "rustealeafblades",
    "item_id_metallicapheads": "metallicapheads",
    "item_id_steelbeanpods": "steelbeanpods",
    "item_id_aushuckstalks": "aushuckstalks",

    # dye ids
    "item_id_dye_black": "blackdye",
    "item_id_dye_pink": "pinkdye",
    "item_id_dye_green": "greendye",
    "item_id_dye_brown": "browndye",
    "item_id_dye_grey": "greydye",
    "item_id_dye_purple": "purpledye",
    "item_id_dye_teal": "tealdye",
    "item_id_dye_orange": "orangedye",
    "item_id_dye_cyan": "cyandye",
    "item_id_dye_red": "reddye",
    "item_id_dye_lime": "limedye",
    "item_id_dye_yellow": "yellowdye",
    "item_id_dye_blue": "bluedye",
    "item_id_dye_magenta": "magentadye",
    "item_id_dye_cobalt": "cobaltdye",
    "item_id_dye_white": "whitedye",
    "item_id_dye_rainbow": "rainbowdye",
    "item_id_paint_copper": "copperpaint",
    "item_id_paint_chrome": "chromepaint",
    "item_id_paint_gold": "goldpaint",

    # weapon ids
    "weapon_id_revolver": 'revolver',
    "weapon_id_dualpistols": 'dualpistols',
    "weapon_id_shotgun": 'shotgun',
    "weapon_id_rifle": 'rifle',
    "weapon_id_smg": 'smg',
    "weapon_id_minigun": 'minigun',
    "weapon_id_bat": 'bat',
    "weapon_id_brassknuckles": 'brassknuckles',
    "weapon_id_katana": 'katana',
    "weapon_id_broadsword": 'broadsword',
    "weapon_id_nunchucks": 'nun-chucks',
    "weapon_id_scythe": 'scythe',
    "weapon_id_yoyo": 'yo-yo',
    "weapon_id_knives": 'knives',
    "weapon_id_molotov": 'molotov',
    "weapon_id_grenades": 'grenades',
    "weapon_id_garrote": 'garrote',
    "weapon_id_pickaxe": 'pickaxe',
    "weapon_id_fishingrod": 'fishingrod',
    "weapon_id_bass": 'bass',
    "weapon_id_umbrella": 'umbrella',
    "weapon_id_bow": 'bow',
    "weapon_id_dclaw": 'dclaw',
    "weapon_id_staff": 'staff',
    "weapon_id_laywaster": 'laywaster',
    "weapon_id_chainsaw": 'chainsaw',

    "weapon_id_spraycan": 'spraycan',
    "weapon_id_paintgun": 'paintgun',
    "weapon_id_paintroller": 'paintroller',
    "weapon_id_paintbrush": 'paintbrush',
    "weapon_id_watercolors": 'watercolors',
    "weapon_id_thinnerbomb": 'thinnerbomb',

    "weapon_id_hoe": 'hoe',
    "weapon_id_pitchfork": 'pitchfork',
    "weapon_id_shovel": 'shovel',
    "weapon_id_slimeringcan": 'slimeringcan',

    "weapon_id_fingernails": 'fingernails',
    "weapon_id_roomba": 'roomba',
    
    "stat_revolver_kills": "revolver_kills",
    "stat_dual_pistols_kills": "dual_pistols_kills",
    "stat_shotgun_kills": "shotgun_kills",
    "stat_rifle_kills": "rifle_kills",
    "stat_smg_kills": "smg_kills",
    "stat_minigun_kills": "miningun_kills",
    "stat_bat_kills": "bat_kills",
    "stat_brassknuckles_kills": "brassknuckles_kills",
    "stat_katana_kills": "katana_kills",
    "stat_broadsword_kills": "broadsword_kills",
    "stat_nunchucks_kills": "nunchucks_kills",
    "stat_scythe_kills": "scythe_kills",
    "stat_yoyo_kills": "yoyo_kills",
    "stat_knives_kills": "knives_kills",
    "stat_molotov_kills": "molotov_kills",
    "stat_grenade_kills": "grenade_kills",
    "stat_garrote_kills": "garrote_kills",
    "stat_pickaxe_kills": "pickaxe_kills",
    "stat_fishingrod_kills": "fishingrod_kills",
    "stat_bass_kills": "bass_kills",
    "stat_bow_kills": "bow_kills",
    "stat_umbrella_kills": "umbrella_kills",
    "stat_dclaw_kills": "dclaw_kills",
    "stat_spraycan_kills": "spraycan_kills",
    "stat_paintgun_kills": "paintgun_kills",
    "stat_paintroller_kills": "paintroller_kills",
    "stat_paintbrush_kills": "paintbrush_kills",
    "stat_watercolor_kills": "watercolor_kills",
    "stat_thinnerbomb_kills": "thinnerbomb_kills",
    "stat_staff_kills": "staff_kills",
    "stat_hoe_kills": "hoe_kills",
    "stat_pitchfork_kills": "pitchfork_kills",
    "stat_shovel_kills": "shovel_kills",
    "stat_slimeringcan_kills": "slimeringcan_kills",
    "stat_fingernails_kills": "fingernails_kills",
    "stat_roomba_kills": "roomba_kills",
    "stat_chainsaw_kills": "chainsaw_kills",
    "stat_megachainsaw_kills": "megachainsaw_kills",
    "vendor_dojo": "Dojo",

    "weapon_class_ammo": "ammo",
    "weapon_class_exploding": "exploding",
    "weapon_class_burning": "burning",
    "weapon_class_captcha": "captcha",
    "weapon_class_defensive": "defensive",
    "weapon_class_paint": "paint",
    # juvies can equip these weapons
    "weapon_class_juvie": "juvie",
    "weapon_class_farming": "farming",
 

    "theforbiddenoneoneone_desc" : "This card that you hold in your hands contains an indescribably powerful being known simply " \
    "as The Forbidden {emote_111}. It is an unimaginable horror, a beast of such supreme might that wields " \
    "destructive capabilities that is beyond any human’s true understanding. And for its power, " \
    "the very fabric of reality conspired to dismember and seal The Forbidden {emote_111} away into the most " \
    "obscured, nightmarish cages conceivable: trading cards. Now you, foolish mortal, have revived " \
    "this ancient evil. Once again this slime-starved beast may roam the lands, obliterating all life " \
    "that dares to evolve.",
    "forbiddenstuffedcrust_eat" : "Dough, pepperoni, grease, marinara and cheese. Those five simple \"ingredients\" folded into one " \
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
    "There is only discord. And then, nothing.",
    "forbiddenstuffedcrust_desc" : "What are you waiting for? You’ve come this far, why do you hesitate? Useless. Useless, useless, useless. " \
    "Escaping your purpose is impossible. Not destiny, purpose. You were never truly alive, never truly free. " \
    "Your one, singular purpose, that you were created to fulfill, is on the precipice of completion. You’ve " \
    "sought that absolution all your life, haven’t you? You’ve begged to be given the answer, to be shown that " \
    "you and your family and your friends were put on this planet for a purpose. Well, here it is. Here is what " \
    "you were meant to do. Don’t fight it. It’s useless. Useless, useless, useless. Don’t keep the universe waiting. " \
    "It’s ready to die. Slather it in some low-quality marinara, toss it up into the air like in the old movies, and " \
    "shove it into the oven, to teach it the true meaning of heat death. Eat a slice of that motherfucking pizza."
}
# def convert(json_name, python_object = "configToConvert")
config = open("C:\\Users\\voupa\\Documents\\GitHub\\endless-war\\json_files\\temp.py", "r+")
string = config.read()
# for key in ITEM_ID.keys():
#     string = string.replace( key, "\""+ ITEM_ID[key] +"\"")
config.close()
while index < len(string):
    # divider = string.find(":", index)
    # if divider == -1:
    #     break
    # tab = string.rfind("\n            ", 0, divider) + 13
    # end_line = string.find("\n", divider)
    # string = string[:tab] + "\"" + string[tab:divider] + "\"" + string[divider:]
    # index = string.find("\n", end_line)

    Ew = string.find("Ew", index)
    if Ew == -1:
        break
    id = string.find("id_", Ew)
    bracket = string.find("(", Ew)
    name_begin = string.find(": \"", id) + 2
    name_end = string.find("\",", name_begin) +1
    line_end = string.find("\n", name_end) + 1
    string = string[:Ew-1] + string[name_begin:name_end] + " : {" + string[bracket+1] + string[line_end:]
    index = line_end
file = open("C:\\Users\\voupa\\Documents\\GitHub\\endless-war\\json_files\\configToConvert.py", "w")
file.write(string)
file.close()