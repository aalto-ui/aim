#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Dynamic Clusters' metric (m12).
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
from aim.metrics.m12.m12_dynamic_clusters import Metric
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
        ("white_50_black_50.png", [0, 0]),
        ("red_with_6_yellow_pixels.png", [0, 0]),
        ("red_with_5_yellow_pixels.png", [0, 0]),
        ("COCO_val2014_000000001700.png", [378, 16]),
        ("aalto.fi_website.png", [681, 16]),
        ("wikipedia.org_website.png", [94, 12]),
    ],
)
def test_dynamic_clusters_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test dynamic clusters metric (desktop GUIs).
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
        and isinstance(result[1], int)
    ):
        assert result == expected_results
