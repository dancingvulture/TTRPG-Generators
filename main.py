"""A module made to generate random names, with a distinct TTRPG focus.
Meant to be run from the command line as main(), use -h for info on what
to input."""


import argparse
import os.path
import time
from generators import generator_dict


def parse_arguments(generator_names):
    # Note to self: should probably make a custom "help" message with
    # better formatting, so many name generators and the auto-generated
    # one is starting to look a bit strained.
    """Parses the command line arguments."""
    parser = argparse.ArgumentParser(prog="Name Generator")
    parser.add_argument(
        "generator",
        choices=generator_names,
        help="choose a generator")
    parser.add_argument(
        "-k", "--keywords",
        help=("Results must contain these words; syntax for this command: "
              "separate each keyword with a commas, but with no spaces"))
    parser.add_argument(
        "-t", "--maxtime",
        type=float,
        help=("Maximum time the program tries to generate "
              "names for in seconds, default is 5"),
        default=5.0)
    parser.add_argument(
        "-u", "--update",
        help="Force update of generator's table file",
        action="store_true",
        default=None)
    parser.add_argument(
        "count",
        type=int,
        help="Number of names to generate")

    args = parser.parse_args()
    return args.generator, args.keywords, args.maxtime, args.update, args.count


def text_file_to_dict(filename: str) -> dict:
    """Used to convert the contents of a text file into a dictionary
    whose entries are lists of strings. The strings are intended to be
    the individual elements we generate random names from, each entry is
    some kind of category useful to whatever name generator we're using.
    Syntax in this text file is as follows:
    - If a line starts with #, the remaining text on the line (sans
      whitespace) will be interpreted as the key to a new entry in the
      dictionary (always a string).
    - Any non-empty line (that doesn't start with a #), is interpreted
      as the contents of the current dictionary entry. The line will be
      split into a list at the commas, whitespace will be cleaned up.
      You're meant to include everything on this one line, if you do
      another it'll just overwrite the previous.
    - Empty lines (i.e. containing only whitespace) are skipped"""
    contents = {}
    current_list = None
    for line in open(filename):
        line = line.strip()

        if not line:  # Skip empty lines.
            pass

        elif line[0] == "#":  # The header for the column.
            current_list = line[1:].strip()

        elif line:
            contents[current_list] = [x.strip() for x in line.split(', ')]

    return contents


def generate(generator, count, keywords, table_directory, maxtime) -> list:
    """Takes the user specified generator and generates however many
    names the user specified. Also applies any keywords the user specified"""
    print("")
    start = time.time()  # Used to prevent the program from stalling out here.

    contents = text_file_to_dict(table_directory + generator + ".txt")
    names = []
    generator = generator_dict[generator]
    if keywords is None:  # If the optional argument is not used.

        for _ in range(count):
            names.append(generator(contents))

    else:  # Generate names until we have count names containing the keywords.
        keywords = [x for x in keywords.lower().split(',')]
        tries = 0
        while len(names) < count:
            tries += 1
            name = generator(contents)
            for keyword in keywords:
                if keyword not in name.lower():
                    break
                elif name.lower() == keyword:  # Mostly for epithets.
                    break
                elif name in names:  # No duplicates.
                    break

            else:  # Only add the name if all keywords are in the generated name.
                names.append(name)

            if time.time() - start > maxtime:
                print(f"Program took longer than {maxtime} seconds, "
                      "forcing print.")
                break

        print(f"Total of {tries:,} names generated.", end=' ')

    return names


def update(filename) -> None:
    """This updates the text file containing the elements used to build
    names for a particular generator. Each generator has its own
    dedicated text file, which this program reads from to know what
    elements to use."""
    contents = text_file_to_dict(filename)

    # First we alphabetize and eliminate redundant entries, we make
    # entries uniformly lowercase so identical entries with different
    # cases aren't accidentally included.
    for key in contents:
        all_lowercase = map(lambda x: x.lower(), contents[key])
        contents[key] = sorted((list(set(all_lowercase))))

    # Then we format the contents of the dictionary to mimic the file format.
    text = ''
    for key in contents:
        text += "# " + key + "\n"
        text += ", ".join(contents[key]) + "\n\n"

    # And then we update the text file.
    with open(filename, "w") as file:
        file.write(text)

    # I'd like to add more information in this message, maybe say what
    # entries were eliminated, what entries were added. But I'd need to
    # save the last version to compare the new one to, which might make
    # for some extra file clutter, and probably not worth it since I
    # just got rid of the whole .pkl file thing. Still, it is a cool
    # feature.
    message = f"{filename} updated"
    display = len(message) * '-' + '\n' + message + '\n' + len(message) * '-'
    print(display)


def capitalize(words: str) -> str:
    """Takes a string and makes the first letter of each word (separated
    by spaces) a capital and makes all others lowercase, then returns 
    this new string. Ignores connected words, like 'the, of, etc.'"""

    connectors = ["the", "of", "in", "is"]
    new_words = ''
    for word in words.lower().split():
        if word in connectors:
            new_words += word + ' '
        else:
            new_words += word[0].upper() + word[1:] + ' '

    return new_words.strip()


def main():
    generator_names = generator_dict.keys()
    generator, keywords, max_time, update_tables, count = parse_arguments(generator_names)
    tables_directory = "tables//"
    filename = tables_directory + generator + ".txt"

    # Check if we need to update the generator's source text file.
    if update_tables:
        update(filename)

    elif not os.path.exists("last_runtime.txt"):
        with open("last_runtime.txt", "w") as file:
            file.write(f"{time.time()}")
        update(filename)

    elif (os.path.getmtime("last_runtime.txt")
          < os.path.getmtime(filename)):
        update(filename)

    with open("last_runtime.txt", "w") as file:
        file.write(f"{time.time()}")

    # Finally, generate (and print) names.
    names = generate(generator, count, keywords, tables_directory, max_time)
    if names:
        longest_name = max(map(len, names))
        print(f"Displaying {len(names)} names\n" + longest_name * '-')

        for name in names:
            print(capitalize(name))

        print(longest_name * '-')

    else:
        print("No names to display")


if __name__ == "__main__":
    main()
