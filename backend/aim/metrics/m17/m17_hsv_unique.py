#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    HSV Unique


Description:
    Hasler & Susstrunk validated this metric in their paper.
    It looks at the number of unique values in the HSV colour space.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Hasler, D. and Suesstrunk, S.E. (2003). Measuring colorfulness in natural
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
from skimage import color

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine, Thomas Langerak, Yuxi Zhu"
__date__ = "2022-05-26"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: HSV Unique.
    """

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
            - Number of Unique HSV  (int, [0, +inf))
            - Number of Unique Hue (int, [0, +inf))
            - Number of Unique Saturation (int, [0, +inf))
            - Number of Unique Value (int, [0, +inf))
        """

        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to HSV color space
        # Note that all 3 H,S,V values are between (0, 255): https://github.com/python-pillow/Pillow/issues/3650
        img_hsv: Image.Image = img.convert("HSV")

        # Calculate total number of image pixels
        total_pixels: int = img_hsv.width * img_hsv.height

        # Get HSV color histogram
        hsv_color_histogram: List[Tuple[int, Tuple]] = img_hsv.getcolors(
            maxcolors=total_pixels
        )

        hsv_unique: List = []
        hsv_count: List = []
        h_list: List = []
        s_list: List = []
        v_list: List = []

        # Create list from histogram
        for hist in list(hsv_color_histogram):
            hist_count, hist_value = hist
            hsv_unique.append(hist_value)
            hsv_count.append(hist_count)
            h, s, v = hist_value
            h_list.append(h)
            s_list.append(s)
            v_list.append(v)

        # Get all unique values, still has all counts (so no minimal occurence). This probably needs some changing in
        # the future
        h_num_unq: int = len(np.unique(h_list))
        s_num_unq: int = len(np.unique(s_list))
        v_num_unq: int = len(np.unique(v_list))

        new_hsv: List = []
        # Only often enough occuring values for hsv
        for u, c in zip(hsv_unique, hsv_count):
            if c > 5:
                new_hsv.append(u)

        hsv_num_unq: int = len(new_hsv)
        return [hsv_num_unq, h_num_unq, s_num_unq, v_num_unq]
