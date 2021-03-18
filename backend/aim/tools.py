#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import platform
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse

# Third-party modules
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver

# First-party modules
from aim.core.constants import CHROME_DRIVER_BASE_FILE_PATH

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-03-18"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tools
# ----------------------------------------------------------------------------


class Screenshots:

    # Public constants
    NAME: str = "Screenshots"
    VERSION: str = "1.0"

    # Initializer
    def __init__(
        self,
        input_file: Path,
        width: int,
        height: int,
        full_page: bool,
        output_dir: Path,
    ):
        self.input_file: Path = input_file
        self.input_urls: List[str] = []
        self.width: int = width
        self.height: int = height
        self.full_page: bool = full_page
        self.output_dir: Path = output_dir
        self.driver: ChromeWebDriver = None
        self.success_counter: int = 0

    # Private methods
    def _read_input_urls(self) -> None:
        with open(self.input_file) as f:
            self.input_urls = f.readlines()

        self.input_urls = [input_url.strip() for input_url in self.input_urls]

    def _get_web_driver(self) -> ChromeWebDriver:
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--force-device-scale-factor")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--disable-gpu")

        plt = platform.system()
        executable_path: str
        if plt == "Windows":
            executable_path = "{}_windows.exe".format(
                CHROME_DRIVER_BASE_FILE_PATH
            )
        elif plt == "Linux":
            executable_path = "{}_linux".format(CHROME_DRIVER_BASE_FILE_PATH)
        elif plt == "Darwin":
            executable_path = "{}_mac".format(CHROME_DRIVER_BASE_FILE_PATH)

        return webdriver.Chrome(
            executable_path=executable_path, options=options
        )

    def _get_document_size(self) -> Tuple[int, int]:
        width: int = self.driver.execute_script(
            "return document.body.parentNode.scrollWidth"
        )
        height: int = self.driver.execute_script(
            "return document.body.parentNode.scrollHeight"
        )

        return (width, height)

    # Public methods
    def take(self) -> None:
        # Read input URLs
        self._read_input_urls()

        # Get web driver
        self.driver = self._get_web_driver()

        # Iterate over input URLs
        self.success_counter = 0
        for input_url in self.input_urls:
            logger.info("Taking a screenshot of {}".format(input_url))

            try:
                self.driver.set_window_size(self.width, self.height)
                self.driver.get(input_url)

                # Take full page screenshot
                if self.full_page:
                    document_size: Tuple[int, int] = self._get_document_size()
                    self.driver.set_window_size(
                        document_size[0], document_size[1]
                    )
                    self.driver.find_element_by_tag_name("body").screenshot(
                        str(
                            self.output_dir
                            / "{}.png".format(urlparse(input_url).hostname)
                        )
                    )
                # Take fixed size screenshot
                else:
                    self.driver.save_screenshot(
                        str(
                            self.output_dir
                            / "{}.png".format(urlparse(input_url).hostname)
                        )
                    )
            except InvalidArgumentException as err:
                logger.error(
                    "Failed to take a screenshot of {}".format(input_url)
                )
                logger.error(err)
            else:
                self.success_counter += 1

        # Close the browser
        self.driver.quit()
