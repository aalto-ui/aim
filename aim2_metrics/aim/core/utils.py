#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AIM constants and utility functions.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
import pathlib

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2020-08-09"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 800
IMAGE_BACKGROUND_COLOR = (255, 255, 255)


# ----------------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------------


def read_image(filepath: pathlib.Path) -> str:
    """
    Read an image from a file.

    Args:
        filepath: Input image file path

    Returns:
        Image encoded in Base64
    """
    with open(filepath, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    return image_base64
