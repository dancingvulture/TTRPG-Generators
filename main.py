"""
A program for generating random names! Options given on the command line
using argparse. I've tried my best to make it easy to add new ones.
"""

from src.generators import GeneratorLibrary
from src.command_line import parse_arguments


def main():
    args = parse_arguments()
    name_generators = GeneratorLibrary().name_generators

    generator_class, *init_args = name_generators[args.generator]
    generator = generator_class(args.update, *init_args)

    generator.generate(args.count, args.keywords, args.maxtime)
    generator.show()


if __name__ == "__main__":
    main()
