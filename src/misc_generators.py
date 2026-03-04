"""\
Shoving any generator in here that doesn't fit with a particular category,
I'll probably end up moving things out of this frequently.\
"""


from rich.table import Table

from src._generator import Creation, Generator, ToadGenerator
from src._display import get_minimal_table_settings


class PlantGenerator(Generator):
    """
    Create plants using the tables in the Herbalist's Primer (pp. 298-301)
    """
    def _generator(self) -> Creation:
        name = self._get_entry("name 1") + " " + self._get_entry("name 2")
        properties = [
            ("rarity", self._get_entry("rarity")),
            ("habit", self._get_entry("habit")),
            ("property", prop := self._get_entry("property")),
            ("climate", self._get_entry("climate")),
            ("biome", self._get_entry("biome")),
            ("quirk", self._get_entry("quirk")),
            ("complication", self._get_entry("complication"))
        ]
        count_distribution = {
            0: 0.28,
            1: 0.28,
            2: 0.28,
            3: 0.1,
            4: 0.06,
        }
        effect_count = self._choose_from_dist(1, count_distribution)

        required_effect = self._get_required_effect(prop)
        if required_effect:
            count_adjustment = 1
            all_effects = [self._get_effect(effect_type=required_effect)]
            effect_count = 1 if effect_count == 0 else effect_count
        else:
            count_adjustment = 0
            all_effects = []

        for _ in range(effect_count - count_adjustment):
            effect = self._get_effect()
            all_effects.append(effect)

        if all_effects:
            properties.append(("known effects", Creation("", *all_effects)))

        return Creation(name, *properties)


    @staticmethod
    def _get_required_effect(prop: str) -> str:
        """
        Some properties would logically require a specific effect, if that's so
        the name of the appropriate effect table will be returned, otherwise
        an empty string is returned.
        """
        if prop in ["magical", "medicinal", "poisonous"]:
            return f"{prop} effect"
        else:
            return ""

    def _get_effect(self, effect_type: str =None) -> tuple[str, str]:
        """
        Get a random effect, optionally, specify a specific type of effect.
        If none is chosen, it defaults to picking a random one.
        """
        if not effect_type: effect_type = self._get_entry("effect type")

        plant_material = self._get_entry("plant material")
        method = self._get_entry("method")
        effect = self._get_entry(effect_type)
        return "", f"Its {plant_material}, when {method}, will {effect}"


class MagicalSymbol(Creation):
    """\
    Description of a magical symbol.\
    """
    def __rich__(self) -> str:
        basic_form = self.attributes["basic form"]
        first_change = self.attributes["first change"]
        second_change = self.attributes["second change"]

        symbol = f"[b]{basic_form}[/b]" + ", " + first_change
        if second_change != "no further modification":
            symbol += ", " + second_change

        return symbol

    @property
    def spacing_preference(self) -> str | int:
        return 0


class ToadMagicSymbolGenerator(ToadGenerator):
    """\
    Generate descriptions of magical symbols. Using tables in the Tome of
    Adventure Design (2nd edition), pg. 146.\
    """
    def _generator(self) -> Creation:
        properties = [
            ("basic form", self._substitute_headers("*basic form*")),
            ("first change", self._substitute_headers("*first change*")),
            ("second change", self._substitute_headers("*second change*")),
        ]
        return MagicalSymbol("Magical Symbol", *properties)


class ToadClueGenerator(ToadGenerator):
    """\
    Generate clues using the tables on pp.140-145 from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        clue_types = {
            "a coded and deliberate message from *author*, to *recipient*,"
            " containing *useful information*": 1,
            "a coded and deliberate message from *author*, to anyone,"
            " containing *useful information*": 1,
            "*evidence of mechanism use*": 1,
            "*writing*": 1,
            "something that is an inherent part of the general decoration,"
            " architecture, environment, or atmosphere": 1,
            "remnants of a(n): *event type*": 1,
        }
        clue = self._choose_from_dist(1, clue_types)
        clue = self._substitute_headers(clue)
        return Creation("clue", ("content", clue))

    def _get_writing(self) -> Creation:
        return self._get_other_generator_output("misc", "writing")

    def _get_monster(self) -> Creation:
        return self._get_other_generator_output("monster", "knave-monsters")

    def _get_author(self) -> Creation:
        return self._substitute_headers("*from whom*")

    def _get_recipient(self) -> Creation:
        return self._substitute_headers("*to whom*")


class Writing(Creation):
    """\
    A creation that represents writing.\
    """
    def __rich__(self) -> Table:
        settings = get_minimal_table_settings()
        table = Table(**settings)
        table.add_column()
        table.add_column()

        writing = self.attributes["nature"]
        table.add_row("[b][i]Writing:[/b][/i]", writing)
        return table

    @property
    def spacing_preference(self) -> str | int:
        writing = self.attributes["nature"]
        if isinstance(writing, Creation):
            return 1
        else:
            return 0


class ToadWritingGenerator(ToadGenerator):
    """\
    Generate writing. Uses tables on pp.144-145 from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        writing = ("nature", self._substitute_headers("*nature of writing*"))
        return Writing("writing", writing)

    def _get_book(self) -> Creation:
        return self._get_other_generator_output("item", "books")

    def _get_item(self) -> Creation:
        return self._get_other_generator_output("item", "fantasy-mundane")
