#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'UMSI' metric (m9).
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
from aim.metrics.m9.m9_umsi import Metric
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR, IDIFF_TOLERANCE
from tests.common.utils import load_expected_result

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-12-11"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.1"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_results"],
    [
        (
            "50.png",
            [
                load_expected_result("m9_0_50.png"),
                load_expected_result("m9_1_50.png"),
            ],
        ),
        (
            "COCO_val2014_000000001700.png",
            [
                load_expected_result("m9_0_COCO_val2014_000000001700.png"),
                load_expected_result("m9_1_COCO_val2014_000000001700.png"),
            ],
        ),
    ],
)
def test_umsi_desktop(input_value: str, expected_results: List[Any]) -> None:
    """
    Test UMSI (desktop GUIs).

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
    ):
        assert (
            image_utils.idiff(result[0], expected_results[0])
            <= IDIFF_TOLERANCE
        )
        assert (
            image_utils.idiff(result[1], expected_results[1])
            <= IDIFF_TOLERANCE
        )
