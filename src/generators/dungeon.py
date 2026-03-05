"""\
Generators for things that are in dungeons, or parts of dungeons.\
"""


from src.generators._generator import Creation, ToadGenerator


class _ToadDungeonGenerator(ToadGenerator):
    """\
    Private base class for all dungeon generators using the Tomb of Adventure
    Design (2nd edition).\
    """
    def __init__(self,
                 force_table_update: bool,
                 additional_tables: list[str],
                 additional_special_case_funcs: dict[str, str]
                 ):
        special_case_funcs = {
            "*trap, basic mechanical*": "_get_trap_basic_mechanical",
            "*trap, magical*": "_get_magical_trap",
            "*trap, complex*": "_get_complex_trap",
            "*unusual mechanism*": "_get_unusual_mechanism",
            "*statue*": "_get_statue",
            "*architectural trick*": "_get_architectural_trick",
            "*level change*": "_get_level_change",
            "*stairs*": "_get_stairs",
            "*teleportation*": "_get_teleportation",
        }
        table_filenames = ["dungeon.txt", "traps.txt"]
        special_case_funcs.update(additional_special_case_funcs)
        table_filenames += additional_tables
        super().__init__(force_table_update,
                         table_filenames,
                         special_case_funcs,
                         )

    def _get_trap_basic_mechanical(self) -> Creation:
        return self._get_other_generator_output("dungeon", "basic-mechanical-traps")

    def _get_magical_trap(self) -> Creation:
        raise NotImplementedError()

    def _get_complex_trap(self) -> Creation:
        raise NotImplementedError()

    def _get_unusual_mechanism(self) -> Creation:
        template = ("*unusual mechanism action* *unusual mechanism object*"
                    " *unusual mechanism modifier*")
        return self._substitute_headers(template)

    def _get_statue(self) -> Creation:
        raise NotImplementedError()

    def _get_architectural_trick(self) -> Creation:
        raise NotImplementedError()

    def _get_level_change(self) -> Creation:
        raise NotImplementedError()

    def _get_stairs(self) -> Creation:
        raise NotImplementedError()

    def _get_teleportation(self) -> Creation:
        raise NotImplementedError()


class ToadBasicMechanicalTrapGenerator(_ToadDungeonGenerator):
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

    def _get_pit_trap(self) -> Creation:
        return self._get_other_generator_output("dungeon", "pit-traps")


class ToadTrapGasGenerator(_ToadDungeonGenerator):
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


class ToadMissileTrapGenerator(_ToadDungeonGenerator):
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


class ToadPitTrapGenerator(_ToadDungeonGenerator):
    """\
    Generate pit traps using table 3-131 (pg. 221) from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        type_ = ("type", self._substitute_headers("*pit trap*"))
        return Creation("pit trap", type_)


class ToadMagicalTrapGenerator(_ToadDungeonGenerator):
    """\
    Generate magical traps using tables (pp. 224-225) from the Tomb of
    Adventure Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        raise NotImplementedError()


class ToadComplexTrapGenerator(_ToadDungeonGenerator):
    """\
    Generate complex traps using tables (pp. 226-230) from the Tomb of
    Adventure Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        raise NotImplementedError()


class ToadCorridorGenerator(_ToadDungeonGenerator):
    """\
    Generate corridors using tables (pg. 150) from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        raise NotImplementedError()


class ToadArchitecturalTrickGenerator(_ToadDungeonGenerator):
    """\
    Generate architectural tricks using tables (pp. 190-191) from the Tomb
    of Adventure Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        raise NotImplementedError()


class ToadStatueGenerator(_ToadDungeonGenerator):
    """\
    Generate statues using tables (pp. 176-177) from the Tomb of
    Adventure Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        raise NotImplementedError()


class ToadLevelChangeGenerator(_ToadDungeonGenerator):
    """\
    Generate a level changes using tables (pg. 164) from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        raise NotImplementedError()


class ToadStairGenerator(_ToadDungeonGenerator):
    """\
    Generate a stairs using tables (pg. 164) from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        attributes = (
            (
                "make",
                self._substitute_headers("*stairs, type*, *stairs, material*")
            ),
            (
                "structural feature",
                self._substitute_headers("*stairs, structural feature*")
            ),
            (
                "distinctive feature",
                self._substitute_headers("*stairs, distinctive feature*")
            ),
            (
                "condition",
                self._substitute_headers("*stairs, condition*")
            )
        )
        return Creation("stairs", *attributes)



class ToadSarcophagusGenerator(_ToadDungeonGenerator):
    """\
    Generate Sarcophagi using the tables (pp. 252-253) in the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        raise NotImplementedError()
