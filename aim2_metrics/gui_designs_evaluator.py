#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI designs evaluator utility application.


Usage: gui_designs_evaluator.py [-h] [-c <path>] [-v] [-i <path>] [-o <path>] [-p]

Example usage: python gui_designs_evaluator.py -i data/inputs/alexa_top_50_global_sites/ -o data/outputs/ -p
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules

# Third-party modules
from loguru import logger

# First-party modules
from aim.core import configmanager, constants, utils
from aim.evaluators.evaluators import GUIDesignsEvaluator

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-02-10"
__email__ = "markku.laine@aalto.fi"
__title__ = "GUI Designs Evaluator"
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
        help="path to input directory",
        dest="input",
        type=configmanager.readable_dir,
        required=False,
        default=constants.EVALUATOR_INPUT_DIR,
    )
    configmanager.parser.add(
        "-o",
        metavar="<path>",
        help="path to output directory",
        dest="output",
        type=configmanager.writable_dir,
        required=False,
        default=constants.EVALUATOR_OUTPUT_DIR,
    )
    configmanager.parser.add(
        "-p",
        help="whether to plot evaluation results",
        dest="plot",
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
        evaluator = GUIDesignsEvaluator(
            input_dir=configmanager.options.input,
            output_dir=configmanager.options.output,
            plot_results=configmanager.options.plot,
        )
        evaluator.evaluate()
        logger.info(
            "{} GUI designs at '{}' were evaluated and the results were stored at '{}'.".format(
                len(evaluator.input_gui_design_files),
                evaluator.input_dir,
                evaluator.output_dir,
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
