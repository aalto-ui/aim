#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pytest fixtures.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import pathlib

# Third-party modules
import pytest

# First-party modules
from tests.core.constants import DATA_TEMP_DIR

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2020-08-11"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------------


@pytest.fixture(
    scope="class"
)  # for scope options, see https://docs.pytest.org/en/latest/fixture.html
def clean_up():
    """
    A class-scoped clean up.
    """
    # Setup

    yield  # execute metric

    # Teardown
    # Delete created GUI images (JPEG)
    for matched_path in pathlib.Path(DATA_TEMP_DIR).glob("*.jpg"):
        matched_path.unlink()  # delete file
