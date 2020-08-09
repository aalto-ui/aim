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
__date__ = "2020-08-05"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


class TestPythonVersion:
    """
    A test class for the Python version.
    """

    # Public methods
    def test_major(self) -> None:
        """
        Test Python major version.
        """
        assert sys.version_info.major == 3

    def test_minor(self) -> None:
        """
        Test Python minor version.
        """
        assert sys.version_info.minor == 7
