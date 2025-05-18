'''Contains packaging information about nwdocstringchecking.py.'''

# GLOBAL MODULES
from setuptools import setup

# INFORMATION
MODULE_ALIAS : str = "nwdsc"
MODULE_NAME : str = "nwdocstringchecking"
MODULE_VERSION : str = "1.0.0"

# SETUP
if __name__ == "__main__":
    setup(
        name = MODULE_NAME,
        version = MODULE_VERSION,
        description = "An application designed to check which methods in a Python file lack of docstrings.",
        author = "numbworks",
        url = f"https://github.com/numbworks/{MODULE_NAME}",
        py_modules = [ MODULE_NAME ],
        install_requires = [ ],
        python_requires = ">=3.12",
        license = "MIT"
    )