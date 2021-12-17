#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions for tests.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import pathlib

# First-party modules
from aim.common import image_utils
from tests.common.constants import DATA_TESTS_EXPECTED_RESULTS_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-12-11"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.1"


# ----------------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------------


def load_expected_result(filename: str) -> str:
    """
    Load an expected result (image) from a file.

    Args:
        filename: Input image file name

    Returns:
        Image encoded in Base64
    """
    # Build expected result file path
    expected_result_filepath: pathlib.Path = (
        pathlib.Path(DATA_TESTS_EXPECTED_RESULTS_DIR) / filename
    )

    # Read expected result
    expected_result_base64: str = image_utils.read_image(
        expected_result_filepath
    )

    return expected_result_base64
