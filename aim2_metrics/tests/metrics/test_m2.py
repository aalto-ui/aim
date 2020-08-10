#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the 'JPEG file size' metric (m2).
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import os
import pathlib
from typing import Any, List, Optional

# Third-party modules
import pytest

# First-party modules
import aim.core.utils as aim_utils
from aim.metrics.m2_jpeg_file_size import Metric2
from tests.core.constants import DATA_TEMP_DIR, DATA_TESTS_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2020-08-10"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


@pytest.mark.usefixtures("clean_up")
class TestM2:
    """
    A test class for the 'JPEG file size' metric (m2).
    """

    # Private methods
    def _test(self, gui_image_filepaths: List[pathlib.Path]) -> None:
        """
        A helper method for executing and testing the metric.

        Args:
            gui_image_filepaths: GUI image file paths
        """
        # Iterate over GUI image filepaths
        for gui_image_filepath in gui_image_filepaths:
            # Read GUI image (PNG)
            gui_image_png_base64: str = aim_utils.read_image(
                gui_image_filepath
            )

            # Convert GUI image from PNG to JPEG
            gui_image_jpeg_base64: str = aim_utils.convert_image(
                gui_image_png_base64, jpeg_image_quality=Metric2.IMAGE_QUALITY
            )

            # Create filepath for JPEG GUI image
            gui_image_jpeg_filepath: pathlib.Path = pathlib.Path(
                DATA_TEMP_DIR
            ) / (gui_image_filepath.stem + ".jpg")

            # Write GUI image (JPEG)
            aim_utils.write_image(
                gui_image_jpeg_base64, gui_image_jpeg_filepath,
            )

            # Execute metric
            results: Optional[List[Any]] = Metric2.execute_metric(
                gui_image_png_base64
            )

            # Test results
            if results is not None:
                assert results[0] == os.stat(gui_image_jpeg_filepath).st_size

    # Public methods
    def test_jpeg_file_sizes(self) -> None:
        """
        Test JPEG file sizes.
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
        self._test(gui_image_filepaths)
