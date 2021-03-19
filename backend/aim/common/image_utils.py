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
from resizeimage import resizeimage

# First-party modules
from aim.common.constants import (
    IMAGE_HEIGHT_DESKTOP,
    IMAGE_QUALITY_JPEG,
    IMAGE_QUALITY_PNG,
    IMAGE_WIDTH_DESKTOP,
)
from aim.exceptions import ValidationError

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-03-19"
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


def write_image(image_base64: str, filepath: pathlib.Path) -> None:
    """
    Write an image to a file.

    Args:
        image_base64: Image encoded in Base64
        filepath: Output image file path
    """
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(image_base64))


def convert_image(
    png_image_base64: str, jpeg_image_quality: int = IMAGE_QUALITY_JPEG
) -> str:
    """
    Convert an image from PNG to JPEG, encoded in Base64.

    (Semi-)transparent pixels are replaced with (semi-)white pixels in
    the output JPEG image.

    Args:
        png_image_base64: PNG image encoded in Base64

    Kwargs:
        jpeg_image_quality: JPEG image quality (defaults to 70)

    Returns:
        JPEG image encoded in Base64
    """
    img_rgb: Image.Image = Image.open(
        BytesIO(base64.b64decode(png_image_base64))
    ).convert("RGB")
    buffered: BytesIO = BytesIO()
    img_rgb.save(buffered, format="JPEG", quality=jpeg_image_quality)
    jpeg_image_base64: str = base64.b64encode(buffered.getvalue()).decode(
        "utf-8"
    )

    return jpeg_image_base64


def crop_image(
    image_base64: str, png_image_quality: int = IMAGE_QUALITY_PNG
) -> str:
    """
    Crop an image, encoded in Base64.

    Args:
        image_base64: Image encoded in Base64

    Kwargs:
        png_image_quality: PNG image quality (defaults to 6)

    Returns:
        PNG image (possibly cropped) encoded in Base64
    """
    img: Image.Image = Image.open(BytesIO(base64.b64decode(image_base64)))
    img_width: int
    img_height: int
    img_width, img_height = img.size
    cropped_image_base64: str

    # Image is too small
    if img_width < IMAGE_WIDTH_DESKTOP or img_height < IMAGE_HEIGHT_DESKTOP:
        raise ValidationError(
            "Image is too small (min {} x {} pixels): {} x {} pixels".format(
                IMAGE_WIDTH_DESKTOP,
                IMAGE_HEIGHT_DESKTOP,
                img_width,
                img_height,
            )
        )
    # Image is too big
    elif img_width > IMAGE_WIDTH_DESKTOP or img_height > IMAGE_HEIGHT_DESKTOP:
        # Image is too wide
        if (img_width / img_height) > (
            IMAGE_WIDTH_DESKTOP / IMAGE_HEIGHT_DESKTOP
        ):
            img = resizeimage.resize_height(img, IMAGE_HEIGHT_DESKTOP)
        # Image is too high (and wide)
        else:
            img = resizeimage.resize_width(img, IMAGE_WIDTH_DESKTOP)

        img = img.crop((0, 0, IMAGE_WIDTH_DESKTOP, IMAGE_HEIGHT_DESKTOP))
        buffered = BytesIO()
        img.save(
            buffered, format="PNG", compress_level=png_image_quality
        )  # [0, 9], where 0 = no compression and 9 = best compression, defaults to 6
        cropped_image_base64 = base64.b64encode(buffered.getvalue()).decode(
            "utf-8"
        )
    # Image dimensions are correct (use the original image)
    else:
        cropped_image_base64 = image_base64

    return cropped_image_base64
