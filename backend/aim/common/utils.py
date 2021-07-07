#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import json
import sys

# Third-party modules
import arrow
from loguru import logger

# First-party modules
from aim.common import configmanager
from aim.common.constants import METRICS_CONFIG_FILE

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
                "colorize": configmanager.options.loguru_colorize,
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

    if configmanager.options.loguru_db:
        handlers.append(
            {
                "sink": configmanager.database_sink,
                "format": format_string,
                "level": "ERROR",
                "backtrace": configmanager.options.loguru_backtrace,
                "serialize": True,
            }
        )

    return handlers


def load_metrics_configurations():
    # Load metrics configurations
    metrics_configurations = {}
    with open(METRICS_CONFIG_FILE) as f:
        metrics_configurations = json.load(f)

    return metrics_configurations


def deep_get(d, keys, default=None):
    """
    Source: https://stackoverflow.com/questions/25833613/python-safe-method-to-get-value-of-nested-dictionary

    Example:
        d = {'meta': {'status': 'OK', 'status_code': 200}}
        deep_get(d, ['meta', 'status_code'])          # => 200
        deep_get(d, ['garbage', 'status_code'])       # => None
        deep_get(d, ['meta', 'garbage'], default='-') # => '-'
    """
    assert type(keys) is list
    if d is None:
        return default
    if not keys:
        return d
    return deep_get(d.get(keys[0]), keys[1:], default)
