from platform import system

PLATFORM = system().lower()

if PLATFORM == 'windows':
    import ctypes
    import locale

    def get_default_ui_language() -> str:
        return locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]
else:
    def get_default_ui_language():
        return 'en_US'


__all__ = 'get_default_ui_language',
