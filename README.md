# Dependencies
- None

# To-Do
- See if there is some way you can't save the random seed used for a given run, so bugs can be easier to recreate.
- See if you can't get `Generator._capitalize` to have a smarter implementation.
- Add a generic version of "get attributes" to `CreationWithAttributes`.
- Ooze generator.
- Clean-up unit test functions.
# Procedures
## Add a new generator 
1. Find or create a generator category.
2. Add the generator and its logic to the generator category's module. 
   1. Make sure to make it a child class of whatever base generators(s) make the most sense. At the very minimum you will need to subclass the base `Generator` class.
   2. Override the `_generator` method with whatever logic is needed for this new generator. The output of this method is always a single output (usually a string).
3. Create an entry in the `GeneratorLibrary` class for this generator.
   1. Each category has a dictionary inside `GeneratorLibrary`, the key is the name of the generator in the form of a string(e.g. "humans", "locations", etc.) The value is a tuple containing the generator and its init arguments.
   2. Decide on the string name, remember this will be used in the command line interface to actually use the generator.
   3. The first entry in the value tuple is always a direct reference to the generator's class, while all others are init arguments used by `main`.
4. Done! The generator will appear as an option in `main`, and can be used inside other generators.
## Add a new generator category
1. Create an appropriately named module.
   1. At the top of the module create a class that represents generator output. Must be a subclass of `Creation`. You'll need to make sure all appropriate methods are overridden.
   2. Add a new generator (see above).
2. Create entries in `GeneratorLibrary`
   1. Make sure your module is imported in absolute terms: `src.new_module as new_module`. Otherwise there will be a circular import error.
   2. Create an appropriately named dictionary to `GeneratorLibrary`'s init, e.g. `self.new_module`.
   3. Create an entry to `self.generators_by_type`, declaring the name of the new generator type as the key (in string form), and the value a link to the `GeneratorLibrary` dictionary.
3. Create a new subparser in `command_line`
   1. Create its subparser function, with a name like `_add_new_module_subparser`. It should take the same arguments as the other subparser functions.
   2. Makes sure the function is called in `parse_arguments`.
4. Add an entry in the `main` logic tree for the new subparser, look to the other entries for guidance on what it should look like.
