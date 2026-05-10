# GLOBAL MODULES
import unittest
from unittest.mock import mock_open, patch

# LOCAL MODULES
import sys, os
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwdocstringchecking import DocStringChecker

# SUPPORT METHODS
# TEST CLASSES
class DocStringCheckerTestCase(unittest.TestCase):

    def test_loadsource_shouldreturnexpectedsourcecode_whenfileisread(self) -> None:

        # Arrange
        source : str = "class Example:\n    def method(self):\n        pass"
        file_path : str = "dummy.py"

        # Act
        with patch("builtins.open", mock_open(read_data = source)) as mocked_file:
            actual : str = DocStringChecker()._DocStringChecker__load_source(file_path = file_path) # type: ignore

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
        actual : list[str] = DocStringChecker()._DocStringChecker__get_missing_docstrings(source = source, exclude = exclude) # type: ignore

        # Assert
        self.assertEqual(expected, actual)

# MAIN
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)