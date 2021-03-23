#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Models.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import pathlib
from enum import Enum
from typing import Dict, Optional, Union

# Third-party modules
from pydantic import BaseModel, Extra, Field, HttpUrl, validator

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-03-23"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"

# ----------------------------------------------------------------------------
# Enumerations
# ----------------------------------------------------------------------------


class MessageType(str, Enum):
    execute = "execute"


# ----------------------------------------------------------------------------
# Models
# ----------------------------------------------------------------------------

# Shared configurations
class MessageConfigBase(BaseModel):
    """
    The MessageConfigBase model.
    """

    class Config:  # see https://pydantic-docs.helpmanual.io/usage/model_config/
        anystr_strip_whitespace = (
            True  # strip leading and trailing whitespace for str
        )
        extra = (
            Extra.forbid
        )  # forbid extra attributes during model initialization
        validate_all = True  # validate model field defaults
        validate_assignment = (
            True  # perform validation on assignment to attributes
        )


class MessageBase(MessageConfigBase):
    """
    The MessageBase model.
    """

    type: MessageType = Field(
        ...,
        description="The type of this message.",
        example=MessageType.execute,
    )
    url: Union[str, HttpUrl] = Field(
        ..., description="The URL of this message.", example="https://aalto.fi"
    )
    data: Optional[str] = Field(
        ...,
        description="The data (PNG image encoded in Base64) of this message.",
    )
    filename: Optional[pathlib.Path] = Field(
        ...,
        description="The filename (PNG image) of this message.",
        example="aalto.fi.png",
    )
    metrics: Dict[str, bool] = Field(
        ...,
        description="The metrics of this message.",
        example={"m1": True, "m5": True},
    )

    @validator("metrics")
    def process_metrics(cls, v: Dict[str, bool]):
        metrics_filtered: Dict[str, bool] = {
            k: v for k, v in v.items() if v is True
        }  # filter
        return metrics_filtered


class MessageURL(MessageBase):
    """
    The MessageURL model.
    """

    url: HttpUrl = Field(
        ..., description="The URL of this message.", example="https://aalto.fi"
    )
    data: Optional[str] = None
    filename: Optional[pathlib.Path] = None

    @validator("data")
    def data_must_be_none(cls, v: Optional[str]):
        if v is not None:
            raise ValueError("Data must be None")
        return v

    @validator("filename")
    def filename_must_be_none(cls, v: Optional[str]):
        if v is not None:
            raise ValueError("Filename must be None")
        return v


class MessageImage(MessageBase):
    """
    The MessageImage model.
    """

    url: str = Field(
        ...,
        description="The URL of this message.",
        example="https://aalto.fi",
        min_length=0,
        max_length=0,
    )
    data: str = Field(
        ...,
        description="The data (PNG image encoded in Base64) of this message.",
    )
    filename: pathlib.Path = Field(
        ...,
        description="The filename (PNG image) of this message.",
        example="aalto.fi.png",
    )
    raw_data: str = Field(
        "",
        description="The raw data (PNG image encoded in Base64) of this message.",
    )

    def __init__(self, **data):
        super().__init__(**data)
        self.raw_data = self.data.split(",")[1]

    @validator("data")
    def data_must_be_image_png_base64(cls, v: str):
        data_format: str = v.split(",")[0][5:]  # remove scheme 'data:'
        if data_format != "image/png;base64":
            raise ValueError("Data format must be 'image/png;base64'")
        return v

    @validator("filename")
    def file_extension_must_be_png(cls, v: pathlib.Path):
        if v.suffix != ".png":
            raise ValueError("File extension must be '.png'")
        return v
