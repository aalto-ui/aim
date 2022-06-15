#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Distinct HSV values


Description:
    The number of distinct values of Hue, Saturation and Value. Images were converted to the HSV color space.
    Color variability was reduced: only values covering more than 0.1% of image were counted

    Category: Color variability.
    For details, see C1-C3 [2].


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

    3.  Hasler, D. and Suesstrunk, S.E. (2003). Measuring colorfulness in natural
        images. In Human vision and electronic imaging VIII (Vol. 5007, pp. 87-95).
        International Society for Optics and Photonics.
        doi: https://doi.org/10.1117/12.477378


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
    Metric: Distinct HSV values.
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
            - Number of Unique HSV  (int, [1, 255^3))
            - Number of Unique Hue (int, [1, 255])
            - Number of Unique Saturation (int, [1, 255])
            - Number of Unique Value (int, [1, 255])
        """

        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to HSV color space
        # Note that all 3 H,S,V values are between (0, 255): https://github.com/python-pillow/Pillow/issues/3650
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

        # Create lists to store h, s and v individually and together from histogram
        hsv_list_unq: List[Tuple] = []
        h_list: List[int] = []
        s_list: List[int] = []
        v_list: List[int] = []

        #  Calculate number of distinct HSV values after color reduction
        for hist in list(hsv_color_histogram):
            hist_count, hist_value = hist
            if hist_count > color_reduction_threshold:
                hsv_list_unq.append(hist_value)
                h, s, v = hist_value
                h_list.append(h)
                s_list.append(s)
                v_list.append(v)

        # Get all unique values, still has all counts (so no minimal occurence). This probably needs some changing in
        # the future
        h_num_unq: int = len(np.unique(h_list))
        s_num_unq: int = len(np.unique(s_list))
        v_num_unq: int = len(np.unique(v_list))

        # Compute unique number of hsv
        hsv_num_unq: int = len(hsv_list_unq)

        return [hsv_num_unq, h_num_unq, s_num_unq, v_num_unq]
