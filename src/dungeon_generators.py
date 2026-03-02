"""\
Generators for things that are in dungeons, or parts of dungeons.\
"""


from src._generator import Creation, ToadGenerator


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


class BasicMechanicalTraps(ToadGenerator):
    """\
    Generates basic mechanical traps using the Tome of Adventure Design (2nd edition)
    table 3-126, pg. 217.\
    """



class Sarcophagus(ToadGenerator):
    """\
    Generate Sarcophagi using the tables in the Tomb of Adventure Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        pass

