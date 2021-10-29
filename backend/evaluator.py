#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Evaluator utility application.


Usage: evaluator.py [-h] [-c <path>] [-v] [-i <path>] [-m <str>] [-p] [-o <path>]

Example usage: python evaluator.py -i data/screenshots/ALEXA_500/ -m m1,m2,m3 -p -o data/evaluations/results/
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
from aim.tools import Evaluation

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-10-29"
__email__ = "markku.laine@aalto.fi"
__title__ = "Evaluator"
__version__ = "1.1"


# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------


def get_configured_metrics():
    metrics_configurations = utils.load_metrics_configurations()
    return ",".join(
        list(
            utils.deep_get(
                metrics_configurations, ["metrics"], default={}
            ).keys()
        )
    )


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
        "-m",
        metavar="<list>",
        help="comma-separated list of metrics to be executed",
        dest="metrics",
        type=str,
        required=False,
        default=get_configured_metrics(),
    )
    configmanager.parser.add(
        "-p",
        help="whether to plot evaluation results",
        dest="plot",
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
        default=constants.EVALUATOR_OUTPUT_DIR,
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
        # Evaluate screenshots
        logger.info(
            "Evaluate screenshots stored at '{}'.".format(
                configmanager.options.input
            )
        )
        evaluation: Evaluation = Evaluation(
            input_dir=Path(configmanager.options.input),
            metrics=[
                metric.strip()
                for metric in configmanager.options.metrics.split(",")
            ],
            plot_results=configmanager.options.plot,
            output_dir=Path(configmanager.options.output),
        )
        evaluation.evaluate()
        logger.info(
            "{} out of {} screenshots were successfully evaluated and the results were stored at '{}'.".format(
                evaluation.success_counter,
                len(evaluation.input_screenshot_files),
                evaluation.output_dir,
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
