"""Each name generator is its own function, most of them are too
different to justify using classes and inheritance."""


from random import choice, choices, randint


def dwarves(contents: dict) -> str:
    """Format is Surname + Epithet + Lineage + Lineage + Title. Rarely
    will a name use all of these, but usually some combination of them.
    I've based this off of
    https://thedwarrowscholar.com/2012/04/27/namingconventions/.
    For surnames, I'm pulling from Gary Gygax's Extraordinary Book of
    Names, Table 5-5: Doughty & Homely, page 186. For Epithets and
    Titles I'm pulling from the same book, pages 133-141."""

    def surname() -> tuple[str, str]:
        gender = choice(["Son", "Daughter"])
        dwarf = choice(contents["Prefix"])

        if gender == "Son":
            dwarf += choice(contents["Masc Suffix"])
        else:
            dwarf += choice(contents["Fem Suffix"])

        return dwarf, gender

    def epithet() -> str:
        layout = choice(
            (
                "1the {}",  # The Adjective.
                "2{}{}",  # AdjectiveNoun
            )
        )

        if layout[0] == "1":
            adjective = choice(contents["Adjective"])
            epithet_ = layout[1:].format(adjective)

        elif layout[0] == "2":
            adjective = choice(contents["Adjective"])
            noun = choice(contents["Noun"])
            epithet_ = layout[1:].format(adjective, noun)
        # noinspection PyUnboundLocalVariable
        return epithet_

    def title(gender: str) -> str:
        # I should include more formats, curate the lists a bit more.
        layout = "{} of the {} {}"

        honor_input = "Masc Honorific" if gender == "Son" else "Fem Honorific"
        honorific = choice(contents[honor_input])
        adjective = choice(contents["Location Adjective"])
        location = choice(contents["Location"])

        return layout.format(honorific, adjective, location)

    dwarf_name, dwarf_gender = surname()
    title_gender = dwarf_gender  # Gender of the honorific in the title.
    if randint(1, 4) == 1:
        dwarf_name += " " + epithet()

    if randint(1, 3) == 1:
        parent_name, parent_gender = surname()
        title_gender = parent_gender
        dwarf_name += f", {dwarf_gender} of {parent_name}"

        if randint(1, 2) == 1:
            dwarf_name += " " + epithet()

        if randint(1, 4) == 1:
            grand_parent_name, grandparent_gender = surname()
            title_gender = grandparent_gender
            dwarf_name += f", {parent_gender} of {grand_parent_name}"

            if randint(1, 2) == 1:
                dwarf_name += " " + epithet()

    if randint(1, 10) == 1:
        dwarf_name += ", " + title(title_gender)

    return dwarf_name


def elves(contents: dict) -> str:
    """A computerized version of table 5-6: Fair & Noble, on pages
    186-187 of Gary Gygax's Extraordinary Book of Names."""

    layout = choices(["1{}{}{}", "2{}{}"], weights=[6, 1])[0]
    prefix = choice(contents["Prefix"])
    suffix = choice(contents["Suffix"])

    if layout[0] == "1":
        middle = choice(contents["Middle"])
        elf = layout[1:].format(prefix, middle, suffix)
    elif layout[0] == "2":
        elf = layout[1:].format(prefix, suffix)
    # noinspection PyUnboundLocalVariable
    return elf


def epithets(contents: dict) -> str:
    """This is inspired by Gary Gygax's Extraordinary Book of Names,
    pages 133-138. I've stolen most of the adjectives, nouns, and verbs
    from there, but have added some of my own choosing as well. I've
    boiled down the formula to be some random combination of adjectives,
    nouns, and verbs. But so far results are really quite random, too
    random to be useful most of the time. Although the keyword feature
    improves this. I wonder if I should have it work closer to the book,
    or try something else."""
    layout = choice([["Adjective"], ["Noun"], ["Verb"],
                     ["Adjective", "Noun"], ["Adjective", "Verb"],
                     ["Noun", "Noun"], ["Noun", "Verb"]])
    epithet = ''
    for thing in layout:
        epithet += choice(contents[thing]) + " "

    return epithet.strip()


def locations(contents: dict) -> str:
    """A computerized version of the locations tables from the Tomb of
    Adventure Design, 2nd Edition, pages 8-14. Largely unchanged, except
    that I've mixed both tables together."""
    approach = choices(["overview", "purpose"], [5, 1])[0]

    if approach == "overview":

        description = choice(contents["Description"])
        location = choice(contents["Location"])
        feature1 = choice(contents["Feature 1"])
        feature2 = choice(contents["Feature 2"])
        location_ = (description + " " + location + " of the " + feature1 + " "
                     + feature2)

    elif approach == "purpose":

        word1 = choice(contents["Word 1"])
        word2 = choice(contents["Word 2"])
        location_ = word1 + " " + word2
    # noinspection PyUnboundLocalVariable
    return location_


def minor_gods(contents: dict) -> str:
    """A computerized version of the Generating Minor Gods table from
    the Tomb of Adventure Design, 2nd Edition, pages 276-277."""
    name1 = choice(contents['Name1'])
    name2 = choice(contents['Name2'])
    title1 = choice(contents['Title1'])
    title2 = choice(contents['Title2'])
    minor_god = name1 + name2 + " " + title1 + " " + title2

    return minor_god


def mystic_orders(contents: dict) -> str:
    """Inspired by Gary Gygax's Extraordinary Book of Names, Table 3-6:
    Mystic Order Names, pages 145-146. Streamlined and with many of my
    own words added to each section, and a few modified or removed."""
    layout = choices([
        "1{} of the {}",
        "2{} of the {} {}",
        "3{} {} of the {} {}",
        "4{} {}"],
        weights=[1, 7, 1, 1])[0]
    group = choices(contents["Group"])[0]
    entity = choices(contents["Entity"])[0]
    descr = choices(contents["Description"], k=2)

    if layout[0] == "1":
        mystic_order = layout[1:].format(group, entity)
    elif layout[0] == "2":
        mystic_order = layout[1:].format(group, descr[0], entity)
    elif layout[0] == "3":
        while descr[0] == descr[1]:
            descr[1] = choice(contents["Description"])  # No duplicates.
        mystic_order = layout[1:].format(descr[0], group, descr[1], entity)
    elif layout[0] == "4":
        mystic_order = layout[1:].format(descr[0], group)
    # noinspection PyUnboundLocalVariable
    return mystic_order


def test(contents: dict) -> str:
    part1 = choice(contents["header0"])
    part2 = choice(contents["header1"])
    test_name = part1 + part2

    return test_name


generator_dict = {
    "dwarves": dwarves,
    "elves": elves,
    "epithets": epithets,
    "locations": locations,
    "minor-gods": minor_gods,
    "mystic-orders": mystic_orders,
    "test": test
}
