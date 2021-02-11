#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Distinct RGB values' metric (m3).
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
from aim.core import image_utils
from aim.metrics.m3_distinct_rgb_values import Metric
from tests.core.constants import DATA_TESTS_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-02-11"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_result"],
    [
        ("transparent.png", [1]),  # transparent -> white pixels
        ("white.png", [1]),
        ("black.png", [1]),
        ("red.png", [1]),
        ("green.png", [1]),
        ("blue.png", [1]),
        ("white_50_transparent_50.png", [1]),  # transparent -> white pixels
        ("black_50_transparent_50.png", [2]),  # transparent -> white pixels
        ("white_50_black_50.png", [2]),
        ("red_50_green_50.png", [2]),
        ("green_50_blue_50.png", [2]),
        ("blue_50_red_50.png", [2]),
        ("red_33_green_33_blue_34.png", [3]),
        ("white_25_black_25_gray_25_white_25.png", [3]),
        ("4_high-contrast_shades_of_gray.png", [4]),
        ("4_low-contrast_shades_of_gray.png", [4]),
        ("red_with_4_yellow_pixels.png", [1]),  # color reduction
        ("red_with_5_yellow_pixels.png", [1]),  # color reduction
        ("red_with_6_yellow_pixels.png", [2]),  # color reduction
    ],
)
def test_distinct_rgb_values_desktop(
    input_value: str, expected_result: List[Any]
) -> None:
    """
    Test distinct RGB values (desktop GUIs).

    Args:
        input_value: GUI image file name
        expected_result: Expected result (list of measures)
    """
    # Build GUI image file path
    gui_image_filepath: pathlib.Path = (
        pathlib.Path(DATA_TESTS_DIR) / input_value
    )

    # Read GUI image (PNG)
    gui_image_png_base64: str = image_utils.read_image(gui_image_filepath)

    # Execute metric
    result: Optional[List[Union[int, float, str]]] = Metric.execute_metric(
        gui_image_png_base64
    )

    # Test result
    if result is not None:
        assert result[0] == expected_result[0]
