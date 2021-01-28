#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    JPEG file size


Description:
    The file size (in bytes) of an image, saved in the JPEG format
    (image quality 70).

    Category: Visual complexity > Information amount > Visual clutter.
    For details, see CL4 [1], A12 [2], and CL4 [3].


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

    4.  Tuch, A.N., Bargas-Avila, J.A., Opwis, K., and Wilhelm, F.H. (2009).
        Visual Complexity of Websites: Effects on Users' Experience,
        Physiology, Performance, and Memory. International Journal of
        Human-Computer Studies, 67(9), 703-715.
        doi: https://doi.org/10.1016/j.ijhcs.2009.04.002

    5.  Rosenholtz, R., Li, Y., and Nakano, L. (2007). Measuring Visual
        Clutter. Journal of Vision, 7(2), 1-22.
        doi: https://doi.org/10.1167/7.2.17


Change log:
    v2.0 (2021-01-27)
      * Revised implementation

    v1.0 (2017-05-29)
      * Initial implementation
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import Any, List, Optional

# First-party modules
import aim.core.utils as aim_utils
from aim.core.constants import GUI_TYPE_DESKTOP, IMAGE_QUALITY_JPEG
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine, Thomas Langerak"
__date__ = "2021-01-27"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: JPEG file size.
    """

    # Public methods
    @staticmethod
    def execute_metric(
        gui_image: str, gui_type: int = GUI_TYPE_DESKTOP
    ) -> Optional[List[Any]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1

        Returns:
            Results (list of measures)
            - JPEG file size in bytes (int, [0, +inf))
        """
        # Convert GUI image from PNG to JPEG, encoded in Base64
        jpeg_gui_image: str = aim_utils.convert_image(
            gui_image, jpeg_image_quality=IMAGE_QUALITY_JPEG
        )

        # Calculate JPEG file size in bytes according to:
        # https://blog.aaronlenoir.com/2017/11/10/get-original-length-from-base-64-string/
        jpeg_file_size_in_bytes: int = int(
            (3 * (len(jpeg_gui_image) / 4)) - (jpeg_gui_image.count("=", -2))
        )

        return [
            jpeg_file_size_in_bytes,
        ]
