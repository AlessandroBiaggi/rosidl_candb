from typing import List

from abc import ABC, abstractmethod

import pathlib

from rosidl_cli.command.helpers import interface_path_as_tuple
from rosidl_cli.command.translate.extensions import TranslateCommandExtension

from .._translate import translate as translate_candb_to_idl


class _TranslateCanDB2Idl(ABC, TranslateCommandExtension):
    output_format = 'idl'

    @property
    @abstractmethod
    def input_format(self) -> str:
        pass

    def translate(
            self,
            package_name: str,
            interface_files: List[pathlib.Path],
            _include_paths: List[pathlib.Path],
            output_path: pathlib.Path,
    ) -> List[pathlib.Path]:
        translated_interface_files = []

        for interface_file in interface_files:
            prefix, interface_file = interface_path_as_tuple(interface_file)
            output_dir = output_path / interface_file.parent

            output_files = translate_candb_to_idl(
                package_dir=prefix,
                package_name=package_name,
                input_file=interface_file,
                output_dir=output_dir,
            )

            for output_file in output_files:
                output_file = output_file.relative_to(output_path)
                translated_interface_files.append(
                    f'{output_path}:{output_file.as_posix()}'
                )

        return translated_interface_files


class TranslateArxmlDB2Idl(_TranslateCanDB2Idl):
    @property
    def input_format(self) -> str:
        return 'arxml'


class TranslateDbcDB2Idl(_TranslateCanDB2Idl):
    @property
    def input_format(self) -> str:
        return 'dbc'


class TranslateKcdDB2Idl(_TranslateCanDB2Idl):
    @property
    def input_format(self) -> str:
        return 'kcd'


class TranslateSymDB2Idl(_TranslateCanDB2Idl):
    @property
    def input_format(self) -> str:
        return 'sym'


class TranslateCddDB2Idl(_TranslateCanDB2Idl):
    @property
    def input_format(self) -> str:
        return 'cdd'
