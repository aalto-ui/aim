#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AIM metric interfaces.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import abc
from typing import Any, List, Optional, Union

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-03-19"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Interfaces
# ----------------------------------------------------------------------------


class AIMMetricInterface(metaclass=abc.ABCMeta):
    # Dunder methods
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "execute_metric")
            and callable(subclass.execute_metric)
            or NotImplemented
        )

    # Abstract methods
    @abc.abstractmethod
    def execute_metric(
        self, gui_image: str, gui_type: int = GUI_TYPE_DESKTOP
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1

        Returns:
            Results (list of measures)

        Raises:
            NotImplementedError: Implementation is missing
        """
        raise NotImplementedError
