from dlang.parser import parse
from os.path import isdir
from os import listdir


FILE_EXTENSION = 'dlang'


_current_lang: str = 'en'
_data = {

}


class TranslatableText:
    def __init__(self, key: str, *args):
        self._format_args = args
        self._key = key

        self.update_translation()

        if args:
            self.translated_text %= args

    def update_translation(self):
        translated_text = get_translation(self._key)

        self.translated_text = self._key if translated_text is None else translated_text

        if self._format_args:
            self.translated_text %= self._format_args

    def format(self, *args):
        self._format_args = args

        if args:
            self.translated_text %= args

    def __str__(self):
        return self.translated_text

    def __repr__(self):
        return f'TranslatableText({repr(self._key)} -> {repr(self.translated_text)})'


def load_translations_from(path: str):
    if not isdir(path):
        return

    for segment in listdir(path):
        if isdir(segment) and segment.endswith('.' + FILE_EXTENSION):
            continue

        with open(f'{path}/{segment}', 'r', encoding='utf-8') as f:
            lang_key = segment[:-len(FILE_EXTENSION) - 1]
            lang_data = parse(f.read())

            if lang_key in _data:
                _data[lang_key].update(lang_data)
            else:
                _data[lang_key] = lang_data


def get_langs_keys():
    return tuple(_data.keys())


def set_current_lang(lang: str):
    if lang not in _data:
        return

    global _current_lang

    if lang in _data:
        _current_lang = lang
        return

    for lang_key in _data:
        if lang_key.lower().startswith(lang.lower()):
            _current_lang = lang_key


def get_lang_data(lang: str = ...):
    if lang is ...:
        lang = _current_lang

    if lang in _data:
        return _data[lang]

    for lang_key in _data:
        if lang_key.lower().startswith(lang.lower()):
            return _data[lang_key]


def get_translation(key: str, lang: str = ...):
    lang_dict = get_lang_data(lang)

    if lang_dict is None or key not in lang_dict:
        return

    return lang_dict[key]


__all__ = (
    'FILE_EXTENSION',
    'TranslatableText',
    'load_translations_from',
    'get_langs_keys',
    'set_current_lang',
    'get_lang_data',
    'get_translation'
)
