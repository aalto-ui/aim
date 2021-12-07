#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Image visual clutter utility functions.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import Dict, List, Optional, Tuple, Union

# Third-party modules
import cv2
import numpy as np
from scipy import signal
from skimage import transform

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2021-08-28"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Image visual clutter utility functions
# ----------------------------------------------------------------------------


def rgb2lab(im: np.ndarray) -> np.ndarray:
    """
    Converts the RGB color space to the CIELab color space.

    Args:
        im: Input RGB image

    Returns:
        Output Lab image
    """
    im = im / 255.0  # get r,g,b value in the range of [0,1]

    # the figure from graybar.m and the infromation from the website
    # http://www.cinenet.net/~spitzak/conversion/whysrgb.html, we can conclude
    # that our RGB system is sRGB

    # if RGB system is sRGB
    mask = im >= 0.04045
    im[mask] = ((im[mask] + 0.055) / 1.055) ** 2.4
    im[~mask] = im[~mask] / 12.92

    # Observer. = 2°, Illuminant = D65
    matrix = np.array(
        [
            [0.412453, 0.357580, 0.180423],
            [0.212671, 0.715160, 0.072169],
            [0.019334, 0.119193, 0.950227],
        ]
    )

    c_im = np.dot(im, matrix.T)
    c_im[:, :, 0] = c_im[:, :, 0] / 95.047
    c_im[:, :, 1] = c_im[:, :, 1] / 100.000
    c_im[:, :, 2] = c_im[:, :, 2] / 108.833

    mask = c_im >= 0.008856
    c_im[mask] = c_im[mask] ** (1 / 3)
    c_im[~mask] = 7.787 * c_im[~mask] + 16 / 116

    im_Lab = np.zeros_like(c_im)

    im_Lab[:, :, 0] = (116 * c_im[:, :, 1]) - 16
    im_Lab[:, :, 1] = 500 * (c_im[:, :, 0] - c_im[:, :, 1])
    im_Lab[:, :, 2] = 200 * (c_im[:, :, 1] - c_im[:, :, 2])

    return im_Lab


def normlize(arr: np.ndarray) -> np.ndarray:
    """
    Normalizes the array input between (min, max) -> (0, 255).

    Args:
        arr: Ndarray image

    Returns:
        Normlized ndarray
    """
    min_min = arr.min()
    max_max = arr.max()

    if min_min == max_max:
        return np.full_like(arr, 255 / 2).astype("uint8")
    else:
        return (
            (arr - arr.min()) * (1 / (arr.max() - arr.min()) * 255)
        ).astype("uint8")


def conv2(
    x: np.ndarray, y: np.ndarray, mode: Optional[str] = None
) -> np.ndarray:
    """
    Computes the two-dimensional convolution of matrices x and y.

    Args:
        x: First ndarray
        y: Second ndarray
        mode: Method of convolution, default=None, if it sets "same" then
              computes the central part of the convolution

    Returns:
        Convolution ndarray of input matrices
    """
    if mode == "same":
        return np.rot90(
            signal.convolve2d(np.rot90(x, 2), np.rot90(y, 2), mode=mode), 2
        )
    else:
        return signal.convolve2d(x, y)


def RRoverlapconv(kernel: np.ndarray, in_: np.ndarray) -> np.ndarray:
    """
    Filters the image in_ with filter kernel, where it only "counts" the
    part of the filter that overlaps the image.  Rescales the filter so its
    weights which overlap the image sum to the same as the full filter
    kernel.

    Args:
        in_: Input ndarray image
        kernel: Input ndarray filter kernel

    Returns:
        Filtered ndarray of input image with the filter kernel
    """
    # Convolve with the original kernel
    out = conv2(in_, kernel, mode="same")

    # Convolve kernel with an image of 1's, of the same size as the input image
    rect = np.ones_like(in_)

    overlapsum = conv2(rect, kernel, "same")
    # Now scale the output image at each pixel by the relative overlap of the filter with the image
    out = np.sum(kernel) * out / overlapsum
    return out


def RRgaussfilter1D(
    halfsupport: int, sigma: Union[int, float], center: Union[int, float] = 0
) -> np.ndarray:
    """
    Creates a one-dimensional gaussian filter kernel, centered at center
    (default=0), with pixels from a range -halfsupport:halfsupport+1, and
    standard deviation sigma.

    Args:
        halfsupport: Range parameter
        sigma: Standard deviation sigma
        center: Center

    Returns:
        Filtered ndarray of input image with the filter kernel
    """
    t = list(range(-halfsupport, halfsupport + 1))
    kernel = np.array(
        [np.exp(-((x - center) ** 2) / (2 * sigma ** 2)) for x in t]
    )
    kernel = kernel / sum(kernel)

    return kernel.reshape(1, kernel.shape[0])


