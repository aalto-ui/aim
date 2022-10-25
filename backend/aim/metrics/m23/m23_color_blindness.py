#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Color blindness


Description:
    A physiologically-based model for simulation of color vision deficiency.

    Notice: "Since there are no strong biological explanations yet to justify
    the causes of tritanopia and tritanomaly, we simulate tritanomaly based on
    the shift paradigm only (Eq. 19) as an approximation to the actual
    phenomenon and restrain our model from trying to model tritanopia."


Source:
    The code is imported and adopted from
    https://github.com/DaltonLens/DaltonLens-Python.


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Machado, G.M., Oliveira, M.M., and Fernandes, L.A.F. (2009).
        A Physiologically-based Model for Simulation of Color Vision
        Deficiency. IEEE Transactions on Visualization and Computer Graphics,
        15(6), 1291-1298. doi: https://doi.org/10.1109/TVCG.2009.113


Change log:
    v1.0 (2022-10-21)
      * Initial implementation
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
import math
from io import BytesIO
from typing import Dict, List, Optional, Union

# Third-party modules
import numpy as np
from PIL import Image
from pydantic import HttpUrl

# First-party modules
from aim.common import image_utils
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-10-21"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Color blindness.
    """

    # Private constants
    # From https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html#Tutorial
    # Converted to a NumPy array using https://github.com/colour-science/colour/blob/develop/colour/blindness/datasets/machado2010.py
    # The severity range is [0.0, 1.0] with a step of 0.1, but here the index is multiplied by 10 to make it an integer.
    _DEFAULT_SEVERITY: Dict[str, float] = {
        "protan": 1.0,
        "deutan": 1.0,
        "tritan": 1.0,
    }  # severity should be between 0.0 and 1.0
    _MACHADO_2009_MATRICES: Dict[str, Dict[int, np.ndarray]] = {
        "protan": {
            0: np.array(
                [
                    [1.000000, 0.000000, -0.000000],
                    [0.000000, 1.000000, 0.000000],
                    [-0.000000, -0.000000, 1.000000],
                ]
            ),
            1: np.array(
                [
                    [0.856167, 0.182038, -0.038205],
                    [0.029342, 0.955115, 0.015544],
                    [-0.002880, -0.001563, 1.004443],
                ]
            ),
            2: np.array(
                [
                    [0.734766, 0.334872, -0.069637],
                    [0.051840, 0.919198, 0.028963],
                    [-0.004928, -0.004209, 1.009137],
                ]
            ),
            3: np.array(
                [
                    [0.630323, 0.465641, -0.095964],
                    [0.069181, 0.890046, 0.040773],
                    [-0.006308, -0.007724, 1.014032],
                ]
            ),
            4: np.array(
                [
                    [0.539009, 0.579343, -0.118352],
                    [0.082546, 0.866121, 0.051332],
                    [-0.007136, -0.011959, 1.019095],
                ]
            ),
            5: np.array(
                [
                    [0.458064, 0.679578, -0.137642],
                    [0.092785, 0.846313, 0.060902],
                    [-0.007494, -0.016807, 1.024301],
                ]
            ),
            6: np.array(
                [
                    [0.385450, 0.769005, -0.154455],
                    [0.100526, 0.829802, 0.069673],
                    [-0.007442, -0.022190, 1.029632],
                ]
            ),
            7: np.array(
                [
                    [0.319627, 0.849633, -0.169261],
                    [0.106241, 0.815969, 0.077790],
                    [-0.007025, -0.028051, 1.035076],
                ]
            ),
            8: np.array(
                [
                    [0.259411, 0.923008, -0.182420],
                    [0.110296, 0.804340, 0.085364],
                    [-0.006276, -0.034346, 1.040622],
                ]
            ),
            9: np.array(
                [
                    [0.203876, 0.990338, -0.194214],
                    [0.112975, 0.794542, 0.092483],
                    [-0.005222, -0.041043, 1.046265],
                ]
            ),
            10: np.array(
                [
                    [0.152286, 1.052583, -0.204868],
                    [0.114503, 0.786281, 0.099216],
                    [-0.003882, -0.048116, 1.051998],
                ]
            ),
        },
        "deutan": {
            0: np.array(
                [
                    [1.000000, 0.000000, -0.000000],
                    [0.000000, 1.000000, 0.000000],
                    [-0.000000, -0.000000, 1.000000],
                ]
            ),
            1: np.array(
                [
                    [0.866435, 0.177704, -0.044139],
                    [0.049567, 0.939063, 0.011370],
                    [-0.003453, 0.007233, 0.996220],
                ]
            ),
            2: np.array(
                [
                    [0.760729, 0.319078, -0.079807],
                    [0.090568, 0.889315, 0.020117],
                    [-0.006027, 0.013325, 0.992702],
                ]
            ),
            3: np.array(
                [
                    [0.675425, 0.433850, -0.109275],
                    [0.125303, 0.847755, 0.026942],
                    [-0.007950, 0.018572, 0.989378],
                ]
            ),
            4: np.array(
                [
                    [0.605511, 0.528560, -0.134071],
                    [0.155318, 0.812366, 0.032316],
                    [-0.009376, 0.023176, 0.986200],
                ]
            ),
            5: np.array(
                [
                    [0.547494, 0.607765, -0.155259],
                    [0.181692, 0.781742, 0.036566],
                    [-0.010410, 0.027275, 0.983136],
                ]
            ),
            6: np.array(
                [
                    [0.498864, 0.674741, -0.173604],
                    [0.205199, 0.754872, 0.039929],
                    [-0.011131, 0.030969, 0.980162],
                ]
            ),
            7: np.array(
                [
                    [0.457771, 0.731899, -0.189670],
                    [0.226409, 0.731012, 0.042579],
                    [-0.011595, 0.034333, 0.977261],
                ]
            ),
            8: np.array(
                [
                    [0.422823, 0.781057, -0.203881],
                    [0.245752, 0.709602, 0.044646],
                    [-0.011843, 0.037423, 0.974421],
                ]
            ),
            9: np.array(
                [
                    [0.392952, 0.823610, -0.216562],
                    [0.263559, 0.690210, 0.046232],
                    [-0.011910, 0.040281, 0.971630],
                ]
            ),
            10: np.array(
                [
                    [0.367322, 0.860646, -0.227968],
                    [0.280085, 0.672501, 0.047413],
                    [-0.011820, 0.042940, 0.968881],
                ]
            ),
        },
        "tritan": {
            0: np.array(
                [
                    [1.000000, 0.000000, -0.000000],
                    [0.000000, 1.000000, 0.000000],
                    [-0.000000, -0.000000, 1.000000],
                ]
            ),
            1: np.array(
                [
                    [0.926670, 0.092514, -0.019184],
                    [0.021191, 0.964503, 0.014306],
                    [0.008437, 0.054813, 0.936750],
                ]
            ),
            2: np.array(
                [
                    [0.895720, 0.133330, -0.029050],
                    [0.029997, 0.945400, 0.024603],
                    [0.013027, 0.104707, 0.882266],
                ]
            ),
            3: np.array(
                [
                    [0.905871, 0.127791, -0.033662],
                    [0.026856, 0.941251, 0.031893],
                    [0.013410, 0.148296, 0.838294],
                ]
            ),
            4: np.array(
                [
                    [0.948035, 0.089490, -0.037526],
                    [0.014364, 0.946792, 0.038844],
                    [0.010853, 0.193991, 0.795156],
                ]
            ),
            5: np.array(
                [
                    [1.017277, 0.027029, -0.044306],
                    [-0.006113, 0.958479, 0.047634],
                    [0.006379, 0.248708, 0.744913],
                ]
            ),
            6: np.array(
                [
                    [1.104996, -0.046633, -0.058363],
                    [-0.032137, 0.971635, 0.060503],
                    [0.001336, 0.317922, 0.680742],
                ]
            ),
            7: np.array(
                [
                    [1.193214, -0.109812, -0.083402],
                    [-0.058496, 0.979410, 0.079086],
                    [-0.002346, 0.403492, 0.598854],
                ]
            ),
            8: np.array(
                [
                    [1.257728, -0.139648, -0.118081],
                    [-0.078003, 0.975409, 0.102594],
                    [-0.003316, 0.501214, 0.502102],
                ]
            ),
            9: np.array(
                [
                    [1.278864, -0.125333, -0.153531],
                    [-0.084748, 0.957674, 0.127074],
                    [-0.000989, 0.601151, 0.399838],
                ]
            ),
            10: np.array(
                [
                    [1.255528, -0.076749, -0.178779],
                    [-0.078411, 0.930809, 0.147602],
                    [0.004733, 0.691367, 0.303900],
                ]
            ),
        },
    }

    # Private methods
    @staticmethod
    def _linearRGB_from_sRGB(im: np.ndarray):
        """
        Convert sRGB to linearRGB, removing the gamma correction.
        Formula taken from Wikipedia https://en.wikipedia.org/wiki/SRGB

        Args:
            im : The input sRGB image, normalized between [0, 1]

        Returns:
            The output RGB image, array of shape (M, N, 3) with dtype float
        """
        out: np.ndarray = np.zeros_like(im)
        small_mask: np.ndarray = im < 0.04045
        large_mask: np.ndarray = np.logical_not(small_mask)
        out[small_mask] = im[small_mask] / 12.92
        out[large_mask] = np.power((im[large_mask] + 0.055) / 1.055, 2.4)
        return out

    @staticmethod
    def _sRGB_from_linearRGB(im: np.ndarray):
        """
        Convert linearRGB to sRGB, applying the gamma correction.
        Formula taken from Wikipedia https://en.wikipedia.org/wiki/SRGB

        Args:
            im : The input RGB image, normalized between [0, 1]

        Returns:
            The output sRGB image, array of shape (M, N, 3) with dtype float
        """
        out: np.ndarray = np.zeros_like(im)
        # Make sure we're in range, otherwise gamma will go crazy.
        im_clipped: np.ndarray = np.clip(im, 0.0, 1.0)
        small_mask: np.ndarray = im_clipped < 0.0031308
        large_mask: np.ndarray = np.logical_not(small_mask)
        out[small_mask] = im_clipped[small_mask] * 12.92
        out[large_mask] = (
            np.power(im_clipped[large_mask], 1.0 / 2.4) * 1.055 - 0.055
        )
        return out

    @staticmethod
    def _as_float32(im: np.ndarray):
        """
        Divide by 255 and cast the uint8 image to float32
        """
        return im.astype(np.float32) / 255.0

    @staticmethod
    def _as_uint8(im: np.ndarray):
        """
        Multiply by 255 and cast the float image to uint8
        """
        return (np.clip(im, 0.0, 1.0) * 255.0).astype(np.uint8)

    @staticmethod
    def _apply_color_matrix(im: np.ndarray, m: np.ndarray):
        """
        Transform a color array with the given 3x3 matrix.

        Args:
            im: Input image with array of shape (..., 3)
            m: Color matrix to apply with array of shape (3, 3)

        Returns:
            Output array with shape of (..., 3), where each input color vector was multiplied by m
        """
        # Another option is np.einsum('ij, ...j', m, im), but it can be much
        # slower, especially on float32 types because the matrix
        # multiplication is heavily optimized.
        # So the matmul is generally (much) faster, but we need to take the
        # transpose of m as it gets applied on the right side. Indeed, for
        # each column color vector v we wanted $v' = m . v$ . To flip the
        # side we can use $m . v = (v^T . m^T)^T$ . The transposes on the 1d
        # vector are implicit and can be ignored, so we just need to compute
        # $v . m^T$. This is what numpy matmul will do for all the vectors
        # thanks to its broadcasting rules that pick the last 2 dimensions of
        # each array, so it will actually compute matrix multiplications of
        # shape (M, 3) x (3, 3) with M the penultimate dimension of m. That
        # will write a matrix of shape (M,3) with each row storing the result
        # of $v' = v . M^T$.
        return im @ m.T

    @classmethod
    def _simulate_cvd_linear_rgb(
        cls,
        image_linear_rgb_float32: np.ndarray,
        deficiency: str,
        severity: float,
    ):
        """
        Simulate the appearance of a linear rgb image for the given color
        vision deficiency.

        Args:
            image_linear_rgb_float32: The input linear RGB image (np.ndarray), with values in [0, 1]
            deficiency: The deficiency (str) to simulate
            severity: The severity (float) between 0 (normal vision) and 1 (complete dichromacy)

        Returns:
            The simulated rgb image (np.ndarray) with values in [0, 1]
        """
        severity_lower: int = int(math.floor(severity * 10.0))
        severity_higher: int = min(severity_lower + 1, 10)
        m1: np.ndarray = cls._MACHADO_2009_MATRICES[deficiency][severity_lower]
        m2: np.ndarray = cls._MACHADO_2009_MATRICES[deficiency][
            severity_higher
        ]

        # alpha = 0 => only m1, alpha = 1.0 => only m2
        alpha: float = severity - severity_lower / 10.0
        m: np.ndarray = alpha * m2 + (1.0 - alpha) * m1

        return cls._apply_color_matrix(image_linear_rgb_float32, m)

    @classmethod
    def _simulate_cvd(
        cls, img_rgb: Image.Image, deficiency: str, severity: float
    ):
        """
        Simulate the appearance of an image for the given color vision deficiency.

        Args:
            img_rgb: The input RGB image (Image.Image), with values in [0, 255]
            deficiency: The deficiency (str) to simulate
            severity: The severity (float) between 0 (normal vision) and 1 (complete dichromacy)

        Returns:
            The simulated sRGB image (Image.Image) with values in [0, 255]
        """
        # Get NumPy linear rgb image of input image
        img_srgb_norm: np.ndarray = cls._as_float32(np.array(img_rgb))
        im_linear_rgb: np.ndarray = cls._linearRGB_from_sRGB(img_srgb_norm)

        # Compute simulated image
        im_cvd_linear_rgb: np.ndarray = cls._simulate_cvd_linear_rgb(
            im_linear_rgb, deficiency, severity
        )
        im_cvd_float: np.ndarray = cls._sRGB_from_linearRGB(im_cvd_linear_rgb)

        # Convert NumPy array to Image.Image format
        im_cvd_unit8: np.ndarray = cls._as_uint8(im_cvd_float)
        img_cvd_srgb: Image.Image = Image.fromarray(im_cvd_unit8, mode="RGB")
        return img_cvd_srgb

    # Public methods
    @classmethod
    def execute_metric(
        cls,
        gui_image: str,
        gui_type: int = GUI_TYPE_DESKTOP,
        gui_url: Optional[HttpUrl] = None,
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1
            gui_url: GUI URL (defaults to None)

        Returns:
            Results (list of measures)
            - Protanopia (str, image (PNG) encoded in Base64)
            - Deuteranopia (str, image (PNG) encoded in Base64)
            - Tritanopia (str, image (PNG) encoded in Base64)
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Compute protanope
        # Definition: A protan or a protanope is a person suffering from
        # protanopia ("strong" protan) or protanomaly ("mild" protan).
        protan_im: Image.Image = cls._simulate_cvd(
            img_rgb, "protan", cls._DEFAULT_SEVERITY["protan"]
        )
        protan_b64: str = image_utils.to_png_image_base64(protan_im)

        # Compute deuteranope
        # Definition: A deutan or a deuteranope is a person suffering from
        # deuteranopia ("strong" deutan) or deuteranomaly ("mild" deutan).
        deutan_im: Image.Image = cls._simulate_cvd(
            img_rgb, "deutan", cls._DEFAULT_SEVERITY["deutan"]
        )
        deutan_b64: str = image_utils.to_png_image_base64(deutan_im)

        # Compute tritanope
        # Definition: A tritan or a tritanope is a person suffering from
        # tritanopia ("strong" tritan) or tritanomaly ("mild" tritan).
        tritan_im: Image.Image = cls._simulate_cvd(
            img_rgb, "tritan", cls._DEFAULT_SEVERITY["tritan"]
        )
        tritan_b64: str = image_utils.to_png_image_base64(tritan_im)

        return [
            protan_b64,
            deutan_b64,
            tritan_b64,
        ]
