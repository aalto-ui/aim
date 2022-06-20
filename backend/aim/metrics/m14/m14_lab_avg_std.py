#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    LAB Average and Standard Derivation


Description:
    LAB colour space Average and Standard Derivation.
    Category: Colour Perception > Color Range > LAB Average and Standard Derivation.

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
from typing import List, Optional, Union

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
    Metric: LAB Average and Standard Derivation.
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
            - L average (float, [0, +inf))
            - L std (float, [0, +inf))
            - A average (float, [0, +inf))
            - A std (float, [0, +inf))
            - B average (float, [0, +inf))
            - B std (float, [0, +inf))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get NumPy array
        img_rgb_nparray: np.ndarray = np.array(img_rgb)

        # Convert the LAB space
        lab: np.ndarray = color.rgb2lab(img_rgb_nparray)

        L: np.ndarray = lab[:, :, 0]
        A: np.ndarray = lab[:, :, 1]
        B: np.ndarray = lab[:, :, 2]

        # Get average and standard deviation for each value separately
        meanL: float = float(np.mean(L))
        stdL: float = float(np.std(L))
        meanA: float = float(np.mean(A))
        stdA: float = float(np.std(A))
        meanB: float = float(np.mean(B))
        stdB: float = float(np.std(B))

        return [
            meanL,
            stdL,
            meanA,
            stdA,
            meanB,
            stdB,
        ]
