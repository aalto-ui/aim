#####################################
# Color Range - Hassler & Susstrunk #
#####################################
#
#   V1.0
#   29/05/2017
#
#   Implemented by:
#   Yuxi Zhu (matlab) & Thomas Langerak (converted to python)
#   (zhuyuxi1990@gmail.com) & (hello@thomaslangerak.nl)
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
#   This metric was proposed by Hasler and Susstrunk as a more computational efficient alternative to CR3-CR6.
#   This metric is proven to have a very high correspondence to the users perception (95%). It relies on the RGYB color
#   spectrum and mainly looks at the average standard deviation for all value. The higher the STD is, the more colourful
#   the image is perceived. The nested loop however make it more computational heavy than it was originally intended.
#   Also it should be noted that this does not the Hue into account, which has been proven to be a significant factor.
#
#############
# Technical #
#############
#
#   Inputs: JPG image (base64)
#   Returns: List of 7 items: Mean Distribution (Red-Green) (float), Standard Deviation Distribution (Red-Green) (float), Mean Distribution (Yellow-Blue) (float), Standard Deviation Distribution (Yellow-Blue) (float), Mean Distribution (RGYB) (float), Standard Deviation Distribution (RGYB) (float), Colorfulness (float)
#
##############
# References #
##############
#
#   1.  Hasler, D. and Susstrunk, S. Measuring Colourfuness in Natural Images. (2003).
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
    img= np.array(img)
    img = util.img_as_ubyte(img)
    img = img.reshape(-1, 3)
    img = [tuple(l) for l in img]

    rg = []
    yb = []
    for item in img:
        [r, g, b] = [int(item[0]), int(item[1]), int(item[2])]
        # These formulae are proposed in Hasler, D. and Susstrunk, S. Measuring Colourfuness in Natural Images. (2003)
        rg.append(np.abs(r - g))
        yb.append(np.abs((0.5 * (r + g)) - b))

    meanRG = np.mean(rg)
    stdRG = np.std(rg)
    meanYB = np.mean(yb)
    stdYB = np.std(yb)
    meanRGYB = np.sqrt(meanRG ** 2 + meanYB ** 2)
    stdRGYB = np.sqrt(stdRG ** 2 + stdYB ** 2)

    # Proposed in the same paper
    colourfulness = stdRGYB + 0.3 * meanRGYB

    result = [meanRG, stdRG, meanYB, stdYB, meanRGYB, stdRGYB, colourfulness]

    return result
