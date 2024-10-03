from typing import TYPE_CHECKING
from typing import List
from typing import Tuple

if TYPE_CHECKING:
    import cantools.database.Message


def filter_messages(
        messages: List['cantools.database.Message'],
        node_names: List[str] = None,
        message_names: List[str] = None,
        strict: bool = False,
) -> Tuple[List[str], List[str], List[str]]:
    if node_names is not None:
        messages = [
            m
            for m in messages
            if (len(m.senders) == 0 or
                len(m.receivers) == 0 or
                any([
                    n in node_names
                    for n in set(m.senders) | set(m.receivers)
                ]))
        ]

    if message_names is not None:
        messages = [
            m
            for m in messages
            if m.name in message_names
        ]

    if strict:
        messages = [
            m
            for m in messages
            if len(m.senders) > 0 or len(m.receivers) > 0
        ]

    return messages
