#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Quadtree decomposition


Description:
    Quadtree decomposition for 3 aesthetic dimensions including balance, symmetry,
    and equilibrium. Number of quadtree decomposition leaves is an indicator of visual complexity.

    Balance: the distribution of optical weight in a picture.
    Optical weight refers to the perception that some objects appear heavier than
    others. Larger objects are heavier, whereas small objects are lighter. Balance in
    screen design is achieved by providing an equal weight of screen elements, left
    and right, top and bottom.

    Symmetry: a unit on one side of the centre line is exactly
    replicated on the other side. Vertical symmetry refers to the balanced arrangement
    of equivalent elements about a vertical axis, and horizontal symmetry
    about a horizontal axis. Radial symmetry consists of equivalent elements
    balanced about two or more axes that intersect at a central point. In two seperate studies
    this metric has not proven to be significant.

    Equilibrium: a stabilisation, a midway centre of suspension. Equilibrium
    on a screen is accomplished through centring the layout itself. The centre of the
    layout coincides with that of the frame.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Ngo, D., Teo, L. and Byrne, J. (2003). Modelling interface aesthetics.
        Information Sciences 152, pp. 25-46.
        doi: https://doi.org/10.1016/S0020-0255(02)00404-8

    2.  Zheng, X., Chakraborty, I., Lin, J. and Rauschenberger, R. (2009)
        Correlating Low-Level Image Statistics with Users' Rapid Aesthetic and
        Affective Judgments of Web Pages. In Proceedings of the SIGCHI
        Conference on Human Factors in Computing Systems (CHI'09 ~ Understanding
        Information), pp. 1-10. ACM.
        doi: https://doi.org/10.1145/1518701.1518703

    3.  Reinecke, K., Yeh, T., Miratrix, L., Mardiko, R., Zhao, Y., Liu, J., and
        Gajos, K. Z. (2013) Predicting Users' First Impressions of Website Aesthetics
        With a Quantification of Perceived Visual Complexity and Colorfulness. In
        Proceedings of the SIGCHI Conference on Human Factors in Computing Systems
        (CHI'13), pp. 2049-2058, ACM.
        doi: https://doi.org/10.1145/2470654.2481281


Change log:
    v2.0 (2023-01-01)
      * Revised implementation

    v1.0.1 (2017-05-29)
      * Initial implementation
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
import math
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple, Union

# Third-party modules
import cv2
import matplotlib.figure
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pydantic import HttpUrl
from skimage import color

# First-party modules
from aim.common import image_utils
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = (
    "Amir Hossein Kargaran, Nafiseh Nikehgbal, Markku Laine, Thomas Langerak"
)
__date__ = "2023-01-01"
__email__ = "markku.laine@aalto.fi"
__version__ = "2.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Quadtree decomposition.
    """

    # Private constants
    _SHOW: bool = False  # show plot results of quadtree decomposition

    # _quadtree_color constants. thresolds are partially based on the paper, however it seems to be working different.
    _COLOR_THRESH: int = (
        55  # color entropy threshold. quite heavily website dependent
    )
    _INTENSITY_THRESH: int = (
        70  # intensity entropy threshold. based on nothing
    )
    _L_BINS: int = 20  # luminince bins
    _H_BINS: int = 30  # hue bins
    _S_BINS: int = 32  # saturation bins
    _MIN_NUM_DIVISION: int = (
        2  # minumm number of quadtree decomposition devision
    )
    _MIN_BLOCK_SIZE_H: int = 8  # minimum height of block
    _MIN_BLOCK_SIZE_W: int = 8  # minimum width of block

    # _quadtree_gray constants.
    _MIN_STD: int = (
        20  # minimum STD threshold of each block for subsequent splitting
    )
    _MIN_BLOCK_SIZE_GRAY: int = 25  # minimum size threshold of each block for subsequent splitting in pixel

    # Lists to save quadtree leaves
    _RES_LEAF_GRAY: List[Tuple[int, int, int, int]] = []
    _RES_LEAF_COLOR: List[Tuple[int, int, int, int]] = []

    # Private methods
    @staticmethod
    def _balance(
        leaves: List[Tuple[int, int, int, int]], width: int, height: int
    ) -> float:
        """ """
        top: List[Tuple[int, int, int, int]] = []
        right: List[Tuple[int, int, int, int]] = []
        left: List[Tuple[int, int, int, int]] = []
        bottom: List[Tuple[int, int, int, int]] = []
        center: List[int] = [int(width / 2), int(height / 2)]

        for leaf in leaves:
            if leaf[0] > center[0]:
                right.append(leaf)
            else:
                left.append(leaf)

            if leaf[1] > center[1]:
                bottom.append(leaf)
            else:
                top.append(leaf)

        w_left: float = 0.0
        w_top: float = 0.0
        w_bottom: float = 0.0
        w_right: float = 0.0

        for leaf in top:
            area: int = leaf[2] * leaf[3]
            mid_point_leaf: List[int] = [
                int(leaf[0] + leaf[2] / 2),
                int(leaf[1] + leaf[3] / 2),
            ]
            distance: int = abs(mid_point_leaf[0] - center[1])
            score: int = distance * area
            w_top += score

        for leaf in bottom:
            area = leaf[2] * leaf[3]
            mid_point_leaf = [
                int(leaf[0] + leaf[2] / 2),
                int(leaf[1] + leaf[3] / 2),
            ]
            distance = abs(mid_point_leaf[0] - center[1])
            score = distance * area
            w_bottom += score

        for leaf in left:
            area = leaf[2] * leaf[3]
            mid_point_leaf = [
                int(leaf[0] + leaf[2] / 2),
                int(leaf[1] + leaf[3] / 2),
            ]
            distance = abs(mid_point_leaf[1] - center[0])
            score = distance * area
            w_left += score

        for leaf in right:
            area = leaf[2] * leaf[3]
            mid_point_leaf = [
                int(leaf[0] + leaf[2] / 2),
                int(leaf[1] + leaf[3] / 2),
            ]
            distance = abs(mid_point_leaf[1] - center[0])
            score = distance * area
            w_right += score

        IB_left_right: float = (w_left - w_right) / max(
            abs(w_left), abs(w_right)
        )
        IB_top_bottom: float = (w_top - w_bottom) / max(
            abs(w_top), abs(w_bottom)
        )
        BM: float = 1 - float(abs(IB_top_bottom) + abs(IB_left_right)) / 2

        return BM

    @staticmethod
    def _symmetry(
        leaves: List[Tuple[int, int, int, int]], width: int, height: int
    ) -> float:
        """ """
        UL_leaves: List[Tuple[int, int, int, int]] = []
        UR_leaves: List[Tuple[int, int, int, int]] = []
        LL_leaves: List[Tuple[int, int, int, int]] = []
        LR_leaves: List[Tuple[int, int, int, int]] = []

        x_center: int = int(width / 2)
        y_center: int = int(height / 2)

        for leaf in leaves:
            if leaf[0] > x_center and leaf[1] < y_center:
                UR_leaves.append(leaf)
            elif leaf[0] <= x_center and leaf[1] < y_center:
                UL_leaves.append(leaf)
            elif leaf[0] > x_center and leaf[1] >= y_center:
                LR_leaves.append(leaf)
            elif leaf[0] <= x_center and leaf[1] >= y_center:
                LL_leaves.append(leaf)

        X_j: List[float] = []
        Y_j: List[float] = []
        H_j: List[float] = []
        B_j: List[float] = []
        T_j: List[float] = []
        R_j: List[float] = []

        # With j being respectively: UL;UR,LL;LR
        for j in [UL_leaves, UR_leaves, LL_leaves, LR_leaves]:
            X_score: float = 0.0
            Y_score: float = 0.0
            H_score: float = 0.0
            B_score: float = 0.0
            T_score: float = 0.0
            R_score: float = 0.0
            for leaf in j:
                x_leaf: int = leaf[0] + int(leaf[2] / 2)
                X_score += int(abs(x_leaf - x_center))
                y_leaf: int = leaf[1] + int(leaf[3] / 2)
                Y_score += int(abs(y_leaf - y_center))
                H_score += int(leaf[3])
                B_score += int(leaf[2])
                T_score += int(abs(y_leaf - y_center) / abs(x_leaf - x_center))
                R_score += float(
                    (((x_leaf - x_center) ** 2) + ((y_leaf - y_center) ** 2))
                    ** 0.5
                )

            X_j.append(X_score)
            Y_j.append(Y_score)
            H_j.append(H_score)
            B_j.append(B_score)
            T_j.append(T_score)
            R_j.append(R_score)

        # Normalize
        X_j = [x / max(X_j) for x in X_j]
        Y_j = [y / max(Y_j) for y in Y_j]
        H_j = [h / max(H_j) for h in H_j]
        B_j = [b / max(B_j) for b in B_j]
        T_j = [t / max(T_j) for t in T_j]
        R_j = [r / max(R_j) for r in R_j]

        SYM_ver: float = (
            abs(X_j[0] - X_j[1])
            + abs(X_j[2] - X_j[3])
            + abs(Y_j[0] - Y_j[1])
            + abs(Y_j[2] - Y_j[3])
            + abs(H_j[0] - H_j[1])
            + abs(H_j[2] - H_j[3])
            + abs(B_j[0] - B_j[1])
            + abs(B_j[2] - B_j[3])
            + abs(T_j[0] - T_j[1])
            + abs(T_j[2] - T_j[3])
            + abs(R_j[0] - R_j[1])
            + abs(R_j[2] - R_j[3])
        ) / 12

        SYM_hor: float = (
            abs(X_j[0] - X_j[2])
            + abs(X_j[1] - X_j[3])
            + abs(Y_j[0] - Y_j[2])
            + abs(Y_j[1] - Y_j[3])
            + abs(H_j[0] - H_j[2])
            + abs(H_j[1] - H_j[3])
            + abs(B_j[0] - B_j[2])
            + abs(B_j[1] - B_j[3])
            + abs(T_j[0] - T_j[2])
            + abs(T_j[1] - T_j[3])
            + abs(R_j[0] - R_j[2])
            + abs(R_j[1] - R_j[3])
        ) / 12

        SYM_rot: float = (
            abs(X_j[0] - X_j[3])
            + abs(X_j[1] - X_j[2])
            + abs(Y_j[0] - Y_j[3])
            + abs(Y_j[1] - Y_j[2])
            + abs(H_j[0] - H_j[3])
            + abs(H_j[1] - H_j[2])
            + abs(B_j[0] - B_j[3])
            + abs(B_j[1] - B_j[2])
            + abs(T_j[0] - T_j[3])
            + abs(T_j[1] - T_j[2])
            + abs(R_j[0] - R_j[3])
            + abs(R_j[1] - R_j[2])
        ) / 12

        SYM: float = 1 - (abs(SYM_ver) + abs(SYM_hor) + abs(SYM_rot)) / 3

        return SYM

    @staticmethod
    def _equilibrium(
        leaves: List[Tuple[int, int, int, int]], width: int, height: int
    ) -> float:
        """
        This implementation seems unreasonably high. However, this is the case in the paper as well.
        """
        area: List[float] = []
        dx: List[float] = []
        dy: List[float] = []

        for leaf in leaves:
            area.append(float(leaf[2] * leaf[3]))
            dx.append(abs(float(leaf[0] + leaf[2] / 2 - width / 2)))
            dy.append(abs(float(leaf[1] + leaf[3] / 2 - height / 2)))

        sum_x: float = 0.0
        sum_y: float = 0.0

        for n in range(len(dx)):
            sum_x += area[n] * dx[n]
            sum_y += area[n] * dx[n]

        EM_x: float = (2 * sum_x) / (width * len(leaves) * np.sum(area))
        EM_y: float = (2 * sum_y) / (height * len(leaves) * np.sum(area))

        EM: float = 1 - float(abs(EM_x) + abs(EM_y)) / 2

        return EM

    @classmethod
    def _intensity_entropy(cls, inp: np.ndarray) -> float:
        """
        Currently RGB entropy is calculated and intensity.
        The papers also refer to textons. This is not implemented as of yet:
        Representing and Recognizing the Visual Appearance of Materials using Three-dimensional Textons
        THOMAS LEUNG AND JITENDRA MALIK, International Journal of Computer Vision 43(1), 29-44, 2001
        """
        inp_lab: np.ndarray = color.rgb2lab(inp)
        L_list: List[float] = list(inp_lab[:, :, 0].flatten())

        p: np.ndarray
        p, _ = np.histogram(
            L_list, bins=cls._L_BINS, range=(0, 100), density=True
        )
        p = p.ravel()
        p = p * 100.0
        p = p + 1e-12
        p_log: List[float] = [math.log(y) for y in p]
        p_result: np.ndarray = p * p_log
        result: float = np.sum(p_result)

        return result

    @classmethod
    def _color_entropy(cls, inp: np.ndarray) -> float:
        """ """
        inp = inp / 255.0
        inp_hsv: np.ndarray = color.rgb2hsv(inp)
        H_list: List[float] = list(inp_hsv[:, :, 0].flatten() * 360.0)
        S_list: List[float] = list(inp_hsv[:, :, 1].flatten() * 100.0)

        h: np.ndarray
        s: np.ndarray
        h, _ = np.histogram(
            H_list, bins=cls._H_BINS, range=(0, 360), density=True
        )
        s, _ = np.histogram(
            S_list, bins=cls._S_BINS, range=(0, 100), density=True
        )

        h = h.ravel()
        h = h * 100.0
        h = h + 1e-12
        h_log: List[float] = [math.log(y) for y in h]
        h_result: np.ndarray = h * h_log

        s = s.ravel()
        s = s * 100.0
        s = s + 1e-12
        s_log = [math.log(y) for y in s]
        s_result: np.ndarray = s * s_log
        result: float = abs(np.sum(h_result) + np.sum(s_result)) / 2

        return result

    @classmethod
    def _quadtree_color(cls, leaf, cor_size, i) -> None:
        """
        The uncertainty of colour in a leaf, given the leaf. Based on the shannon entropy
        """
        ent_color: float = cls._color_entropy(leaf)
        ent_int: float = cls._intensity_entropy(leaf)

        height: int = leaf.shape[0]
        width: int = leaf.shape[1]
        c_height: int = int(height / 2)
        c_width: int = int(width / 2)

        # If entropy fullfulls requirements
        # or the website has not been divided in enough leaves
        # and there is still room for division:
        if (
            (
                ent_color < cls._COLOR_THRESH
                or ent_int > cls._INTENSITY_THRESH
                or i < cls._MIN_NUM_DIVISION
            )
            and c_height > cls._MIN_BLOCK_SIZE_H
            and c_width > cls._MIN_BLOCK_SIZE_W
        ):
            i += 1
            # Divide the leaf in 4 new leaves
            new_leaf = [
                leaf[0:c_height, 0:c_width],
                leaf[c_height:height, 0:c_width],
                leaf[0:c_height, c_width:width],
                leaf[c_height:height, c_width:width],
            ]

            # Coordinates and size of each leaf
            new_cor_size = [
                (cor_size[0] + 0, cor_size[1] + 0, c_width, c_height),
                (cor_size[0] + 0, cor_size[1] + c_height, c_width, c_height),
                (cor_size[0] + c_width, cor_size[1] + 0, c_width, c_height),
                (
                    cor_size[0] + c_width,
                    cor_size[1] + c_height,
                    c_width,
                    c_height,
                ),
            ]
            for x in range(len(new_leaf)):
                # Run recursively
                cls._quadtree_color(new_leaf[x], new_cor_size[x], i)
        else:
            # If not, append the coordinates and size
            cls._RES_LEAF_COLOR.append(cor_size)
        return None

    @classmethod
    def _quadtree_gray(cls, leaf_gray, x, y) -> None:
        """
        Compute quadtree decomposition over gray image by evaluaing the std of image pixels.
        It decides whether to perform or not the split of leaf by compraing std of image with the min std threshold.

        Args:
            leaf_gray: gray img (np.ndarray)
            x: x offset of the leaves to analyze
            y: y offset of the leaves to analyze

        Return:
            None
        """
        h, w = leaf_gray.shape
        _, std_float = cv2.meanStdDev(leaf_gray)
        std: int = int(std_float)

        if std >= cls._MIN_STD and max(h, w) >= cls._MIN_BLOCK_SIZE_GRAY:
            if w >= h:
                # split along the X axis
                # decompose for both images
                w2 = int(w / 2)
                leaf_gray1 = leaf_gray[0:h, 0:w2]
                leaf_gray2 = leaf_gray[0:h, w2:]
                cls._quadtree_gray(leaf_gray1, x, y)
                cls._quadtree_gray(leaf_gray2, x + w2, y)
            else:
                # split along the Y axis
                # decompose for both images
                h2 = int(h / 2)
                leaf_gray1 = leaf_gray[0:h2, 0:]
                leaf_gray2 = leaf_gray[h2:, 0:]
                cls._quadtree_gray(leaf_gray1, x, y)
                cls._quadtree_gray(leaf_gray2, x, y + h2)
        else:
            cls._RES_LEAF_GRAY.append((x, y, w, h))
        return None

    @classmethod
    def plot(
        cls,
        org_img: np.ndarray,
        res_leaf: List[Tuple[int, int, int, int]],
        edgecolor: str = "red",
        facecolor: str = "none",
        linewidth: int = 1,
        inv_dpi: float = 1e-2,
    ) -> matplotlib.figure.Figure:
        """
        This function is used to generate a graphical representation of the QuadTree decomposition.

        Args:
            org_img: original image (np.ndarray)
            res_leaf: list of blcok leaves (List[Tuple[int, int, int, int]])
            edgecolor: color of the rectangles, default is red (str)
            facecolor: color used for rectangles fills. Default is "none" (str)
            linewidth: width in px of the rectangles' borders. Default is 1 (int)
            inv_dpi: scale of figure. Default is 0.01 (float)

        Return:
            plot image of the quadTree Decomposition (matplotlib.figure.Figure)
        """

        # create a new figure with inv_dpi of original image size
        fig_size_w: float = float(org_img.shape[1] * inv_dpi)
        fig_size_h: float = float(org_img.shape[0] * inv_dpi)
        plt.figure(figsize=(fig_size_w, fig_size_h))
        plt.axis("off")  # no axis

        fig = plt.imshow(org_img)  # plot the original image

        # for each leaf block, crate the rectangle and add it to plot
        for block in res_leaf:
            rect = patches.Rectangle(
                (block[0], block[1]),
                block[2],
                block[3],
                linewidth=linewidth,
                edgecolor=edgecolor,
                facecolor=facecolor,
            )
            fig.axes.add_patch(rect)

        # show the results
        if cls._SHOW:
            plt.show()

        plt.close()
        return fig.figure

    def _get_img_from_fig(
        fig: matplotlib.figure.Figure, dpi: int = 100
    ) -> np.ndarray:
        """
        Return a matplotlib figure as a numpy array.

        Args:
            fig: Input matplotlib figure (matplotlib.figure.Figure)
            dpi: Dots per inch (int)

        Returns:
            Output array of an input figure

        Source:
            https://stackoverflow.com/questions/7821518/matplotlib-save-plot-to-numpy-array
        """
        buf: BytesIO = BytesIO()
        fig.savefig(buf, format="png", dpi=dpi)
        buf.seek(0)
        img_buff: np.ndarray = np.frombuffer(buf.getvalue(), dtype=np.uint8)
        buf.close()
        img_arr_bgr: np.ndarray = cv2.imdecode(img_buff, 1)
        im_arr_rgb: np.ndarray = cv2.cvtColor(img_arr_bgr, cv2.COLOR_BGR2RGB)

        return im_arr_rgb

    # Public methods
    @classmethod
    def execute_metric(
        cls,
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
            - balance dimension (float, [0, +inf))
            - symmetry dimension (float, [0, +inf))
            - equilibrium (int, [float, +inf))
            - number of leaves (float, [0, +inf))
            - Quadtree blocks - color entropy based (str, image (PNG) encoded in Base64)
            - Quadtree blocks - gray std based (str, image (PNG) encoded in Base64)
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (should be RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")
        img_rgb_nparray: np.ndarray = np.array(img_rgb)

        # Image Height and Width
        _HEIGHT = img_rgb_nparray.shape[1]
        _WIDTH = img_rgb_nparray.shape[0]

        # COLOR: Compute quadtree color
        cor_size = (0, 0, _HEIGHT, _WIDTH)
        cls._quadtree_color(leaf=img_rgb_nparray, cor_size=cor_size, i=0)
        # Compute quadtree image
        fig_quadtree_color = cls.plot(
            org_img=img_rgb_nparray, res_leaf=cls._RES_LEAF_COLOR
        )
        quadtree_color_arr: np.ndarray = cls._get_img_from_fig(
            fig_quadtree_color
        )
        quadtree_color_im: Image.Image = Image.fromarray(quadtree_color_arr)
        quadtree_color_b64: str = image_utils.to_png_image_base64(
            quadtree_color_im
        )

        # GRAY: Convert img_rgb_nparray to gray scale
        img_gray_nparray: np.ndarray = cv2.cvtColor(
            img_rgb_nparray, cv2.COLOR_RGB2GRAY
        )
        # Compute quadtree gray
        cls._quadtree_gray(leaf_gray=img_gray_nparray, x=0, y=0)
        # Compute quadtree image
        fig_quadtree_gray = cls.plot(img_rgb_nparray, cls._RES_LEAF_GRAY)
        quadtree_gray_arr: np.ndarray = cls._get_img_from_fig(
            fig_quadtree_gray
        )
        quadtree_gray_im: Image.Image = Image.fromarray(quadtree_gray_arr)
        quadtree_gray_b64: str = image_utils.to_png_image_base64(
            quadtree_gray_im
        )

        # Compute metrics for quadtree color: balance, symmetry, and equilibrium
        balance_dim: float = cls._balance(cls._RES_LEAF_COLOR, _HEIGHT, _WIDTH)
        symmetry_dim: float = cls._symmetry(
            cls._RES_LEAF_COLOR, _HEIGHT, _WIDTH
        )
        equilibrium_dim: float = cls._equilibrium(
            cls._RES_LEAF_COLOR, _HEIGHT, _WIDTH
        )
        num_leaves: int = len(cls._RES_LEAF_COLOR)

        return [
            balance_dim,
            symmetry_dim,
            equilibrium_dim,
            num_leaves,
            quadtree_color_b64,
            quadtree_gray_b64,
        ]
