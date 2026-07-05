# GLOBAL MODULES
import os
import sys
import unittest
from argparse import ArgumentParser, Namespace
from io import StringIO
from parameterized import parameterized
from subprocess import CompletedProcess
from typing import Any, Optional
from unittest.mock import MagicMock, Mock, patch

# LOCAL MODULES
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwdocstringchecking import DocStringChecker
from nwdocstringcheckingcli import CLISTRING, _MessageCollection, _MessageCollectionCLIManager, APFactory
from nwdocstringcheckingcli import AsciiBannerManager, CLIManager, CLIValidator, TerminalWindowManager

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
    def test_createstandard_shouldcallexpectedprivatemethodsandreturnbanner_wheninvoked(self) -> None:

        # Arrange
        ascii_banner_manager : AsciiBannerManager = AsciiBannerManager()
        version : str = "1.0.1"
        max_lenght : int = 65
        
        figlet_tpl : tuple = ("ascii_art", max_lenght)
        frame_tpl : tuple = ("top_border", "bottom_border")

        with patch.object(ascii_banner_manager, "_AsciiBannerManager__validate") as validate, \
                patch.object(ascii_banner_manager, "_AsciiBannerManager__create_figlet", return_value = figlet_tpl) as create_figlet, \
                patch.object(ascii_banner_manager, "_AsciiBannerManager__create_frame", return_value = frame_tpl) as create_frame:

            # Act
            actual : str = ascii_banner_manager.create_standard(version = version)

            # Assert
            validate.assert_called_once_with(version)
            create_figlet.assert_called_once()
            create_frame.assert_called_once_with(version, max_lenght)

            self.assertIn("top_border", actual)
            self.assertIn("ascii_art", actual)
            self.assertIn("bottom_border", actual)
    def test_createmini_shouldcallexpectedprivatemethodsandreturnminibanner_wheninvoked(self) -> None:

        # Arrange
        ascii_banner_manager : AsciiBannerManager = AsciiBannerManager()
        version : str = "1.0.1"
        expected : str = os.linesep.join([
            "***************",
            "* NWDS v1.0.1 *",
            "***************",
            ""
        ])

        with patch.object(ascii_banner_manager, "_AsciiBannerManager__validate") as validate:

            # Act
            actual : str = ascii_banner_manager.create_mini(version = version)

            # Assert
            validate.assert_called_once_with(version)
            self.assertEqual(expected, actual)
    def test_create_shouldreturnstandardbanner_whenterminalwidthisgreaterthanorequaltomaxlength(self) -> None:

        # Arrange
        ascii_banner_manager : AsciiBannerManager = AsciiBannerManager()
        version : str = "1.0.1"
        terminal_width : int = 80
        max_length : int = 54
        figlet_tpl : tuple = ("ascii_art", max_length)
        expected_banner : str = "standard_banner"

        with patch.object(ascii_banner_manager, "_AsciiBannerManager__create_figlet", return_value = figlet_tpl) as create_figlet, \
                patch.object(ascii_banner_manager, "create_standard", return_value = expected_banner) as create_standard:

            # Act
            actual : str = ascii_banner_manager.create(version = version, terminal_width = terminal_width)

            # Assert
            create_figlet.assert_called_once()
            create_standard.assert_called_once_with(version)
            self.assertEqual(expected_banner, actual)
    def test_create_shouldreturnminibanner_whenterminalwidthislessthanmaxlength(self) -> None:

        # Arrange
        ascii_banner_manager : AsciiBannerManager = AsciiBannerManager()
        version : str = "1.0.1"
        terminal_width : int = 40
        max_length : int = 54
        figlet_tpl : tuple = ("ascii_art", max_length)
        expected_banner : str = "mini_banner"

        with patch.object(ascii_banner_manager, "_AsciiBannerManager__create_figlet", return_value = figlet_tpl) as create_figlet, \
                patch.object(ascii_banner_manager, "create_mini", return_value = expected_banner) as create_mini:

            # Act
            actual : str = ascii_banner_manager.create(version = version, terminal_width = terminal_width)

            # Assert
            create_figlet.assert_called_once()
            create_mini.assert_called_once_with(version)
            self.assertEqual(expected_banner, actual)
