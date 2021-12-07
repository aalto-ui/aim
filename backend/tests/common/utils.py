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
from typing import List

# First-party modules
from tests.common.constants import DATA_TESTS_EXPECTED_RESULTS_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-12-07"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------------


def load_expected_result_b64(filename: str) -> str:
    """
    Load an expected result (PNG image data encoded in Base64) from a file.

    Args:
        filename: Input file name

    Returns:
        PNG image data encoded in Base64

    Raises:
        ValueError: If PNG image data is not encoded in Base64
    """
    # Build input file path
    input_filepath: pathlib.Path = (
        pathlib.Path(DATA_TESTS_EXPECTED_RESULTS_DIR) / filename
    )

    # Load expected result
    with open(input_filepath, "r") as f:
        data: str = f.read()
        data_parts: List[str] = data.split(",")
        data_format: str = data_parts[0][5:]  # remove scheme 'data:'
        if data_format != "image/png;base64":
            raise ValueError("Data format must be 'image/png;base64'")
        expected_result: str = data_parts[1].strip()

    return expected_result
