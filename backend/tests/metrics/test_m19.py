#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Average number of colors per dynamic cluster' metric (m19).
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
from aim.metrics.m19.m19_avg_num_colors_per_dynamic_cluster import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-06-09"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        ("white_50_black_50.png", [0]),
        ("red_with_6_yellow_pixels.png", [0]),
        ("aalto.fi_website.png", [18]),
        ("wikipedia.org_website.png", [12]),
    ],
)
def test_avg_num_colors_per_dynamic_cluster_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test Average number of colors per dynamic cluster metric (desktop GUIs).
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
    if (
        result is not None
        and isinstance(result[0], int)
    ):
        assert result == expected_results
