import pathlib

from rosidl_candb_pycommon import \
    NamingConvention, \
    to_pascal_case, \
    to_snake_case, \
    KEYWORDS


class IdlNamingConvention(NamingConvention):
    def __init__(self, package_name: str, database_name: str):
        self._package_name = package_name
        self._database_name = database_name

    @property
    def package_name(self) -> str:
        return self._package_name

    @property
    def database_name(self) -> str:
        return self._database_name

    def idl_name(self, message_name: str) -> str:
        return self.struct(message_name)

    def idl_path(self, message_name: str) -> pathlib.Path:
        return pathlib.Path('msg', self.idl_name(message_name)).with_suffix('.idl')

    def stamped_idl_path(self, message_name: str) -> pathlib.Path:
        return pathlib.Path('msg', self.stamped_struct(message_name)).with_suffix('.idl')

    def struct(self, message_name: str, *argv: str) -> str:
        struct_name = ''.join(map(to_pascal_case, [
            self._database_name,
            message_name,
            *argv,
        ]))
        while struct_name in KEYWORDS:
            struct_name += '_'
        return struct_name

    def stamped_struct(self, message_name: str) -> str:
        return self.struct(message_name, 'stamped')

    def field(self, _message_name: str, signal_name: str) -> str:
        field_name = to_snake_case(signal_name)
        while field_name in KEYWORDS:
            field_name += '_'
        return field_name

    def id(self, _message_name: str) -> str:
        return 'ID'

    def length(self, _message_name: str) -> str:
        return 'LENGTH'

    def cycle_time(self, _message_name: str) -> str:
        return 'CYCLE_DURATION_MS'

    def is_fd(self, _message_name: str) -> str:
        return 'IS_FD'

    def scale(self, _message_name: str, signal_name: str) -> str:
        return f"{to_snake_case(signal_name).upper()}_SCALE"

    def offset(self, _message_name: str, signal_name: str) -> str:
        return f"{to_snake_case(signal_name).upper()}_OFFSET"

    def stamped_length(self, message_name: str) -> str:
        return f"_{self.struct_field_name(message_name)}_type::{self.length()}"

    def choice(
            self,
            message_name: str,
            signal_name: str,
            choice_name: str,
            index: int or str = None
    ) -> str:
        return NamingConvention.constant(
            to_snake_case(message_name).upper(),
            to_snake_case(signal_name).upper(),
            'CHOICE',
            to_snake_case(choice_name).upper(),
            str(index) if index is not None else None,
        )

    def initial(self, _message_name: str, signal_name: str) -> str:
        return NamingConvention.constant(to_snake_case(signal_name).upper(), 'INITIAL')

    def invalid(self, _message_name: str, signal_name: str) -> str:
        return NamingConvention.constant(to_snake_case(signal_name).upper(), 'INVALID')

    def header_field_name(self, _message_name: str) -> str:
        return 'header'

    def struct_field_name(self, message_name: str) -> str:
        return to_snake_case(message_name).lower()