class TerminalWindowManagerTestCase(unittest.TestCase):

    def test_defaultshutilwidthfunction_shouldreturncolumns_whenshutilissuccessful(self) -> None:

        # Arrange
        expected : int = 80

        with patch("shutil.get_terminal_size") as get_terminal_size:

            get_terminal_size.return_value = os.terminal_size((expected, 24))

            # Act
            actual : Optional[int] = TerminalWindowManager.default_shutil_width_function()

            # Assert
            self.assertEqual(actual, expected)
    def test_defaultshutilwidthfunction_shouldreturnnone_whenexceptionisraised(self) -> None:

        # Arrange
        with patch("nwdocstringcheckingcli.get_terminal_size", side_effect = Exception("Error")):

            # Act
            actual : Optional[int] = TerminalWindowManager.default_shutil_width_function()

            # Assert
            self.assertIsNone(actual)
    
    def test_defaultsttywidthfunction_shouldreturnwidth_whensttyissuccessful(self) -> None:

        # Arrange
        expected : int = 100

        process : Mock = Mock(spec = CompletedProcess)
        process.stdout = f"  {expected}  \n"
        
        with patch("subprocess.run", return_value = process) as mock_run:

            # Act
            actual : Optional[int] = TerminalWindowManager.default_stty_width_function()

            # Assert
            mock_run.assert_called_once_with(
                ["/bin/sh", "-c", "stty size | cut -d' ' -f2"],
                capture_output = True,
                text = True,
                check = False,
            )
            self.assertEqual(actual, expected)
    def test_defaultsttywidthfunction_shouldreturnnone_whensttyreturnsnegative(self) -> None:

        # Arrange
        process : Mock = Mock(spec = CompletedProcess)
        process.stdout = "-10\n"
        
        with patch("subprocess.run", return_value = process):

            # Act
            actual_width : Optional[int] = TerminalWindowManager.default_stty_width_function()

            # Assert
            self.assertIsNone(actual_width)
    def test_defaultsttywidthfunction_shouldreturnnone_whenexceptionisraised(self) -> None:

        # Arrange
        with patch("subprocess.run", side_effect = Exception("Error")):

            # Act
            actual_width : Optional[int] = TerminalWindowManager.default_stty_width_function()

            # Assert
            self.assertIsNone(actual_width)

    def test_init_shouldassignprovidedfunctions_wheninvokedwitharguments(self) -> None:

        # Arrange
        shutil_width_function : Mock = Mock()
        stty_width_function : Mock = Mock()

        # Act
        tw_manager : TerminalWindowManager = TerminalWindowManager(
            shutil_width_function = shutil_width_function,
            stty_width_function = stty_width_function
        )

        # Assert
        self.assertEqual(tw_manager._TerminalWindowManager__shutil_width_function, shutil_width_function)   # type: ignore
        self.assertEqual(tw_manager._TerminalWindowManager__stty_width_function, stty_width_function)       # type: ignore
    def test_init_shouldassigndefaultfunctions_wheninvokedwithoutarguments(self) -> None:

        # Arrange
        tw_manager : TerminalWindowManager = TerminalWindowManager()

        # Assert
        self.assertEqual(tw_manager._TerminalWindowManager__shutil_width_function, TerminalWindowManager.default_shutil_width_function) # type: ignore
        self.assertEqual(tw_manager._TerminalWindowManager__stty_width_function, TerminalWindowManager.default_stty_width_function)     # type: ignore

    def test_getorcutoff_shouldreturnshutilwidth_whenshutilissuccessful(self) -> None:

        # Arrange
        expected : int = 120
        shutil_width_function : Mock = Mock(return_value = expected)
        stty_width_function : Mock = Mock()
        
        tw_manager : TerminalWindowManager = TerminalWindowManager(
            shutil_width_function = shutil_width_function,
            stty_width_function = stty_width_function
        )

        # Act
        actual : int = tw_manager.get_or_cutoff()

        # Assert
        self.assertEqual(actual, expected)
        shutil_width_function.assert_called_once()
        stty_width_function.assert_not_called()
    def test_getorcutoff_shouldreturnsttywidth_whenshutilfailsandsttyissuccessful(self) -> None:

        # Arrange
        expected : int = 90
        shutil_width_function : Mock = Mock(return_value = None)
        stty_width_function : Mock = Mock(return_value = expected)
        
        tw_manager : TerminalWindowManager = TerminalWindowManager(
            shutil_width_function = shutil_width_function,
            stty_width_function = stty_width_function
        )

        # Act
        actual : int = tw_manager.get_or_cutoff()

        # Assert
        self.assertEqual(actual, expected)
        shutil_width_function.assert_called_once()
        stty_width_function.assert_called_once()
    def test_getorcutoff_shouldreturncutoffwidth_whenbothfunctionsfail(self) -> None:

        # Arrange
        shutil_width_function : Mock = Mock(return_value = None)
        stty_width_function : Mock = Mock(return_value = None)
        
        tw_manager : TerminalWindowManager = TerminalWindowManager(
            shutil_width_function = shutil_width_function,
            stty_width_function = stty_width_function
        )

        # Act
        actual : int = tw_manager.get_or_cutoff()

        # Assert
        self.assertEqual(actual, TerminalWindowManager.cutoff_width)
        shutil_width_function.assert_called_once()
        stty_width_function.assert_called_once()
