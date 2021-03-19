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
__date__ = "2021-03-19"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

# Metrics
COLOR_REDUCTION_THRESHOLD_DESKTOP: int = 5
COLOR_REDUCTION_THRESHOLD_MOBILE: int = 2

GUI_TYPE_DESKTOP: int = 0
GUI_TYPE_MOBILE: int = 1

IMAGE_WIDTH_DESKTOP: int = 1280
IMAGE_HEIGHT_DESKTOP: int = 800

IMAGE_BACKGROUND_COLOR: Tuple[int, int, int] = (255, 255, 255)

IMAGE_QUALITY_JPEG: int = 70
IMAGE_QUALITY_PNG: int = 6

GAUSSIAN_KERNEL_SIZE: Tuple[int, int] = (0, 0)
GAUSSIAN_KERNEL_STANDARD_DEVIATION: int = 2

CANNY_EDGE_DETECTION_PYTHON_MIN_THRESHOLD: int = 0
CANNY_EDGE_DETECTION_PYTHON_MAX_THRESHOLD: int = 255

# Tools
SCREENSHOTER_INPUT_FILE: str = "data/alexa_top_50_global_sites_2021-01-25.txt"
SCREENSHOTER_OUTPUT_DIR: str = "data/screenshots/DEFAULT/"
EVALUATOR_INPUT_DIR: str = SCREENSHOTER_OUTPUT_DIR
EVALUATOR_EXCLUDE_FILENAME: str = "exclude.txt"
EVALUATOR_OUTPUT_DIR: str = "data/evaluations/DEFAULT/"

# Web application
ALLOWED_HOSTS: List[str] = [
    "localhost",
    "127.0.0.1",
    "interfacemetrics.aalto.fi",
]
SERVER_CONFIG_FILE: str = "server.conf"
METRICS_CONFIG_FILE: str = "../frontend/src/config/metrics.json"
METRICS_DIR: str = "aim/metrics/"
METRICS_FILE_PATTERN: str = "m*/m*_*.py"
CHROME_DRIVER_BASE_FILE_PATH = "webdrivers/chromedriver"
