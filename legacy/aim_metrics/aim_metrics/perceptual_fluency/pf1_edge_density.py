##########################
# Clutter - Edge Density #
##########################
#
#   V1.0
#   29/05/2017
#
#   Implemented by:
#   Thomas Langerak
#   (hello@thomaslangerak.nl)
#
#   Based on code by:
#   Yuxi Zhu
#   (zhuyuxi1990@gmail.com)
#
#   Supervisor:
#   Antti Oulasvirta
#
#   This work was funded by Technology Industries of Finland in a three-year
#   project grant on self-optimizing web services. The principal investigator
#   is Antti Oulasvirta of Aalto University (antti.oulasvirta@aalto.fi)
#
###########
# Summary #
###########
#
#   Mack and Oliva suggested Edge Density as a metric for clutter. This is the ratio of how many pixels are regard as
#   an edge compared to the total number of pixels in the image. Miniukovich and De Angeli found it to have a clear
#   indication of clutter, also Rosenholtz et al. did find any relevance. However noted that the lack of colour variance
#   decreases the accuracy compared to Feature Congestion.
#
#############
# Technical #
#############
#
#   Inputs: JPG image (base64)
#   Returns: List of 1 item: Edge Density (float)
#
##############
# References #
##############
#
#   1.  Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.
#       Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems - CHI '15, (2015).
#
#   2.  Rosenholtz, R., Li, Y. and Nakano, L. Measuring visual clutter. Journal of Vision 7, 2 (2007), 17.
#
##############
# Change Log #
##############
#
###############
# Bugs/Issues #
###############
#
#   Sigma from original paper in the Canny is not taken into account.
#
import cv2
from skimage import util, color
import numpy as np
import base64
from PIL import Image
from io import BytesIO


def execute(b64):
    b64 = base64.b64decode(b64)
    b64 = BytesIO(b64)
    img = Image.open(b64)
    img= np.array(img)
    img_la = color.rgb2gray(img)
    img_la = util.img_as_ubyte(img_la)

    # 0.11 and 0.27, sigma = 1,     from Measuring visual clutter
    # See sigma here: https://dsp.stackexchange.com/questions/4716/differences-between-opencv-canny-and-matlab-canny
    img_la = cv2.GaussianBlur(img_la, (7, 7), 1)
    cd = cv2.Canny(img_la, 0.11, 0.27)
    total = cd.shape[0] * cd.shape[1] # Total number of pixels
    number_edges = np.count_nonzero(cd) # Number of edge pixels
    contour_density = float(number_edges) / float(total) # Ratio

    result = [contour_density]

    return result
