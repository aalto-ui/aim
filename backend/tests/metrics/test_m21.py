#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Grid Quality' metric (m21).
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
from aim.metrics.m21.m21_grid_quality import Metric
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
        ("seg1.png", [12, 8, 26, 18, 5, 4, 0.2555, 0.2555, 5, 4]),
        ("seg2.png", [2, 2, 8, 8, 2, 2, 0.0, 0.0, 2, 2]),
        ("seg3.png", [4, 2, 16, 8, 3, 2, 0.0211, 0.0, 3, 2]),
        ("seg4.png", [2, 2, 6, 6, 1, 1, 0.5608, 0.5608, 1, 1]),
        (
            "interfacemetrics_aalto.png",
            [27, 21, 80, 62, 22, 17, 0.2086, 0.2086, 11, 9],
        ),
    ],
)
def test_grid_quality_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test Grid Quality (desktop GUIs).

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
    if result is not None and all(isinstance(i, (float, int)) for i in result):
        assert [round(float(i), 4) for i in result] == expected_results
