from dlang.translator import get_translator


class TranslatableObject:
    def __init__(self):
        get_translator().add_translatable_object(self)

    def update_translation(self) -> str: ...


class TranslatableText(TranslatableObject):
    def __init__(self, translated_value_key: str, *args, **kwargs):
        super().__init__()

        self._translated_value_key = translated_value_key
        self._format_args = args
        self._format_kwargs = kwargs
        self._translated_text = get_translator().get_translation(translated_value_key, *args, **kwargs)

    @property
    def translate_key(self):
        return self._translated_value_key

    @property
    def translated_text(self):
        return self._translated_text

    def set_format(self, *args, **kwargs):
        self._format_args = (*args, *self._format_args[len(args):])
        self._format_kwargs.update(kwargs)

        self.update_translation()

    def update_translation(self):
        self._translated_text = get_translator().get_translation(
            self._translated_value_key,
            *self._format_args,
            **self._format_kwargs
        )

        return self._translated_text

    def __str__(self):
        return self._translated_text

    def __repr__(self):
        format_args_segment = format_kwargs_segment = ''

        if self._format_args:
            format_args_segment = ', '

            if len(self._format_args) == 1:
                format_args_segment += repr(self._format_args[0])
            else:
                format_args_segment += repr(self._format_args)[1:-1]

        for key, value in self._format_kwargs.items():
            format_kwargs_segment += f', {key}={repr(value)}'

        if len(self._format_args) == 1:
            format_kwargs_segment = format_kwargs_segment[2:]

        return f'{self.__class__.__name__}({repr(self._translated_value_key)}{format_args_segment}{format_kwargs_segment})'


__all__ = 'TranslatableObject', 'TranslatableText'