def DoG1filter(
    a: int, sigma: Union[int, float]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates 2 one-dimensional gaussian filters. Two-dimensional DoG filters
    can be contructed by combining 2 one-dimensional DoG filters separately,
    in x and y directions.

    Args:
        a : Half-support of the filter
        sigma: Standard deviation

    Returns:
        Two one-dimensional ndarray gaussian filters

    References:
        Jitendra Malik and Pietro Perona. Preattentive texture discrimination
        with early vision mechanisms. Journal of Optical Society of America A,
        7(5), May 1990, 923-932.
    """
    sigi = 0.71 * sigma
    sigo = 1.14 * sigma

    t = range(-a, a + 1)

    gi = np.array([np.exp(-(x ** 2) / (2 * sigi ** 2)) for x in t])
    gi = gi / np.sum(gi)
    go = np.array([np.exp(-(x ** 2) / (2 * sigo ** 2)) for x in t])
    go = go / np.sum(go)

    return gi.reshape(1, gi.shape[0]), go.reshape(1, go.shape[0])


def addborder(
    im: np.ndarray, xbdr: int, ybdr: int, arg: Union[str, int, float]
) -> np.ndarray:
    """
    Make image with added border.

    Args:
        im: Input ndarray image
        xbdr: X border size
        ybdr: Y border size
        arg: Constant int for add border values, 'even' for Even reflection,
             'odd' Odd reflection, 'wrap' for Wraparound

    Returns:
        Output ndarray addbordered image

    Examples:
        imnew = addborder(im,5,5,128)  Add 5 wide border of val 128
        imnew = addborder (im,5,5,'even')  Even reflection
        imnew = addborder (im,5,5,'odd')  Odd reflection
        imnew = addborder (im,5,5,'wrap')  Wrap around
    """
    ysize, xsize = im.shape

    # check thickness
    if (xbdr > xsize) or (ybdr > ysize):
        raise ValueError("borders must be thinner than image")

    # if arg is a number, fill border with its value.
    if isinstance(arg, (int, float)):
        imbig = cv2.copyMakeBorder(
            im, ybdr, ybdr, xbdr, xbdr, cv2.BORDER_CONSTANT, value=arg
        )

    # Even reflections
    elif arg == "even":
        imbig = cv2.copyMakeBorder(
            im, ybdr, ybdr, xbdr, xbdr, cv2.BORDER_REFLECT
        )

    # Odd reflections
    elif arg == "odd":
        imbig = cv2.copyMakeBorder(
            im, ybdr, ybdr, xbdr, xbdr, cv2.BORDER_REFLECT_101
        )

    # Wraparound
    elif arg == "wrap":
        imbig = cv2.copyMakeBorder(im, ybdr, ybdr, xbdr, xbdr, cv2.BORDER_WRAP)
    else:
        raise ValueError("unknown border style")
    return imbig


def filt2(
    kernel: np.ndarray,
    im1: np.ndarray,
    reflect_style: Union[str, int, float] = "odd",
) -> np.ndarray:
    """
    Improved version of filter2 in MATLAB, which includes reflection.
    Default style is 'odd'. Also can be 'even', or 'wrap'.

    Args:
        kernel: Kernel
        im1: Input ndarray image
        reflect_style: Kernel reflection, see examples

    Return:
        Output ndarray filterd image with kernel and reflection

    Examples:
        im2 = filt2(kern,image)  Apply kernel with odd reflection (default)
        im2 = filt2(kern,image,'even')  Use even reflection
        im2 = filt2(kern,image,128)  Fill with 128's
    """
    ky, kx = kernel.shape
    iy, ix = im1.shape

    imbig = addborder(im1, kx, ky, reflect_style)
    imbig = conv2(imbig, kernel, "same")
    im2 = imbig[ky : ky + iy, kx : kx + ix]

    return im2


def RRcontrast1channel(pyr: Dict, DoG_sigma: Union[int, float] = 2) -> List:
    """
    Filters a Gaussian pyramid, pyr, with a 1-channel contrast feature detector.

    Args:
        pyr: Gaussian pyramid. It can be computed from this "pyrtools" package
        DoG_sigma: Size of the center-surround (Difference-of-Gaussian) filter
                   used for computing the contrast. Default = 2.
                   Refer to DoG1filter

    Returns:
        1-channel list contrast
    """
    levels = len(pyr)
    contrast = [0] * levels

    # Here we're using the difference-of-gaussian filters. Separable.
    # Refer to routine 'DoG1filter'.
    innerG1, outerG1 = DoG1filter(round(DoG_sigma * 3), DoG_sigma)

    # Do contrast feature computation with these filters:
    for i in range(0, levels):
        inner = filt2(innerG1, pyr[(i, 0)])
        inner = filt2(innerG1.T, inner)
        outer = filt2(outerG1, pyr[(i, 0)])
        outer = filt2(outerG1.T, outer)
        tmp = inner - outer
        contrast[i] = abs(tmp)  # ** 2

    return contrast


def reduce(
    image0: np.ndarray, kernel: Union[None, np.ndarray] = None
) -> np.ndarray:
    """
    Reduce for building Gaussian or Laplacian pyramids. 1-D separable kernels.

    Args:
        image0: Input ndarray
        kernel: Kernel

    Returns:
        Ndarray output image

    Examples:
        imnew = reduce(im0)  Reduce with default kernel: [.05 .25 .4 .25 .05]
        imnew = reduce(im0, kern)  Reduce with kern; sums to unity
    """
    if kernel is None:
        # Default kernel
        kernel = np.array([[0.05, 0.25, 0.4, 0.25, 0.05]])

    ysize, xsize = image0.shape

    image0 = filt2(kernel, image0)  # Filter horizontally.
    # filt2 is filter2 with reflection.
    image1 = image0[:, range(0, xsize, 2)]

    image1 = filt2(kernel.T, image1)  # Filter vertically.
    image2 = image1[range(0, ysize, 2), :]

    return image2


def RRoverlapconvexpand(
    in_: np.ndarray,
    kernel: np.ndarray = np.array([[0.05, 0.25, 0.4, 0.25, 0.05]]),
) -> np.ndarray:
    """
    See Examples.

    Args:
        in_: Input ndarray
        kernel: Kernel

    Retruns:
        Output ndarray, see examples

    Examples:
        out = RRoverlapconvexpand(in_)  Return an image expanded to double size
        out = RRoverlapconvexpand(in, kernel)  Specify 1-D kernel with unity sum
    """
    ysize, xsize = in_.shape
    kernel = kernel * 2  # kernel sum=2 to account for padding.

    tmp = np.zeros([ysize, 2 * xsize])  # First double the width
    k = list(range(0, xsize))
    k_2 = [x * 2 for x in k]
    tmp[:, k_2] = in_[:, k]
    tmp = RRoverlapconv(kernel, tmp)  # ..and filter horizontally.

    out = np.zeros([2 * ysize, 2 * xsize])  # Next double the height
    k = list(range(0, ysize))
    k_2 = [x * 2 for x in k]
    out[k_2, :] = tmp[k, :]
    out = RRoverlapconv(kernel.T, out)  # ..and filter vertically.

    return out


def HV(in_: list):
    """
    Outputs H-V, computes difference of first 2 elements of a list.
    """
    out = in_[0] - in_[1]
    return out


def DD(in_: list):
    """
    Outputs R-L, computes difference of last 2 elements of a list.
    """
    out = in_[3] - in_[2]
    return out


def sumorients(in_: list):
    """
    Sums the four orientations into one image, computes sum of 4 elements of a list.
    """
    out = in_[0] + in_[1] + in_[2] + in_[3]
    return out


def poolnew(
    in_: list, sigma: Union[int, float, None] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Pools with a gaussian. Note assumes that input image is actually
    4 equal-size images, side by side.

    Args:
        in_: List of orientations, 4 equal-size images, side by side
        sigma: Standard deviation sigma of gaussian filter

    Returns:
        4 equal-size pooled images, side by side

    """
    in1 = in_[0]  # H -> first quarter
    in2 = in_[1]  # V -> second quarter
    in3 = in_[2]  # L -> third quarter
    in4 = in_[3]  # R -> last quarter

    if sigma is None:
        out1 = reduce(RRoverlapconvexpand(in1))
        out2 = reduce(RRoverlapconvexpand(in2))
        out3 = reduce(RRoverlapconvexpand(in3))
        out4 = reduce(RRoverlapconvexpand(in4))
    else:
        kernel = RRgaussfilter1D(round(2 * sigma), sigma)
        out1 = reduce(RRoverlapconvexpand(in1, kernel), kernel)
        out2 = reduce(RRoverlapconvexpand(in2, kernel), kernel)
        out3 = reduce(RRoverlapconvexpand(in3, kernel), kernel)
        out4 = reduce(RRoverlapconvexpand(in4, kernel), kernel)

    out = out1, out2, out3, out4

    return out


def imrotate(
    im: np.ndarray,
    angle: Union[float, int],
    method: str = "bicubic",
    bbox: str = "crop",
) -> np.ndarray:
    """
    Rotate an image by Skimage package. Basically just a wrapper to deal with
    the fact that skimage thinks floating point images need to be between
    [-1.0,1.0].

    Args:
        im: Input ndarray image
        anlge: Angle is in DEGREE
        method: Interpolation
        bbox: If output should be as the same size of the input the bbox
              should be "crop", if not should be "losse"

    Retruns:
        Rotated output ndarray image
    """
    # interpolation methods
    func_method = {
        "nearest": 0,
        "bilinear": 1,
        "biquadratic": 2,
        "bicubic": 3,
        "biquartic": 4,
        "biquintic": 5,
    }

    # crop or not methods
    func_bbox = {"loose": True, "crop": False}

    immin = np.min(im)
    imrange = np.max(im) - immin
    im = im - immin
    im = im / imrange
    # roatate
    im = transform.rotate(
        im, angle, order=func_method[method], resize=func_bbox[bbox]
    )
    im = im * imrange
    im = im + immin

    return im


def orient_filtnew(
    pyr: np.ndarray, sigma: Union[int, float] = 16 / 14
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Filters "pyr" (in principle, one level of the Gaussian pyramid generated
    by gausspyr) with 2nd derivative filters in 4 directions.

    Args:
        pyr: Gaussian pyramid. It can be computed from this "pyrtools" package
        sigma: Sigma of filter

    Returns:
        4 output images appended together in a list, in the order horizontal,
        vertical, up-left, and down-right.
    """
    halfsupport = round(3 * sigma)
    # halfsupport was 10, for default sigma.  We need a halfsupport of about
    # 2*sigma for a single Gaussian.  Here we have three, one at -sigma, one at
    # sigma, so we should need a halfsupport of about 3*sigma.

    sigy = sigma
    sigx = sigma  # Was sigx = 3*sigma.

    gx = RRgaussfilter1D(halfsupport, sigx)
    gy = RRgaussfilter1D(halfsupport, sigy, sigma)
    Ga = conv2(gx, gy.T)
    Ga = Ga / np.sum(Ga)
    gy = RRgaussfilter1D(halfsupport, sigy)
    Gb = conv2(gx, gy.T)
    Gb = Gb / np.sum(Gb)
    gy = RRgaussfilter1D(halfsupport, sigy, -sigma)
    Gc = conv2(gx, gy.T)
    Gc = Gc / np.sum(Gc)
    H = -Ga + 2 * Gb - Gc
    V = H.T

    GGa = imrotate(Ga, 45, "bicubic", "crop")
    GGa = GGa / np.sum(GGa)
    GGb = imrotate(Gb, 45, "bicubic", "crop")
    GGb = GGb / np.sum(GGb)
    GGc = imrotate(Gc, 45, "bicubic", "crop")
    GGc = GGc / np.sum(GGc)
    R = -GGa + 2 * GGb - GGc
    GGa = imrotate(Ga, -45, "bicubic", "crop")
    GGa = GGa / np.sum(GGa)
    GGb = imrotate(Gb, -45, "bicubic", "crop")
    GGb = GGb / np.sum(GGb)
    GGc = imrotate(Gc, -45, "bicubic", "crop")
    GGc = GGc / np.sum(GGc)
    L = -GGa + 2 * GGb - GGc

    hout = filt2(H, pyr)
    vout = filt2(V, pyr)
    lout = filt2(L, pyr)
    rout = filt2(R, pyr)

    hvdd = hout, vout, lout, rout

    return hvdd


def histc(x: np.ndarray, bins: np.ndarray) -> np.ndarray:
    """
     MATLAB `histc` equivalent function.

     Args:
         x: Input array
         bins: Array of bins. It has to be 1-dimensional and monotonic

    Rrturns
        Counts the number of values in x that are within each specified bin range
    """
    map_to_bins = np.digitize(
        x, bins
    )  # Get indices of the bins to which each value in input array belongs.
    res = np.zeros(bins.shape)
    for el in map_to_bins:
        res[el - 1] += 1  # Increment appropriate bin.
    return res


def entropy(x: np.ndarray, nbins: Optional[int] = None) -> float:
    """
    Computes the entropy of signal "x", given the number of bins "nbins" used
    uniform binning in the calculation.

    Args:
        x: Ndarray signal x
        nbins: Number of bins

    Returns:
        A float, entropy of x
    """
    nsamples = x.shape[0]

    if nbins is None:
        nbins = int(np.ceil(np.sqrt(nsamples)))
    elif nbins == 1:
        return 0

    edges = np.histogram(x, bins=nbins - 1)[1]
    ref_hist = histc(x, edges)
    ref_hist = ref_hist / float(np.sum(ref_hist))
    ref_hist = ref_hist[np.nonzero(ref_hist)]
    ref_ent = -np.sum(ref_hist * np.log(ref_hist))

    return ref_ent
