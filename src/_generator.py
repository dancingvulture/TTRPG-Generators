"""
Module containing the base generator class and the child classes which are
easily applicable to more than one type of generator.
"""
import time
import os
import re
import random
from copy import deepcopy
from typing import Any
import src.generators as generators  # Absolute import to avoid circular conflict.


class Creation:
    """
    Base class for generator output, this allows the use of a common and simply
    implemented interface for all generator outputs. Init requires a name and
    an arbitrary list of attributes represented with 0 or more 2-tuples. The
    first entry of the tuple is the attribute's name, the second is the
    attribute's value.
    """

    def __init__(self, name: str | None, *attribute: tuple[str, str | 'Creation']):
        self.name = name
        self.attributes, self.unlabelled_attributes = self._collect_attributes(*attribute)
        self.nested = 0

    @staticmethod
    def _collect_attributes(*attribute: tuple[str, str | 'Creation']
                            ) -> tuple[dict[str, str | 'Creation'], list[str | 'Creation']]:
        """
        Take in a number of attribute 2-tuples and collect the labelled
        attributes into a dictionary, and the unlabelled ones into a list.
        """
        attributes = {}
        unlabelled_attributes = []
        for attribute_label, value in attribute:
            if not attribute_label:
                unlabelled_attributes.append(value)
            else:
                attributes[attribute_label] = value

        return attributes, unlabelled_attributes

    @staticmethod
    def _capitalize(words: str) -> str:
        """
        Takes a string and makes the first letter of each word (separated
        by spaces) a capital and makes all others lowercase, then returns
        this new string. Ignores connected words, like 'the, of, etc.'
        """
        if not words: return words
        connectors = ["the", "of", "in", "is"]
        new_words = ''
        for word in words.lower().split():
            if word in connectors:
                new_words += word + ' '
            else:
                new_words += word[0].upper() + word[1:] + ' '
        new_words = new_words[0].upper() + new_words[1:]  # Capitalize first letter

        return new_words.strip()

    def __contains__(self, item: str) -> bool:
        if item in str(self):
            return True
        else:
            return False

    def __eq__(self, other: 'Creation') -> bool:
        if other.name == self.name and other.attributes == self.attributes:
            return True
        else:
            return False

    def __len__(self):
        """
        Returns the length of the longest line.
        """
        lines = str(self).split('\n')
        return max(map(len, lines))

    def __repr__(self) -> str:
        display = self._capitalize(self.name)
        for attribute_label, attribute in self.attributes.items():
            display += self._get_attr_display(attribute_label, attribute)

        for attribute in self.unlabelled_attributes:
            display += self._get_unlabelled_attr_display(attribute)

        return display

    def _get_attr_display(self,
                          attribute_label: str,
                          attribute: str | 'Creation'
                          ) -> str:
        """
        Given an attribute and its label, give the display value, and account
        for arbitrary nesting.
        """
        display = "\n  "
        if isinstance(attribute, Creation):
            attribute.nested += self.nested + 1
        for _ in range(self.nested):
            display += "  "
        display += f"- {attribute_label}: {attribute}"
        return display

    def _get_unlabelled_attr_display(self,
                                     attribute: str | 'Creation'
                                     ) -> str:
        """
        Makes the display value for attributes without labels
        """
        display = "\n  "
        if isinstance(attribute, Creation):
            attribute.nested += self.nested + 1
        for _ in range(self.nested):
            display += "  "
        display += f"- {attribute}"
        return display

