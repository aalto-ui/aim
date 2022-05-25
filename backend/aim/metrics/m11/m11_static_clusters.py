#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Static Clusters


Description:
    The number of static 32-sized color clusters.

    Category: Colour Perception.

    The number of static 32-sized color clusters (the sub-cube edge size of clusters is 32 values out of possible 256,
    per each RGB channel). Only clusters containing more than 5 values are counted. It is significant factor for
    dominant colours and clutter, but not for colour variance. CR3 is proven to be more accurate, though also more
    computational complex.



Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Miniukovich, A. and De Angeli, A. (2015). Computation of Interface
        Aesthetics. In Proceedings of the 33rd Annual ACM Conference on Human
        Factors in Computing Systems (CHI '15), pp. 1163-1172. ACM.
        doi: https://doi.org/10.1145/2702123.2702575

    2.  Miniukovich, A. and De Angeli, A. (2014). Quantification of Interface
        Visual Complexity. In Proceedings of the 2014 International Working
        Conference on Advanced Visual Interfaces (AVI '14), pp. 153-160. ACM.
        doi: https://doi.org/10.1145/2598153.2598173

Change log:
    v2.0 (2021-05-16)
      * Revised implementation

    v1.0 (2017-05-29)
      * Initial implementation
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
from io import BytesIO
from typing import List, Optional, Tuple, Union

# Third-party modules
import numpy as np
from PIL import Image

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine, Thomas Langerak, Yuxi Zhu"
__date__ = "2022-05-16"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Static Clusters.
    """

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
            - Static Clusters (int, [0, 32^3))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (should be RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")
        # Calculate total number of image pixels
        total_pixels: int = img_rgb.width * img_rgb.height

        # Get RGB color histogram
        # Get unique colours and their frequencies
        rgb_color_histogram: List[Tuple[int, Tuple]] = img_rgb.getcolors(
            maxcolors=total_pixels
        )

        # Divide rgb spectrum (0-255) to a 32x32x32 matrix
        cluster: np.ndarray = np.zeros((32, 32, 32))
        for h in list(rgb_color_histogram):
            h_count, h_value = h
            rc, gc, bc = tuple(int(i / 8) for i in h_value)
            cluster[rc, gc, bc] += h_count

        # The amount of cells that have more than 5 entries
        num_clusters: int = int((cluster > 5).sum())

        return [
            num_clusters,
        ]
