#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'White Space' metric (m22).
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import pathlib
from typing import Any, Dict, List, Optional, Tuple, Union

# Third-party modules
import pytest

# First-party modules
from aim.common import image_utils
from aim.common.constants import GUI_TYPE_DESKTOP, GUI_TYPE_MOBILE
from aim.metrics.m22.m22_white_space import Metric
from aim.segmentation.model import Segmentation
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-08-05"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        ("aalto.fi_website.png", [0.2663]),
        ("myhelsinki.fi_website.png", [0.884]),
        ("wikipedia.org_website.png", [0.3033]),
        ("black.png", [1.0]),
    ],
)
def test_white_space_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test White Space (desktop GUIs).

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

    # Execute segmentation
    result_segments: Dict[str, Any] = Segmentation.execute(
        gui_image=gui_image_png_base64, gui_type=GUI_TYPE_DESKTOP
    )

    # Execute metric
    result: Optional[List[Union[int, float, str]]] = Metric.execute_metric(
        gui_image_png_base64,
        gui_segments=result_segments,
        gui_type=GUI_TYPE_DESKTOP,
    )

    # Test result
    if result is not None and isinstance(result[0], float):
        assert round(result[0], 4) == expected_results[0]
