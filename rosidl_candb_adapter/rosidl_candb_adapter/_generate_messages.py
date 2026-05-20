from typing import TYPE_CHECKING

from . import deduce_message_type

if TYPE_CHECKING:
    from typing import Iterable

import pathlib

import cantools.database
import jinja2

from ._naming_convention import NamingConvention
from ._utils import filter_tuples, filter_messages, signal_constants, format_message_constant


def generate_messages(
        *,
        package_dir: pathlib.Path,
        package_name: str,
        input_file: pathlib.Path,
        output_dir: pathlib.Path,
        template_dir: pathlib.Path,
        node_tuples: 'Iterable[str]' = None,
        message_tuples: 'Iterable[str]' = None,
        strict: bool = False,
):
    assert package_dir.is_absolute()
    assert not input_file.is_absolute()

    abs_input_file = (package_dir / input_file).absolute()
    try:
        db = cantools.database.load_file(
            filename=str(abs_input_file)
        )
    except cantools.database.UnsupportedDatabaseFormatError as e:
        raise RuntimeError(f"Error loading database file '{input_file}'") from e

    node_names = [n.name for n in db.nodes]
    if node_tuples is not None:
        node_names = list(filter_tuples(
            str(package_dir),
            str(input_file),
            allowed=node_names,
            tuples=node_tuples,
        ))

    message_names = [m.name for m in db.messages]
    if message_tuples is not None:
        message_names = list(filter_tuples(
            str(package_dir),
            str(input_file),
            allowed=message_names,
            tuples=message_tuples
        ))
    messages = list(filter_messages(
        messages=db.messages,
        node_names=node_names,
        message_names=message_names,
        strict=strict,
    ))

    naming_convention = NamingConvention(package_name, input_file.stem)

    if not template_dir.exists():
        raise RuntimeError(f"Template directory '{template_dir}' does not exist")

    loader = jinja2.FileSystemLoader(template_dir)
    env = jinja2.Environment(loader=loader)

    message_template = env.get_template('message.j2')
    message_stamped_template = env.get_template('message_stamped.j2')

    for message in messages:
        message_constants = {signal: signal_constants(signal) for signal in message.signals}

        message_file = output_dir / naming_convention.message_path(message)
        message_file = message_file.resolve().absolute()
        message_file.parent.mkdir(exist_ok=True, parents=True)

        message_stream = message_template.stream(
            message=message,
            naming_convention=naming_convention,
            message_constants=message_constants,
            deduce_message_type=deduce_message_type,
            format_message_constant=format_message_constant,
        )
        message_stream.dump(str(message_file))

        yield message.name, message_file.relative_to(output_dir)

        message_stamped_file = output_dir / naming_convention.stamped_message_path(message)
        message_stamped_file = message_stamped_file.resolve().absolute()
        message_stamped_file.parent.mkdir(exist_ok=True, parents=True)

        message_stamped_stream = message_stamped_template.stream(
            message=message,
            naming_convention=naming_convention,
            message_constants=message_constants,
            deduce_message_type=deduce_message_type,
            format_message_constant=format_message_constant,
        )
        message_stamped_stream.dump(str(message_stamped_file))

        yield message.name, message_stamped_file.relative_to(output_dir)
