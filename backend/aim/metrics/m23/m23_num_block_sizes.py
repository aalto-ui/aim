#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Number of Block Sizes


Description:
    The number of block sizes, grid proportionality. This metric is
    calculated in two ways, by considering all blocks or only parent blocks.
    Parent blocks are those whose area is on top of another block area (child).
    This code also supports tolerance because of segmentation errors.

    Category: Grid Quality > Number of Block Sizes.
    For details, see G3 [1].

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
import numpy as np
from pydantic import HttpUrl
from scipy.sparse.csgraph import connected_components

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
    Metric: Number of Block Sizes.
    """

    _PIXEL_TOLERANCE_WIDTH: int = 0  # 0 or positive
    _PIXEL_TOLERANCE_HEIGHT: int = 0  # 0 or positive

    @staticmethod
    def block_size_relation(
        segments: List, pixel_tolerance_width, pixel_tolerance_height
    ) -> Tuple[np.ndarray, np.ndarray, List[int], List[int]]:
        """
        Execute the metric.

        Args:
            segments: List of GUI elements
            pixel_tolerance_width: width pixel tolerance threshold
            pixel_tolerance_height: height pixel tolerance threshold

        Returns:
            Relation of elements (blocks) sizes W children (np.ndarray)
            Relation of elements (blocks) sizes W/O children (np.ndarray)
            List of ids of elements in relation matrix (blocks) W children (List)
            List of ids of elements in relation matrix W/O children (List)
        """

        # Compute block sizes
        block_size_total: List[List[Tuple[int, int]]] = []
        block_size_total_without_children: List[List[Tuple[int, int]]] = []
        block_ids: List[int] = []
        block_ids_without_children: List[int] = []

        # For each of element we also add the shape with tolerances.
        for element in segments:

            # Store different shapes with tolerances of each shape
            block_shapes: List[Tuple[int, int]] = []
            block_shapes_without_children: List[Tuple[int, int]] = []

            # Save order of id of elements
            block_ids.append(element["id"])
            # W/O considering children
            if not element.get("parent", None):
                block_ids_without_children.append(element["id"])

            for w_tol in range(
                pixel_tolerance_width,
                -1 * pixel_tolerance_width - 1,
                -1,
            ):
                for h_tol in range(
                    pixel_tolerance_height,
                    -1 * pixel_tolerance_height - 1,
                    -1,
                ):
                    shape = (
                        element["width"] + w_tol,
                        element["height"] + h_tol,
                    )
                    block_shapes.append(shape)
                    # W/O considering children
                    if not element.get("parent", None):
                        block_shapes_without_children.append(shape)

            block_size_total.append(block_shapes)
            # if element is not a child
            if len(block_shapes_without_children) > 0:
                block_size_total_without_children.append(
                    block_shapes_without_children
                )

        # Find relation between shapes, if they are the same.
        blocks_total_len: int = len(block_size_total)
        blocks_relation: np.ndarray = np.zeros(
            (blocks_total_len, blocks_total_len), dtype=int
        )
        for i_block in range(0, blocks_total_len):
            for j_block in range(0, blocks_total_len):
                if j_block > i_block:
                    if bool(
                        set(block_size_total[i_block])
                        & set(block_size_total[j_block])
                    ):
                        blocks_relation[i_block, j_block] = 1
                        blocks_relation[j_block, i_block] = 1

        # Find relation between shapes, if they are the same (without children)
        blocks_total_without_children_len: int = len(
            block_size_total_without_children
        )
        blocks_relation_without_children: np.ndarray = np.zeros(
            (
                blocks_total_without_children_len,
                blocks_total_without_children_len,
            ),
            dtype=int,
        )
        for i_block in range(0, blocks_total_without_children_len):
            for j_block in range(0, blocks_total_without_children_len):
                if j_block > i_block:
                    if bool(
                        set(block_size_total_without_children[i_block])
                        & set(block_size_total_without_children[j_block])
                    ):
                        blocks_relation_without_children[i_block, j_block] = 1
                        blocks_relation_without_children[j_block, i_block] = 1

        return (
            blocks_relation,
            blocks_relation_without_children,
            block_ids,
            block_ids_without_children,
        )

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
            - Number of Block Sizes (int, [0, +inf))
        """

        # Get all elements
        if gui_segments is not None:
            segments: List = gui_segments["segments"]
        else:
            raise ValueError(
                "This Metric requires gui_segments to be not None"
            )

        # Number of Unique block sizes
        num_block_size: int = 0
        num_block_size_without_children: int = 0

        if len(segments) != 0:

            # Compute block size relation
            blocks_relation: np.ndarray
            blocks_relation_without_children: np.ndarray
            (
                blocks_relation,
                blocks_relation_without_children,
                _,
                _,
            ) = cls.block_size_relation(
                segments,
                pixel_tolerance_width=cls._PIXEL_TOLERANCE_WIDTH,
                pixel_tolerance_height=cls._PIXEL_TOLERANCE_HEIGHT,
            )

            # Compute number of different block sizes the GUI have
            num_block_size = connected_components(blocks_relation)[0]
            num_block_size_without_children = connected_components(
                blocks_relation_without_children
            )[0]

        return [num_block_size, num_block_size_without_children]
