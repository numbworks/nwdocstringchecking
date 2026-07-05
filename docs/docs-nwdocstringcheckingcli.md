# nwdocstringcheckingcli
Contact: numbworks@gmail.com

## Revision History

| Date | Author | Description |
|---|---|---|
| 2025-05-18 | numbworks | Created. |
| 2026-07-05 | numbworks | Last updated (v2.0.1). |

## Introduction

`nwdocstringcheckingcli` is a command-line application built on the top of `nwdocstringchecking`.

## CLI Reference

|*Command*|*Sub Command*|Options|Exit Codes|
|---|---|---|---|
|||*--help, -h*|Success|

|Option|Value|Default|
|---|---|---|
|--file_paths|`<file path>`|-|
|*--exclude*|`<string>`|-|

## Examples

Run it against a `file_path`:

```sh
root@e584fefc57f0:/# alias nwds="python src/nwdocstringcheckingcli.py"
root@e584fefc57f0:/# nwds --file_path src/nwdocstringchecking.py
```

```
*******************************************
'##::: ##:'##:::::'##:'########:::'######::
 ###:: ##: ##:'##: ##: ##.... ##:'##... ##:
 ####: ##: ##: ##: ##: ##:::: ##: ##:::..::
 ## ## ##: ##: ##: ##: ##:::: ##:. ######::
 ##. ####: ##: ##: ##: ##:::: ##::..... ##:
 ##:. ###: ##: ##: ##: ##:::: ##:'##::: ##:
 ##::. ##:. ###. ###:: ########::. ######::
..::::..:::...::...:::........::::......:::
************************Version: 2.0.1*****

file_path: 'src/nwdocstringchecking.py'
exclude: '[]'

_MessageCollectionValidator.provided_file_path_doesnt_exis
```

Run it against a `file_path` with `exclude`:

```sh
alias nwds="python src/nwdocstringcheckingcli.py"
nwds --file_path src/nwdocstringchecking.py --exclude Message --exclude Something
```

```
*******************************************
'##::: ##:'##:::::'##:'########:::'######::
 ###:: ##: ##:'##: ##: ##.... ##:'##... ##:
 ####: ##: ##: ##: ##: ##:::: ##: ##:::..::
 ## ## ##: ##: ##: ##: ##:::: ##:. ######::
 ##. ####: ##: ##: ##: ##:::: ##::..... ##:
 ##:. ###: ##: ##: ##: ##:::: ##:'##::: ##:
 ##::. ##:. ###. ###:: ########::. ######::
..::::..:::...::...:::........::::......:::
************************Version: 2.0.1*****

file_path: 'src/nwdocstringchecking.py'
exclude: '['Message', 'Something']'

All methods have docstrings.
```

## Markdown Toolset

Suggested toolset to view and edit this Markdown file:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)
- [Markdown PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf)