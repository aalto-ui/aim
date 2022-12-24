#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Grid quality


Description:
    Grid quality indicates the internal alignment of the various components
    or identifiable regions of the GUI with respect to each other.

    The code considers each GUI element as a visual block. This metric is
    calculated in two ways, by considering all blocks or only parent blocks.
    Parent blocks are those whose area is on top of another block area
    (child).

    Category: Visual complexity > Information organization > Layout quality.
    For details, see 'Grid quality' [1].


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1. Miniukovich, A. and De Angeli, A. (2015). Computation of Interface
       Aesthetics. In Proceedings of the 33rd Annual ACM Conference on Human
       Factors in Computing Systems (CHI '15), pp. 1163-1172. ACM.
       doi: https://doi.org/10.1145/2702123.2702575

    2. Balinsky, H. (2006). Evaluating Interface Aesthetics: Measure of
       Symmetry. In Digital publishing (Vol. 6076, pp. 52-63). SPIE.
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
    Metric: Grid quality.
    """

    # Private constants
    _G2_PIXEL_TOLERANCE_ROW: int = 2  # 0 or positive
    _G2_PIXEL_TOLERANCE_COLUMN: int = 2  # 0 or positive

    _G3_PIXEL_TOLERANCE_WIDTH: int = 2  # 0 or positive
    _G3_PIXEL_TOLERANCE_HEIGHT: int = 2  # 0 or positive

    _G4_PIXEL_TOLERANCE_WIDTH: int = 2  # 0 or positive
    _G4_PIXEL_TOLERANCE_HEIGHT: int = 2  # 0 or positive

    _G5_PIXEL_TOLERANCE_VERTICAL: int = 2  # 0 or positive

    @classmethod
    def g1_num_visual_blocks(cls, gui_type, segments: List) -> Tuple[int, int]:
        """
        Count the number of visual GUI blocks. For details, see G1 [1].

        Args:
            gui_type: GUI type, desktop = 0 (default), mobile = 1
            segments: List of GUI elements

        Returns:
            - Number of visual GUI blocks (int, [0, +inf))
            - Number of visual GUI blocks - without children (int, [0, +inf))
        """
        # Based on [1], this metric should not apply for mobile GUIs
        if gui_type == GUI_TYPE_MOBILE:
            raise ValueError("The value of 'gui_type' cannot be 1 (mobile).")

        # Count the number of all elements
        num_blocks: int = int(len(segments))

        # Count the number of elements - without children (filter elements that do not have 'parent' as a key)
        num_blocks_woch: int = len(
            list(filter(lambda element: "parent" not in element, segments))
        )

        return num_blocks, num_blocks_woch

    @staticmethod
    def count_points(points: List[int], tolerance: int) -> int:
        """
        Count the number of points with tolerance distance from each other.

        Args:
            points: List of alignment points
            tolerance: Tolerance distance

        Returns:
            - Number of points with tolerance
        """
        points_tol: List[int]

        if len(points) == 0:
            points_tol = points
        else:
            # Sort alignment points
            points = sorted(points)

            # Alignment points with at least tolerance + 1 distance are added
            points_tol = [points[0]]
            for p in points:
                if p - points_tol[-1] > tolerance:
                    points_tol.append(p)

        # Count the number of points
        n_points: int = len(points_tol)
        return n_points

    @classmethod
    def g2_num_alignment_points(
        cls, gui_type, segments: List
    ) -> Tuple[int, int]:
        """
        Count the number of alignment points of GUI blocks. Due to
        segmentation errors, this code considers only points with tolerance
        distances from each other. For details, see G2 [1].

        Args:
            gui_type: GUI type, desktop = 0 (default), mobile = 1
            segments: List of GUI elements

        Returns:
            - Number of alignment points (int, [0, +inf))
            - Number of alignment points - without children (int, [0, +inf))
        """
        # Based on [1], this metric should not apply for mobile GUIs
        if gui_type == GUI_TYPE_MOBILE:
            raise ValueError("The value of 'gui_type' cannot be 1 (mobile).")

        # Compute the alignment points based on columns and rows
        columns: List = []
        rows: List = []
        columns_woch: List = []
        rows_woch: List = []
        for element in segments:
            position = element["position"]
            columns = columns + [
                position["column_min"],
                position["column_max"],
            ]
            rows = rows + [position["row_min"], position["row_max"]]
            # - without children (filter elements that do not have 'parent' as a key)
            if "parent" not in element:
                columns_woch = columns_woch + [
                    position["column_min"],
                    position["column_max"],
                ]
                rows_woch = rows_woch + [
                    position["row_min"],
                    position["row_max"],
                ]

        # Compute the number of all alignment points
        num_align_points: int = cls.count_points(
            points=rows, tolerance=cls._G2_PIXEL_TOLERANCE_ROW
        ) + cls.count_points(
            points=columns, tolerance=cls._G2_PIXEL_TOLERANCE_COLUMN
        )

        # Compute the number of all alignment points - without children (filter elements that do not have 'parent' as a key)
        num_align_points_woch = cls.count_points(
            points=rows_woch, tolerance=cls._G2_PIXEL_TOLERANCE_ROW
        ) + cls.count_points(
            points=columns_woch, tolerance=cls._G2_PIXEL_TOLERANCE_COLUMN
        )

        return num_align_points, num_align_points_woch

    @staticmethod
    def intersection_list(blocks_list: List) -> np.ndarray:
        """
        Compute array of intersection-relation of list elements.

        Args:
            blocks_list: List of differrent shapes of each element with tolerance

        Returns:
            - intersection-realtion array of input list
        """

        # Compute len of input list
        blocks_list_len: int = len(blocks_list)

        # Output intersection  array
        blocks_intersection: np.ndarray = np.zeros(
            (blocks_list_len, blocks_list_len), dtype=int
        )

        # Compute intersections
        for i_block in range(0, blocks_list_len):
            for j_block in range(0, blocks_list_len):
                if j_block > i_block:
                    # check if there is an intersection
                    if bool(
                        set(blocks_list[i_block]) & set(blocks_list[j_block])
                    ):
                        blocks_intersection[i_block, j_block] = 1
                        blocks_intersection[j_block, i_block] = 1

        return blocks_intersection

    @classmethod
    def block_size_relation(
        cls, segments: List, pixel_tolerance_width, pixel_tolerance_height
    ) -> Tuple[np.ndarray, np.ndarray, List[int], List[int]]:
        """
        Compute the relation of elements in terms of shape (considering the
        tolerance).

        Args:
            segments: List of GUI elements
            pixel_tolerance_width: Width pixel tolerance threshold
            pixel_tolerance_height: Height pixel tolerance threshold

        Returns:
            - Relation of elements (blocks) shapes (np.ndarray)
            - Relation of elements (blocks) shapes - without children (np.ndarray)
            - List of ids of elements in relation matrix (blocks) (List)
            - List of ids of elements in relation matrix - without children (List)
        """
        # Compute blocks shapes
        blocks_shapes: List[List[Tuple[int, int]]] = []
        blocks_shapes_woch: List[List[Tuple[int, int]]] = []
        blocks_ids: List[int] = []
        blocks_ids_woch: List[int] = []

        # For each element we also add the shape with tolerances
        for element in segments:
            # Store different shapes with tolerances of each shape
            temp_shapes: List[Tuple[int, int]] = []
            temp_shapes_woch: List[Tuple[int, int]] = []

            # Save the order of ids of elements
            blocks_ids.append(element["id"])
            # Save the order of ids of elements - without considering children
            if "parent" not in element:
                blocks_ids_woch.append(element["id"])

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
                    temp_shapes.append(shape)
                    # Without considering children
                    if "parent" not in element:
                        temp_shapes_woch.append(shape)

            blocks_shapes.append(temp_shapes)
            # If element is not a child
            if len(temp_shapes_woch) > 0:
                blocks_shapes_woch.append(temp_shapes_woch)

        # Find relation between shapes, if they are the same
        blocks_relation = cls.intersection_list(blocks_shapes)
        blocks_relation_woch = cls.intersection_list(blocks_shapes_woch)

        return (
            blocks_relation,
            blocks_relation_woch,
            blocks_ids,
            blocks_ids_woch,
        )

    @classmethod
    def g3_num_block_sizes(cls, segments: List) -> Tuple[int, int]:
        """
        Count the number of block sizes, grid proportionality. This code also
        supports tolerance because of segmentation errors. For details,
        see G3 [1].

        Args:
            segments: List of GUI elements

        Returns:
            - Number of block sizes (int, [0, +inf))
            - Number of block sizes - without children (int, [0, +inf))
        """
        # Number of unique block sizes
        num_block_size: int = 0
        num_block_size_woch: int = 0

        if len(segments) != 0:
            # Compute block size relation
            blocks_relation: np.ndarray
            blocks_relation_woch: np.ndarray
            (
                blocks_relation,
                blocks_relation_woch,
                _,
                _,
            ) = cls.block_size_relation(
                segments,
                pixel_tolerance_width=cls._G3_PIXEL_TOLERANCE_WIDTH,
                pixel_tolerance_height=cls._G3_PIXEL_TOLERANCE_HEIGHT,
            )

            # Compute the number of different block sizes the GUI has
            num_block_size = connected_components(blocks_relation)[0]
            num_block_size_woch = connected_components(blocks_relation_woch)[0]

        return num_block_size, num_block_size_woch

    @staticmethod
    def coverage_mask(
        segments: List,
        blocks_ids: List[int],
        mask_blocks_zeroes: np.ndarray,
        height: int,
        width: int,
    ) -> float:
        """
        Compute the GUI coverage of same size elements.

        Args:
            segments: List of GUI elements
            blocks_ids: List of GUI elements (blocks) ids
            mask_blocks_zeroes: Mask blocks with no same size pair
            height: Height of input GUI
            width: Width of input GUI

        Returns:
            - Relation of elements (blocks) shapes (np.ndarray)
            - Relation of elements (blocks) shapes - without children (np.ndarray)
            - List of ids of elements in relation matrix (blocks) (List)
            - List of ids of elements in relation matrix - without children (List)
        """
        coverage_array = np.zeros((height, width), dtype=int)

        for mask_index in range(0, len(mask_blocks_zeroes)):
            # If it has a same size pair, then:
            if not mask_blocks_zeroes[mask_index]:
                ele = list(
                    filter(
                        (
                            lambda element: blocks_ids[mask_index]
                            == element["id"]
                        ),
                        segments,
                    )
                )[0]
                position = ele["position"]
                coverage_array[
                    position["row_min"] : position["row_max"],
                    position["column_min"] : position["column_max"],
                ] = 1

        gui_coverage = float(np.mean(coverage_array))
        return gui_coverage

    @classmethod
    def g4_gui_coverage(
        cls, segments: List, height, width
    ) -> Tuple[float, float]:
        """
        The proportion of GUI covered by same-size blocks (the cell coverage
        computation from [2]). This code computes the percentage coverage of
        GUI blocks with same size. In other words, it does not consider blocks
        with just one size appearance. For details, see G4 [1].

        Args:
            segments: List of GUI elements
            height: Height of input GUI
            width: Width of input GUI

        Returns:
            - GUI coverage (float, [0, 1])
            - GUI coverage - without children (float, [0, 1])
        """
        if len(segments) != 0:
            # Compute block size relation
            blocks_relation: np.ndarray
            blocks_relation_woch: np.ndarray
            (
                blocks_relation,
                blocks_relation_woch,
                blocks_ids,
                blocks_ids_woch,
            ) = cls.block_size_relation(
                segments,
                pixel_tolerance_width=cls._G4_PIXEL_TOLERANCE_WIDTH,
                pixel_tolerance_height=cls._G4_PIXEL_TOLERANCE_HEIGHT,
            )

            # Find blocks with no same size pair (reverse: find block with at least one same size pair)
            mask_blocks_zeroes = np.all(blocks_relation == 0, axis=1)
            mask_block_woch_zeroes = np.all(blocks_relation_woch == 0, axis=1)

            # Compute the GUI coverage percentage with the same size blocks
            gui_coverage: float = cls.coverage_mask(
                segments, blocks_ids, mask_blocks_zeroes, height, width
            )
            gui_coverage_woch: float = cls.coverage_mask(
                segments,
                blocks_ids_woch,
                mask_block_woch_zeroes,
                height,
                width,
            )

        return gui_coverage, gui_coverage_woch

    @classmethod
    def count_vertical_sizes(cls, vertical_sizes: List[int]) -> int:
        """
        Count the number of vertical sizes with tolerance distance from each
        other.

        Args:
            vertical_sizes: List of alignment points

        Returns:
            Number of vertical sizes with tolerance
        """
        vertical_sizes_tol: List[int]

        if len(vertical_sizes) == 0:
            vertical_sizes_tol = vertical_sizes
        else:
            # Sort vertical sizes
            vertical_sizes = sorted(vertical_sizes)

            # Vertical sizes with at least tolerance + 1 distance are added
            vertical_sizes_tol = [vertical_sizes[0]]
            for p in vertical_sizes:
                if (
                    p - vertical_sizes_tol[-1]
                    > cls._G5_PIXEL_TOLERANCE_VERTICAL
                ):
                    vertical_sizes_tol.append(p)

        # Count the number of vertical sizes
        n_vertical_sizes: int = len(vertical_sizes_tol)
        return n_vertical_sizes

    @classmethod
    def g5_num_vertical_block_sizes(cls, segments: List) -> Tuple[int, int]:
        """
        The number of vertical block sizes, i.e., vertical grid
        proportionality. This code computes the number of different heights
        for blocks in the GUI. For details, see G5 [1].

        Args:
            segments: List of GUI elements

        Returns:
            - Number of vertical block sizes (int, [0, +inf))
            - Number of vertical block sizes - without children (int, [0, +inf))
        """
        # Number of unique vertical sizes
        num_vertical_sizes: int = 0
        num_vertical_sizes_woch: int = 0

        # Compute vertical sizes (height of elements)
        if len(segments) != 0:
            vertical_sizes: List[int] = []
            vertical_sizes_woch: List[int] = []
            for element in segments:
                height = element["height"]
                vertical_sizes.append(height)
                # Without considering children
                if "parent" not in element:
                    vertical_sizes_woch.append(height)

            # Compute unique vertical sizes
            num_vertical_sizes = cls.count_vertical_sizes(vertical_sizes)
            num_vertical_sizes_woch = cls.count_vertical_sizes(
                vertical_sizes_woch
            )

        return num_vertical_sizes, num_vertical_sizes_woch

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
            gui_segments: GUI segments (defaults to None)
            gui_url: GUI URL (defaults to None)

        Returns:
            Results (list of measures)
            - Number of visual GUI blocks (int, [0, +inf))
            - Number of visual GUI blocks - without children (int, [0, +inf))
            - Number of alignment points (int, [0, +inf))
            - Number of alignment points - without children (int, [0, +inf))
            - Number of block sizes (int, [0, +inf))
            - Number of block sizes - without children (int, [0, +inf))
            - GUI coverage (float, [0, 1])
            - GUI coverage - without children (float, [0, 1])
            - Number of vertical block sizes (int, [0, +inf))
            - Number of vertical block sizes - without children (int, [0, +inf))
        """
        # Get all elements
        if gui_segments is not None:
            segments: List = gui_segments["segments"]
            height, width, _ = gui_segments["img_shape"]
        else:
            raise ValueError("The value of 'gui_segments' cannot be 'None'.")

        # Based on [1], G1 and G2 metrics should not apply for mobile GUIs.
        # Compute (non-mobile) grid quality metrics
        g1: Tuple[int, int] = cls.g1_num_visual_blocks(gui_type, segments)
        g2: Tuple[int, int] = cls.g2_num_alignment_points(gui_type, segments)

        # Comptute the rest of grid quality metrics
        g3: Tuple[int, int] = cls.g3_num_block_sizes(segments)
        g4: Tuple[float, float] = cls.g4_gui_coverage(segments, height, width)
        g5: Tuple[int, int] = cls.g5_num_vertical_block_sizes(segments)

        return [
            g1[0],
            g1[1],
            g2[0],
            g2[1],
            g3[0],
            g3[1],
            g4[0],
            g4[1],
            g5[0],
            g5[1],
        ]
