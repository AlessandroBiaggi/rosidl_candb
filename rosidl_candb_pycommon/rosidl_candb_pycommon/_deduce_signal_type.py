from typing import Any
from typing import Dict
from typing import TYPE_CHECKING

import math

if TYPE_CHECKING:
    import cantools.database


def deduce_signal_type(
        signal: 'cantools.database.Signal',
        types: Dict[str, Any],
        *,
        raw: bool = False
) -> str:
    if raw:
        if 'int' not in types:
            raise RuntimeError(f"Unsupported raw signals")
        types = types['int']

        if not False in types:
            raise RuntimeError(f"Unsupported raw signals")
        types = types[False]

        try:
            return _find_closest_signal_type(signal.length, types[False])
        except RuntimeError as e:
            raise RuntimeError(f"Unsupported raw signal '{signal.name}'") from e
    elif signal.is_float:
        if 'float' not in types:
            raise RuntimeError(f"Unsupported float signals")
        types = types['float']

        try:
            return _find_closest_signal_type(signal.length, types)
        except RuntimeError as e:
            raise RuntimeError(f"'Unsupported float signal '{signal.name}'") from e
    else:
        is_signed = signal.is_signed or signal.scale < 0
        num_val_bits = signal.length - 1 if is_signed else signal.length
        max_abs_value = math.pow(2, num_val_bits) * abs(signal.scale) + abs(signal.offset)

        assert math.isfinite(max_abs_value), \
            f"Invalid calculated maximum value of signal '{signal.name}': {max_abs_value}"

        if _is_integer(signal.scale) and _is_integer(signal.offset):
            num_bits = math.log2(max_abs_value)
            if is_signed:
                num_bits += 1

            if num_bits <= 1 and signal.scale == 1 and signal.offset == 0 and 'bool' in types:
                return types['bool']

            if 'int' not in types:
                raise RuntimeError(f"Unsupported int signals")
            types = types['int']

            if is_signed not in types:
                raise RuntimeError(f"Unsupported {'signed' if is_signed else 'unsigned'} int signals")
            types = types[is_signed]

            try:
                return _find_closest_signal_type(num_bits, types)
            except RuntimeError as e:
                raise RuntimeError(f"Unsupported integer signal '{signal.name}'") from e
        else:
            if 'float' not in types:
                raise RuntimeError(f"Unsupported float signals")
            types = types['float']

            FLOAT_MAX = (2 - 2 ** -23) * 2 ** 127
            if max_abs_value <= FLOAT_MAX and 32 in types:
                return types[32]

            DOUBLE_MAX = (2 - 2 ** -52) * 2 ** 1023
            if max_abs_value <= DOUBLE_MAX and 64 in types:
                return types[64]

            raise RuntimeError(f"Unsupported decimal signal '{signal.name}'") \
                from RuntimeError(f"No suitable type for scale {signal.scale} and offset {signal.offset}")


def _find_closest_signal_type(bits: int or float, types: Dict[int, str]) -> str:
    for type_bits, type_name in sorted(types.items()):
        if bits <= type_bits:
            return type_name
    else:
        raise RuntimeError(f'No suitable type for {bits} bits')


def _is_integer(value: int or float) -> bool:
    match value:
        case int():
            return True
        case float():
            return value.is_integer()
        case _:
            raise TypeError(f"Unsupported type {type(value)}")
