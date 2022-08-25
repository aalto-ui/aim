#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Text Segmentation utility functions.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import Dict, List, Optional, Tuple, Union

# Third-party modules
import cv2
import numpy as np

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2021-08-05"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Text Segmentation utility functions
# ----------------------------------------------------------------------------


class Text:
    def __init__(self, id, content, location):
        self.id = id
        self.content = content
        self.location = location

        self.width = self.location["right"] - self.location["left"]
        self.height = self.location["bottom"] - self.location["top"]
        self.area = self.width * self.height
        self.word_width = self.width / len(self.content)

    def visualize_element(self, img, color, line, show=False):
        loc = self.location
        cv2.rectangle(
            img,
            (loc["left"], loc["top"]),
            (loc["right"], loc["bottom"]),
            color,
            line,
        )
        if show:
            cv2.imshow("text", img)
            cv2.waitKey()
            cv2.destroyWindow("text")


def visualize_texts(
    org_img, texts, color=(0, 0, 255), line=2, show=False, write_path=None
):
    img = org_img.copy()
    for text in texts:
        text.visualize_element(img, color=color, line=line)

    if show:
        cv2.imshow("Texts", img)
        cv2.waitKey(0)
        cv2.destroyWindow("Texts")

    if write_path is not None:
        cv2.imwrite(write_path, img)


def text2json(texts, img_shape):
    output = {"img_shape": img_shape, "texts": []}
    for text in texts:
        c = {"id": text.id, "content": text.content}
        loc = text.location
        c["column_min"], c["row_min"], c["column_max"], c["row_max"] = (
            loc["left"],
            loc["top"],
            loc["right"],
            loc["bottom"],
        )
        c["width"] = text.width
        c["height"] = text.height
        output["texts"].append(c)
    return output


def text_cvt_orc_format_paddle(paddle_result):
    texts = []
    for i, line in enumerate(paddle_result):
        points = np.array(line[0])
        location = {
            "left": int(min(points[:, 0])),
            "top": int(min(points[:, 1])),
            "right": int(max(points[:, 0])),
            "bottom": int(max(points[:, 1])),
        }
        content = line[1][0]
        texts.append(Text(i, content, location))
    return texts
