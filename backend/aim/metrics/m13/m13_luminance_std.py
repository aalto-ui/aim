#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Luminance standard deviation


Description:
    The standard deviation of pixel luminance.

    Category: Visual complexity > Information amount > Color variability.
    For details, see C9 [1].

    In the reference, there is no specific type of luminance recommended,
    so the type is determined based on the legacy implementation.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Miniukovich, A. and De Angeli, A. (2014). Quantification of Interface
        Visual Complexity. In Proceedings of the 2014 International Working
        Conference on Advanced Visual Interfaces (AVI '14), pp. 153-160. ACM.
        doi: https://doi.org/10.1145/2598153.2598173


Change log:
    v2.0 (2022-05-25)
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
from typing import Any, Dict, List, Optional, Union

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

__author__ = "Amir Hossein Kargaran, Markku Laine, Thomas Langerak"
__date__ = "2022-05-25"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Luminance standard deviation.
    """

    # Private constants
    _L_COEF: List[float] = [
        0.2126,
        0.7152,
        0.0722,
    ]  # Rec. 709 luma coefficients, https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-E.pdf

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
            - Luminance standard deviation (float, [0, +inf))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get NumPy array
        img_rgb_nparray: np.ndarray = np.array(img_rgb).astype(float)

        # Get RGB
        red: np.ndarray = img_rgb_nparray[:, :, 0]
        green: np.ndarray = img_rgb_nparray[:, :, 1]
        blue: np.ndarray = img_rgb_nparray[:, :, 2]

        # In the reference, there is no specific type of luminance
        # recommended, so the type is determined based on the legacy
        # implementation.
        # Based on: https://en.wikipedia.org/wiki/Luma_(video)
        # Y = 0.2126 R + 0.7152 G + 0.0722 B
        luminance: np.ndarray = (
            cls._L_COEF[0] * red
            + cls._L_COEF[1] * green
            + cls._L_COEF[2] * blue
        )

        # Compute luminance standard deviation
        luminance_std: float = float(np.std(luminance))

        return [
            luminance_std,
        ]
