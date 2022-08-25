#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Number of Alignment Points of Blocks


Description:
    The number of alignment points of GUI blocks. This metric is
    calculated in two ways, by considering all blocks or only parent blocks.
    Parent blocks are those whose area is on top of another block area (child).
    Moreover, due to segmentation errors, this code considers only points with
    tolerance distances from each other.

    Category: Grid Quality > Number of Alignment Points of Blocks.
    For details, see G2 [1].


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Miniukovich, A. and De Angeli, A. (2015). Computation of Interface
        Aesthetics. In Proceedings of the 33rd Annual ACM Conference on Human
        Factors in Computing Systems (CHI '15), pp. 1163-1172. ACM.
        doi: https://doi.org/10.1145/2702123.2702575

    2. Balinsky, H. (2006). Evaluating interface aesthetics: measure of symmetry.
       In Digital publishing (Vol. 6076, pp. 52-63). SPIE.
       doi: https://doi.org/10.1117/12.642120


Change log:
    v1.0 (2022-08-05)
      * Initial implementation
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import Any, Dict, List, Optional, Tuple, Union

# Third-party modules
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
    Metric: Number of Alignment Points of Blocks.
    """

    _PIXEL_TOLERANCE_ROW: int = 0  # 0 or positive
    _PIXEL_TOLERANCE_COLUMN: int = 0  # 0 or positive

    @classmethod
    def count_points(cls, points: List[int], axis: int = 0) -> int:
        """
        Count number of points with tolerance distance from each other.

        Args:
            points: List of Alignment points
            axis: 0 for rows and 1 for columns, default 0

        Returns:
            number of points with tolerance
        """

        if axis == 1:
            tolerance = cls._PIXEL_TOLERANCE_COLUMN
        else:
            tolerance = cls._PIXEL_TOLERANCE_ROW

        # Sort alignment points
        points = sorted(points)
        # Alignment points with at least tolerance + 1 distance are added
        points_tol: List[int] = [points[0]]
        for p in points:
            if p - points_tol[-1] > tolerance:
                points_tol.append(p)

        # Count number of points
        n_points: int = len(points_tol)
        return n_points

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
            - Number of Alignment Points of Blocks (int, [0, +inf))
        """

        # Based on [1] this metric should not apply for mobile GUIs.
        if gui_type == GUI_TYPE_MOBILE:
            raise ValueError(
                "This Metric requires gui_type to be non mobile (e.g, desktop)"
            )

        # Get all elements
        if gui_segments is not None:
            segments: List = gui_segments["segments"]
        else:
            raise ValueError(
                "This Metric requires gui_segments to be not None"
            )

        # Compute alignment points based on column and rows
        columns: List = []
        rows: List = []
        columns_wo_children: List = []
        rows_wo_children: List = []
        for element in segments:
            position = element["position"]
            columns = columns + [
                position["column_min"],
                position["column_max"],
            ]
            rows = rows + [position["row_min"], position["row_max"]]
            # W/O considering children
            if not element.get("parent", None):
                columns_wo_children = columns_wo_children + [
                    position["column_min"],
                    position["column_max"],
                ]
                rows_wo_children = rows_wo_children + [
                    position["row_min"],
                    position["row_max"],
                ]

        # Compute number of alignment point for row W and W/O children
        num_align_points_row: int = cls.count_points(points=rows, axis=0)
        num_align_points_row_wo_children = cls.count_points(
            points=rows_wo_children, axis=0
        )

        # Compute number of alignment point for column W and W/O children
        num_align_points_column = cls.count_points(points=columns, axis=1)
        num_align_points_column_wo_children = cls.count_points(
            points=columns_wo_children, axis=1
        )

        # Compute number of unique alignment points
        num_align_points: int = num_align_points_row + num_align_points_column
        # Compute number of unique alignment points W/O considering children
        num_align_points_wo_children = (
            num_align_points_row_wo_children
            + num_align_points_column_wo_children
        )

        return [num_align_points, num_align_points_wo_children]
