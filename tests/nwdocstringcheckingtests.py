# GLOBAL MODULES
import unittest
from unittest.mock import Mock, mock_open, patch
from argparse import ArgumentParser, Namespace
from parameterized import parameterized
from typing import Callable, Optional, Tuple

# LOCAL MODULES
import sys, os
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwdocstringchecking import _MessageCollection, APFactory, APAdapter, DocStringManager, DocStringChecker

# SUPPORT METHODS
# TEST CLASSES
import unittest

# SUPPORT METHODS
# TEST CLASSES
class MessageCollectionTestCase(unittest.TestCase):

    def test_parserdescription_shouldreturnexpectedmessage_wheninvoked(self):

        # Arrange
        expected : str = "Checks if all methods in a Python file have docstrings."

        # Act
        actual : str = _MessageCollection.parser_description()

        # Assert
        self.assertEqual(expected, actual)
    def test_filepathtothepythonfile_shouldreturnexpectedmessage_wheninvoked(self):

        # Arrange
        expected : str = "The file path to the Python file to check docstrings for."

        # Act
        actual : str = _MessageCollection.file_path_to_the_python_file()

        # Assert
        self.assertEqual(expected, actual)
    def test_excludesubstrings_shouldreturnexpectedmessage_wheninvoked(self):

        # Arrange
        expected : str = "One or multiple substrings to exclude from the output."

        # Act
        actual : str = _MessageCollection.exclude_substrings()

        # Assert
        self.assertEqual(expected, actual)
    def test_allmethodshavedocstrings_shouldreturnexpectedmessage_wheninvoked(self):

        # Arrange
        expected : str = "All methods have docstrings."

        # Act
        actual : str = _MessageCollection.all_methods_have_docstrings()

        # Assert
        self.assertEqual(expected, actual)
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
        self.assertIn("-fp", arguments)
        self.assertIn("--exclude", arguments)
        self.assertIn("-e", arguments)
class APAdapterTestCase(unittest.TestCase):

    @parameterized.expand([
        ("nwsomething.py", ["_MessageCollection", "__init__"], ("nwsomething.py", ["_MessageCollection", "__init__"])),
        (None, [], (None, []))
    ])
    def test_parseargs_shouldreturnexpectedtuple_wheninvoked(
        self, 
        file_path : Optional[str], 
        exclude : list[str], 
        expected : Tuple[Optional[str], list[str]]) -> None:

        # Arrange
        argument_parser : ArgumentParser = ArgumentParser()
        argument_parser.add_argument("--file_path", "-fp", required = True)
        argument_parser.add_argument("--exclude", "-e", required = False, action = "append", default = [])
        argument_parser.parse_args = Mock(return_value = Namespace(file_path = file_path, exclude = exclude))

        ap_factory : Mock = Mock()
        ap_factory.create = Mock(return_value = argument_parser)

        # Act
        ap_adapter : APAdapter = APAdapter(ap_factory = ap_factory)
        actual : Tuple[Optional[str], list[str]] = ap_adapter.parse_args()

        # Assert
        self.assertEqual(expected, actual)
class DocStringManagerTestCase(unittest.TestCase):

    def test_loadsource_shouldreturnexpectedsourcecode_whenfileisread(self) -> None:

        # Arrange
        source : str = "class Example:\n    def method(self):\n        pass"
        file_path : str = "dummy.py"

        # Act
        with patch("builtins.open", mock_open(read_data = source)) as mocked_file:
            actual : str = DocStringManager().load_source(file_path = file_path)

        # Assert
        self.assertEqual(source, actual)
        mocked_file.assert_called_once_with(file_path, "r", encoding = "utf-8")
    def test_getmissingdocstrings_shouldreturnmethodswithoutdocstrings_whenmissingdocstrings(self) -> None:

        # Arrange
        source : str = "\n".join([
            "class SomeClass:",
            "    def documented(self):",
            "        '''Docstring'''",
            "        pass",
            "",
            "    def undocumented(self):",
            "        pass"
        ])
        exclude : list[str] = []
        expected : list[str] = ["SomeClass.undocumented"]

        # Act
        actual : list[str] = DocStringManager().get_missing_docstrings(source = source, exclude = exclude)

        # Assert
        self.assertEqual(expected, actual)
    def test_logdocstrings_shouldlogexpectedmethodnames_whenmissingdocstrings(self) -> None:

        # Arrange
        logging_function : Mock = Mock()
        missing : list[str] = ["SomeClass.method1", "SomeClass.method2"]
        
        # Act
        ds_manager : DocStringManager = DocStringManager(logging_function = logging_function)
        ds_manager.log_docstrings(missing = missing)

        # Assert
        for method in missing:
            logging_function.assert_any_call(method)
    def test_logdocstrings_shouldlogallmethodshavedocstrings_whennomissingdocstrings(self) -> None:

        # Arrange
        logging_function : Mock = Mock()
        missing : list[str] = []
        expected : str = _MessageCollection.all_methods_have_docstrings()
        
        # Act
        ds_manager : DocStringManager = DocStringManager(logging_function = logging_function)
        ds_manager.log_docstrings(missing = missing)

        # Assert
        logging_function.assert_called_once_with(expected)
class DocStringCheckerTestCase(unittest.TestCase):

    def test_run_shouldcallexitfunction_whenfilepathisnone(self) -> None:

        # Arrange
        ap_adapter : APAdapter = Mock()
        ap_adapter.parse_args.return_value = (None, [])

        ds_manager : DocStringManager = Mock()
        exit_function : Callable[[], None] = Mock()

        ds_checker : DocStringChecker = DocStringChecker(
            ap_adapter = ap_adapter,
            ds_manager = ds_manager,
            exit_function = exit_function
        )

        # Act
        ds_checker.run()

        # Assert
        exit_function.assert_called_once()
    def test_run_shouldcalldependencymethods_wheninvoked(self) -> None:

        # Arrange
        file_path : str = "nwsomething.py"
        exclude : list[str] = ["__init__"]
        source : str = "Some source code"
        missing : list[str] = ["SomeClass.undocumented"]

        ap_adapter : APAdapter = Mock()
        ap_adapter.parse_args.return_value = (file_path, exclude)

        ds_manager : DocStringManager = Mock()
        ds_manager.load_source.return_value = source
        ds_manager.get_missing_docstrings.return_value = missing

        exit_function : Callable[[], None] = Mock()

        ds_checker : DocStringChecker = DocStringChecker(
            ap_adapter = ap_adapter,
            ds_manager = ds_manager,
            exit_function = exit_function
        )

        # Act
        ds_checker.run()

        # Assert
        ds_manager.load_source.assert_called_once_with(file_path = file_path)
        ds_manager.get_missing_docstrings.assert_called_once_with(source = source, exclude = exclude)
        ds_manager.log_docstrings.assert_called_once_with(missing = missing)