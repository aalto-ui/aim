#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Static clusters


Description:
    The number of static 32-sized color clusters; only clusters with more
    than five values are counted.

    In previous papers [2, 3], Miniukovich et al. use color reduction; only
    RGB values covering more than five pixels (for desktop) or two pixels
    (for mobile) are counted). However, in their most recent work [1], color
    reduction is not used; instead, clusters with more than five values are
    counted. As [1] is their most recent work, this code follows its
    approach.

    Category: Visual complexity > Information amount > Color variability >
    Dominant colors. For details, see CV4 [1], A1 [2], and C6 [3].


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Miniukovich, A. and De Angeli, A. (2015). Computation of Interface
        Aesthetics. In Proceedings of the 33rd Annual ACM Conference on Human
        Factors in Computing Systems (CHI '15), pp. 1163-1172. ACM.
        doi: https://doi.org/10.1145/2702123.2702575

    2.  Miniukovich, A. and De Angeli, A. (2014). Visual Impressions of Mobile
        App Interfaces. In Proceedings of the 8th Nordic Conference on
        Human-Computer Interaction (NordiCHI '14), pp. 31-40. ACM.
        doi: https://doi.org/10.1145/2639189.2641219

    3.  Miniukovich, A. and De Angeli, A. (2014). Quantification of Interface
        Visual Complexity. In Proceedings of the 2014 International Working
        Conference on Advanced Visual Interfaces (AVI '14), pp. 153-160. ACM.
        doi: https://doi.org/10.1145/2598153.2598173


Change log:
    v2.0 (2022-05-16)
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
from pydantic import HttpUrl

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
    Metric: Static clusters.
    """

    # Private constants
    _CUBE_SIZE: int = 32  # the sub-cube edge size of clusters is 32 values out of possible 256
    _IMTOCUBE_DIV: float = 256 / _CUBE_SIZE  # 8.0
    _CLUSTER_REDUCTION_THRESHOLD: int = (
        5  # only clusters containing more than 5 values are counted
    )

    # Public methods
    @classmethod
    def execute_metric(
        cls,
        gui_image: str,
        gui_type: int = GUI_TYPE_DESKTOP,
        gui_url: Optional[HttpUrl] = None,
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1
            gui_url: GUI URL (defaults to None)

        Returns:
            Results (list of measures)
            - Number of static color clusters (int, [0, 32^3))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (should be RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Calculate total number of image pixels
        total_pixels: int = img_rgb.width * img_rgb.height

        # Get RGB color histogram
        rgb_color_histogram: List[Tuple[int, Tuple]] = img_rgb.getcolors(
            maxcolors=total_pixels
        )

        # Divide RGB spectrum (0-255) to a (cls._CUBE_SIZE, cls._CUBE_SIZE, cls._CUBE_SIZE) matrix
        cluster: np.ndarray = np.zeros(
            (cls._CUBE_SIZE, cls._CUBE_SIZE, cls._CUBE_SIZE)
        )
        for h in list(rgb_color_histogram):
            h_count, h_rgb = h
            rc, gc, bc = tuple(int(i / cls._IMTOCUBE_DIV) for i in h_rgb)
            cluster[rc, gc, bc] += h_count

        # The amount of cells that have more than cls._CLUSTER_REDUCTION_THRESHOLD entries
        n_clusters: int = int(
            (cluster > cls._CLUSTER_REDUCTION_THRESHOLD).sum()
        )

        return [
            n_clusters,
        ]
