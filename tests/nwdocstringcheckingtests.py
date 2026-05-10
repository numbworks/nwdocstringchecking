# GLOBAL MODULES
import unittest
from unittest.mock import mock_open, patch

# LOCAL MODULES
import sys, os
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwdocstringchecking import _MessageCollection, Validator, DocStringChecker

# SUPPORT METHODS
# TEST CLASSES
class ValidatorTestCase(unittest.TestCase):

    def test_validatefilepath_shouldraiseexceptionwithexpectedmessage_whenfiledoesnotexist(self):

        # Arrange
        file_path : str = r"C:/NonExistentFile.txt"
        expected : str = _MessageCollection.provided_file_path_doesnt_exist(file_path)

        # Act, Assert
        with patch("os.path.isfile", return_value = False):
            with self.assertRaises(Exception) as context:
                Validator.validate_file_path(file_path = file_path)
            
            self.assertEqual(str(context.exception), expected)
    def test_validatefilepath_shoulddonothing_whenfileexists(self):

        # Arrange
        file_path : str = r"C:/Exists.txt"

        # Act, Assert
        with patch("os.path.isfile", return_value = True):
            Validator.validate_file_path(file_path = file_path)
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
    def test_getmissingdocstrings_shouldexcludemethods_whenexcludelistisprovided(self) -> None:

        # Arrange
        source : str = "\n".join([
            "class SomeClass:",
            "    def append(self):",
            "        pass",
            "",
            "    def remove(self):",
            "        pass"
        ])
        exclude : list[str] = ["remove"]
        expected : list[str] = ["SomeClass.append"]

        # Act
        actual : list[str] = DocStringChecker()._DocStringChecker__get_missing_docstrings(source = source, exclude = exclude) # type: ignore

        # Assert
        self.assertEqual(expected, actual)

    def test_run_shouldraiseexception_whenfilepathdoesnotexist(self) -> None:

        # Arrange
        file_path : str = "non_existent.py"

        # Act, Assert
        with patch("os.path.isfile") as isfile:
            isfile.return_value = False
            
            with self.assertRaises(Exception) as context:
                DocStringChecker().run(file_path = file_path)
            
            self.assertIn("The provided 'file_path' doesn't exist", str(context.exception))
    def test_run_shouldreturnmissingdocstrings_whenfileexists(self) -> None:

        # Arrange
        file_path : str = "exists.py"
        source : str = (
            "class SomeClass:\n"
            "    def undocumented(self):\n"
            "        pass"
        )
        expected : list[str] = ["SomeClass.undocumented"]

        # Act
        with patch("os.path.isfile") as isfile:
            isfile.return_value = True

            with patch("builtins.open", mock_open(read_data = source)):
                actual : list[str] = DocStringChecker().run(file_path = file_path)

        # Assert
        self.assertEqual(expected, actual)

# MAIN
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)