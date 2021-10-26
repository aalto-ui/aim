#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    UMSI (Unified Model of Saliency and Importance)


Description:
    The visual importance heatmap and the overlay with the input image.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Fosco, C., Casser, V., Kumar Bedi, A., O'Donovan, P., Hertzmann, A., Bylinskii, Z.
        redicting Visual Importance Across Graphic Design Types. In ACM UIST, 2020.
        doi: https://doi.org/10.1145/3379337.3415825


Change log:
    v1.0 (2021-10-20)
      * Initial implementation
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
import os
import sys
from io import BytesIO
from typing import List, Optional, Union

# Third-party modules
import cv2
import keras
import keras.backend as K
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import scipy
from PIL import Image

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Chuhan Jiao, Markku Laine"
__date__ = "2021-10-20"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: UMSI (Unified Model of Saliency and Importance).
    """

    # Input shape of the model
    shape_r = 240
    shape_c = 320

    @classmethod
    def padding(cls, img, shape_r, shape_c, channels=3):
        """
        Resize the image maintain the aspect ratio by padding.

        Args:
            img: Image RGB data
            shape_r: Model required width
            shape_c: Model requied height
            channels: Number of channels of the output image

        Returns:
            Image data (numpy ndarray) with shape
            (shape_r, shape_c, channels)
        """

        img_padded = np.zeros((shape_r, shape_c, channels), dtype=np.uint8)
        if channels == 1:
            img_padded = np.zeros((shape_r, shape_c), dtype=np.uint8)

        original_shape = img.shape
        rows_rate = original_shape[0] / shape_r
        cols_rate = original_shape[1] / shape_c

        if rows_rate > cols_rate:
            new_cols = (original_shape[1] * shape_r) // original_shape[0]

            img = cv2.resize(img, (new_cols, shape_r))

            if new_cols > shape_c:
                new_cols = shape_c
            img_padded[
                :,
                ((img_padded.shape[1] - new_cols) // 2) : (
                    (img_padded.shape[1] - new_cols) // 2 + new_cols
                ),
            ] = img
        else:
            new_rows = (original_shape[0] * shape_c) // original_shape[1]
            img = cv2.resize(img, (shape_c, new_rows))
            if new_rows > shape_r:
                new_rows = shape_r
            img_padded[
                ((img_padded.shape[0] - new_rows) // 2) : (
                    (img_padded.shape[0] - new_rows) // 2 + new_rows
                ),
                :,
            ] = img

        return img_padded

    @classmethod
    def preprocess_images(cls, img, shape_r, shape_c, pad=True):
        """
        Preprocess the image to the size required by the model.

        Args:
            img: Image RGB data
            shape_r: Model required width
            shape_c: Model requied height
            pad: A boolean variable that decides whether the
                 image needs to be padded. If True, the output
                 image will maintain the aspect ratio of the
                 input image

        Returns:
            Preprocessed_image (numpy ndarray) with shape
            (1, shape_r, shape_c, 3)
        """

        if pad:
            ims = np.zeros((1, shape_r, shape_c, 3))
        else:
            ims = []

        original_image = img

        if original_image is None:
            raise ValueError("There is something wrong with the input image")
        if pad:
            padded_image = cls.padding(original_image, shape_r, shape_c, 3)
            ims[0] = padded_image
        else:
            original_image = original_image.astype(np.float32)
            original_image[..., 0] -= 103.939
            original_image[..., 1] -= 116.779
            original_image[..., 2] -= 123.68
            ims.append(original_image)
            ims = np.array(ims)
            print("ims.shape in preprocess_imgs", ims.shape)

        if pad:
            ims[:, :, :, 0] = ims[:, :, :, 0] - 103.939
            ims[:, :, :, 1] = ims[:, :, :, 1] - 116.779
            ims[:, :, :, 2] = ims[:, :, :, 2] - 123.68

        return ims

    @classmethod
    def postprocess_predictions(
        cls, pred, shape_r, shape_c, blur=False, normalize=False
    ):
        """
        Preprocess the image to the size required by the model.

        Args:
            pred: The heatmap predicted by the model
            shape_r: The width of the original image
            shape_c: The height of the original image
            blur: A boolean variable that decides whether
                  the input heatmap needs to be blurred
            normalize: A boolean variable that decides whether
                  the output heatmap([0,1]) needs to be
                  normalized to [0,255]

        Returns:
            The heatmap with width=shape_r and height=shape_c
        """
        predictions_shape = pred.shape
        rows_rate = shape_r / predictions_shape[0]
        cols_rate = shape_c / predictions_shape[1]

        if blur:
            sigma = blur
            pred = scipy.ndimage.filters.gaussian_filter(pred, sigma=sigma)

        if rows_rate > cols_rate:
            new_cols = (predictions_shape[1] * shape_r) // predictions_shape[0]
            pred = cv2.resize(pred, (new_cols, shape_r))
            img = pred[
                :,
                ((pred.shape[1] - shape_c) // 2) : (
                    (pred.shape[1] - shape_c) // 2 + shape_c
                ),
            ]
        else:
            new_rows = (predictions_shape[0] * shape_c) // predictions_shape[1]

            pred = cv2.resize(pred, (shape_c, new_rows))

            img = pred[
                ((pred.shape[0] - shape_r) // 2) : (
                    (pred.shape[0] - shape_r) // 2 + shape_r
                ),
                :,
            ]

        if normalize:
            img = img / np.max(img) * 255

        return img

    @classmethod
    def heatmap_overlay(cls, im, heatmap, colmap="hot"):
        """
        Overlay the heatmap on the input image.

        Args:
            im: The original input image
            heatmap: The heatmap which has the same width
                and height as the im
            colmap: The style of the heatmap

        Returns:
            The overlay image.
        """
        cm_array = cm.get_cmap(colmap)
        im_array = np.asarray(im)
        heatmap_norm = (heatmap - np.min(heatmap)) / float(
            np.max(heatmap) - np.min(heatmap)
        )
        heatmap_hot = cm_array(heatmap_norm)
        res_final = im_array.copy()
        heatmap_rep = np.repeat(heatmap_norm[:, :, np.newaxis], 3, axis=2)
        res_final[...] = heatmap_hot[
            ..., 0:3
        ] * 255.0 * heatmap_rep + im_array[...] * (1 - heatmap_rep)
        return res_final

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
            - UMSI, image (PNG) encoded in Base64
        """

        # Create PIL image
        umsi_image: Image.Image = Image.open(
            BytesIO(base64.b64decode(gui_image))
        )
        umsi_image = umsi_image.convert("RGB")
        width, height = umsi_image.size

        # Preprocess the image
        cv_image = cv2.cvtColor(np.asarray(umsi_image), cv2.COLOR_RGB2BGR)
        pre_image = cls.preprocess_images(cv_image, cls.shape_r, cls.shape_c)

        # Load the UMSI model
        ckpt_path = "/usr/src/app/aim/metrics/m9/xception_cl_fus_aspp_imp1k_10kl-3cc0.1mse-5nss5bc_bs4_ep30_valloss-2.5774_full.h5"
        model = keras.models.load_model(ckpt_path)

        # Predict and post process the heatmap
        preds = model.predict(pre_image)
        heat_map = cls.postprocess_predictions(
            preds[0][0, :, :, 0], height, width
        )
        overlay = cls.heatmap_overlay(umsi_image, heat_map, "viridis")

        # convert 2d-array heatmap to PIL Image
        pil_heatmap = np.uint8(cm.get_cmap("viridis")(heat_map) * 255)

        # Save the results
        final_heatmap = Image.fromarray(pil_heatmap)
        final_overlay = Image.fromarray(overlay, mode="RGB")
        buffered_h = BytesIO()
        buffered_o = BytesIO()
        final_heatmap.save(buffered_h, format="PNG", compress_level=6)
        final_overlay.save(buffered_o, format="PNG", compress_level=6)
        h_b64: str = base64.b64encode(buffered_h.getvalue()).decode("utf-8")
        o_b64: str = base64.b64encode(buffered_o.getvalue()).decode("utf-8")
        return [h_b64, o_b64]
