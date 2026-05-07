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
            "*trap*": "_get_trap",
            "*basic mechanical trap*": "_get_trap_basic_mechanical",
            "*trap gas*": "_get_trap_gas",
            "*missile trap*": "_get_missile_trap",
            "*pit trap*": "_get_pit_trap",
            "*magical trap*": "_get_magical_trap",
            "*complex trap*": "_get_complex_trap",
            "*archway*": "_get_archway",
            "*door*": "_get_door",
            "*unusual mechanism*": "_get_unusual_mechanism",
            "*bridge*": "_get_bridge",
            "*corridor*": "_get_corridor",
            "*architectural trick*": "_get_architectural_trick",
            "*pillar*": "_get_pillar",
            "*furniture*": "_get_furniture",
            "*throne*" : "_get_throne",
            "*statue*": "_get_statue",
            "*level change*": "_get_level_change",
            "*stairs*": "_get_stairs",
            "*teleportation*": "_get_teleportation",
            "*npc*": "_get_npc",
        }
        table_filenames = [
            "toad/map.txt",
            "toad/traps.txt",
            "toad/tricks.txt"
        ]
        special_case_funcs.update(additional_special_case_funcs)
        table_filenames += additional_tables
        super().__init__(force_table_update,
                         table_filenames,
                         special_case_funcs,
                         )

    def _get_trap(self) -> Creation:
        return self._get_other_generator_output("dungeon", "traps")

    def _get_trap_basic_mechanical(self) -> Creation:
        return self._get_other_generator_output("dungeon", "basic-mechanical-traps")

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

    def _get_magical_trap(self) -> Creation:
        return self._get_other_generator_output("dungeon", "magical-traps")

    def _get_complex_trap(self) -> Creation:
        return self._get_other_generator_output("dungeon", "complex-traps")

    def _get_archway(self) -> Creation:
        return self._get_other_generator_output("dungeon", "archways")

    def _get_door(self) -> Creation:
        return self._get_other_generator_output("dungeon", "doors")

    def _get_unusual_mechanism(self) -> Creation:
        template = ("*unusual mechanism action* *unusual mechanism object*"
                    " *unusual mechanism modifier*")
        return self._substitute_headers(template)

    def _get_bridge(self) -> Creation:
        return self._get_other_generator_output("dungeon", "bridges")

    def _get_corridor(self) -> Creation:
        return self._get_other_generator_output("dungeon" ,"corridors")

    def _get_architectural_trick(self) -> Creation:
        return self._get_other_generator_output("dungeon", "architectural-tricks")

    def _get_pillar(self) -> Creation:
        return self._get_other_generator_output("dungeon", "pillars")

    def _get_furniture(self) -> Creation:
        return self._get_other_generator_output("dungeon", "furniture")

    def _get_throne(self) -> Creation:
        return self._get_other_generator_output("dungeon", "thrones")

    def _get_statue(self) -> Creation:
        return self._get_other_generator_output("dungeon", "statues")

    def _get_level_change(self) -> Creation:
        return self._get_other_generator_output("dungeon", "level-changes")

    def _get_stairs(self) -> Creation:
        return self._get_other_generator_output("dungeon", "stairs")

    def _get_teleportation(self) -> Creation:
        return self._get_other_generator_output("dungeon", "teleportation")

    def _get_npc(self) -> Creation:
        return self._get_other_generator_output("npc", "fantasy")

###########################################
################## TRAPS ##################
###########################################

class ToadTrapGenerator(_ToadDungeonGenerator):
    """\
    This generator just picks, from a probability distribution, another trap
    generator to call.\
    """
    def _generator(self) -> Creation:
        trap_distribution = {
            ("dungeon", "basic-mechanical-traps"): 1,
        }
        gen_type, gen_name = self._choose_from_dist(1, trap_distribution)
        return self._get_other_generator_output(gen_type, gen_name)


class ToadBasicMechanicalTrapGenerator(_ToadDungeonGenerator):
    """\
    Generates basic mechanical traps using the Tome of Adventure Design (2nd edition)
    table 3-126, pg. 217.\
    """
    def _generator(self) -> Creation:
        attributes = [
            ("mechanism", self._substitute_headers("*trap, basic mechanical*"))
        ]
        self._add_extra_attributes(attributes)
        return Creation("Trap, basic mechanical", *attributes)

    def _add_extra_attributes(self, attributes):
        """\
        Random chance to add extra attributes, it's possible nothing will be
        added, attributes are appended directly.\
        """
        concealment_dist = {
            True: 0.4,
            False: 0.6,
        }
        complex_trigger_dist = {
            True: 0.2,
            False: 0.8,
        }

        if self._choose_from_dist(1, concealment_dist):
            attributes.append(("concealment", self._substitute_headers("*trap, concealment*")))

        if self._choose_from_dist(1, complex_trigger_dist):
            attributes.append(("trigger", self._substitute_headers("*trap, complex trigger*")))


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
        type_ = ("type", self._substitute_headers("*trap, pit*"))
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


###########################################
################### MAP ###################
###########################################

