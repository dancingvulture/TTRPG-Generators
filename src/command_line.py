"""
Contains all needed command line objects.
"""


import argparse
from src.generators import GeneratorLibrary


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
    parser.add_argument(
        "-kw", "--keywords",
        help=("Results must contain these words; syntax for this command: "
              "separate each keyword with a commas, but with no spaces"),
        type=lambda keywords: [x for x in keywords.lower().split(',')]
    )
    parser.add_argument(
        "-mt", "--maxtime",
        type=float,
        help=("Maximum time the program tries to generate "
              "names for in seconds, default is 5."),
        default=5.0
    )
    parser.add_argument(
        "-up", "--update",
        help="Force update of generator's table file.",
        action="store_true",
        default=None
    )
    parser.add_argument(
        "count",
        type=int,
        help="Number of names to generate."
    )
