""" Package containing all the class modules.\n
    Classes:
        'EwBasic' -- Basic class at the top of the hierarqy with general attributes and methods\n
        'EwCharacter' -- Basic object class for all game characters: enemies, players, etc.\n
        'EwResponse' -- Basic object class to handle text responses from the bot\n
        'EwDiscordUSer' -- Basic object class for discord interaction specific to the game\n
        
"""
from ewClass.BaseClass import EwBasic, EwCharacter, EwDiscordUser, EwResponse
from ewClass.CharacterInteraction import EwEnemy, EwPlayer
from ewClass import EwApartment
from ewClass import cmd
from ewClass import furniture
from ewClass import id
from ewClass import user
from ewClass import district
from ewClass import event
from ewClass import dungeonevent
from ewClass import offer