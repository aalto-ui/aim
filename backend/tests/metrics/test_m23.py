#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Number of Block Sizes' metric (m23).
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
from aim.metrics.m23.m23_num_block_sizes import Metric
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
        ("interfacemetrics_aalto.png", [26, 20]),
        ("white.png", [0, 0]),
    ],
)
def test_num_block_sizes_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test Number of Block Sizes (desktop GUIs).

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
    result_segments: Dict[str, Any]
    _, result_segments = Segmentation.execute(
        gui_image=gui_image_png_base64, gui_type=GUI_TYPE_DESKTOP
    )

    # Execute metric
    result: Optional[List[Union[int, float, str]]] = Metric.execute_metric(
        gui_image_png_base64,
        gui_segments=result_segments,
        gui_type=GUI_TYPE_DESKTOP,
    )

    # Test result
    if result is not None and all(isinstance(res, int) for res in result):
        assert result == expected_results
