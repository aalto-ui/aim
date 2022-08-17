#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Dynamic clusters


Description:
    The number of dynamic color clusters after color reduction; only RGB
    values covering more than five pixels are counted. If a difference
    between two colors in a color cube is less than or equal to three, two
    colors are united in the same cluster, which continues recursively for
    all colors.

    Category: Visual complexity > Information amount > Color variability >
    Dominant colors. For details, see CV5 [1], A2 [2], and C7 [3].


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
    Metric: Dynamic clusters.
    """

    # Private constants
    # Color points with enough presence: The papers [1,2] do not indicate any difference between desktop and
    # mobile thresholds, but for mobile a lower number (e.g., 2) can be used if another source recommends it.
    _COLOR_REDUCTION_THRESHOLD_DESKTOP: int = 5
    _COLOR_REDUCTION_THRESHOLD_MOBILE: int = 5
    _DISTANCE_THRESHOLD: int = 3  # If the distance in all color components is less than 3, two colors are united in the same cluster

    # Private methods
    @classmethod
    def _get_dynamic_clusters(
        cls,
        img_rgb: Image.Image,
        gui_type: int = GUI_TYPE_DESKTOP,
    ) -> List:
        """
        Get dynamic clusters of the input image.

        Args:
            img_rgb: input RGB image

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1

        Returns:
            List of computed dynamic clusters
        """
        # Determine color cluster threshold
        _CLUSTER_THRESHOLD: int = (
            cls._COLOR_REDUCTION_THRESHOLD_MOBILE
            if gui_type == GUI_TYPE_MOBILE
            else cls._COLOR_REDUCTION_THRESHOLD_DESKTOP
        )

        # Calculate total number of image pixels
        total_pixels: int = img_rgb.width * img_rgb.height

        # Get RGB color histogram
        rgb_color_histogram: List[Tuple[int, Tuple]] = img_rgb.getcolors(
            maxcolors=total_pixels
        )
        frequency: List = []

        # Create list from histogram
        for h in list(rgb_color_histogram):
            h_count, h_rgb = h
            rc, gc, bc = h_rgb
            add: List = [rc, gc, bc, h_count]
            frequency.append(add)

        # Only colour points with enough presence
        frequency = list(
            filter(lambda e: e[3] > _CLUSTER_THRESHOLD, frequency)
        )
        # Sort the pixels on frequency. This way we can cut the while loop short
        # Order of proccesing the clusters may change the result
        # The paper does not contain any recommendations, the order is fixed as follows:
        frequency = sorted(frequency, key=lambda e: (e[3], e[2], e[1], e[0]))

        # Create first cluster
        center_of_clusters: List = []
        add = [
            frequency[0][0],
            frequency[0][1],
            frequency[0][2],
            frequency[0][3],
            1,
        ]
        center_of_clusters.append(add)

        # Find for all colour points a cluster
        for k in range(len(frequency) - 1, -1, -1):
            belong1cluster: bool = False

            # For every colour point calculate distance to all clusters
            for center in range(len(center_of_clusters)):
                point_freq: np.ndarray = np.array(
                    [frequency[k][0], frequency[k][1], frequency[k][2]]
                )
                point_center: np.ndarray = np.array(
                    [
                        center_of_clusters[center][0],
                        center_of_clusters[center][1],
                        center_of_clusters[center][2],
                    ]
                )

                # If a cluster is close enough, add this colour and recalculate the cluster Now the colour goes to
                # the first cluster fullfilling this. There is no indication in the paper that it should be the first
                # cluster meeting the requirement or the closest cluster.
                distance: float = float(
                    np.linalg.norm(point_freq - point_center)
                )
                if distance <= cls._DISTANCE_THRESHOLD:
                    new_count: int = int(
                        center_of_clusters[center][3] + frequency[k][3]
                    )
                    new_center: List[int] = [
                        int(
                            (
                                point_freq[0] * frequency[k][3]
                                + point_center[0]
                                * center_of_clusters[center][3]
                            )
                            / new_count
                        ),
                        int(
                            (
                                point_freq[1] * frequency[k][3]
                                + point_center[1]
                                * center_of_clusters[center][3]
                            )
                            / new_count
                        ),
                        int(
                            (
                                point_freq[2] * frequency[k][3]
                                + point_center[2]
                                * center_of_clusters[center][3]
                            )
                            / new_count
                        ),
                    ]

                    center_of_clusters[center][0] = new_center[0]
                    center_of_clusters[center][1] = new_center[1]
                    center_of_clusters[center][2] = new_center[2]
                    center_of_clusters[center][3] = new_count
                    center_of_clusters[center][4] += 1
                    belong1cluster = True
                    break

            # Create new cluster if the colour point is not close enough to other clusters
            if not belong1cluster:
                add = [
                    frequency[k][0],
                    frequency[k][1],
                    frequency[k][2],
                    frequency[k][3],
                    1,
                ]
                center_of_clusters.append(add)

        # Only keep clusters with more than 5 colour entries
        new_center_of_clusters: List = []
        for x in range(len(center_of_clusters)):
            if center_of_clusters[x][4] > _CLUSTER_THRESHOLD:
                new_center_of_clusters.append(center_of_clusters[x])

        return new_center_of_clusters

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
            - Number of dynamic color clusters (int, [0, +inf))
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (should be RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get dynamic clusters of the input image
        center_of_clusters = cls._get_dynamic_clusters(
            img_rgb, GUI_TYPE_DESKTOP
        )

        # Number of dynamic clusters
        count_dynamic_cluster: int = int(len(center_of_clusters))

        return [count_dynamic_cluster]
