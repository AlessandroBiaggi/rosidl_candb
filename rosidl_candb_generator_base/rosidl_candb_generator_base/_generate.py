from typing import List

import pathlib
import cantools.database

from ._base_naming_convention import BaseNamingConvention


def generate(
        package_dir: pathlib.Path,
        package_name: str,
        input_file: pathlib.Path,
        output_dir: pathlib.Path,
) -> List[pathlib.Path]:
    assert package_dir.is_absolute()
    assert not input_file.is_absolute()

    abs_input_file = (package_dir / input_file).resolve().absolute()
    if not abs_input_file.is_file():
        raise RuntimeError(f"Database file '{input_file}' does not exist")

    try:
        db = cantools.database.load_file(
            filename=str(abs_input_file)
        )
    except cantools.database.UnsupportedDatabaseFormatError as e:
        raise RuntimeError(f"Error loading database file '{input_file}'") from e

    database_name = input_file.stem
    naming_convention = BaseNamingConvention(
        package_name=package_name,
        database_name=database_name,
    )

    for msg in db.messages:
        for signal in msg.signals:
            signal.name = naming_convention.field(msg.name, signal.name)
    db.refresh()

    header_path = output_dir / naming_convention.header_path()
    source_path = output_dir / naming_convention.source_path()
    fuzzer_source_path = output_dir / naming_convention.fuzzer_source_path()

    header, source, _, _ = \
        cantools.database.can.c_source.generate(
            database=db,
            database_name=database_name,
            header_name=header_path.name,
            source_name=source_path.name,
            fuzzer_source_name=fuzzer_source_path.name,
        )

    header_path.parent.mkdir(parents=True, exist_ok=True)
    with header_path.open('w') as h:
        h.write(header)

    source_path.parent.mkdir(parents=True, exist_ok=True)
    with source_path.open('w') as h:
        h.write(source)

    return [header_path, source_path]
