#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model:
    UI segmentation and element detection


Description:
    This UI segmentation is mostly based on old-fashioned computer vision
    approaches to detect UI components and texts. Most part of this code is
    imported from https://github.com/MulongXie/UIED.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Xie, M., Feng, S., Xing, Z., Chen, J., and Chen, C. (2020). UIED: A
        Hybrid Tool for GUI Element Detection. In Proceedings of the 28th ACM
        Joint Meeting on European Software Engineering Conference and
        Symposium on the Foundations of Software Engineering (ESEC/FSE '20),
        pp. 1655-1659. ACM. doi: https://doi.org/10.1145/3368089.3417940

    2.  Chen, J., Xie, M., Xing, Z., Chen, C., Xu, X., Zhu, L., and Li, G.
        (2020). Object Detection for Graphical User Interface: Old Fashioned
        or Deep Learning or a Combination? In Proceedings of the 28th ACM
        Joint Meeting on European Software Engineering Conference and
        Symposium on the Foundations of Software Engineering (ESEC/FSE '20),
        pp. 1202-1214. ACM. doi: https://doi.org/10.1145/3368089.3409691


Change log:
    v1.0 (2022-08-05)
      * Initial implementation
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
import os
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple

# Third-party modules
import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
from pydantic import HttpUrl

# First-party modules
from aim.common import image_utils
from aim.common.constants import GUI_TYPE_DESKTOP, GUI_TYPE_MOBILE
from aim.segmentation.image_seg_utils import (
    Component,
    binarization,
    compo_block_recognition,
    compo_filter,
    component_detection,
    compos_containment,
    compos_update,
    corners2json,
    draw_bounding_box,
    merge_intersected_compos,
    nesting_inspection,
    resize_by_longest_edge,
    rm_contained_compos_not_in_block,
    rm_line,
    transform_img,
)
from aim.segmentation.merge_seg_utils import (
    Element,
    check_containment,
    merge_text_line_to_paragraph,
    reassign_ids,
    refine_elements,
    refine_texts,
    remove_top_bar,
    save_elements,
    show_elements,
)
from aim.segmentation.text_seg_utils import (
    Text,
    text2json,
    text_cvt_orc_format_paddle,
    visualize_texts,
)

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


class Segmentation:
    """
    UI segmentation and element detection.

    Reference: Based on Xie et al.'s Python implementation available at
    https://github.com/MulongXie/UIED (see LICENSE within the distribution).
    """

    # Private constants
    _IS_SHOW: bool = False  # show outputs
    _IS_CLF: bool = False  # use cnn classifier to determine type of components

    _KEY_PARAMS_DESKTOP: Dict = {
        "min-grad": 10,
        "ffl-block": 5,
        "min-ele-area": 300,
        "merge-contained-ele": True,
        "merge-line-to-paragraph": True,
        "remove-bar": False,
        "threshold-rec-min-evenness": 0.7,
        "threshold-rec-max-dent-ratio": 0.25,
        "threshold-line-thickness": 8,
        "threshold-line-min-length": 0.95,
        "max-line-gap": 20,
        "intersection-bias": 2,
        "max-text-height-ratio": 0.3,
        "resize": 800,
    }

    _KEY_PARAMS_MOBILE: Dict = {
        "min-grad": 5,
        "ffl-block": 5,
        "min-ele-area": 20,
        "merge-contained-ele": True,
        "merge-line-to-paragraph": True,
        "remove-bar": False,
        "threshold-rec-min-evenness": 0.7,
        "threshold-rec-max-dent-ratio": 0.25,
        "threshold-line-thickness": 8,
        "threshold-line-min-length": 0.95,
        "max-line-gap": 10,
        "intersection-bias": 2,
        "max-text-height-ratio": 0.3,
        "resize": 800,
    }

    # RICO CNN model: https://drive.google.com/file/d/1Gzpi-V_Sj7SSFQMNzy6bcgkEwaZBhGWS/view?usp=sharing
    # Component detection based on CNN architecture trained on RICO Dataset. It can classify UI elements into the
    # following classes: (Button, CheckBox, Chronometer, EditText, ImageButton, ImageView, ProgressBar, RadioButton,
    # RatingBar, SeekBar, Spinner, Switch, ToggleButton,  VideoView , TextView)
    _CNN_MODEL_PATH: str = os.path.join(
        os.path.dirname(__file__), "cnn-rico-1.h5"
    )
    # Shape of input images
    _CNN_INPUT_SHAPE: Tuple = (64, 64, 3)
    # Model output classes
    _CLASS_MAP: List[str] = [
        "Button",
        "CheckBox",
        "Chronometer",
        "EditText",
        "ImageButton",
        "ImageView",
        "ProgressBar",
        "RadioButton",
        "RatingBar",
        "SeekBar",
        "Spinner",
        "Switch",
        "ToggleButton",
        "VideoView",
        "TextView",
    ]
    if _IS_CLF:
        # Third-party modules
        from tensorflow.keras.models import load_model

        _CNN_MODEL = load_model(_CNN_MODEL_PATH)

    # Private methods
    @classmethod
    def compo_detection(
        cls,
        img: np.ndarray,
        img_resized: np.ndarray,
        key_params: Dict,
        classifier: bool = False,
        show: bool = False,
    ):
        # Step 1: Pre-processing: img -> get binary map
        grey: np.ndarray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        binary: np.ndarray = binarization(
            img_resized, grad_min=int(key_params["min-grad"]), show=False
        )

        # Step 2: Element detection
        binary = rm_line(
            binary,
            max_line_thickness=key_params["threshold-line-thickness"],
            min_line_length_ratio=key_params["threshold-line-min-length"],
            show=False,
        )
        uicompos: List[Component] = component_detection(
            binary,
            min_obj_area=int(key_params["min-ele-area"]),
            min_rec_evenness=key_params["threshold-rec-min-evenness"],
            max_dent_ratio=key_params["threshold-rec-max-dent-ratio"],
        )

        # Step 3: Results refinement
        uicompos = compo_filter(
            uicompos,
            min_area=int(key_params["min-ele-area"]),
            img_shape=binary.shape,
        )
        uicompos = merge_intersected_compos(uicompos)
        uicompos = compo_block_recognition(binary, uicompos)
        if key_params["merge-contained-ele"]:
            uicompos = rm_contained_compos_not_in_block(uicompos)
        uicompos = compos_update(uicompos, img_resized.shape)
        uicompos = compos_containment(uicompos)

        # Step 4: Nesting inspection (check if big compos have nesting element)
        uicompos += nesting_inspection(
            grey,
            uicompos,
            ffl_block=key_params["ffl-block"],
            line_thickness=key_params["threshold-line-thickness"],
            min_rec_evenness=key_params["threshold-rec-min-evenness"],
            max_dent_ratio=key_params["threshold-rec-max-dent-ratio"],
        )
        uicompos = compos_update(uicompos, img_resized.shape)

        # Step 5: Element classification (all category classification)
        if classifier:
            for compo in uicompos:
                im = compo.compo_clipping(img_resized)
                im_transformed: np.ndarray = transform_img(
                    im, cls._CNN_INPUT_SHAPE
                )
                compo.subcategory = cls._CLASS_MAP[
                    np.argmax(cls._CNN_MODEL.predict(im_transformed))
                ]

        # Step 6: Save detection result
        uicompos = compos_update(uicompos, img_resized.shape)
        # Resize to default
        uicompos = [
            uic.resize(img.shape[0] / img_resized.shape[0]) for uic in uicompos
        ]
        # Save JSON
        compo_json: Dict = corners2json(uicompos, img.shape)
        draw_bounding_box(
            img, uicompos, name="Components", show=show, write_path=None
        )
        return compo_json

    @classmethod
    def text_detection(
        cls,
        img: np.ndarray,
        paddle_model: PaddleOCR = None,
        show: bool = False,
    ):
        """
        :param img:
        :param paddle_model: the preload paddle model for paddle ocr
        :param show:
        """
        # If you have issues with tools.infer see this issue:
        # https://github.com/PaddlePaddle/PaddleOCR/issues/1024#issuecomment-1105946934
        if paddle_model is None:
            paddle_model = PaddleOCR(
                use_angle_cls=True, lang="ch", show_log=False
            )
        paddle_result = paddle_model.ocr(img, cls=True)
        texts: List[Text] = text_cvt_orc_format_paddle(paddle_result)

        visualize_texts(
            img, texts, color=(0, 0, 255), line=1, write_path=None, show=show
        )
        text_json: Dict = text2json(texts, img.shape)
        return text_json

    @classmethod
    def merge(
        cls,
        img: np.ndarray,
        compo_json: Dict,
        text_json: Dict,
        key_params: Dict,
        show: bool = False,
    ):
        # Load text and non-text compo
        ele_id: int = 0
        compos: List[Element] = []
        for compo in compo_json["segments"]:
            element: Element = Element(
                ele_id,
                (
                    compo["column_min"],
                    compo["row_min"],
                    compo["column_max"],
                    compo["row_max"],
                ),
                compo["class"],
                compo["subclass"],
            )
            compos.append(element)
            ele_id += 1
        texts: List[Element] = []
        for text in text_json["texts"]:
            element = Element(
                ele_id,
                (
                    text["column_min"],
                    text["row_min"],
                    text["column_max"],
                    text["row_max"],
                ),
                "Text",
                text_content=text["content"],
            )
            texts.append(element)
            ele_id += 1

        # Show resized detected elements
        show_elements(
            img, texts + compos, show=show, win_name="Elements Before Merging"
        )

        # Refine elements
        texts = refine_texts(
            texts,
            img.shape,
            max_height_ratio=key_params["max-text-height-ratio"],
        )
        elements: List[Element] = refine_elements(
            compos,
            texts,
            intersection_bias=(
                key_params["intersection-bias"],
                key_params["intersection-bias"],
            ),
            containment_ratio=0.8,
        )

        if key_params["remove-bar"]:
            elements = remove_top_bar(elements, img_height=img.shape[0])

        if key_params["merge-line-to-paragraph"]:
            elements = merge_text_line_to_paragraph(
                elements, max_line_gap=key_params["max-line-gap"]
            )
        elements = reassign_ids(elements)
        elements = check_containment(
            elements,
            bias=(
                key_params["intersection-bias"],
                key_params["intersection-bias"],
            ),
        )

        # Save all merged elements, clips and blank background
        components: Dict = save_elements(elements, img.shape)
        board: np.ndarray = show_elements(
            img,
            elements,
            show=show,
            win_name="Elements After Merging",
            write_path=None,
        )
        return board, components

    @classmethod
    def execute(
        cls,
        gui_image: str,
        gui_type: int = GUI_TYPE_DESKTOP,
        gui_url: Optional[HttpUrl] = None,
    ) -> Dict[str, Any]:
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get NumPy array
        img_rgb_nparray: np.ndarray = np.array(img_rgb)

        # Convert NumPy array to Cv2 format (BGR)
        img_cv: np.ndarray = cv2.cvtColor(img_rgb_nparray, cv2.COLOR_RGB2BGR)

        # Select Parameters
        KEY_PARAMS: Dict = (
            cls._KEY_PARAMS_MOBILE
            if gui_type == GUI_TYPE_MOBILE
            else cls._KEY_PARAMS_DESKTOP
        )

        # Resize Input image
        img_cv_resized: np.ndarray = resize_by_longest_edge(
            img_cv, KEY_PARAMS["resize"]
        )

        # Show Original Image
        if cls._IS_SHOW:
            cv2.imshow("Original Image", img_cv)
            cv2.waitKey(0)
            cv2.destroyWindow("Original Image")

        # Text detection
        text_json: Dict = cls.text_detection(
            img_cv, paddle_model=None, show=cls._IS_SHOW
        )

        # Image detection
        compo_json: Dict = cls.compo_detection(
            img_cv,
            img_cv_resized,
            KEY_PARAMS,
            classifier=cls._IS_CLF,
            show=cls._IS_SHOW,
        )

        # Merge
        components: Dict[str, Any]
        board_bgr: np.ndarray
        board_bgr, components = cls.merge(
            img_cv, compo_json, text_json, KEY_PARAMS, show=cls._IS_SHOW
        )

        # Convert board to Pillow image format
        board_rgb: np.ndarray = cv2.cvtColor(board_bgr, cv2.COLOR_BGR2RGB)
        board_im: Image.Image = Image.fromarray(board_rgb)

        # Convert board to b64 (str)
        board_b64: str = image_utils.to_png_image_base64(board_im)

        # Save in component dictionary
        components["img_b64"] = board_b64

        return components
