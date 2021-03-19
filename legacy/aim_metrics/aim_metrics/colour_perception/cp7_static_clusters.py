##################################
# Color Range - Dynamic Clusters #
##################################
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
#   The number of static 32-sized color clusters (the sub-cube edge size of clusters is 32 values out of possible 256,
#   per each RGB channel). Only clusters containing more than 5 values are counted. It is significant factor for
#   dominant colours and clutter, but not for colour variance. CR3 is proven to be more accurate, though also more
#   computational complex.
#
#############
# Technical #
#############
#
#   Inputs: JPG image (base64)
#   Returns: List of 1 item: Number of Clusters (int)
#
##############
# References #
##############
#
#   1.  Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.
#       Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems - CHI '15, (2015).
#
#   2.  Miniukovich, A., De Angeli A.. Quantification of Interface Visual Complexity. In the 2014 International
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
import collections
import math
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

    # Get unique colours and their frequencies
    # Divide rgb spectrum (0-255) to a 32x32x32 matrix
    hist = collections.Counter(img)
    hist = hist.items()
    cluster = np.zeros((32, 32, 32))
    for x in range(len(hist)):
        rc = int(math.ceil((hist[x][0][0] / 8) + 1)) - 1
        gc = int(math.ceil((hist[x][0][1] / 8) + 1)) - 1
        bc = int(math.ceil((hist[x][0][2] / 8) + 1)) - 1
        cluster[rc, gc, bc] += hist[x][1]

    # The amount of cells that have more than 5 entries
    result = (cluster > 5).sum()

    return [result]
