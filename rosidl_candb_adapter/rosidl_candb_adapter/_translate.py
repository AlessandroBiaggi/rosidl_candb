from typing import Iterable

import pathlib
import cantools.database

from ament_index_python import get_package_share_directory

from rosidl_candb_pycommon import \
    TemplateContext, \
    filter_messages, \
    filter_tuples

from ._idl_naming_convention import IdlNamingConvention


def translate(
        *,
        package_dir: pathlib.Path,
        package_name: str,
        input_file: pathlib.Path,
        output_dir: pathlib.Path,
        template_dir: pathlib.Path,
        node_tuples: Iterable[str] = None,
        message_tuples: Iterable[str] = None,
        strict: bool = False,
) -> Iterable[tuple[str, pathlib.Path, pathlib.Path, dict[str, str]]]:
    assert package_dir.is_absolute()
    assert not input_file.is_absolute()

    try:
        abs_input_file = (package_dir / input_file).absolute()
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

    if template_dir is None:
        share_dir = get_package_share_directory('rosidl_candb_adapter')
        share_dir = pathlib.Path(share_dir)
        template_dir = share_dir / 'resource'
        assert template_dir.exists(), f"Template directory '{template_dir}' does not exist"
    elif not template_dir.exists():
        raise RuntimeError(f"Template directory '{template_dir}' does not exist")

    messages = filter_messages(
        messages=db.messages,
        node_names=node_names,
        message_names=message_names,
        strict=strict,
    )

    database_name = input_file.stem
    naming_convention = IdlNamingConvention(
        package_name=package_name,
        database_name=database_name
    )

    template_ctx = TemplateContext(
        resolve_paths=[template_dir],
        globals={
            'package_name': package_name,
            'relative_input_file': input_file,
            'database_name': database_name,
            'node_names': node_names,
            'naming_convention': naming_convention,
        },
    )
    output_names_and_files = []

    for message in messages:
        output_file = output_dir / naming_convention.idl_path(message.name)
        output_file = output_file.resolve().absolute()

        stamped_output_file = output_dir / naming_convention.stamped_idl_path(message.name)
        stamped_output_file = stamped_output_file.resolve().absolute()

        try:
            template_ctx.expand_template(
                template_name='msg.idl.em',
                output_file=output_file,
                locals={'message': message},
            )

            template_ctx.expand_template(
                template_name='msg_stamped.idl.em',
                output_file=stamped_output_file,
                locals={'message': message},
            )
        except Exception as e:
            raise RuntimeError(f"Error processing message {message.name}") from e

        output_names_and_files.append((message.name,
                                       output_file,
                                       stamped_output_file,
                                       {s.name: naming_convention.field(message.name, s.name)
                                        for s in message.signals}))

    return output_names_and_files
