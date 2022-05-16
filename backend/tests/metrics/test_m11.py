#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Static Clusters' metric (m11).
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
from aim.metrics.m11.m11_static_clusters import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-05-16"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        ("white_50_black_50.png", [2]),
        ("red_with_6_yellow_pixels.png", [2]),
        ("red_with_5_yellow_pixels.png", [1]),
        ("red_with_4_yellow_pixels.png", [1]),
    ],
)
def test_static_clusters_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test static clusters metric (desktop GUIs).
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
    if result is not None and isinstance(result[0], int):
        assert result[0] == expected_results[0]
