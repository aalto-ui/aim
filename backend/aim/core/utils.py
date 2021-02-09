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
from tornado.options import define, options, parse_config_file

# First-party modules
from aim.core import configmanager

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-02-09"
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

# def parse_configs(show_configs=True):
#     """
#     Parse execution environment configurations.

#     Args:
#         show_configs (bool): Whether parsed configurations should be shown in the console
#     """
#     define("port", default=None, help="Port to listen on", type=int)
#     define("environment", default=None, help="Runtime environment", type=str)
#     define("name", default=None, help="Instance name", type=str)
#     # define("chrome_path", default=None, help="Path to Chrome executable", type=str)
#     # define("chrome_screenshots_dir", default=None, help="Directory to store temporary headless Chrome screenshot files", type=str)
#     define("database_uri", default=None, help="Database URI", type=str)
#     # define("results_data_dir", default=None, help="Directory to store result files", type=str)
#     # define("screenshots_data_dir", default=None, help="Directory to store screenshot files", type=str)
#     # define("vg2_bin_path", default=None, help="Path to vg2 executable", type=str)
#     # define("vg2_configs_dir", default=None, help="Directory to store temporary vg2 config files", type=str)
#     # define("vg2_inputs_dir", default=None, help="Directory to store temporary vg2 input files", type=str)
#     # define("vg2_outputs_dir", default=None, help="Directory to store temporary vg2 output files", type=str)

#     # Determine execution environment and parse configs
#     environment = os.environ.get("AIM_ENV", "development")
#     if environment == "production":
#         config_file = "configs/production.conf"
#     elif environment == "test":
#         config_file = "configs/test.conf"
#     else:
#         config_file = "configs/development.conf"
#     parse_config_file(config_file)
#     # parse_command_line()

#     if show_configs:
#         print("Current working directory: {}".format(os.getcwd()))
#         print("Port: {}".format(options.port))
#         print("Execution environment: {}".format(options.environment))
#         print("Instance name: {}".format(options.name))
#         # print("Chrome path: {}".format(options.chrome_path))
#         # print("Chrome screenshots directory: {}".format(options.chrome_screenshots_dir))
#         print("Database URI: {}".format(options.database_uri))
#         # print("Results data directory: {}".format(options.results_data_dir))
#         # print("Screenshots data directory: {}".format(options.screenshots_data_dir))
#         # print("VG2 binary path: {}".format(options.vg2_bin_path))
#         # print("VG2 configs directory: {}".format(options.vg2_configs_dir))
#         # print("VG2 inputs directory: {}".format(options.vg2_inputs_dir))
#         # print("VG2 outputs directory: {}".format(options.vg2_outputs_dir))
