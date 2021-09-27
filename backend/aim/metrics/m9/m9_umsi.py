#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    UMSI (Unified Model of Saliency and Importance)


Description:
    Todo


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    Todo


Change log:
    v1.0 (2021-09-27)
      * Initial implementation
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import List, Optional, Union

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Chuhan Jiao, Markku Laine"
__date__ = "2021-09-27"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: UMSI (Unified Model of Saliency and Importance).
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
            - UMSI, image (PNG) encoded in Base64
        """
        umsi_image = gui_image

        return [umsi_image]
