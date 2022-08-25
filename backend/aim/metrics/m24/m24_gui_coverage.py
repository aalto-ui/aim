#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    GUI Coverage


Description:
    The proportion of GUI covered by same-size blocks (the cell coverage computation from [2]).
    This code computes the number of gui blocks with same size. It does not consider blocks with
    just one size appearance.

    Category: Grid Quality > GUI Coverage.
    For details, see G4 [1].


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
from aim.metrics.m23.m23_num_block_sizes import Metric as m23

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
    Metric: GUI Coverage.
    """

    _PIXEL_TOLERANCE_WIDTH: int = 2  # 0 or positive
    _PIXEL_TOLERANCE_HEIGHT: int = 2  # 0 or positive

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
            - GUI Coverage (float, [0, 1])
        """
        # Get all elements
        if gui_segments is not None:
            segments: List = gui_segments["segments"]
            height, width, _ = gui_segments["img_shape"]
        else:
            raise ValueError(
                "This Metric requires gui_segments to be not None"
            )

        # GUI coverage percent with the same size blocks
        gui_coverage: float = 0.0
        gui_coverage_without_children: float = 0.0

        if len(segments) != 0:
            # Compute block size relation
            blocks_relation: np.ndarray
            blocks_relation_without_children: np.ndarray
            (
                blocks_relation,
                blocks_relation_without_children,
                block_ids,
                block_ids_without_children,
            ) = m23.block_size_relation(
                segments,
                pixel_tolerance_width=cls._PIXEL_TOLERANCE_WIDTH,
                pixel_tolerance_height=cls._PIXEL_TOLERANCE_HEIGHT,
            )

            # Coverage array
            coverage_array = np.zeros((height, width), dtype=int)
            coverage_array_without_children = np.zeros(
                (height, width), dtype=int
            )

            # Find blocks with no same size pair (reverse: find block with at least one same size pair)
            mask_blocks_zeroes = np.all(blocks_relation == 0, axis=1)
            mask_block_without_children_zeroes = np.all(
                blocks_relation_without_children == 0, axis=1
            )

            # Compute coverage array
            for mask_index in range(0, len(mask_blocks_zeroes)):
                if not mask_blocks_zeroes[mask_index]:
                    ele = list(
                        filter(
                            (
                                lambda element: block_ids[mask_index]
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

            # Compute coverage array (without children)
            for mask_index in range(
                0, len(mask_block_without_children_zeroes)
            ):
                if not mask_block_without_children_zeroes[mask_index]:
                    ele = list(
                        filter(
                            (
                                lambda element: block_ids_without_children[
                                    mask_index
                                ]
                                == element["id"]
                            ),
                            segments,
                        )
                    )[0]
                    position = ele["position"]
                    coverage_array_without_children[
                        position["row_min"] : position["row_max"],
                        position["column_min"] : position["column_max"],
                    ] = 1

            # Compute percentage
            gui_coverage = float(np.mean(coverage_array))
            gui_coverage_without_children = float(
                np.mean(coverage_array_without_children)
            )

        return [gui_coverage, gui_coverage_without_children]
