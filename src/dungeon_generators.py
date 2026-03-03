"""\
Generators for things that are in dungeons, or parts of dungeons.\
"""


from src._generator import Creation, ToadGenerator


class ToadBasicMechanicalTrapGenerator(ToadGenerator):
    """\
    Generates basic mechanical traps using the Tome of Adventure Design (2nd edition)
    table 3-126, pg. 217.\
    """
    def _generator(self) -> Creation:
        trap = self._substitute_headers("*basic mechanical trap*")
        return Creation("Trap, basic mechanical", ("Mechanism", trap))

    def _get_trap_gas(self) -> Creation:
        """\
        Get a gas meant to be part of a trap.\
        """
        return self._get_other_generator_output("dungeon", "trap-gasses")

    def _get_missile_trap(self) -> Creation:
        """\
        Get a basic missile trap.\
        """
        return self._get_other_generator_output("dungeon", "missile-traps")


class ToadTrapGasGenerator(ToadGenerator):
    """\
    Generate gasses meant to be part of a trap. Uses Tomb of Adventure Design (2nd end)
    pp. 219-220.\
    """
    def _generator(self) -> Creation:
        properties = [
            ("effect", self._get_entry("trap gas effect")),
            ("behavior", self._get_entry("trap gas behavior"))
        ]
        return Creation("Gas", *properties)


class ToadMissileTrapGenerator(ToadGenerator):
    """\
    Generate missile traps using the Tome of Adventure Design (2nd edition)\
    table 3-130, pg. 221.
    """
    def _generator(self) -> Creation:
        missile_type = ("missile type", self._get_entry("trap missile type"))
        special = ("special", self._get_entry("missile trap special"))

        if special != "none":
            return Creation("missile trap", missile_type)
        else:
            return Creation("missile trap", missile_type, special)


class ToadSarcophagusGenerator(ToadGenerator):
    """\
    Generate Sarcophagi using the tables in the Tomb of Adventure Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        pass

