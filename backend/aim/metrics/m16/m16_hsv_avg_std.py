#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    HSV average and standard deviation


Description:
    HSV color space average and standard deviation.

    The HSV (Hue, Saturation, Value) color space aligns more closely with the
    human visual system. These metrics report average and standard deviation
    for each channel in HSV. Empirical research has shown hue and saturation
    channels to correlated with aesthetic impression.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Hasler, D. and Suesstrunk, S.E. (2003). Measuring Colorfulness in
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
from typing import List, Optional, Union

# Third-party modules
import numpy as np
from PIL import Image
from pydantic import HttpUrl

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface
from aim.metrics.m16.utils import atan2d, np_cosd, np_sind

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
    Metric: HSV average and standard deviation.
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
            - Hue average (float, [0, +inf))
            - Saturation average (float, [0, +inf))
            - Saturation standard deviation (float, [0, +inf))
            - Value average (float, [0, +inf))
            - Value standard deviation (float, [0, +inf))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to HSV color space
        # Note that all three values (Hue, Satuation, and Value) are between
        # (0, 255): https://github.com/python-pillow/Pillow/issues/3650
        img_hsv: Image.Image = img.convert("HSV")

        # Get NumPy array
        # Multiplication / division is needed to get proper values for Hue,
        # Saturation and Value (0 to 359, 0 to 1, 0 to 1, respectively).
        img_hsv_nparray: np.ndarray = np.array(img_hsv) / 255.0
        img_hue: np.ndarray = img_hsv_nparray[:, :, 0].copy() * 359.0
        img_saturation: np.ndarray = img_hsv_nparray[:, :, 1].copy()
        img_value: np.ndarray = img_hsv_nparray[:, :, 2].copy()

        # Hue is an angle, so cannot simply add and average it
        # Based on: http://mkweb.bcgsc.ca/color-summarizer/?faq#averagehue
        hue_avg_sin: float = float(np.mean(np_sind(img_hue)))
        hue_avg_cos: float = float(np.mean(np_cosd(img_hue)))
        hue_avg: float = float(atan2d(hue_avg_cos, hue_avg_sin))

        # Compute average and standard deviation for Saturation and Value
        saturation_avg: float = float(np.mean(img_saturation))
        saturation_std: float = float(np.std(img_saturation))
        value_avg: float = float(np.mean(img_value))
        value_std: float = float(np.std(img_value))

        return [
            hue_avg,
            saturation_avg,
            saturation_std,
            value_avg,
            value_std,
        ]
