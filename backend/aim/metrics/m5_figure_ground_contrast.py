#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Figure-ground contrast


Description:
    The difference in color or luminance between two adjacent areas.

    Category: Visual complexity > Information discriminability.
    For details, see 'Figure-ground contrast' [1, 2, 3].


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

    4.  Reber, R., Wurtz, P., and Zimmermann, T.D. (2004). Exploring "fringe"
        Consciousness: The Subjective Experience of Perceptual Fluency and
        its Objective Bases. Consciousness and Cognition, 13(1), 47-60.
        doi: https://doi.org/10.1016/S1053-8100(03)00049-7

    5.  Hall, R.H. and Hanna, P. (2004). The Impact of Web Page
        Text-Background Colour Combinations on Readability, Retention,
        Aesthetics and Behavioural Intention. Behaviour & Information
        Technology, 23(3), 183-195.
        doi: https://doi.org/10.1080/01449290410001669932

    6.  Reber, R., Winkielman, P., and Schwarz, N. (1998). Effects of
        Perceptual Fluency on Affective Judgments. Psychological Science,
        9(1), 45-48. doi: https://doi.org/10.1111/1467-9280.00008


Change log:
    v2.0 (2021-02-11)
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
from typing import List, Optional, Tuple, Union

# Third-party modules
import cv2
import numpy as np
from PIL import Image

# First-party modules
from aim.common.constants import (
    CANNY_EDGE_DETECTION_PYTHON_MAX_THRESHOLD,
    GAUSSIAN_KERNEL_SIZE,
    GAUSSIAN_KERNEL_STANDARD_DEVIATION,
    GUI_TYPE_DESKTOP,
    GUI_TYPE_MOBILE,
)
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine, Thomas Langerak, Yuxi Zhu"
__date__ = "2021-03-19"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Figure-ground contrast.
    """

    # Public methods
    @staticmethod
    def execute_metric(
        gui_image: str, gui_type: int = GUI_TYPE_DESKTOP
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1

        Returns:
            Results (list of measures)
            - Figure-ground contrast (float, [0, 1])
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (should be RGBA) to L (grayscale) color space
        img_l: Image.Image = img.convert("L")

        # Get NumPy array
        img_l_nparray: np.ndarray = np.array(img_l)

        # Gaussian filter parameters
        ksize: Tuple[int, int] = GAUSSIAN_KERNEL_SIZE
        sigma: int = GAUSSIAN_KERNEL_STANDARD_DEVIATION
        # Note 1: ksize.width and ksize.height can differ but they both must
        # be positive and odd. Or, they can be zero's and then they are
        # computed from sigma. For details, see
        # https://docs.opencv.org/4.4.0/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1
        # Note 2: According to the following link
        # (https://dsp.stackexchange.com/questions/4716/differences-between-opencv-canny-and-matlab-canny),
        # OpenCV's GaussianBlur() function
        # (https://docs.opencv.org/4.4.0/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1)
        # with sigma=2 mimics the default sigma (sqrt(2)) in MATLAB Canny.

        # Smooth image
        img_blurred_nparray: np.ndarray = cv2.GaussianBlur(
            src=img_l_nparray, ksize=ksize, sigmaX=sigma, sigmaY=sigma
        )

        # Generate levels (with a step of 1) and luminance levels; from 0.1
        # to 0.7 for desktop GUIs and from 0.05 to 0.65 for mobile GUIs with
        # a step of 0.1
        levels: List[int] = [level for level in range(1, 8, 1)]
        luminance_levels: List[float] = (
            [round(0.1 * (level - 0.5), 2) for level in levels]
            if gui_type == GUI_TYPE_MOBILE
            else [round(0.1 * level, 1) for level in levels]
        )

        # Canny edge detection parameters
        high_thresholds: List[float] = [
            round(
                CANNY_EDGE_DETECTION_PYTHON_MAX_THRESHOLD * luminance_level, 2
            )
            for luminance_level in luminance_levels
        ]
        low_thresholds: List[float] = [
            round(0.4 * high_threshold, 2)
            for high_threshold in high_thresholds
        ]  # 40% of high thresholds
        # Note 1: According to [2, 3], high thresholds varied from 0.1 to 0.7
        # and from 0.05 to 0.65 (MATLAB) with a step of 0.1 for desktop GUIs
        # and mobile GUIs, respectively. However, MATLAB's edge() function
        # (https://www.mathworks.com/help/images/ref/edge.html) with the
        # 'Canny' method expects thresholds to be in the range of [0, 1],
        # whereas OpenCV's Canny() function
        # (https://docs.opencv.org/4.4.0/dd/d1a/group__imgproc__feature.html#ga04723e007ed888ddf11d9ba04e2232de)
        # does not specify the scale. According to the following link
        # (https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/),
        # OpenCV's Canny() function expects thresholds to be in the range of
        # [0, 255], though.

        # Count edge pixels per level
        edge_pixels_per_level: List[int] = []  # Edge strengths
        for index in range(len(luminance_levels)):
            # Detect edges
            img_contours_nparray: np.ndarray = cv2.Canny(
                image=img_blurred_nparray,
                threshold1=low_thresholds[index],
                threshold2=high_thresholds[index],
            )
            n_edge_pixels: int = np.count_nonzero(img_contours_nparray)
            edge_pixels_per_level.append(n_edge_pixels)

        # Compute the sum of weighted difference in pixels between each
        # successive level
        sum_of_weighted_differences: float = 0.0
        for index in range(len(edge_pixels_per_level) - 1):
            level: int = levels[index]
            # The difference in pixels between each successive level
            difference: int = (
                edge_pixels_per_level[index] - edge_pixels_per_level[index + 1]
            )
            weight: float = 1 - (
                (level - 1) / (len(edge_pixels_per_level) - 1)
            )
            # The weighted difference in pixels between each successive level
            weighted_difference: float = difference * weight
            sum_of_weighted_differences += weighted_difference

        # Compute figure-ground contrast
        # (normalized sum of weighted differences)
        try:
            figure_ground_contrast: float = sum_of_weighted_differences / (
                edge_pixels_per_level[0] - edge_pixels_per_level[-1]
            )
        except ZeroDivisionError:
            figure_ground_contrast = 0.0
        # Note 1: According to the equation in [3], the denominator is
        # supposed to be E1 - E6, but the text description says 0.1 - 0.7
        # (i.e., E1 - E7). The latter should be correct.

        return [
            figure_ground_contrast,
        ]
