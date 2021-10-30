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
import shutil
from pathlib import Path
from typing import Any, Callable

# Third-party modules
import configargparse

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-10-30"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.1"


# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------


def _confirm_prompt(question, default="no"):
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Unknown setting '{}' for default.".format(default))

    while True:
        try:
            resp = input(question + prompt).strip().lower()
            if default is not None and resp == "":
                return default == "yes"
            else:
                if resp.lower() in ["yes", "no", "y", "n"]:
                    return resp.lower() in ["yes", "y"]
                else:
                    raise ValueError
        except ValueError:
            print("Prease respond with 'yes' or 'no' (or 'y' or 'n').\n")


def readable_file(path):
    """
    A custom type for readable file.


    Raises:
        ArgumentTypeError: If the 'path' argument is not a valid or readable file
    """
    input_path: Path = Path(path)
    if not input_path.is_file():
        raise configargparse.ArgumentTypeError(
            "The path '{}' is not a valid file.".format(input_path)
        )
    if os.access(input_path, os.R_OK):
        return input_path
    else:
        raise configargparse.ArgumentTypeError(
            "The path '{}' is not a readable file.".format(input_path)
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
            "The path '{}' is not a valid directory.".format(input_path)
        )
    else:
        input_path.mkdir(parents=True, exist_ok=True)

    if os.access(input_path, os.R_OK):
        return input_path
    else:
        raise configargparse.ArgumentTypeError(
            "The path '{}' is not a readable directory.".format(input_path)
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
            "The path '{}' is not a valid directory.".format(input_path)
        )
    else:
        try:
            input_path.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            if _confirm_prompt(
                "The directory '{}' already exists. Delete all its contents before continuing?".format(
                    input_path
                ),
                default="yes",
            ):
                shutil.rmtree(input_path)
            input_path.mkdir(parents=True, exist_ok=True)

    if os.access(input_path, os.W_OK):
        return input_path
    else:
        raise configargparse.ArgumentTypeError(
            "The path '{}' is not a writable directory.".format(input_path)
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
    "--loguru_db",
    help="whether to log to database",
    dest="loguru_db",
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

# Loguru database sink reference
database_sink: Callable[[Any], None] = lambda msg: None
