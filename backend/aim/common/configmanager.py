#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration manager.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import os
from pathlib import Path

# Third-party modules
import configargparse

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-03-17"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------


def readable_file(path):
    """
    A custom type for readable file.


    Raises:
        ArgumentTypeError: If the 'path' argument is not a valid or readable file
    """
    input_path: Path = Path(path)
    if not input_path.is_file():
        raise configargparse.ArgumentTypeError(
            "The path '{}' is not a valid file.".format(path)
        )
    if os.access(path, os.R_OK):
        return path
    else:
        raise configargparse.ArgumentTypeError(
            "The path '{}' is not a readable file.".format(path)
        )


def readable_dir(path):
    """
    A custom type for readable directory.


    Raises:
        ArgumentTypeError: If the 'path' argument is not a valid or readable directory
    """
    input_path: Path = Path(path)
    if input_path.is_file():
        raise configargparse.ArgumentTypeError(
            "The path '{}' is not a valid directory.".format(path)
        )
    else:
        input_path.mkdir(parents=True, exist_ok=True)

    if os.access(path, os.R_OK):
        return path
    else:
        raise configargparse.ArgumentTypeError(
            "The path '{}' is not a readable directory.".format(path)
        )


def writable_dir(path):
    """
    A custom type for writable directory.


    Raises:
        ArgumentTypeError: If the 'path' argument is not a valid or writable directory
    """
    input_path: Path = Path(path)
    if input_path.is_file():
        raise configargparse.ArgumentTypeError(
            "The path '{}' is not a valid directory.".format(path)
        )
    else:
        input_path.mkdir(parents=True, exist_ok=True)

    if os.access(path, os.W_OK):
        return path
    else:
        raise configargparse.ArgumentTypeError(
            "The path '{}' is not a writable directory.".format(path)
        )


# ----------------------------------------------------------------------------
# Initialization
# ----------------------------------------------------------------------------

# Get global singleton instance
parser = configargparse.get_argument_parser()

# Common configurations
#   -XXX  command line argument only
#   --XXX command line and configuration file argument
parser.add(
    "-c",
    metavar="<path>",
    help="path to configuration file",
    dest="configuration",
    type=str,
    choices=["loguru.ini"],
    required=False,
    is_config_file=True,
    default="loguru.ini",
)
parser.add(
    "--loguru_level",
    help="minimum logging level",
    dest="loguru_level",
    type=str,
    choices=[
        "TRACE",
        "DEBUG",
        "INFO",
        "SUCCESS",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ],
    required=False,
    default="DEBUG",
)
parser.add(
    "--loguru_stdout",
    help="whether to log to stdout",
    dest="loguru_stdout",
    required=False,
    action="store_true",
    default=False,
)
parser.add(
    "--loguru_file",
    help="whether to log to file",
    dest="loguru_file",
    required=False,
    action="store_true",
    default=False,
)
parser.add(
    "--loguru_backtrace",
    help="whether to show full stacktrace",
    dest="loguru_backtrace",
    required=False,
    action="store_true",
    default=False,
)
parser.add(
    "--loguru_colorize",
    help="whether to colorize the stdout output",
    dest="loguru_colorize",
    required=False,
    action="store_true",
    default=False,
)

# Options to access parsed configurations
options = None
