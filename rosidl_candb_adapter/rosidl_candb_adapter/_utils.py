from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable

    import cantools.database

import re

from ._can_to_message_types import CAN_TO_MSG_TYPES


def _is_integer(value: int | float) -> bool:
    match value:
        case int():
            return True
        case float():
            return value.is_integer()
        case _:
            raise TypeError(f"Unsupported type {type(value)}")


def _find_closest_signal_type(bits: int | float, types: dict[int, str]) -> str:
    for type_bits, type_name in sorted(types.items()):
        if bits <= type_bits:
            return type_name
    else:
        raise RuntimeError(f'No suitable type for {bits} bits')


def filter_tuples(
        *required: str,
        allowed: list[str],
        tuples: 'Iterable[str]',
        separator: str = ':',
):
    min_tuple_len = len(required)

    for tup in tuples:
        parts = tup.split(separator)

        if len(parts) < min_tuple_len:
            raise ValueError(f"Invalid tuple '{tup}'")

        for part, req in zip(parts[:min_tuple_len], required):
            if part != req:
                continue

        if parts[min_tuple_len] not in allowed:
            continue

        yield separator.join(parts[min_tuple_len:])


def filter_messages(
        messages: 'Iterable[cantools.database.Message]',
        node_names: list[str] = None,
        message_names: list[str] = None,
        strict: bool = False,
):
    for message in messages:
        if strict and len(message.senders) == 0 and len(message.receivers) == 0:
            continue

        if node_names is not None and all(n not in node_names for n in set(message.senders) | set(message.receivers)):
            continue

        if message_names is not None and message.name not in message_names:
            continue

        yield message


def not_none(x):
    return x is not None


def signal_constants(signal) -> dict:
    constants = {
        'scale': signal.scale,
        'offset': signal.offset,
    }

    if signal.initial:
        constants['initial'] = signal.initial

    if signal.invalid:
        constants['initial'] = signal.invalid

    if signal.choices:
        choice_constants = constants['choices'] = dict()

        for choice in sorted(signal.choices.values(), key=lambda c: c.value):
            choice_name = re.sub('\s+', ' ', choice.name)
            if choice_name not in constants:
                choice_constants[choice_name] = [choice]
            else:
                choice_constants[choice_name].append(choice)

    return constants

def format_message_constant(value, type: str) -> str:
    if type == CAN_TO_MSG_TYPES['uint'][1]:
        return 'true' if value else 'false'
    else:
        return str(value)
