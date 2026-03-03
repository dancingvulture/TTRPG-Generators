"""
For storing name generator classes.
"""

from random import choice, choices, randint
from src._generator import (Generator, Creation, LinkedGenerator,
                            KnaveGenerator, ToadGenerator)


class Name(Creation):
    """
    A class whose instance contains a single name.
    """


class TestGenerator(Generator):
    def _generator(self) -> Name:
        part1 = self._get_entry("header0")
        part2 = self._get_entry("header1")
        test_name = part1 + part2

        return Name(test_name)


class DwarfNameGenerator(Generator):
    """
    Format is Surname + Epithet + Lineage + Lineage + Title. Rarely
    will a name use all of these, but usually some combination of them.
    I've based this off of
    https://thedwarrowscholar.com/2012/04/27/namingconventions/.
    For surnames, I'm pulling from Gary Gygax's Extraordinary Book of
    Names, Table 5-5: Doughty & Homely, page 186. For Epithets and
    Titles I'm pulling from the same book, pages 133-141.
    """
    def _generator(self) -> Name:
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

        return Name(dwarf_name)

    def _surname(self) -> tuple[str, str]:
        gender = choice(["Son", "Daughter"])
        dwarf = self._get_entry("Prefix")

        if gender == "Son":
            dwarf += self._get_entry("Masc Suffix")
        else:
            dwarf += self._get_entry("Fem Suffix")

        return dwarf, gender

    def _epithet(self) -> str:
        layout = choice(
            (
                "1the {}",  # The Adjective.
                "2{}{}",  # AdjectiveNoun
            )
        )

        if layout[0] == "1":
            adjective = self._get_entry("Adjective")
            epithet_ = layout[1:].format(adjective)

        elif layout[0] == "2":
            adjective = self._get_entry("Adjective")
            noun = self._get_entry("Noun")
            epithet_ = layout[1:].format(adjective, noun)

        else:
            raise Exception("How did you get here??")

        return epithet_

    def _title(self, gender: str) -> str:
        # I should include more formats, curate the lists a bit more.
        layout = "{} of the {} {}"

        honor_input = "Masc Honorific" if gender == "Son" else "Fem Honorific"
        honorific = self._get_entry(honor_input)
        adjective = self._get_entry("Location Adjective")
        location = self._get_entry("Location")

        return layout.format(honorific, adjective, location)


class ElfNameGenerator(Generator):
    """
    A computerized version of table 5-6: Fair & Noble, on pages 186-187
    of Gary Gygax's Extraordinary Book of Names.
    """
    def _generator(self) -> Name:
        layout = choices(["1{}{}{}", "2{}{}"], weights=[6, 1])[0]
        prefix = self._get_entry("Prefix")
        suffix = self._get_entry("Suffix")

        if layout[0] == "1":
            middle = self._get_entry("Middle")
            elf = layout[1:].format(prefix, middle, suffix)
        else:
            elf = layout[1:].format(prefix, suffix)
        return Name(elf)


class EpithetGenerator(Generator):
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
    def _generator(self) -> Name:
        layout = choice([["Adjective"], ["Noun"], ["Verb"],
                         ["Adjective", "Noun"], ["Adjective", "Verb"],
                         ["Noun", "Noun"], ["Noun", "Verb"]])
        epithet = ''
        for thing in layout:
            epithet += self._get_entry(thing) + " "

        return Name(epithet.strip())


class HumanNameGenerator(LinkedGenerator):
    """
    Generate human names using the Knave 2e tables. I may want to get
    more surnames.
    """
    def _generator(self) -> Name:
        templates_and_weights =  [
            ("*name*", 0.3),
            ("*name* *surname*", 0.2),
            ("*name* *surname* *surname*", 0.1),
            ("*name* *name* *surname*", 0.1),
            ("*name* *name*", 0.1),
            ("*surname* *surname*", 0.1),
            ("*surname* *name*", 0.1),
        ]
        choice_args = zip(*templates_and_weights)
        template_chosen = choices(*choice_args)[0]
        return Name(self._substitute_headers(template_chosen))

    def _get_first_name(self) -> str:
        """
        Using names across multiple different tables.
        """
        templates_and_weights = [
            ("*name*", 0.2),
            ("*greek*", 0.2),
            ("*spanish*", 0.1),
            ("*russian*", 0.1),
            ("*japanese*", 0.1),
            ("*arabic*", 0.1),
            ("*english*", 0.2)
        ]
        choice_args = zip(*templates_and_weights)
        header_chosen = choices(*choice_args)[0]
        return self._substitute_headers(header_chosen)

    def _get_surname(self) -> str:
        """
        Method copied from KnaveGenerator, I don't lik the repeat code
        but subclassing KnaveGenerator for this one method seems like
        overkill.
        """
        return (f"{self._substitute_headers("*surname 1*")}"
                f"{self._substitute_headers("*surname 2*")}")


