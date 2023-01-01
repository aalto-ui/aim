#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Mirror symmetry - contour pixel


Description:
    The similarity of an object reflection across a straight axis. The measure
    considered contour pixels of image. In this metric contour symmetry
    was measured by looking for a match for each contour pixel across the central
    vertical axis. If a contour pixel had a counterpart across the main vertical
    axis, it was counted as a symmetrical pixel. The metric compute ratio of
    symmetrical pixels to all edge pixels and normalized it by edge density.

    Category: Organization of Information > Symmetry.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Miniukovich, A. and De Angeli, A. (2014). Quantification of Interface
        Visual Complexity. In Proceedings of the 2014 International Working
        Conference on Advanced Visual Interfaces (AVI '14), pp. 153-160. ACM.
        doi: https://doi.org/10.1145/2598153.2598173

    2.  Miniukovich, A. and De Angeli, A. (2014). Visual Impressions of Mobile
        App Interfaces. In Proceedings of the 8th Nordic Conference on
        Human-Computer Interaction (NordiCHI '14), pp. 31-40. ACM.
        doi: https://doi.org/10.1145/2639189.2641219


Change log:
    v2.0 (2022-12-24)
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
from typing import Any, Dict, List, Optional, Tuple, Union

# Third-party modules
import cv2
import numpy as np
from PIL import Image
from pydantic import HttpUrl

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP, GUI_TYPE_MOBILE
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine, Thomas Langerak"
__date__ = "2022-12-24"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Mirror Symmetry (Contour Pixel).
    """

    # Private constants
    _CANNY_EDGE_DETECTION_MATLAB_LOW_THRESHOLD_DESKTOP: float = 0.11
    _CANNY_EDGE_DETECTION_MATLAB_HIGH_THRESHOLD_DESKTOP: float = 0.27
    _CANNY_EDGE_DETECTION_PYTHON_LOW_THRESHOLD_MOBILE: int = 50
    _CANNY_EDGE_DETECTION_PYTHON_HIGH_THRESHOLD_MOBILE: int = 50
    _CANNY_EDGE_DETECTION_PYTHON_MIN_THRESHOLD: int = 0
    _CANNY_EDGE_DETECTION_PYTHON_MAX_THRESHOLD: int = 255
    _GAUSSIAN_KERNEL_SIZE: Tuple[int, int] = (0, 0)
    _GAUSSIAN_KERNEL_STANDARD_DEVIATION: int = 2
    _KEY_RADIUS: int = 3
    _SYMMETRY_RADIUS: int = 4

    @staticmethod
    def _get_pixels_in_radius(
        x: int, y: int, width: int, height: int, radius: int
    ) -> List[List[int]]:
        # Get x border
        if x < radius:
            rad_x_left: int = -x
            rad_x_right: int = radius
        elif width - x < radius:
            rad_x_right = 1 * (width - x)
            rad_x_left = -radius
        else:
            rad_x_left = -radius
            rad_x_right = radius

        # Get y borders
        if y < radius:
            rad_y_top: int = -y
            rad_y_bottom: int = radius
        elif height - y < radius:
            rad_y_bottom = 1 * (height - y)
            rad_y_top = -radius
        else:
            rad_y_top = -radius
            rad_y_bottom = radius

        pixels: List[List[int]] = []
        for m in range(rad_x_left, rad_x_right):
            for n in range(rad_y_top, rad_y_bottom):
                if m != 0 or n != 0:
                    pixel: List[int] = [x + m, y + n]
                    pixels.append(pixel)

        return pixels

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
            - Normalized pixel symmetry (float, [0, +inf])
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (should be RGBA) to L (grayscale) color space
        img_l: Image.Image = img.convert("L")

        # Get NumPy array
        img_l_nparray: np.ndarray = np.array(img_l)

        # Gaussian filter parameters
        ksize: Tuple[int, int] = cls._GAUSSIAN_KERNEL_SIZE
        sigma: int = cls._GAUSSIAN_KERNEL_STANDARD_DEVIATION
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
        low_threshold: float = (
            cls._CANNY_EDGE_DETECTION_PYTHON_LOW_THRESHOLD_MOBILE
            if gui_type == GUI_TYPE_MOBILE
            else round(
                cls._CANNY_EDGE_DETECTION_PYTHON_MAX_THRESHOLD
                * cls._CANNY_EDGE_DETECTION_MATLAB_LOW_THRESHOLD_DESKTOP,
                2,
            )
        )  # 50 or 28.05 [0, 255] for mobile and desktop GUIs, respectively
        high_threshold: float = (
            cls._CANNY_EDGE_DETECTION_PYTHON_HIGH_THRESHOLD_MOBILE
            if gui_type == GUI_TYPE_MOBILE
            else round(
                cls._CANNY_EDGE_DETECTION_PYTHON_MAX_THRESHOLD
                * cls._CANNY_EDGE_DETECTION_MATLAB_HIGH_THRESHOLD_DESKTOP,
                2,
            )
        )  # 50 or 68.85 [0, 255] for mobile and desktop GUIs, respectively
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

        # Calculate image shape and number of all pixels
        img_shape: Tuple[int, ...] = img_contours_nparray.shape
        height: int = img_shape[0]
        width: int = img_shape[1]
        n_all_pixels: int = height * width  # height * width

        # Set all pixels in radius of an edge pixel to 0
        n_all_keys: int = 0
        for y in range(height):
            for x in range(width):
                if img_contours_nparray[y][x] != 0:
                    n_all_keys += 1
                    pixels_in_radius: List[
                        List[int]
                    ] = cls._get_pixels_in_radius(
                        x, y, width, height, cls._KEY_RADIUS
                    )
                    for pixel in pixels_in_radius:
                        img_contours_nparray[pixel[1], pixel[0]] = 0

        # Check vertical symmetry
        n_all_sym: int = 0
        for y in range(height):
            for x in range(int(width / 2)):
                if img_contours_nparray[y][x] != 0:
                    vertical_pixels: List[
                        List[int]
                    ] = cls._get_pixels_in_radius(
                        width - x, y, width, height, cls._SYMMETRY_RADIUS
                    )
                    horizontal_pixels: List[
                        List[int]
                    ] = cls._get_pixels_in_radius(
                        x, height - y, width, height, cls._SYMMETRY_RADIUS
                    )

                    for pixel in vertical_pixels:
                        if (
                            img_contours_nparray[int(pixel[1]), int(pixel[0])]
                            != 0
                        ):
                            n_all_sym += 1
                            break

                    for pixel in horizontal_pixels:
                        if (
                            img_contours_nparray[int(pixel[1]), int(pixel[0])]
                            != 0
                        ):
                            n_all_sym += 1
                            break

        # Compute normalized pixel symmetry
        try:
            sym_normalized: float = (float(n_all_sym) / float(n_all_keys)) * (
                (
                    float((n_all_keys - 1) * cls._SYMMETRY_RADIUS)
                    / float(n_all_pixels)
                )
                ** -1
            )
        except ZeroDivisionError:
            sym_normalized = 0.0

        return [
            sym_normalized,
        ]
