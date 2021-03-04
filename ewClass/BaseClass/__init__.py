""" Package with all the most high level class modules, for organization purposes \n
    Classes:
        'EwBasic' -- Basic class at the top of the hierarqy with general attributes and methods\n
        'EwCharacter' -- Basic object class for all game characters: enemies, players, etc.\n
        'EwResponse' -- Basic object class to handle text responses from the bot\n
        'EwDiscordUSer' -- Basic object class for discord interaction specific to the game\n
"""
from ewClass.BaseClass.basic import EwBasic
from ewClass.BaseClass.character import EwCharacter
from ewClass.BaseClass.message import EwResponse
from ewClass.BaseClass.discord_user import EwDiscordUser