% nwds

# NAME
nwds - lists Python methods that miss docstrings

# SYNOPSIS
**nwds** [options]

# DESCRIPTION
**nwds** is a CLI application designed to identify which methods in a Python file are missing docstrings.

# OPTIONS

**--file_path**
The path to the Python file to check docstrings for.

**--exclude**
One or multiple substrings to exclude from the output.

**--help, -h**
Shows help and usage information.

# EXAMPLES

**Run it against a file_path:**

```text
nwds --file_path somefile.py
```

**Run it against a file_path with exclude:**

```text
nwds --file_path somefile.py --exclude Message --exclude Something
```

# AUTHOR
numbworks (numbworks@gmail.com)