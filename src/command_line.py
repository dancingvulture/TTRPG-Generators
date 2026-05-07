"""
Contains all needed command line objects.
"""


import argparse
from types import MappingProxyType

import src.generators as generators


_SUBPARSERS = (
    (
        "name",
        "Generate names.",
        "None",
    ),
    (
        "item",
        "Generate items.",
        "None",
    ),
    (
        "pc",
        "Generate player characters.",
        "None",
    ),
    (
        "npc",
        "Generate NPCs.",
        "None",
    ),
    (
        "monster",
        "Generate monsters.",
        "None",
    ),
    (
        "misc",
        "Miscellaneous generators.",
        "None",
    ),
    (
        "dungeon",
        "Dungeons generators.",
        "None",
    ),
)


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

    for name, parser_help, kwarg_help in _SUBPARSERS:
        _add_subparser(subparsers, name, parser_help, kwarg_help)

    return parser.parse_args()


def _add_subparser(subparsers: argparse._SubParsersAction,
                   name: str,
                   parser_help: str,
                   kwargs_help: str,
                   ) -> None:
    """\
    Create a subparser for a generator type.\
    """
    parser = subparsers.add_parser(
        name,
        help=parser_help,
    )
    generator_names = generators.get_names(name)
    parser.add_argument(
        "generator",
        choices=generator_names,
        help="Choose a generator."
    )
    parser.add_argument(
        "count",
        type=int,
        help="Number to generate.",
    )
    parser.add_argument(
        "-kw", "--kwargs",
        help="Some generators will take special inputs, those that do are"
             f" listed here: \n{kwargs_help}\n\n snytax is kwarg=value, separate"
             f" multiple kwargs with commas, no spaces.",
        type=lambda x: _get_kwargs(x),
        default=MappingProxyType({}),
    )
    parser.add_argument(
        "-sr", "--search",
        help="Results must contain these words; syntax for this command:"
              " separate each search with a commas, but with no spaces",
        type=lambda search: [x for x in search.lower().split(',')],
    )
    parser.add_argument(
        "-mt", "--maxtime",
        help="Maximum time the program tries to generate names for in seconds,"
             " default is 5.",
        type=float,
        default=5.0,
    )
    parser.add_argument(
        "-up", "--update",
        help="Force update of generator's table file.",
        action="store_true",
    )
    parser.add_argument(
        "-sp", "--suppress-print",
        help="Suppress the print output of the main generator, mainly for"
             " debugging purposes.",
        action="store_true",
    )


def _get_kwargs(raw: str) -> dict[str, str]:
    """\
    Process kwargs.\
    """
    kwargs = {}
    for key, value in raw.strip().split(","):
        kwargs[key] = value
    return kwargs
