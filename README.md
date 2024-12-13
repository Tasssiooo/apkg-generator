# How to use

It's very simple, the first argument (input) is the path to the input, a file that contains the terms (it can be any kind of text file).

    $ ./apkggen ~/Documents/myterms.txt

The second argument (output) is the path to the output file, it's an optional argument, if not given, it will default to the same path as input.

    $ ./apkggen ~/Documents/myterms.txt -o ~/Documents/myapkg_from_myterms.apkg

The third argument is the language, if you choose to scrap from Wiktionary, use single language codes like: en, es, it, etc. Cambridge has bilingual dictionaries so you can use double language codes like: en-pt, en-es, es-en, etc.

    $ ./apkggen ~/Documents/myterms.txt -o ~/Documents/myapkg_from_myterms.apkg en-pt

#### Cambridge available codes:

- en (us)
- en-pt
- en-jp
- en-es
- es-en
- en-cn
- en-tw
- en-nl
- en-fr
- en-de
- en-id
- en-it
- en-no
- en-pl
- en-sv

The last argument is the source where you want to scrap from. For now, there is only [Cambridge Dictionary](https://dictionary.cambridge.org/) and [Wiktionary](https://www.wiktionary.org/). The argument **must** be either _cam_ for Cambridge or _wik_ for Wiktionary.

    $ ./apkggen ~/Documents/myterms.txt -o ~/Documents/myapkg_from_myterms.apkg en-pt cam

# APIs

- [Cambridge](https://github.com/Tasssiooo/cambridge-dictionary-api);
- [Wiktionary](https://en.wiktionary.org/api/rest_v1/);
