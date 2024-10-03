import pathlib

from cantools.database.can.c_source import camel_to_snake_case

from rosidl_candb_pycommon import \
    NamingConvention, \
    to_snake_case, \
    KEYWORDS


class BaseNamingConvention(NamingConvention):
    def __init__(
            self,
            package_name: str,
            database_name: str,
    ):
        self._package_name = package_name
        self._database_name = database_name

        self._namespace = ['candb', to_snake_case(self._database_name), 'detail']

    def struct(self, message_name: str) -> str:
        return '_'.join([self._database_name, camel_to_snake_case(message_name), 't'])

    def header_path(self) -> pathlib.Path:
        return pathlib.Path(*self._namespace, to_snake_case(self._database_name)).with_suffix('.h')

    def source_path(self) -> pathlib.Path:
        return pathlib.Path(*self._namespace, to_snake_case(self._database_name)).with_suffix('.c')

    def fuzzer_source_path(self) -> pathlib.Path:
        return pathlib.Path(*self._namespace, f"{to_snake_case(self._database_name)}_fuzzer").with_suffix('.c')

    def fuzzer_makefile_path(self) -> pathlib.Path:
        return pathlib.Path(*self._namespace, f"{to_snake_case(self._database_name)}_fuzzer").with_suffix('.mk')

    def field(self, _message_name: str, signal_name: str) -> str:
        field_name = camel_to_snake_case(signal_name)
        while field_name in KEYWORDS:
            field_name += '_'
        return field_name

    def _func(self, message_name: str, *argv: str) -> str:
        return '_'.join([self._database_name, camel_to_snake_case(message_name), *argv])

    def pack(self, message_name: str) -> str:
        return self._func(message_name, 'pack')

    def unpack(self, message_name: str) -> str:
        return self._func(message_name, 'unpack')
