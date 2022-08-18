#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Distinct RGB values per dynamic clusters


Description:
    Ratio of distinct RGB values to the number of dynamic clusters.
    The number of dynamic color clusters after color reduction; only RGB
    values covering more than five pixels are counted. If a difference
    between two colors in a color cube is less than or equal to three, two
    colors are united in the same cluster, which continues recursively for
    all colors.

    Category: Visual complexity > Color variability > Color range (Color depth)
    For details, see CV5 [1], A8 [2]


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

Change log:
    v2.0 (2022-06-09)
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
from aim.common.constants import GUI_TYPE_DESKTOP, GUI_TYPE_MOBILE
from aim.metrics.interfaces import AIMMetricInterface
from aim.metrics.m12.m12_dynamic_clusters import Metric as M12_Metric

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine, Thomas Langerak, Yuxi Zhu"
__date__ = "2022-06-09"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Distinct RGB values per dynamic clusters.
    """

    # get_dynamic_clusters is imported from the same method in metric m12.
    _get_dynamic_clusters = M12_Metric._get_dynamic_clusters

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
            - Ratio of distinct RGB values per dynamic clusters (float)
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (should be RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get dynamic clusters of the input image
        center_of_clusters = cls._get_dynamic_clusters(img_rgb, gui_type)

        # Number of clusters
        count_dynamic_cluster: int = int(len(center_of_clusters))

        # Count number of distinct RGB values in clusters
        num_distinct_rgb: int = int(0)
        for x in range(len(center_of_clusters)):
            num_distinct_rgb += center_of_clusters[x][4]

        # Ratio of distinct RGB values per dynamic clusters
        ratio_unq_colors_dynamic_cluster: float = float(0)
        if count_dynamic_cluster != 0:
            ratio_unq_colors_dynamic_cluster = float(
                num_distinct_rgb / count_dynamic_cluster
            )

        return [ratio_unq_colors_dynamic_cluster]
