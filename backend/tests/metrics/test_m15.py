#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Colorfulness (Hasler and Süsstrunk)' metric (m15).
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
from aim.metrics.m15.m15_colorfulness_hassler_susstrunk import Metric
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
        ("black.png", [0.0]),
        ("gray.png", [0.0],),
        ("4_low-contrast_shades_of_gray.png", [0.0],),
        ("white_50_black_50.png", [0.0],),
        ("4_high-contrast_shades_of_gray.png", [0.0],),
        ("black_50_transparent_50.png", [0.0],),
        ("white.png", [0.0],),
        ("blue.png", [76.5],),
        ("green.png", [85.5296],),
        ("red.png", [85.5296],),
        ("red_50_green_50.png", [293.25], ),
        ("green_50_blue_50.png", [272.618694],),
        ("blue_50_red_50.png", [272.618694],),
        ("myhelsinki.fi_website.png", [63.443773],),
        ("aalto.fi_website.png", [83.143299],),
    ],
)
def test_colorfulness_hassler_susstrunk_desktop(
        input_value: str, expected_results: List[Any]
) -> None:
    """
    Test colorfulness (Hasler and Süsstrunk) (desktop GUIs).

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
