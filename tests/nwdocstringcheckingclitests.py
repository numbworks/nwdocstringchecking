# GLOBAL MODULES
import os
import sys
import unittest
from argparse import ArgumentParser, Namespace
from io import StringIO
from parameterized import parameterized
from typing import Any
from unittest.mock import MagicMock, patch

# LOCAL MODULES
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwdocstringchecking import DocStringChecker
from nwdocstringcheckingcli import CLISTRING, _MessageCollection, APFactory, AsciiBannerManager, CLIManager

# SUPPORT METHODS
# TEST CLASSES
class AsciiBannerManagerTestCase(unittest.TestCase):

    def test_validate_shouldraisevalueerror_whenversionisnone(self) -> None:

        # Arrange
        # Act, Assert
        with self.assertRaises(ValueError) as context:
            AsciiBannerManager()._AsciiBannerManager__validate(version = None) # type: ignore

        self.assertEqual(_MessageCollection.provided_version_empty_whitespace(), str(context.exception))
    def test_validate_shouldraisevalueerror_whenversioniswhitespace(self) -> None:

        # Arrange
        version : str = " "

        # Act, Assert
        with self.assertRaises(ValueError) as context:
            AsciiBannerManager()._AsciiBannerManager__validate(version = version) # type: ignore

        self.assertEqual(_MessageCollection.provided_version_empty_whitespace(), str(context.exception))
    def test_createfiglet_shouldreturnexpectedmaxlength_wheninvoked(self) -> None:

        # Arrange
        expected : int = 43

        # Act
        _, max_length = AsciiBannerManager()._AsciiBannerManager__create_figlet() # type: ignore

        # Assert
        self.assertEqual(expected, max_length)
    def test_createframe_shouldreturnexpectedtuple_wheninvoked(self) -> None:

        # Arrange
        version : str = "1.0.5"
        max_length : int = 65
        
        expected_top_line : str = "*" * 65
        expected_bottom_line : str = "*" * 46 + "Version: 1.0.5" + "*" * 5

        # Act
        top_line, bottom_line = AsciiBannerManager()._AsciiBannerManager__create_frame(version = version, max_length = max_length) # type: ignore

        # Assert
        self.assertEqual(expected_top_line, top_line)
        self.assertEqual(expected_bottom_line, bottom_line)
    def test_create_shouldcallexpectedprivatemethodsandreturnbanner_wheninvoked(self) -> None:

        # Arrange
        ascii_banner_manager : AsciiBannerManager = AsciiBannerManager()
        version : str = "1.0.5"
        max_lenght : int = 65
        
        figlet_tpl : tuple = ("ascii_art", max_lenght)
        frame_tpl : tuple = ("top_border", "bottom_border")

        with patch.object(ascii_banner_manager, "_AsciiBannerManager__validate") as mocked_validate, \
                patch.object(ascii_banner_manager, "_AsciiBannerManager__create_figlet", return_value = figlet_tpl) as mocked_create_figlet, \
                patch.object(ascii_banner_manager, "_AsciiBannerManager__create_frame", return_value = frame_tpl) as mocked_create_frame:

            # Act
            actual : str = ascii_banner_manager.create(version = version)

            # Assert
            mocked_validate.assert_called_once_with(version)
            mocked_create_figlet.assert_called_once()
            mocked_create_frame.assert_called_once_with(version, max_lenght)

            self.assertIn("top_border", actual)
            self.assertIn("ascii_art", actual)
            self.assertIn("bottom_border", actual)
class APFactoryTestCase(unittest.TestCase):

    def test_create_shouldreturnexpectedargumentparser_wheninvoked(self) -> None:

        # Arrange
        # Act
        argument_parser : ArgumentParser = APFactory().create()

        # Assert
        self.assertIsInstance(argument_parser, ArgumentParser)

        arguments : list[str] = []
        for action in argument_parser._actions:
            arguments.extend(action.option_strings)

        self.assertIn("--file_path", arguments)
        self.assertIn("--exclude", arguments)
    def test_create_shouldraiseerror_whenrequiredruntimeargumentismissing(self):

        # Arrange
        args_list : list[str] = CLISTRING.OPTION_FILEPATH_FLAGS
        argument_parser : ArgumentParser = APFactory().create()

        # Act, Assert
        with patch("sys.stderr", new_callable = StringIO):
            with self.assertRaises(SystemExit):
                argument_parser.parse_args(args_list)
class CLIManagerTestCase(unittest.TestCase):                

    def test_runandlog_shouldlogexceptionmessage_whenexceptionisraised(self):

        # Arrange
        expected : str = "Unexpected Error"
        ap_factory : MagicMock = MagicMock(spec = APFactory)
        ap_factory.create.side_effect = Exception(expected)
        
        logging_function : MagicMock = MagicMock()
        
        cli_manager : CLIManager = CLIManager(
            ap_factory = ap_factory,
            logging_function = logging_function
        )

        # Act
        cli_manager.run_and_log()

        # Assert
        logging_function.assert_any_call(expected)
    def test_runandlog_shoulddonothing_whensystemexitoccurs(self):

        # Arrange
        ap_factory : MagicMock = MagicMock(spec = APFactory)
        ap_factory.create.side_effect = SystemExit()
        
        logging_function : MagicMock = MagicMock()
        
        cli_manager : CLIManager = CLIManager(
            ap_factory = ap_factory,
            logging_function = logging_function
        )

        # Act
        cli_manager.run_and_log()

        # Assert
        calls : list[Any] = logging_function.call_args_list

        for call in calls:
            self.assertNotIsInstance(call.args[0], SystemExit)
    
    @parameterized.expand([
        ("example.py", []),
        ("example.py", ["get"])
    ])
    def test_runandlog_shouldcallexpectedmethods_wheninvoked(self, file_path : str, exclude : list[str]) -> None:

        # Arrange
        args : Namespace = Namespace(file_path = file_path, exclude = exclude)
        missing : list[str] = ["SomeClass.get_data"]

        argument_parser : MagicMock = MagicMock(spec = ArgumentParser)
        argument_parser.parse_args.return_value = args

        ap_factory : MagicMock = MagicMock(spec = APFactory)
        ap_factory.create.return_value = argument_parser

        docstring_checker : MagicMock = MagicMock(spec = DocStringChecker)
        docstring_checker.run.return_value = missing

        cli_manager : CLIManager = CLIManager(
            ap_factory = ap_factory,
            docstring_checker = docstring_checker
        )

        # Act
        with patch.object(cli_manager, "_CLIManager__log_ascii_banner") as log_ascii_banner, \
             patch.object(cli_manager, "_CLIManager__log_namespace") as log_namespace, \
             patch.object(cli_manager, "_CLIManager__log_docstrings") as log_docstrings:

            cli_manager.run_and_log()

            # Assert
            log_ascii_banner.assert_called_once()
            ap_factory.create.assert_called_once()
            argument_parser.parse_args.assert_called_once()
            log_namespace.assert_called_once_with(args)
            docstring_checker.run.assert_called_once_with(file_path = file_path)
            log_docstrings.assert_called_once_with(missing)

# MAIN
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)