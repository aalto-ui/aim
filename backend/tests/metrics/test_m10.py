#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'WAVE (Weighted Affective Valence Estimates)' metric (m10).
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
from aim.metrics.m10.m10_wave import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-05-11"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        ("aalto.fi_website.png", [0.532875]),
        ("myhelsinki.fi_website.png", [0.628527]),
        ("wikipedia.org_website.png", [0.488411]),
        ("blue_light.png", [1.0]),
        ("gold.png", [0.0]),
    ],
)
def test_wave_desktop(input_value: str, expected_results: List[Any]) -> None:
    """
    Test wave metric (desktop GUIs).

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
    if result is not None and isinstance(result[0], float):
        assert round(result[0], 6) == expected_results[0]
