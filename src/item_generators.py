"""
Generate various kinds of items.
"""


from src._generator import KnaveGenerator
from src.name_generators import _NameGenerator
from random import choice


class Magic(KnaveGenerator, _NameGenerator):
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


class FantasyMundane(KnaveGenerator, _NameGenerator):
    """
    Generate mundane fantasy items.
    """
    def _generator(self) -> str:
        templates = (
            "*tool*",
            "*misc. item*",
            "book:*book*",
            "*clothing*",
            "*treasure*",
            "*weapon*",

            "book:*book* bound in *fabric*",
            "*clothing* made from *fabric*",

            "*tool* made of *material*",
            "*misc. item* made of *material*",
            "*clothing* made of *material*",
            "*weapon* made of *material*",

            "*tool* decoration:*decoration*",
            "*misc. item* decoration:*decoration*",
            "book:*book* decoration:*decoration*",
            "*clothing* decoration:*decoration*",
            "*treasure* decoration:*decoration*",
            "*weapon* decoration:*decoration*",

            "*item trait* *tool*",
            "*item trait* *misc. item*",
            "*item trait* book of *book*",
            "*item trait* *clothing*",
            "*item trait* *treasure*",
            "*item trait* *weapon*",
        )
        template_chosen = choice(templates)
        return self._substitute_headers(template_chosen)
