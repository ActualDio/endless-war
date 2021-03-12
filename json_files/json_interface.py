
import json
import os
import glob
JSON_TAG_START = "# ==._*/JSON_TAG_START\*_.==\n"
JSON_TAG_END = "# ==._*/JSON_TAG_END\*_.==\n"
ITEM_ID = {
    "emote_tacobell": "<:tacobell:431273890195570699>",
    "emote_pizzahut": "<:pizzahut:431273890355085323>",
    "emote_kfc": "<:kfc:431273890216673281>",
    "emote_moon": "<:moon:431418525303963649>",
    "emote_111": "<:111:431547758181220377>",

    "emote_copkiller": "<:copkiller:431275071945048075>",
    "emote_rowdyfucker": "<:rowdyfucker:431275088076079105>",
    "emote_ck": "<:ck:504173691488305152>",
    "emote_rf": "<:rf:504174176656162816>",

    "emote_theeye": "<:theeye:431429098909466634>",
    "emote_slime1": "<:slime1:431564830541873182>",
    "emote_slime2": "<:slime2:431570132901560320>",
    "emote_slime3": "<:slime3:431659469844381717>",
    "emote_slime4": "<:slime4:431570132901560320>",
    "emote_slime5": "<:slime5:431659469844381717>",
    "emote_slimeskull": "<:slimeskull:431670526621122562>",
    "emote_slimeheart": "<:slimeheart:431673472687669248>",
    "emote_dice1": "<:dice1:436942524385329162>",
    "emote_dice2": "<:dice2:436942524389654538>",
    "emote_dice3": "<:dice3:436942524041527298>",
    "emote_dice4": "<:dice4:436942524406300683>",
    "emote_dice5": "<:dice5:436942524444049408>",
    "emote_dice6": "<:dice6:436942524469346334>",
    "emote_negaslime": "<:ns:453826200616566786>",
    "emote_bustin": "<:bustin:455194248741126144>",
    "emote_ghost": "<:lordofghosts:434002083256205314>",
    "emote_slimefull": "<:slimefull:496397819154923553>",
    "emote_purple": "<:purple:496397848343216138>",
    "emote_pink": "<:pink:496397871180939294>",
    "emote_slimecoin": "<:slimecoin:440576133214240769>",
    "emote_slimegun": "<:slimegun:436500203743477760>",
    "emote_slimeshot": "<:slimeshot:436604890928644106>",
    "emote_slimecorp": "<:slimecorp:568637591847698432>",
    "emote_nlacakanm": "<:nlacakanm:499615025544298517>",
    "emote_megaslime": "<:megaslime:436877747240042508>",
    "emote_srs": "<:srs:631859962519224341>",
    "emote_staydead": "<:sd:506840095714836480>",
    "emote_janus1": "<:janus1:694404178956779592>",
    "emote_janus2": "<:janus2:694404179342655518>",
    "emote_masterpoudrin": "<:masterpoudrin:694788959418712114>",
    "emote_poketubers": "<:c_poketubers:706989587112787998>",
    "emote_pulpgourds": "<:c_pulpgourds:706989587469172746>",
    "emote_sourpotatoes": "<:c_sourpotatoes:706989587196543067>",
    "emote_bloodcabbages": "<:c_bloodcabbages:706989586475253832>",
    "emote_joybeans": "<:c_joybeans:706989586949210223>",
    "emote_killiflower": "<:c_killiflower:706989587003736114>",
    "emote_razornuts": "<:c_razornuts:706989587129434364>",
    "emote_pawpaw": "<:c_pawpaw:706989587137953812>",
    "emote_sludgeberries": "<:c_sludgeberries:706989587205062656>",
    "emote_suganmanuts": "<:c_suganmanuts:706989587276234862>",
    "emote_pinkrowddishes": "<:c_pinkrowddishes:706989586684969091>",
    "emote_dankwheat": "<:c_dankwheat:706989586714460222>",
    "emote_brightshade": "<:c_brightshade:706989586676580373>",
    "emote_blacklimes": "<:c_blacklimes:706989586890489947>",
    "emote_phosphorpoppies": "<:c_phosphorpoppies:706989586898878496>",
    "emote_direapples": "<:c_direapples:706989586928238663>",
    "emote_rustealeaves": "<:c_rustealeaves:743337308295790642>",
    "emote_metallicaps": "<:c_metallicaps:743337308228419714>",
    "emote_steelbeans": "<:c_steelbeans:743337307968372757>",
    "emote_aushucks": "<:c_aushucks:743337307859320923>",
    "emote_blankregional": "<:bl:747207921926144081>",
    "emote_greenlawn": "<:gr:726271625489809411>",
    "emote_limelawn": "<:li:726271664815472692>",
    "emote_frozentile": "<:ft:743276248381259846>",

    # Emotes for the negaslime writhe animation
    "emote_vt": "<:vt:492067858160025600>",
    "emote_ve": "<:ve:492067844930928641>",
    "emote_va": "<:va:492067850878451724>",
    "emote_v_": "<:v_:492067837565861889>",
    "emote_s_": "<:s_:492067830624157708>",
    "emote_ht": "<:ht:492067823150039063>",
    "emote_hs": "<:hs:492067783396294658>",
    "emote_he": "<:he:492067814933266443>",
    "emote_h_": "<:h_:492067806465228811>",
    "emote_blank": "<:blank:570060211327336472>",

    # Emotes for troll romance
    "emote_maws": "<:q_maws:752228834027241554>",
    "emote_hats": "<:q_hats:752228833968783441>",
    "emote_slugs": "<:q_slugs:752228834333556756>",
    "emote_shields": "<:q_shields:752228833897218159>",
    "emote_broken_heart": ":broken_heart:",

    # Emotes for minesweeper
    "emote_ms_hidden": ":pick:",
    "emote_ms_mine": ":x:",
    "emote_ms_flagged": ":triangular_flag_on_post:",
    "emote_ms_0": ":white_circle:",
    "emote_ms_1": ":heart:",
    "emote_ms_2": ":yellow_heart:",
    "emote_ms_3": ":green_heart:",
    "emote_ms_4": ":blue_heart:",
    "emote_ms_5": ":purple_heart:",
    "emote_ms_6": ":six:",
    "emote_ms_7": ":seven:",
    "emote_ms_8": ":eight:",

    # Emote for deleting slime tweets
    "emote_delete_tweet": "<:blank:570060211327336472>",
    # Slime twitter verified checkmark
    "emote_verified": "<:slime_checkmark:797234128398319626>",

    "event_type_slimeglob": "slimeglob",
    "event_type_slimefrenzy": "slimefrenzy",
    "event_type_poudrinfrenzy": "poudrinfrenzy",
    "event_type_minecollapse": "minecollapse",
    "event_type_voidhole": "voidhole",
    "event_type_voidconnection": "voidconnection",
    "event_type_shambaquarium": "shambaquarium",
    "rarity_plebeian": "Plebeian",
    "rarity_patrician": "Patrician",
    "rarity_promotional": "Promotional",
    "rarity_princeps": "princeps",

    "enemy_attacktype_unarmed": "unarmed",
    "enemy_attacktype_fangs": "fangs",
    "enemy_attacktype_talons": "talons",
    "enemy_attacktype_tusks": "tusks",
    "enemy_attacktype_raiderscythe": "scythe",
    "enemy_attacktype_gunkshot": "gunkshot",
    "enemy_attacktype_molotovbreath": "molotovbreath",
    "enemy_attacktype_armcannon": "armcannon",
    "enemy_attacktype_axe": "axe",
    "enemy_attacktype_hooves": "hooves",
    "enemy_attacktype_body": "body",

    "enemy_attacktype_amateur": "amateur",

    "enemy_attacktype_gvs_g_seeds": "g_seeds",
    "enemy_attacktype_gvs_g_appleacid": "g_appleacid",
    "enemy_attacktype_gvs_g_bloodshot": "g_bloodshot",
    "enemy_attacktype_gvs_g_nuts": "g_nuts",
    "enemy_attacktype_gvs_g_chompers": "g_chompers",
    "enemy_attacktype_gvs_g_fists": "g_fists",
    "enemy_attacktype_gvs_g_brainwaves": "g_brainwaves",
    "enemy_attacktype_gvs_g_vapecloud": "g_vapecloud",
    "enemy_attacktype_gvs_g_hotbox": "g_hotbox",
    "enemy_attacktype_gvs_g_blades": "g_blades",
    "enemy_attacktype_gvs_g_explosion": "g_explosion",

    "enemy_attacktype_gvs_s_shamboni": "s_shamboni",
    "enemy_attacktype_gvs_s_teeth": "s_teeth",
    "enemy_attacktype_gvs_s_tusks": "s_tusks",
    "enemy_attacktype_gvs_s_fangs": "s_fangs",
    "enemy_attacktype_gvs_s_talons": "s_talons",
    "enemy_attacktype_gvs_s_molotovbreath": "s_molotovbreath",
    "enemy_attacktype_gvs_s_raiderscythe": "s_scythe",
    "enemy_attacktype_gvs_s_cudgel": "s_cudgel",
    "enemy_attacktype_gvs_s_grenadecannon": "s_grenadecannon",

    "enemy_weathertype_normal": "normal",
    "enemy_weathertype_rainresist": "rainresist",

    "enemy_type_juvie": "juvie",
    "enemy_type_dinoslime": "dinoslime",

    "enemy_type_slimeadactyl": "slimeadactyl",
    "enemy_type_desertraider": "desertraider",
    "enemy_type_mammoslime": "mammoslime",

    "enemy_type_microslime": "microslime",
    "enemy_type_slimeofgreed": "slimeofgreed",

    "enemy_type_megaslime": "megaslime",
    "enemy_type_slimeasaurusrex": "slimeasaurusrex",
    "enemy_type_greeneyesslimedragon": "greeneyesslimedragon",
    "enemy_type_unnervingfightingoperator": "unnervingfightingoperator",

    "enemy_type_civilian": "civilian",
    "enemy_type_civilian_innocent": "innocent",

    "enemy_type_gaia_poketubers": "poketubers",
    "enemy_type_gaia_pulpgourds": "pulpgourds",
    "enemy_type_gaia_sourpotatoes": "sourpotatoes",
    "enemy_type_gaia_bloodcabbages": "bloodcabbages",
    "enemy_type_gaia_joybeans": "joybeans",
    "enemy_type_gaia_purplekilliflower": "purplekilliflower",
    "enemy_type_gaia_razornuts": "razornuts",
    "enemy_type_gaia_pawpaw": "pawpaw",
    "enemy_type_gaia_sludgeberries": "sludgeberries",
    "enemy_type_gaia_suganmanuts": "suganmanuts",
    "enemy_type_gaia_pinkrowddishes": "pinkrowddishes",
    "enemy_type_gaia_dankwheat": "dankwheat",
    "enemy_type_gaia_brightshade": "brightshade",
    "enemy_type_gaia_blacklimes": "blacklimes",
    "enemy_type_gaia_phosphorpoppies": "phosphorpoppies",
    "enemy_type_gaia_direapples": "direapples",
    "enemy_type_gaia_rustealeaves": "rustealeaves",
    "enemy_type_gaia_metallicaps": "metallicaps",
    "enemy_type_gaia_steelbeans": "steelbeans",
    "enemy_type_gaia_aushucks": "aushucks",

    "enemy_type_defaultshambler": "defaultshambler",
    "enemy_type_bucketshambler": "bucketshambler",
    "enemy_type_juveolanternshambler": "juveolanternshambler",
    "enemy_type_flagshambler": "flagshambler",
    "enemy_type_shambonidriver": "shambonidriver",
    "enemy_type_mammoshambler": "mammoshambler",
    "enemy_type_gigashambler": "gigashambler",
    "enemy_type_microshambler": "microshambler",
    "enemy_type_shamblersaurusrex": "shamblesaurusrex",
    "enemy_type_shamblerdactyl": "shamblerdactyl",
    "enemy_type_dinoshambler": "dinoshambler",
    "enemy_type_ufoshambler": "ufoshambler",
    "enemy_type_brawldenboomer": "brawldenboomer",
    "enemy_type_juvieshambler": "juvieshambler",
    "enemy_type_shambleballplayer": "shambleballplayer",
    "enemy_type_shamblerwarlord": "shamblerwarlord",
    "enemy_type_shamblerraider": "shamblerraider",
    "enemy_type_gvs_boss": "blueeyesshamblerdragon",

    "enemy_type_sandbag": "sandbag",

    "enemy_type_doubleheadlessdoublehorseman": "doubleheadlessdoublehorseman",
    "enemy_type_doublehorse": "doublehorse",

    "enemy_ai_sandbag": "Sandbag",
    "enemy_ai_coward": "Coward",
    "enemy_ai_attacker_a": "Attacker-A",
    "enemy_ai_attacker_b": "Attacker-B",
    "enemy_ai_defender": "Defender",
    "enemy_ai_gaiaslimeoid": "Gaiaslimeoid",
    "enemy_ai_shambler": "Shambler",

    "enemy_class_normal": "normal",
    "enemy_class_gaiaslimeoid": "gaiaslimeoid",
    "enemy_class_shambler": "shambler",

    "trauma_id_suicide": "suicide",
    "trauma_id_betrayal": "betrayal",
    "trauma_id_environment": "environment",

    "trauma_class_slimegain": "slimegain",
    "trauma_class_damage": "damage",

    "trauma_class_sapregeneration": "sapgen",
    "trauma_class_accuracy": "accuracy",
    "trauma_class_bleeding": "bleeding",
    "trauma_class_movespeed": "movespeed",
    "trauma_class_hunger": "hunger",

    "acquisition_smelting": "smelting",
    "acquisition_milling": "milling",
    "acquisition_mining": "mining",
    "acquisition_dojo": "dojo",
    "acquisition_fishing": "fishing",
    "acquisition_bartering": "bartering",
    "acquisition_trickortreating": "trickortreating",
    "acquisition_bazaar": "bazaar",

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

    "weather_sunny": "sunny",
    "weather_rainy": "rainy",
    "weather_windy": "windy",
    "weather_lightning": "lightning",
    "weather_cloudy": "cloudy",
    "weather_snow": "snow",
    "weather_foggy": "foggy",
    "weather_bicarbonaterain": "bicarbonaterain",

    "theforbiddenoneoneone_desc": "This card that you hold in your hands contains an indescribably powerful being known simply " \
    "as The Forbidden {emote_111}. It is an unimaginable horror, a beast of such supreme might that wields " \
    "destructive capabilities that is beyond any human’s true understanding. And for its power, " \
    "the very fabric of reality conspired to dismember and seal The Forbidden {emote_111} away into the most " \
    "obscured, nightmarish cages conceivable: trading cards. Now you, foolish mortal, have revived " \
    "this ancient evil. Once again this slime-starved beast may roam the lands, obliterating all life " \
    "that dares to evolve.",
    "forbiddenstuffedcrust_eat": "Dough, pepperoni, grease, marinara and cheese. Those five simple \"ingredients\" folded into one " \
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
    "forbiddenstuffedcrust_desc": "What are you waiting for? You’ve come this far, why do you hesitate? Useless. Useless, useless, useless. " \
    "Escaping your purpose is impossible. Not destiny, purpose. You were never truly alive, never truly free. " \
    "Your one, singular purpose, that you were created to fulfill, is on the precipice of completion. You’ve " \
    "sought that absolution all your life, haven’t you? You’ve begged to be given the answer, to be shown that " \
    "you and your family and your friends were put on this planet for a purpose. Well, here it is. Here is what " \
    "you were meant to do. Don’t fight it. It’s useless. Useless, useless, useless. Don’t keep the universe waiting. " \
    "It’s ready to die. Slather it in some low-quality marinara, toss it up into the air like in the old movies, and " \
    "shove it into the oven, to teach it the true meaning of heat death. Eat a slice of that motherfucking pizza.",

    "poi_id_thesewers": "thesewers",
    "poi_id_slimeoidlab": "slimecorpslimeoidlaboratory",
    "poi_id_realestate": "realestateagency",
    "poi_id_glocksburycomics": "glocksburycomics",
    "poi_id_slimypersuits": "slimypersuits",
    "poi_id_mine": "themines",
    "poi_id_mine_sweeper": "theminessweeper",
    "poi_id_mine_bubble": "theminesbubble",
    "poi_id_thecasino": "thecasino",
    "poi_id_711": "outsidethe711",
    "poi_id_speakeasy": "thekingswifessonspeakeasy",
    "poi_id_dojo": "thedojo",
    "poi_id_arena": "thebattlearena",
    "poi_id_nlacu": "newlosangelescityuniversity",
    "poi_id_foodcourt": "thefoodcourt",
    "poi_id_cinema": "nlacakanmcinemas",
    "poi_id_bazaar": "thebazaar",
    "poi_id_recyclingplant": "recyclingplant",
    "poi_id_stockexchange": "theslimestockexchange",
    "poi_id_endlesswar": "endlesswar",
    "poi_id_slimecorphq": "slimecorphq",
    "poi_id_cv_mines": "cratersvillemines",
    "poi_id_cv_mines_sweeper": "cratersvilleminessweeper",
    "poi_id_cv_mines_bubble": "cratersvilleminesbubble",
    "poi_id_tt_mines": "toxingtonmines",
    "poi_id_tt_mines_sweeper": "toxingtonminessweeper",
    "poi_id_tt_mines_bubble": "toxingtonminesbubble",
    "poi_id_diner": "smokerscough",
    "poi_id_seafood": "redmobster",
    "poi_id_jr_farms": "juviesrowfarms",
    "poi_id_og_farms": "oozegardensfarms",
    "poi_id_ab_farms": "arsonbrookfarms",
    "poi_id_neomilwaukeestate": "neomilwaukeestate",
    "poi_id_beachresort": "thebeachresort",
    "poi_id_countryclub": "thecountryclub",
    "poi_id_slimesea": "slimesea",
    "poi_id_slimesendcliffs": "slimesendcliffs",
    "poi_id_greencakecafe": "greencakecafe",
    "poi_id_sodafountain": "sodafountain",
    "poi_id_bodega": "bodega",
    "poi_id_wafflehouse": "wafflehouse",
    "poi_id_blackpond": "blackpond",
    "poi_id_basedhardware": "basedhardware",
    "poi_id_clinicofslimoplasty": "clinicofslimoplasty",
    "poi_id_thebreakroom": "thebreakroom",
    "poi_id_underworld": "underworld",
    "poi_id_ferry": "ferry",
    "poi_id_subway_pink01": "subwaypink01",
    "poi_id_subway_pink02": "subwaypink02",
    "poi_id_subway_gold01": "subwaygold01",
    "poi_id_subway_gold02": "subwaygold02",
    "poi_id_subway_green01": "subwaygreen01",
    "poi_id_subway_green02": "subwaygreen02",
    "poi_id_subway_black01": "subwayblack01",
    "poi_id_subway_black02": "subwayblack01",
    "poi_id_subway_purple01": "subwaypurple01",
    "poi_id_subway_purple02": "subwaypurple02",
    "poi_id_blimp": "blimp",
    "poi_id_apt": "apt",
    "poi_id_wt_port": "wreckingtonport",
    "poi_id_vc_port": "vagrantscornerport",
    "poi_id_tt_subway_station": "toxingtonsubwaystation",
    "poi_id_ah_subway_station": "astatineheightssubwaystation",
    "poi_id_gd_subway_station": "gatlingsdalesubwaystation",
    "poi_id_ck_subway_station": "copkilltownsubwaystation",
    "poi_id_ab_subway_station": "arsonbrooksubwaystation",
    "poi_id_sb_subway_station": "smogsburgsubwaystation",
    "poi_id_dt_subway_station": "downtownsubwaystation",
    "poi_id_kb_subway_station": "krakbaysubwaystation",
    "poi_id_gb_subway_station": "glocksburysubwaystation",
    "poi_id_wgb_subway_station": "westglocksburysubwaystation",
    "poi_id_jp_subway_station": "jaywalkerplainsubwaystation",
    "poi_id_nsb_subway_station": "northsleezesubwaystation",
    "poi_id_ssb_subway_station": "southsleezesubwaystation",
    "poi_id_bd_subway_station": "brawldensubwaystation",
    "poi_id_cv_subway_station": "cratersvillesubwaystation",
    "poi_id_wt_subway_station": "wreckingtonsubwaystation",
    "poi_id_rr_subway_station": "rowdyroughhousesubwaystation",
    "poi_id_gld_subway_station": "greenlightsubwaystation",
    "poi_id_jr_subway_station": "juviesrowsubwaystation",
    "poi_id_vc_subway_station": "vagrantscornersubwaystation",
    "poi_id_afb_subway_station": "assaultflatssubwaystation",
    "poi_id_vp_subway_station": "vandalparksubwaystation",
    "poi_id_pa_subway_station": "poudrinalleysubwaystation",
    "poi_id_og_subway_station": "oozegardenssubwaystation",
    "poi_id_cl_subway_station": "crooklinesubwaystation",
    "poi_id_lc_subway_station": "littlechernobylsubwaystation",
    "poi_id_bd_subway_station": "brawldensubwaystation",
    "poi_id_nny_subway_station": "newnewyonkerssubwaystation",
    "poi_id_underworld_subway_station": "underworldsubwaystation",
    "poi_id_df_blimp_tower": "dreadfordblimptower",
    "poi_id_afb_blimp_tower": "assaultflatsblimptower",
    "poi_id_downtown": "downtown",
    "poi_id_smogsburg": "smogsburg",
    "poi_id_copkilltown": "copkilltown",
    "poi_id_krakbay": "krakbay",
    "poi_id_poudrinalley": "poudrinalley",
    "poi_id_rowdyroughhouse": "rowdyroughhouse",
    "poi_id_greenlightdistrict": "greenlightdistrict",
    "poi_id_oldnewyonkers": "oldnewyonkers",
    "poi_id_littlechernobyl": "littlechernobyl",
    "poi_id_arsonbrook": "arsonbrook",
    "poi_id_astatineheights": "astatineheights",
    "poi_id_gatlingsdale": "gatlingsdale",
    "poi_id_vandalpark": "vandalpark",
    "poi_id_glocksbury": "glocksbury",
    "poi_id_northsleezeborough": "northsleezeborough",
    "poi_id_southsleezeborough": "southsleezeborough",
    "poi_id_oozegardens": "oozegardens",
    "poi_id_cratersville": "cratersville",
    "poi_id_wreckington": "wreckington",
    "poi_id_juviesrow": "juviesrow",
    "poi_id_slimesend": "slimesend",
    "poi_id_vagrantscorner": "vagrantscorner",
    "poi_id_assaultflatsbeach": "assaultflatsbeach",
    "poi_id_newnewyonkers": "newnewyonkers",
    "poi_id_brawlden": "brawlden",
    "poi_id_toxington": "toxington",
    "poi_id_charcoalpark": "charcoalpark",
    "poi_id_poloniumhill": "poloniumhill",
    "poi_id_westglocksbury": "westglocksbury",
    "poi_id_jaywalkerplain": "jaywalkerplain",
    "poi_id_crookline": "crookline",
    "poi_id_dreadford": "dreadford",
    "poi_id_maimridge": "maimridge",
    "poi_id_thevoid": "thevoid",
    "poi_id_toxington_pier": "toxingtonpier",
    "poi_id_jaywalkerplain_pier": "jaywalkerplainpier",
    "poi_id_crookline_pier": "crooklinepier",
    "poi_id_assaultflatsbeach_pier": "assaultflatsbeachpier",
    "poi_id_vagrantscorner_pier": "vagrantscornerpier",
    "poi_id_slimesend_pier": "slimesendpier",
    "poi_id_juviesrow_pier": "juviesrowpier",
    "poi_id_apt_downtown": "aptdowntown",
    "poi_id_apt_smogsburg": "aptsmogsburg",
    "poi_id_apt_krakbay": "aptkrakbay",
    "poi_id_apt_poudrinalley": "aptpoudrinalley",
    "poi_id_apt_greenlightdistrict": "aptgreenlightdistrict",
    "poi_id_apt_oldnewyonkers": "aptoldnewyonkers",
    "poi_id_apt_littlechernobyl": "aptlittlechernobyl",
    "poi_id_apt_arsonbrook": "aptarsonbrook",
    "poi_id_apt_astatineheights": "aptastatineheights",
    "poi_id_apt_gatlingsdale": "aptgatlingsdale",
    "poi_id_apt_vandalpark": "aptvandalpark",
    "poi_id_apt_glocksbury": "aptglocksbury",
    "poi_id_apt_northsleezeborough": "aptnorthsleezeborough",
    "poi_id_apt_southsleezeborough": "aptsouthsleezeborough",
    "poi_id_apt_oozegardens": "aptoozegardens",
    "poi_id_apt_cratersville": "aptcratersville",
    "poi_id_apt_wreckington": "aptwreckington",
    "poi_id_apt_slimesend": "aptslimesend",
    "poi_id_apt_vagrantscorner": "aptvagrantscorner",
    "poi_id_apt_assaultflatsbeach": "aptassaultflatsbeach",
    "poi_id_apt_newnewyonkers": "aptnewnewyonkers",
    "poi_id_apt_brawlden": "aptbrawlden",
    "poi_id_apt_toxington": "apttoxington",
    "poi_id_apt_charcoalpark": "aptcharcoalpark",
    "poi_id_apt_poloniumhill": "aptpoloniumhill",
    "poi_id_apt_westglocksbury": "aptwestglocksbury",
    "poi_id_apt_jaywalkerplain": "aptjaywalkerplain",
    "poi_id_apt_crookline": "aptcrookline",
    "poi_id_apt_dreadford": "aptdreadford",
    "poi_id_apt_maimridge": "aptmaimridge",
    "transport_type_ferry": "ferry",
    "transport_type_subway": "subway",
    "transport_type_blimp": "blimp",
    "transport_line_ferry_wt_to_vc": "ferrywttovc",
    "transport_line_ferry_vc_to_wt": "ferryvctowt",
    "transport_line_subway_yellow_northbound": "subwayyellownorth",
    "transport_line_subway_yellow_southbound": "subwayyellowsouth",
    "transport_line_subway_red_northbound": "subwayrednorth",
    "transport_line_subway_red_southbound": "subwayredsouth",
    "transport_line_subway_blue_eastbound": "subwayblueeast",
    "transport_line_subway_blue_westbound": "subwaybluewest",
    "transport_line_subway_white_eastbound": "subwaywhiteeast",
    "transport_line_subway_white_westbound": "subwaywhitewest",
    "transport_line_subway_green_eastbound": "subwaygreeneast",
    "transport_line_subway_green_westbound": "subwaygreenwest",
    "transport_line_blimp_df_to_afb": "blimpdftoafb",
    "transport_line_blimp_afb_to_df": "blimpafbtodf"
}
key_dict = {}
vegetable_list = ["poketubers",
                  "pulpgourds",
                  "sourpotatoes",
                  "bloodcabbages",
                  "joybeans",
                  "purplekilliflower",
                  "razornuts",
                  "pawpaw",
                  "sludgeberries",
                  "suganmanuts",
                  "pinkrowddishes",
                  "dankwheat",
                  "brightshade",
                  "blacklimes",
                  "phosphorpoppies",
                  "direapples",
                  "rustealeaves",
                  "metallicaps",
                  "steelbeans",
                  "aushucks"]
