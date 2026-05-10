'''
A CLI application built on the top of nwdocstringchecking.
'''

# GLOBAL MODULES
import ast
import sys
from ast import Module
from argparse import ArgumentParser, Namespace
from typing import Callable, Optional, Tuple, cast

# LOCAL MODULES
# CONSTANTS
# STATIC CLASSES
class _MessageCollectionAPFactory():

    '''Collects all the messages used for logging and for the exceptions used by APFactory.'''

    @staticmethod
    def parser_description() -> str:
        return "Checks if all methods in a Python file have docstrings."
    @staticmethod
    def file_path_to_the_python_file() -> str:
        return "The file path to the Python file to check docstrings for."
    @staticmethod
    def exclude_substrings() -> str:
        return "One or multiple substrings to exclude from the output."
class _MessageCollection(_MessageCollectionAPFactory):

    '''Collects all the messages used for logging and for the exceptions.'''

# CLASSES
class APFactory():

    '''Encapsulates all the logic related to the creation of a custom instance of argparse.ArgumentParser.'''

    def create(self) -> ArgumentParser:

        '''Creates a custom instance of argparse.ArgumentParser.'''

        argument_parser : ArgumentParser = ArgumentParser(description = _MessageCollection.parser_description())
        argument_parser.add_argument("--file_path", "-fp", required = True, help = _MessageCollection.file_path_to_the_python_file())
        argument_parser.add_argument("--exclude", "-e", required = False, action = "append", default = [], help = _MessageCollection.exclude_substrings())

        return argument_parser
class APAdapter():

    '''Customizes argparse.ArgumentParser for this use case.'''

    __ap_factory : APFactory

    def __init__(self, ap_factory : APFactory = APFactory()) -> None:
        self.__ap_factory = ap_factory

    def parse_args(self) -> Tuple[Optional[str], list[str]]:

        '''Parses provided arguments.'''

        try:

            parser : ArgumentParser = self.__ap_factory.create()
            args : Namespace = parser.parse_args()

            return (args.file_path, args.exclude)

        except:
            return (None, [])

# MAIN
def main(): pass

if __name__ == "__main__":
    main()