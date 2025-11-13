"""
For storing name generator classes. This is the real core of the program.
"""

import time
import os
from random import choice, choices, randint


class _NameGenerator:
    """
    Base name generator class, not much use on its own but it has some
    mechanics useful to all name generator objects.
    """
    def __init__(self, table_filenames: list[str], force_table_update: bool):
        self._tables_directory = "tables//"
        self._last_runtime_filename = "last_runtime.txt"
        self.names = []

        table_filenames = [self._tables_directory + x for x in table_filenames]
        self._update_tables(force_table_update, table_filenames)
        self._tables = self._get_tables(table_filenames)

    def generate(self, count: int, keywords: list[str], max_time,
                 suppress_print=False) -> None:
        """
        Generates names using the classes built in name generator.
        """
        start = time.time()  # Used to prevent the program from stalling out here.
        if keywords is None:  # If the optional argument is not used.

            for _ in range(count):
                self.names.append(self._generator())

        else:  # Generate names until we have count names containing the keywords.
            tries = 0
            while len(self.names) < count:
                tries += 1
                name = self._generator()
                for keyword in keywords:
                    if keyword not in name.lower():
                        break
                    elif name.lower() == keyword:  # Mostly for epithets.
                        break
                    elif name in self.names:  # No duplicates.
                        break

                else:  # Only add the name if all keywords are in the generated name.
                    self.names.append(name)

                if time.time() - start > max_time:
                    if not suppress_print:
                        print(f"Program took longer than {max_time} seconds, "
                              "forcing print.")
                    break
            if not suppress_print:
                print(f"Total of {tries:,} names generated.", end=' ')

    def show(self) -> None:
        if self.names:
            longest_name = max(map(len, self.names))
            print(f"Displaying {len(self.names)} names\n" + longest_name * '-')

            for name in self.names:
                print(self._capitalize(name))

            print(longest_name * '-')

        else:
            print("No names to display")

    @staticmethod
    def _capitalize(words: str) -> str:
        """
        Takes a string and makes the first letter of each word (separated
        by spaces) a capital and makes all others lowercase, then returns
        this new string. Ignores connected words, like 'the, of, etc.'
        """

        connectors = ["the", "of", "in", "is"]
        new_words = ''
        for word in words.lower().split():
            if word in connectors:
                new_words += word + ' '
            else:
                new_words += word[0].upper() + word[1:] + ' '

        return new_words.strip()

    def _generator(self) -> str:
        """
        Placeholder meant to be overwritten by child classes.
        """
        raise NotImplementedError("You need to overwrite the _generator"
                                  " method.")

    @staticmethod
    def _text_file_to_dict(filename: str) -> dict:
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

    def _get_tables(self, table_filenames: list[str]) -> dict[str, list]:
        """
        Using the table filenames grab all tables and compile them into
        a single dictionary.
        """
        tables = {}
        for filename in table_filenames:
            tables_from_file = self._text_file_to_dict(filename)
            for header, content in tables_from_file.items():
                if header in tables:
                    raise Exception(f"Header: {header} from {filename} is "
                                    f"already being used. Table contents: "
                                    f"{tables[header]}")
                else:
                    tables[header] = content
        return tables

    def _update_tables(self,
                       force_update: bool,
                       table_filenames: list[str]) -> None:
        """
        Check if the source table(s) for the generator need to be
        updated, and update them if so.
        """
        if force_update:
            self._update(table_filenames)

        elif not os.path.exists(self._last_runtime_filename):
            with open(self._last_runtime_filename, "w") as file:
                file.write(f"{time.time()}")
            self._update(table_filenames)

        else:
            last_m_times = {x:os.path.getmtime(x) for x in table_filenames}
            last_runtime = os.path.getmtime(self._last_runtime_filename)
            files_to_update = filter(
                lambda x: self._was_modified(x, last_runtime),
                last_m_times
            )
            self._update(list(files_to_update))

        with open(self._last_runtime_filename, "w") as file:
            file.write(f"{time.time()}")

    @staticmethod
    def _was_modified(filename: str, last_runtime: float) -> bool:
        """
        Check if a file was modified since the last runtime.
        """
        mod_time = os.path.getmtime(filename)
        return True if mod_time > last_runtime else False

    def _update(self, table_filenames: list[str]) -> None:
        """
        Updates the specified table(s) associated .txt files. Putting
        the contents  in alphabetical order and
        """
        for filename in table_filenames:
            contents = self._text_file_to_dict(filename)

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

            message = f"{filename} updated"
            display = len(message) * '-' + '\n' + message + '\n' + len(message) * '-'
            print(display)


