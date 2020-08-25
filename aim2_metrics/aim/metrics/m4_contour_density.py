#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Contour density


Description:
    The ratio of contour pixels to all pixels.

    Category: Visual complexity > Information amount > Visual clutter.
    For details, see CL1 [1], A9 [2], and CL1 [3].


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
    v2.0 (2020-08-25)
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
from typing import Any, List, Optional, Tuple

# Third-party modules
import cv2
import numpy as np
from PIL import Image

# First-party modules
from aim.core.constants import (
    CANNY_EDGE_DETECTION_PYTHON_HIGH_THRESHOLD_DESKTOP,
    CANNY_EDGE_DETECTION_PYTHON_HIGH_THRESHOLD_MOBILE,
    CANNY_EDGE_DETECTION_PYTHON_LOW_THRESHOLD_DESKTOP,
    CANNY_EDGE_DETECTION_PYTHON_LOW_THRESHOLD_MOBILE,
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
__date__ = "2020-08-25"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric4(AIMMetricInterface):
    """
    Metric 4: Contour density.
    """

    # Public methods
    @staticmethod
    def execute_metric(
        gui_image: str, gui_type: int = GUI_TYPE_DESKTOP
    ) -> Optional[List[Any]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1

        Returns:
            Results (list of measures)
            - Contour density (float, [0, 1])
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

        # Canny edge detection parameters
        low_threshold: int = (
            CANNY_EDGE_DETECTION_PYTHON_LOW_THRESHOLD_MOBILE
            if gui_type == GUI_TYPE_MOBILE
            else CANNY_EDGE_DETECTION_PYTHON_LOW_THRESHOLD_DESKTOP
        )
        high_threshold: int = (
            CANNY_EDGE_DETECTION_PYTHON_HIGH_THRESHOLD_MOBILE
            if gui_type == GUI_TYPE_MOBILE
            else CANNY_EDGE_DETECTION_PYTHON_HIGH_THRESHOLD_DESKTOP
        )
        # Note 1: According to [3], low and high thresholds for desktop GUIs
        # were set to 0.11 and 0.27 (MATLAB), respectively. However, MATLAB's
        # edge() function (https://www.mathworks.com/help/images/ref/edge.html)
        # with the 'Canny' method expects thresholds to be in the range of
        # [0, 1], whereas OpenCV's Canny() function
        # (https://docs.opencv.org/4.4.0/dd/d1a/group__imgproc__feature.html#ga04723e007ed888ddf11d9ba04e2232de)
        # does not specify the scale. According to the following link
        # (https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/),
        # OpenCV's Canny() function expects thresholds to be in the range of
        # [0, 255], though.
        # Note 2: According to a personal discussion with Miniukovich, both
        # low and high thresholds for mobile GUIs were set to 50 on the 0-255
        # scale. This information is not present in [2].

        # Detect edges
        img_contours_nparray: np.ndarray = cv2.Canny(
            image=img_blurred_nparray,
            threshold1=low_threshold,
            threshold2=high_threshold,
        )

        # Calculate contour density
        img_shape: Tuple[int, int] = img_contours_nparray.shape
        n_all_pixels: int = img_shape[0] * img_shape[1]  # height * width
        n_contour_pixels: int = np.count_nonzero(img_contours_nparray)
        contour_density: float = n_contour_pixels / n_all_pixels

        return [
            contour_density,
        ]
