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
from tests.common.constants import DATA_TESTS_INPUT_VALUES_DIR
from tests.common.utils import load_expected_result_b64

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-12-07"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.1"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ["input_value", "expected_result"],
    [
        (
            "50.png",
            [
                load_expected_result_b64("m9_0_50.png.b64"),
                load_expected_result_b64("m9_1_50.png.b64"),
            ],
        ),
        (
            "COCO_val2014_000000001700.png",
            [
                load_expected_result_b64(
                    "m9_0_COCO_val2014_000000001700.png.b64"
                ),
                load_expected_result_b64(
                    "m9_1_COCO_val2014_000000001700.png.b64"
                ),
            ],
        ),
    ],
)
def test_umsi_desktop(input_value: str, expected_result: List[Any]) -> None:
    """
    Test UMSI (desktop GUIs).

    Args:
        input_value: GUI image file name
        expected_result: Expected result (list of measures)
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
        assert result[0] == expected_result[0]
        assert result[1] == expected_result[1]
