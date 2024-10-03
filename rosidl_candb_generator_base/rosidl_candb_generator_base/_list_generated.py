from typing import List

import pathlib

from ._base_naming_convention import BaseNamingConvention


def list_generated(
        package_dir: pathlib.Path,
        package_name: str,
        input_file: pathlib.Path,
        output_dir: pathlib.Path,
) -> List[pathlib.Path]:
    abs_input_file = (package_dir / input_file).resolve().absolute()
    if not abs_input_file.is_file():
        raise RuntimeError(f"Database file '{input_file}' does not exist")

    database_name = input_file.stem
    naming_convention = BaseNamingConvention(
        package_name=package_name,
        database_name=database_name,
    )

    generated_files = [
        output_dir / naming_convention.header_path(),
        output_dir / naming_convention.source_path(),
    ]

    generated_files = map(pathlib.Path.resolve, generated_files)
    generated_files = map(pathlib.Path.absolute, generated_files)

    return generated_files
