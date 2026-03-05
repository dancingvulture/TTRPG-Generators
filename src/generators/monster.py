"""
Contains monster generator classes.
"""


from src.generators._generator import Creation, LinkedGenerator, KnaveGenerator
from src.dice import Roller
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
            value = self._roll_dice(value)
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
        for trait_num in range(1, trait_count + 1):
            trait = self._substitute_headers("*monster trait*")
            attributes.append((f"trait {trait_num}", trait))

        return KnaveMonster(monster_type, *attributes)
    