"""
Shoving any generator in here that doesn't fit with a particular category,
I'll probably end up moving things out of this frequently.
"""


from src._generator import Creation, Generator


class Plant(Generator):
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
            properties.append(("Known Effects", Creation("", *all_effects)))

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
