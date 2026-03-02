"""
Program for generating random things for TTRPG games.
"""

from src.generators import GeneratorLibrary
from src.command_line import parse_arguments


def main():
    args = parse_arguments()

    get_gen = GeneratorLibrary().generators_by_type
    generator_class, *default_init_args = get_gen[args.type][args.generator]

    if args.type in ("name", "item", "npc", "monster", "dungeon", "misc"):
        command_line_init_args = [args.update]
        generator_args = (args.count, args.keywords, args.maxtime)

    else:
        raise Exception(f"Invalid type: {args.type}")

    init_args = command_line_init_args + default_init_args
    generator = generator_class(*init_args)

    generator.generate(*generator_args, suppress_print=args.suppress_print)
    if not args.suppress_print:
        generator.show()


if __name__ == "__main__":
    main()
