#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Contour congestion


Description:
    The mental effort needed to differentiate spatially proximal lines.

    Category: Visual complexity > Information discriminability.
    For details, see 'Contour congestion' [1, 2, 3].


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

    4.  van den Berg, R., Cornelissen, F.W., and Roerdink, J.B.T.M. (2009).
        A Crowding Model of Visual Clutter. Journal of Vision, 9(4):24, 1-11.
        doi: https://doi.org/10.1167/9.4.24

    5.  Levi, D.M. (2008). Crowding—An Essential Bottleneck for Object
        Recognition: A Mini-Review. Vision Research, 48(5), 635-654.
        doi: https://doi.org/10.1016/j.visres.2007.12.009

    6.  Wong, N., carpendale, S., and Greenberg, S. (2003). EdgeLens: An
        Interactive Method for Managing Edge Congestion in Graphs. In
        Proceedings of IEEE Symposium on Information Visualization
        (INFOVIS '03), pp. 51-58. IEEE.
        doi: https://doi.org/10.1109/INFVIS.2003.1249008


Change log:
    v2.0 (2021-02-10)
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
from typing import Any, Dict, List, Optional, Tuple

# Third-party modules
import numpy as np
from PIL import Image

# First-party modules
from aim.core.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine, Thomas Langerak"
__date__ = "2021-02-10"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Contour congestion.
    """

    # Private constants
    _Y_START: int = 0
    _Y_STOP: int = 1
    _X_START: int = 2
    _X_STOP: int = 3
    _RGB_DIFFERENCE_THRESHOLD: int = 50
    _CONGESTION_CLOSE_PROXIMITY_THRESHOLD: int = 20

    # Private methods
    @classmethod
    def _is_contour_pixel(
        cls,
        img_rgb_nparray: np.ndarray,
        img_contours_nparray: np.ndarray,
        img_height: int,
        img_width: int,
        pixel_y: int,
        pixel_x: int,
    ) -> bool:
        """
        Test whether pixel is contour.

        Args:
            img_rgb_nparray: Image RGB data
            img_contours_nparray: Image contours data
            img_height: Image height
            img_width: Image width
            pixel_y: Pixel y
            pixel_x: Pixel x

        Returns:
            True, if pixel is contour; otherwise False.
        """
        # Get pixel color channels
        pixel_r: int = int(img_rgb_nparray[pixel_y][pixel_x][0])
        pixel_g: int = int(img_rgb_nparray[pixel_y][pixel_x][1])
        pixel_b: int = int(img_rgb_nparray[pixel_y][pixel_x][2])

        # Get adjacent pixels (indexes)
        adjacent_pixels: List[Tuple[int, int]] = [
            (pixel_y - 1, pixel_x),  # north
            # (pixel_y - 1, pixel_x + 1),  # northeast
            (pixel_y, pixel_x + 1),  # east
            # (pixel_y + 1, pixel_x + 1),  # southeast
            (pixel_y + 1, pixel_x),  # south
            # (pixel_y + 1, pixel_x - 1),  # southwest
            (pixel_y, pixel_x - 1),  # west
            # (pixel_y - 1, pixel_x - 1),  # northwest
        ]

        # Iterate over adjacent pixels
        contour: bool = False
        for n in range(len(adjacent_pixels)):
            # Get adjacent pixel
            adjacent_pixel_y: int = adjacent_pixels[n][0]
            adjacent_pixel_x: int = adjacent_pixels[n][1]

            # Process only those adjacent pixels that are within image
            # dimensions
            if (
                0 <= adjacent_pixel_y < img_height
                and 0 <= adjacent_pixel_x < img_width
            ):
                # Get adjacent pixel color channels
                adjacent_pixel_r: int = int(
                    img_rgb_nparray[adjacent_pixel_y][adjacent_pixel_x][0]
                )
                adjacent_pixel_g: int = int(
                    img_rgb_nparray[adjacent_pixel_y][adjacent_pixel_x][1]
                )
                adjacent_pixel_b: int = int(
                    img_rgb_nparray[adjacent_pixel_y][adjacent_pixel_x][2]
                )

                # Compute difference per color channel
                difference_r: int = abs(adjacent_pixel_r - pixel_r)
                difference_g: int = abs(adjacent_pixel_g - pixel_g)
                difference_b: int = abs(adjacent_pixel_b - pixel_b)

                # Test differences (inclusive disjunction)
                if (
                    difference_r > cls._RGB_DIFFERENCE_THRESHOLD
                    or difference_g > cls._RGB_DIFFERENCE_THRESHOLD
                    or difference_b > cls._RGB_DIFFERENCE_THRESHOLD
                ) and img_contours_nparray[adjacent_pixel_y][
                    adjacent_pixel_x
                ] == 0:
                    contour = True
                    break

        return contour

    @classmethod
    def _detect_contours(
        cls, img_rgb_nparray: np.ndarray, img_height: int, img_width: int
    ) -> np.ndarray:
        """
        Detect contours in RGB image data.

        Args:
            img_rgb_nparray: Image RGB data
            img_height: Image height
            img_width: Image width

        Returns:
            Image contours data
        """
        # Create empty image data for contour pixels to be added
        img_contours_nparray: np.ndarray = np.zeros(
            (img_height, img_width), dtype=int
        )

        # Iterate over image width pixels (X-axis)
        for pixel_x in range(img_width):
            # Iterate over image height pixels (Y-axis)
            for pixel_y in range(img_height):
                if cls._is_contour_pixel(
                    img_rgb_nparray,
                    img_contours_nparray,
                    img_height,
                    img_width,
                    pixel_y,
                    pixel_x,
                ):
                    img_contours_nparray[pixel_y][pixel_x] = 255

        return img_contours_nparray

    @classmethod
    def _is_congested_contour_pixel(
        cls,
        img_contours_nparray: np.ndarray,
        img_height: int,
        img_width: int,
        pixel_y: int,
        pixel_x: int,
    ) -> bool:
        """
        Test whether contour pixel is congested.

        Args:
            img_contours_nparray: Image contours data
            img_height: Image height
            img_width: Image width
            pixel_y: Contour pixel y
            pixel_x: Contour pixel x

        Returns:
            True, if contour pixel is congested; otherwise False.
        """
        # Initialize close proximity contour pixel tests
        close_proximity_contour_pixel_tests: Dict[str, bool] = {
            "north": False,
            "east": False,
            "south": False,
            "west": False,
        }

        # Get close proximity pixels (indexes)
        # North
        close_pixels_north: Tuple[int, int, int, int] = (
            pixel_y - cls._CONGESTION_CLOSE_PROXIMITY_THRESHOLD,
            pixel_y,
            pixel_x,
            pixel_x + 1,
        )
        # East
        close_pixels_east: Tuple[int, int, int, int] = (
            pixel_y,
            pixel_y + 1,
            pixel_x + 1,
            pixel_x + 1 + cls._CONGESTION_CLOSE_PROXIMITY_THRESHOLD,
        )
        # South
        close_pixels_south: Tuple[int, int, int, int] = (
            pixel_y + 1,
            pixel_y + 1 + cls._CONGESTION_CLOSE_PROXIMITY_THRESHOLD,
            pixel_x,
            pixel_x + 1,
        )
        # West
        close_pixels_west: Tuple[int, int, int, int] = (
            pixel_y,
            pixel_y + 1,
            pixel_x - cls._CONGESTION_CLOSE_PROXIMITY_THRESHOLD,
            pixel_x,
        )

        # Test whether close proximity area is within image dimensions
        # Assumption: screen bezel consists of contour pixels
        if close_pixels_north[cls._Y_START] < 0:
            close_proximity_contour_pixel_tests["north"] = True
        else:
            n_close_pixels_north: int = np.count_nonzero(
                img_contours_nparray[
                    close_pixels_north[cls._Y_START] : close_pixels_north[
                        cls._Y_STOP
                    ],
                    close_pixels_north[cls._X_START] : close_pixels_north[
                        cls._X_STOP
                    ],
                ]
            )
            if n_close_pixels_north > 0:
                close_proximity_contour_pixel_tests["north"] = True

        # Test whether close proximity area is within image dimensions
        # Assumption: screen bezel consists of contour pixels
        if img_width < close_pixels_east[cls._X_STOP]:
            close_proximity_contour_pixel_tests["east"] = True
        else:
            n_close_pixels_east: int = np.count_nonzero(
                img_contours_nparray[
                    close_pixels_east[cls._Y_START] : close_pixels_east[
                        cls._Y_STOP
                    ],
                    close_pixels_east[cls._X_START] : close_pixels_east[
                        cls._X_STOP
                    ],
                ]
            )
            if n_close_pixels_east > 0:
                close_proximity_contour_pixel_tests["east"] = True

        # Test whether close proximity area is within image dimensions
        # Assumption: screen bezel consists of contour pixels
        if img_height < close_pixels_south[cls._Y_STOP]:
            close_proximity_contour_pixel_tests["south"] = True
        else:
            n_close_pixels_south: int = np.count_nonzero(
                img_contours_nparray[
                    close_pixels_south[cls._Y_START] : close_pixels_south[
                        cls._Y_STOP
                    ],
                    close_pixels_south[cls._X_START] : close_pixels_south[
                        cls._X_STOP
                    ],
                ]
            )
            if n_close_pixels_south > 0:
                close_proximity_contour_pixel_tests["south"] = True

        # Test whether close proximity area is within image dimensions
        # Assumption: screen bezel consists of contour pixels
        if close_pixels_west[cls._X_START] < 0:
            close_proximity_contour_pixel_tests["west"] = True
        else:
            n_close_pixels_west: int = np.count_nonzero(
                img_contours_nparray[
                    close_pixels_west[cls._Y_START] : close_pixels_west[
                        cls._Y_STOP
                    ],
                    close_pixels_west[cls._X_START] : close_pixels_west[
                        cls._X_STOP
                    ],
                ]
            )
            if n_close_pixels_west > 0:
                close_proximity_contour_pixel_tests["west"] = True

        # Contour pixel is considered congested if there are close proximity
        # contour pixels in every principal compass point
        congested_contour: bool = False
        if all(close_proximity_contour_pixel_tests.values()):
            congested_contour = True

        return congested_contour

    @classmethod
    def _detect_congested_contours(
        cls, img_contours_nparray: np.ndarray, img_height: int, img_width: int
    ) -> np.ndarray:
        """
        Detect congested contours in image contours data.

        Args:
            img_contours_nparray: Image contours data
            img_height: Image height
            img_width: Image width

        Returns:
            Image congested contours data
        """
        # Create empty image data for congested contour pixels to be added
        img_congested_contours_nparray: np.ndarray = np.zeros(
            (img_height, img_width), dtype=int
        )

        # Extract contour pixels
        contour_pixels: np.ndarray = np.argwhere(img_contours_nparray != 0)

        # Iterate over contour pixels
        for contour_pixel in contour_pixels:
            contour_pixel_y = contour_pixel[0]
            contour_pixel_x = contour_pixel[1]

            if cls._is_congested_contour_pixel(
                img_contours_nparray,
                img_height,
                img_width,
                contour_pixel_y,
                contour_pixel_x,
            ):
                img_congested_contours_nparray[contour_pixel_y][
                    contour_pixel_x
                ] = 255

        return img_congested_contours_nparray

    @staticmethod
    def _compute_contour_congestion(
        img_contours_nparray: np.ndarray,
        img_congested_contours_nparray: np.ndarray,
    ) -> float:
        """
        Compute contour congestion.

        Args:
            img_contours_nparray: Image contours data
            img_congested_contours_nparray: Image congested contours data

        Returns:
            Contour congestion
        """
        # Compute contour congestion
        try:
            n_contour_pixels: int = np.count_nonzero(img_contours_nparray)
            n_congested_contour_pixels: int = np.count_nonzero(
                img_congested_contours_nparray
            )
            contour_congestion: float = (
                n_congested_contour_pixels / n_contour_pixels
            )
        except ZeroDivisionError:
            contour_congestion = 0.0

        return contour_congestion

    # Public methods
    @classmethod
    def execute_metric(
        cls, gui_image: str, gui_type: int = GUI_TYPE_DESKTOP
    ) -> Optional[List[Any]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1

        Returns:
            Results (list of measures)
            - Contour congestion (float, [0, 1])
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get NumPy array
        img_rgb_nparray: np.ndarray = np.array(img_rgb)

        # Get image dimensions
        img_shape: Tuple[int, ...] = img_rgb_nparray.shape
        img_height: int = img_shape[0]
        img_width: int = img_shape[1]

        # Detect contours
        img_contours_nparray: np.ndarray = cls._detect_contours(
            img_rgb_nparray, img_height, img_width
        )

        # Detect congested contours
        img_congested_contours_nparray: np.ndarray = (
            cls._detect_congested_contours(
                img_contours_nparray, img_height, img_width
            )
        )

        # Compute contour congestion
        contour_congestion: float = cls._compute_contour_congestion(
            img_contours_nparray, img_congested_contours_nparray
        )

        return [
            contour_congestion,
        ]
