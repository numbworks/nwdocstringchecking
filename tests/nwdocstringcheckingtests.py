# GLOBAL MODULES
import unittest
from unittest.mock import Mock
from argparse import ArgumentParser, Namespace
from typing import Callable, Optional, Tuple

# LOCAL MODULES
import sys, os
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwdocstringchecking import _MessageCollection, APFactory, APAdapter

# SUPPORT METHODS
# TEST CLASSES
import unittest

# SUPPORT METHODS
class SupportMethodProvider():

    '''Collection of generic purpose test-aiding methods.'''

    @staticmethod
    def get_args_tuple(
            file_path : Optional[str] = "nwsomething.py", 
            exclude : list[str] = ["_MessageCollection", "__init__"]
        ) -> Tuple[Optional[str], list[str]]:
        return (file_path, exclude)

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
class APAdapterTestCase(unittest.TestCase):

    def test_parseargs_shouldreturnexpectedtuple_wheninvoked(self) -> None:

        # Arrange
        file_path, exclude = SupportMethodProvider().get_args_tuple()
        expected : Tuple[Optional[str], list[str]] = (file_path, exclude)

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