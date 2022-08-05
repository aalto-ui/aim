#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Color Harmonization utility functions.
Some Codes are imported and adopted from https://github.com/tartarskunk/ColorHarmonization
"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from io import BytesIO
from typing import List, Union

# Third-party modules
import cv2
import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2022-06-29"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"

# ----------------------------------------------------------------------------
# Color Harmonization utility functions
# ----------------------------------------------------------------------------


def deg_distance(deg_arr: np.ndarray, deg_float: float) -> np.ndarray:
    """
    Compute absolute minimum distance between an array elements and a float

    Args:
        deg_arr: array of degrees (np.ndarray)
        deg_float: float degree (float)

    Returns:
        minimum distance between each element of deg_arr and deg_float
    """

    # Compute min distance between each 2 degrees
    d1: np.ndarray = np.abs(deg_arr - deg_float)
    d2: np.ndarray = np.abs(360 - d1)
    d: np.ndarray = np.minimum(d1, d2)
    return d


def normalized_gaussian(
    X: np.ndarray, mu: Union[int, float], S: np.ndarray
) -> np.ndarray:
    """
    Compute normalized gaussian for input array

    Args:
        X: array of inputs
        mu: mean
        S: sigma

    Returns:
        normalized gaussian
    """

    # Compute exponent of Gaussian distribution formula
    # More on https://en.wikipedia.org/wiki/Normal_distribution
    X = np.asarray(X).astype(np.float64)
    S = np.asarray(S).astype(np.float64)
    D: np.ndarray = np.deg2rad(X - mu)
    S = np.deg2rad(S)
    D2: np.ndarray = np.multiply(D, D)
    S2: np.ndarray = np.multiply(S, S)
    dist: np.ndarray = np.exp(-D2 / (2 * S2))
    return dist


class HueSector:
    def __init__(self, center: Union[int, float], width: Union[int, float]):
        # In Degree [0,2 pi)
        self.center: Union[int, float] = center
        self.width: Union[int, float] = width
        self.border: List[Union[float, int]] = [
            (self.center - self.width / 2),
            (self.center + self.width / 2),
        ]

    def is_in_sector(self, H: np.ndarray) -> np.ndarray:
        # True/False matrix if hue resides in the sector
        hue_in_arr: np.ndarray = deg_distance(H, self.center) < self.width / 2
        return hue_in_arr

    def distance_to_border(self, H: np.ndarray) -> np.ndarray:
        # distance to border
        H_1: np.ndarray = deg_distance(H, self.border[0])
        H_2: np.ndarray = deg_distance(H, self.border[1])
        H_dist2bdr: np.ndarray = np.minimum(H_1, H_2)
        return H_dist2bdr

    def closest_border(self, H: np.ndarray) -> np.ndarray:
        # closest border
        H_1: np.ndarray = deg_distance(H, self.border[0])
        H_2: np.ndarray = deg_distance(H, self.border[1])
        H_cls_bdr: np.ndarray = np.argmin((H_1, H_2), axis=0)
        H_cls_bdr = 2 * (H_cls_bdr - 0.5)
        return H_cls_bdr

    def distance_to_center(self, H: np.ndarray) -> np.ndarray:
        # distance to center
        H_dist2ctr: np.ndarray = deg_distance(H, self.center)
        return H_dist2ctr


class HarmonicScheme:
    def __init__(self, sectors: List[HueSector]):
        # sectors
        self.sectors: List[HueSector] = sectors

    def hue_distance(self, H: np.ndarray) -> np.ndarray:
        # hue distance
        H_dis: List[np.ndarray] = []
        for i in range(len(self.sectors)):
            sector: HueSector = self.sectors[i]
            H_dis.append(sector.distance_to_border(H))
            H_dis[i][sector.is_in_sector(H)] = 0
        H_dis_arr: np.ndarray = np.asarray(H_dis)
        H_dis_arr = H_dis_arr.min(axis=0)
        return H_dis_arr

    def harmony_score(self, X: np.ndarray):
        # Opencv store H as [0, 180) --> [0, 360)
        H: np.ndarray = X[:, :, 0].astype(np.int32) * 2
        # Opencv store S as [0, 255] --> [0, 1]
        S: np.ndarray = X[:, :, 1].astype(np.float32) / 255.0

        # Compute harmnoy score
        H_dis: np.ndarray = self.hue_distance(H)
        H_dis = np.deg2rad(H_dis)
        score: float = float(np.sum(np.multiply(H_dis, S)))
        return score

    def hue_shifted(self, X: np.ndarray, num_superpixels: int = -1):
        # Shift Hue
        Y: np.ndarray = X.copy()
        H: np.ndarray = X[:, :, 0].astype(np.int32) * 2

        H_d2b: List[np.ndarray] = [
            sector.distance_to_border(H) for sector in self.sectors
        ]
        H_d2b_arr: np.ndarray = np.asarray(H_d2b)

        H_cls: np.ndarray = np.argmin(H_d2b_arr, axis=0)

        if num_superpixels != -1:
            SEEDS: cv2.ximgproc_SuperpixelSEEDS = (
                cv2.ximgproc.createSuperpixelSEEDS(
                    X.shape[1], X.shape[0], X.shape[2], num_superpixels, 10
                )
            )
            SEEDS.iterate(X, 4)

            grid_num: int = SEEDS.getNumberOfSuperpixels()
            labels: np.ndarray = SEEDS.getLabels()

            for i in range(grid_num):
                s: float = float(np.average(H_cls[labels == i]))
                H_cls[labels == i] = 1 if s > 0.5 else 0

        H_ctr: np.ndarray = np.zeros((H.shape))
        H_wid: np.ndarray = np.zeros((H.shape))
        H_d2c: np.ndarray = np.zeros((H.shape))
        H_dir: np.ndarray = np.zeros((H.shape))

        for i in range(len(self.sectors)):
            sector: HueSector = self.sectors[i]
            mask: np.ndarray = H_cls == i
            H_ctr[mask] = sector.center
            H_wid[mask] = sector.width
            H_dir += sector.closest_border(H) * mask
            H_dist2ctr: np.ndarray = sector.distance_to_center(H)
            H_d2c += H_dist2ctr * mask

        H_sgm: np.ndarray = H_wid / 2
        H_gau: np.ndarray = normalized_gaussian(H_d2c, 0, H_sgm)

        H_tmp: np.ndarray = np.multiply(H_sgm, 1 - H_gau)
        H_shf: np.ndarray = np.multiply(H_dir, H_tmp)
        H_new: np.ndarray = (H_ctr + H_shf).astype(np.int32)

        for i in range(len(self.sectors)):
            sector = self.sectors[i]
            mask = sector.is_in_sector(H)
            np.copyto(H_new, H, where=sector.is_in_sector(H))

        H_new = np.remainder(H_new, 360)
        H_new = (H_new / 2).astype(np.uint8)
        Y[:, :, 0] = H_new
        return Y


