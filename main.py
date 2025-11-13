"""
A program for generating random names! Options given on the command line
using argparse. I've tried my best to make it easy to add new ones.
"""

import argparse
from src.generators import generator_dict

def parse_arguments(generator_names):
    # Note to self: should probably make a custom "help" message with
    # better formatting, so many name generators and the auto-generated
    # one is starting to look a bit strained.
    """Parses the command line arguments."""
    parser = argparse.ArgumentParser(prog="Name Generator")
    parser.add_argument(
        "generator",
        choices=generator_names,
        help="choose a generator"
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
              "names for in seconds, default is 5"),
        default=5.0
        )
    parser.add_argument(
        "-up", "--update",
        help="Force update of generator's table file",
        action="store_true",
        default=None
        )
    parser.add_argument(
        "count",
        type=int,
        help="Number of names to generate"
        )

    return parser.parse_args()


def main():
    name_generator_names = generator_dict.keys()
    args = parse_arguments(name_generator_names)

    generator_class, table_filenames = generator_dict[args.generator]
    generator = generator_class(table_filenames, args.update)
    generator.generate(args.count, args.keywords, args.maxtime)
    generator.show()


if __name__ == "__main__":
    main()
