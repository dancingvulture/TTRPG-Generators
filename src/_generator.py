"""
Module containing the base generator class and the child classes which are
easily applicable to more than one type of generator.
"""


import time
import os
import re
from random import choice
import src.generators as gen  # Absolute import to avoid


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

        self._table_filenames = table_filenames
        table_filenames_plus_directory = [self._tables_directory + x for x in table_filenames]
        self._update_tables(force_table_update, table_filenames_plus_directory)
        self._tables = self._get_tables(table_filenames_plus_directory)

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

    def _substitute_headers(self, entry: str) -> str:
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
                new_entry = choice(self._tables[hdr[1:-1]])  # Trim asterisks.
                new_entry = self._substitute_headers(new_entry)

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
    def __init__(self, force_table_update: bool, additional_tables: list[str]):
        special_case_funcs = {
            "*surname*": "_get_surname",
            "*inn*": "_get_inn_name",
            "*spell*": "_get_spell",
        }
        table_filenames = ["alchemy.txt", "civilization.txt", "delving.txt",
                           "equipment.txt", "monster.txt", "people.txt",
                           "spells.txt", "travel.txt"]
        table_filenames += additional_tables
        super().__init__(force_table_update, table_filenames, special_case_funcs)

    @staticmethod
    def _get_spell() -> str:
        """
        Get a single spell, used for when the input into _substitute_headers
        contains '*spell*'.
        """
        Spells, *init_args = gen.GeneratorLibrary().name["spells"]
        spell_generator = Spells(False)
        spell_generator.generate(1, None, 0.10, True)
        return spell_generator.items[0]

    def _get_surname(self):
        return (f"{self._substitute_headers("*surname 1*")}"
                f"{self._substitute_headers("*surname 2*")}")

    def _get_inn_name(self):
        return (f"{self._substitute_headers("*inn name 1*")}"
                f" {self._substitute_headers("*inn name 2*")}")
