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
    def test_getmissingdocstrings_shouldexcludemethods_whenexcludelistisprovided(self) -> None:

        # Arrange
        source : str = "\n".join([
            "class SomeClass:",
            "    def documented(self):",
            "        pass",
            "",
            "    def undocumented(self):",
            "        pass"
        ])
        exclude : list[str] = ["un"]
        expected : list[str] = ["SomeClass.documented"]

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

    def test_run_should_return_missing_docstrings_when_file_exists(self) -> None:

        # Arrange
        file_path : str = "exists.py"
        source : str = (
            "class A:\n"
            "    def b(self):\n"
            "        pass"
        )
        expected : list[str] = ["A.b"]
        checker : DocStringChecker = DocStringChecker()

        # Act
        with patch("os.path.isfile") as mock_isfile:
            mock_isfile.return_value = True
            with patch("builtins.open", mock_open(read_data = source)):
                actual : list[str] = checker.run(file_path = file_path)

        # Assert
        self.assertEqual(expected, actual)

# MAIN
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)