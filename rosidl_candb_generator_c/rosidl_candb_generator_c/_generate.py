from typing import Iterable

import pathlib
import cantools.database

from ament_index_python import get_package_share_directory

from rosidl_candb_pycommon import \
    TemplateContext, \
    filter_messages, \
    filter_tuples

from ._c_naming_convention import CNamingConvention


def generate(
        *,
        package_dir: pathlib.Path,
        package_name: str,
        input_file: pathlib.Path,
        output_dir: pathlib.Path,
        template_dir: pathlib.Path = None,
        node_tuples: Iterable[str] = None,
        message_tuples: Iterable[str] = None,
        strict: bool = False,
) -> Iterable[pathlib.Path]:
    assert package_dir.is_absolute()
    assert not input_file.is_absolute()

    try:
        abs_input_file = (package_dir / input_file).absolute()
        db = cantools.database.load_file(
            filename=str(abs_input_file)
        )
    except cantools.database.UnsupportedDatabaseFormatError as e:
        raise RuntimeError(f"Error loading database file '{input_file}'") from e

    if template_dir is None:
        share_dir = get_package_share_directory('rosidl_candb_generator_c')
        share_dir = pathlib.Path(share_dir)
        template_dir = share_dir / 'resource'
        assert template_dir.is_dir()
    elif not template_dir.is_dir():
        raise RuntimeError(f"Template directory '{template_dir}' does not exist")

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
    naming_convention = CNamingConvention(
        package_name=package_name,
        database_name=database_name,
    )

    template_ctx = TemplateContext(
        resolve_paths=[template_dir],
        globals={
            'package_name': package_name,
            'relative_input_file': input_file,
            'database_name': database_name,
            'node_names': node_names,
            'messages': messages,
            'naming_convention': naming_convention,
        },
    )

    output_files = []

    for message in messages:
        header_output_file = (output_dir / naming_convention.header_path(message.name)).resolve().absolute()

        try:
            template_ctx.expand_template(
                template_name='msg.h.em',
                output_file=header_output_file,
                locals={'message': message},
            )
        except Exception as e:
            raise RuntimeError(f"Error generating header file '{header_output_file}'") from e

        output_files.append(header_output_file)

        pack_output_file = (output_dir / naming_convention.pack_source_path(message.name)).resolve().absolute()

        try:
            template_ctx.expand_template(
                template_name='msg__pack.c.em',
                output_file=pack_output_file,
                locals={'message': message},
            )
        except Exception as e:
            raise RuntimeError(f"Error generating pack source file '{pack_output_file}'") from e

        output_files.append(pack_output_file)

        unpack_output_file = (output_dir / naming_convention.unpack_source_path(message.name)).resolve().absolute()

        try:
            template_ctx.expand_template(
                template_name='msg__unpack.c.em',
                output_file=unpack_output_file,
                locals={'message': message},
            )
        except Exception as e:
            raise RuntimeError(f"Error generating unpack source file '{unpack_output_file}'") from e

        output_files.append(unpack_output_file)

    return output_files
