#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Dynamic Clusters


Description:
    The number of dynamic clusters and the number of colours per dynamic cluster.

    Category: Colour Perception.

    In the paper by Miniukovich and De Angeli suggest (among others) two factors for an indication for colourfulness
    The number of dynamic clusters and the number of colours per dynamic cluster.

    "The number of dynamic clusters of colors after color reduction (more than 5 pixels). If a difference between
    two colors in a color cube is less than or equal to 3, two colors are united in the same cluster, which continues
    recursively for all colors. Only clusters containing more than 5 values are counted."

    The number of clusters has not proven statistically relevant. The number of colours per clusters is.
    Both are returned with this function.


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
    v2.0 (2021-05-25)
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
    Metric: Dunamic Clusters.
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
            - Number of Clusters (int),
            - Average number of colours per Cluster (int)
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
        frequency: List = []

        # Create list from histogram
        for h in list(rgb_color_histogram):
            h_count, h_value = h
            rc, gc, bc = h_value
            add = [rc, gc, bc, h_count]
            frequency.append(add)

        # Sort the pixels on frequency. This way we can cut the while loop short
        frequency = sorted(frequency, key=lambda hist_element: hist_element[3])

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

        for k in range(len(frequency) - 1, -1, -1):
            # Only colour points with enough presence
            if frequency[k][3] < 6:
                break
            else:
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
                    distance: float = np.linalg.norm(point_freq - point_center)

                    # If a cluster is close enough, add this colour and recalculate the cluster
                    # Now the colour goes to the first cluster fullfilling this. Maybe it should be also the closest?
                    if distance <= 3:
                        new_count: int = (
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
            if center_of_clusters[x][4] > 5:
                new_center_of_clusters.append(center_of_clusters[x])

        # Number of clusters, not statistically relevant
        count_dynamic_cluster: int = len(new_center_of_clusters)

        # Average number of colours per cluster
        average_colour_dynamic_cluster: int = 0
        for x in range(len(new_center_of_clusters)):
            average_colour_dynamic_cluster += new_center_of_clusters[x][4]

        if count_dynamic_cluster != 0:
            average_colour_dynamic_cluster = int(
                average_colour_dynamic_cluster / count_dynamic_cluster
            )
        else:
            average_colour_dynamic_cluster = 0

        return [count_dynamic_cluster, average_colour_dynamic_cluster]
