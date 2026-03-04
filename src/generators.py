"""
Module containing a single manager object that is meant to retrieve information
about all generators.
"""


import src._generator as generator
import src.name_generators as name_generators
import src.item_generators as item_generators
import src.npc_generators as npc_generators
import src.monster_generators as monster_generators
import src.dungeon_generators as dungeon_generators
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
                name_generators.TestGenerator,
                ["test.txt"]
            ),
            "dwarves": (
                name_generators.DwarfNameGenerator,
                ["dwarves.txt"]
            ),
            "elves": (
                name_generators.ElfNameGenerator,
                ["elves.txt"]
            ),
            "epithets": (
                name_generators.EpithetGenerator,
                ["epithets.txt"]
            ),
            "humans": (
                name_generators.HumanNameGenerator,
                ["real names.txt", "knave//people.txt"],
                {"*name*": "_get_first_name", "*surname*": "_get_surname"},
            ),
            "inns": (
                name_generators.KnaveInnNameGenerator,
                [],
                {}
            ),
            "locations": (
                name_generators.ToadLocationGenerator,
                [],
                {}
            ),
            "minor-gods": (
                name_generators.ToadMinorGodGenerator,
                [],
                {}
            ),
            "mystic-orders": (
                name_generators.ToadMysticOrderGenerator,
                [],
                {}
            ),
            "spells": (
                name_generators.KnaveSpellGenerator,
                [],
                {}
            ),
        }
        self.item = {
            "magic": (
                item_generators.MagicItemGenerator,
                [],
                {}
            ),
            "fantasy-mundane": (
                item_generators.MundaneFantasyItemGenerator,
                [],
                {}
            ),
            "gems": (
                item_generators.GemGenerator,
                ["rocks.txt"],
            ),
            "wh-scrolls": (
                item_generators.WhitehackScrollGenerator,
                [],
                {},
            ),
            "books": (
                item_generators.KnaveBookGenerator,
                [],
                {}
            )
        }
        self.npc = {
            "fantasy": (
                npc_generators.KnaveFantasyNPCGenerator,
                [],
                {"*mundane item*": "_get_fantasy_mundane"}
            )
        }
        self.monster = {
            "oozes": (
                monster_generators.OozeGenerator,
                ["oozes.txt"],
                {}
            ),
            "knave-monsters" : (
                monster_generators.KnaveMonsterGenerator,
                [],
                {}
            )
        }
        self.dungeon = {
            "basic-mechanical-traps": (
                dungeon_generators.ToadBasicMechanicalTrapGenerator,
                [],
                {
                    "*trap gas*": "_get_trap_gas",
                    "*missile trap*": "_get_missile_trap",
                    "*pit trap*": "_get_pit_trap"
                }
            ),
            "missile-traps": (
                dungeon_generators.ToadMissileTrapGenerator,
                [],
                {}
            ),
            "pit-traps" :(
                dungeon_generators.ToadPitTrapGenerator,
                [],
                {
                    "*ooze*": "_get_ooze",
                }
            ),
            "trap-gasses": (
                dungeon_generators.ToadTrapGasGenerator,
                [],
                {}
            )
        }
        self.misc = {
            "plants": (
                misc_generators.PlantGenerator,
                ["herbs.txt"]
            ),
            "magic-symbols": (
                misc_generators.ToadMagicSymbolGenerator,
                [],
                {}
            ),
            "clues": (
                misc_generators.ToadClueGenerator,
                [],
                {
                    "*writing*": "_get_writing",
                    "*monster*": "_get_monster",
                }
            ),
            "writing": (
                misc_generators.ToadWritingGenerator,
                [],
                {
                    "*knave book*": "_get_knave_book",
                    "*item*": "_get_item",
                }
            )
        }

        self.generators_by_type = {
            "name": self.name,
            "item": self.item,
            "npc": self.npc,
            "monster": self.monster,
            "dungeon": self.dungeon,
            "misc": self.misc,
        }


def get_generator(generator_type: str,
                  generator_name: str,
                  *,
                  force_update: bool=False,
                  ) -> generator.Generator:
    """\
    Get a generator instance by specifying the type and name.\
    """
    library = GeneratorLibrary().generators_by_type
    gen_class, *init_args = library[generator_type][generator_name]
    return gen_class(force_update, *init_args)
