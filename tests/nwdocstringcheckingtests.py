# GLOBAL MODULES
# LOCAL MODULES
import sys, os
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwdocstringchecking import _MessageCollection

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
