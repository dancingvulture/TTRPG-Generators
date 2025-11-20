"""
Generate various kinds of items.
"""


from src._generator import KnaveGenerator
from src.name_generators import _NameGenerator
from random import choice


class MagicItem(KnaveGenerator, _NameGenerator):
    """
    Generate magic items using the Knave 2e tables.
    """
    def _generator(self) -> str:
        templates = [
            "*item_base* (effect: *effect*)"
        ]
        template_chosen = choice(templates)
        return self._substitute_headers(template_chosen)

    def _get_item_base(self) -> str:
        bases = ["*tool*", "*misc. item*", "*book*", "*clothing*",
                 "*treasure*", "*weapon*"]
        chosen_base = choice(bases)
        return self._substitute_headers(chosen_base)
