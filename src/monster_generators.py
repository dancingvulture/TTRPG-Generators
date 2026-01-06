"""
Contains monster generator classes.
"""


from src._generator import Creation, LinkedGenerator
from src.dice import Roller
import re


class Monster(Creation):
    """
    Class for containing monster information.
    """
    @property
    def preferred_spacing(self) -> str:
        return "\n\n"


class Oozes(LinkedGenerator):
    """
    Uses tables from the Monster Overhaul (pp. 57-58).
    """
    def _generator(self) -> Creation:
        attributes_template = [
            ("type", "*type*"),
            ("embedded in the ooze", "*embedded*"),
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
    def _roll_dice(text: str) -> str:
        """
        Searches for any rollable dice in the text, which should be bookened by
        '$' (e.g. $1d20$). The dice are rolled, and the result (a sum), is
        substituted in place of the dice string.
        """
        dice_strings = re.compile(r"\$[^$]*\$").findall(text)
        roller = Roller()
        for dice_str in dice_strings:
            roll = roller.sum(dice_str[1:-1])  # Cut out $.
            text = text.replace(dice_str, str(roll), 1)
        return text

    @staticmethod
    def _extract_ooze_type(text: str) -> str:
        sentences = re.compile(r"[\w ]*.").findall(text)
        ooze_type = sentences[0][:-1]
        return ooze_type
