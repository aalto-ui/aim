#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    UIED Segmentation


Description:
    This UI Segmentation is method mostly based on old-fashioned computer vision approaches to detect UI components
    and texts. Model code is imported from https://github.com/MulongXie/UIED.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Xie, M., Feng, S., Xing, Z., Chen, J., & Chen, C. (2020).UIED: a hybrid tool for GUI element detection.
        In Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and Symposium
        on the Foundations of Software Engineering, pp. 1655-1659. ACM.
        doi: https://doi.org/10.1145/3368089.3417940

    2.  Chen, J., Xie, M., Xing, Z., Chen, C., Xu, X., Zhu, L., & Li, G. (2020). Object detection for graphical user
        interface: Old fashioned or deep learning or a combination?. In proceedings of the 28th ACM joint meeting on
        European Software Engineering Conference and Symposium on the Foundations of Software Engineering pp. 1202-1214.
        ACM.
        doi: https://doi.org/10.1145/3368089.3409691



Change log:
    v1.0 (2022-08-05)
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
from PIL import Image
from pydantic import HttpUrl

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP, GUI_TYPE_MOBILE
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-08-05"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: UIED Segmentation.
    """

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
            - UIED segmented image (str, image (PNG) encoded in Base64)
        """

        # Get all elements
        if gui_segments is not None:
            segmented_im_b64: str = gui_segments["img_b64"]
        else:
            raise ValueError(
                "This Metric requires gui_segments to be not None"
            )

        return [
            segmented_im_b64,
        ]
