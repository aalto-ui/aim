#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Constants.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import List, Tuple

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-10-29"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.1"


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

# Images
IMAGE_QUALITY_JPEG: int = 75
IMAGE_COMPRESS_LEVEL_PNG: int = 6

IMAGE_WIDTH_DESKTOP: int = 1280
IMAGE_HEIGHT_DESKTOP: int = 800

IMAGE_BACKGROUND_COLOR: Tuple[int, int, int] = (255, 255, 255)

# Metrics
GUI_TYPE_DESKTOP: int = 0
GUI_TYPE_MOBILE: int = 1

# Tools
SCREENSHOTER_INPUT_FILE: str = "data/screenshots/ALEXA_500/urls.csv"
SCREENSHOTER_OUTPUT_DIR: str = "data/screenshots/results/"
EVALUATOR_INPUT_DIR: str = "data/screenshots/ALEXA_500/"
EVALUATOR_EXCLUDE_FILENAME: str = "exclude.txt"
EVALUATOR_OUTPUT_DIR: str = "data/evaluations/results/"

# Web application
ALLOWED_HOSTS: List[str] = [
    "localhost",
    "127.0.0.1",
    "interfacemetrics.aalto.fi",
]
METRICS_CONFIG_FILE: str = "../metrics.json"
METRICS_DIR: str = "aim/metrics/"
METRICS_FILE_PATTERN: str = "m*/m*_*.py"
CHROME_DRIVER_BASE_FILE_PATH = "webdrivers/chromedriver"
