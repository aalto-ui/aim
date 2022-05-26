#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HSV math utility functions.
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import Callable

# Third-party modules
import numpy as np

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2021-05-26"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"

# ----------------------------------------------------------------------------
# HSV math utility functions
# ----------------------------------------------------------------------------


sind: Callable[[float], float] = lambda degrees: np.sin(np.deg2rad(degrees))
cosd: Callable[[float], float] = lambda degrees: np.cos(np.deg2rad(degrees))

# artan2 function from: https://stackoverflow.com/questions/35749246/python-atan-or-atan2-what-should-i-use
atan2: Callable[[float, float], float] = lambda c, s: np.pi * (
    1.0
    - 0.5 * (1 + np.sign(c)) * (1 - np.sign(s**2))
    - 0.25 * (2 + np.sign(c)) * np.sign(s)
) - np.sign(c * s) * np.arctan(
    (np.abs(c) - np.abs(s)) / (np.abs(c) + np.abs(s))
)

atan2d: Callable[[float, float], float] = (
    lambda c, s: atan2(c, s) * 180.0 / np.pi
)

np_sind = np.vectorize(sind)
np_cosd = np.vectorize(cosd)
