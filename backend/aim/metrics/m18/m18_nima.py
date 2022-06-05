#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    NIMA (Neural IMage Assessment)


Description:
    Technical and aesthetic qualities of the input image.

    Category:

Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Talebi, H., & Milanfar, P. (2018). NIMA: Neural image assessment.
        IEEE transactions on image processing, 27(8), 3998-4011.
        doi: https://doi.org/10.1109/TIP.2018.2831899

Change log:
    v1.0 (2022-06-05)
      * Initial implementation
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
import os
from io import BytesIO
from typing import List, Optional, Union

# Third-party modules
import torch
from PIL import Image
from pydantic import HttpUrl

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface
from aim.metrics.m18.utils import (
    NIMA,
    Transform,
    get_mean_score,
    get_std_score,
)

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-06-05"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: NIMA (Neural IMage Assessment).
    """

    # Transform method
    _transform = Transform().val_transform

    # Load Model: from https://s3-us-west-1.amazonaws.com/models-nima/pretrain-model.pth
    _MODEL_PATH = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "pretrain-model.pth"
    )
    _DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    _MODEL = NIMA()
    _STATE_DICT = torch.load(
        _MODEL_PATH, map_location=lambda storage, loc: storage
    )
    _MODEL.load_state_dict(_STATE_DICT)
    _MODEL = _MODEL.to(_DEVICE)
    _MODEL.eval()

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
            - NIMA mean_score (float, [0, +inf))
            - NIMA std_score (float, [0, +inf))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Resize image to fit network input
        img_resized = cls._transform(img_rgb)
        img_resized = img_resized.unsqueeze_(0)
        # To device (CPU or GPU)
        img_resized = img_resized.to(cls._DEVICE)

        # Predict
        with torch.no_grad():
            prob = cls._MODEL(img_resized).data.cpu().numpy()[0]

        # Compute Metrics
        mean_score: float = get_mean_score(prob)
        std_score: float = get_std_score(prob)
        # scores = [float(x) for x in prob]

        return [mean_score, std_score]
