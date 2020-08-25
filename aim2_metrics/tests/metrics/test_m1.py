#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'PNG file size' metric (m1).
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import pathlib
from typing import Any, List, Optional

# Third-party modules
import pytest

# First-party modules
import aim.core.utils as aim_utils
from aim.metrics.m1_png_file_size import Metric1
from tests.core.constants import DATA_TESTS_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2020-08-25"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_result"],
    [
        ("aalto.fi_website.png", [898817]),
        ("myhelsinki.fi_website.png", [1410433]),
        ("wikipedia.org_website.png", [352787]),
    ],
)
def test_png_file_size_desktop(
    input_value: str, expected_result: List[Any]
) -> None:
    """
    Test PNG file size (desktop GUIs).

    Args:
        input_value: GUI image file name
        expected_result: Expected result (list of measures)
    """
    # Build GUI image file path
    gui_image_filepath: pathlib.Path = pathlib.Path(
        DATA_TESTS_DIR
    ) / input_value

    # Read GUI image (PNG)
    gui_image_png_base64: str = aim_utils.read_image(gui_image_filepath)

    # Execute metric
    result: Optional[List[Any]] = Metric1.execute_metric(gui_image_png_base64)

    # Test result
    if result is not None:
        assert result[0] == expected_result[0]
