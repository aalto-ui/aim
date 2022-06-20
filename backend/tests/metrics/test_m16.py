#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'HSV Average and Standard Derivation' metric (m16).
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
from aim.metrics.m16.m16_hsv_avg_std import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-05-26"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        ("black.png", [0, 0, 0, 0, 0]),
        (
            "white_50_black_50.png",
            [0.0, 0.0, 0.0, 0.5, 0.5],
        ),
        ("red.png", [0.0, 1.0, 0.0, 1.0, 0.0]),
        ("blue.png", [239.333333, 1.0, 0.0, 1.0, 0.0]),
        ("green.png", [119.666667, 1.0, 0.0, 1.0, 0.0]),
        ("green_50_blue_50.png", [179.5, 1.0, 0.0, 1.0, 0.0]),
        (
            "aalto.fi_website.png",
            [26.772276, 0.350224, 0.336497, 0.767209, 0.286625],
        ),
    ],
)
def test_hsv_avg_std_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test HSV Average and Standard Derivation (desktop GUIs).

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
    if result is not None and all(isinstance(i, float) for i in result):
        assert [round(float(i), 6) for i in result] == expected_results
