#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Subband entropy


Description:
    The amount of redundancy introduced to a scene.

    Category: Visual complexity > Information amount > Visual clutter.
    For details, see CL2 [1], A10 [2], and CL2 [3].


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Miniukovich, A. and De Angeli, A. (2015). Computation of Interface
        Aesthetics. In Proceedings of the 33rd Annual ACM Conference on Human
        Factors in Computing Systems (CHI '15), pp. 1163-1172. ACM.
        doi: https://doi.org/10.1145/2702123.2702575

    2.  Miniukovich, A. and De Angeli, A. (2014). Visual Impressions of Mobile
        App Interfaces. In Proceedings of the 8th Nordic Conference on
        Human-Computer Interaction (NordiCHI '14), pp. 31-40. ACM.
        doi: https://doi.org/10.1145/2639189.2641219

    3.  Miniukovich, A. and De Angeli, A. (2014). Quantification of Interface
        Visual Complexity. In Proceedings of the 2014 International Working
        Conference on Advanced Visual Interfaces (AVI '14), pp. 153-160. ACM.
        doi: https://doi.org/10.1145/2598153.2598173

    4.  Rosenholtz, R., Li, Y., and Nakano, L. (2007). Measuring Visual
        Clutter. Journal of Vision, 7(2), 1-22.
        doi: https://doi.org/10.1167/7.2.17


Change log:
    v1.0 (2021-08-28)
      * Initial implementation
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
from io import BytesIO
from typing import Dict, List, Optional, Union

# Third-party modules
import numpy as np
import pyrtools as pt
from PIL import Image

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.common.image_visual_clutter_utils import entropy, rgb2lab
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2021-08-28"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Subband entropy.
    """

    # Private constants
    _W_LEVELS: int = (
        3  # the number of spatial scales for the subband decomposition
    )
    _WGHT_CHROM: float = 0.0625  # the weight on chrominance
    _WOR: int = 4  # the number of orientations for the subband decomposition
    _ZERO_THRESHOLD: float = (
        0.008  # threshold to consider an array as a zeros array
    )

    # Private methods
    @classmethod
    def _band_entropy(cls, map_: np.ndarray) -> List[float]:
        """
        Compute Shannon entropies of all the subbands.

        Args:
            map_: a monochromatic image

        Returns:
            A list containing Shannon entropies of all the subbands
        """
        # Decompose the image into subbands
        SFpyr = pt.pyramids.SteerablePyramidFreq(
            map_, height=cls._W_LEVELS, order=cls._WOR - 1
        )
        S = SFpyr.pyr_coeffs

        en_band = []
        for ind in S.keys():
            en_band.append(entropy(S[ind].ravel()))

        return en_band

    # Public methods
    @classmethod
    def execute_metric(
        cls, gui_image: str, gui_type: int = GUI_TYPE_DESKTOP
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1

        Returns:
            Results (list of measures)
            - Subband entropy (float, [0, +inf))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get NumPy array
        img_rgb_nparray: np.ndarray = np.array(img_rgb)

        # Convert image into the perceptually-based CIELab color space
        lab: np.ndarray = rgb2lab(img_rgb_nparray)
        lab_float: np.ndarray = lab.astype(np.float32)

        # Split image to the luminance (L) and chrominance (a,b) channels
        L: np.ndarray = lab_float[:, :, 0]
        a: np.ndarray = lab_float[:, :, 1]
        b: np.ndarray = lab_float[:, :, 2]

        # Compute subband entropy for the luminance channel
        en_band: List[float] = cls._band_entropy(L)
        clutter_se: float = float(np.mean(en_band))

        # Compute subband entropy for the chrominance channels
        for jj in [a, b]:
            if np.max(jj) - np.min(jj) < cls._ZERO_THRESHOLD:
                jj = np.zeros_like(jj)

            en_band = cls._band_entropy(jj)
            clutter_se = float(clutter_se + cls._WGHT_CHROM * np.mean(en_band))

        clutter_se = clutter_se / (1 + 2 * cls._WGHT_CHROM)

        return [
            clutter_se,
        ]
