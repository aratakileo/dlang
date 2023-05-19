from dlang.uilang import get_sys_lang_code
from dlang.resource import RESOURCES_PATH
from os.path import isdir, isfile
from dlang.loader import loads
from typing import Sequence
from warnings import warn
from os import listdir


FILE_EXTENSION = 'dlang'
TRANSLATION_PRESET_PATH = RESOURCES_PATH + 'lang/'
TRANSLATE_KEY_PREFIX_OF_LANG_NAME = 'lang.'

_active_translator = None


class Translator:
    def __init__(
            self,
            path_or_paths: str | Sequence[str],
            current_lang=...,
            failure_lang='en',
            list_of_used_lang_presets: Sequence[str] = ...
    ):
        global _active_translator
        _active_translator = self

        if isinstance(path_or_paths, str):
            self._paths = path_or_paths,
        else:
            self._paths = *path_or_paths,

        self._lang_keys: tuple[str] = ()
        self._lang_native_names: tuple[str] = ()
        self._all_translation_data: dict[str, dict[str, str]] = {}
        self._list_of_used_lang_presets = list_of_used_lang_presets
        self._list_of_translatable_objects = []
        self._current_lang = self._failure_lang = ''

        self.load_translation()

        if current_lang is ...:
            current_lang = get_sys_lang_code()[:2]

            if current_lang not in self._lang_keys:
                current_lang = failure_lang

        self.current_lang = current_lang
        self.failure_lang = failure_lang

    @property
    def path_or_paths(self) -> tuple[str]:
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
            self._current_translation_data: dict[str, str] = {}
            return

        self._current_translation_data = self._all_translation_data[new_value]

        self.__update_translatable_objects()

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
            self._failure_translation_data: dict[str, str] = {}
            return

        self._failure_translation_data = self._all_translation_data[new_value]

        self.__update_translatable_objects()

    @property
    def list_of_used_lang_presets(self):
        return self._list_of_used_lang_presets

    @list_of_used_lang_presets.setter
    def list_of_used_lang_presets(self, new_value: Sequence[str]):
        old_value = self._list_of_used_lang_presets
        self._list_of_used_lang_presets = new_value

        if old_value != new_value:
            self.load_translation()

    @property
    def lang_keys(self):
        return self._lang_keys

    @property
    def lang_native_names(self):
        return self._lang_native_names

    def __update_translatable_objects(self):
        for translatable_object in self._list_of_translatable_objects:
            translatable_object.update_translation()

    def load_translation(self):
        self._all_translation_data = {}
        paths = self._paths if not self._list_of_used_lang_presets else (TRANSLATION_PRESET_PATH, *self._paths)

        for path in paths:
            if not isdir(path):
                warn(f"DLANG -> '{path}' is not a dir")
                continue

            for file_path in listdir(path):
                file_path = path + '/' + file_path

                if not (isfile(file_path) and file_path.endswith('.' + FILE_EXTENSION)):
                    continue

                lang_key = file_path.replace('\\', '/').split('/')[-1].split('.')[-2]

                if self._list_of_used_lang_presets is not ... and lang_key not in self._list_of_used_lang_presets:
                    continue

                with open(file_path, 'r', encoding='utf-8') as file:
                    if lang_key not in self._all_translation_data:
                        self._all_translation_data[lang_key] = {}

                    self._all_translation_data[lang_key].update(loads(file.read()))

        self._lang_keys = tuple(self._all_translation_data.keys())
        lang_native_names = []

        for lang_key, lang_data in self._all_translation_data.items():
            translate_key = TRANSLATE_KEY_PREFIX_OF_LANG_NAME + lang_key
            lang_native_names.append(translate_key if translate_key not in lang_data else lang_data[translate_key])

        self._lang_native_names = *lang_native_names,

        self.__update_translatable_objects()

    def get_translation(self, translate_key: str, *args, **kwargs):
        if translate_key not in self._current_translation_data:
            if translate_key not in self._failure_translation_data:
                return translate_key

            value = self._failure_translation_data[translate_key]
        else:
            value = self._current_translation_data[translate_key]

        if not (args or kwargs):
            return value

        return value.format(*args, **kwargs)

    def add_translatable_object(self, translatable_object):
        self._list_of_translatable_objects.append(translatable_object)

    def remove_translatable_object(self, translatable_object):
        self._list_of_translatable_objects.remove(translatable_object)


def get_translator() -> Translator | None:
    return _active_translator


__all__ = 'Translator', 'get_translator'
