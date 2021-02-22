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
from typing import Any, Dict, Optional, Union
from urllib.parse import urlparse

# Third-party modules
import tornado.ioloop
import tornado.websocket
from pydantic.error_wrappers import ValidationError
from tornado.options import options

# First-party modules
from aim.core import image_utils
from aim.core.constants import ALLOWED_HOSTS
from aim.models.models import MessageBase, MessageImage, MessageURL

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-02-22"
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
            message_data: Dict[str, Any] = json.loads(message)

            # Create message base model
            message_base: MessageBase = MessageBase(**message_data)

            # Create variables
            # server_name: str = options.name
            # session_id: str = uuid.uuid4().hex

            # Input: URL
            if message_base.data is None:
                pass
            # Input: image
            else:
                # Create message image model
                message_image = MessageImage(**message_base.dict())

                # Crop image
                png_image_base64: str = image_utils.crop_image(
                    message_image.raw_data
                )
                image_utils.write_image(
                    png_image_base64,
                    pathlib.Path(options.runtime_data_dir)
                    / "{}.png".format(options.name),
                )
        except ValidationError as e:
            self.write_message(
                {
                    "type": "error",
                    "action": "pushValidationError",
                    "message": e.errors(),
                }
            )

        # Close WebSocket
        self.close()
