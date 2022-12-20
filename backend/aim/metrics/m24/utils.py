#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AIM legacy segmentation utility functions.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Third-party modules
import cv2
import numpy as np
import scipy.spatial as spatial

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine, Khushhall Chandra Mahajan, Janin Koch, Samuli De Pascale"
__date__ = "2022-08-05"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# AIM legacy segmentation utility functions
# ----------------------------------------------------------------------------


class BBox(object):
    def __init__(self, x1, y1, x2, y2):
        # (x1, y1) is the upper left corner,
        # (x2, y2) is the lower right corner,
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def taxicab_diagonal(self):
        return self.x2 - self.x1 + self.y2 - self.y1

    def overlaps(self, other):
        # Return True if self and other overlap.
        return not (
            (self.x1 > other.x2)
            or (self.x2 < other.x1)
            or (self.y1 > other.y2)
            or (self.y2 < other.y1)
        )


def makeClassFromCont(contours):
    bboxes = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w < 5 or h < 5:
            continue
        bboxes.append(BBox(x, y, x + w, y + h))
    return bboxes


def remove_overlaps(contours):
    # This function returns a set of bboxes after removing the overlapping contours
    bboxes = makeClassFromCont(contours)

    corners = []
    ulcorners = []

    # dict mapping corners to Bboxes.
    bbox_map = {}

    for bbox in bboxes:
        ul = (bbox.x1, bbox.y1)
        lr = (bbox.x2, bbox.y2)
        bbox_map[ul] = bbox
        bbox_map[lr] = bbox
        ulcorners.append(ul)
        corners.append(ul)
        corners.append(lr)

    try:
        tree = spatial.KDTree(np.asarray(corners))
    except Exception:
        return 0

    for corner in ulcorners:
        bbox = bbox_map[corner]

        # Find all points which are within a taxicab distance of corner
        indices = tree.query_ball_point(
            corner, bbox_map[corner].taxicab_diagonal(), p=1
        )
        for near_corner in tree.data[indices]:
            near_bbox = bbox_map[tuple(near_corner)]
            if bbox != near_bbox and bbox.overlaps(near_bbox):
                # Expand both the bboxes
                bbox.x1 = near_bbox.x1 = min(bbox.x1, near_bbox.x1)
                bbox.y1 = near_bbox.y1 = min(bbox.y1, near_bbox.y1)
                bbox.x2 = near_bbox.x2 = max(bbox.x2, near_bbox.x2)
                bbox.y2 = near_bbox.y2 = max(bbox.y2, near_bbox.y2)

    return set(bbox_map.values())
