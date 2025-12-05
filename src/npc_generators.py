"""
Generate various types of NPCs.
"""


from src._generator import Creation, KnaveGenerator
from random import choices, shuffle


class NPC(Creation):
    """
    A class whose instance represents an NPC.
    """


class FantasyNPCs(KnaveGenerator):
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

    def _get_fantasy_mundane(self) -> Creation:
        return self._get_other_generator_output("item", "fantasy-mundane")

    def _get_name(self, race: str) -> str:
        templates = {
            "human": "humans",
            "dwarf": "dwarves",
            "elf": "elves",
        }
        generator_type = "name"
        generator_name = templates[race]
        return str(self._get_other_generator_output(generator_type, generator_name))

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
