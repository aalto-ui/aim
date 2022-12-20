#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'UIED segmentation' metric (m25).
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import pathlib
from typing import Any, Dict, List, Optional, Union

# Third-party modules
import pytest

# First-party modules
from aim.common import image_utils
from aim.common.constants import GUI_TYPE_DESKTOP, GUI_TYPE_MOBILE
from aim.metrics.m25.m25_uied_segmentation import Metric
from aim.segmentation.model import Segmentation
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR, IDIFF_TOLERANCE
from tests.common.utils import load_expected_result

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
        (
            "interfacemetrics_aalto.png",
            [load_expected_result("m25_0_interfacemetrics_aalto.png")],
        ),
    ],
)
def test_uied_segmentation_desktop(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test UIED segmentation (desktop GUIs).

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
    gui_segments: Dict[str, Any] = Segmentation.execute(
        gui_image=gui_image_png_base64, gui_type=GUI_TYPE_DESKTOP
    )

    # Execute metric
    result: Optional[List[Union[int, float, str]]] = Metric.execute_metric(
        gui_image_png_base64,
        gui_segments=gui_segments,
        gui_type=GUI_TYPE_DESKTOP,
    )

    # Test result
    if result is not None and isinstance(result[0], str):
        assert (
            image_utils.idiff(result[0], expected_results[0])
            <= IDIFF_TOLERANCE
        )


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        ("uied_mobile.png", [load_expected_result("m25_0_uied_mobile.png")]),
    ],
)
def test_uied_segmentation_mobile(
    input_value: str, expected_results: List[Any]
) -> None:
    """
    Test UIED segmentation (mobile GUIs).

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
    gui_segments: Dict[str, Any] = Segmentation.execute(
        gui_image=gui_image_png_base64, gui_type=GUI_TYPE_MOBILE
    )

    # Execute metric
    result: Optional[List[Union[int, float, str]]] = Metric.execute_metric(
        gui_image_png_base64,
        gui_segments=gui_segments,
        gui_type=GUI_TYPE_MOBILE,
    )

    # Test result
    if result is not None and isinstance(result[0], str):
        assert (
            image_utils.idiff(result[0], expected_results[0])
            <= IDIFF_TOLERANCE
        )
