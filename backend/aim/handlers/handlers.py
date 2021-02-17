#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handlers.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import json
import logging
import pathlib
import uuid
from typing import Any, Awaitable, Dict, List, Optional, Union
from urllib.parse import urlparse

# Third-party modules
import tornado.ioloop
import tornado.websocket
from tornado.options import options

# First-party modules
from aim.core import image_utils
from aim.core.constants import ALLOWED_HOSTS
from aim.exceptions.exceptions import ValidationError

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-02-09"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Handlers
# ----------------------------------------------------------------------------

class AIMWebSocketHandler(tornado.websocket.WebSocketHandler):

    # Public methods
    def check_origin(self, origin: str) -> bool:
        """
        https://www.tornadoweb.org/en/stable/websocket.html?highlight=websocket#tornado.websocket.WebSocketHandler.check_origin
        """
        origin_host: Optional[str] = urlparse(origin).hostname
        if origin_host is not None and origin_host in ALLOWED_HOSTS:
            return True
        else:
            return False

    def on_message(self, message: Union[str, bytes]):
        logging.info("A message received: {!r}".format(message))

        try:
            # Load message
            msg: Dict[str, Any] = json.loads(message)

            # Get message data
            msg_type: str = msg.get("type", "")
            msg_url: str = msg.get("url", "")
            msg_filename: Optional[str] = msg.get("filename", None)
            msg_metrics: Dict[str, bool] = {k: v for k, v in msg.get("metrics", {}).items() if v is True}  # filter
            msg_data: Optional[str] = msg.get("data", None)
            server_name: str = options.name
            session_id: str = uuid.uuid4().hex

            # Validate message data
            if msg_type != "execute":
                raise ValidationError("Unsupported message type: '{}'".format(msg_type))

            # Get and update image data
            msg_url = None
            msg_filename = msg_filename.strip().lower()
            msg_filename_extension: str = pathlib.Path(msg_filename).suffix
            msg_data_format: str = msg_data.split(",")[0][5:]  # remove scheme 'data:'
            msg_data_raw: str = msg_data.split(",")[1]

            # Validate image data
            if msg_filename_extension != ".png":
                raise ValidationError("Invalid message filename extension: '{}'".format(msg_filename_extension))
            if msg_data_format != "image/png;base64":
                raise ValidationError("Invalid message data format: '{}'".format(msg_data_format))

            # Crop image
            png_image_base64: str = image_utils.crop_image(msg_data_raw)
            image_utils.write_image(png_image_base64, pathlib.Path(options.runtime_data_dir) / "{}.png".format(options.name))
        except ValidationError as e:
            self.write_message(
                {
                    "type": "error",
                    "action": "pushValidationError",
                    "message": str(e)
                }
            )

        # Close WebSocket
        self.close()
