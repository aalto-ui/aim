###################################
# Color Range - Number of Colours #
###################################
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
#   Once segmentation is ready exclude images from the count.
#
from skimage import util
import collections
import numpy as np
import base64
from PIL import Image
from io import BytesIO


def execute(b64, type):
    try:
        b64 = base64.b64decode(b64)
        b64 = BytesIO(b64)
        img = Image.open(b64)
        img = np.array(img)
        img = util.img_as_ubyte(img)
        img = img.reshape(-1, 3) # FIX: breaks with some images
        img = [tuple(l) for l in img]

        # Create histogram
        hist = collections.Counter(img)
        hist = hist.items()

        rgb_unique = []
        count = []

        # Add rgb and frequency to list
        for x in range(len(hist)):
            add = [hist[x][0][0], hist[x][0][1], hist[x][0][2]]
            rgb_unique.append(add)
            count.append(hist[x][1])

        # The number of colors after color reduction: only values that occurred more than 5 (for web) or 2 (for mobile) times per image were counted
        occurence = [5, 2]

        # Count only the colours that occur often enough
        counter = 0
        for x in range(len(rgb_unique)):
            if count[x] >= occurence[type]:
                counter += 1

        count_rgb = [counter]
    except ValueError:
        count_rgb = [0]

    return count_rgb