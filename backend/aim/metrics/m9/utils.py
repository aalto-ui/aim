#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UMSI utility functions.
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import Dict, Iterable, List, Union

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-06-14"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"

# ----------------------------------------------------------------------------
# UMSI utility functions
# ----------------------------------------------------------------------------

# Desktop, Mobile, Tablet, Console Screen Resolution Data From https://gs.statcounter.com/screen-resolution-stats
screen_resolutions: List[Dict] = [
    {"height": "2340", "width": "1080", "xusage": ["Mobile", "Console"]},
    {"height": "1920", "width": "1080", "xusage": ["Mobile"]},
    {"height": "1440", "width": "2560", "xusage": ["Desktop", "Console"]},
    {"height": "1366", "width": "1024", "xusage": ["Tablet", "Desktop"]},
    {"height": "1280", "width": "800", "xusage": ["Tablet"]},
    {"height": "1280", "width": "720", "xusage": ["Mobile"]},
    {"height": "1200", "width": "1920", "xusage": ["Desktop"]},
    {"height": "1194", "width": "834", "xusage": ["Tablet"]},
    {"height": "1152", "width": "2048", "xusage": ["Desktop"]},
    {"height": "1138", "width": "712", "xusage": ["Tablet"]},
    {"height": "1112", "width": "834", "xusage": ["Tablet", "Desktop"]},
    {"height": "1080", "width": "1920", "xusage": ["Desktop", "Console"]},
    {"height": "1080", "width": "810", "xusage": ["Tablet", "Desktop"]},
    {"height": "1050", "width": "1680", "xusage": ["Desktop"]},
    {"height": "1024", "width": "1280", "xusage": ["Desktop", "Console"]},
    {"height": "1024", "width": "768", "xusage": ["Tablet", "Desktop"]},
    {"height": "1024", "width": "600", "xusage": ["Tablet"]},
    {"height": "976", "width": "600", "xusage": ["Tablet"]},
    {"height": "962", "width": "601", "xusage": ["Tablet"]},
    {"height": "960", "width": "1280", "xusage": ["Desktop"]},
    {"height": "960", "width": "600", "xusage": ["Tablet"]},
    {"height": "960", "width": "540", "xusage": ["Mobile"]},
    {"height": "926", "width": "428", "xusage": ["Tablet", "Mobile"]},
    {
        "height": "915",
        "width": "412",
        "xusage": ["Tablet", "Mobile", "Console"],
    },
    {"height": "900", "width": "1600", "xusage": ["Desktop"]},
    {"height": "900", "width": "1440", "xusage": ["Desktop"]},
    {
        "height": "896",
        "width": "414",
        "xusage": ["Tablet", "Mobile", "Console"],
    },
    {
        "height": "892",
        "width": "412",
        "xusage": ["Tablet", "Mobile", "Console"],
    },
    {
        "height": "873",
        "width": "393",
        "xusage": ["Tablet", "Mobile", "Console"],
    },
    {
        "height": "869",
        "width": "412",
        "xusage": ["Tablet", "Mobile", "Console"],
    },
    {"height": "864", "width": "1536", "xusage": ["Desktop"]},
    {"height": "864", "width": "1152", "xusage": ["Desktop"]},
    {"height": "854", "width": "534", "xusage": ["Tablet"]},
    {"height": "854", "width": "480", "xusage": ["Mobile"]},
    {"height": "854", "width": "385", "xusage": ["Tablet", "Mobile"]},
    {
        "height": "851",
        "width": "393",
        "xusage": ["Tablet", "Mobile", "Console"],
    },
    {
        "height": "846",
        "width": "412",
        "xusage": ["Tablet", "Mobile", "Console"],
    },
    {
        "height": "844",
        "width": "390",
        "xusage": ["Tablet", "Mobile", "Console"],
    },
    {
        "height": "812",
        "width": "375",
        "xusage": ["Tablet", "Mobile", "Console"],
    },
    {"height": "800", "width": "1422", "xusage": ["Console"]},
    {"height": "800", "width": "1334", "xusage": ["Tablet"]},
    {"height": "800", "width": "1280", "xusage": ["Tablet", "Desktop"]},
    {"height": "800", "width": "480", "xusage": ["Mobile"]},
    {
        "height": "800",
        "width": "360",
        "xusage": ["Tablet", "Console", "Mobile", "Desktop"],
    },
    {
        "height": "780",
        "width": "360",
        "xusage": ["Tablet", "Console", "Mobile"],
    },
    {"height": "768", "width": "1366", "xusage": ["Desktop"]},
    {"height": "768", "width": "1360", "xusage": ["Desktop"]},
    {"height": "768", "width": "1280", "xusage": ["Desktop"]},
    {"height": "768", "width": "1024", "xusage": ["Tablet", "Desktop"]},
    {
        "height": "760",
        "width": "360",
        "xusage": ["Tablet", "Console", "Mobile"],
    },
    {"height": "752", "width": "1280", "xusage": ["Tablet"]},
    {"height": "745", "width": "1324", "xusage": ["Console"]},
    {
        "height": "740",
        "width": "360",
        "xusage": ["Tablet", "Console", "Mobile"],
    },
    {
        "height": "736",
        "width": "414",
        "xusage": ["Tablet", "Console", "Mobile"],
    },
    {"height": "732", "width": "412", "xusage": ["Mobile", "Console"]},
    {
        "height": "720",
        "width": "1280",
        "xusage": ["Tablet", "Desktop", "Console"],
    },
    {
        "height": "720",
        "width": "360",
        "xusage": ["Tablet", "Console", "Mobile"],
    },
    {"height": "712", "width": "1138", "xusage": ["Tablet"]},
    {"height": "675", "width": "1200", "xusage": ["Console"]},
    {"height": "670", "width": "1187", "xusage": ["Console"]},
    {
        "height": "667",
        "width": "375",
        "xusage": ["Tablet", "Console", "Mobile"],
    },
    {"height": "658", "width": "1170", "xusage": ["Console"]},
    {"height": "656", "width": "1167", "xusage": ["Console"]},
    {
        "height": "640",
        "width": "360",
        "xusage": ["Tablet", "Desktop", "Console", "Mobile"],
    },
    {"height": "628", "width": "800", "xusage": ["Console"]},
    {"height": "614", "width": "1093", "xusage": ["Desktop"]},
    {"height": "601", "width": "962", "xusage": ["Tablet"]},
    {"height": "600", "width": "1024", "xusage": ["Tablet", "Desktop"]},
    {"height": "600", "width": "960", "xusage": ["Tablet"]},
    {
        "height": "600",
        "width": "800",
        "xusage": ["Mobile", "Desktop", "Console"],
    },
    {"height": "595", "width": "1053", "xusage": ["Console"]},
    {"height": "586", "width": "1041", "xusage": ["Console"]},
    {"height": "570", "width": "320", "xusage": ["Mobile"]},
    {
        "height": "568",
        "width": "320",
        "xusage": ["Tablet", "Mobile", "Console"],
    },
    {"height": "552", "width": "1024", "xusage": ["Tablet"]},
    {"height": "540", "width": "960", "xusage": ["Console"]},
    {"height": "534", "width": "854", "xusage": ["Tablet"]},
    {"height": "534", "width": "320", "xusage": ["Mobile"]},
    {"height": "480", "width": "854", "xusage": ["Console"]},
    {"height": "480", "width": "800", "xusage": ["Tablet"]},
    {"height": "480", "width": "640", "xusage": ["Console"]},
    {"height": "480", "width": "320", "xusage": ["Mobile"]},
    {"height": "472", "width": "800", "xusage": ["Console"]},
    {"height": "461", "width": "614", "xusage": ["Console"]},
    {"height": "320", "width": "240", "xusage": ["Mobile"]},
    {"height": "240", "width": "320", "xusage": ["Mobile"]},
]


