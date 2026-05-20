import argparse
import json
import os
import pathlib

from ament_index_python import get_package_share_directory

from ._generate_messages import generate_messages


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Convert Can Database files to .msg",
    )

    parser.add_argument(
        '--package-name', type=str, default=None,
        help='The name of the package',
    )
    parser.add_argument(
        '--arguments-file', type=pathlib.Path, required=True,
        help='The JSON file containing the candb tuples to convert to .msg',
    )
    parser.add_argument(
        '--output-dir', type=pathlib.Path, default=None,
        help='The base directory to create .msg files in',
    )
    parser.add_argument(
        '--template-dir', type=pathlib.Path, default=None,
        help='The directory containing the templates',
    )
    parser.add_argument(
        '--msg-output-file', type=pathlib.Path, required=True,
        help='The output file containing the tuples for the generated .msg files'
    )

    args = parser.parse_args(args)

    with open(str(args.arguments_file), 'r') as h:
        arguments = json.load(h)

    if args.package_name:
        arguments['package_name'] = args.package_name
    elif 'package_name' not in arguments:
        raise ValueError("Package name required")

    if args.output_dir:
        arguments['output_dir'] = args.output_dir
    elif 'output_dir' in arguments:
        arguments['output_dir'] = pathlib.Path(arguments['output_dir'])
    else:
        raise ValueError("Output directory required")

    if args.template_dir:
        arguments['template_dir'] = args.template_dir
    elif 'template_dir' in arguments:
        arguments['template_dir'] = pathlib.Path(arguments['template_dir'])
    else:
        share_dir = get_package_share_directory('rosidl_candb_adapter')
        share_dir = pathlib.Path(share_dir)
        arguments['template_dir'] = share_dir / 'resource'

    if 'interface_tuples' not in arguments:
        raise ValueError(f"Arguments file {args.arguments_file} is missing 'interface_tuples' field", )

    try:
        args.msg_output_file.parent.mkdir(parents=True, exist_ok=True)
        with args.msg_output_file.open('w') as f:
            for interface_tuple in arguments['interface_tuples']:
                base_path, relative_path = map(pathlib.Path, interface_tuple.rsplit(':', 1))
                message_names_and_files = generate_messages(
                    package_dir=base_path,
                    package_name=arguments['package_name'],
                    input_file=relative_path,
                    output_dir=arguments['output_dir'],
                    template_dir=arguments['template_dir'],
                    node_tuples=arguments.get('node_tuples', None),
                    message_tuples=arguments.get('message_tuples', None),
                    strict=arguments.get('strict', False),
                )

                for message_name, message_file in message_names_and_files:
                    f.write(f"{base_path}:{relative_path}:{message_name}:"
                            f"{args.output_dir}:{message_file}\n"
                            .replace(os.sep, '/'))
    except Exception as e:
        raise RuntimeError(f"Could not translate {interface_tuple}") from e