class CLIValidatorTestCase(unittest.TestCase):

    def test_validatefilepath_shouldreturnfilepath_whenvalidfilepath(self) -> None:

        # Arrange
        file_path : str = "valid_file.py"

        # Act
        with patch("nwdocstringchecking.Validator.validate_file_path") as validate_file_path:
            validate_file_path.return_value = None
            actual : str = CLIValidator().validate_file_path(file_path = file_path)

        # Assert
        self.assertEqual(file_path, actual)
    def test_validatefilepath_shouldraiseexception_wheninvalidfilepath(self) -> None:

        # Arrange
        file_path : str = "invalid_file.py"
        message : str = "The provided 'file_path' doesn't exist: 'invalid_file.py'."

        # Act, Assert
        with patch("nwdocstringchecking.Validator") as validator_class:
            validator_instance = validator_class.return_value
            validator_instance.validate_file_path.side_effect = Exception(message)
            
            with self.assertRaises(Exception) as context:
                CLIValidator().validate_file_path(file_path = file_path)
            
            self.assertEqual(message, str(context.exception))
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

    def test_logdocstrings_shouldlogeachmethod_whenmissinglistisnotempty(self) -> None:

        # Arrange
        missing : list[str] = ["ClassA.method_one", "ClassB.method_two"]
        logging_function : MagicMock = MagicMock()
        cli_manager : CLIManager = CLIManager(logging_function = logging_function)

        # Act
        cli_manager._CLIManager__log_docstrings(missing = missing) # type: ignore

        # Assert
        self.assertEqual(logging_function.call_count, 2)
        logging_function.assert_any_call("ClassA.method_one")
        logging_function.assert_any_call("ClassB.method_two")
    def test_logdocstrings_shouldlogsuccessmessage_whenmissinglistisempty(self) -> None:

        # Arrange
        missing : list[str] = []
        expected : str = _MessageCollectionCLIManager.all_methods_have_docstrings()
        logging_function : MagicMock = MagicMock()
        cli_manager : CLIManager = CLIManager(logging_function = logging_function)

        # Act
        cli_manager._CLIManager__log_docstrings(missing = missing) # type: ignore

        # Assert
        logging_function.assert_called_once_with(expected)
    def test_lognamespace_shouldlogallarguments_wheninvoked(self) -> None:

        # Arrange
        args : Namespace = Namespace(file_path = "test.py", exclude = ["test_"])
        logging_function : MagicMock = MagicMock()
        cli_manager : CLIManager = CLIManager(logging_function = logging_function)

        # Act
        cli_manager._CLIManager__log_namespace(args = args) # type: ignore

        # Assert
        self.assertEqual(logging_function.call_count, 3)
        logging_function.assert_any_call("file_path: 'test.py'")
        logging_function.assert_any_call("exclude: '['test_']'")
        logging_function.assert_any_call("")

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
            docstring_checker.run.assert_called_once_with(file_path = file_path, exclude = exclude)
            log_docstrings.assert_called_once_with(missing)

# MAIN
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)