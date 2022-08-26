#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    NIMA (Neural IMage Assessment)


Description:
    The predicted technical and aesthetic qualities of images.


Source:
    Model is imported from here:
    https://github.com/delldu/ImageNima/tree/master/models


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Talebi, H. and Milanfar, P. (2018). NIMA: Neural Image Assessment.
        IEEE Transactions on Image Processing, 27(8), 3998-4011.
        doi: https://doi.org/10.1109/TIP.2018.2831899


Change log:
    V2.0 (2022-06-16)
      * Change Model

    v1.0 (2022-06-05)
      * Initial implementation
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
import collections
import pathlib
from io import BytesIO
from typing import List, Optional, Union

# Third-party modules
import torch
import torch.nn as nn
from PIL import Image
from pydantic import HttpUrl
from torchvision import models, transforms

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-06-16"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: NIMA (Neural IMage Assessment).
    """

    # Transform method: Since the trained model only works with square
    # photos, we should resize the input image. _tranform can be changed to
    # any transformer. The implemented transformer returns the center square
    # of the resized input image (smaller edge is 224, without changing
    # ratio), which is one of the most popular transformers for non-square
    # images.
    _transform: transforms.transforms.Compose = transforms.Compose(
        [
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
        ]
    )

    # Load Model
    # The original model can be downloaded from here: https://github.com/delldu/ImageNima/tree/master/models
    _MODEL_PATH: pathlib.Path = pathlib.Path("aim/metrics/m18/dense121_all.pt")

    # Choose GPU if available
    _DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Define DENS-NET121 Model
    _NUM_CLASS: int = 10
    _MODEL: models.densenet.DenseNet = models.densenet121(pretrained=False)
    _NUM_FTRS: int = _MODEL.classifier.in_features
    _MODEL.classifier = nn.Sequential(
        nn.Linear(_NUM_FTRS, _NUM_CLASS), nn.Softmax(1)
    )

    # Load state dict: weights
    _STATE_DICT: collections.OrderedDict = torch.load(
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
            - NIMA mean score (float, [0, 10])
            - NIMA standard deviation score (float, [0, +inf))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Compute votes and send to device (CPU or GPU)
        weighted_votes: torch.Tensor = torch.arange(10, dtype=torch.float) + 1
        weighted_votes = weighted_votes.to(cls._DEVICE)

        # Resize image to fit network input
        img_resized: torch.Tensor = cls._transform(img_rgb)
        img_resized = img_resized.to(cls._DEVICE)

        # Predict
        with torch.no_grad():
            scores: torch.Tensor = cls._MODEL(img_resized.view(1, 3, 224, 224))
            mean: torch.Tensor = torch.matmul(scores, weighted_votes)
            std: torch.Tensor = torch.sqrt(
                (
                    scores * torch.pow((weighted_votes - mean.view(-1, 1)), 2)
                ).sum(dim=1)
            )

        # Compute metrics
        nima_mean_score: float = float(mean.item())
        nima_std_score: float = float(std.item())

        return [
            nima_mean_score,
            nima_std_score,
        ]