inner_dict = ["props", "permissions", "neighbors", "schedule", "effectiveness", "ingredients","fn_effect", "tool_props"]


class Tree_node:
    """Object class for the creation of a navigation tree of the json files \n
    """
    root = None
    branches = []
    key_name = ""
    path = ""

    def __init__(self,
                 root=None,
                 key_name="",
                 branches=[],
                 path=""):

        # create the top of the tree
        if root == None and key_name == "" and branches == [] and path == "":
            self.root = root
            self.branches = branches
            self.key_name = "Root"
            self.path = path
        elif root != None and key_name != "":
            self.root = root
            self.key_name = key_name
            root.append_branch(self)
            self.branches = []

    def append_branch(self, node):
        """Adds a branch to the node that calls it \n

        Arguments:
            'node': Tree_node -- The node to be added as a branch \n
        """
        self.branches.append(node)
        node.path = self.path + "\\" + node.key_name
        if node.key_name in key_dict.keys():
            x = 1
        else:
            key_dict.update({node.key_name: node})

    def remove_branch(self, index):
        """Remove a branch from this root node \n

        Arguments:
            'index': int -- Index for the position in the branch list you want to remove \n
        """
        to_remove = self.branches[index]
        for element in self.branches[index+1:]:
            element.path = element.root.path + str(self.index)

        del key_dict[to_remove.key_name]
        del self.branches[index]


