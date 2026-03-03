"""\
Variables used across modules which contain values used when displaying things.\
"""
from typing import Any
from copy import deepcopy

from rich.box import Box


_EMPTY = Box(
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
)
_MINIMAL_TABLE_SETTINGS = {
    "title_justify": "left",
    "show_header": False,
    "box": _EMPTY,
    "pad_edge": False,
    "padding": 0,
    "show_edge": False,
}

def get_minimal_table_settings() -> dict[str, Any]:
    """\
    Get a deepcopy of the minimal table settings.\
    """
    return deepcopy(_MINIMAL_TABLE_SETTINGS)