class Test(_NameGenerator):
    def _generator(self) -> str:
        part1 = choice(self._tables["header0"])
        part2 = choice(self._tables["header1"])
        test_name = part1 + part2

        return test_name


class Dwarves(_NameGenerator):
    """
    Format is Surname + Epithet + Lineage + Lineage + Title. Rarely
    will a name use all of these, but usually some combination of them.
    I've based this off of
    https://thedwarrowscholar.com/2012/04/27/namingconventions/.
    For surnames, I'm pulling from Gary Gygax's Extraordinary Book of
    Names, Table 5-5: Doughty & Homely, page 186. For Epithets and
    Titles I'm pulling from the same book, pages 133-141.
    """
    def _generator(self) -> str:
        dwarf_name, dwarf_gender = self._surname()
        title_gender = dwarf_gender  # Gender of the honorific in the title.
        if randint(1, 4) == 1:
            dwarf_name += " " + self._epithet()

        if randint(1, 3) == 1:
            parent_name, parent_gender = self._surname()
            title_gender = parent_gender
            dwarf_name += f", {dwarf_gender} of {parent_name}"

            if randint(1, 2) == 1:
                dwarf_name += " " + self._epithet()

            if randint(1, 4) == 1:
                grand_parent_name, grandparent_gender = self._surname()
                title_gender = grandparent_gender
                dwarf_name += f", {parent_gender} of {grand_parent_name}"

                if randint(1, 2) == 1:
                    dwarf_name += " " + self._epithet()

        if randint(1, 10) == 1:
            dwarf_name += ", " + self._title(title_gender)

        return dwarf_name

    def _surname(self) -> tuple[str, str]:
        gender = choice(["Son", "Daughter"])
        dwarf = choice(self._tables["Prefix"])

        if gender == "Son":
            dwarf += choice(self._tables["Masc Suffix"])
        else:
            dwarf += choice(self._tables["Fem Suffix"])

        return dwarf, gender

    def _epithet(self) -> str:
        layout = choice(
            (
                "1the {}",  # The Adjective.
                "2{}{}",  # AdjectiveNoun
            )
        )

        if layout[0] == "1":
            adjective = choice(self._tables["Adjective"])
            epithet_ = layout[1:].format(adjective)

        elif layout[0] == "2":
            adjective = choice(self._tables["Adjective"])
            noun = choice(self._tables["Noun"])
            epithet_ = layout[1:].format(adjective, noun)
        # noinspection PyUnboundLocalVariable
        return epithet_

    def _title(self, gender: str) -> str:
        # I should include more formats, curate the lists a bit more.
        layout = "{} of the {} {}"

        honor_input = "Masc Honorific" if gender == "Son" else "Fem Honorific"
        honorific = choice(self._tables[honor_input])
        adjective = choice(self._tables["Location Adjective"])
        location = choice(self._tables["Location"])

        return layout.format(honorific, adjective, location)


class Elves(_NameGenerator):
    """
    A computerized version of table 5-6: Fair & Noble, on pages 186-187
    of Gary Gygax's Extraordinary Book of Names.
    """
    def _generator(self) -> str:
        layout = choices(["1{}{}{}", "2{}{}"], weights=[6, 1])[0]
        prefix = choice(self._tables["Prefix"])
        suffix = choice(self._tables["Suffix"])

        if layout[0] == "1":
            middle = choice(self._tables["Middle"])
            elf = layout[1:].format(prefix, middle, suffix)
        else:
            elf = layout[1:].format(prefix, suffix)
        return elf


