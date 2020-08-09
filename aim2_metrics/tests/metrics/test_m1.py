#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'PNG file size' metric (m1).
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import os
import pathlib
from typing import Any, List, Optional

# First-party modules
import aim.core.utils as aim_utils
from aim.metrics.m1_png_file_size import Metric1
from tests.core.constants import DATA_TESTS_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2020-08-09"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


class TestM1:
    """
    A test class for the 'PNG file size' metric (m1).
    """

    # Private methods
    def _test(
        self, gui_image_filepath: pathlib.Path, expected_results: List[int]
    ) -> None:
        """
        A helper method for executing and testing the metric.

        Args:
            gui_image_filepath: GUI image file path
            expected_results: Expected result (list of measures)
        """
        # Read GUI image (PNG)
        gui_image_png_base64: str = aim_utils.read_image(gui_image_filepath)

        # Execute metric
        results: Optional[List[Any]] = Metric1.execute_metric(
            gui_image_png_base64
        )

        # Test results
        if results is not None:
            assert results[0] == expected_results[0]

    # Public methods
    def test_png_file_sizes(self) -> None:
        """
        Test PNG file sizes.
        """
        gui_image_filenames: List[str] = [
            "aalto.fi_website.png",
            "myhelsinki.fi_website.png",
            "wikipedia.org_website.png",
        ]
        gui_image_filepaths: List[pathlib.Path] = [
            pathlib.Path(DATA_TESTS_DIR) / gui_image_name
            for gui_image_name in gui_image_filenames
        ]

        # Run tests
        for gui_image_filepath in gui_image_filepaths:
            self._test(
                gui_image_filepath, [os.stat(gui_image_filepath).st_size]
            )
