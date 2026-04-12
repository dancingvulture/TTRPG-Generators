"""
Generate various types of NPCs.
"""


from src.generators._generator import (
    Creation, 
    KnaveGenerator, 
    PerilousWildsGenerator
)
from random import choices, shuffle


class NPC(Creation):
    """
    A class whose instance represents an NPC.
    """


class KnaveNPCGenerator(KnaveGenerator):
    """
    Generate Fantasy NPCs.
    """
    def _generator(self) -> NPC:
        race = self._get_race()
        name = self._get_name(race)
        attributes = [("race", race)]

        additional_attribute_chances = [
            (1, 0.5),
            (2, 0.3),
            (3, 0.2),
        ]
        attribute_counts, weights = zip(*additional_attribute_chances)
        attribute_count = choices(attribute_counts, weights=weights)[0]
        additional_attributes = self._get_attributes(attribute_count)
        attributes = attributes + additional_attributes

        return NPC(name, *attributes)

    @staticmethod
    def _get_race() -> str:
        races_and_weights = [
            ("human", 0.5),
            ("dwarf", 0.25),
            ("elf", 0.25)
        ]
        races, weights = zip(*races_and_weights)
        race_chosen = choices(races, weights=weights)[0]
        return race_chosen

    def _get_name(self, race: str) -> str:
        templates = {
            "human": "humans",
            "dwarf": "dwarves",
            "elf": "elves",
        }
        generator_type = "name"
        generator_name = templates[race]
        return self._get_other_generator_output(generator_type, generator_name).name

    def _get_attributes(self, count: int) -> list[tuple[str, str | Creation]]:
        attributes = []
        attribute_types = [
            ("archetype", "*archetype*"),
            ("personality", "*personality*"),
            ("npc detail", "*npc detail*"),
            ("asset", "*asset*"),
            ("liability", "*liability*"),
            ("mannerism", "*mannerism*"),
            ("item", "*mundane item*"),
        ]
        shuffle(attribute_types)

        for _ in range(count):
            name, value = attribute_types.pop()
            value = self._substitute_headers(value)
            attributes.append((name, value))

        return attributes


class PerilousWildsNPCGenerator(PerilousWildsGenerator):
    """\
    Generate NPCs using the Perilous Wilds tables (pp. 52-53).\
    """
    def _generator(self) -> Creation:
        name = self._get_name()
        attributes = [
            ("context", context := self._get_entry("npc context")),
            ("occupation", self._get_occupation(context)),
            ("activity", self._substitute_headers("*detail, activity*")),
            ("alignment", self._substitute_headers("*detail, alignment*")),
            ("trait", self._substitute_headers("*npc trait*")),
        ]
        return Creation(name, *attributes)

    def _get_name(self) -> str:
        """\
        Use name generators to get a name.\
        """
        race_dist = {
            "humans": 0.50,
            "dwarves": 0.25,
            "elves": 0.25,
        }
        race = self._choose_from_dist(1, race_dist)
        name = self._get_other_generator_output("name", race)
        return name.name

    def _get_occupation(self, context):
        """\
        Get the occupation of the npc, based on their context.\
        """
        occupation_tables = {
            "wilderness": lambda: self._substitute_headers("*npc context, wilderness*"),
            "rural": lambda: self._substitute_headers("*npc context, rural*"),
            "urban": lambda: self._substitute_headers("*npc context, urban*"),
        }
        occupation = occupation_tables[context]()
        return occupation
