#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AIM backend server.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import logging
import pathlib
from typing import Any, Dict

# Third-party modules
import tornado.ioloop
import tornado.log
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options

# First-party modules
from aim.core.constants import SERVER_CONFIG_FILE
from aim.handlers.handlers import AIMWebSocketHandler

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-02-09"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Definitions
# ----------------------------------------------------------------------------

define("port", default=8888, help="Port to listen on", type=int)
define("environment", default="development", help="Runtime environment", type=str)
define("name", default="aim-dev", help="Instance name", type=str)
define("runtime_data_dir", default="data/temp", help="Directory to store runtime data", type=str)


# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------

def parse_options() -> None:
    server_config_filepath: pathlib.Path = pathlib.Path(SERVER_CONFIG_FILE)
    if server_config_filepath.exists() and server_config_filepath.is_file():
        tornado.options.parse_config_file(SERVER_CONFIG_FILE)
    else:
        tornado.options.parse_command_line()


def make_app() -> tornado.web.Application:
    settings: Dict[str, Any] = {
        "debug": True if options.environment == "development" else False,
        "websocket_max_message_size": 5242880  # 5 MB
    }
    return tornado.web.Application(handlers=[
        (r"/", AIMWebSocketHandler),
    ], **settings)


def main() -> None:
    # Parse options
    parse_options()

    # Make application
    app: tornado.web.Application = make_app()
    app.listen(options.port)
    logging.info("Server is listening on http://localhost:{}".format(options.port))

    # Start application
    tornado.ioloop.IOLoop.current().start()


# ----------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
