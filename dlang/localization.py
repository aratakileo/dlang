from dlang.parser import parse
from os.path import isdir
from os import listdir


FILE_EXTENSION = 'dlang'


_data = {

}


def load_localization_from(path: str):
    if not isdir(path):
        return

    for segment in listdir(path):
        if isdir(segment) and segment.endswith('.' + FILE_EXTENSION):
            continue

        with open(f'{path}/{segment}', 'r', encoding='utf-8') as f:
            _data[segment[:-len(FILE_EXTENSION) - 1]] = parse(f.read())


__all__ = 'FILE_EXTENSION', 'load_localization_from',
