"""\
Generate player characters from various systems.\
"""


from collections import Counter

from src.generators._generator import Creation, KnaveGenerator


class KnaveAbilityScores(Creation):
    """\
    A creation holding a set of ability scores\
    """
    def __rich__(self) -> str:
        """\
        A nice abbreviated display method.\
        """
        score_abbreviations = {
            "strength": "STR",
            "dexterity": "DEX",
            "constitution": "CON",
            "intelligence": "INT",
            "wisdom": "WIS",
            "charisma": "CHA",
        }
        display_scores = []
        for ability, score in self.attributes.items():
            score = score[0]
            if score != "0":
                abbrev = score_abbreviations[ability]
                display = f"{abbrev} +{score}"
                display_scores.append(display)
        return ", ".join(display_scores)

class KnavePCGenerator(KnaveGenerator):
    """\
    Generate first level human knave PCs.\
    """
    def _generator(self) -> Creation:
        name = self._get_name()
        attributes = [
            ("Hit points", self._get_hp()),
            ("abilities", abilities := self._get_abilities()),
        ]
        intelligence = int(abilities.attributes["intelligence"][0])
        careers, equipment = self._get_careers_and_equipment(intelligence)

        attributes.append(("career", careers))
        attributes.append(("equipment", equipment))

        self._add_attributes(attributes)
        return Creation(name, *attributes)


    def _get_name(self) -> str:
        """\
        Get a name from the Knave name tables, with a random chance of having a
        surname as well.\
        """
        name = self._get_entry("name")
        has_surname_dist = {
            True: 0.4,
            False: 0.6,
        }
        has_surname = self._choose_from_dist(1, has_surname_dist)
        if has_surname:
            name += " " + self._get_surname()

        return name

    def _get_abilities(self) -> KnaveAbilityScores:
        """\
        Distribute three points randomly among the six ability scores.\
        """
        score_counter = Counter(
            {"strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0}
        )
        for _ in range(3):
            scr = self._get_entry("ability score")
            score_counter[scr] += 1

        scores = [(scr, str(count)) for scr, count in score_counter.items()]
        return KnaveAbilityScores("ability scores", *scores)

    def _add_attributes(self,
                        attributes: list[tuple[str, str | Creation]]
                        ) -> None:
        """\
        Add a few random attributes to lend some characterization. Appends to an
        existing attribute list.\
        """
        attribute_types = {
            "personality": 1,
            "npc detail": 1,
            "asset": 1,
            "liability": 1,
            "mannerism": 1,
            "mundane item": 1,
        }
        additional_attribute_count_dist = {
            1: 0.5,
            2: 0.3,
            3: 0.2,
        }
        count = self._choose_from_dist(1, additional_attribute_count_dist)
        new_attributes = self._choose_from_dist(count, attribute_types, repeats=False)
        if isinstance(new_attributes, str): new_attributes = [new_attributes]
        for attr in new_attributes:
            attr_tuple = (attr, self._substitute_headers(f"*{attr}*"))
            attributes.append(attr_tuple)

    def _get_careers_and_equipment(self,
                                   intelligence: int
                                   ) -> tuple[str, str]:
        """\
        Get a random career and equipment set.\
        """
        careers = []
        equipment = [
            f"{int(self._roll_dice('$3d6$')) * 10} coins",
            "2 rations",
            "50' of rope",
            "2 torches",
        ]
        for index in range(2):
            car, eqp = self._get_entry("career and equipment").split(":")
            car = car.strip()

            while index == 1 and car == careers[0]:
                car, eqp = self._get_entry("career and equipment").split(":")
                car = car.strip()

            eqp = [e.strip() for e in eqp.strip().split(",")]
            careers.append(car)
            equipment.extend(eqp)

        self._add_spellbooks(equipment, intelligence)
        return ", ".join(careers), ", ".join(equipment)

    def _add_spellbooks(self,
                        equipment: list[str],
                        intelligence: int,
                        ) -> None:
        """\
        Add a number of random spellbooks based on intelligence.\
        """
        for _ in range(intelligence):
            spell = self._get_other_generator_output("name", "spells")
            spellbook = f"spellbook: {spell}"
            equipment.append(spellbook)


    def _get_hp(self) -> str:
        """\
        Roll 1d6 for hp.\
        """
        return self._roll_dice("$1d6$")
