from dlang.uilang import get_sys_lang_code
from dlang.resource import RESOURCES_PATH
from os.path import isdir, isfile
from dlang.parser import parse
from typing import Sequence
from warnings import warn
from os import listdir


FILE_EXTENSION = 'dlang'
TRANSLATION_PRESET_PATH = RESOURCES_PATH + 'lang/'

_active_translator = None


class Translator:
    def __init__(
            self,
            path_or_paths: str | Sequence[str],
            current_lang=...,
            failure_lang='en',
            use_translation_preset=True
    ):
        global _active_translator
        _active_translator = self

        if isinstance(path_or_paths, str):
            self._paths = path_or_paths,
        else:
            self._paths = *path_or_paths,

        self._all_translation_data = {}
        self._use_translation_preset = use_translation_preset
        self._current_lang = self._failure_lang = ''

        self.load_translation()

        if current_lang is ...:
            current_lang = get_sys_lang_code()[:2]

        self.current_lang = current_lang
        self.failure_lang = failure_lang

    @property
    def path_or_paths(self):
        return self._paths

    @path_or_paths.setter
    def path_or_paths(self, new_value: str | Sequence[str]):
        old_value = self._paths

        if isinstance(new_value, str):
            self._paths = new_value,
        else:
            self._paths = *new_value,

        if self._paths != old_value:
            self.load_translation()

    @property
    def current_lang(self):
        return self._current_lang

    @current_lang.setter
    def current_lang(self, new_value: str):
        old_value = self._current_lang
        self._current_lang = new_value

        if new_value == old_value:
            return

        if new_value not in self._all_translation_data:
            self._current_translation_data = {}
            return

        self._current_translation_data = self._all_translation_data[new_value]

    @property
    def failure_lang(self):
        return self._failure_lang

    @failure_lang.setter
    def failure_lang(self, new_value: str):
        old_value = self._failure_lang
        self._failure_lang = new_value

        if new_value == old_value:
            return

        if new_value not in self._all_translation_data:
            self._failure_translation_data = {}
            return

        self._failure_translation_data = self._all_translation_data[new_value]

    @property
    def use_dlang_preset(self):
        return self._use_translation_preset

    @use_dlang_preset.setter
    def use_dlang_preset(self, new_value: bool):
        old_value = self._use_translation_preset
        self._use_translation_preset = new_value

        if old_value != new_value:
            self.load_translation()

    @property
    def current_translation_data(self):
        return {} if self._current_lang not in self._all_translation_data else self._all_translation_data[
            self._current_lang
        ].copy()

    def load_translation(self):
        self._all_translation_data = {}
        paths = self._paths if not self._use_translation_preset else (TRANSLATION_PRESET_PATH, *self._paths)

        for path in paths:
            if not isdir(path):
                warn(f"DLANG -> '{path}' is not a dir")
                continue

            for file_path in listdir(path):
                file_path = path + '/' + file_path

                if not (isfile(file_path) and file_path.endswith(f'.{FILE_EXTENSION}')):
                    continue

                with open(file_path, 'r', encoding='utf-8') as file:
                    lang_key = file_path.replace('\\', '/').split('/')[-1].split('.')[-2]

                    if lang_key not in self._all_translation_data:
                        self._all_translation_data[lang_key] = {}

                    self._all_translation_data[lang_key].update(parse(file.read()))

    def get_translation(self, key: str, *args):
        if key not in self._current_translation_data:
            if key not in self._failure_translation_data:
                return key

            value = self._failure_translation_data[key]
        else:
            value = self._current_translation_data[key]

        if not args:
            return value

        return value % args


def get_translator() -> Translator | None:
    return _active_translator


__all__ = 'FILE_EXTENSION', 'Translator', 'get_translator'
