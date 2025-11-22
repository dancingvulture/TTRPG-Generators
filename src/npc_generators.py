"""
Generate various types of NPCs.
"""


from src._generator import KnaveGenerator
from src.name_generators import _NameGenerator
import src.generators as generators
from random import choice, choices


class FantasyNPCs(KnaveGenerator, _NameGenerator):
    """
    Generate Fantasy NPCs
    """
    def _generator(self) -> str:
        templates = (
            "*name_and_race* (*detail*)",
        )
        chosen_template = choice(templates)
        return self._substitute_headers(chosen_template)

    def _get_name_and_race(self) -> str:
        templates_and_weights = [
            ("*human_name*", 0.5),
            ("*dwarf_name*", 0.25),
            ("*elf_name*", 0.25)
        ]
        templates, weights = zip(*templates_and_weights)
        template_chosen = choices(templates, weights=weights)[0]
        return self._substitute_headers(template_chosen)

    def _get_human_name(self) -> str:
        return self._get_other_generator_output("name", "humans")

    def _get_dwarf_name(self) -> str:
        return self._get_other_generator_output("name", "dwarves")

    def _get_elf_name(self) -> str:
        return self._get_other_generator_output("name", "elves")

    def _get_fantasy_mundane(self) -> str:
        return self._get_other_generator_output("item", "fantasy-mundane")

    def _get_detail(self) -> str:
        templates = (
            "*archetype*", "*personality*", "*npc detail*", "asset:*asset*",
            "liability:*liability*", "mannerism:*mannerism*", "has *mundane item*"
        )
        template_chosen = choice(templates)
        return self._substitute_headers(template_chosen)
