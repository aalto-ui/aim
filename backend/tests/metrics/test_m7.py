#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'PNG file size' metric (m1).
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
from aim.metrics.m7.m7_subband_entropy import Metric
from tests.common.constants import DATA_TESTS_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2021-08-28"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_result"],
    [
        ("aalto.fi_website.png", [3.2021]),
        ("myhelsinki.fi_website.png", [3.7556]),
        ("wikipedia.org_website.png", [3.6787]),
    ],
)
def test_subband_entropy_desktop(
    input_value: str, expected_result: List[Any]
) -> None:
    """
    Test PNG file size (desktop GUIs).

    Args:
        input_value: GUI image file name
        expected_result: Expected result (list of measures)
    """
    # Build GUI image file path
    gui_image_filepath: pathlib.Path = (
        pathlib.Path(DATA_TESTS_DIR) / input_value
    )

    # Read GUI image (PNG)
    gui_image_png_base64: str = image_utils.read_image(gui_image_filepath)

    # Execute metric
    result: Optional[List[Union[int, float, str]]] = Metric.execute_metric(
        gui_image_png_base64
    )

    # Test result
    if result is not None:
        assert result[0].round(decimals=4) == expected_result[0]
