#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Quadtree decomposition' metric (m27).
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
from aim.metrics.m27.m27_quadtree_decomposition import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR, IDIFF_TOLERANCE
from tests.common.utils import load_expected_result

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2023-01-01"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        ("blue.png", [0.333333, 0.56664, 0.959375, 16]),
        (
            "duckduckgo.com.png",
            [
                0.372068,
                0.473168,
                0.997173,
                230,
                load_expected_result("m27_1_duckduckgo.com.png"),
                load_expected_result("m27_2_duckduckgo.com.png"),
            ],
        ),
    ],
)
def test_duadtree_decomposition_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test Quadtree decomposition (desktop GUIs).

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
        and isinstance(result[0], float)
        and isinstance(result[1], float)
        and isinstance(result[2], float)
        and isinstance(result[3], int)
        and isinstance(result[4], str)
        and isinstance(result[5], str)
    ):

        assert [round(float(r), 6) for r in result[:4]] == expected_results[:4]

        if len(expected_results) == 5:
            assert (
                image_utils.idiff(result[4], expected_results[3])
                <= IDIFF_TOLERANCE
            )
            assert (
                image_utils.idiff(result[5], expected_results[4])
                <= IDIFF_TOLERANCE
            )
