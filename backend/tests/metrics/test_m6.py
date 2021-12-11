#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Contour congestion' metric (m6).
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
from aim.metrics.m6.m6_contour_congestion import Metric
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
        ("aalto.fi_website.png", [0.5822306238185255]),
        ("transparent.png", [0.0]),  # transparent -> white pixels
        ("white.png", [0.0]),
        ("black.png", [0.0]),
        ("gray.png", [0.0]),
        ("red.png", [0.0]),
        ("green.png", [0.0]),
        ("blue.png", [0.0]),
        (
            "white_50_transparent_50.png",
            [0.0],
        ),  # transparent -> white pixels
        (
            "black_50_transparent_50.png",
            [0.0],
        ),  # transparent -> white pixels
        ("white_50_black_50.png", [0.0]),
        ("red_50_green_50.png", [0.0]),
        ("green_50_blue_50.png", [0.0]),
        ("blue_50_red_50.png", [0.0]),
        ("4_high-contrast_shades_of_gray.png", [0.0]),
        ("4_low-contrast_shades_of_gray.png", [0.0]),
        ("10_black_stripes_20px_margin.png", [0.0]),
        ("3_black_stripes_19px_margin.png", [0.0]),
        ("2_narrow_black_stripes_19px_margin.png", [0.5]),
    ],
)
def test_contour_congestion_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test contour congestion (desktop GUIs).

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
