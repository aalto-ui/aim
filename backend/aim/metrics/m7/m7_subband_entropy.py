#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Subband Entropy clutter measure


Description:
    This measure (Subband Entropy) of visual clutter is based on the notion
    that clutter is related to the number of bits required for subband
    (wavelet) image coding.

    Category: Visual complexity > Information discriminability.
    For details, see 'Subband Entropy clutter measure' [1].


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Rosenholtz, Ruth, Yuanzhen Li, and Lisa Nakano.
        "Measuring visual clutter." Journal of vision 7.2 (2007): 17-17.
        doi:https://doi.org/10.1167/7.2.17

Change log:
    v1.0 (2021-08-27)
      * Initial implementation

"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union

# Third-party modules
import numpy as np
from PIL import Image
import pyrtools as pt

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface
from aim.common.image_visual_clutter_utils import rgb2lab, entropy
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
    Metric: Subband Entropy clutter measure.
    """

    # Private constants
    _W_LEVELS: int = 3 # the number of spatial scales for the subband decomposition
    _WGHT_CHROM: float = 0.0625 # the weight on chrominance 
    _WOR: int = 4 # the number of orientations for the subband decomposition
    
    # Private methods
    @classmethod
    def _band_entropy(
        cls,
        map_: np.ndarray,
    ) -> List:
        """
        Compute Shannon entropies of all the subbands.

        Args:
            map_: a monochromatic image
            
        Returns:
            a list containing Shannon entropies of all the subbands.
        """
   
        # Decompose the image into subbands
        SFpyr = pt.pyramids.SteerablePyramidFreq(map_, height=cls._W_LEVELS, order=cls._WOR-1)
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
            - Subband Entropy (float)
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get NumPy array
        img_rgb_nparray: np.ndarray = np.array(img_rgb)

        # Convert image into the perceptually-based CIELab color space.
        lab = rgb2lab(img_rgb_nparray)
        lab_float = lab.astype(np.float32)
        
        # Split image to luminance(L) and the chrominance(a,b) channels
        L = lab_float[:,:,0]
        a = lab_float[:,:,1]
        b = lab_float[:,:,2]

        # Compute subband entropy for luminance channel
        en_band = cls._band_entropy(L)
        clutter_se = np.mean(en_band)

        # Compute subband entropy for chrominance channels
        for jj in [a, b]:
            if np.max(jj)-np.min(jj) < 0.008:
                jj = np.zeros_like(jj)

            en_band = cls._band_entropy(jj)
            clutter_se = clutter_se + cls._WGHT_CHROM * np.mean(en_band)

        clutter_se = clutter_se/(1 + 2 * cls._WGHT_CHROM)   
    
        return [
            clutter_se,
        ]
