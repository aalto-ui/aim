#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    UMSI (Unified Model of Saliency and Importance)


Description:
    The predicted human attention on different design classes and natural
    images, visualized as a heatmap and heatmap overlay.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Fosco, C., Casser, V., Bedi, A.K., O'Donovan, P., Hertzmann, A., and
        Bylinskii, Z. (2020). Predicting Visual Importance Across Graphic
        Design Types. In Proceedings of the 33rd Annual ACM Symposium on User
        Interface Software and Technology (UIST '20), pp. 249-260. ACM.
        doi: https://doi.org/10.1145/3379337.3415825


Change log:
    v1.1 (2022-06-14)
      * Upgrade TF to 2.x.x
      * Support Crop

    v1.0 (2021-10-30)
      * Initial implementation
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
import gc
import os
import pathlib
import sys
import warnings
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple, Union

# Third-party modules
import cv2
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import scipy
import skimage.transform as skit
from PIL import Image
from pydantic import HttpUrl

# First-party modules
from aim.common import image_utils
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface
from aim.metrics.m9.utils import compute_crops_height

# isort: off
# Third-party modules - Ignore Keras outputs and logs
stderr = sys.stderr
sys.stderr = open(os.devnull, "w")
from tensorflow import keras  # noqa: E402
from tensorflow.keras import backend as K  # noqa: E402

sys.stderr = stderr
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

warnings.filterwarnings("ignore", category=UserWarning, module="keras.*")
# isort: on


# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine, Chuhan Jiao, Amir Hossein Kargaran"
__date__ = "2022-06-14"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.1"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: UMSI (Unified Model of Saliency and Importance).

    Reference:
        Based on Fosco et al.'s Python implementation available at https://github.com/diviz-mit/predimportance-public (see LICENSE within the distribution).
    """

    # Private constants
    _SHAPE_R: int = 240  # input shape (rows) of the model
    _SHAPE_C: int = 320  # input shape (columns) of the model
    _SHOW: bool = False
    _USE_CV2: bool = False
    _HEATMAP_STYLE: str = "viridis"

    # Private methods
    @classmethod
    def _preprocess_images(
        cls, original_images: List[Image.Image], show: bool = False
    ) -> np.ndarray:
        """
        Preprocess images to the size required by the model.

        Args:
            original_images: List of original images
            show: True, if input visualizations must be shown.
                  Otherwise, False

        Returns:
            Preprocessed image data with the shape of (n_images, rows, columns, channels)
        """
        imgs: np.ndarray = np.zeros(
            (len(original_images), cls._SHAPE_R, cls._SHAPE_C, 3)
        )

        for i, original_image in enumerate(original_images):
            img: Union[np.ndarray, Image.Image]
            if cls._USE_CV2:
                img = cv2.cvtColor(
                    np.asarray(original_image), cv2.COLOR_RGB2BGR
                )
            else:
                img = original_image

            padded_image: np.ndarray = cls._padding(img)
            imgs[i] = padded_image

            if show:
                plt.figure(figsize=[15, 7])
                plt.subplot(1, 2, 1)
                if cls._USE_CV2:
                    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                else:
                    plt.imshow(img)
                plt.title("Original image")
                plt.subplot(1, 2, 2)
                if cls._USE_CV2:
                    plt.imshow(cv2.cvtColor(padded_image, cv2.COLOR_BGR2RGB))
                else:
                    plt.imshow(padded_image)
                plt.title("Input to network")
                plt.show()

        imgs[:, :, :, 0] -= 103.939
        imgs[:, :, :, 1] -= 116.779
        imgs[:, :, :, 2] -= 123.68

        return imgs

    @classmethod
    def _padding(
        cls, original_image: Union[np.ndarray, Image.Image]
    ) -> np.ndarray:
        """
        Resize the image by padding so that it maintains its original aspect ratio.

        Args:
            original_image: Original image

        Returns:
            Resized (and padded) image data with the shape of
            (rows, columns, channels)
        """
        img_padded: np.ndarray = np.zeros(
            (cls._SHAPE_R, cls._SHAPE_C, 3), dtype=np.uint8
        )

        original_shape: Union[Tuple[int, ...], Any]
        if cls._USE_CV2:
            original_shape = original_image.shape
        else:
            original_shape = np.asarray(original_image).shape

        rows_rate: float = original_shape[0] / cls._SHAPE_R
        cols_rate: float = original_shape[1] / cls._SHAPE_C

        if rows_rate > cols_rate:
            new_cols: int = (
                original_shape[1] * cls._SHAPE_R
            ) // original_shape[0]
            if cls._USE_CV2:
                original_image = cv2.resize(
                    original_image, (new_cols, cls._SHAPE_R)
                )
            else:
                original_image = original_image.resize(
                    (new_cols, cls._SHAPE_R)
                )

            if new_cols > cls._SHAPE_C:
                new_cols = cls._SHAPE_C
            img_padded[
                :,
                ((img_padded.shape[1] - new_cols) // 2) : (
                    (img_padded.shape[1] - new_cols) // 2 + new_cols
                ),
            ] = original_image
        else:
            new_rows: int = (
                original_shape[0] * cls._SHAPE_C
            ) // original_shape[1]
            if cls._USE_CV2:
                original_image = cv2.resize(
                    original_image, (cls._SHAPE_C, new_rows)
                )
            else:
                original_image = original_image.resize(
                    (cls._SHAPE_C, new_rows)
                )

            if new_rows > cls._SHAPE_R:
                new_rows = cls._SHAPE_R

            img_padded[
                ((img_padded.shape[0] - new_rows) // 2) : (
                    (img_padded.shape[0] - new_rows) // 2 + new_rows
                ),
                :,
            ] = original_image

        return img_padded

    @classmethod
    def _postprocess_predictions(
        cls,
        original_images: List[Image.Image],
        predictions: List[np.ndarray],
        blur: bool = False,
        normalize: bool = False,
    ) -> List[np.ndarray]:
        """
        Postprocess predictions back to the original size.

        Args:
            original_images: List of original images
            predictions: Heatmaps predicted by the model
            blur: True, if prediction heatmaps must be blurred.
                  Otherwise, False
            normalize: True, if prediction heatmaps must be normalized from
                       [0, 1] to [0, 255]

        Returns:
            Postprocessed prediction heatmaps
        """
        heatmap_batch: List[np.ndarray] = []
        for i, original_image in enumerate(original_images):
            width: int
            height: int
            width, height = original_image.size
            prediction: np.ndarray = predictions[0][i, :, :, 0]
            prediction_shape: Tuple[int, ...] = prediction.shape
            rows_rate: float = height / prediction_shape[0]
            cols_rate: float = width / prediction_shape[1]

            if blur:
                sigma: bool = blur
                prediction = scipy.ndimage.filters.gaussian_filter(
                    prediction, sigma=sigma
                )

            img: np.ndarray
            if rows_rate > cols_rate:
                new_cols: int = (
                    prediction_shape[1] * height
                ) // prediction_shape[0]
                if cls._USE_CV2:
                    prediction = cv2.resize(prediction, (new_cols, height))
                else:
                    prediction = skit.resize(prediction, (height, new_cols))
                img = prediction[
                    :,
                    ((prediction.shape[1] - width) // 2) : (
                        (prediction.shape[1] - width) // 2 + width
                    ),
                ]
            else:
                new_rows: int = (
                    prediction_shape[0] * width
                ) // prediction_shape[1]
                if cls._USE_CV2:
                    prediction = cv2.resize(prediction, (width, new_rows))
                else:
                    prediction = skit.resize(prediction, (new_rows, width))
                img = prediction[
                    ((prediction.shape[0] - height) // 2) : (
                        (prediction.shape[0] - height) // 2 + height
                    ),
                    :,
                ]

            if normalize:
                img = img / np.max(img) * 255
            heatmap_batch.append(img)

        return heatmap_batch

    @classmethod
    def _heatmap_overlays(
        cls,
        original_images: List[Image.Image],
        heatmaps: List[np.ndarray],
        colmap: str = "hot",
    ) -> List[np.ndarray]:
        """
        Overlay prediction heatmap on the original image.

        Args:
            original_images: List of original images
            heatmaps: Prediction heatmaps
            colmap: Heatmap style

        Returns:
            Prediction heatmap overlays
        """
        heatmap_overlay_batch: List[np.ndarray] = []
        for i, original_image in enumerate(original_images):
            heatmap: np.ndarray = heatmaps[i]
            cm_array: matplotlib.colors.ListedColormap = cm.get_cmap(colmap)
            im_array: np.ndarray = np.asarray(original_image)
            heatmap_norm: np.ndarray = (heatmap - np.min(heatmap)) / float(
                np.max(heatmap) - np.min(heatmap)
            )
            heatmap_cm: np.ndarray = cm_array(heatmap_norm)
            res_final: np.ndarray = im_array.copy()
            heatmap_rep: np.ndarray = np.repeat(
                heatmap_norm[:, :, np.newaxis], 3, axis=2
            )
            res_final[...] = heatmap_cm[
                ..., 0:3
            ] * 255.0 * heatmap_rep + im_array[...] * (1 - heatmap_rep)
            heatmap_overlay_batch.append(res_final)

        return heatmap_overlay_batch

    @classmethod
    def _crop_h(
        cls,
        img: Image.Image,
        h_levels: List[int],
    ) -> List[Image.Image]:
        """
        Crop the input image by the height levels.

        Args:
            img: Input image
            h_levels: Height levels

        Returns:
            List of cropped images
        """
        # Convert to np array
        img_arr = np.array(img)

        # Loop over the h_levels
        cropped_images: List[Image.Image] = []
        for idx in range(0, len(h_levels) - 1):

            # Crop the input based on h_levels
            start_crop: int = h_levels[idx]
            end_crop: int = h_levels[idx + 1]
            cropped_arr: np.ndarray = img_arr[start_crop:end_crop, :]
            cropped_im: Image.Image = Image.fromarray(cropped_arr)

            # Store cropped images
            cropped_images.append(cropped_im)
        return cropped_images

    @classmethod
    def _show_results(
        cls,
        original_images: List[Image.Image],
        heatmaps: List[np.ndarray],
        heatmap_overlays: List[np.ndarray],
    ) -> None:
        """
        Show results visualized.

        Args:
            original_images: List of original images
            heatmaps: Prediction heatmaps
            heatmap_overlays: Prediction heatmap overlays

        Returns:
            None
        """
        for i, _ in enumerate(original_images):
            plt.figure(figsize=[15, 7])
            plt.subplot(1, 3, 1)
            plt.imshow(original_images[i])
            plt.title("Original image")
            plt.subplot(1, 3, 2)
            plt.imshow(heatmaps[i])
            plt.title("Prediction heatmap")
            plt.subplot(1, 3, 3)
            plt.imshow(heatmap_overlays[i])
            plt.title("Prediction heatmap overlay")
            plt.show()

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
            - UMSI prediction heatmap (str, image (PNG) encoded in Base64)
            - UMSI prediction heatmap overlay (str, image (PNG) encoded in Base64)
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Compute height levels for the crop
        width, height = img_rgb.size
        h_levels = compute_crops_height(width, height)

        # Original images to be predicted: here is the cropped_images
        original_images: List[Image.Image] = []
        original_images = cls._crop_h(img_rgb, h_levels)

        # Preprocess images
        img_batch: np.ndarray = cls._preprocess_images(
            original_images, show=cls._SHOW
        )

        # Load model
        # The original model can be downloaded from here: http://predimportance.mit.edu/data/xception_cl_fus_aspp_imp1k_10kl-3cc0.1mse-5nss5bc_bs4_ep30_valloss-2.5774_full.h5
        model_filepath: pathlib.Path = pathlib.Path(
            "aim/metrics/m9/xception_cl_fus_aspp_imp1k_10kl-3cc0.1mse-5nss5bc_bs4_ep30_valloss-2.5774_full.h5"
        )
        model: keras.engine.training.Model = keras.models.load_model(
            model_filepath, compile=False, custom_objects={"K": K}
        )

        # Predict maps
        predictions: List[np.ndarray] = model.predict(img_batch)

        # Postprocess predictions
        heatmap_batch: List[np.ndarray] = cls._postprocess_predictions(
            original_images, predictions
        )

        # Create prediction heatmap overlays
        heatmap_overlay_batch: List[np.ndarray] = cls._heatmap_overlays(
            original_images, heatmap_batch, colmap=cls._HEATMAP_STYLE
        )

        # Show results
        if cls._SHOW:
            cls._show_results(
                original_images, heatmap_batch, heatmap_overlay_batch
            )

        # Concatenate all batch cropped images
        heatmap_batch_stack: np.ndarray = np.concatenate(heatmap_batch, axis=0)
        heatmap_overlay_batch_stack: np.ndarray = np.concatenate(
            heatmap_overlay_batch, axis=0
        )

        # Prepare final results
        img_umsi_prediction_heatmap: Image.Image = Image.fromarray(
            # Apply the color map, rescale to the 0-255 range, convert to
            # 8-bit unsigned integers. Note: Slight loss of accuracy due
            # the float32 to uint8 conversion.
            (cm.get_cmap("viridis")(heatmap_batch_stack) * 255).astype("uint8")
        ).convert("RGB")
        img_umsi_prediction_heatmap_overlay: Image.Image = Image.fromarray(
            heatmap_overlay_batch_stack
        ).convert("RGB")
        umsi_prediction_heatmap: str = image_utils.to_png_image_base64(
            img_umsi_prediction_heatmap
        )
        umsi_prediction_heatmap_overlay: str = image_utils.to_png_image_base64(
            img_umsi_prediction_heatmap_overlay
        )

        # Clean up to prevent Keras memory leaks
        # Source: https://www.thekerneltrip.com/python/keras-memory-leak/
        del model
        K.clear_session()
        _ = gc.collect()

        return [
            umsi_prediction_heatmap,
            umsi_prediction_heatmap_overlay,
        ]
