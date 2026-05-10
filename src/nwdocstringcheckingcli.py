'''
A CLI application built on the top of nwdocstringchecking.
'''

# GLOBAL MODULES
import os
from argparse import ArgumentParser, Namespace
from typing import Any, Callable, Final

# LOCAL MODULES
from nwdocstringchecking import DocStringChecker, Validator
from setupinfo import CLI_DESCRIPTION, PROJECT_VERSION

# CONSTANTS
class CLISTRING:

    '''Collects all the CLI-related strings.'''

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
class _MessageCollectionCLIManager():

    '''Collects all the messages used for logging and for the exceptions.'''
    
    @staticmethod
    def all_methods_have_docstrings() -> str:
        return "All methods have docstrings."
class _MessageCollection(
        _MessageCollectionAsciiBannerManager,
        _MessageCollectionCLIManager):

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
class CLIValidator:

    '''Handles CLI argument validation.'''

    def validate_file_path(self, file_path: str) -> str:

        '''Returns file_path or raises Exception.'''

        Validator().validate_file_path(file_path)

        return file_path
class APFactory():

    '''Encapsulates all the logic related to the creation of a custom instance of argparse.ArgumentParser.'''

    __cli_validator : CLIValidator

    def __init__(self, cli_validator : CLIValidator = CLIValidator()) -> None:
        self.__cli_validator = cli_validator

    def create(self) -> ArgumentParser:

        '''
            Creates a custom instance of argparse.ArgumentParser.

            The "prog" argument is not provided in order to make the "usage" statement  dynamic:

                usage: nwdocstringcheckingcli.py [-h] --file_path FILE_PATH [--exclude EXCLUDE]
        '''

        argument_parser : ArgumentParser = ArgumentParser(description = CLI_DESCRIPTION)

        argument_parser.add_argument(
            *CLISTRING.OPTION_FILEPATH_FLAGS,
            dest = CLISTRING.OPTION_FILEPATH_DEST,
            required = CLISTRING.OPTION_FILEPATH_REQUIRED,
            help = CLISTRING.OPTION_FILEPATH_HELP,
            type = self.__cli_validator.validate_file_path)
        
        argument_parser.add_argument(
            *CLISTRING.OPTION_EXCLUDE_FLAGS,
            dest = CLISTRING.OPTION_EXCLUDE_DEST,
            required = CLISTRING.OPTION_EXCLUDE_REQUIRED,
            help = CLISTRING.OPTION_EXCLUDE_HELP,
            default = CLISTRING.OPTION_EXCLUDE_DEFAULT,
            action = CLISTRING.OPTION_EXCLUDE_ACTION)

        return argument_parser
class CLIManager():

    '''Collects all the logic related to the CLI management.'''

    __ap_factory : APFactory
    __ascii_banner_manager : AsciiBannerManager
    __docstring_checker : DocStringChecker
    __logging_function : Callable[[str], None]

    def __init__(
        self, 
        ap_factory : APFactory = APFactory(), 
        ascii_banner_manager : AsciiBannerManager = AsciiBannerManager(),
        docstring_checker : DocStringChecker = DocStringChecker(),
        logging_function : Callable[[str], None] = lambda msg : print(msg)) -> None:
        
        self.__ap_factory = ap_factory
        self.__ascii_banner_manager = ascii_banner_manager
        self.__docstring_checker = docstring_checker
        self.__logging_function = logging_function

    def __log_ascii_banner(self) -> None:
        self.__logging_function(self.__ascii_banner_manager.create(PROJECT_VERSION))
    def __log_namespace(self, args : Namespace):

        '''Logs the provided args.'''

        for key, value in vars(args).items():
            self.__logging_function(f"{key}: '{value}'")
            
        self.__logging_function("")
    def __log_docstrings(self, missing: list[str]) -> None:

        '''Prints missing docstrings.'''

        if missing:
            for method in missing:
                self.__logging_function(method)
        else:
            self.__logging_function(_MessageCollection.all_methods_have_docstrings())

    def run_and_log(self) -> None:

        '''
            Extract the missing docstrings and log them.
            
            The SystemExit exception occurs when a required option is not provided.
            SystemExit doesn't inherit from Exception and has no message, therefore we need to handle it accordingly.            
        '''

        try:

            self.__log_ascii_banner()

            argument_parser : ArgumentParser = self.__ap_factory.create()
            args : Namespace = argument_parser.parse_args()

            self.__log_namespace(args)

            missing : list[str] = self.__docstring_checker.run(file_path = args.file_path, exclude = args.exclude)
            
            self.__log_docstrings(missing)
            
        except (Exception, SystemExit) as e:
            
            if not isinstance(e, SystemExit):
                self.__logging_function(str(e))

# MAIN
def main(): CLIManager().run_and_log()

if __name__ == "__main__":
    main()