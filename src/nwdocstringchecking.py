'''
A library designed to identify which methods in a Python file are missing docstrings.

Alias: nwds
'''

# GLOBAL MODULES
import ast
import os
from ast import Module
from typing import Optional, cast

# LOCAL MODULES
# CONSTANTS
# STATIC CLASSES
class _MessageCollectionValidator():

    '''Collects all the messages used for logging and for the exceptions used by Validator.'''

    @staticmethod
    def provided_file_path_doesnt_exist(file_path : str) -> str:
        return f"The provided 'file_path' doesn't exist: '{file_path}'."
class _MessageCollection(
        _MessageCollectionValidator):

    '''Collects all the messages used for logging and for the exceptions.'''
class _Validator():

    '''Collects all validation methods.'''

    @staticmethod
    def validate_file_path(file_path : str) -> None:

        '''Returns file_path or raises Exception.'''
        
        if not os.path.isfile(file_path):
            raise Exception(_MessageCollection.provided_file_path_doesnt_exist(file_path))

# CLASSES
class DocStringChecker():

    '''Collects all the logic related to docstrings management.'''

    def __load_source(self, file_path : str) -> str:

        '''Loads source from file_path.'''

        source : str = ""

        with open(file_path, "r", encoding='utf-8') as file:
            source = file.read()

        return source
    def __get_missing_docstrings(self, source : str, exclude : list[str]) -> list[str]:

        '''Returns all the method names missing docstrings by excluding specified substrings.'''

        tree : Module = ast.parse(source = source)

        method_names : list[str] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if ast.get_docstring(item) is None:
                            method_name = f"{node.name}.{item.name}"
                            if not any(substring in method_name for substring in exclude):
                                method_names.append(method_name)

        return method_names

    def run(self, file_path : str, exclude : list[str] = []) -> list[str]:

        '''Runs the docstring check.'''

        _Validator.validate_file_path(file_path)

        source : str = self.__load_source(file_path = cast(str, file_path))
        missing : list[str] = self.__get_missing_docstrings(source = source, exclude = exclude)

        return missing

# MAIN
if __name__ == "__main__":
    pass