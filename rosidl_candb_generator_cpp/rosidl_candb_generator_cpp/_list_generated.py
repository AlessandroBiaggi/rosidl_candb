from typing import Iterable

import pathlib
import cantools.database

from rosidl_candb_pycommon import \
    filter_messages, \
    filter_tuples

from ._cpp_naming_convention import CppNamingConvention

def list_generated(
        *,
        package_dir: pathlib.Path,
        package_name: str,
        input_file: pathlib.Path,
        output_dir: pathlib.Path,
        node_tuples: Iterable[str] = None,
        message_tuples: Iterable[str] = None,
        strict: bool = False
) -> Iterable[pathlib.Path]:
    abs_input_file = (package_dir / input_file).resolve().absolute()
    if not abs_input_file.is_file():
        raise RuntimeError(f"Database file '{input_file}' does not exist")

    try:
        db = cantools.database.load_file(
            filename=str(abs_input_file)
        )
    except cantools.database.UnsupportedDatabaseFormatError as e:
        raise RuntimeError(f"Error loading database file '{input_file}'") from e

    node_names = [n.name for n in db.nodes]
    if node_tuples is not None:
        node_names = filter_tuples(
            str(package_dir),
            str(input_file),
            allowed=node_names,
            tuples=node_tuples
        )

    message_names = None
    if message_tuples is not None:
        message_names = filter_tuples(
            str(package_dir),
            str(input_file),
            allowed=[m.name for m in db.messages],
            tuples=message_tuples
        )

    messages = filter_messages(
        messages=db.messages,
        node_names=node_names,
        message_names=message_names,
        strict=strict,
    )

    database_name = input_file.stem
    naming_convention = CppNamingConvention(
        package_name=package_name,
        database_name=database_name,
    )

    generated_files = [
        output_dir / naming_convention.unpack_header_path(),
        output_dir / naming_convention.pack_header_path(),
        *map(lambda m: output_dir / naming_convention.message_pack_header_path(m.name), messages),
        *map(lambda m: output_dir / naming_convention.message_unpack_header_path(m.name), messages),
    ]

    generated_files = map(pathlib.Path.resolve, generated_files)
    generated_files = map(pathlib.Path.absolute, generated_files)

    return generated_files
