'''
An application designed to check which methods in a Python file lack of docstrings.

Alias: nwdsc
'''

# GLOBAL MODULES
import ast
import sys
from ast import Module
from argparse import ArgumentParser, Namespace
from typing import Callable, Optional, cast

# LOCAL MODULES
# CONSTANTS
# STATIC CLASSES
class _MessageCollection():

    '''Collects all the messages used for logging and for the exceptions.'''

    @staticmethod
    def parser_description() -> str:
        return "Checks if all methods in a Python file have docstrings."
    @staticmethod
    def file_path_to_the_python_file() -> str:
        return "The file path to the Python file to check docstrings for."
    @staticmethod
    def exclude_substrings() -> str:
        return "One or multiple substrings to exclude from the output."
    
    @staticmethod
    def all_methods_have_docstrings() -> str:
        return "All methods have docstrings."

# CLASSES
class APAdapter():

    '''Customizes argparse.ArgumentParser for this use case.'''

    __parser_factory : Callable[[], ArgumentParser]

    def __init__(
            self,
            parser_factory : Callable[[], ArgumentParser] = lambda : ArgumentParser(description = _MessageCollection.parser_description())
        ) -> None:
        self.__parser_factory = parser_factory

    def parse_args(self) -> tuple[Optional[str], list[str]]:

        '''Parses provided arguments.'''

        try:

            parser : ArgumentParser = self.__parser_factory()
            parser.add_argument("--file_path", "-fp", required = True, help = _MessageCollection.file_path_to_the_python_file())
            parser.add_argument("--exclude", "-e", required = False, action = "append", default = [], help = _MessageCollection.exclude_substrings())

            args : Namespace = parser.parse_args()

            return (args.file_path, args.exclude)

        except:
            return (None, [])
class DocStringManager():

    '''Collects all the logic related to docstrings management.'''

    __logging_function : Callable[[str], None]

    def __init__(self, logging_function : Callable[[str], None] = lambda msg : print(msg)) -> None:
    
        self.__logging_function = logging_function

    def load_source(self, file_path : str) -> str:

        '''Loads source from file_path.'''

        source : str = ""

        with open(file_path, "r", encoding='utf-8') as file:
            source = file.read()

        return source
    def get_missing_docstrings(self, source : str, exclude : list[str]) -> list[str]:

        '''Returns all the method names missing docstrings by excluding specified substrings.'''

        tree : Module = ast.parse(source=source)

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
    def log_docstrings(self, missing: list[str]) -> None:

        '''Prints missing docstrings.'''

        if missing:
            for method in missing:
                self.__logging_function(method)
        else:
            self.__logging_function(_MessageCollection.all_methods_have_docstrings())
class DocStringChecker():

    '''Collects all the logic related to docstrings checking.'''

    __ap_adapter : APAdapter
    __docstring_manager : DocStringManager
    __exit_function : Callable[[], None]

    def __init__(
        self, 
        ap_adapter : APAdapter = APAdapter(), 
        docstring_manager : DocStringManager = DocStringManager(),
        exit_function : Callable[[], None] = lambda : sys.exit()) -> None:

        self.__ap_adapter = ap_adapter
        self.__docstring_manager = docstring_manager
        self.__exit_function = exit_function

    def run(self) -> None:

        '''Runs the docstring check.'''

        file_path, exclude = self.__ap_adapter.parse_args()

        if file_path is None:
            self.__exit_function()

        source : str = self.__docstring_manager.load_source(file_path = cast(str, file_path))
        missing : list[str] = self.__docstring_manager.get_missing_docstrings(source = source, exclude = exclude)
        self.__docstring_manager.log_docstrings(missing = missing)

# MAIN
if __name__ == "__main__":
    DocStringChecker().run()