class Generator:
    """
    Base generator class, from which all the other base generator classes
    are derived. Contains the machinery to grab and compile tables from
    the given filenames and update said files if needed.
    """
    def __init__(self, force_table_update: bool, table_filenames: list[str]):
        self._tables_directory = "tables//"
        self._last_runtime_filename = "last_runtime.txt"
        self.items = []
        self._demarcation_char = " | "

        self._table_filenames = table_filenames
        table_filenames_plus_directory = [self._tables_directory + x for x in table_filenames]
        self._update_tables(force_table_update, table_filenames_plus_directory)
        self._tables = self._get_tables(table_filenames_plus_directory)

    def generate(self, count: int, keywords: list[str] | None,
                 max_time: float, suppress_print=False) -> list[Creation]:
        """
        This method belongs to the base Generator class. Although not useful in
        that class itself, any derived name generators use this to actually run
        their generators. Adding all results to the .items property (a list).
            - count: Number to generate.
            - keywords: If not None, results will only include those that contain
                        the given keywords.
            - max_time: Usually only comes up if keywords is being used, the
                        generator will just keep going until it generates 'count'
                        results, rejecting any that don't contain all keywords.
                        If this takes longer than 'max_time', the generator stops
                        and just shows what it has.
            - suppress_print=False: stops the generator from printing to stdout
                                    while running. This is used primarily when
                                    generators call other generators, so as not
                                    to flood stdout with redundant messages.
        """
        start = time.time()  # Used to prevent the program from stalling out here.
        if keywords is None:  # If the optional argument is not used.

            for _ in range(count):
                self.items.append(self._generator())

        else:  # Generate names until we have count names containing the keywords.
            tries = 0
            while len(self.items) < count:
                tries += 1
                creation = self._generator()
                for keyword in keywords:
                    if keyword not in creation:
                        break
                    elif creation in self.items:  # No duplicates.
                        break

                else:  # Only add the name if all keywords are in the generated name.
                    self.items.append(creation)

                if time.time() - start > max_time:
                    if not suppress_print:
                        print(f"Program took longer than {max_time} seconds, "
                              "forcing print.")
                    break
            if not suppress_print:
                print(f"Total of {tries:,} results generated.", end=' ')

        return self.items

    def show(self) -> None:
        """
        Takes any results produced by the generator and prints them.
        """
        if self.items:
            longest_result = max(map(len, self.items))
            print(f"Displaying {len(self.items)} results\n" + longest_result * '-')

            for result in self.items:
                print(result, end="\n")

            print(longest_result * '-')

        else:
            print("No results to display")

    def _generator(self) -> Creation:
        """
        Placeholder meant to be overwritten by child classes.
        """
        raise NotImplementedError("You need to overwrite the _generator"
                                  " method.")

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

    def _get_entry(self, table_name: str) -> str:
        """
        Get a random entry from the given table.
        """
        return random.choice(self._tables[table_name])

    def _text_file_to_dict(self, filename: str) -> dict:
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
        demar = self._demarcation_char
        for line in open(filename):
            line = line.strip()

            if not line:  # Skip empty lines.
                pass

            elif line[0] == "#":  # The header for the column.
                current_list = line[1:].strip()

            elif line:
                contents[current_list] = [x.strip() for x in line.split(demar)]

        return contents

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
        demar = self._demarcation_char
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
                text += demar.join(contents[key]) + "\n\n"

            # And then we update the text file.
            with open(filename, "w") as file:
                file.write(text)

            message = f"{filename} updated"
            display = len(message) * '-' + '\n' + message + '\n' + len(message) * '-'
            print(display)

    @staticmethod
    def _get_other_generator_output(generator_type: str, generator_name: str
                                    ) -> Creation:
        """
        Use the GeneratorLibrary interface to call any other generator by
        specifying the type of generator, and its name.
        """
        library = generators.GeneratorLibrary().generators_by_type
        generator_class, *init_args = library[generator_type][generator_name]
        generator = generator_class(False, *init_args)
        items = generator.generate(1, None, 0.1, suppress_print=True)
        return items[0]

    @staticmethod
    def _choose_from_dist(count: int,
                          distribution: dict[Any, int | float],
                          repeats=True,
                          ) -> Any | list[Any]:
        """
        Given a distribution, represented by a dictionary whose keys are the
        things we're picking, and whose values are is the probability of being
        chosen, or the weight.
        We return count items from the distribution. The kwarg repeats tells us
        whether multiple identical items can be chosen from the distribution
        (True by default).
        """
        distribution_copy = deepcopy(distribution)
        if repeats:
            values, weights = zip(*distribution_copy.items())
            chosen_values = random.choices(values, weights=weights, k=count)
        else:
            chosen_values = []
            for _ in range(count):
                values, weights = zip(*distribution_copy.items())
                current_value = random.choices(values, weights=weights)[0]
                chosen_values.append(current_value)
                distribution_copy.pop(current_value)

        return chosen_values if count > 1 else chosen_values[0]



