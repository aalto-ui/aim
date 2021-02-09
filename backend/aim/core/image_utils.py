#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Image utility functions.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
import pathlib
from io import BytesIO

# Third-party modules
from PIL import Image

# First-party modules
from aim.core.constants import IMAGE_QUALITY_JPEG

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-02-09"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Image utility functions
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
        image_base64: str = base64.b64encode(f.read()).decode("utf-8")

    return image_base64


def write_image(image_base64: str, filepath: pathlib.Path):
    """
    Write an image to a file.

    Args:
        image_base64: Image encoded in Base64
        filepath: Output image file path
    """
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(image_base64))


def convert_image(
    png_image: str, jpeg_image_quality: int = IMAGE_QUALITY_JPEG
) -> str:
    """
    Convert an image from PNG to JPEG, encoded in Base64.

    (Semi-)transparent pixels are replaced with (semi-)white pixels in
    the output JPEG image.

    Args:
        png_image: PNG image encoded in Base64

    Kwargs:
        jpeg_image_quality: JPEG image quality (defaults to 70)

    Returns:
        JPEG image encoded in Base64
    """
    img_rgb: Image.Image = Image.open(
        BytesIO(base64.b64decode(png_image))
    ).convert("RGB")
    buffered: BytesIO = BytesIO()
    img_rgb.save(buffered, format="JPEG", quality=jpeg_image_quality)
    jpeg_image_base64: str = base64.b64encode(buffered.getvalue()).decode(
        "utf-8"
    )

    return jpeg_image_base64
