##################################
# Color Range - Dynamic Clusters #
##################################
#
#   V1.0
#   29/05/2017
#
#   Implemented by:
#   Thomas Langerak
#   (hello@thomaslangerak.nl)
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
#   This is the standard deviation of luminance over all pixels. It has been proven to not be statically relevant for
#   the perceived colour variance of a webpage.
#
#############
# Technical #
#############
#
#   Inputs: JPG image (base64)
#   Returns: List of 1 item: Standard Deviation in Luminance (float)
#
##############
# References #
##############
#
#   1.  Miniukovich, A., De Angeli A.. Quantification of Interface Visual Complexity. In the 2014 International
#       Working Conference on Advanced Visual Interfaces (2014), ACM, 153-160.
#
##############
# Change Log #
##############
#
###############
# Bugs/Issues #
###############
#
from skimage import util
import numpy as np
import base64
from PIL import Image
from io import BytesIO


def execute(b64):
    b64 = base64.b64decode(b64)
    b64 = BytesIO(b64)
    img = Image.open(b64)
    img = np.array(img)
    img = util.img_as_ubyte(img)
    img = img.reshape(-1, 3)
    img = [tuple(l) for l in img]

    lum = []
    for pixel in img:
        # Based on: https://en.wikipedia.org/wiki/Luma_(video)
        y = 0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2]
        lum.append(y)

    result = np.std(lum)

    return [result]
