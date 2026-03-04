# Reduce Code Maintenance
Currently, to add a new generator you have to add its code to a `x_generators` module and an entry for it in the `GeneratorLibrary` it would be nice if all the code needed for a new generator could be in one place.
- See if it's possible to find a way for `GeneratorLibrary` to automatically build the generator list by itself.
- See if it's possible for the command_line interface to automatically build itself.
- Have special exception func list built automatically during `LinkedGenerator`'s init, rather than needing to be explicitly passed.

Much of the above might be possible by the names alone, for example to find generators, `GeneratorLibrary` could look into `x_generator` modules and pull every name ending in `Generator`.
# New Feature Ideas
- Find a way to implement `kwargs` as input to `Generator.generate()`, especially making it work with the command line interface
- Find a way to save results, and re-roll parts of it (might be easier with a GUI).
- Rework the keyword search to actually be useful on `Creation` objects.
- Allow regular expressions to work with keyword searches.

# Refactoring
- See if you can't 

# Pie in the Sky
- Maybe design a GUI? Replaced headers could be hover text instead of being displayed below.
