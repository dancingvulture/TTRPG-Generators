"""\
Generators for things that are in dungeons, or parts of dungeons.\
"""


from src._generator import Creation, ToadGenerator


class BasicMechanicalTraps(ToadGenerator):
    """\
    Generates basic mechanical traps using the Tome of Adventure Design (2nd edition)
    table 3-126, pg. 217.\
    """


class TrapGasses(ToadGenerator):
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


class MissileTraps(ToadGenerator):
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



class Sarcophagus(ToadGenerator):
    """\
    Generate Sarcophagi using the tables in the Tomb of Adventure Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        pass

