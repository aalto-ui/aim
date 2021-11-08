#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Screenshoter utility application.


Usage: screenshoter.py [-h] [-c <path>] [-v] [-i <path>] [-sw <int>] [-sh <int>] [-f] [-o <path>]

Example usage: python screenshoter.py -i data/screenshots/ALEXA_500/urls.csv -sw 1280 -sh 800 -f -o data/screenshots/results/
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from pathlib import Path

# Third-party modules
from loguru import logger

# First-party modules
from aim.common import configmanager, constants, utils
from aim.common.constants import (
    IMAGE_HEIGHT_DESKTOP,
    IMAGE_WIDTH_DESKTOP,
    SCREENSHOTER_INPUT_FILE,
    SCREENSHOTER_OUTPUT_DIR,
)
from aim.tools import Screenshot

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-11-08"
__email__ = "markku.laine@aalto.fi"
__title__ = "Screenshoter"
__version__ = "1.1"


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
        "-sw",
        metavar="<int>",
        help="width of screenshots",
        dest="width",
        type=int,
        required=False,
        default=constants.IMAGE_WIDTH_DESKTOP,
    )
    configmanager.parser.add(
        "-sh",
        metavar="<int>",
        help="height of screenshots (minimum height with full page screenshots)",
        dest="height",
        type=int,
        required=False,
        default=constants.IMAGE_HEIGHT_DESKTOP,
    )
    configmanager.parser.add(
        "-f",
        help="whether to take full page screenshots",
        dest="full_page",
        required=False,
        action="store_true",
        default=False,
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
    configmanager.options = configmanager.parser.parse_known_args()[
        0
    ]  # Get known options, i.e., Namespace from the tuple

    # Configure logger
    utils.configure_loguru_logger()

    # Show title
    utils.show_header(__title__, __version__)

    # Show configurations
    utils.show_configurations()


def main():
    # Initialize the application
    init()

    try:
        # Take a screenshot of URLs
        logger.info(
            "Take a screenshot of URLs read from '{}'.".format(
                configmanager.options.input
            )
        )
        screenshot: Screenshot = Screenshot(
            input_file=Path(configmanager.options.input),
            width=configmanager.options.width,
            height=configmanager.options.height,
            full_page=configmanager.options.full_page,
            output_dir=Path(configmanager.options.output),
        )
        screenshot.take()
        if len(screenshot.input_urls) > 0:
            logger.info(
                "{} out of {} screenshots were successfully taken and stored at '{}'.".format(
                    screenshot.success_counter,
                    len(screenshot.input_urls),
                    screenshot.output_dir,
                )
            )
        else:
            logger.info("No screenshots to be taken")
    except Exception as err:
        logger.error(err)
        raise


# ----------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
