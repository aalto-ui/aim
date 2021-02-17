#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    PNG file size


Description:
    The file size (in bytes) of an image, saved in the PNG format
    (24-bit per pixel).

    Category: Visual complexity > Information amount > Color variability >
    Color range. For details, see CV1 [1], A4 [2], and C5 [3].


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
    v2.0 (2021-02-11)
      * Revised implementation

    v1.0 (2017-05-29)
      * Initial implementation
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import List, Optional, Union

# First-party modules
from aim.core.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine, Thomas Langerak, Yuxi Zhu"
__date__ = "2021-02-11"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: PNG file size.
    """

    # Public methods
    @staticmethod
    def execute_metric(
        gui_image: str, gui_type: int = GUI_TYPE_DESKTOP
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1

        Returns:
            Results (list of measures)
            - PNG file size in bytes (int, [0, +inf))
        """
        # Calculate PNG file size in bytes according to:
        # https://blog.aaronlenoir.com/2017/11/10/get-original-length-from-base-64-string/
        png_file_size_in_bytes: int = int(
            (3 * (len(gui_image) / 4)) - (gui_image.count("=", -2))
        )

        return [
            png_file_size_in_bytes,
        ]
