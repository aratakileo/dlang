def escape_text(text: str):
    return text.replace('\\', '\\\\').replace(':', '\\:').replace('=', '\\=').replace('#', '\\#')


def dumps(obj: dict[str, str]):
    output_text = ''

    for key, value in obj.items():
        output_text += '\n' + escape_text(key).replace('\n', ' ').strip(' ') + ' := ' + escape_text(
            value
        ).strip('\n').strip(' ')

    return output_text.strip('\n')
