#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Evaluators.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import importlib
import time
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

# Third-party modules
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns
from loguru import logger

# First-party modules
from aim.core import image_utils

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-02-09"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Evaluators
# ----------------------------------------------------------------------------


class GUIDesignsEvaluator:

    # Private constants
    _METRICS: List[str] = [
        "m1_png_file_size",  # PNG file size
        "m2_jpeg_file_size",  # JPEG file size
        "m3_distinct_rgb_values",  # Distinct RGB values
        "m4_contour_density",  # Contour density
        "m5_figure_ground_contrast",  # Figure-ground contrast
        "m6_contour_congestion",  # Contour congestion
    ]
    _METRIC_RESULTS = {
        "m1_result_1": {"name": "PNG file size in bytes"},
        "m2_result_1": {"name": "JPEG file size in bytes"},
        "m3_result_1": {"name": "Number of distinct RGB values"},
        "m4_result_1": {"name": "Contour density"},
        "m5_result_1": {"name": "Figure-ground contrast"},
        "m6_result_1": {"name": "Contour congestion"},
    }

    # Public constants
    NAME: str = "GUI Designs Evaluator"
    VERSION: str = "1.0"

    # Initializer
    def __init__(self, input_dir: str, output_dir: str, plot_results: bool):
        self.input_dir: Path = Path(input_dir)
        self.input_csv_file: Optional[Path] = None
        self.input_gui_design_files: List[Path] = []
        self.results: Optional[List[Dict[str, Any]]] = None
        self.output_dir: Path = Path(output_dir) / self.input_dir.name
        self.output_csv_file: Path = self.output_dir / "{}.csv".format(
            self.output_dir.name
        )
        self.plot_results: bool = plot_results

    # Private methods
    def _set_input_csv_file(self):
        for csv_file_path in list(self.input_dir.glob("*.csv"))[:1]:
            self.input_csv_file = csv_file_path

    def _set_input_gui_design_files(self):
        # Get input CSV file
        if self.input_csv_file:
            # Read input data
            input_df = pd.read_csv(self.input_csv_file)

            # Exclude some rows
            input_df = input_df.loc[input_df["include"] == "yes"]

            # Get input GUI design files
            self.input_gui_design_files = [
                self.input_dir / file for file in input_df["filename"].tolist()
            ]
        # No input CSV file available
        else:
            # Get input GUI design files
            self.input_gui_design_files = list(self.input_dir.glob("*.png"))

    def _set_results(self):
        # Get output CSV file (previous results)
        if self.output_csv_file.exists():
            # Create DataFrame
            results_df: pd.DataFrame = pd.read_csv(self.output_csv_file)

            # Remove unfinished evaluation rows
            results_df = results_df.dropna()

            # Convert DataFrame to List
            self.results = results_df.to_dict("records")
        # No output CSV file (previous results) available
        else:
            self.results = []

    def _execute_metrics(self):
        # Iterate over input GUI design files
        for input_gui_design_file in self.input_gui_design_files[
            len(self.results) :
        ]:
            logger.info("Evaluating {}...".format(input_gui_design_file.name))

            # Start total timer
            start_time_total: float = time.time()

            # Initialize GUI design results row
            results_row = {}
            results_row["filename"] = input_gui_design_file.name
            results_row["evaluation_date"] = date.today().isoformat()

            # Read GUI design image (PNG)
            start_time: float = time.time()
            gui_image_png_base64: str = image_utils.read_image(input_gui_design_file)
            end_time: float = time.time()
            results_row["read_image_time"] = round(end_time - start_time, 4)

            # Iterate over AIM metrics
            for metric in self._METRICS:
                # Import metric module
                metric_module = importlib.import_module(
                    "aim.metrics." + metric
                )

                # Execute metric
                start_time: float = time.time()
                metric_results: Optional[
                    List[Any]
                ] = metric_module.Metric.execute_metric(gui_image_png_base64)
                end_time: float = time.time()
                results_row[metric.partition("_")[0] + "_time"] = round(
                    end_time - start_time, 4
                )

                # Iterate over metrics results
                for index, metric_result in enumerate(metric_results):
                    if type(metric_result) is float:
                        results_row[
                            metric.partition("_")[0]
                            + "_result_"
                            + str(index + 1)
                        ] = round(metric_result, 4)
                    else:
                        results_row[
                            metric.partition("_")[0]
                            + "_result_"
                            + str(index + 1)
                        ] = metric_result

            # End total timer
            end_time_total: float = time.time()
            results_row["total_evaluation_time"] = round(
                end_time_total - start_time_total, 4
            )

            # Append results
            self.results.append(results_row)

            # Precaution against crashes: save results after each GUI design
            # evaluation instead of after completing all of them
            self._save_results()

    def _save_results(self):
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

        # Create directories, if needed
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)

        # Save results
        results_df.to_csv(self.output_csv_file, index=False)

    def _reformat_large_tick_values(self, tick_val, pos):
        """
        Turns large tick values (in the billions, millions and thousands) such as 4500 into 4.5K and also appropriately turns 4000 into 4K (no zero after the decimal).

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
            # Get output CSV file (evaluation results)
            evaluation_results_df = pd.read_csv(
                self.output_csv_file,
                header=0,
                dtype={"filename": "str"},
                parse_dates=[1],
            )

            # Plot metric evaluation results
            width: int = 700  # in pixels
            height: int = 500  # in pixels
            dpi: int = 72
            for key, value in self._METRIC_RESULTS.items():
                # Create a new figure and configure it
                sns.set(rc={"figure.figsize": (width / dpi, height / dpi)})
                sns.set_style("ticks")
                sns.set_context("paper", font_scale=1.5)
                plt.figure()

                # Plot data on a histogram and configure it
                ax = sns.histplot(
                    list(evaluation_results_df[key]),
                    kde=False,
                    color="#7553A0",
                    bins=30,
                )
                ax.set_xlabel(
                    value["name"],
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
                    ticker.FuncFormatter(self._reformat_large_tick_values)
                )
                sns.despine(ax=ax, left=False, bottom=False)

                # Save plot
                output_plot_file: Path = (
                    self.output_dir / "{}_evaluator.png".format(key)
                )
                plt.savefig(output_plot_file, dpi=dpi, transparent=False)

    # Public methods
    def evaluate(self):
        self._set_input_csv_file()
        self._set_input_gui_design_files()
        self._set_results()
        self._execute_metrics()
        self._plot_results()
