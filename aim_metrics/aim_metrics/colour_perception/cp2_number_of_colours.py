###################################
# Color Range - Number of Colours #
###################################
#
#   V1.1
#   15/10/2018
#
#   Implemented by:
#   Kseniia Palin & Markku Laine
#   (kseniia.palin@aalto.fi) & (markku.laine@aalto.fi)
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
#   The number of unique colours is an indication of colour variance according to (1). Every unique colour is counted.
#   If it occurs often enough (more than 5 times for a website, more than 2 for a smartphone application) it is taken
#   into account for the final count. It is important to notice that more colours on first thought might be bad. However
#   this metric is heavily prone to the amount of images on a website. Hence a simple photograph website, might sore
#   high on this scale.
#
#############
# Technical #
#############
#
#   Inputs: PNG image (base64), type (website=0/mobile=1) (int)
#   Returns: List of 1 item: Number of Colours (int)
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
import numpy as np
import base64
from PIL import Image
from io import BytesIO
import matplotlib.image as mpimg


def execute(b64, type):
    b64 = base64.b64decode(b64)
    b64 = BytesIO(b64)
    img = mpimg.imread(b64, format='PNG')
    img = img[:,:,:3]
    img = img.reshape(-1, 3)
    img = [tuple(l) for l in img]

    # Create histogram
    hist = collections.Counter(img)

    # Count the number of colors: only values that occur more than 5 (for web, type=0) or 2 (for mobile, type=1) times per image are counted
    min_threshold = 5 if type == 0 else 2 if type == 1 else 0
    count_rgb = [len({x : hist[x] for x in hist if hist[x] >= min_threshold })]

    return count_rgb
