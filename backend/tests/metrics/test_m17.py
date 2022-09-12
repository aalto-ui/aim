#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Distinct values of Hue, Saturation, and Value' metric (m17).
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
from aim.metrics.m17.m17_distinct_hsv_values import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-06-15"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        ("red.png", [1, 1, 1]),
        ("4_high-contrast_shades_of_gray.png", [1, 1, 4]),
        (
            "green_50_blue_50.png",
            [2, 1, 1],
        ),
    ],
)
def test_distinct_hsv_values_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test Distinct values of Hue, Saturation, and Value (desktop GUIs).

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
    if result is not None and all(isinstance(i, int) for i in result):
        assert result == expected_results
