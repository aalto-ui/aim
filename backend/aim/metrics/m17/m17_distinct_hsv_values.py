#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Distinct values of Hue, Saturation, and Value


Description:
    The number of distinct values in the HSV color space after color
    reduction; only values covering more than 0.1% of image are counted.

    Category: Visual complexity > Information amount > Color variability >
    Color range. For details, see A5-A7 [1] and C1-C3 [2].


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Miniukovich, A. and De Angeli, A. (2014). Visual Impressions of Mobile
        App Interfaces. In Proceedings of the 8th Nordic Conference on
        Human-Computer Interaction (NordiCHI '14), pp. 31-40. ACM.
        doi: https://doi.org/10.1145/2639189.2641219

    2.  Miniukovich, A. and De Angeli, A. (2014). Quantification of Interface
        Visual Complexity. In Proceedings of the 2014 International Working
        Conference on Advanced Visual Interfaces (AVI '14), pp. 153-160. ACM.
        doi: https://doi.org/10.1145/2598153.2598173

    3.  Hasler, D. and Suesstrunk, S.E. (2003). Measuring Colorfulness in
        Natural Images. In Human Vision and Electronic Imaging VIII, 5007,
        87-95. SPIE. doi: https://doi.org/10.1117/12.477378


Change log:
    v2.0 (2022-05-26)
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
import numpy as np
from PIL import Image
from pydantic import HttpUrl

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine, Thomas Langerak, Yuxi Zhu"
__date__ = "2022-06-15"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Distinct values of Hue, Saturation, and Value.
    """

    # Private constants
    _COLOR_REDUCTION_THRESHOLD_RATIO: float = (
        0.001  # Threshold for minimum occuring of values: 0.1 %
    )

    # Public methods
    @classmethod
    def execute_metric(
        cls,
        gui_image: str,
        gui_type: int = GUI_TYPE_DESKTOP,
        gui_url: Optional[HttpUrl] = None,
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1
            gui_url: GUI URL (defaults to None)

        Returns:
            Results (list of measures)
            - Number of distinct Hue values (int, [1, 255])
            - Number of distinct Saturation values (int, [1, 255])
            - Number of distinct Value values (int, [1, 255])
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to HSV color space
        # Note that all three values (Hue, Satuation, and Value) are between
        # (0, 255): https://github.com/python-pillow/Pillow/issues/3650
        img_hsv: Image.Image = img.convert("HSV")

        # Calculate total number of image pixels
        total_pixels: int = img_hsv.width * img_hsv.height

        # Set color reduction threshold
        color_reduction_threshold: int = int(
            total_pixels * cls._COLOR_REDUCTION_THRESHOLD_RATIO
        )

        # Get HSV color histogram
        hsv_color_histogram: List[Tuple[int, Tuple]] = img_hsv.getcolors(
            maxcolors=total_pixels
        )

        # Create lists to store values of HSV, Hue, Saturation, and Value from the histogram
        hue_values: List[int] = []
        saturation_values: List[int] = []
        value_values: List[int] = []

        # Collect distinct HSV values (and their associated Hue, Saturation, and Value values) after color reduction
        for hist in list(hsv_color_histogram):
            hist_count, hist_value = hist
            if hist_count > color_reduction_threshold:
                h, s, v = hist_value
                hue_values.append(h)
                saturation_values.append(s)
                value_values.append(v)

        # Calculate number of distinct Hue, Saturation, and Value values
        n_distinct_hue_values: int = len(set(hue_values))
        n_distinct_saturation_values: int = len(set(saturation_values))
        n_distinct_value_values: int = len(set(value_values))

        return [
            n_distinct_hue_values,
            n_distinct_saturation_values,
            n_distinct_value_values,
        ]
