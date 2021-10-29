#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import importlib
import platform
import re
import time
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

# Third-party modules
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.common.by import By

# First-party modules
from aim.common import image_utils, utils
from aim.common.constants import (
    CHROME_DRIVER_BASE_FILE_PATH,
    EVALUATOR_EXCLUDE_FILENAME,
    METRICS_DIR,
    METRICS_FILE_PATTERN,
)

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-10-29"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.1"


# ----------------------------------------------------------------------------
# Tools
# ----------------------------------------------------------------------------


class Screenshot:

    # Public constants
    NAME: str = "Screenshot"
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

    def _get_document_size(self) -> Tuple[int, int]:
        width: int = self.driver.execute_script(
            "return document.body.parentNode.scrollWidth"
        )
        height: int = self.driver.execute_script(
            "return document.body.parentNode.scrollHeight"
        )

        return (width, height)

    # Public methods
    @staticmethod
    def get_web_driver() -> ChromeWebDriver:
        options: ChromeOptions = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--force-device-scale-factor")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--disable-gpu")

        plt: str = platform.system()
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

    def take(self) -> None:
        # Read input URLs
        self._read_input_urls()

        # Get web driver
        self.driver = self.get_web_driver()

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
                    self.driver.find_element(By.TAG_NAME, "body").screenshot(
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
            except Exception as err:
                logger.error(
                    "Failed to take a screenshot of {}".format(input_url)
                )
                logger.error(err)
            else:
                self.success_counter += 1

        # Close the browser
        self.driver.quit()


class Evaluation:

    # Public constants
    NAME: str = "Evaluation"
    VERSION: str = "1.1"

    # Initializer
    def __init__(
        self,
        input_dir: Path,
        metrics: List[str],
        plot_results: bool,
        output_dir: Path,
    ):
        self.input_dir: Path = input_dir
        self.input_screenshot_files: List[Path] = []
        self.excluded_screenshots_file: Path = (
            self.input_dir / EVALUATOR_EXCLUDE_FILENAME
        )
        self.excluded_screenshots: List[str] = []
        self.metrics: List[str] = metrics
        self.plot_results: bool = plot_results
        self.results: Optional[List[Dict[str, Any]]] = []
        self.output_dir: Path = output_dir
        self.output_results_csv_file: Path = self.output_dir / "results.csv"
        self.output_results_json_file: Path = self.output_dir / "results.json"
        self.output_quantiles_csv_file: Path = (
            self.output_dir / "quantiles.csv"
        )
        self.success_counter: int = 0
        self.metrics_configurations: Dict[
            str, Any
        ] = utils.load_metrics_configurations()

    # Private methods
    def _read_excluded_screenshots(self) -> None:
        if self.excluded_screenshots_file.exists():
            with open(self.excluded_screenshots_file) as f:
                self.excluded_screenshots = f.readlines()

        self.excluded_screenshots = [
            excluded_screenshot.strip()
            for excluded_screenshot in self.excluded_screenshots
        ]

    def _read_input_screenshot_files(self) -> None:
        # Get input screenshot files
        self.input_screenshot_files = list(self.input_dir.glob("*.png"))

        # Filter out excluded screenhots
        self.input_screenshot_files = [
            input_screenshot_file
            for input_screenshot_file in self.input_screenshot_files
            if input_screenshot_file.name not in self.excluded_screenshots
        ]

    def _read_previous_results(self):
        # Get output results CSV file (previous results)
        if self.output_results_csv_file.exists():
            # Create DataFrame
            results_df: pd.DataFrame = pd.read_csv(
                self.output_results_csv_file
            )

            # Remove unfinished evaluation rows
            results_df = results_df.dropna()

            # Convert DataFrame to List
            self.results = results_df.to_dict(orient="records")

    def _execute_metrics(self):
        # Iterate over input screenshot files
        self.success_counter = 0
        for input_screenshot_file in self.input_screenshot_files[
            len(self.results) :
        ]:
            logger.info(
                "Evaluating a screenshot of {}".format(
                    input_screenshot_file.name
                )
            )

            try:
                # Start total timer
                start_time_total: float = time.time()

                # Initialize screenshot results row
                results_row = {}
                results_row["filename"] = input_screenshot_file.name
                results_row["evaluation_date"] = date.today().isoformat()

                # Read screenshot image (PNG)
                start_time: float = time.time()
                image_png_base64: str = image_utils.read_image(
                    input_screenshot_file
                )
                end_time: float = time.time()
                results_row["read_image_time"] = round(
                    end_time - start_time, 4
                )

                # Iterate over selected metrics
                for metric in self.metrics:
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
                        start_time: float = time.time()
                        metric_results: Optional[
                            List[Union[int, float, str]]
                        ] = metric_module.Metric.execute_metric(
                            image_png_base64
                        )
                        end_time: float = time.time()
                        results_row[metric + "_time"] = round(
                            end_time - start_time, 4
                        )

                        # Iterate over metrics results
                        for index, metric_result in enumerate(metric_results):
                            if type(metric_result) is float:
                                results_row[
                                    self.metrics_configurations["metrics"][
                                        metric
                                    ]["results"][index]["id"]
                                ] = round(metric_result, 4)
                            elif type(metric_result) is int:
                                results_row[
                                    self.metrics_configurations["metrics"][
                                        metric
                                    ]["results"][index]["id"]
                                ] = metric_result
                            else:  # str
                                # Image (PNG) encoded in Base64
                                pass

                # End total timer
                end_time_total: float = time.time()
                results_row["total_evaluation_time"] = round(
                    end_time_total - start_time_total, 4
                )

                # Append results
                self.results.append(results_row)

                # Precaution against crashes: save results and quantiles
                # after each screenshot evaluation instead of after
                # completing all of them
                self._save_results_and_quantiles()
            except Exception as err:
                logger.error(
                    "Failed to evaluate a screenshot of {}".format(
                        input_screenshot_file
                    )
                )
                logger.error(err)
            else:
                self.success_counter += 1

    def _save_results_and_quantiles(self):
        # Create DataFrame
        results_df: pd.DataFrame = pd.DataFrame(self.results)

        # Reorder columns
        cols: List[str] = results_df.columns.tolist()
        sorted(cols)
        cols.remove("filename")
        cols.remove("evaluation_date")
        cols.remove("read_image_time")
        cols.remove("total_evaluation_time")
        cols = [
            "filename",
            "evaluation_date",
            "total_evaluation_time",
            "read_image_time",
        ] + cols
        results_df = results_df[cols]
        results_df = results_df.sort_values(by=["filename"])
        quantiles_df = results_df.quantile([0.25, 0.5, 0.75])
        quantiles_df = quantiles_df.round(decimals=4)

        # Save results and quantiles
        results_df.to_csv(self.output_results_csv_file, index=False)
        quantiles_df.to_csv(self.output_quantiles_csv_file, index=True)

        # Save results to json for the frontend
        results_df.to_json(self.output_results_json_file, orient="records")

    def _reformat_large_tick_values(self, tick_val, pos):
        """
        Turns large tick values (in the billions, millions and thousands)
        such as 4500 into 4.5K and also appropriately turns 4000 into 4K
        (no zero after the decimal).

        Source: https://dfrieds.com/data-visualizations/how-format-large-tick-values.html
        """
        if tick_val >= 1000000000:
            val = round(tick_val / 1000000000, 1)
            new_tick_format = "{:}B".format(val)
        elif tick_val >= 1000000:
            val = round(tick_val / 1000000, 1)
            new_tick_format = "{:}M".format(val)
        elif tick_val >= 1000:
            val = round(tick_val / 1000, 1)
            new_tick_format = "{:}K".format(val)
        else:
            new_tick_format = round(tick_val, 4)

        # Make new_tick_format into a string value
        new_tick_format = str(new_tick_format)

        # Code below will keep 4.5M as is but change values such as 4.0M to 4M since that zero after the decimal isn't needed
        index_of_decimal = new_tick_format.find(".")

        if index_of_decimal != -1 and (tick_val >= 1000 or tick_val == 0):
            value_after_decimal = new_tick_format[index_of_decimal + 1]
            if value_after_decimal == "0":
                # Remove the 0 after the decimal point since it's not needed
                new_tick_format = (
                    new_tick_format[0:index_of_decimal]
                    + new_tick_format[index_of_decimal + 2 :]
                )

        return new_tick_format

    def _plot_results(self):
        # Plot results
        if self.plot_results:
            # Get output results CSV file (evaluation results)
            evaluation_results_df = pd.read_csv(
                self.output_results_csv_file,
                header=0,
                dtype={"filename": "str"},
                parse_dates=[1],
            )

            # Plot metric evaluation results
            width: int = 700  # in pixels
            height: int = 500  # in pixels
            dpi: int = 72

            # Iterate over selected metrics
            for metric in self.metrics:
                # Iterate over metric results
                for result in self.metrics_configurations["metrics"][metric][
                    "results"
                ]:
                    if result["type"] != "b64":
                        # Create a new figure and configure it
                        sns.set(
                            rc={"figure.figsize": (width / dpi, height / dpi)}
                        )
                        sns.set_style("ticks")
                        sns.set_context("paper", font_scale=1.5)
                        plt.figure()

                        # Plot data on a histogram and configure it
                        ax = sns.histplot(
                            list(evaluation_results_df[result["id"]]),
                            kde=False,
                            color="#7553A0",
                            bins=30,
                        )
                        ax.set_xlabel(
                            result["name"],
                            fontstyle="normal",
                            fontweight="normal",
                            labelpad=10,
                        )
                        ax.set_ylabel(
                            "Frequency",
                            fontstyle="normal",
                            fontweight="normal",
                            labelpad=10,
                        )
                        ax.xaxis.grid(False)
                        ax.yaxis.grid(False)
                        ax.xaxis.set_major_formatter(
                            ticker.FuncFormatter(
                                self._reformat_large_tick_values
                            )
                        )
                        sns.despine(ax=ax, left=False, bottom=False)

                        # Save plot
                        output_plot_file: Path = (
                            self.output_dir
                            / "{}_histogram.png".format(result["id"])
                        )
                        plt.savefig(
                            output_plot_file, dpi=dpi, transparent=False
                        )

    # Public methods
    def evaluate(self):
        self._read_excluded_screenshots()
        self._read_input_screenshot_files()
        self._read_previous_results()
        self._execute_metrics()
        self._plot_results()
