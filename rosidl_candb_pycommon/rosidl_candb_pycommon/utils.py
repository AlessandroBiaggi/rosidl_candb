from typing import Any
from typing import TYPE_CHECKING

import re

if TYPE_CHECKING:
    import cantools.database


def not_none(x: Any) -> bool:
    return x is not None


def escape(text: str) -> str:
    return repr(text)


def message_constants(message: 'cantools.database.Message') -> dict:
    constants = dict()

    for signal in message.signals:
        signal_constants = constants[signal] = dict()

        signal_constants['scale'] = signal.scale
        signal_constants['offset'] = signal.offset

        if signal.initial:
            signal_constants['initial'] = signal.initial

        if signal.invalid:
            signal_constants['invalid'] = signal.invalid

        if signal.choices:
            signal_constant_choices = signal_constants['choices'] = dict()

            for choice in sorted(signal.choices.values(), key=lambda c: c.value):
                choice_name = re.sub('\s+', ' ', choice.name)
                if choice_name not in constants:
                    signal_constant_choices[choice_name] = [choice]
                else:
                    signal_constant_choices[choice_name].append(choice)

    return constants
