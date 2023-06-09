#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'MD-EAM' metric (m30).
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
from aim.metrics.m30.m30_mdeam import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR, IDIFF_TOLERANCE
from tests.common.utils import load_expected_result

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine, Yao Wang"
__date__ = "2023-06-08"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        (
            "aalto.fi_website.png",
            [
                load_expected_result("m30_0_aalto.fi_website.png"),
                load_expected_result("m30_1_aalto.fi_website.png"),
                load_expected_result("m30_2_aalto.fi_website.png"),
                load_expected_result("m30_3_aalto.fi_website.png"),
                load_expected_result("m30_4_aalto.fi_website.png"),
                load_expected_result("m30_5_aalto.fi_website.png"),
            ],
        ),
        (
            "myhelsinki.fi_website.png",
            [
                load_expected_result("m30_0_myhelsinki.fi_website.png"),
                load_expected_result("m30_1_myhelsinki.fi_website.png"),
                load_expected_result("m30_2_myhelsinki.fi_website.png"),
                load_expected_result("m30_3_myhelsinki.fi_website.png"),
                load_expected_result("m30_4_myhelsinki.fi_website.png"),
                load_expected_result("m30_5_myhelsinki.fi_website.png"),
            ],
        ),
    ],
)
def test_mdeam_desktop(input_value: str, expected_results: List[Any]) -> None:
    """
    Test MD-EAM (desktop GUIs).

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
        and isinstance(result[0], str)
        and isinstance(result[1], str)
        and isinstance(result[2], str)
        and isinstance(result[3], str)
        and isinstance(result[4], str)
        and isinstance(result[5], str)
    ):
        assert (
            image_utils.idiff(result[0], expected_results[0])
            <= IDIFF_TOLERANCE
        )
        assert (
            image_utils.idiff(result[1], expected_results[1])
            <= IDIFF_TOLERANCE
        )
        assert (
            image_utils.idiff(result[2], expected_results[2])
            <= IDIFF_TOLERANCE
        )
        assert (
            image_utils.idiff(result[3], expected_results[3])
            <= IDIFF_TOLERANCE
        )
        assert (
            image_utils.idiff(result[4], expected_results[4])
            <= IDIFF_TOLERANCE
        )
        assert (
            image_utils.idiff(result[5], expected_results[5])
            <= IDIFF_TOLERANCE
        )
