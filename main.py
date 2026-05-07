"""
Program for generating random things for TTRPG games.
"""

import src.generators as gen
from src.command_line import parse_arguments


def main():
    args = parse_arguments()

    generator = gen.get_instance(
        args.type,
        args.generator,
        force_update=args.update
    )
    generator.generate(
        args.count,
        args.search,
        args.maxtime,
        suppress_print=args.suppress_print,
        **args.kwargs
    )
    if not args.suppress_print:
        generator.show()


if __name__ == "__main__":
    main()
