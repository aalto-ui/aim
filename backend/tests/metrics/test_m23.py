#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Color blindness' metric (m23).
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
from aim.metrics.m23.m23_color_blindness import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR, IDIFF_TOLERANCE
from tests.common.utils import load_expected_result

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-10-21"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        (
            "myhelsinki.fi_website.png",
            [
                load_expected_result("m23_0_myhelsinki.fi_website.png"),
                load_expected_result("m23_1_myhelsinki.fi_website.png"),
                load_expected_result("m23_2_myhelsinki.fi_website.png"),
            ],
        ),
        (
            "colored_crayons.png",
            [
                load_expected_result("m23_0_colored_crayons.png"),
                load_expected_result("m23_1_colored_crayons.png"),
                load_expected_result("m23_2_colored_crayons.png"),
            ],
        ),
        (
            "rgbspan.png",
            [
                load_expected_result("m23_0_rgbspan.png"),
                load_expected_result("m23_1_rgbspan.png"),
                load_expected_result("m23_2_rgbspan.png"),
            ],
        ),
    ],
)
def test_color_blindness_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test Color blindness (desktop GUIs).

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
