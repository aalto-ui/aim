#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    White space


Description:
    The proportion of white space.

    Category: Visual complexity > Layout quality.
    For details, see 'White space' [1].


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
    Metric: White space.
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
            gui_segments: GUI segments (defaults to None)
            gui_url: GUI URL (defaults to None)

        Returns:
            Results (list of measures)
            - White space (float, [0, 1])
        """
        # Based on [1] this metric should not apply for mobile GUIs.
        if gui_type == GUI_TYPE_MOBILE:
            raise ValueError("The value of 'gui_type' cannot be 1 (mobile).")

        if gui_segments is not None:
            # Create a binary array (default = 1) with the same size of image
            height, width, _ = gui_segments["img_shape"]
            segments: List = gui_segments["segments"]
            img_binary = np.ones((height, width), dtype=int)

            # Fill the binary array with 0 for the elements
            for element in segments:
                position = element["position"]
                img_binary[
                    position["row_min"] : position["row_max"],
                    position["column_min"] : position["column_max"],
                ] = 0

            # Compute white space (percentage)
            white_space: float = float(np.mean(img_binary))
        else:
            raise ValueError("The value of 'gui_segments' cannot be 'None'.")

        return [
            white_space,
        ]
