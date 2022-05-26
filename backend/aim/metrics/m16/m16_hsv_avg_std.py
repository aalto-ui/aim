#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    HSV Unique


Description:
    Hasler & Susstrunk validated this metric in their paper. It looks at the average
    value and standard deviation for every value in the HSV colour space.
    Category: Colour Perception > Color Range > HSV Average and Standard Derivation.


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
    Metric: Hassler & Susstrunk.
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
            - Average Hue  (float, [0, +inf))
            - Average Saturation (float, [0, +inf))
            - Standard Deviation of Saturation (float, [0, +inf))
            - Average Value (float, [0, +inf))
            - Standard Deviation of Value (float, [0, +inf))
        """

        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to HSV color space
        # Note that all 3 H,S,V values are between (0, 255): https://github.com/python-pillow/Pillow/issues/3650
        img_hsv: Image.Image = img.convert("HSV")

        # Get NumPy array
        # Mult/Div(s) are needed to get proper values. for hue, saturation and value (0 to 359, 0 to 1, 0 to 1)
        img_hsv_nparray: np.ndarray = np.array(img_hsv) / 255.0
        img_hue: np.ndarray = img_hsv_nparray[:, :, 0].copy() * 359.0
        img_saturation: np.ndarray = img_hsv_nparray[:, :, 1].copy()
        img_value: np.ndarray = img_hsv_nparray[:, :, 2].copy()

        # Hue is an angle, so cannot simple add and average it
        # Based on: http://mkweb.bcgsc.ca/color-summarizer/?faq#averagehue
        avg_hue_sin: float = np.mean(np_sind(img_hue))
        avg_hue_cos: float = np.mean(np_cosd(img_hue))
        avgHue = atan2d(avg_hue_cos, avg_hue_sin) % 360

        avgSaturation: float = np.mean(img_saturation)
        stdSaturation: float = np.std(img_saturation)
        avgValue: float = np.mean(img_value)
        stdValue: float = np.std(img_value)

        return [avgHue, avgSaturation, stdSaturation, avgValue, stdValue]
