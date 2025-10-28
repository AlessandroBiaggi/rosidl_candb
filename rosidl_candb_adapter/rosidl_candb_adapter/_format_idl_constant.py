from typing import Any

from cantools.database.namedsignalvalue import NamedSignalValue

from ._deduce_idl_type import CAN_SIGNAL_TYPES_TO_IDL


def format_idl_constant(v: Any, idl_type: str) -> str:
    if isinstance(v, NamedSignalValue):
        v = v.value

    if idl_type == CAN_SIGNAL_TYPES_TO_IDL['bool']:
        return 'TRUE' if bool(v) else 'FALSE'
    elif idl_type in CAN_SIGNAL_TYPES_TO_IDL['float'].values():
        return f"{float(v)}"
    elif (
            idl_type in CAN_SIGNAL_TYPES_TO_IDL['int'][True].values()
            or
            idl_type in CAN_SIGNAL_TYPES_TO_IDL['int'][False].values()
    ):
        try:
            return f"{int(v)}"
        except Exception as e:
            raise ValueError(f"type: {type(v)} repr: {repr(v)}") from e
    else:
        raise ValueError(f"Unsupported IDL type '{idl_type}' for constant value '{v}'")
