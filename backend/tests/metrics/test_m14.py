#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'LAB average and standard deviation' metric (m14).
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
from aim.metrics.m14.m14_lab_avg_std import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-05-25"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        ("black.png", [0, 0, 0, 0, 0, 0]),
        (
            "white_50_black_50.png",
            [50.0, 50.0, -0.001227, 0.001227, 0.002327, 0.002327],
        ),
        (
            "aalto.fi_website.png",
            [71.31528, 29.834743, 2.38476, 11.358011, 18.279885, 27.783723],
        ),
    ],
)
def test_lab_avg_std_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test LAB average and standard deviation (desktop GUIs).

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
