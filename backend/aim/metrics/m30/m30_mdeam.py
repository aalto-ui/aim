#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    MDEAM (Multi-duration Element Attention Model)


Description:
    The predicted human attention under three viewing durations, visualized as heatmaps of three durations (0.5, 3, and 5 seconds).


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Y. Wang, M. Bâce and A. Bulling, "Scanpath Prediction on Information Visualisations,"
        in IEEE Transactions on Visualization and Computer Graphics. doi: 10.1109/TVCG.2023.3242293


Change log:
    v1.0 (2023-06-09)
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

# isort: off
# Third-party modules - Ignore Keras outputs and logs
stderr = sys.stderr
sys.stderr = open(os.devnull, "w")
import keras  # noqa: E402
import keras.backend as K  # noqa: E402

from aim.metrics.m30.multiduration_models import xception_se_lstm

sys.stderr = stderr
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

warnings.filterwarnings("ignore", category=UserWarning, module="keras.*")
# isort: on


# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine, Yao Wang"
__date__ = "2023-06-07"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: MDEAM (Multi-duration Element Attention Model).

    Reference:
        Based on Wang et al.'s Python implementation available at https://darus.uni-stuttgart.de/dataset.xhtml?persistentId=doi:10.18419/darus-3361 (see LICENSE within the distribution: https://darus.uni-stuttgart.de/dataset.xhtml?persistentId=doi:10.18419/darus-3361&version=1.0&selectTab=termsTab).
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
            prediction0: np.ndarray = predictions[0][i, 0, :, :, 0]
            prediction1: np.ndarray = predictions[0][i, 1, :, :, 0]
            prediction2: np.ndarray = predictions[0][i, 2, :, :, 0]
            prediction_shape: Tuple[int, ...] = prediction0.shape
            rows_rate: float = height / prediction_shape[0]
            cols_rate: float = width / prediction_shape[1]

            if blur:
                sigma: bool = blur
                prediction0 = scipy.ndimage.filters.gaussian_filter(
                    prediction0, sigma=sigma
                )
                prediction1 = scipy.ndimage.filters.gaussian_filter(
                    prediction1, sigma=sigma
                )
                prediction2 = scipy.ndimage.filters.gaussian_filter(
                    prediction2, sigma=sigma
                )

            img: np.ndarray
            if rows_rate > cols_rate:
                new_cols: int = (
                    prediction_shape[1] * height
                ) // prediction_shape[0]
                if cls._USE_CV2:
                    prediction1 = cv2.resize(prediction1, (new_cols, height))
                else:
                    prediction1 = skit.resize(prediction1, (height, new_cols))
                img0 = prediction0[
                    :,
                    ((prediction0.shape[1] - width) // 2) : (
                        (prediction0.shape[1] - width) // 2 + width
                    ),
                ]
                img1 = prediction1[
                    :,
                    ((prediction1.shape[1] - width) // 2) : (
                        (prediction1.shape[1] - width) // 2 + width
                    ),
                ]
                img2 = prediction2[
                    :,
                    ((prediction2.shape[1] - width) // 2) : (
                        (prediction2.shape[1] - width) // 2 + width
                    ),
                ]
            else:
                new_rows: int = (
                    prediction_shape[0] * width
                ) // prediction_shape[1]
                if cls._USE_CV2:
                    prediction1 = cv2.resize(prediction1, (width, new_rows))
                else:
                    prediction1 = skit.resize(prediction1, (new_rows, width))
                img0 = prediction0[
                    ((prediction0.shape[0] - height) // 2) : (
                        (prediction0.shape[0] - height) // 2 + height
                    ),
                    :,
                ]
                img1 = prediction1[
                    ((prediction1.shape[0] - height) // 2) : (
                        (prediction1.shape[0] - height) // 2 + height
                    ),
                    :,
                ]
                img2 = prediction2[
                    ((prediction2.shape[0] - height) // 2) : (
                        (prediction2.shape[0] - height) // 2 + height
                    ),
                    :,
                ]

            if normalize:
                img0 = img0 / np.max(img0) * 255
                img1 = img1 / np.max(img1) * 255
                img2 = img2 / np.max(img2) * 255
            heatmap_batch.append(img0)
            heatmap_batch.append(img1)
            heatmap_batch.append(img2)

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

        # Original images to be predicted
        original_images: List[Image.Image] = []
        original_images.append(img_rgb)

        # Preprocess images
        img_batch: np.ndarray = cls._preprocess_images(
            original_images, show=cls._SHOW
        )

        # Load model
        model_filepath: pathlib.Path = pathlib.Path(
            "aim/metrics/m30/massvis_bucket_500_2000_5000_kl10cc-5nss-1ccmatch3_ep06_valloss1.1899.hdf5"
        )

        loaded_model = xception_se_lstm(input_shape = (240,320,3), n_outs = 3, ups=16, verbose=False)

        loaded_model.load_weights(model_filepath)

        # Predict maps
        predictions: List[np.ndarray] = loaded_model.predict(img_batch)

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

        # Prepare final results
        # Apply the color map, rescale to the 0-255 range, convert to
        # 8-bit unsigned integers. Note: Slight loss of accuracy due
        # the float32 to uint8 conversion.
        img_umsi_prediction_heatmap0: Image.Image = Image.fromarray(
            (cm.get_cmap("viridis")(heatmap_batch[0]) * 255).astype("uint8")
        ).convert("RGB")
        img_umsi_prediction_heatmap1: Image.Image = Image.fromarray(
            (cm.get_cmap("viridis")(heatmap_batch[1]) * 255).astype("uint8")
        ).convert("RGB")
        img_umsi_prediction_heatmap2: Image.Image = Image.fromarray(
            (cm.get_cmap("viridis")(heatmap_batch[2]) * 255).astype("uint8")
        ).convert("RGB")
        img_umsi_prediction_heatmap_overlay: Image.Image = Image.fromarray(
            heatmap_overlay_batch[0]
        ).convert("RGB")
        umsi_prediction_heatmap0: str = image_utils.to_png_image_base64(
            img_umsi_prediction_heatmap0
        )
        umsi_prediction_heatmap1: str = image_utils.to_png_image_base64(
            img_umsi_prediction_heatmap1
        )
        umsi_prediction_heatmap2: str = image_utils.to_png_image_base64(
            img_umsi_prediction_heatmap2
        )
        umsi_prediction_heatmap_overlay: str = image_utils.to_png_image_base64(
            img_umsi_prediction_heatmap_overlay
        )

        # Clean up to prevent Keras memory leaks
        # Source: https://www.thekerneltrip.com/python/keras-memory-leak/
        del loaded_model
        K.clear_session()
        _ = gc.collect()

        return [
            umsi_prediction_heatmap0,
            umsi_prediction_heatmap1,
            umsi_prediction_heatmap2,
            umsi_prediction_heatmap_overlay,
        ]