def iterate_dict(dictionary, root):
    for key in dictionary.keys():
        try:
            dictionary[key].keys()
            if key in inner_dict:
                continue
            if key in vegetable_list:
                key = key + root.path[:root.path.find(".json")]
            node = Tree_node(root=root, key_name=key)
            iterate_dict(dictionary[key], node)
        except:
            continue


def create_tree():
    """Creates a tree data structure for accessing the json indexes and keys \n
    """
    # Get the current folder's file-path
    dir = "C:\\Users\\voupa\\Documents\\GitHub\\endless-war\\json_files"
    # Get all the json files in the current folder
    files = glob.glob(dir + "\\*.json")
    top_root = Tree_node()
    for path in files:
        f = open(path, "r")
        loaded_dict = json.load(f)
        f.close()
        branch = Tree_node(root=top_root, key_name=path[path.rfind("\\")+1:])
        iterate_dict(loaded_dict, branch)


# Testing
create_tree()
file = open("ewcfg.py", "r")
config = file.read()
file.close()
start_of_section = config.rfind(JSON_TAG_START) + len(JSON_TAG_START)
end_of_section = config.rfind(JSON_TAG_END)
id_section = config[start_of_section:end_of_section]
id_section = id_section.replace("\'", "\"")
file = open("ewcfg.py", "r")
lines = file.readlines()
file.close()
printing = ""
for line in lines:
    if line.find(" = '") != -1:
        id = line[line.find(" = '")+4:line.find("'\n")]
        if id in key_dict.keys():
            config = config[:config.find(line)] + config[config.find(line)+len(line):]
            start_of_section = config.rfind(JSON_TAG_START) + len(JSON_TAG_START)
            end_of_section = config.rfind(JSON_TAG_END)
            id_section = id_section + line
config = config[:start_of_section] + id_section + config[end_of_section:]
file = open("ewcfg.py", "w")
file.write(config)
file.close()