def compute_height(input_width: int) -> int:
    """
        Compute best matched height for the input width.

    Args:
        input_width (int): Input width

    Returns:
        best matched height (int)
    """

    res_candidates: List = []

    # Compute distance between input_width and existing width in resolutions
    for item in screen_resolutions:
        item_copy: Dict = item.copy()
        item_copy["distance"] = str(abs(int(item["width"]) - input_width))
        res_candidates.append(item_copy)

    # Compute the nearest one to the input width, most usage, less height
    res_candidates_sorted: List = sorted(
        res_candidates,
        key=lambda d: (
            int(d["distance"]),
            1 / len(d["xusage"]),
            int(d["height"]),
        ),
    )
    # Compute the best height: first item from the sorted list of res_candidates
    best_height: int = int(res_candidates_sorted[0]["height"])

    return best_height


def compute_crops_height(input_width: int, input_height: int) -> List[int]:
    """
        Compute crop heights.

    Args:
        input_width (int): Input width
        input_height (int): Input height

    Returns:
        List of crop Candidates (List[int])
    """
    # Compute the best matched height
    best_height: int = compute_height(input_width)
    # Crop size is the minimum size between input height and best matched height
    crop_height: int = min(best_height, input_height)
    # Compute crop candidates based on the input height and crop height
    cc_heights: List[int] = list(range(0, input_height + 1, crop_height))
    # Change last crop to the input height
    cc_heights[-1] = input_height

    return cc_heights
