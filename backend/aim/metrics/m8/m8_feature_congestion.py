#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Metric:
    Feature Congestion clutter measure


Description:
    This measure (Feature Congestion) of visual clutter is based on the analogy 
    that a display or scene is more cluttered the more difficult it would be to
    add a new item which would reliably draw attention.

    Category: Visual complexity > Information discriminability.
    For details, see 'Feature Congestion clutter measure' [1, 2].


Funding information and contact:
    This work was funded by Technology Industries of Finland in a three-year
    project grant on self-optimizing web services. The principal investigator
    is Antti Oulasvirta (antti.oulasvirta@aalto.fi) of Aalto University.


References:
    1.  Rosenholtz, Ruth, Yuanzhen Li, and Lisa Nakano.
        "Measuring visual clutter." Journal of vision 7.2 (2007): 17-17.
        doi:https://doi.org/10.1167/7.2.17
        
    2.  Ruth Rosenholtz, Yuanzhen Li, Jonathan Mansfield, and Zhenlan Jin.
        "Feature Congestion: A Measure of Display Clutter". 
        CHI '05: Proc. of the SIGCHI conference on Human factors in computing systems. May 2005. 761-770. 
        doi:https://doi.org/10.1167/6.6.827
                
Change log:
    v1.0 (2021-08-31)
      * Initial implementation

"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import base64
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union

# Third-party modules
import numpy as np
from PIL import Image
import pyrtools as pt

# First-party modules
from aim.common.constants import GUI_TYPE_DESKTOP
from aim.metrics.interfaces import AIMMetricInterface
from aim.common.image_visual_clutter_utils import *
# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2021-08-31"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------


