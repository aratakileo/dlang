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
- [Parameters, when initializing `dlang.Translator`](#parameters-when-initializing-dlangtranslator)
- [Syntax of `.dlang` language files](#syntax-of-dlang-language-files)

### Quick start
To start using the library tools, it will be enough to write the following code:
```py
import dlang

# initializing the main component and loading translations
# replace 'path_to_your_translates_directory/' to your path or to list of path
translator = dlang.Translator('path_to_your_translates_directory/')

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
- the translation language that the translator will use if the translation key does not exist in the selected translation or if the selected translation language has not been downloaded, then this translation language will be used
```py
print(translator.failure_lang)
```
- list of translation language whose presets (ready-made translations from the library itself) will loaded before load translations from `path_or_paths`
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
# replace 'your key' to your key of translated value, all other arguments after first are specified here for example
print(translator.get_translation('your key', 1234, False, some_value='something', last_some_value=(5, 6, 7, 8)))
```

### Parameters, when initializing `dlang.Translator`
Let's take a look on the code below:
```py
import dlang

translator = dlang.Translator(
    # this parameter is mandatory, as a value, you must specify the path or a list of paths to folders with translation 
    # files. In this case, you will need to replace 'path_to_your_translates_directory/' with your value
    path_or_paths='path_to_your_translates_directory/',
    
    # current/selected translation language. If you did not specify anything, or specified the value `...` (Ellipsis), 
    # then in this case, if the program is running on Windows, the language will be set as in the user's system, 
    # if such a translation language has been loaded, otherwise `failure_language` will be set. If the program is not 
    # running on Windows, the default language will be English
    current_lang='uk',
    
    # the translation language that the translator will use if the translation key does not exist in the selected 
    # translation or if the selected translation language has not been downloaded, then this translation language 
    # will be used
    failure_lang='de',
    
    # list of translation language whose presets (ready-made translations from the library itself) will loaded before 
    # load translations from `path_or_paths`
    list_of_used_lang_presets=('de', 'uk')
)
```

### Syntax of `.dlang` language files
The syntax of the `.dlang` language files was based on the `.lang` language files for Minecraft Bedrock Edition from Mojang Studios.

Each translated value is recorded in the file in this way:
```
key of the translated value := translated value
```
In this case, the key of the translated value can consist of any characters, except newline characters and special chars: `:`, `=`, `#`. Any characters can be used in the translated value except for special char: `:`, `=`, `#`. That means that the translated value can be multi-line. If there is a need to use special characters in one case or another, then you can just escape them this way: `\:`, `\=`, `\#`. The same applies to the `\ ` symbol: `\\`. Also, if necessary, the newline character can be escaped: `\n`.

Also, the `.dlang` syntax supports single-line comments that the parser will skip:
```py
# your comment is here

key of the translated value := translated value  # or here
```
It is also important to note that the language key is taken from the file name, namely:
- if there is only one dot in the file name to separate the name itself and its extension, then the part of the name up to the dot will be taken as the language key. For example, `ru` will be taken from the name `ru.dlang`
- if there are several dots in the name, then the text between the last and penultimate dots will be taken as the language key. For example, `es` will be taken from the name `com.my.application.translation.es.dlang`
