#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AIM constants.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import Tuple

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2020-08-21"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

COLOR_REDUCTION_THRESHOLD_DESKTOP: int = 5
COLOR_REDUCTION_THRESHOLD_MOBILE: int = 2

GUI_TYPE_DESKTOP: int = 0
GUI_TYPE_MOBILE: int = 1

IMAGE_WIDTH_DESKTOP: int = 1280
IMAGE_HEIGHT_MOBILE: int = 800

IMAGE_BACKGROUND_COLOR: Tuple[int, int, int] = (255, 255, 255)

IMAGE_QUALITY_JPEG: int = 70
