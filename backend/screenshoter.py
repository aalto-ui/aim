#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Screenshoter utility application.


Usage: screenshoter.py [-h] [-c <path>] [-v] [-i <path>] [-w <int>] [-h <int>] [-o <path>]

Example usage: python screenshoter.py -i data/alexa_top_50_global_sites.txt -w 1280 -h 800 -f -o data/screenshots/ALEXA_50/
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from pathlib import Path

# Third-party modules
from loguru import logger

# First-party modules
from aim.core import configmanager, constants, utils
from aim.core.constants import (
    IMAGE_HEIGHT_DESKTOP,
    IMAGE_WIDTH_DESKTOP,
    SCREENSHOTER_INPUT_FILE,
    SCREENSHOTER_OUTPUT_DIR,
)
from aim.tools import Screenshots

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-03-17"
__email__ = "markku.laine@aalto.fi"
__title__ = "Screenshoter"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------


def init():
    # Add application-specific configuration options
    configmanager.parser.add_argument(
        "-v",
        "--version",
        help="print the {} version number and exit".format(__title__),
        action="version",
        version="{} {}".format(__title__, __version__),
    )
    configmanager.parser.add(
        "-i",
        metavar="<path>",
        help="path to input file",
        dest="input",
        type=configmanager.readable_file,
        required=False,
        default=constants.SCREENSHOTER_INPUT_FILE,
    )
    configmanager.parser.add(
        "-w",
        metavar="<int>",
        help="width of screenshots",
        dest="width",
        type=int,
        required=False,
        default=constants.IMAGE_WIDTH_DESKTOP,
    )
    configmanager.parser.add(
        "-h",
        metavar="<int>",
        help="height of screenshots (minimum height with full page screenshots)",
        dest="height",
        type=int,
        required=False,
        default=constants.IMAGE_HEIGHT_DESKTOP,
    )
    configmanager.parser.add(
        "-o",
        metavar="<path>",
        help="path to output directory",
        dest="output",
        type=configmanager.writable_dir,
        required=False,
        default=constants.SCREENSHOTER_OUTPUT_DIR,
    )
    configmanager.parser.add(
        "-f",
        help="whether to take full page screenshots",
        dest="full_page",
        required=False,
        action="store_true",
        default=False,
    )
    configmanager.options = configmanager.parser.parse_known_args()[
        0
    ]  # Get known options, i.e., Namespace from the tuple

    # Configure logger
    utils.configure_logger()

    # Show title
    utils.show_header(__title__, __version__)

    # Show configurations
    utils.show_configurations()


def main():
    # Initialize the application
    init()

    try:
        # Evaluate GUI designs
        screenshots: Screenshots = Screenshots(
            input_file=Path(configmanager.options.input),
            width=configmanager.options.width,
            height=configmanager.options.height,
            full_page=configmanager.options.full_page,
            output_dir=Path(configmanager.options.output),
        )
        screenshots.take()
        logger.info(
            "{} screenshots were taken and stored at '{}'.".format(
                len(screenshots.input_urls),
                screenshots.output_dir,
            )
        )
    except Exception as err:
        logger.error(err)
        raise


# ----------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
