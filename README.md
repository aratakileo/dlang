# dlang (double language)
A convenient flexible python library for implementing a multilingual interface, for translating your application

### Requirements
- `python >= 3.10`

### Install
```
pip install git+https://github.com/teacondemns/dlang.git
```

<details>
  <summary>for <code>windows</code></summary>
  

```
py -m pip install git+https://github.com/teacondemns/dlang.git
```
</details>

<details>
  <summary>for <code>unix</code>/<code>macos</code></summary>
  

```
python3 -m pip install git+https://github.com/teacondemns/dlang.git
```
</details>

# How to use
### Navigation
- [Quick start](#quick-start)
- [Attributes and methods of `dlang.Translator`](#attributes-and-methods-of-dlangtranslator)

### Quick start
To start using the library tools, it will be enough to write the following code:
```py
import dlang

# initializing the main component and loading translations
# replace 'path_to_your_translates_directory/' to your path or paths
translator = dlang.Translator(['path_to_your_translates_directory/'])

# get a translation by the translated value key
print(translator.get_translation('lang.de'))
```
In order to access the main component of the library from another file, it is enough to call `dlang.get_translator()`:
```py
import dlang

# such logic can be used only if initialization has been performed once, as in the code above
translator = dlang.get_translator()
```

### Attributes and methods of `dlang.Translator`
- the paths by which the translator loads translations
```py
print(translator.path_or_paths)
```
- current/selected translation language
```py
print(translator.current_lang)
```
- the translation language to be accessed by the translator if the specified key of the translated value is not found in the translation of the current language. The translator will also replace the value of `current_lang` with the value of `failure_lang` if the translation language specified in `current_lang` is not found in the translations
```py
print(translator.failure_lang)
```
- list of translation languages whose presets (ready-made translations from the library itself) were used
```py
print(translator.list_of_used_lang_presets)
```
- list of languages whose translations have been loaded
```py
print(translator.lang_keys)
```
- names of downloaded languages in the native language
```py
print(translator.lang_native_names)
```
- load translations using the specified paths, including the path of preset translations (ready-made translations from the library itself)
```py
translator.load_translations()
```
- get a translation by the translated value key
```py
print(translator.get_translation('lang.jp'))
```
