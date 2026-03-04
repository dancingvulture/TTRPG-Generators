"""\
Package containing all generator modules and the generator library.\
"""


from src.generators._library import GeneratorLibrary
import src.generators._generator as generator


_LIBRARY = GeneratorLibrary()


def get_instance(generator_type: str,
                 generator_name: str,
                 *,
                 force_update: bool=False,
                 ) -> generator.Generator:
    """\
    Get a generator instance by specifying the type and name.\
    """
    gen_by_type = _LIBRARY.generators_by_type
    gen_class, *init_args = gen_by_type[generator_type][generator_name]
    return gen_class(force_update, *init_args)


def get_names(generator_type: str) -> list[str]:
    """\
    Get all generator names for a type of generator.\
    """
    return list(getattr(_LIBRARY, generator_type))
