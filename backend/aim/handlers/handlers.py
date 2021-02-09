#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handlers.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# from datetime import datetime
# import os
# import json
# import uuid
# import six
# import validators
# import re
# Standard library modules
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

# Third-party modules
import tornado.ioloop
import tornado.websocket

# First-party modules
from aim.core.constants import ALLOWED_HOSTS

# from tornado.options import options

# from aim.segmentation import segmentation
# from aim import utils as aim_utils
# from aim import metric_executor
# from aim.errors.validation_error import ValidationError

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-02-03"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Handlers
# ----------------------------------------------------------------------------

class AIMWebSocketHandler(tornado.websocket.WebSocketHandler):

    # Public methods
    def check_origin(self, origin) -> bool:
        """
        https://www.tornadoweb.org/en/stable/websocket.html?highlight=websocket#tornado.websocket.WebSocketHandler.check_origin
        """
        origin_host: Optional[str] = urlparse(origin).hostname
        if origin_host is not None and origin_host in ALLOWED_HOSTS:
            return True
        else:
            return False

    def open(self):
        logging.info("A client connected.")

    def on_close(self):
        logging.info("A client disconnected")

    def on_message(self, message):
        logging.info("message: {}".format(message))


class MetricWebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        # pass
        print("New connection")

    def on_message(self, message):
        print("message received")
        # try:
        #     # Get message data
        #     message = json.loads(message)
        #     # print(message)
        #     message_type = message["type"]
        #     url = message["url"]
        #     filename = message["filename"]
        #     metrics = {k: v for k, v in message["metrics"].items() if v == True} # filter
        #     data = message["data"]
        #     server = options.name
        #     session = uuid.uuid4().hex

        #     if message_type != "execute":
        #         raise ValidationError("Unsupported message type: '{}'".format(message_type))

        #     # Generate base64 encoded images
        #     # print("Generating base64 encoded images...")
        #     if filename is None: # URL as input
        #         url = url.strip().lower()
        #         # Validations
        #         if (options.environment == "development" and not validators.url(url, public=False)) or \
        #             (options.environment == "production" or options.environment == "test") and (not validators.url(url, public=True) or re.match("^https?://localhost\.", url)):
        #             raise ValidationError("Invalid URL: {}".format(url))
        #         pngb64 = aim_utils.generate_screenshot(url)
        #     else: # screenshot as input
        #         url = None
        #         filename = filename.strip().lower()
        #         # Validations
        #         file_extension = (os.path.splitext(filename)[1]).split(".")[1]
        #         if file_extension != "png":
        #             raise ValidationError("Invalid file extension: '{}'".format(file_extension))
        #         data_format = data.split(",")[0][5:] # remove scheme 'data:'
        #         if data_format != "image/png;base64":
        #             raise ValidationError("Invalid data format: '{}'".format(data_format))
        #         data_raw = data.split(",")[1]
        #         chrome_screenshot_filepath = os.path.join(options.chrome_screenshots_dir, "{}.png".format(options.name))
        #         aim_utils.write_image(data_raw, chrome_screenshot_filepath)
        #         size = aim_utils.get_screenshot_size()
        #         if size > 5242880: # 5 MB
        #             raise ValidationError("File is too large (max 5 MB): {} bytes".format(size))
        #         pngb64 = aim_utils.resize_image(data_raw)
        #     jpgb64 = aim_utils.png2jpeg(pngb64)

        #     # Store screenshot and log associated data
        #     screenshot_path = self.store_image(session, pngb64)
        #     screenshot_log_dict = {
        #         "server": server,
        #         "session": session,
        #         "datetime": aim_utils.get_datetime_utcnowiso(),
        #         "url": url,
        #         "filename": filename,
        #         "image": screenshot_path
        #     }
        #     self.log_data("screenshots", screenshot_log_dict)

        #     # Segment screenshot
        #     # print("Segmenting screenshot...")
        #     if self.is_segmentation_needed(metrics, metric_executor.metrics_mapping):
        #         seg_results = segmentation.get_elements(pngb64)
        #         preview = seg_results["preview"]
        #         seg_elements = seg_results["elements"]
        #     else:
        #         preview = pngb64
        #         seg_elements = None

        #     self.write_message({
        #         "type": "preview",
        #         "action": "pushPreview",
        #         "preview": preview
        #     })

        #     # Execute metrics
        #     for metric in {k: v for k, v in metrics.items()}:
        #         # print("Executing metric {}...".format(metric))
        #         metric_executor_start = datetime.now()
        #         result = metric_executor.execute_metric(metric, pngb64, jpgb64, seg_elements)
        #         metric_executor_end = datetime.now()

        #         # Store result and log associated data
        #         result_with_paths = []
        #         image_counter = 0
        #         for result_value in result:
        #             if isinstance(result_value, six.string_types): # string, i.e., base64 image data (non-numerical value)
        #                 result_path = self.store_image(session, result_value, metric, image_counter)
        #                 result_with_paths.append(result_path)
        #                 image_counter += 1
        #             else:
        #                 result_with_paths.append(result_value)
        #         result_log_dict = {
        #             "server": server,
        #             "session": session,
        #             "datetime": aim_utils.get_datetime_utcnowiso(),
        #             "url": url,
        #             "filename": filename,
        #             "metric": metric,
        #             "result": result_with_paths,
        #             "execution_time": (metric_executor_end - metric_executor_start).total_seconds()
        #         }
        #         self.log_data("results", result_log_dict) # log data

        #         self.write_message(json.dumps({
        #             "metric": metric,
        #             "result": result,
        #             "type": "result",
        #             "action": "pushResult",
        #         }))
        # except ValidationError as e:
        #     self.write_message({
        #         "type": "error",
        #         "action": "pushValidationError",
        #         "message": e.message
        #     })

        # self.close()

    def on_close(self):
        # pass
        print("Connection closed")

    def check_origin(self, origin):
        print("Origin: {}".format(origin))
        return True

    # def is_segmentation_needed(self, metrics, metrics_mapping):
    #     for k, v in metrics.items():
    #         try:
    #             if metrics_mapping[k]["format"] == "seg":
    #                 return True
    #         except:
    #             pass

    #     return False

    # def log_data(self, collection_name, data):
    #     db = self.settings["db"]
    #     collection = db[collection_name]
    #     collection.insert_one(data)

    # def store_image(self, session, image_data, metric=None, image_counter=0):
    #     # Screenshot
    #     if metric is None:
    #         filepath = os.path.join(options.screenshots_data_dir, "{}.png".format(session))
    #         aim_utils.write_image(image_data, filepath)
    #     # Result
    #     else:
    #         filepath = os.path.join(options.results_data_dir, "{}-{}_{}.png".format(session, metric, image_counter))
    #         aim_utils.write_image(image_data, filepath)

    #     return os.path.split(filepath)[1] # tail part, i.e., filename only
