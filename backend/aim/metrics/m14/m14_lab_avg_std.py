#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    LAB average and standard deviation


Description:
    LAB color space average and standard deviation.

    In the reference, there is no specific type of luminance recommended,
    so the type is determined based on the legacy implementation.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Hasler, D. and Suesstrunk, S.E. (2003). Measuring Colorfulness in
        Natural Images. In Human Vision and Electronic Imaging VIII, 5007,
        87-95. SPIE. doi: https://doi.org/10.1117/12.477378


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
from skimage import color

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine, Thomas Langerak, Yuxi Zhu"
__date__ = "2022-05-25"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: LAB average and standard deviation.
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
            - L average (float, [0, 100])
            - L standard deviation (float, [0, +inf))
            - A average (float, [-128, +128])
            - A standard deviation (float, [0, +inf))
            - B average (float, [-128, +128))
            - B standard deviation (float, [0, +inf))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get NumPy array
        img_rgb_nparray: np.ndarray = np.array(img_rgb)

        # Convert to the CIE Lab color space. The color.rgb2lab function gets
        # optional parameters for type of luminance. In the reference, there
        # is no specific type of luminance recommended, so the type is
        # determined based on the legacy implementation. Name of the
        # illuminant types are: {“A”, “B”, “C”, “D50”, “D55”, “D65”, “D75”,
        # “E”}. The default value is: "D65" (CIE standard illuminant).
        # The observer parameter is the aperture angle of the observer.
        # The observer types are: {“2”, “10”, “R”}, The default value is "2".
        # Reference: https://en.wikipedia.org/wiki/Standard_illuminant
        lab: np.ndarray = color.rgb2lab(
            img_rgb_nparray, illuminant="D65", observer="2"
        )

        # Get LAB
        L: np.ndarray = lab[:, :, 0]
        A: np.ndarray = lab[:, :, 1]
        B: np.ndarray = lab[:, :, 2]

        # Compute average and standard deviation for each value separately
        L_avg: float = float(np.mean(L))
        L_std: float = float(np.std(L))
        A_avg: float = float(np.mean(A))
        A_std: float = float(np.std(A))
        B_avg: float = float(np.mean(B))
        B_std: float = float(np.std(B))

        return [
            L_avg,
            L_std,
            A_avg,
            A_std,
            B_avg,
            B_std,
        ]
