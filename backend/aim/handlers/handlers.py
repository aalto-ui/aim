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
import pathlib
import re
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

# Third-party modules
import tornado.ioloop
import tornado.websocket
from pydantic.error_wrappers import ValidationError
from tornado.options import options

# First-party modules
from aim.core import image_utils
from aim.core.constants import ALLOWED_HOSTS, METRICS_DIR, METRICS_FILE_PATTERN
from aim.models.models import MessageBase, MessageImage

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-02-23"
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
            msg_base: MessageBase = MessageBase(**message_data)

            # Create variables
            # server_name: str = options.name
            # session_id: str = uuid.uuid4().hex

            # Input: URL
            if msg_base.data is None:
                pass
            # Input: image
            else:
                # Create message image model
                msg: MessageImage = MessageImage(**msg_base.dict())

                # Crop image
                png_image_base64: str = image_utils.crop_image(msg.raw_data)
                image_utils.write_image(
                    png_image_base64,
                    pathlib.Path(options.runtime_data_dir)
                    / "{}.png".format(options.name),
                )

            # Iterate over selected metrics and execute them one by one
            for metric in {k: v for k, v in msg.metrics.items()}:
                print("Executing metric {}...".format(metric))

                # Locate metric implementation
                metric_files = list(
                    pathlib.Path(METRICS_DIR).glob(
                        metric + METRICS_FILE_PATTERN
                    )
                )

                # Metric implementation is available
                if len(metric_files) > 0:
                    # Import metric module
                    metric_module = importlib.import_module(
                        "{}{}".format(
                            re.sub("/", ".", METRICS_DIR), metric_files[0].stem
                        )
                    )

                    # Execute metric
                    result: Optional[List[Union[int, float, str]]] = metric_module.Metric.execute_metric(  # type: ignore
                        png_image_base64
                    )
                # Metric implementation is not available
                else:
                    print("Error: Metric implementation is not available.")
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
                    "action": "pushValidationError",  # TODO: Support and use a new generic error type
                    "message": str(e),
                }
            )

        # Close WebSocket
        self.close()
