#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Color harmony


Description:
    The closest harmonic color scheme and distance to it.


Source:
    The utils module contains some code that is imported and adopted from
    https://github.com/tartarskunk/ColorHarmonization.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Cohen-Or, D., Sorkine, O., Gal, R., Leyvand, T., and Xu, Y.Q. (2006).
        Color Harmonization. ACM Transactions on Graphics, 25(3), 624-630.
        doi: https://doi.org/10.1145/1141911.1141933


Change log:
    v1.0 (2022-06-29)
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
import cv2
import matplotlib
import numpy as np
from PIL import Image
from pydantic import HttpUrl

# First-party modules
from aim.common import image_utils
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface
from aim.metrics.m20.utils import (
    HarmonicScheme,
    HueSector,
    count_hue_histogram,
    get_img_from_fig,
    plot_histogram,
)

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-06-29"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Color harmony.
    """

    # Private constants
    # Harmonic templates on the hue wheel based on [1] (see the appendix)
    # List of sectors (center, width)
    _HUE_TEMPLATES: Dict[str, List[Tuple]] = {
        "i": [(0.00, 0.05)],
        "V": [(0.00, 0.26)],
        "L": [(0.00, 0.05), (0.25, 0.22)],
        "mirror_L": [(0.00, 0.05), (-0.25, 0.22)],
        "I": [(0.00, 0.05), (0.50, 0.05)],
        "T": [(0.25, 0.50)],
        "Y": [(0.00, 0.26), (0.50, 0.05)],
        "X": [(0.00, 0.26), (0.50, 0.26)],
    }

    # Number of superpixels: -1 if you don't want to use superpixels
    # More on: https://docs.opencv.org/3.4/df/d81/classcv_1_1ximgproc_1_1SuperpixelSEEDS.html
    _NUM_SUPER_PIXEL = -1

    # Private methods
    @classmethod
    def _get_sectors(
        cls, template_type: str, alpha: Union[float, int]
    ) -> List[HueSector]:
        """
        Compute Shannon entropies of all the subbands.

        Args:
            template_type: Template type (options: 'i', 'V', 'L', 'mirror_L',
                           'I', 'T', 'Y', and 'X')
            alpha: Angle of the template

        Returns:
            A list of HueSectors for the template
        """
        # Compute sectors
        sectors: List[HueSector] = []
        for t in cls._HUE_TEMPLATES[template_type]:
            center: float = t[0] * 360 + float(alpha)
            width: float = t[1] * 360
            sector = HueSector(center, width)
            sectors.append(sector)

        return sectors

    @classmethod
    def _get_schemes(cls, X: np.ndarray) -> Tuple[str, Dict]:
        """
        Compute closest scheme templates.

        Args:
            X: HSV image (np.ndarray)

        Returns:
            - Best-fitting harmonic template (str)
            - Template schemes (Dict)
        """

        N: int = 360
        template_types: List[str] = list(cls._HUE_TEMPLATES.keys())
        num_tamplates: int = len(template_types)
        F_matrix: np.ndarray = np.zeros((num_tamplates, N))

        # Compute all possible (template, alpha) harmonic scores
        for i in range(num_tamplates):
            m: str = template_types[i]
            for alpha in range(N):
                sectors: List[HueSector] = cls._get_sectors(m, alpha)
                harmomic_scheme: HarmonicScheme = HarmonicScheme(sectors)
                F_matrix[i, alpha] = harmomic_scheme.harmony_score(X)

        # Compute best template
        (best_m_idx, _) = np.unravel_index(np.argmin(F_matrix), F_matrix.shape)
        best_m: str = template_types[best_m_idx]

        # Compute the best alpha for each template
        harmomic_schemes: Dict = {}
        for key in cls._HUE_TEMPLATES.keys():
            harmomic_schemes[key] = {
                "alpha": 0,
                "harmonic_scheme": HarmonicScheme([]),
                "distance": 0.0,
            }
        for m_idx, scheme_m in enumerate(cls._HUE_TEMPLATES.keys()):
            # best alpha
            scheme_alpha: int = int(np.argmin(F_matrix[m_idx]))
            harmomic_schemes[scheme_m]["alpha"] = scheme_alpha

            # best distance
            scheme_distance: float = float(F_matrix[m_idx, scheme_alpha])
            harmomic_schemes[scheme_m]["distance"] = scheme_distance

            # build best scheme
            sectors = cls._get_sectors(scheme_m, scheme_alpha)
            harmomic_schemes[scheme_m]["harmonic_scheme"] = HarmonicScheme(
                sectors
            )

        return best_m, harmomic_schemes

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
            - Distance to the closest harmonic template (float, [0, +inf))
            - Harmonized image (str, image (PNG) encoded in Base64)
            - Source and target hues (str, image (PNG) encoded in Base64)
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get NumPy array of RGB image
        img_rgb_arr: np.ndarray = np.array(img_rgb)

        # Convert RGB image (array) to HSV (array)
        img_hsv_arr: np.ndarray = cv2.cvtColor(img_rgb_arr, cv2.COLOR_RGB2HSV)

        # Compute the best harmonic scheme and distance
        best_m, all_harmomic_scheme = cls._get_schemes(img_hsv_arr)
        # Get best scheme
        best_harmomic_scheme: HarmonicScheme = all_harmomic_scheme[best_m][
            "harmonic_scheme"
        ]
        # Get best distance
        best_distance: float = float(all_harmomic_scheme[best_m]["distance"])

        # Compute shifted HSV image (array)
        shifted_img_hsv_arr: np.ndarray = best_harmomic_scheme.hue_shifted(
            img_hsv_arr, num_superpixels=cls._NUM_SUPER_PIXEL
        )

        # Convert shifted HSV image (array) to RGB image (array)
        shifted_img_rgb_arr: np.ndarray = cv2.cvtColor(
            shifted_img_hsv_arr, cv2.COLOR_HSV2RGB
        )

        # Convert shifted RGB image (array) to RGB image (pillow image)
        shifted_im: Image.Image = Image.fromarray(shifted_img_rgb_arr)

        # Convert shifted RGB image (pillow image) to b64 (str)
        shifted_b64: str = image_utils.to_png_image_base64(shifted_im)

        # Compute Hue plots for before (source) and after (target) shifts
        histogram_source: np.ndarray = count_hue_histogram(img_hsv_arr)
        histogram_target: np.ndarray = count_hue_histogram(shifted_img_hsv_arr)

        # Get the plots
        fig_source: matplotlib.figure.Figure = plot_histogram(
            histogram_source, best_harmomic_scheme, "Source Hue"
        )
        fig_target: matplotlib.figure.Figure = plot_histogram(
            histogram_target, best_harmomic_scheme, "Target Hue"
        )

        # Convert Matplotlib plots to arrays
        source_arr: np.ndarray = get_img_from_fig(fig_source)
        target_arr: np.ndarray = get_img_from_fig(fig_target)

        # Concat Source and Target hues side by side
        hues_arr: np.ndarray = np.concatenate((source_arr, target_arr), axis=1)

        # Convert concatenated hue plots to Pillow image format
        hues_im: Image.Image = Image.fromarray(hues_arr)

        # Convert concatenated hue plots to b64 (str)
        hues_b64: str = image_utils.to_png_image_base64(hues_im)

        return [
            best_distance,
            shifted_b64,
            hues_b64,
        ]
