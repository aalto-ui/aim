#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Merge (Image and Text) Segmentation utility functions.
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
# Merge (Image and Text) Segmentation utility functions.
# ----------------------------------------------------------------------------


class Element:
    def __init__(
        self, id, corner, category, subcategory=None, text_content=None
    ):
        self.id = id
        self.category = category
        self.subcategory = subcategory
        self.col_min, self.row_min, self.col_max, self.row_max = corner
        self.width = self.col_max - self.col_min
        self.height = self.row_max - self.row_min
        self.area = self.width * self.height

        self.text_content = text_content
        self.parent_id = None
        self.children = []  # list of elements

    def init_bound(self):
        self.width = self.col_max - self.col_min
        self.height = self.row_max - self.row_min
        self.area = self.width * self.height

    def put_bbox(self):
        return self.col_min, self.row_min, self.col_max, self.row_max

    def wrap_info(self):
        info = {
            "id": self.id,
            "class": self.category,
            "subclass": self.subcategory,
            "height": self.height,
            "width": self.width,
            "position": {
                "column_min": self.col_min,
                "row_min": self.row_min,
                "column_max": self.col_max,
                "row_max": self.row_max,
            },
        }
        if self.text_content is not None:
            info["text_content"] = self.text_content
        if len(self.children) > 0:
            info["children"] = []
            for child in self.children:
                info["children"].append(child.id)
        if self.parent_id is not None:
            info["parent"] = self.parent_id
        return info

    def resize(self, resize_ratio):
        self.col_min = int(self.col_min * resize_ratio)
        self.row_min = int(self.row_min * resize_ratio)
        self.col_max = int(self.col_max * resize_ratio)
        self.row_max = int(self.row_max * resize_ratio)
        self.init_bound()
        return self

    def element_merge(
        self, element_b, new_element=False, new_category=None, new_id=None
    ):
        col_min_a, row_min_a, col_max_a, row_max_a = self.put_bbox()
        col_min_b, row_min_b, col_max_b, row_max_b = element_b.put_bbox()
        new_corner = (
            min(col_min_a, col_min_b),
            min(row_min_a, row_min_b),
            max(col_max_a, col_max_b),
            max(row_max_a, row_max_b),
        )
        if element_b.text_content is not None:
            self.text_content = (
                element_b.text_content
                if self.text_content is None
                else self.text_content + "\n" + element_b.text_content
            )
        if new_element:
            return Element(new_id, new_corner, new_category)
        else:
            self.col_min, self.row_min, self.col_max, self.row_max = new_corner
            self.init_bound()

    def calc_intersection_area(self, element_b, bias=(0, 0)):
        a = self.put_bbox()
        b = element_b.put_bbox()
        col_min_s = max(a[0], b[0]) - bias[0]
        row_min_s = max(a[1], b[1]) - bias[1]
        col_max_s = min(a[2], b[2])
        row_max_s = min(a[3], b[3])
        w = np.maximum(0, col_max_s - col_min_s)
        h = np.maximum(0, row_max_s - row_min_s)
        inter = w * h

        iou = inter / (self.area + element_b.area - inter)
        ioa = inter / self.area
        iob = inter / element_b.area

        return inter, iou, ioa, iob

    def element_relation(self, element_b, bias=(0, 0)):
        """
        @bias: (horizontal bias, vertical bias)
        :return: -1 : a in b
                 0  : a, b are not intersected
                 1  : b in a
                 2  : a, b are identical or intersected
        """
        inter, iou, ioa, iob = self.calc_intersection_area(element_b, bias)

        # area of intersection is 0
        if ioa == 0:
            return 0
        # a in b
        if ioa >= 1:
            return -1
        # b in a
        if iob >= 1:
            return 1
        return 2

    def visualize_element(self, img, color, line, show=False):
        loc = self.put_bbox()
        cv2.rectangle(img, loc[:2], loc[2:], color, line)
        if show:
            cv2.imshow("Element", img)
            cv2.waitKey(0)
            cv2.destroyWindow("Element")


