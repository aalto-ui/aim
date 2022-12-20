#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    AIM Legacy Segmentation


Description:
    AIM Legacy Segmentation. Tool for segmentation of images.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Oulasvirta, A., De Pascale, S., Koch, J., ... & Weinkauf, T. (2018).
        Aalto Interface Metrics (AIM) A Service and Codebase for Computational
        GUI Evaluation. In The 31st Annual ACM Symposium on User Interface Software
        and Technology Adjunct Proceedings, pp. 16-19.
        doi: https://doi.org/10.1145/2702123.2702575


Change log:
    v2.0 (2022-08-05)
      * Revised implementation

    v1.0.1 (2018-10-18)
      * Initial implementation
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
from io import BytesIO
from typing import Any, Dict, List, Optional, Union

# Third-party modules
import cv2
import numpy as np
from PIL import Image
from pydantic import HttpUrl
from skimage import img_as_ubyte
from skimage.feature import canny
from skimage.filters import rank
from skimage.morphology import disk

# First-party modules
from aim.common import image_utils
from aim.common.constants import GUI_TYPE_DESKTOP, GUI_TYPE_MOBILE
from aim.metrics.interfaces import AIMMetricInterface
from aim.metrics.m24 import utils

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine, Khushhall Chandra Mahajan, Janin Koch, Samuli De Pascale"
__date__ = "2022-08-05"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: AIM Legacy Segmentation.
    """

    # Private constants
    _H_BLUR: int = 13  # 11 # Horizontal Blurring filter
    _V_BLUR: int = 9  # 13 # Vertical Blurring filter
    _H_THRESHOLD_MIN_SIZE: int = 10  # Minimum acceptable height of element
    _W_THRESHOLD_MIN_SIZE: int = 15  # Minimum acceptable width of element
    _DETAILED: bool = True
    _SHOW: bool = False
    _BOUNDING_BOX: bool = False  # Bounding Box

    # Private methods
    @classmethod
    def segment(cls, img_bgr: np.ndarray):

        BW = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(
            BW, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

        denoised = rank.median(BW, disk(5))
        gradient_denoised = rank.gradient(denoised, disk(1))

        gradient_0 = rank.gradient(img_bgr[:, :, 0], disk(1))
        gradient_1 = rank.gradient(img_bgr[:, :, 1], disk(1))
        gradient_2 = rank.gradient(img_bgr[:, :, 2], disk(1))

        sobelx64f = cv2.Sobel(BW, cv2.CV_64F, 1, 0, ksize=5)
        abs_sobel64f = np.absolute(sobelx64f)
        sobel_8u = np.uint8(abs_sobel64f)
        img_canny = canny(BW)

        contours_thresh, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        contours_0, _ = cv2.findContours(
            gradient_0, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        contours_1, _ = cv2.findContours(
            gradient_1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        contours_2, _ = cv2.findContours(
            gradient_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        contours_denoised, _ = cv2.findContours(
            gradient_denoised, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        contours_sobel, _ = cv2.findContours(
            sobel_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        contours_canny, _ = cv2.findContours(
            img_as_ubyte(img_canny), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )

        contours = (
            contours_0
            + contours_1
            + contours_2
            + contours_denoised
            + contours_sobel
            + contours_canny
        )

        temp = np.zeros_like(BW)
        if cls._BOUNDING_BOX:
            bbox = utils.remove_overlaps(contours)
            for bb in bbox:
                temp = cv2.rectangle(
                    temp, (bb.x1, bb.y1), (bb.x2, bb.y2), (255, 255, 255), 1
                )

        for c in contours_thresh:
            x, y, w, h = cv2.boundingRect(c)
            temp = cv2.rectangle(
                temp, (x, y), (x + w, y + h), (255, 255, 255), 1
            )

        # Horizontal Blurring filter
        size: int = cls._H_BLUR
        kmb: np.ndarray = np.zeros((size, size))
        kmb[int(size / 2), :] = np.ones(size)
        kmb = kmb / size

        # Apply horizontal blurring here
        temp = cv2.filter2D(temp, -1, kmb)
        contours_all_h, _ = cv2.findContours(
            temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )

        # Vertical Blurring filter
        size = cls._V_BLUR
        kmb = np.zeros((size, size))
        kmb[:, int(size / 2)] = np.ones(size)
        kmb = kmb / size

        # Apply vertical blurring here
        temp = cv2.filter2D(temp, -1, kmb)
        contours_all_v, _ = cv2.findContours(
            temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )

        return contours_all_v, contours_all_h

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
            gui_segments: GUI segmentation (defaults to None)
            gui_url: GUI URL (defaults to None)

        Returns:
            Results (list of measures)
            - AIM Legacy segmented image (str, image (PNG) encoded in Base64)
        """

        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (should be RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")
        img_rgb_nparray: np.ndarray = np.array(img_rgb)
        img_bgr_nparray = cv2.cvtColor(img_rgb_nparray, cv2.COLOR_RGB2BGR)
        img_out_bgr_nparray = np.copy(img_bgr_nparray)

        contours_all_v, contours_all_h = cls.segment(img_bgr_nparray)

        thickness = 1
        if cls._DETAILED:
            contours_all = contours_all_h
        else:
            contours_all = contours_all_v
            thickness = 2

        elements = []
        for i, c in enumerate(contours_all):
            x, y, w, h = cv2.boundingRect(c)

            if w <= cls._W_THRESHOLD_MIN_SIZE:
                continue
            if h <= cls._H_THRESHOLD_MIN_SIZE:
                continue

            img_out_bgr_nparray = cv2.rectangle(
                img_out_bgr_nparray,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                thickness,
            )

            elements.append(
                {
                    "id": i,
                    "x_position": x,
                    "y_position": y,
                    "width": w,
                    "height": h,
                }
            )

        if cls._SHOW:
            cv2.imshow("Output", img_out_bgr_nparray)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # Convert output segmented array Pillow Image
        img_out_rgb_nparray: np.ndarray = cv2.cvtColor(
            img_out_bgr_nparray, cv2.COLOR_BGR2RGB
        )
        img_out: Image.Image = Image.fromarray(img_out_rgb_nparray)

        # Convert output segmented image to b64 (str)
        img_b64: str = image_utils.to_png_image_base64(img_out)

        # Result
        result: Dict[str, Any] = {
            "segments": elements,
            "img_shape": list(img_out_rgb_nparray.shape),
            "img_b64": img_b64,
        }

        return [
            result["img_b64"],
        ]
