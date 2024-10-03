from typing import TYPE_CHECKING

from rosidl_candb_pycommon import deduce_signal_type

if TYPE_CHECKING:
    import cantools.database

CAN_SIGNAL_TYPES_TO_IDL = {
    'bool': 'boolean',
    'float': {32: 'float', 64: 'double'},
    'int': {
        True: {8: 'int8', 16: 'int16', 32: 'int32', 64: 'int64'},
        False: {8: 'uint8', 16: 'uint16', 32: 'uint32', 64: 'uint64'},
    },
}

def deduce_idl_type(
        signal: 'cantools.database.Signal',
        *,
        raw: bool = False
) -> str:
    return deduce_signal_type(
        signal=signal,
        types=CAN_SIGNAL_TYPES_TO_IDL,
        raw=raw,
    )
