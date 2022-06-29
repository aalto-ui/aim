#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Color Harmonization' metric (m20).
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
from aim.metrics.m20.m20_color_harmonization import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR, IDIFF_TOLERANCE
from tests.common.utils import load_expected_result

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-06-29"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        ("red.png", [0.0]),
        ("aim_bad_harmony.png", [1246.757656]),
    ],
)
def test_color_harmonization_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test Color Harmonization (desktop GUIs).

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
        and isinstance(result[1], str)
        and isinstance(result[2], str)
    ):
        assert round(result[0], 6) == expected_results[0]
