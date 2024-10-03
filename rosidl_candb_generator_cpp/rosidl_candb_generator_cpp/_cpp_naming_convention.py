import re
import pathlib

from rosidl_candb_pycommon import \
    NamingConvention, \
    to_snake_case

from rosidl_candb_adapter import IdlNamingConvention
from rosidl_candb_generator_base import BaseNamingConvention


class CppNamingConvention(NamingConvention):
    def __init__(
            self,
            package_name: str,
            database_name: str
    ):
        self._package_name = package_name
        self._database_name = database_name

        self._idl_naming_convention = IdlNamingConvention(package_name, database_name)
        self._base_naming_convention = BaseNamingConvention(package_name, database_name)

        self._namespace = 'candb', to_snake_case(database_name)

    def namespace(self) -> str:
        return '::'.join(self._namespace)

    def struct(self, message_name: str) -> str:
        return '::'.join(['msg', self._idl_naming_convention.struct(message_name)])

    def stamped_struct(self, message_name: str) -> str:
        return '::'.join(['msg', self._idl_naming_convention.stamped_struct(message_name)])

    def pack_header_path(self) -> pathlib.Path:
        return pathlib.Path(*self._namespace, 'pack').with_suffix('.hpp')

    def unpack_header_path(self) -> pathlib.Path:
        return pathlib.Path(*self._namespace, 'unpack').with_suffix('.hpp')

    def message_pack_header_path(self, message_name: str) -> pathlib.Path:
        return pathlib.Path(*self._namespace, 'detail', f"{to_snake_case(message_name)}__pack").with_suffix('.hpp')

    def message_unpack_header_path(self, message_name: str) -> pathlib.Path:
        return pathlib.Path(*self._namespace, 'detail', f"{to_snake_case(message_name)}__unpack").with_suffix('.hpp')

    def struct_header_path(self, message_name: str) -> pathlib.Path:
        struct_name = self._idl_naming_convention.struct(message_name)
        return self._struct_header_path(struct_name)

    def stamped_struct_header_path(self, message_name: str) -> pathlib.Path:
        struct_name = self._idl_naming_convention.stamped_struct(message_name)
        return self._struct_header_path(struct_name)

    def _struct_header_path(self, struct_name: str) -> pathlib.Path:
        # See rosidl_cmake/cmake/string_camel_case_to_lower_case_underscore.cmake
        struct_name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', struct_name)
        struct_name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', struct_name)
        struct_name = struct_name.lower()

        return pathlib.Path('msg', struct_name).with_suffix('.hpp')

    def visibility_control_header(self) -> pathlib.Path:
        return pathlib.Path('rosidl_candb_generator_cpp__visibility_control').with_suffix('.hpp')

    def base_header_path(self) -> pathlib.Path:
        return self._base_naming_convention.header_path()

    def header_field_name(self, message_name: str) -> str:
        return self._idl_naming_convention.header_field_name(message_name)

    def struct_field_name(self, message_name: str) -> str:
        return self._idl_naming_convention.struct_field_name(message_name)

    def field(self, message_name: str, signal_name: str) -> str:
        return self._idl_naming_convention.field(message_name, signal_name)

    def _macro(self, *argv: str) -> str:
        return '__'.join([
            self._package_name,
            *self._namespace,
            *argv,
        ]).upper()

    def header_guard(self, *argv: str) -> pathlib.Path:
        return self._macro(*map(to_snake_case, argv), 'HPP')

    def visibility_control_public(self) -> str:
        return f"rosidl_candb_generator_cpp_PUBLIC_{self._package_name}"

    def visibility_control_export(self) -> str:
        return f"rosidl_candb_generator_cpp_EXPORT_{self._package_name}"

    def visibility_control_import(self) -> str:
        return f"rosidl_candb_generator_cpp_IMPORT_{self._package_name}"

    def _assoc(self, struct_name: str, *argv: str) -> str:
        return '::'.join([struct_name, *argv])

    def id(self, message_name: str) -> str:
        return self._assoc(message_name, self._idl_naming_convention.id(message_name))

    def length(self, struct_name: str) -> str:
        return self._assoc(struct_name, self._idl_naming_convention.length(struct_name))

    def cycle_time(self, struct_name: str) -> str:
        return self._assoc(struct_name, self._idl_naming_convention.cycle_time(struct_name))

    def is_fd(self, message_name: str) -> str:
        return self._assoc(message_name, self._idl_naming_convention.is_fd(message_name))

    def scale(self, struct_name: str, signal_name: str) -> str:
        return self._assoc(struct_name, self._idl_naming_convention.scale(struct_name, signal_name))

    def offset(self, struct_name: str, signal_name: str) -> str:
        return self._assoc(struct_name, self._idl_naming_convention.offset(struct_name, signal_name))

    def _func(self, *argv: str) -> str:
        return '::'.join([
            *self._namespace,
            *argv,
        ])

    def pack_decl(self) -> str:
        return 'pack'

    def pack_impl(self) -> str:
        return self._func(self.pack_decl())

    def unpack_decl(self) -> str:
        return 'unpack'

    def unpack_impl(self) -> str:
        return self._func(self.unpack_decl())

    def base_struct(self, message_name: str) -> str:
        return self._base_naming_convention.struct(message_name)

    def base_field(self, message_name: str, signal_name: str) -> str:
        return self._base_naming_convention.field(message_name, signal_name)

    def base_pack(self, message_name: str) -> str:
        return self._base_naming_convention.pack(message_name)

    def base_unpack(self, message_name: str) -> str:
        return self._base_naming_convention.unpack(message_name)
