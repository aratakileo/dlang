# ATTENTION: dict key do not support newline char unlike dict value, which is also stripped of the spaces
# and newlines chars on the right and left


def parse(text: str):
    parsed_dict = {}

    special_chars_buffer = ''
    dict_value = ''
    dict_key = ''

    is_waiting_for_newline_char_to_continue = False

    for current_char in text:
        if is_waiting_for_newline_char_to_continue:
            if current_char != '\n':
                continue

            dict_value += '\n'
            is_waiting_for_newline_char_to_continue = False
            continue

        if current_char in '\\:=#n':  # special chars: \, :, =, #, n
            special_chars_buffer += current_char

            if special_chars_buffer == ':=':
                has_newline = '\n' in dict_value

                if not dict_key or has_newline:
                    if has_newline:
                        # if there is newline char before `:=`
                        lines_buffer = dict_value.split('\n')

                        if dict_key:
                            # if `dict_key` already defined then its value is set in the form of all buffered lines,
                            # except for the last one, where `:=` is located
                            parsed_dict[dict_key] = '\n'.join(lines_buffer[:-1]).strip().strip('\n')

                        dict_key = lines_buffer[-1].strip()
                    else:
                        # if `dict_key` is not defined
                        dict_key = dict_value.strip()

                    dict_value = ''
                else:
                    # if `dict_key` is already defined or `:=` used in the same line as value key
                    dict_value += special_chars_buffer

                special_chars_buffer = ''
            elif special_chars_buffer == '#':
                # this code is responsible for starting ignoring all characters after the `#` character,
                # before the newline character or the end of the file

                is_waiting_for_newline_char_to_continue = True
                special_chars_buffer = ''
            elif len(special_chars_buffer) == 2:
                # this next two conditions are responsible for escaping characters: \n, \\, \:, \=, \#
                if special_chars_buffer in '\\\\\\:\\=\\#':
                    dict_value += special_chars_buffer[-1]
                elif special_chars_buffer == '\\n':
                    dict_value += '\n'
                else:
                    # incorrect escape combinations are simply added like other text
                    dict_value += special_chars_buffer

                special_chars_buffer = ''

            continue

        if special_chars_buffer:
            # this is necessary if there are chars left in the `special_chars_buffer`
            # and the `current_char` does not belong to special chars

            dict_value += special_chars_buffer
            special_chars_buffer = ''

        dict_value += current_char

    # set the last value to the dict
    parsed_dict[dict_key] = dict_value.strip().strip('\n')

    return parsed_dict