class Metric(AIMMetricInterface):
    """
    Metric: Subband Entropy clutter measure.
    """

    # Private constants
    _NUM_LEVELS = 3 # the number of levels
    _CONTRAST_FILT_SIGMA = 1 # the standard deviation of the center-surround DoG1 filter used for computing the contrast 
    _CONTRAST_POOL_SIGMA = 3 # the standard deviation of this Gaussian window for contrast clutter
    _COLOR_POOL_SIGMA = 3 # the standard deviation of this Gaussian window for color clutter
    _ORIENT_POOL_SIGMA = 7/2 # orient_pool_sigma is the standard deviation of this Gaussian window
    _ORIENT_NOISE = 0.001  # Was eps, but that gave too much orientation noise in the saliency maps.  Then changed to 0.000001

    ## OPP_ENERGY constants:
    # These probably seem like arbitrary numbers, but it's just trying to get
    # three very different feature extraction methods to operate at basically
    # the same scales.
    _OPP_ENERGY_NOISE = 1.0 # Was 1.5
    _OPP_ENERGY_FILTER_SCALE = 16/14*1.75
    _OPP_ENERGY_POOL_SCALE = 1.75

    # clutter coeficients to compute final feature congestion map
    _COLOR_COEF = 0.2088
    _CONTRAST_COEF = 0.0660
    _ORIENT_COEF = 0.0269
    _MINKOWSKI_ORDER = 1 # a parameter when combining local clutter over space
    

    # Create empty luminance(L) and the chrominance(a,b) channels
    _L_pyr = {}
    _a_pyr = {}
    _b_pyr = {}
    
    @staticmethod
    def _collapse(clutter_levels: List) -> np.ndarray:
        """
        Collapse over scales by taking the maximum.
        
        First get a Gaussian kernel to upsample the clutter maps on bigger scales
        so that the clutter maps would have the same sizes, and max can be taken
        across scales.
        
        Args:
            clutter_levels: List of clutter levels
            
        Returns:
            Collapsed clutter map
        """
        kernel_1d = np.array([[0.05, 0.25, 0.4, 0.25, 0.05]])
        kernel_2d = conv2(kernel_1d, kernel_1d.T)

        clutter_map = clutter_levels[0].copy()
        for scale in range(1,len(clutter_levels)):
            clutter_here = clutter_levels[scale]

            for kk in range(scale, 0, -1):
                clutter_here = pt.upConv(image=clutter_here, filt=kernel_2d, edge_type='reflect1', step=[2,2], start=[0,0])

            common_sz = min(clutter_map.shape[0], clutter_here.shape[0]), min(clutter_map.shape[1], clutter_here.shape[1])
            for i in range(0, common_sz[0]):
                for j in range(0, common_sz[1]):
                    clutter_map[i][j] = max(clutter_map[i][j], clutter_here[i][j])

            return clutter_map


    # Private methods
    @classmethod
    def _color_clutter(cls) -> np.ndarray:
        """  
        Computes the color clutter map of an image. 
        
        Color clutter is computed as the "volume" of a color distribution
        ellipsoid, which is the determinant of covariance matrix. Covariance 
        matrix can be computed efficiently through linear filtering. More 
        specifically, cov(X,Y) = E(XY)-E(X)E(Y), where E (expectation value) 
        can be approximated by filtering with a Gaussian window. 
        
        Returns:
            Results
            - color_clutter_map (ndarray): an array of the same size as inputImage 
        """
        
        # initiatialization
        covMx = {}
        color_clutter_levels = [0] * cls._NUM_LEVELS
        DL = [0] * cls._NUM_LEVELS
        Da = [0] * cls._NUM_LEVELS
        Db = [0] * cls._NUM_LEVELS


        # sensitivitis to the L,a,and b channels are different, therefore we use
        # deltaL2, deltaa2, and deltab2 to "scale" the L,a,b axes when computing
        # the covariance matrix. Eventually these numbers should be vary according
        # to the spatial scales, mimicing our visual system's sensitivity function
        deltaL2 = 0.0007 ** 2
        deltaa2 = 0.1 ** 2
        deltab2 = 0.05 ** 2

        # Get a Gaussian filter for computing the covariance
        bigG = RRgaussfilter1D(round(2*cls._COLOR_POOL_SIGMA), cls._COLOR_POOL_SIGMA)

        for i in range(0, cls._NUM_LEVELS):
            # get E(X) by filtering X with a 1-D Gaussian window separably in x and y directions:
            DL[i] = RRoverlapconv(bigG, cls._L_pyr[(i,0)])
            DL[i] = RRoverlapconv(bigG.T, DL[i])   # E(L)
            Da[i] = RRoverlapconv(bigG, cls._a_pyr[(i,0)])
            Da[i] = RRoverlapconv(bigG.T, Da[i])   # E(a)
            Db[i] = RRoverlapconv(bigG, cls._b_pyr[(i,0)]);
            Db[i] = RRoverlapconv(bigG.T, Db[i])    # E(b)


            # Covariance matrix 
            # covMx(L,a,b) = | cov(L,L)  cov(L,a)  cov(L,b) |
            #                | cov(a,L)  cov(a,a)  cov(a,b) |
            #                | cov(b,L)  cov(b,a)  cov(b,b) |
            # where cov(X,Y) = E(XY) - E(X)E(Y)
            #   and if X is the same as Y, then it's the variance var(X) =
            #   E(X.^2)-E(X).^2
            # and as cov(X,Y) = cov(Y,X), covMx is symmetric
            # covariance matrix elements:
            covMx[(i,0,0)] = RRoverlapconv(bigG, cls._L_pyr[(i,0)] ** 2)
            covMx[(i,0,0)] = RRoverlapconv(bigG.T, covMx[(i,0,0)]) - DL[i] ** 2 + deltaL2  # cov(L,L) + deltaL2
            covMx[(i,0,1)] = RRoverlapconv(bigG, cls._L_pyr[(i,0)] * cls._a_pyr[(i,0)])
            covMx[(i,0,1)] = RRoverlapconv(bigG.T, covMx[(i,0,1)]) - DL[i] * Da[i]        # cov(L,a)
            covMx[(i,0,2)] = RRoverlapconv(bigG, cls._L_pyr[(i,0)] * cls._b_pyr[(i,0)])
            covMx[(i,0,2)] = RRoverlapconv(bigG.T, covMx[(i,0,2)]) - DL[i] * Db[i]        # cov(L,b)
            covMx[(i,1,1)] = RRoverlapconv(bigG, cls._a_pyr[(i,0)] ** 2)
            covMx[(i,1,1)] = RRoverlapconv(bigG.T, covMx[(i,1,1)]) - Da[i] ** 2 + deltaa2  # cov(a,a) + deltaa2
            covMx[(i,1,2)] = RRoverlapconv(bigG, cls._a_pyr[(i,0)] * cls._b_pyr[(i,0)])
            covMx[(i,1,2)] = RRoverlapconv(bigG.T, covMx[(i,1,2)]) - Da[i] * Db[i]        # cov(a,b)
            covMx[(i,2,2)] = RRoverlapconv(bigG, cls._b_pyr[(i,0)] ** 2)    
            covMx[(i,2,2)] = RRoverlapconv(bigG.T, covMx[(i,2,2)]) - Db[i] ** 2 + deltab2;  # cov(b,b) + deltab2

            # Get the determinant of covariance matrix
            # which is the "volume" of the covariance ellipsoid
            detIm = covMx[(i,0,0)]*(covMx[(i,1,1)]*covMx[(i,2,2)]-covMx[(i,1,2)]*covMx[(i,1,2)])\
            - covMx[(i,0,1)]*(covMx[(i,0,1)]*covMx[(i,2,2)]-covMx[(i,1,2)]*covMx[(i,0,2)])\
            + covMx[(i,0,2)]*(covMx[(i,0,1)]*covMx[(i,1,2)]-covMx[(i,1,1)]*covMx[(i,0,2)])

            # take the square root considering variance is squared, and the cube
            # root, since this is the volume and the contrast measure is a "length"
            color_clutter_levels[i] = np.sqrt(detIm) ** (1/3)
            
        # Compute color clutter map   
        color_clutter_map = cls._collapse(color_clutter_levels)
        
        return color_clutter_map
    
    @classmethod
    def _contrast_clutter(cls) -> np.ndarray:  
        """
        Computes the contrast clutter map of an image.
        
 
         Returns:
            Results
            - contrast_clutter_map (ndarray): an array of the same size as inputImage 
        """
        # We then compute a form of "contrast-energy" by filtering the luminance
        # channel L by a center-surround filter and squaring (or taking the absolute 
        # values of) the filter outputs. The center-surround filter is a DoG1 filter 
        # with std 'contrast_filt_sigma'.
        contrast = RRcontrast1channel(cls._L_pyr, cls._CONTRAST_FILT_SIGMA)

        # initiate clutter_map and clutter_levels:
        m, n = len(contrast), 1
        contrast_clutter_levels = [0] * m
        
        # Get a Gaussian filter for computing the variance of contrast
        # Since we used a Gaussian pyramid to find contrast features, these filters 
        # have the same size regardless of the scale of processing.
        bigG = RRgaussfilter1D(round(cls._CONTRAST_POOL_SIGMA*2), cls._CONTRAST_POOL_SIGMA)

        for scale in range(0,m):
            for channel in range(0,n):
                # var(X) = E(X.^2) - E(X).^2
                # get E(X) by filtering X with a 1-D Gaussian window separably in x and y directions
                meanD = RRoverlapconv(bigG, contrast[scale])
                meanD = RRoverlapconv(bigG.T, meanD)
                # get E(X.^2) by filtering X.^2 with a 1-D Gaussian window separably in x and y directions
                meanD2 = RRoverlapconv(bigG, contrast[scale] ** 2)
                meanD2 = RRoverlapconv(bigG.T, meanD2)

                # get variance by var(X) = E(X.^2) - E(X).^2
                stddevD = np.sqrt(abs(meanD2 - meanD ** 2))
                contrast_clutter_levels[scale] = stddevD

        contrast_clutter_map = cls._collapse(contrast_clutter_levels)
        return contrast_clutter_map
    
    @classmethod
    def _rr_orientation_opp_energy(cls) -> np.ndarray:
        """
        OPP_ENERGY    This runs the oriented opponent energy calculation that
        serves as the first stages in Bergen & Landy's (1990)
        texture segmentor, except it uses DOOG filters (which actually
        don't work as well, but at least we can more easily control the
        scale).
        """

        hvdd = [0] * cls._NUM_LEVELS
        hv = [0] * cls._NUM_LEVELS
        dd = [0] * cls._NUM_LEVELS
        out = [0] * cls._NUM_LEVELS
        total = [0] * cls._NUM_LEVELS

        for scale in range(0, cls._NUM_LEVELS):
            # Check this is the right order for Landy/Bergen. RRR
            hvdd[scale] = orient_filtnew(cls._L_pyr[(scale,0)],cls._OPP_ENERGY_FILTER_SCALE) 
            # filt with 4 oriented filters 0, 45, 90, 135.  Was sigma = 16/14, orient_filtnew,
            # then 16/14*1.75 to match contrast and other scales.
            # Eventually make this sigma a variable that's passed to this routine.
            # hvdd[scale] is the 4 output images concatenated together, 
            # in the order horizontal, vertical, up-left, and down-right.

            hvdd[scale] = [x ** 2 for x in hvdd[scale]]    #local energy
            hvdd[scale] = poolnew(hvdd[scale], cls._OPP_ENERGY_POOL_SCALE) #Pools with a gaussian filter.  Was effectively sigma=1, then 1.75 to match 1.75 above.
            # RRR Should look at these results and see if this is the right amount of
            # pooling for the new filters.  It was right for the Landy-Bergen
            # filters.
            hv[scale] = HV(hvdd[scale]) # get the difference image between horizontal and vertical: H-V (0-90)
            dd[scale] = DD(hvdd[scale]) # get the difference image between right and left: R-L (45-135)
            # Normalize by the total response at this scale, assuming the total
            # response is high enough.  If it's too low, we'll never see this
            # orientation.  I'm not sure what to do here -- set it to zeros and
            # it's like that's the orientation.  Maybe output the total response
            # and decide what to do later.  RRR
            total[scale] = sumorients(hvdd[scale]) + cls._OPP_ENERGY_NOISE # add noise based upon sumorients at visibility threshold
            hv[scale] = hv[scale]/total[scale] # normalize the hv and dd image
            dd[scale] = dd[scale]/total[scale]
            out[scale] = hv[scale], dd[scale] # out is the 2 output images concatenated together, in the order of hv, dd

        return out

    @classmethod
    def _orientation_clutter(cls):
        """
        Computes the orientation clutter map of an image. 

        Orientation clutter is computed as the "volume" of an orientation distribution
        ellipsoid, which is the determinant of covariance matrix. Treats cos(2 theta)
        and sin(2 theta) (computed from OrientedOppEnergy) as a two-vector, and gets
        The covariance of this two-vector.  The covariance 
        matrix can be computed efficiently through linear filtering. More 
        specifically, cov(X,Y) = E(XY)-E(X)E(Y), where E (expectation value) 
        can be approximated by filtering with a Gaussian window. 
        poolScale is set to 7/2.

        This currently seems far too dependent on luminance contrast.  Check into
        why this is so -- I thought we were normalizing by local contrast.

        Returns:
            Results
            - orientation_clutter_map (ndarray): an array of the same size as inputImage
        """
 
        Dc = [0] * cls._NUM_LEVELS  # mean "cos 2 theta" at distractor scale
        Ds = [0] * cls._NUM_LEVELS  # mean "sin 2 theta" at distractor scale

        # Get approximations to cos(2theta) and sin(2theta) from oriented opponent
        # energy, at each of the numlevels of the pyramid
        angles = cls._rr_orientation_opp_energy()

        # Compute the two-vector [meancos, meansin] at each scale, as well as the
        # things we need to compute the mean and covariance of this two-vector at
        # the larger, distractor scale.
        bigG = RRgaussfilter1D(round(8*cls._ORIENT_POOL_SIGMA), 4*cls._ORIENT_POOL_SIGMA)
        maxbigG = max(bigG) ** 2


        covMx = {}
        orientation_clutter_levels = [0] * cls._NUM_LEVELS

        for i in range(0,cls._NUM_LEVELS):
            cmx = angles[i][0]
            smx = angles[i][1]

            # Pool to get means at distractor scale. In pooling, don't pool over the target
            # region (implement this by pooling with a big Gaussian, then
            # subtracting the pooling over the target region computed above.  Note,
            # however, that we first need to scale the target region pooling so
            # that its peak is the same height as this much broader Gaussian used
            # to pool over the distractor region.
            Dc[i] = RRoverlapconv(bigG, cmx)
            Dc[i] = RRoverlapconv(bigG.T, Dc[i])
            Ds[i] = RRoverlapconv(bigG, smx)
            Ds[i] = RRoverlapconv(bigG.T, Ds[i])

            # Covariance matrix elements.  Compare with computations in
            # RRStatisticalSaliency.  I tried to match computeColorClutter, but I
            # don't remember the meaning of some of the terms I removed.  XXX
            covMx[(i,0,0)] = RRoverlapconv(bigG, cmx ** 2)
            covMx[(i,0,0)] = RRoverlapconv(bigG.T, covMx[(i,0,0)]) - Dc[i] ** 2 + cls._ORIENT_NOISE
            covMx[(i,0,1)] = RRoverlapconv(bigG, cmx * smx)
            covMx[(i,0,1)] = RRoverlapconv(bigG.T, covMx[(i,0,1)]) - Dc[i] * Ds[i]
            covMx[(i,1,1)] = RRoverlapconv(bigG, smx ** 2)
            covMx[(i,1,1)] = RRoverlapconv(bigG.T, covMx[(i,1,1)]) - Ds[i] ** 2 + cls._ORIENT_NOISE

            # Get determinant of covariance matrix, which is the volume of the
            # covariance ellipse
            detIm = covMx[(i,0,0)] * covMx[(i,1,1)] - covMx[(i,0,1)] ** 2
            # Take the square root considering variance is squared, and the square
            # root again, since this is the area and the contrast measure is a "length"
            orientation_clutter_levels[i] = detIm ** (1/4)

        # Compute orientation clutter map   
        orientation_clutter_map = cls._collapse(orientation_clutter_levels)
        return orientation_clutter_map
    

    
    # Public methods
    @classmethod
    def execute_metric(
        cls, gui_image: str, gui_type: int = GUI_TYPE_DESKTOP
    ) -> Optional[List[Union[int, float, str]]]:
        """
        Execute the metric.

        Args:
            gui_image: GUI image (PNG) encoded in Base64

        Kwargs:
            gui_type: GUI type, desktop = 0 (default), mobile = 1

        Returns:
            Results (list of measures)
            - Subband Entropy (float)
        """
        # Create PIL image
        img: Image.Image = Image.open(BytesIO(base64.b64decode(gui_image)))

        # Convert image from ??? (e.g., RGBA) to RGB color space
        img_rgb: Image.Image = img.convert("RGB")

        # Get NumPy array
        img_rgb_nparray: np.ndarray = np.array(img_rgb)

        # Convert image into the perceptually-based CIELab color space.
        lab = rgb2lab(img_rgb_nparray)
        lab_float = lab.astype(np.float32)
        
        # Split image to luminance(L) and the chrominance(a,b) channels
        L = lab_float[:,:,0]
        a = lab_float[:,:,1]
        b = lab_float[:,:,2]

        
        # Get Gaussian pyramids (one for each of L,a,b)
        pyr = pt.pyramids.GaussianPyramid(L, height=cls._NUM_LEVELS)
        cls._L_pyr = pyr.pyr_coeffs
        pyr = pt.pyramids.GaussianPyramid(a, height=cls._NUM_LEVELS)
        cls._a_pyr = pyr.pyr_coeffs
        pyr = pt.pyramids.GaussianPyramid(b, height=cls._NUM_LEVELS)
        cls._b_pyr = pyr.pyr_coeffs

        
        # compute the color, contrast and orientation clutters
        color_clutter_map = cls._color_clutter()
        contrast_clutter_map = cls._contrast_clutter()
        orientation_clutter_map = cls._orientation_clutter()


        # Computes Feature Congestion measure of visual clutter
        clutter_map_fc = color_clutter_map / cls._COLOR_COEF \
        + contrast_clutter_map / cls._CONTRAST_COEF \
        + orientation_clutter_map / cls._ORIENT_COEF

        clutter_scalar_fc = np.mean(clutter_map_fc ** cls._MINKOWSKI_ORDER) ** (1 / cls._MINKOWSKI_ORDER) #element wise
        
        
        # Output Image: ndarray format
        output_image_fc = normlize(clutter_map_fc)
        
        return [
            clutter_scalar_fc,
        ]
