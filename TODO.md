# Bugs


# Generators
- Tomb of Adventure Design
  - [ ] ToadMagicalTrapGenerator
  - [ ] ToadComplexTrapGenerator
  - [ ] ToadTransitionGenerator
  - [ ] ToadArchwayGenerator
  - [ ] ToadDoorGenerator
  - [x] ToadBridgeGenerator
  - [ ] ToadTeleportationGenerator
  - [x] ToadArchitecturalTrickGenerator
  - [x] ToadPillarGenerator
  - [x] ToadFurnitureGenerator
  - [x] ToadStatueGenerator
  - [x] ToadThroneGenerator
  - [ ] ToadLevelChangeGenerator
  - [ ] ToadSarcophagusGenerator
- Perilous wilds
  - The details table, in particular, could be used widely across many generators
- Treasure
- The ironforged oracle tables
- Art generator, for wall carvings, tapestries, paintings, etc

Much of the above might be possible by the names alone, for example to find generators, `GeneratorLibrary` could look into `x_generator` modules and pull every name ending in `Generator`.
# New Feature Ideas
- Find a way to implement `kwargs` as input to `Generator.generate()`, especially making it work with the command line interface
- Find a way to save results, and re-roll parts of it (might be easier with a GUI).
- Rework the keyword search to actually be useful on `Creation` objects.
- Allow regular expressions to work with keyword searches.

# Refactoring
- See if you can't create some syntax so exhausted headers can have a different display name than their column header. Probably something like `*header $$ display*`
- At this point most of the "special case funcs" are just calls to other generators (outside of surname and inn name ones in `KnaveGenerator`). Might make sense to rework that entire function to just call to other generators.
- With the sheer number of tables, it may be a good idea to, instead of having them all stored by-column in a dictionary, store them first by file, THEN by column. So the column names don't have to get gigantic. New syntax will likely have to be created to support this, i.e. `table: column` or something. This should pair well with explicit exhausted header substitutes.

## Reduce Code Maintenance
Currently, to add a new generator you have to add its code to a `x_generators` module and an entry for it in the `GeneratorLibrary` it would be nice if all the code needed for a new generator could be in one place.
- See if it's possible to find a way for `GeneratorLibrary` to automatically build the generator list by itself.
- See if it's possible for the command_line interface to automatically build itself.
- Have special exception func list built automatically during `LinkedGenerator`'s init, rather than needing to be explicitly passed.

## Pie in the Sky
- Maybe design a GUI? Replaced headers could be hover text instead of being displayed below.
- Might be worth it to change the table file syntax to parse markdown tables instead of the raw text being used. 
