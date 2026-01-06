"""
Run unit tests on the generator program.
"""


import argparse
import subprocess
import sys
from src.generators import GeneratorLibrary



_COUNT_ARGS = {
    "type": lambda x: int(float(x)),
    "help": "Number to generate."
}
_SUPPRESS_PRINT_ARGS = {
    "help": "Run generators without printing an output.",
    "action": "store_true",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Unit Test Program for TTRPG Generator."
    )
    subparsers = parser.add_subparsers(
        help="Choose a test",
        dest="test"
    )
    _add_run_all_via_cdm_subparser(subparsers)

    return parser.parse_args()


def _add_run_all_via_cdm_subparser(subparsers) -> None:
    parser = subparsers.add_parser(
        "run-all-cmd",
        help="Run all generators with the command line interface.",
    )
    parser.add_argument("-sp", "--suppress_print", **_SUPPRESS_PRINT_ARGS)
    parser.add_argument("count", **_COUNT_ARGS)


def run_all_via_cmd(count: int, suppress_print: bool) -> None:
    """
    Runs every single generator through the command line interface. That way
    the full flow of the program is tested.
    """
    library = GeneratorLibrary()
    py_cmd = "py" if sys.platform == 'windows' else 'python3'

    # First we gather all command line inputs and displays in a list.
    all_inputs_and_displays = []
    for gen_type, gen_dict in library.generators_by_type.items():
        for gen_name in gen_dict:
            cmd_input = [f"{py_cmd}", "main.py", f"{gen_type}", f"{gen_name}",
                         f"{count}"]
            if suppress_print:
                cmd_input = cmd_input[:3] + ["-sp"] + cmd_input[3:]
            display = f"Testing Generator --> {gen_type}:{gen_name}    "
            all_inputs_and_displays.append([cmd_input, display])

    # Then we make all displays equal length
    longest = max(map(lambda x: len(x[1]), all_inputs_and_displays))
    for index in range(len(all_inputs_and_displays)):
        old_display = all_inputs_and_displays[index][1]
        adjusted_display = old_display + " " * (longest - len(old_display))
        all_inputs_and_displays[index][1] = adjusted_display

    # Now we finally test all inputs.
    for cmd_input, display in all_inputs_and_displays:
        if suppress_print:
            print(display, end="\t", flush=True)
            subprocess.run(cmd_input)
            print("Done!")
        else:
            print(display)
            subprocess.run(cmd_input)
            print("")


def main():
    args = parse_arguments()
    if args.test == "run-all-cmd":
        run_all_via_cmd(args.count, args.suppress_print)
    else:
        raise Exception(f"Invalid test: {args.test}")


if __name__ == "__main__":
    main()
