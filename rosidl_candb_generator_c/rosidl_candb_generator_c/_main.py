from typing import List

import argparse
import json
import pathlib
import sys

from ._generate import generate
from ._list_generated import list_generated


def main(argv: List[str] = sys.argv[1:]) -> int:
    parser = argparse.ArgumentParser(
        description="Generate C code from Can Database files",
    )

    parser.add_argument(
        '--generator-arguments-file', type=pathlib.Path, required=True,
        help='The location of the file containing the generator arguments',
    )
    parser.add_argument(
        '--package-name', type=str, default=None,
        help='The name of the package',
    )
    parser.add_argument(
        '--output-dir', type=pathlib.Path, default=None,
        help='The directory to output the generated files',
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    generate_parser = subparsers.add_parser('generate', help='Generate C code from Can Database files')
    _ = subparsers.add_parser('list', help='List generated files')

    generate_parser.add_argument(
        '--template-dir', type=pathlib.Path, required=False,
        help='The directory containing the templates to use',
    )

    args = parser.parse_args(argv)

    if not (args.generator_arguments_file.exists() and args.generator_arguments_file.is_file()):
        raise RuntimeError(f"Generator arguments file {args.generator_arguments_file} does not exist or is not a file")

    with open(str(args.generator_arguments_file), 'r') as h:
        arguments = json.load(h)

    if 'interface_tuples' not in arguments:
        print(
            f"Generator arguments file {args.generator_arguments_file} is not valid",
            file=sys.stderr,
        )
        return -1

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

    match args.command:
        case 'generate':
            return generate_main(args, arguments)
        case 'list':
            return list_main(args, arguments)
        case _:
            print(f"Unknown command {args.command}", file=sys.stderr)
            return -1


def generate_main(args: argparse.Namespace, arguments: dict) -> int:
    if args.template_dir:
        arguments['template_dir'] = args.template_dir
    elif 'template_dir' in arguments:
        arguments['template_dir'] = pathlib.Path(arguments['template_dir'])

    for interface_tuple in arguments['interface_tuples']:
        base_path, relative_path = interface_tuple.rsplit(':', 1)

        try:
            generated_files = generate(
                package_dir=pathlib.Path(base_path),
                package_name=arguments['package_name'],
                input_file=pathlib.Path(relative_path),
                output_dir=arguments['output_dir'],
                template_dir=arguments.get('template_dir', None),
                node_tuples=arguments.get('node_tuples', None),
                message_tuples=arguments.get('message_tuples', None),
                strict=arguments.get('strict', False),
            )

            assert all([f.is_file() for f in generated_files]), \
                f"Error generating C code for {interface_tuple}: not all files were generated " \
                f"({', '.join([f for f in generated_files if not f.is_file()])})"
        except Exception as e:
            print(f"Error generating C code for {interface_tuple}: {e}", file=sys.stderr)
            return -1

    return 0


def list_main(_: argparse.Namespace, arguments: dict) -> int:
    generated_files = []

    for interface_tuple in arguments['interface_tuples']:
        base_path, relative_path = interface_tuple.rsplit(':', 1)

        try:
            generated_files.extend(
                list_generated(
                    package_dir=pathlib.Path(base_path),
                    package_name=arguments['package_name'],
                    input_file=pathlib.Path(relative_path),
                    output_dir=arguments['output_dir'],
                    node_tuples=arguments.get('node_tuples', None),
                    message_tuples=arguments.get('message_tuples', None),
                    strict=arguments.get('strict', False),
                )
            )
        except Exception as e:
            print(f"Error listing generated C files for {interface_tuple}: {e}", file=sys.stderr)
            return -1

    generated_files = sorted(generated_files)
    generated_files = map(str, generated_files)
    print(' '.join(generated_files))