def count_hue_histogram(X: np.ndarray) -> np.ndarray:
    N: int = 360
    H: np.ndarray = X[:, :, 0].astype(np.int32) * 2
    S: np.ndarray = X[:, :, 1].astype(np.float64) / 255.0
    H_flat: np.ndarray = H.flatten()
    S_flat: np.ndarray = S.flatten()

    histo: np.ndarray = np.zeros(N)
    for i in range(len(H_flat)):
        histo[H_flat[i]] += S_flat[i]
    return histo


def plothis(
    hue_histo: np.ndarray, harmonic_scheme: HarmonicScheme, caption: str
) -> matplotlib.figure.Figure:
    N: int = 360

    # Compute pie slices
    theta: np.ndarray = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    width: float = float(np.pi / 180)

    # Compute colors
    hue_colors: np.ndarray = np.zeros((N, 4))
    shadow_colors: np.ndarray = np.zeros((N, 4))
    for i in range(N):
        # Compute colors, RGB values for the hue
        color_HSV: np.ndarray = np.zeros((1, 1, 3), dtype=np.uint8)
        color_HSV[0, 0, :] = [int(i / 2), 255, 255]
        color_BGR = cv2.cvtColor(color_HSV, cv2.COLOR_HSV2BGR)
        B: float = float(int(color_BGR[0, 0, 0]) / 255.0)
        G: float = float(int(color_BGR[0, 0, 1]) / 255.0)
        R: float = float(int(color_BGR[0, 0, 2]) / 255.0)
        hue_colors[i] = (R, G, B, 1.0)

        # Compute colors, for the shadow
        shadow_colors[i] = (0.0, 0.0, 0.0, 1.0)

    # Create hue, guidline and shadow arrays
    hue_histo = hue_histo.astype(float)
    # Normalize hue histo
    hue_histo_msx: float = float(np.max(hue_histo))
    if hue_histo_msx != 0.0:
        hue_histo /= np.max(hue_histo)

    # Compute angels of shadow, template types
    shadow_histo: np.ndarray = np.array([0.0] * N)
    for sector in harmonic_scheme.sectors:
        sector_center: Union[int, float] = sector.center
        sector_width: Union[int, float] = sector.width
        end: int = int((sector_center + sector_width / 2) % 360)
        start: int = int((sector_center - sector_width / 2) % 360)

        if start < end:
            shadow_histo[start:end] = 1.0
        else:
            shadow_histo[start:360] = 1.0
            shadow_histo[0:end] = 1.0

    # Plot, 1280 * 800
    fig: matplotlib.figure.Figure = plt.figure(figsize=(6.4, 8))
    ax = fig.add_subplot(111, projection="polar")
    # add hue histogram
    ax.bar(
        theta, hue_histo, width=width, bottom=0.0, color=hue_colors, alpha=1.0
    )
    # add guidline
    guide_histo: np.ndarray = np.array([0.05] * N)
    ax.bar(
        theta,
        guide_histo,
        width=width,
        bottom=1.0,
        color=hue_colors,
        alpha=1.0,
    )
    # add shadow angels for the template types
    ax.bar(
        theta,
        shadow_histo,
        width=width,
        bottom=0.0,
        color=shadow_colors,
        alpha=0.1,
    )
    ax.set_title(caption, pad=15)

    plt.close()

    return fig


def get_img_from_fig(
    fig: matplotlib.figure.Figure, dpi: int = 100
) -> np.ndarray:
    """
    Returns a matplotlib figure as a numpy array

    Args:
        fig: input matplotlib figure (matplotlib.figure.Figure)
        dpi: dots per inch (int)

    Returns:
        output array of input figure

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
