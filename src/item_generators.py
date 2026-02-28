"""
Generate various kinds of items.
"""


from src._generator import Creation, Generator, KnaveGenerator
from src.dice import Roller
from random import choice, choices, shuffle


class Item(Creation):
    """
    A class instance represents an item.
    """


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
        name = self._get_entry("name 1") + " " + self._get_entry("name 2")
        attributes = [
            ("rarity", self._get_entry("rarity")),
            ("type", self._get_entry("type")),
            ("form", self._get_entry("form")),
            ("location", self._get_entry("location")),
            ("quirk", self._get_entry("quirk")),
            ("complication", self._get_entry("complication")),
        ]
        count_distribution = {
            0: 0.28,
            1: 0.28,
            2: 0.28,
            3: 0.1,
            4: 0.06,
        }
        use_count = self._choose_from_dist(1, count_distribution)
        all_uses = [self._get_use() for _ in range(use_count)]
        if all_uses:
            known_uses = ("known uses", Creation(None, *all_uses))
            attributes.append(known_uses)
        return Item(name, *attributes)

    def _get_use(self) -> tuple[str, str]:
        """
        Get a random use.
        """
        use_type = self._get_entry("use type")
        use = self._get_entry(use_type)
        method = self._get_entry("method")
        return "", f"When {method}, it will {use}."


class WHScroll(Item):
    """
    A whitehack scroll.
    """
    def __rich__(self) -> str:
        spell = self.attributes["spell"]
        magnitude = self._capitalize(self.attributes["magnitude"])
        cost = self.attributes["cost"]
        fabric = self.attributes["fabric"]
        return f"{magnitude} ({cost} HP) {fabric} scroll of {spell}"


class WhitehackScroll(KnaveGenerator):
    """
    Generate scrolls for use in the whitehack 4e system.
    """
    def _generator(self) -> Creation:
        magnitude_dist = {
            "trivial": 0.20,
            "simple": 0.20,
            "standard": 0.45,
            "major": 0.10,
            "powerful": 0.05,
        }
        magnitude = self._choose_from_dist(1, magnitude_dist)

        attributes = [
            ("cost", self._get_cost(magnitude)),
            ("spell", self._get_other_generator_output("name", "spells")),
            ("fabric", self._get_fabric()),
        ]
        attributes.insert(0, ("magnitude", self._add_rarity_coloring(magnitude)))

        return WHScroll("Spell Scroll", *attributes)

    @staticmethod
    def _get_cost(magnitude) -> int:
        """
        Based on the magnitude, get the cost of the scroll
        """
        roller = Roller()
        cost_table = {
            "trivial": 0,
            "simple": 1,
            "standard": 2,
            "major": roller.sum("1d6"),
            "powerful": roller.sum("2d6"),
        }
        return cost_table[magnitude]

    @staticmethod
    def _add_rarity_coloring(magnitude: str) -> str:
        """
        Based off of the magnitude, add coloring to the text.
        """
        color_table = {
            "trivial": 244,   # Grey
            "simple": 34,     # Green
            "standard": 75,   # Blue
            "major": 201,     # Purple
            "powerful": 202,  # Orange
        }
        color = color_table[magnitude]
        return f"[color({color})]{magnitude}[/color({color})]"

    def _get_fabric(self) -> str:
        """\
        Randomly choose the fabric the scroll is made from, favoring parchment
        over other more exotic types.\
        """
        fabric = choices(
            ["parchment", self._substitute_headers("*fabric*")],
            weights=[0.75, 0.25],
        )
        return fabric[0]
