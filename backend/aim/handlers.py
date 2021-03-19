#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handlers.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import importlib
import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

# Third-party modules
import tornado.ioloop
import tornado.websocket
from pydantic.error_wrappers import ValidationError
from tornado.options import options

# First-party modules
from aim.common import image_utils
from aim.common.constants import (
    ALLOWED_HOSTS,
    METRICS_DIR,
    METRICS_FILE_PATTERN,
)
from aim.models import MessageBase, MessageImage

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-03-19"
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

    # def open(self):
    #     logging.info("Connection opened")

    def on_message(self, message: Union[str, bytes]):
        # logging.info("Message received: {!r}".format(message))

        try:
            # Load message
            message_data: Dict[str, Any] = json.loads(message)

            # Create message base model
            msg_base: MessageBase = MessageBase(**message_data)

            # Create variables
            # server_name: str = options.name
            # session_id: str = uuid.uuid4().hex

            # Input: URL
            if msg_base.data is None:
                logging.error(
                    "Error: URL input implementation is not available."
                )
                raise NotImplementedError(
                    "URL input implementation is not available."
                )
            # Input: image
            else:
                # Create message image model
                msg: MessageImage = MessageImage(**msg_base.dict())

                # Crop image
                png_image_base64: str = image_utils.crop_image(msg.raw_data)
                image_utils.write_image(
                    png_image_base64,
                    Path(options.runtime_data_dir)
                    / "{}.png".format(options.name),
                )

            # Iterate over selected metrics and execute them one by one
            for metric in {k: v for k, v in msg.metrics.items()}:
                logging.info("Executing metric {}...".format(metric))

                # Locate metric implementation
                metric_files = [
                    metric_file
                    for metric_file in list(
                        Path(METRICS_DIR).glob(METRICS_FILE_PATTERN)
                    )
                    if metric_file.name.startswith(metric + "_")
                ]

                # Metric implementation is available
                if len(metric_files) > 0:
                    # Import metric module
                    metric_module = importlib.import_module(
                        "{}{}.{}".format(
                            re.sub("/", ".", METRICS_DIR),
                            metric,
                            metric_files[0].stem,
                        )
                    )

                    # Execute metric
                    result: Optional[List[Union[int, float, str]]] = metric_module.Metric.execute_metric(  # type: ignore
                        png_image_base64
                    )
                # Metric implementation is not available
                else:
                    logging.error(
                        "Error: Metric implementation is not available."
                    )
                    raise NotImplementedError(
                        "Metric '{}' implementation is not available.".format(
                            metric
                        )
                    )

                self.write_message(
                    {
                        "metric": metric,
                        "result": result,
                        "type": "result",
                        "action": "pushResult",
                    }
                )
        except ValidationError as e:
            self.write_message(
                {
                    "type": "error",
                    "action": "pushValidationError",
                    "message": e.errors(),
                }
            )
        except NotImplementedError as e:
            self.write_message(
                {
                    "type": "error",
                    "action": "pushGeneralError",
                    "message": str(e),
                }
            )
        except Exception as e:
            self.write_message(
                {
                    "type": "error",
                    "action": "pushGeneralError",
                    "message": str(e),
                }
            )

        # Close WebSocket
        self.close()

    # def on_close(self):
    #     logging.info("Connection closed")
