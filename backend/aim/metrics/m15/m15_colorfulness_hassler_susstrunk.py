#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
     Colorfulness (Hasler and Süsstrunk)


Description:
    The colorfulness in natural images.

    The Hassler-Süsstrunk colorfulness metric is computed based on the RGYB
    color spectrum and mainly comprises standard deviations. The higher the
    deviation, the more colorful the image is perceived. This has a high
    correlation with aesthetic impression, but has been mainly tested with
    natural images not user interfaces. The metric is, however,
    computationally expensive. Note that this metric does not take Hue into
    account.


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
    Metric: Colorfulness.
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
        img_rgb_nparray: np.ndarray = np.array(img_rgb).astype(float)

        # Get RGB
        red: np.ndarray = img_rgb_nparray[:, :, 0]
        green: np.ndarray = img_rgb_nparray[:, :, 1]
        blue: np.ndarray = img_rgb_nparray[:, :, 2]

        # Compute Red-Green and Yellow-Blue
        rg: np.ndarray = red - green
        yb: np.ndarray = 0.5 * (red + green) - blue

        # Compute metrics based on Hassler and Süsstrunk's paper
        rgyb_avg: float = float(np.sqrt(np.mean(rg) ** 2 + np.mean(yb) ** 2))
        rgyb_std: float = float(np.sqrt(np.std(rg) ** 2 + np.std(yb) ** 2))
        colorfulness: float = float(rgyb_std + cls._CF_COEF * rgyb_avg)

        return [
            colorfulness,
        ]
