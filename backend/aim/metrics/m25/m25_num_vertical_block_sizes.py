#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Number of Vertical Block Sizes


Description:
    The number of vertical block sizes, i.e., vertical grid
    proportionality. This code computes the number of different
    heights for blocks in the GUI.

    Category: Grid Quality > Number of Vertical Block Sizes.
    For details, see G5 [1].


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Miniukovich, A. and De Angeli, A. (2015). Computation of Interface
        Aesthetics. In Proceedings of the 33rd Annual ACM Conference on Human
        Factors in Computing Systems (CHI '15), pp. 1163-1172. ACM.
        doi: https://doi.org/10.1145/2702123.2702575


Change log:
    v1.0 (2022-08-05)
      * Initial implementation
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import Any, Dict, List, Optional, Union

# Third-party modules
import numpy as np
from pydantic import HttpUrl

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP, GUI_TYPE_MOBILE
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-08-05"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Number of Vertical Block Sizes.
    """

    _PIXEL_TOLERANCE_VERTICAL: int = 0  # 0 or positive

    @classmethod
    def count_vertical_sizes(cls, vertical_sizes: List[int]) -> int:
        """
        Count number of vertical sizes with tolerance distance from each other.

        Args:
            vertical_sizes: List of Alignment points

        Returns:
            number of vertical sizes with tolerance
        """

        # Sort vertical sizes
        vertical_sizes = sorted(vertical_sizes)
        # Vertical sizes with at least tolerance + 1 distance are added
        vertical_sizes_tol: List[int] = [vertical_sizes[0]]
        for p in vertical_sizes:
            if p - vertical_sizes_tol[-1] > cls._PIXEL_TOLERANCE_VERTICAL:
                vertical_sizes_tol.append(p)

        # Count number of vertical sizes
        n_vertical_sizes: int = len(vertical_sizes_tol)
        return n_vertical_sizes

    # Public methods
    @classmethod
    def execute_metric(
        cls,
        gui_image: str,
        gui_type: int = GUI_TYPE_DESKTOP,
        gui_segments: Optional[Dict[str, Any]] = None,
        gui_url: Optional[HttpUrl] = None,
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1
            gui_segments: GUI segmentation (defaults to None)
            gui_url: GUI URL (defaults to None)

        Returns:
            Results (list of measures)
            - Number of Vertical Block Sizes (int, [0, +inf))
        """

        # Get all elements
        if gui_segments is not None:
            segments: List = gui_segments["segments"]
        else:
            raise ValueError(
                "This Metric requires gui_segments to be not None"
            )

        # Number of Unique vertical sizes
        num_vertical_sizes: int = 0
        num_vertical_sizes_without_children: int = 0

        # Compute vertical sizes (height of elements)
        if len(segments) != 0:
            vertical_sizes: List[int] = []
            vertical_sizes_without_children: List[int] = []
            for element in segments:
                height = element["height"]
                vertical_sizes.append(height)
                # W/O considering children
                if not element.get("parent", None):
                    vertical_sizes_without_children.append(height)

            # Compute unique vertical sizes
            num_vertical_sizes = cls.count_vertical_sizes(vertical_sizes)
            num_vertical_sizes_without_children = cls.count_vertical_sizes(
                vertical_sizes_without_children
            )

        return [num_vertical_sizes, num_vertical_sizes_without_children]
