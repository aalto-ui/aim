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
import re
import time
import uuid
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

# Third-party modules
import tornado.ioloop
import tornado.websocket
from loguru import logger
from motor.motor_tornado import MotorDatabase
from pydantic.error_wrappers import ValidationError
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from tornado.options import options

# First-party modules
from aim.common import image_utils, utils
from aim.common.constants import (
    ALLOWED_HOSTS,
    IMAGE_HEIGHT_DESKTOP,
    IMAGE_WIDTH_DESKTOP,
    METRICS_DIR,
    METRICS_FILE_PATTERN,
)
from aim.models import MessageBase, MessageImage, MessageInput, MessageURL
from aim.tools import Screenshot

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-03-26"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Handlers
# ----------------------------------------------------------------------------


class AIMWebSocketHandler(tornado.websocket.WebSocketHandler):

    # Private methods
    def _save_data(self, collection_name, data):
        db: MotorDatabase = self.settings["db"]
        collection = db[collection_name]
        collection.insert_one(data)

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
    #     logger.debug("Connection opened")

    def on_message(self, message: Union[str, bytes]):
        logger.debug("Message received: {!r}".format(message))

        try:
            # Load message
            message_data: Dict[str, Any] = json.loads(message)

            # Create message base model
            msg: MessageBase = MessageBase(**message_data)

            # Create variables
            server_name: str = options.name
            session_id: str = uuid.uuid4().hex
            png_image_base64: str

            # Input: URL
            if msg.input == MessageInput.url:
                # Create message URL model
                msg_url: MessageURL = MessageURL(**msg.dict())

                # Take screenshot
                driver: ChromeWebDriver = Screenshot.get_web_driver()
                driver.set_window_size(
                    IMAGE_WIDTH_DESKTOP, IMAGE_HEIGHT_DESKTOP
                )
                driver.get(msg_url.url)
                png_image_base64 = driver.get_screenshot_as_base64()
            # Input: image
            else:
                # Create message image model
                msg_image: MessageImage = MessageImage(**msg.dict())

                # Crop image
                png_image_base64 = image_utils.crop_image(msg_image.raw_data)

            # Store input image
            input_image_path: Path = options.data_inputs_dir / "{}.png".format(
                session_id
            )
            image_utils.write_image(png_image_base64, input_image_path)

            # Save inputs data
            self._save_data(
                "inputs",
                {
                    "server": server_name,
                    "session": session_id,
                    "datetime": utils.custom_isoformat(datetime.utcnow()),
                    "type": msg.input,
                    "url": msg.url,
                    "filename": msg.filename.name
                    if msg.filename is not None
                    else None,
                    "image": input_image_path.name,
                },
            )

            # Push preview
            self.write_message(
                {
                    "type": "preview",
                    "action": "pushPreview",
                    "preview": png_image_base64,
                }
            )

            # Iterate over selected metrics and execute them one by one
            for metric in {k: v for k, v in msg.metrics.items()}:
                logger.debug("Executing metric {}...".format(metric))

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
                    metric_module: ModuleType = importlib.import_module(
                        "{}{}.{}".format(
                            re.sub("/", ".", METRICS_DIR),
                            metric,
                            metric_files[0].stem,
                        )
                    )

                    # Execute metric
                    start_time: float = time.time()
                    results: Optional[List[Union[int, float, str]]] = metric_module.Metric.execute_metric(  # type: ignore
                        png_image_base64
                    )
                    end_time: float = time.time()
                    execution_time: float = round(end_time - start_time, 4)
                # Metric implementation is not available
                else:
                    logger.error(
                        "Error: Metric implementation is not available."
                    )
                    raise NotImplementedError(
                        "Metric '{}' implementation is not available.".format(
                            metric
                        )
                    )

                results_modified: Optional[List[Union[int, float, str]]]
                if results is not None:
                    # Iterate over metric results
                    results_modified = []
                    for count, result in enumerate(results, start=0):
                        logger.debug("Result: {}".format(result))
                        # str = image encoded in Base64
                        if isinstance(result, str):
                            # Store result image
                            result_image_path: Path = (
                                options.data_results_dir
                                / "{}-{}_{}.png".format(
                                    session_id, metric, count
                                )
                            )
                            image_utils.write_image(result, result_image_path)

                            # Replace Based64 encoded image with a file path
                            results_modified.append(result_image_path.name)
                        # int or float
                        else:
                            results_modified.append(result)
                else:
                    results_modified = None

                # Save results data
                self._save_data(
                    "results",
                    {
                        "server": server_name,
                        "session": session_id,
                        "datetime": utils.custom_isoformat(datetime.utcnow()),
                        "metric": metric,
                        "results": results_modified,
                        "execution_time": execution_time,
                    },
                )

                # Push result
                self.write_message(
                    {
                        "metric": metric,
                        "results": results,
                        "type": "results",
                        "action": "pushResults",
                    }
                )
        except ValidationError as e:
            logger.error("ValidationError", e)
            self.write_message(
                {
                    "type": "error",
                    "action": "pushValidationError",
                    "message": e.errors(),
                }
            )
        except NotImplementedError as e:
            logger.error("NotImplementedError", e)
            self.write_message(
                {
                    "type": "error",
                    "action": "pushGeneralError",
                    "message": str(e),
                }
            )
        except Exception as e:
            logger.error("Exception: {!r}".format(e))
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
    #     logger.debug("Connection closed")
