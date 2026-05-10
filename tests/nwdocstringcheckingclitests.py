# GLOBAL MODULES
import unittest
from unittest.mock import mock_open, patch

# LOCAL MODULES
import sys, os
sys.path.append(os.path.dirname(__file__).replace('tests', 'src'))
from nwdocstringchecking import DocStringChecker

# SUPPORT METHODS
# TEST CLASSES



# MAIN
if __name__ == "__main__":
    result = unittest.main(argv=[''], verbosity=3, exit=False)