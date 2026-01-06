"""
Module containing a single manager object that is meant to retrieve information
about all generators.
"""


import src.name_generators as name_generators
import src.item_generators as item_generators
import src.npc_generators as npc_generators
import src.monster_generators as monster_generators
import src.misc_generators as misc_generators


class GeneratorLibrary:
    """
    Stores information on all generators so they can be easily used across the
    program. I have to make this a class so that I can avoid import errors.
    """
    def __init__(self):
        # Each entry for a given generator type is saved in a dictionary, the
        # key is the name of the generator rendered as a string, this is used
        # in main by typing the name into the command line (although it's easy
        # enough to use elsewhere). The Value is a tuple, the first entry is
        # always the generator class itself, while all other tuple entries
        # (if they exist) are arguments used to initiate the generator class.
        self.name = {
            "test": (
                name_generators.Test,
                ["test.txt"]
            ),
            "dwarves": (
                name_generators.Dwarves,
                ["dwarves.txt"]
            ),
            "elves": (
                name_generators.Elves,
                ["elves.txt"]
            ),
            "epithets": (
                name_generators.Epithets,
                ["epithets.txt"]
            ),
            "humans": (
                name_generators.Humans,
                ["real names.txt", "people.txt"],
                {"*name*": "_get_first_name", "*surname*": "_get_surname"},
            ),
            "inn": (
                name_generators.Inn,
                [],
                {}
            ),
            "locations": (
                name_generators.Locations,
                ["locations.txt"]
            ),
            "minor-gods": (
                name_generators.MinorGods,
                ["minor gods.txt"]
            ),
            "mystic-orders": (
                name_generators.MysticOrders,
                ["mystic orders.txt"]
            ),
            "spells": (
                name_generators.Spells,
                [],
                {}
            ),
        }
        self.item = {
            "magic": (
                item_generators.Magic,
                [],
                {}
            ),
            "fantasy-mundane": (
                item_generators.FantasyMundane,
                [],
                {}
            )
        }
        self.npc = {
            "fantasy": (
                npc_generators.FantasyNPCs,
                [],
                {"*mundane item*": "_get_fantasy_mundane"},
            )
        }
        self.monster = {
            "oozes": (
                monster_generators.Oozes,
                ["oozes.txt"],
                {}
            ),
        }
        self.misc = {
            "plants": (
                misc_generators.Plant,
                ["herbs.txt"]
            )
        }

        self.generators_by_type = {
            "name": self.name,
            "item": self.item,
            "npc": self.npc,
            "monster": self.monster,
            "misc": self.misc
        }
