#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'Segmentation'.
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import pathlib
from typing import Any, Dict, List, Tuple, Union

# Third-party modules
import pytest

# First-party modules
from aim.common import image_utils
from aim.common.constants import GUI_TYPE_DESKTOP, GUI_TYPE_MOBILE
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
    ["input_value"],
    [
        (["interfacemetrics_aalto.png"]),
         (["black.png"]),
    ],
)
def test_segmentation_desktop(input_value: str) -> None:
    """
    Test Segmentation (desktop GUIs).

    Args:
        input_value: GUI image file name
    """
    # Build GUI image file path
    gui_image_filepath: pathlib.Path = (
            pathlib.Path(DATA_TESTS_INPUT_VALUES_DIR) / input_value
    )

    # Read GUI image (PNG)
    gui_image_png_base64: str = image_utils.read_image(gui_image_filepath)

    # Execute segmentation
    result: Dict[str, Any] = Segmentation.execute(
        gui_image=gui_image_png_base64, gui_type=GUI_TYPE_DESKTOP
    )

    # Test result
    if result is not None and isinstance(result, Dict):
        assert ('segments' in result) == True
        assert ('img_shape' in result) == True
        assert ('img_b64' in result) == True


@pytest.mark.parametrize(
    ["input_value"],
    [
        (["uied_mobile.png"]),
    ],
)
def test_segmentation_mobile(input_value: str) -> None:
    """
    Test Segmentation (desktop GUIs).

    Args:
        input_value: GUI image file name
    """
    # Build GUI image file path
    gui_image_filepath: pathlib.Path = (
            pathlib.Path(DATA_TESTS_INPUT_VALUES_DIR) / input_value
    )

    # Read GUI image (PNG)
    gui_image_png_base64: str = image_utils.read_image(gui_image_filepath)

    # Execute segmentation
    result: Dict[str, Any] = Segmentation.execute(
        gui_image=gui_image_png_base64, gui_type=GUI_TYPE_MOBILE
    )

    # Test result
    if result is not None and isinstance(result, Dict):
        assert ('segments' in result) == True
        assert ('img_shape' in result) == True
        assert ('img_b64' in result) == True
