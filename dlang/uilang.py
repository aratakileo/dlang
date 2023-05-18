from platform import system

PLATFORM = system().lower()

if PLATFORM == 'windows':
    import ctypes
    import locale

    def get_sys_lang_code() -> str:
        return locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]
else:
    def get_sys_lang_code():
        return 'en_US'


__all__ = 'get_sys_lang_code',
