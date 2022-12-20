from dlang.parser import parse
from os.path import isdir
from os import listdir


FILE_EXTENSION = 'dlang'


_current_lang: str = 'en'
_data = {

}


def load_localizations_from(path: str):
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
    _current_lang = lang


def get_lang_data(lang: str = ...):
    if lang is ...:
        lang = _current_lang

    for lang_key in _data.keys():
        if lang_key.lower().startswith(lang.lower()):
            return _data[lang_key]


def get_localization(key: str, lang: str = ...):
    lang_dict = get_lang_data(lang)

    if lang_dict is None or key not in lang_dict:
        return

    return lang_dict[key]


__all__ = (
    'FILE_EXTENSION',
    'load_localizations_from',
    'get_langs_keys',
    'set_current_lang',
    'get_lang_data',
    'get_localization'
)
