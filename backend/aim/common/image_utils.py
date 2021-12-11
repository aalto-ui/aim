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
import numpy as np
from PIL import Image
from resizeimage import resizeimage
from skimage.metrics import structural_similarity as ssim

# First-party modules
from aim.common.constants import (
    IMAGE_COMPRESS_LEVEL_PNG,
    IMAGE_HEIGHT_DESKTOP,
    IMAGE_QUALITY_JPEG,
    IMAGE_WIDTH_DESKTOP,
)
from aim.exceptions import ValidationError

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-12-11"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.2"


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
        jpeg_image_quality: JPEG image quality (defaults to 75)

    Returns:
        JPEG image encoded in Base64
    """
    img_rgb: Image.Image = Image.open(
        BytesIO(base64.b64decode(png_image_base64))
    ).convert("RGB")
    jpeg_image_base64: str = to_jpeg_image_base64(
        img_rgb, jpeg_image_quality=jpeg_image_quality
    )

    return jpeg_image_base64


def crop_image(
    image_base64: str, png_image_compress_level: int = IMAGE_COMPRESS_LEVEL_PNG
) -> str:
    """
    Crop an image, encoded in Base64.

    Args:
        image_base64: Image encoded in Base64

    Kwargs:
        png_image_compress_level: PNG image compress level (defaults to 6)

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
        cropped_image_base64 = to_png_image_base64(
            img, png_image_compress_level=png_image_compress_level
        )
    # Image dimensions are correct (use the original image)
    else:
        cropped_image_base64 = image_base64

    return cropped_image_base64


def to_png_image_base64(
    pil_image: Image.Image,
    png_image_compress_level: int = IMAGE_COMPRESS_LEVEL_PNG,
) -> str:
    """
    Convert a PIL image to a PNG image encoded in Base64.

    Args:
        pil_image: PIL image

    Kwargs:
        png_image_compress_level: PNG image compress level (defaults to 6)

    Returns:
        PNG image encoded in Base64
    """
    buffer: BytesIO = BytesIO()
    pil_image.save(
        buffer, format="PNG", compress_level=png_image_compress_level
    )  # [0, 9], where 0 = no compression and 9 = best compression, defaults to 6
    png_image_base64: str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return png_image_base64


def to_jpeg_image_base64(
    pil_image: Image.Image, jpeg_image_quality: int = IMAGE_QUALITY_JPEG
) -> str:
    """
    Convert a PIL image to a JPEG image encoded in Base64.

    Args:
        pil_image: PIL image

    Kwargs:
        jpeg_image_quality: JPEG image quality (defaults to 75)

    Returns:
        JPEG image encoded in Base64
    """
    buffer: BytesIO = BytesIO()
    pil_image.save(
        buffer, format="JPEG", quality=jpeg_image_quality
    )  # [0, 100], where 0 = worst and 100 = best, defaults to 75
    jpeg_image_base64: str = base64.b64encode(buffer.getvalue()).decode(
        "utf-8"
    )

    return jpeg_image_base64


def base64_to_data(
    image_base64: str,
) -> np.ndarray:
    """
    Convert Base64 encoded image string to Numpy array.

    (Semi-)transparent pixels are replaced with (semi-)white pixels in
    the output image data.

    Args:
        image_base64: Image string encoded in Base64

    Returns:
        Image data as Numpy array
    """
    # Create a PIL image
    pil_image: Image.Image = Image.open(
        BytesIO(base64.b64decode(image_base64))
    ).convert("RGB")

    # Convert to numpy array
    image_data: np.ndarray = np.array(pil_image, dtype=np.uint8)

    return image_data


def idiff(image_a_base64: str, image_b_base64: str) -> float:
    """
    Compute the difference between two multi-channel (color) images.

    Args:
        image_a_base64: Image A string encoded in Base64
        image_b_base64: Image B string encoded in Base64

    Returns:
        The difference in percentage [0, 1],
        where 0 = no difference and 1 = completely different
    """
    # Convert to Numpy arrays
    ndarray_a: np.ndarray = base64_to_data(image_a_base64)
    ndarray_b: np.ndarray = base64_to_data(image_b_base64)

    # Compute the mean structural similarity index [-1, 1],
    # where -1 = completely different and 1 = no difference
    s = ssim(
        ndarray_a,
        ndarray_b,
        multichannel=True,
        data_range=max(ndarray_a.max(), ndarray_b.max())
        - min(ndarray_a.min(), ndarray_b.min()),
    )

    # Compute the difference in percentage [0, 1],
    # where 0 = no difference and 1 = completely different
    d = 1 - (1 + s) / 2

    return d