class ToadTransitionGenerator(_ToadDungeonGenerator):
    """\
    Generate transitions using table (pg. 150) from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        raise NotImplementedError()


class ToadArchwayGenerator(_ToadDungeonGenerator):
    """\
    Generate archways using table (pg. 151) from the Tomb of Adventure Design
    (2nd edition).\
    """
    def _generator(self) -> Creation:
        raise NotImplementedError()


class ToadBridgeGenerator(_ToadDungeonGenerator):
    """\
    Generate bridges using table (pg. 151) from the Tomb of Adventure Design
    (2nd edition).\
    """
    def _generator(self) -> Creation:
        attributes = [
            ("material", self._substitute_headers("*bridge, material*")),
        ]
        self._add_unusual_features(attributes)
        return Creation("bridge", *attributes)


    def _add_unusual_features(self,
                              attributes: list[tuple[str, str | Creation]]
                              ) -> None:
        """\
        Append unusual features to a list of bridge attributes. \
        """
        unusual_feature_count_dist = {
            0: 0.75,
            1: 0.20,
            2: 0.05,
        }
        count = self._choose_from_dist(1, unusual_feature_count_dist)
        for _ in range(count):
            attr = self._substitute_headers("*bridge, unusual feature*")
            attributes.append(("unusual feature", attr))


class ToadCorridorGenerator(_ToadDungeonGenerator):
    """\
    Generate corridors using tables (pg. 150) from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        # The outcome of shape may produce roll-able dice.
        shape = self._substitute_headers("*corridor, shape*")
        attributes = [
            ("shape", shape),
            ("construction", self._substitute_headers("*corridor, construction*")),
            ("width", self._substitute_headers("*corridor, width*")),
            ("height", self._substitute_headers("*corridor, height*")),
        ]
        self._add_unusual_features(attributes)

        return Creation("corridor", *attributes)

    def _add_unusual_features(self,
                              attributes: list[tuple[str, str | Creation]]
                              ) -> None:
        """\
        Add zero to two unusual features to a corridor's attributes.
        append changes directly to the list.\
        """
        unusual_features_distribution = {
            0: 0.4,
            1: 0.4,
            2: 0.2,
        }
        unusual_features_count = self._choose_from_dist(1, unusual_features_distribution)
        for num in range(unusual_features_count):
            feature = (
                f"unusual feature",
                self._substitute_headers("*corridor, unusual features*")
            )
            attributes.append(feature)


class ToadDoorGenerator(_ToadDungeonGenerator):
    """\
    Generate doors using tables (pp. 152-153) from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        attr_count_dist = {
            0: 0.50,
            1: 0.30,
            2: 0.15,
            3: 0.05,
        }
        count = self._choose_from_dist(1, attr_count_dist)

        attr_type_dist = {
            "material": 1,
            "color": 1,
            "opens": 1,
            "oddity": 1,
            "unusual shape": 1,
        }
        attr_types = self._choose_from_dist(count, attr_type_dist, repeats=False)
        if isinstance(attr_types, str): attr_types = [attr_types]
        attributes = []
        for at in attr_types:
            attr = (at, self._substitute_headers(f"*door, {at}*"))
            attributes.append(attr)

        return Creation("door", *attributes)


class ToadTeleportationGenerator(_ToadDungeonGenerator):
    """\
    Generate teleporters using tables (pp. 156-157) from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        raise NotImplementedError()


class ToadPillarGenerator(_ToadDungeonGenerator):
    """\
    Generate pillars using table 3-69 (pg. 173) from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        attributes = [
            ("description", self._substitute_headers("*pillar, description*")),
        ]
        decoration = self._substitute_headers("*pillar, decoration*")
        if decoration != "none":
            attributes.append(("decoration", decoration))
        return Creation("pillar", *attributes)


class ToadFurnitureGenerator(_ToadDungeonGenerator):
    """\
    Generate furniture using table 3-63 (pg. 170) from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        kind = self._substitute_headers("*furniture, type*")
        if isinstance(kind, Creation): return kind

        feature = ("feature", self._substitute_headers("*furniture, unusual feature*"))
        if feature[1] != "none":
            return Creation(kind, feature)
        else:
            return Creation(kind)


class ToadStatueGenerator(_ToadDungeonGenerator):
    """\
    Generate statues using tables (pp. 176-177) from the Tomb of
    Adventure Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        attributes = (
            ("material", self._substitute_headers("*statue, material*")),
            ("condition", self._substitute_headers("*statue, condition*")),
            ("subject", self._substitute_headers("*statue, subject*"))
        )
        return Creation("statue", *attributes)


class ToadThroneGenerator(_ToadDungeonGenerator):
    """\
    Generate thrones using tables (pp. 178-181) from the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        name = (self._substitute_headers("*throne, name 1*") + " "
                + self._substitute_headers("*throne, name 2*"))
        detail = ("detail", self._substitute_headers("*throne, detail*"))
        return Creation(name, detail)


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


###########################################
################# TRICKS ##################
###########################################

class ToadArchitecturalTrickGenerator(_ToadDungeonGenerator):
    """\
    Generate architectural tricks using tables (pp. 190-191) from the Tomb
    of Adventure Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        attributes = (
            (
                "central feature",
                self._substitute_headers("*architectural trick, central feature*")
            ),
            (
                "how it functions",
                self._substitute_headers("*architectural trick, how it functions*")
            ),
            (
                "what happens",
                self._substitute_headers("*architectural trick, what happens when functioning*")
            ),
            (
                "what is accessed",
                self._substitute_headers("*architectural trick, what is accessed*")
            )
        )
        return Creation("architectural trick", *attributes)


###########################################
################### MISC ##################
###########################################

class ToadSarcophagusGenerator(_ToadDungeonGenerator):
    """\
    Generate Sarcophagi using the tables (pp. 252-253) in the Tomb of Adventure
    Design (2nd edition).\
    """
    def _generator(self) -> Creation:
        raise NotImplementedError()
