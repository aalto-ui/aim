#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
     Hasler and Susstrunk Colorfulness


Description:
    This metric was proposed by Hasler and Susstrunk. This metric is proven to have a very high
    correspondence to the users perception (95%). It relies on the RGYB color spectrum and mainly
    looks at the average standard deviation for all value. The higher the STD is, the more colourful
    the image is perceived. The nested loop however make it more computational heavy than it was
    originally intended. Also, it should be noted that this does not the Hue into account, which has
    been proven to be a significant factor.
    Category: Color variability.

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
    Metric: Hasler and Susstrunk Colorfulness.
    """

    # Private constants
    _CF_COEF: float = 0.3  # a magic coefficient for computing colorfulness

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
            - Colorfulness (float, [0, +inf))
        """

        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get NumPy array
        img_rgb_nparray: np.ndarray = np.array(img_rgb)

        # GET RGB
        blue: np.ndarray = img_rgb_nparray[:, :, 0].copy()
        green: np.ndarray = img_rgb_nparray[:, :, 1].copy()
        red: np.ndarray = img_rgb_nparray[:, :, 2].copy()

        # Compute Red-Green and Yellow-Blue
        rg: np.ndarray = abs(red - green)
        yb: np.ndarray = abs((0.5 * (red + green)) - blue)

        # Compute Metrics based on the Hassler & Susstrunk's paper.
        meanRG: float = float(np.mean(rg))
        stdRG: float = float(np.std(rg))
        meanYB: float = float(np.mean(yb))
        stdYB: float = float(np.std(yb))
        meanRGYB: float = float(np.sqrt(meanRG**2 + meanYB**2))
        stdRGYB: float = float(np.sqrt(stdRG**2 + stdYB**2))
        colourfulness: float = float(stdRGYB + cls._CF_COEF * meanRGYB)

        return [colourfulness]
