#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Number of Visual Blocks


Description:
    The number of visual GUI blocks.
    The code considers each GUI element as a visual block. This metric is
    calculated in two ways, by considering all blocks or only parent blocks.
    Parent blocks are those whose area is on top of another block area (child).

    Category: Grid Quality > Number of Visual Blocks.
    For details, see G1 [1].


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
from typing import Any, Dict, List, Optional, Union

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
    Metric: Number of Visual Blocks.
    """

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
            - Number of Visual Blocks (int, [0, +inf))
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

        # Get elements without considering children: Filter elements that do not have 'parent' as a key
        segments_without_children: List = list(
            filter(lambda element: not element.get("parent", None), segments)
        )

        # Count number of all elements
        num_vis_blocks_with_children: int = int(len(segments))
        # Count number of elements without considering children
        num_vis_blocks_without_children: int = int(
            len(segments_without_children)
        )

        return [num_vis_blocks_with_children, num_vis_blocks_without_children]
