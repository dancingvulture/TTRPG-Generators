"""
Contains monster generator classes.
"""


from src.generators._generator import (
    Creation,
    LinkedGenerator,
    KnaveGenerator,
    PerilousWildsGenerator,
)
import re


class Monster(Creation):
    """
    Class for containing monster information.
    """


class KnaveMonster(Monster):
    """\
    Class containing knave monster information.\
    """
    @property
    def spacing_preference(self) -> str | int:
        return 1


class OozeGenerator(LinkedGenerator):
    """
    Uses tables from the Monster Overhaul (pp. 57-58).
    """
    def _generator(self) -> Creation:
        attributes_template = [
            ("type", "*type*"),
            ("embedded", "*embedded*"),
            ("twist", "*twist*"),
            ("texture", "*ooze texture*"),
            ("local use", "*ooze use*")
        ]
        attributes = []
        for name, value in attributes_template:
            value = self._substitute_headers(value)
            attributes.append((name, value))

        ooze_type = self._extract_ooze_type(attributes[0][1])
        name = ooze_type + " ooze"

        return Monster(name, *attributes)

    @staticmethod
    def _extract_ooze_type(text: str) -> str:
        sentences = re.compile(r"[\w ]*.").findall(text)
        ooze_type = sentences[0][:-1]
        return ooze_type


class KnaveMonsterGenerator(KnaveGenerator):
    """\
    Generate a monster using the knave tables.\
    """
    def _generator(self) -> Creation:
        monster_type = self._substitute_headers("*monster*")
        trait_dist = {
            0: 0.15,
            1: 0.60,
            2: 0.30,
            3: 0.05,
        }
        trait_count = self._choose_from_dist(1, trait_dist)
        attributes = []
        for _ in range(trait_count):
            trait = self._substitute_headers("*monster trait*")
            attributes.append(("trait", trait))

        return KnaveMonster(monster_type, *attributes)


class PerilousWildsCreatureGenerator(PerilousWildsGenerator):
    """\
    Generate monsters using the perilous wilds tables (pg. 49)\
    """
    def _generator(self) -> Creation:
        creature_type = self._substitute_headers("*creature, type*")
        creature_base = self._get_creature_base(creature_type)
        creature, tags = self._get_creature_and_tags(creature_base)
        attributes = self._get_attributes(creature_type)
        self._add_extra_attributes(attributes)
        return Monster(creature_base, *attributes)


    @staticmethod
    def _get_creature_and_tags(text: str) -> tuple[str, list[str]]:
        """\
        From a roll on the monster table, extract the creature and the tag,
        if it exists.\
        """
        creature = re.compile("[^(]*").findall(text)[0].strip()
        tags = re.compile(r"\(.*\)").findall(text)
        if tags: tags = [x[1:-1] for x in tags]

        return creature, tags

    def _get_creature_base(self, creature_type: str) -> str:
        """\
        Given the type, get the base creature description.\
        """
        bases = {
            "beast": lambda: self._substitute_headers("*creature, beast*"),
            "human": lambda: "human",
            "humanoid": lambda: self._substitute_headers("*creature, humanoid*"),
            "monster": lambda: self._substitute_headers("*creature, monster*"),
        }
        creature_base = bases[creature_type]()
        return creature_base

    def _get_attributes(self, creature_type: str) -> list[tuple[str, str | Creation]]:
        """\
        Different creature types have different attributes.\
        """
        attributes_by_type = {
            "beast": lambda: [
                ("activity", self._substitute_headers("*detail, activity*")),
                ("disposition", self._substitute_headers("*detail, disposition*")),
                ("no. appearing", self._substitute_headers("*detail, no. appearing*")),
                ("size", self._substitute_headers("*detail, size*")),
            ],
            "human": lambda: [
                ("activity", self._substitute_headers("*detail, activity*")),
                ("alignment", self._substitute_headers("*detail, alignment*")),
                ("disposition", self._substitute_headers("*detail, disposition*")),
                ("no. appearing", self._substitute_headers("*detail, no. appearing*")),
            ],
            "humanoid": lambda: [
                ("activity", self._substitute_headers("*detail, activity*")),
                ("alignment", self._substitute_headers("*detail, alignment*")),
                ("disposition", self._substitute_headers("*detail, disposition*")),
                ("no. appearing", self._substitute_headers("*detail, no. appearing*")),
            ],
            "monster": lambda: [
                ("activity", self._substitute_headers("*detail, activity*")),
                ("alignment", self._substitute_headers("*detail, alignment*")),
                ("disposition", self._substitute_headers("*detail, disposition*")),
                ("no. appearing", self._substitute_headers("*detail, no. appearing*")),
            ],
        }
        return attributes_by_type[creature_type]()

    def _add_extra_attributes(self, attributes: list[tuple[str, str | Creation]]) -> None:
        """\
        Regardless of creature type, there is a random chance to have a number
        of attributes. They are appended to the attributes list.\
        """
        count_dist = {
            1: 0.30,
            2: 0.30,
            3: 0.20,
            4: 0.20,
        }
        count = self._choose_from_dist(1, count_dist)

    def _add_tags(self):
        pass
