'''
A CLI application built on the top of nwdocstringchecking.
'''

# GLOBAL MODULES
import os
from argparse import ArgumentParser, Namespace
from typing import Any, Callable, Final, Optional, Tuple, cast

# LOCAL MODULES
from nwdocstringchecking import Validator
from setupinfo import CLI_NAME, CLI_DESCRIPTION, PROJECT_VERSION

# CONSTANTS
class CLISTRING:

    '''Collects all the CLI-related strings.'''

    COMMAND_DEST : Final[str] = "command"
    COMMAND_REQUIRED : Final[bool] = True
    COMMAND_ARGS : dict[str, Any] = { "dest": COMMAND_DEST, "required": COMMAND_REQUIRED }

    OPTION_FILEPATH_FLAGS : Final[list[str]] = ["--file_path"]
    OPTION_FILEPATH_DEST : Final[str] = "file_path"
    OPTION_FILEPATH_REQUIRED : Final[bool] = True
    OPTION_FILEPATH_HELP : Final[str] = "The path to the Python file to check docstrings for."

    OPTION_EXCLUDE_FLAGS : Final[list[str]] = ["--exclude"]
    OPTION_EXCLUDE_DEST : Final[str] = "exclude"
    OPTION_EXCLUDE_REQUIRED : Final[bool] = False
    OPTION_EXCLUDE_HELP : Final[str] = "One or multiple substrings to exclude from the output."
    OPTION_EXCLUDE_DEFAULT : Final[list[str]] = []
    OPTION_EXCLUDE_ACTION : Final[str] = "append"

# STATIC CLASSES
class _MessageCollectionAsciiBannerManager():

    '''Collects all the messages used for logging and for the exceptions.'''

    @staticmethod
    def provided_version_empty_whitespace() -> str:
        return "The provided 'version' is empty or whitespace."
class _MessageCollection(
        _MessageCollectionAsciiBannerManager):

    '''Collects all the messages used for logging and for the exceptions.'''

# CLASSES
class AsciiBannerManager:

    """Creates the ASCII banner for the provided library's version."""

    def __validate(self, version: str) -> None:
        
        """Validates the provided 'version'."""

        if not version or not version.strip():
            raise ValueError(_MessageCollection.provided_version_empty_whitespace())
    def __create_figlet(self) -> tuple:
        
        """Returns a tuple containing the figlet and its width."""
        
        lines : list[str] = [
            "'##::: ##:'##:::::'##:'########:::'######::",
            " ###:: ##: ##:'##: ##: ##.... ##:'##... ##:",
            " ####: ##: ##: ##: ##: ##:::: ##: ##:::..::",
            " ## ## ##: ##: ##: ##: ##:::: ##:. ######::",
            " ##. ####: ##: ##: ##: ##:::: ##::..... ##:",
            " ##:. ###: ##: ##: ##: ##:::: ##:'##::: ##:",
            " ##::. ##:. ###. ###:: ########::. ######::",
            "..::::..:::...::...:::........::::......:::"
        ]

        return (os.linesep.join(lines), len(lines[0]))
    def __create_frame(self, version: str, max_length: int) -> tuple:
        
        """Returns a tuple containing the frame of the figlet."""
        
        version_token : str = f"Version: {version}"
        
        margin_length : int = 5
        total_length : int = max_length - len(version_token) - margin_length

        top_line : str = "*" * max_length
        bottom_line : str = f"{top_line[:total_length]}{version_token}{'*' * margin_length}"

        return (top_line, bottom_line)

    def create(self, version: str) -> str:
        
        """Creates the formatted ASCII banner with a versioned frame."""
        
        self.__validate(version)

        figlet, max_length = self.__create_figlet()
        top_line, bottom_line = self.__create_frame(version, max_length)

        ascii_banner : str = os.linesep.join([
            top_line,
            figlet,
            bottom_line,
            ""
        ])

        return ascii_banner
class APFactory():

    '''Encapsulates all the logic related to the creation of a custom instance of argparse.ArgumentParser.'''

    def create(self) -> ArgumentParser:

        '''Creates a custom instance of argparse.ArgumentParser.'''

        argument_parser : ArgumentParser = ArgumentParser(prog = CLI_NAME, description = CLI_DESCRIPTION)

        argument_parser.add_argument(
            *CLISTRING.OPTION_FILEPATH_FLAGS,
            dest = CLISTRING.OPTION_FILEPATH_DEST,
            required = CLISTRING.OPTION_FILEPATH_REQUIRED,
            help = CLISTRING.OPTION_FILEPATH_HELP,
            type = Validator().validate_file_path)
        
        argument_parser.add_argument(
            *CLISTRING.OPTION_EXCLUDE_FLAGS,
            dest = CLISTRING.OPTION_EXCLUDE_DEST,
            required = CLISTRING.OPTION_EXCLUDE_REQUIRED,
            help = CLISTRING.OPTION_EXCLUDE_HELP,
            default = CLISTRING.OPTION_EXCLUDE_DEFAULT,
            action = CLISTRING.OPTION_EXCLUDE_ACTION)

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