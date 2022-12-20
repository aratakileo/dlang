def parse(text: str):
    parsed_data = {}

    special_chars_buffer = ''
    chars_buffer = ''
    key_buffer = ''

    ignore = False

    for char in text:
        if ignore:
            if char != '\n':
                continue

            ignore = False

        if char in '\\:=#n':
            special_chars_buffer += char

            if special_chars_buffer == ':=':
                has_new_line = '\n' in chars_buffer

                if not key_buffer or has_new_line:
                    if has_new_line:
                        lines = chars_buffer.split('\n')

                        if key_buffer:
                            parsed_data[key_buffer] = '\n'.join(lines[:-1])

                        key_buffer = lines[-1]
                    else:
                        key_buffer = chars_buffer

                    chars_buffer = ''
                else:
                    chars_buffer += special_chars_buffer

                special_chars_buffer = ''
            elif special_chars_buffer == '#':
                ignore = True
                special_chars_buffer = ''
            elif len(special_chars_buffer) == 2:
                if special_chars_buffer in '\\\\\\:\\=\\#':
                    chars_buffer += special_chars_buffer[-1]
                elif special_chars_buffer == '\\n':
                    chars_buffer += '\n'
                else:
                    chars_buffer += special_chars_buffer

                special_chars_buffer = ''

            continue

        if special_chars_buffer:
            chars_buffer += special_chars_buffer
            special_chars_buffer = ''

        chars_buffer += char

    parsed_data[key_buffer] = chars_buffer

    return parsed_data
