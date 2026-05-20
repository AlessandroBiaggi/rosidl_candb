import math

import cantools.database

from ._can_to_message_types import CAN_TO_MSG_TYPES
from ._utils import _find_closest_signal_type, _is_integer


def deduce_message_type(signal: cantools.database.Signal, *, raw: bool = False) -> str:
    if raw:
        try:
            return _find_closest_signal_type(signal.length, CAN_TO_MSG_TYPES['int'])
        except RuntimeError as e:
            raise RuntimeError(f"Unsupported raw signal '{signal.name}'") from e
    elif signal.is_float:
        try:
            return _find_closest_signal_type(signal.length, CAN_TO_MSG_TYPES['float'])
        except RuntimeError as e:
            raise RuntimeError(f"'Unsupported float signal '{signal.name}'") from e

    is_signed = signal.is_signed or signal.scale < 0
    num_bits = signal.length - 1 if is_signed else signal.length
    max_abs_value = math.pow(2, num_bits) * abs(signal.scale) + abs(signal.offset)

    if _is_integer(signal.scale) and _is_integer(signal.offset):
        assert math.isfinite(max_abs_value), \
            f"Invalid calculated maximum value of signal '{signal.name}': {max_abs_value}"

        num_bits = math.log2(max_abs_value)
        if is_signed:
            num_bits += 1

        assert num_bits > 0, f"Invalid calculated number of bits of signal '{signal.name}': {num_bits}"

        try:
            return _find_closest_signal_type(num_bits, CAN_TO_MSG_TYPES['int' if is_signed else 'uint'])
        except RuntimeError as e:
            raise RuntimeError(f"Unsupported integer signal '{signal.name}'") from e
    else:
        types = CAN_TO_MSG_TYPES['float']

        if max_abs_value <= (2 - 2 ** -23) * 2 ** 127:
            return types[32]
        elif max_abs_value <= (2 - 2 ** -52) * 2 ** 1023:
            return types[64]

        raise RuntimeError(f"Unsupported decimal signal '{signal.name}'") \
            from RuntimeError(f"No suitable type for scale {signal.scale} and offset {signal.offset}")
