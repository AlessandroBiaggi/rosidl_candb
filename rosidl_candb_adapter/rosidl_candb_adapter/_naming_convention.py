import pathlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable


from ._case_style import to_snake_case, to_pascal_case
from ._utils import not_none


class NamingConvention:
    def __init__(self, package_name: str, database_name: str):
        self._package_name = package_name
        self._database_name = database_name

    @staticmethod
    def constant(
            *parts: 'Iterable[str | None]',
            glue: str = '__',
    ) -> str:
        constant_name = glue.join(filter(not_none, parts))
        constant_name = to_snake_case(constant_name).upper()
        if len(constant_name) > 0 and constant_name[0].isdigit():
            constant_name = 'C_' + constant_name
        return constant_name

    @property
    def package_name(self) -> str:
        return self._package_name

    @property
    def database_name(self) -> str:
        return self._database_name

    def message_name(self, message) -> str:
        return to_pascal_case(message.name)

    def stamped_message_name(self, message) -> str:
        return to_pascal_case(message.name) + 'Stamped'

    def message_file(self, message) -> pathlib.Path:
        return pathlib.Path(self.message_name(message)).with_suffix('.msg')

    def stamped_message_file(self, message) -> pathlib.Path:
        return pathlib.Path(self.stamped_message_name(message)).with_suffix('.msg')

    def message_path(self, message) -> pathlib.Path:
        return pathlib.Path('msg') / self.message_file(message)

    def stamped_message_path(self, message) -> pathlib.Path:
        return pathlib.Path('msg') / self.stamped_message_file(message)

    def field_name(self, _message, signal) -> str:
        return to_snake_case(signal.name)

    def stamped_message_field_name(self, message) -> str:
        return to_snake_case(message.name)

    def header_field_name(self, _message) -> str:
        return 'header'

    def id(self, _message) -> str:
        return 'ID'

    def dlc(self, _message) -> str:
        return 'DLC'

    def cycle_time(self, _message) -> str:
        return 'CYCLE_TIME'

    def is_fd(self, _message) -> str:
        return 'IS_FD'

    def scale(self, message, signal) -> str:
        return self.constant(self.field_name(message, signal), 'SCALE')

    def offset(self, message, signal) -> str:
        return self.constant(self.field_name(message, signal), 'OFFSET')

    def maximum(self, message, signal) -> str:
        return self.constant(self.field_name(message, signal), 'MAX')

    def minimum(self, message, signal) -> str:
        return self.constant(self.field_name(message, signal), 'MIN')

    def initial(self, message, signal) -> str:
        return self.constant(self.field_name(message, signal), 'INITIAL')

    def invalid(self, message, signal) -> str:
        return self.constant(self.field_name(message, signal), 'INVALID')

    def choice(self, _message, signal, choice) -> str:
        return self.constant(signal.name, choice.name)
