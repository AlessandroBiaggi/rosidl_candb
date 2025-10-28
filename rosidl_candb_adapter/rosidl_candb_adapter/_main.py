from typing import List

import argparse
import json
import os
import pathlib
import sys

from ._translate import translate


def main(argv: List[str] = sys.argv[1:]) -> int:
    parser = argparse.ArgumentParser(
        description="Convert Can Database files to .idl",
    )

    parser.add_argument(
        '--package-name', type=str, default=None,
        help='The name of the package',
    )
    parser.add_argument(
        '--arguments-file', type=pathlib.Path, required=True,
        help='The JSON file containing the non-idl tuples to convert to .idl',
    )
    parser.add_argument(
        '--output-dir', type=pathlib.Path, default=None,
        help='The base directory to create .idl files in',
    )
    parser.add_argument(
        '--template-dir', type=pathlib.Path, default=None,
        help='The directory containing the templates',
    )
    parser.add_argument(
        '--idl-output-file', type=pathlib.Path, required=True,
        help='The output file containing the tuples for the generated .idl files'
    )
    parser.add_argument(
        '--pkt-output-file', type=pathlib.Path, required=True,
        help='The output file containing the tuples for the generated .idl files'
    )
    parser.add_argument(
        '--sig-output-file', type=pathlib.Path, required=True,
        help='The output file containint the tuples for the generated .idl files'
    )

    args = parser.parse_args(argv)
    if not (args.arguments_file.exists() and args.arguments_file.is_file()):
        print(
            f"Arguments file {args.arguments_file} does not exist or is not a file",
            file=sys.stderr,
        )
        return -1

    with open(str(args.arguments_file), 'r') as h:
        arguments = json.load(h)

    if args.package_name:
        arguments['package_name'] = args.package_name
    elif 'package_name' not in arguments:
        print(
            f"Package name is required",
            file=sys.stderr,
        )
        return -1

    if args.output_dir:
        arguments['output_dir'] = args.output_dir
    elif 'output_dir' in arguments:
        arguments['output_dir'] = pathlib.Path(arguments['output_dir'])
    else:
        print(
            f"Output directory is required",
            file=sys.stderr,
        )
        return -1

    if args.template_dir:
        arguments['template_dir'] = args.template_dir
    elif 'template_dir' in arguments:
        arguments['template_dir'] = pathlib.Path(arguments['template_dir'])

    if 'interface_tuples' not in arguments:
        print(
            f"Arguments file {args.arguments_file} is not valid",
            file=sys.stderr,
        )
        return -1

    idl_tuples = []

    for interface_tuple in arguments['interface_tuples']:
        base_path, relative_path = map(pathlib.Path, interface_tuple.rsplit(':', 1))

        try:
            names_and_idl_files_and_signals = translate(
                package_dir=base_path,
                package_name=arguments['package_name'],
                input_file=relative_path,
                output_dir=arguments['output_dir'],
                template_dir=arguments.get('template_dir', None),
                node_tuples=arguments.get('node_tuples', None),
                message_tuples=arguments.get('message_tuples', None),
                strict=arguments.get('strict', False),
            )
            idl_tuples.extend([
                (relative_path,
                 message_name,
                 *map(lambda f: f.relative_to(args.output_dir), abs_idl_files),
                 signal_field_name_mapping)
                for message_name, *abs_idl_files, signal_field_name_mapping in names_and_idl_files_and_signals
            ])
        except Exception as e:
            raise RuntimeError(f"Could not translate {interface_tuple}") from e

    try:
        args.idl_output_file.parent.mkdir(parents=True, exist_ok=True)
        args.pkt_output_file.parent.mkdir(parents=True, exist_ok=True)
        args.sig_output_file.parent.mkdir(parents=True, exist_ok=True)

        with (
            args.idl_output_file.open('w') as f,
            args.pkt_output_file.open('w') as g,
            args.sig_output_file.open('w') as h,
        ):
            for relative_path, message_name, interface_relpath, stamped_interface_relpath, signal_field_mapping in idl_tuples:
                f.write(f"{args.output_dir}:{interface_relpath}\n".replace(os.sep, '/'))
                f.write(f"{args.output_dir}:{stamped_interface_relpath}\n".replace(os.sep, '/'))
                g.write(f"{relative_path}:{message_name}:{interface_relpath}:{stamped_interface_relpath}\n".replace(os.sep, '/'))

                for signal_name, field_name in signal_field_mapping.items():
                    h.write(f"{relative_path}:{message_name}:{signal_name}:{interface_relpath}:{field_name}\n".replace(os.sep, '/'))

    except Exception as e:
        raise RuntimeError(f"Could not write output file") from e

    return 0
