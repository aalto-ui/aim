#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the Python version.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import sys

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2020-08-21"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


class TestPythonVersion:
    """
    A test class for the Python version.
    """

    # Constants
    PYTHON_VERSION_MAJOR: int = 3
    PYTHON_VERSION_MINOR: int = 7

    # Public methods
    def test_major(self) -> None:
        """
        Test Python major version.
        """
        assert sys.version_info.major == self.PYTHON_VERSION_MAJOR

    def test_minor(self) -> None:
        """
        Test Python minor version.
        """
        assert sys.version_info.minor == self.PYTHON_VERSION_MINOR
