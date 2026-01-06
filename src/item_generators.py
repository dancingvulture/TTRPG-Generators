"""
Generate various kinds of items.
"""


from src._generator import Creation, Generator, KnaveGenerator
from random import choice, choices, shuffle


class Item(Creation):
    """
    A class instance represents an item.
    """
    @property
    def preferred_spacing(self) -> str:
        return "\n\n"


class Magic(KnaveGenerator):
    """
    Generate magic items using the Knave 2e tables.
    """
    def _generator(self) -> Creation:
        item_base = "Magical " + self._get_item_base()
        attributes = [("effect", self._substitute_headers("*effect*"))]

        return Item(item_base, *attributes)

    def _get_item_base(self) -> str:
        bases = ["*tool*", "*misc. item*", "*book*", "*clothing*",
                 "*treasure*", "*weapon*"]
        chosen_base = choice(bases)
        return self._substitute_headers(chosen_base)


class FantasyMundane(KnaveGenerator):
    """
    Generate mundane fantasy items.
    """
    def _generator(self) -> Creation:
        # Item attributes.
        material = ("material", "*material*")
        decoration = ("decoration", "*decoration*")
        fabric = ("fabric", "*fabric*")
        item_trait = ("item trait", "*item trait*")
        subject = ("subject", "*book*")  # Special attribute for books.

        # Item types and valid attributes.
        item_types = {
            "*tool*": [material, decoration, item_trait],
            "*misc. item*": [material, decoration, item_trait],
            "book": [fabric, decoration, item_trait],
            "*clothing*": [fabric, material, decoration, item_trait],
            "*treasure*": [decoration, item_trait],
            "*weapon*": [material, decoration, item_trait]
        }
        item = choice(list(item_types.keys()))

        # Choose how many attributes to have
        counts_and_weights = (
            (0, 0.3),
            (1, 0.5),
            (2, 0.2)
        )
        counts, weights = zip(*counts_and_weights)
        attribute_count = choices(counts, weights)[0]

        # Choose what attributes to have.
        available_attributes = item_types[item]
        shuffle(available_attributes)
        chosen_attributes = [] if item != "book" else [subject]

        for _ in range(attribute_count):
            chosen_attributes.append(available_attributes.pop())

        # Turn any headers into table entries.
        item = self._substitute_headers(item)
        for index in range(len(chosen_attributes)):
            name = chosen_attributes[index][0]
            value = chosen_attributes[index][1]
            chosen_attributes[index] = (name, self._substitute_headers(value))

        return Item(item, *chosen_attributes)


class Gem(Generator):
    """
    Generate Gems using the tables from Geologists Primer (pp. 302-305)
    """
    def _generator(self) -> Creation:
        pass