class Epithets(_NameGenerator):
    """
    This is inspired by Gary Gygax's Extraordinary Book of Names,
    pages 133-138. I've stolen most of the adjectives, nouns, and verbs
    from there, but have added some of my own choosing as well. I've
    boiled down the formula to be some random combination of adjectives,
    nouns, and verbs. But so far results are really quite random, too
    random to be useful most of the time. Although the keyword feature
    improves this. I wonder if I should have it work closer to the book,
    or try something else.
    """
    def _generator(self) -> str:
        layout = choice([["Adjective"], ["Noun"], ["Verb"],
                         ["Adjective", "Noun"], ["Adjective", "Verb"],
                         ["Noun", "Noun"], ["Noun", "Verb"]])
        epithet = ''
        for thing in layout:
            epithet += choice(self._tables[thing]) + " "

        return epithet.strip()


class Locations(_NameGenerator):
    """
    A computerized version of the locations tables from the Tomb of
    Adventure Design, 2nd Edition, pages 8-14. Largely unchanged, except
    that I've mixed both tables together.
    """
    def _generator(self) -> str:
        approach = choices(["overview", "purpose"], [5, 1])[0]

        if approach == "overview":
            description = choice(self._tables["Description"])
            location = choice(self._tables["Location"])
            feature1 = choice(self._tables["Feature 1"])
            feature2 = choice(self._tables["Feature 2"])
            location_ = (description + " " + location + " of the " + feature1 + " "
                         + feature2)

        else:  # approach == "purpose"
            word1 = choice(self._tables["Word 1"])
            word2 = choice(self._tables["Word 2"])
            location_ = word1 + " " + word2
        return location_

class MinorGods(_NameGenerator):
    """
    A computerized version of the Generating Minor Gods table from
    the Tomb of Adventure Design, 2nd Edition, pages 276-277.
    """
    def _generator(self) -> str:
        name1 = choice(self._tables['Name1'])
        name2 = choice(self._tables['Name2'])
        title1 = choice(self._tables['Title1'])
        title2 = choice(self._tables['Title2'])
        minor_god = name1 + name2 + " " + title1 + " " + title2

        return minor_god


class MysticOrders(_NameGenerator):
    """
    Inspired by Gary Gygax's Extraordinary Book of Names, Table 3-6:
    Mystic Order Names, pages 145-146. Streamlined and with many of my
    own words added to each section, and a few modified or removed.
    """
    def _generator(self) -> str:
        layout = choices([
            "1{} of the {}",
            "2{} of the {} {}",
            "3{} {} of the {} {}",
            "4{} {}"],
            weights=[1, 7, 1, 1])[0]
        group = choices(self._tables["Group"])[0]
        entity = choices(self._tables["Entity"])[0]
        descr = choices(self._tables["Description"], k=2)

        if layout[0] == "1":
            mystic_order = layout[1:].format(group, entity)
        elif layout[0] == "2":
            mystic_order = layout[1:].format(group, descr[0], entity)
        elif layout[0] == "3":
            while descr[0] == descr[1]:
                descr[1] = choice(self._tables["Description"])  # No duplicates.
            mystic_order = layout[1:].format(descr[0], group, descr[1], entity)
        else:  # layout[0] == "4":
            mystic_order = layout[1:].format(descr[0], group)
        return mystic_order


# This lists every generator, it's associated string (put in on the
# command line), and the set of table files it uses.
generator_dict = {
    "dwarves": (Dwarves, ["dwarves.txt"]),
    "elves": (Elves, ["elves.txt"]),
    "epithets": (Epithets, ["epithets.txt"]),
    "locations": (Locations, ["locations.txt"]),
    "minor-gods": (MinorGods, ["minor gods.txt"]),
    "mystic-orders": (MysticOrders, ["mystic orders.txt"]),
    "test": (Test, ["test.txt"])
}
