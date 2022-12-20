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
from typing import Any, Dict, List, Optional, Union

# Third-party modules
from pydantic import HttpUrl

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2022-12-20"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.2"


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
        self,
        gui_image: str,
        gui_type: int = GUI_TYPE_DESKTOP,
        gui_segments: Optional[Dict[str, Any]] = None,
        gui_url: Optional[HttpUrl] = None,
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1
            gui_segments: GUI segments (defaults to None)
            gui_url: GUI URL (defaults to None)

        Returns:
            Results (list of measures)

        Raises:
            NotImplementedError: Implementation is missing
        """
        raise NotImplementedError
