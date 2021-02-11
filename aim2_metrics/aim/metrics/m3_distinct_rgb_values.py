#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Distinct RGB values


Description:
    The number of distinct values in the RGB color space after color
    reduction; only values covering more than five pixels (for desktop)
    or two pixels (for mobile) are counted.

    Category: Visual complexity > Information amount > Color variability >
    Color range. For details, see CV2 [1], A3 [2], and C4 [3].


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Miniukovich, A. and De Angeli, A. (2015). Computation of Interface
        Aesthetics. In Proceedings of the 33rd Annual ACM Conference on Human
        Factors in Computing Systems (CHI '15), pp. 1163-1172. ACM.
        doi: https://doi.org/10.1145/2702123.2702575

    2.  Miniukovich, A. and De Angeli, A. (2014). Visual Impressions of Mobile
        App Interfaces. In Proceedings of the 8th Nordic Conference on
        Human-Computer Interaction (NordiCHI '14), pp. 31-40. ACM.
        doi: https://doi.org/10.1145/2639189.2641219

    3.  Miniukovich, A. and De Angeli, A. (2014). Quantification of Interface
        Visual Complexity. In Proceedings of the 2014 International Working
        Conference on Advanced Visual Interfaces (AVI '14), pp. 153-160. ACM.
        doi: https://doi.org/10.1145/2598153.2598173


Change log:
    v2.0 (2021-02-11)
      * Revised implementation

    v1.0 (2017-05-29)
      * Initial implementation
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
from io import BytesIO
from typing import List, Optional, Tuple, Union

# Third-party modules
from PIL import Image

# First-party modules
from aim.core.constants import (
    COLOR_REDUCTION_THRESHOLD_DESKTOP,
    COLOR_REDUCTION_THRESHOLD_MOBILE,
    GUI_TYPE_DESKTOP,
    GUI_TYPE_MOBILE,
)
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine, Kseniia Palin, Thomas Langerak, Yuxi Zhu"
__date__ = "2021-02-11"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Distinct RGB values.
    """

    # Public methods
    @staticmethod
    def execute_metric(
        gui_image: str, gui_type: int = GUI_TYPE_DESKTOP
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1

        Returns:
            Results (list of measures)
            - Number of distinct RGB values (int, [0, +inf))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (should be RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Calculate total number of image pixels
        total_pixels: int = img_rgb.width * img_rgb.height

        # Get RGB color histogram
        rgb_color_histogram: List[Tuple[int, Tuple]] = img_rgb.getcolors(
            maxcolors=total_pixels
        )

        # Set color reduction threshold; five (pixels) for desktop GUIs and
        # two (pixels) for mobile GUIs
        color_reduction_threshold: int = (
            COLOR_REDUCTION_THRESHOLD_MOBILE
            if gui_type == GUI_TYPE_MOBILE
            else COLOR_REDUCTION_THRESHOLD_DESKTOP
        )

        # Calculate number of distinct RGB values after color reduction
        n_distinct_rgb_values: int = len(
            set(
                [
                    t
                    for t in rgb_color_histogram
                    if t[0] > color_reduction_threshold
                ]
            )
        )

        return [
            n_distinct_rgb_values,
        ]
