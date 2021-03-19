#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import sys

# Third-party modules
import arrow
from loguru import logger

# First-party modules
from aim.common import configmanager

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-03-19"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------------


def configure_logger():
    logger.configure(handlers=get_loguru_handlers())


def show_header(title, version):
    logger.info("{} {}".format(title, version))
    logger.info(len("{} {}".format(title, version)) * "=")
    logger.info("")


def show_configurations():
    logger.debug(configmanager.options)
    logger.debug("\n{}".format(configmanager.parser.format_help()))
    logger.debug("\n{}".format(configmanager.parser.format_values()))


def custom_isoformat(datetime_obj):
    return (
        arrow.get(datetime_obj)
        .format("YYYY-MM-DDTHH:mm:ss.SSSZZ")
        .replace("+00:00", "Z")
    )


def format_string(record):
    return (
        "<green>{}</green> | ".format(custom_isoformat(record["time"]))
        + "<level>{level: <8}</level> | "
        + "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        + "<level>{message}</level>\n{exception}"
    )


def get_loguru_handlers():
    handlers = []
    if configmanager.options.loguru_stdout:
        handlers.append(
            {
                "sink": sys.stdout,
                "format": format_string,
                "level": configmanager.options.loguru_level,
                "backtrace": configmanager.options.loguru_backtrace,
            }
        )

    if configmanager.options.loguru_file:
        handlers.append(
            {
                "sink": "logs/error.log",
                "format": format_string,
                "level": configmanager.options.loguru_level,
                "rotation": "100 MB",
                "retention": "3 months",
                "backtrace": configmanager.options.loguru_backtrace,
            }
        )

    return handlers