class LinkedGenerator(Generator):
    """
    A base class containing the machinery to use linked tables. That is,
    tables whose results have you roll on other tables to an arbitrarily
    nested degree.

    Links to other tables within table entries, also called headers, are
    noted with a special syntax in the .txt file. Any text bookended by
    asterisks (e.g. *city theme*) is the exact name of another table
    (i.e. its header).

    Compared to the base Generator class, the LinkedGenerator has one
    additional argument, special_case_funcs. This is for any headers that
    require special treatment not covered in the _substitute_headers
    method. The key is the header (including asterisks) and the value is
    the special case function.
    """
    def __init__(self, force_table_update: bool, table_filenames: list[str],
                 special_case_names: dict[str, str]):
        super().__init__(force_table_update, table_filenames)
        self._special_case_funcs = self._get_special_case_funcs(special_case_names)

    def _substitute_headers(self, entry: str | Creation) -> str | Creation:
        """
        This function searches entry for any *headers*, each header consists of
        one or more words that are bookended by asterisks. A header links to
        another table with the matching header, when we find a header we
        substitute *header* for a random entry on that header's table.
        If that entry is another header, we roll on THAT header's table, and so
        on and so on. This ends when we get an entry containing no headers, in
        which case this function simply returns the entry unchanged.
        """
        # First we search the entry for any headers it may have.
        headers = re.compile(r"\*[^*]*\*").findall(entry)

        # This loop will substitute each header present in our entry with a
        # random new entry from that header's table. If there are no headers
        # present in entry, the loop won't execute and entry will be returned
        # unmodified.
        for hdr in headers:
            # First we deal with special cases.
            for special_case, func in self._special_case_funcs.items():
                if hdr == special_case:
                    new_entry = func()
                    break  # To avoid executing the else clause below.
            else:
                # For the general case, We pick a random entry from the table
                # indicated by the header. Because this new entry could also be
                # a header, we apply this method to it.
                new_entry = random.choice(self._tables[hdr[1:-1]])  # Trim asterisks.
                new_entry = self._substitute_headers(new_entry)

            # Some special exception functions produce Creations instead of
            # strings, we have to handle them differently.
            if isinstance(new_entry, Creation):
                return new_entry

            # Our new entry obtained, we substitute it into our entry
            entry = entry.replace(hdr, new_entry, 1)

        return entry

    def _get_special_case_funcs(self, func_map: dict[str, str]) -> dict[str, any]:
        """
        All we can do is pass the name of the special case functions as a
        string, and map them to each special case. All this method does
        iterate through that map, producing a new map that connects each
        special case directly to its special case function.
        """
        special_case_funcs = {}
        for special_case, func_name in func_map.items():
            special_case_funcs[special_case] = getattr(self, func_name)
        return special_case_funcs


class KnaveGenerator(LinkedGenerator):
    """
    A base class for any generator using the Knave 2e tables.
    """
    def __init__(self, force_table_update: bool, additional_tables: list[str],
                 additional_special_case_funcs: dict[str, str]):
        special_case_funcs = {
            "*surname*": "_get_surname",
            "*inn*": "_get_inn_name",
            "*spell*": "_get_spell",
        }
        table_filenames = ["alchemy.txt", "civilization.txt", "delving.txt",
                           "equipment.txt", "monster.txt", "people.txt",
                           "spells.txt", "travel.txt"]
        special_case_funcs = special_case_funcs | additional_special_case_funcs
        table_filenames += additional_tables
        super().__init__(force_table_update, table_filenames, special_case_funcs)

    def _get_spell(self) -> str:
        """
        Get a single spell, used for when the input into _substitute_headers
        contains '*spell*'.
        """
        spell = self._get_other_generator_output("name", "spells")
        return str(spell)

    def _get_surname(self) -> str:
        return (f"{self._substitute_headers("*surname 1*")}"
                f"{self._substitute_headers("*surname 2*")}")

    def _get_inn_name(self) -> str:
        return (f"{self._substitute_headers("*inn name 1*")}"
                f" {self._substitute_headers("*inn name 2*")}")
