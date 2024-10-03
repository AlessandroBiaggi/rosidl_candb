import re
import pathlib

from rosidl_candb_pycommon import \
    NamingConvention, \
    to_snake_case, \
    to_pascal_case

from rosidl_candb_adapter import IdlNamingConvention
from rosidl_candb_generator_base import BaseNamingConvention


class CNamingConvention(NamingConvention):
    def __init__(
            self,
            package_name: str,
            database_name: str
    ):
        self._package_name = package_name
        self._database_name = database_name

        self._idl_naming_convention = IdlNamingConvention(package_name, database_name)
        self._base_naming_convention = BaseNamingConvention(package_name, database_name)

        self._path = 'candb', to_snake_case(database_name)

    def struct(self, message_name: str) -> str:
        return '__'.join([
            self._package_name,
            'msg',
            self._idl_naming_convention.struct(message_name)
        ])

    def header_path(self, message_name: str) -> pathlib.Path:
        return pathlib.Path(*self._path, to_snake_case(message_name)).with_suffix('.h')

    def pack_source_path(self, message_name: str) -> pathlib.Path:
        return pathlib.Path(*self._path, f"{to_snake_case(message_name)}__pack").with_suffix('.c')

    def unpack_source_path(self, message_name: str) -> pathlib.Path:
        return pathlib.Path(*self._path, f"{to_snake_case(message_name)}__unpack").with_suffix('.c')

    def struct_header_path(self, message_name: str) -> pathlib.Path:
        message_name = self._idl_naming_convention.struct(message_name)

        # See rosidl_cmake/cmake/string_camel_case_to_lower_case_underscore.cmake
        message_name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', message_name)
        message_name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', message_name)

        return pathlib.Path('msg', message_name.lower()).with_suffix('.h')

    def visibility_control_header(self) -> str:
        return pathlib.Path('rosidl_candb_generator_c__visibility_control').with_suffix('.h')

    def base_header_path(self) -> pathlib.Path:
        return self._base_naming_convention.header_path()

    def field(self, message_name: str, signal_name: str) -> str:
        return self._idl_naming_convention.field(message_name, signal_name)

    def _macro(self, message_name: str, *argv: str) -> str:
        return '__'.join([
            self._package_name,
            *self._path,
            to_snake_case(message_name),
            *argv,
        ]).upper()

    def header_guard(self, message_name: str) -> pathlib.Path:
        return self._macro(message_name, 'H')

    def visibility_control_public(self) -> str:
        return f"rosidl_candb_generator_c_PUBLIC_{self._package_name}"

    def visibility_control_export(self) -> str:
        return f"rosidl_candb_generator_c_EXPORT_{self._package_name}"

    def visibility_control_import(self) -> str:
        return f"rosidl_candb_generator_c_IMPORT_{self._package_name}"

    def _const(self, message_name: str, *argv: str) -> str:
        return '__'.join([
            self._package_name, 'msg',
            self._idl_naming_convention.struct(message_name),
            *argv,
        ])

    def id(self, struct_name: str) -> str:
        return self._const(struct_name, self._idl_naming_convention.id(struct_name))

    def length(self, struct_name: str) -> str:
        return self._const(struct_name, self._idl_naming_convention.length(struct_name))

    def is_fd(self, struct_name: str) -> str:
        return self._const(struct_name, self._idl_naming_convention.is_fd(struct_name))

    def cycle_time(self, struct_name: str) -> str:
        return self._const(struct_name, self._idl_naming_convention.cycle_time(struct_name))

    def scale(self, struct_name: str, signal_name: str) -> str:
        return self._assoc(struct_name, self._idl_naming_convention.scale(struct_name, signal_name))

    def offset(self, struct_name: str, signal_name: str) -> str:
        return self._assoc(struct_name, self._idl_naming_convention.offset(struct_name, signal_name))

    def _func(self, message_name: str, *argv: str) -> str:
        return '__'.join([
            self._package_name,
            *self._path,
            to_snake_case(message_name),
            *argv,
        ])

    def pack(self, message_name: str) -> str:
        return self._func(message_name, 'pack')

    def unpack(self, message_name: str) -> str:
        return self._func(message_name, 'unpack')

    def base_struct(self, message_name: str) -> str:
        return self._base_naming_convention.struct(message_name)

    def base_field(self, message_name: str, signal_name: str) -> str:
        return self._base_naming_convention.field(message_name, signal_name)

    def base_pack(self, message_name: str) -> str:
        return self._base_naming_convention.pack(message_name)

    def base_unpack(self, message_name: str) -> str:
        return self._base_naming_convention.unpack(message_name)
