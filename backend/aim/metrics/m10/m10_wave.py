#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    WAVE (Weighted Affective Valence Estimates)


Description:
    This is the mean of a simple mapping of pixel colors to the color preference values
    experimentally obtained by Palmer and Schloss.

    Category: Colour Perception.

    Details: Under their hypothesis that people's color preferences reflect their dispositions
    towards objects of those colors, they had participants grade their feelings towards
    sets of objects of particular colors, and used those gradings to construct these
    color preference values.
    It should be noted that these preferences are likely significantly influenced by
    sociocultural factors, and thus this particular set of preference values may not
    accurately reflect all website visitors' impressions of the color scheme.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Palmer, S.E. and Schloss, K.B., (2010). An ecological valence theory of human color preference.
        Proceedings of the National Academy of Sciences, 107(19), pp.8877-8882.
        doi: https://doi.org/10.1073/pnas.0906172107


Change log:
    v2.0 (2022-05-11)
      * Revised implementation

    v1.0 (2018-11-23)
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

__author__ = "Amir Hossein Kargaran, Markku Laine, Yustynn Panicker"
__date__ = "2022-05-11"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Average WAVE score (Weighted Affective Valence Estimates).
    """

    # Private constants
    _WAVE_COLOR_TO_SCORE = {
        (24, 155, 154): 0.6377440347071583,
        (37, 152, 114): 0.7125813449023862,
        (59, 125, 181): 0.7396963123644252,
        (86, 197, 208): 0.8297180043383949,
        (96, 163, 215): 1.0,
        (101, 190, 131): 0.648590021691974,
        (115, 56, 145): 0.8080260303687636,
        (124, 159, 201): 0.8318872017353579,
        (126, 152, 68): 0.3579175704989154,
        (129, 199, 144): 0.5726681127982647,
        (133, 204, 208): 0.5932754880694144,
        (156, 78, 155): 0.6843817787418656,
        (159, 90, 48): 0.18329718004338397,
        (162, 32, 66): 0.8481561822125814,
        (162, 115, 167): 0.7451193058568331,
        (162, 149, 59): 0.0,
        (164, 219, 228): 0.7028199566160521,
        (170, 194, 228): 0.7537960954446855,
        (177, 200, 101): 0.33731019522776573,
        (179, 208, 68): 0.4652928416485901,
        (184, 158, 199): 0.63882863340564,
        (193, 224, 196): 0.46095444685466386,
        (204, 119, 141): 0.4859002169197397,
        (208, 154, 119): 0.39154013015184386,
        (218, 198, 118): 0.49132321041214755,
        (224, 231, 153): 0.2928416485900217,
        (235, 45, 92): 0.5488069414316703,
        (242, 149, 185): 0.4577006507592191,
        (243, 145, 51): 0.7114967462039046,
        (251, 200, 166): 0.3741865509761389,
        (252, 232, 158): 0.5140997830802604,
        (253, 228, 51): 0.7201735357917572,
    }

    _MATCH_COLORS = list(_WAVE_COLOR_TO_SCORE.keys())
    _NUM_MATCH_COLORS = len(_MATCH_COLORS)

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
            - Average WAVE score across pixels (float, [0, 1))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get NumPy array
        img_rgb_nparray: np.ndarray = np.array(img_rgb)

        ax1, ax2, _ = img_rgb_nparray.shape

        # repeated values for every possible match color
        repeated_img_nparray = np.tile(
            img_rgb_nparray, cls._NUM_MATCH_COLORS
        ).reshape(ax1, ax2, cls._NUM_MATCH_COLORS, 3)

        l2_norms = (
            (repeated_img_nparray - np.array(cls._MATCH_COLORS)) ** 2
        ).sum(axis=3)

        match_indices = l2_norms.argmin(axis=2).flatten()
        wave_values: list = [
            cls._WAVE_COLOR_TO_SCORE[cls._MATCH_COLORS[i]]
            for i in match_indices
        ]
        wave_mean: float = np.mean(wave_values)

        return [
            wave_mean,
        ]