def show_elements(
    org_img, eles, show=False, win_name="Element", line=2, write_path=None
):
    color_map = {
        "Text": (0, 0, 255),
        "Component": (0, 255, 0),
        "Block": (0, 255, 0),
        "Text Content": (255, 0, 255),
    }
    img = org_img.copy()
    for ele in eles:
        color = color_map[ele.category]
        ele.visualize_element(img, color, line)

    if show:
        cv2.imshow(win_name, img)
        cv2.waitKey(0)
        cv2.destroyWindow(win_name)

    if write_path is not None:
        cv2.imwrite(write_path, img)
    return img


def save_elements(elements, img_shape):
    components = {"segments": [], "img_shape": img_shape}
    for i, ele in enumerate(elements):
        c = ele.wrap_info()
        components["segments"].append(c)
    return components


def reassign_ids(elements):
    for i, element in enumerate(elements):
        element.id = i

    return elements


def refine_texts(texts, img_shape, max_height_ratio):
    refined_texts = []
    for text in texts:
        # remove potential noise
        if (
            len(text.text_content) > 1
            and text.height / img_shape[0] < max_height_ratio
        ):
            refined_texts.append(text)
    return refined_texts


def merge_text_line_to_paragraph(elements, max_line_gap):
    texts = []
    non_texts = []
    for ele in elements:
        if ele.category == "Text":
            texts.append(ele)
        else:
            non_texts.append(ele)

    changed = True
    while changed:
        changed = False
        temp_set = []
        for text_a in texts:
            merged = False
            for text_b in temp_set:
                inter_area, _, _, _ = text_a.calc_intersection_area(
                    text_b, bias=(0, max_line_gap)
                )
                if inter_area > 0:
                    text_b.element_merge(text_a)
                    merged = True
                    changed = True
                    break
            if not merged:
                temp_set.append(text_a)
        texts = temp_set.copy()
    return non_texts + texts


def refine_elements(
    compos, texts, intersection_bias=(2, 2), containment_ratio=0.8
):
    """
    1. remove compos contained in text
    2. remove compos containing text area that's too large
    3. store text in a compo if it's contained by the compo as the compo's text child element
    """
    elements = []
    contained_texts = []
    for compo in compos:
        is_valid = True
        text_area = 0
        for text in texts:
            inter, iou, ioa, iob = compo.calc_intersection_area(
                text, bias=intersection_bias
            )
            if inter > 0:
                # the non-text is contained in the text compo
                if ioa >= containment_ratio:
                    is_valid = False
                    break
                text_area += inter
                # the text is contained in the non-text compo
                if iob >= containment_ratio and compo.category != "Block":
                    contained_texts.append(text)
        if is_valid and text_area / compo.area < containment_ratio:
            # for t in contained_texts:
            #     t.parent_id = compo.id
            # compo.children += contained_texts
            elements.append(compo)

    # elements += texts
    for text in texts:
        if text not in contained_texts:
            elements.append(text)
    return elements


def check_containment(elements, bias=(2, 2)):
    new_elements = elements.copy()
    for i in range(len(new_elements) - 1):
        for j in range(i + 1, len(new_elements)):
            relation = new_elements[i].element_relation(new_elements[j], bias)
            if relation == -1:
                new_elements[j].children.append(new_elements[i])
                new_elements[i].parent_id = new_elements[j].id
            if relation == 1:
                new_elements[i].children.append(new_elements[j])
                new_elements[j].parent_id = new_elements[i].id

    return new_elements


def remove_top_bar(elements, img_height):
    new_elements: List[Element] = []
    max_height: float = img_height * 0.04
    for ele in elements:
        if ele.row_min < 10 and ele.height < max_height:
            continue
        new_elements.append(ele)
    return new_elements
