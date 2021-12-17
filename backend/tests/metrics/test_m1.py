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
from typing import Any, List, Optional, Union

# Third-party modules
import pytest

# First-party modules
from aim.common import image_utils
from aim.metrics.m1.m1_png_file_size import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-12-11"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.1"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        ("aalto.fi_website.png", [898817]),
        ("myhelsinki.fi_website.png", [1410433]),
        ("wikipedia.org_website.png", [352787]),
    ],
)
def test_png_file_size_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test PNG file size (desktop GUIs).

    Args:
        input_value: GUI image file name
        expected_results: Expected results (list of measures)
    """
    # Build GUI image file path
    gui_image_filepath: pathlib.Path = (
        pathlib.Path(DATA_TESTS_INPUT_VALUES_DIR) / input_value
    )

    # Read GUI image (PNG)
    gui_image_png_base64: str = image_utils.read_image(gui_image_filepath)

    # Execute metric
    result: Optional[List[Union[int, float, str]]] = Metric.execute_metric(
        gui_image_png_base64
    )

    # Test result
    if result is not None:
        assert result[0] == expected_results[0]
