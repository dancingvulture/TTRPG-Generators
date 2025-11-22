"""
Contains all needed command line objects.
"""


import argparse
from src.generators import GeneratorLibrary


_KEYWORD_ARGS = {
    "help": ("Results must contain these words; syntax for this command: "
              "separate each keyword with a commas, but with no spaces"),
    "type": lambda keywords: [x for x in keywords.lower().split(',')]
}
_MAXTIME_ARGS = {
    "type": float,
    "help": ("Maximum time the program tries to generate "
              "names for in seconds, default is 5."),
    "default": 5.0
}
_FORCE_UPDATE_ARGS = {
    "help": "Force update of generator's table file.",
    "action": "store_true",
    "default": None
}
_COUNT_ARGS = {
    "type": int,
    "help": "Number to generate."
}


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="TTRPG Generator",
        description="Essentially a set of random tables to use for help with"
                    " prepping TTRPG games. All output is ultimately text in"
                    " the terminal."
    )
    subparsers = parser.add_subparsers(
        help="Choose your generator type.",
        dest="type"
    )
    library = GeneratorLibrary()

    _add_name_subparser(subparsers, library)
    _add_item_subparser(subparsers, library)
    _add_npc_subparser(subparsers, library)

    return parser.parse_args()


def _add_name_subparser(subparsers, library: GeneratorLibrary) -> None:
    """
    Subparser for using the name generators.
    """
    parser = subparsers.add_parser(
        "name",
        help="Generate names.",
    )
    generator_names = library.name.keys()

    parser.add_argument(
        "generator",
        choices=generator_names,
        help="choose a generator."
    )
    parser.add_argument("-kw", "--keywords", **_KEYWORD_ARGS)
    parser.add_argument("-mt", "--maxtime", **_MAXTIME_ARGS)
    parser.add_argument("-up", "--update", **_FORCE_UPDATE_ARGS)
    parser.add_argument("count", **_COUNT_ARGS)


def _add_item_subparser(subparsers, library: GeneratorLibrary) -> None:
    """
    Subparser for using the name generators.
    """
    parser = subparsers.add_parser(
        "item",
        help="Generate items.",
    )
    generator_names = library.item.keys()

    parser.add_argument(
        "generator",
        choices=generator_names,
        help="choose a generator."
    )
    parser.add_argument("-kw", "--keywords", **_KEYWORD_ARGS)
    parser.add_argument("-mt", "--maxtime", **_MAXTIME_ARGS)
    parser.add_argument("-up", "--update", **_FORCE_UPDATE_ARGS)
    parser.add_argument("count", **_COUNT_ARGS)


def _add_npc_subparser(subparsers, library: GeneratorLibrary) -> None:
    """
    Subparsers for using the npc generators.
    """
    parser = subparsers.add_parser(
        "npc",
        help="generate NPCs.",
    )
    generator_names = library.npc.keys()

    parser.add_argument(
        "generator",
        choices=generator_names,
        help="choose a generator."
    )
    parser.add_argument("-kw", "--keywords", **_KEYWORD_ARGS)
    parser.add_argument("-mt", "--maxtime", **_MAXTIME_ARGS)
    parser.add_argument("-up", "--update", **_FORCE_UPDATE_ARGS)
    parser.add_argument("count", **_COUNT_ARGS)
