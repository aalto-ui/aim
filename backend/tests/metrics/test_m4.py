#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Contour density' metric (m4).
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
from aim.metrics.m4.m4_contour_density import Metric
from tests.common.constants import DATA_TESTS_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-03-19"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_result"],
    [
        ("aalto.fi_website.png", [0.036322265625]),
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
            [0.00078125],
        ),  # transparent -> white pixels
        ("white_50_black_50.png", [0.00078125]),
        ("red_50_green_50.png", [0.00078125]),
        ("green_50_blue_50.png", [0.00078125]),
        ("blue_50_red_50.png", [0.00078125]),
        ("4_high-contrast_shades_of_gray.png", [0.00234375]),
        ("4_low-contrast_shades_of_gray.png", [0.0]),
    ],
)
def test_contour_density_desktop(
    input_value: str, expected_result: List[Any]
) -> None:
    """
    Test contour density (desktop GUIs).

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