class KnaveInnNameGenerator(KnaveGenerator):
    """
    Generate inn names using the Knave 2e tables.
    """
    def _generator(self) -> Name:
        return Name(self._get_inn_name())


class ToadLocationGenerator(ToadGenerator):
    """
    A computerized version of the locations tables from the Tomb of
    Adventure Design, 2nd Edition, pages 8-14. Largely unchanged, except
    that I've mixed both tables together.
    """
    def _generator(self) -> Name:
        approach = choices(["overview", "purpose"], [5, 1])[0]

        if approach == "overview":
            description = self._get_entry("location description")
            location = self._get_entry("location")
            feature1 = self._get_entry("feature 1")
            feature2 = self._get_entry("feature 2")
            location = (description + " " + location + " of the " + feature1 + " "
                         + feature2)

        else:  # approach == "purpose"
            word1 = self._get_entry("word 1")
            word2 = self._get_entry("word 2")
            location = word1 + " " + word2
        return Name(location)


class ToadMinorGodGenerator(ToadGenerator):
    """
    A computerized version of the Generating Minor Gods table from
    the Tomb of Adventure Design, 2nd Edition, pages 276-277.
    """
    def _generator(self) -> Name:
        name1 = self._get_entry('Name1')
        name2 = self._get_entry('Name2')
        title1 = self._get_entry('Title1')
        title2 = self._get_entry('Title2')
        minor_god = name1 + name2 + " " + title1 + " " + title2

        return Name(minor_god)


class ToadMysticOrderGenerator(ToadGenerator):
    """
    Inspired by Gary Gygax's Extraordinary Book of Names, Table 3-6:
    Mystic Order Names, pages 145-146. Streamlined and with many of my
    own words added to each section, and a few modified or removed.
    """
    def _generator(self) -> Name:
        layout = choices([
            "1{} of the {}",
            "2{} of the {} {}",
            "3{} {} of the {} {}",
            "4{} {}"],
            weights=[1, 7, 1, 1])[0]
        group = self._get_entry("Group")
        entity = self._get_entry("Entity")
        descr0 = self._get_entry("Description")
        descr1 = self._get_entry("Description")

        if layout[0] == "1":
            mystic_order = layout[1:].format(group, entity)
        elif layout[0] == "2":
            mystic_order = layout[1:].format(group, descr0, entity)
        elif layout[0] == "3":
            while descr0 == descr1:
                descr1 = self._get_entry("Description")  # No duplicates.
            mystic_order = layout[1:].format(descr0, group, descr1, entity)
        else:  # layout[0] == "4":
            mystic_order = layout[1:].format(descr0, group)
        return Name(mystic_order)


class KnaveSpellGenerator(KnaveGenerator):
    """
    Spell generator using the knave 2e tables.
    """
    def _generator(self) -> Name:
        templates = {
            (1, 2, 3): "{} {}",
            (4, 5, 6): "The {} {} {}",
            (7, 8, 9): "{}'s {} {}",
            (10, 11, 12): "{}'s {} {} {}",
        }
        headers = {
            1: ("*element*", "*form*"),
            2: ("*effect*", "*form*"),
            3: ("*effect*", "*element*"),
            4: ("*quality*", "*element*", "*form*"),
            5: ("*quality*", "*effect*", "*form*"),
            6: ("*quality*", "*effect*", "*element*"),
            7: ("*wizard name*", "*element*", "*form*"),
            8: ("*wizard name*", "*effect*", "*form*"),
            9: ("*wizard name*", "*effect*", "*element*"),
            10: ("*wizard name*", "*quality*", "*element*", "*form*"),
            11: ("*wizard name*", "*quality*", "*effect*", "*form*"),
            12: ("*wizard name*", "*quality*", "*effect*", "*element*"),
        }
        # Choose a tuple of headers randomly, then pick the appropriate template.
        headers_chosen = randint(1, 12)
        for key in templates:
            if headers_chosen in key:
                template_chosen = templates[key]
                break
        else:
            raise Exception("the creator of this fault did not specify a reason")

        # Our entry is the chosen template populated with the chosen headers,
        # we just run that through the _substitute_headers method and boom,
        # we have a spell.
        entry = template_chosen.format(*headers[headers_chosen])
        spell = self._substitute_headers(entry)
        return Name(spell)
