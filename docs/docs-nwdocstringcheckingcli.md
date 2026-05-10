# nwdocstringcheckingcli
Contact: numbworks@gmail.com

## Revision History

| Date | Author | Description |
|---|---|---|
| 2025-05-18 | numbworks | Created. |
| 2026-05-10 | numbworks | Last updated (2.0.0). |

## Introduction

`nwdocstringcheckingcli` is a command-line application built on the top of `nwdocstringchecking`.

## Overview

This application is designed to run as a CLI (command-line interface) from within a terminal.

Invoking the script without arguments:

```
root@17b38eb6123b:/# python nwdocstringchecking.py
```

will return the help information:

```
usage: nwdocstringchecking.py [-h] --file_path FILE_PATH [--exclude EXCLUDE]
nwdocstringchecking.py: error: the following arguments are required: --file_path/-fp
```

Invoking the script against a Python file with missing docstrings:

```
root@17b38eb6123b:/# python nwdocstringchecking.py --file_path nwdocstringchecking.py
```

will return a list of method names:

```
_MessageCollection.parser_description
_MessageCollection.file_path_to_the_python_file
_MessageCollection.exclude_substrings
_MessageCollection.all_methods_have_docstrings
DocStringManager.__init__
DocStringChecker.__init__
```

Using the `exclude` argument(s):

```
root@17b38eb6123b:/# python nwdocstringchecking.py --file_path nwdocstringchecking.py --exclude _MessageCollection --exclude __init__
```

will filter the output accordingly and/or return the following message:

```
All methods have docstrings.
```

## Markdown Toolset

Suggested toolset to view and edit this Markdown file:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)
- [Markdown PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf)