############################
# Color Range - HSV Unique #
############################
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
#   Hasler & Susstrunk validated this metric in their paper. It looks at the number of unique values in the HSV colour
#   space.
#
#############
# Technical #
#############
#
#   Inputs: JPG image (base64)
#   Returns: List of 4 items: Number of Unique HSV (int), Number of Unique Hue (int), Number of Unique Saturation (int), Number of Unique Value (int)
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
from skimage import color, util
import collections
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
    img = color.rgb2hsv(img)
    img = img.reshape(-1, 3)
    img = [tuple(l) for l in img]

    hist = collections.Counter(img)
    hist = hist.items()

    hsv_unique = []
    count = []
    h = []
    s = []
    v = []

    for x in range(len(hist)):
        add = [hist[x][0][0], hist[x][0][1], hist[x][0][2]]
        hsv_unique.append(add)
        count.append(hist[x][1])
        h.append(hist[x][0][0])
        s.append(hist[x][0][1])
        v.append(hist[x][0][2])

    # Get all unique values, still has all counts (so no minimal occurence). This probably needs some changing in the future
    h_unique = np.unique(h)
    s_unique = np.unique(s)
    v_unique = np.unique(v)

    new_hsv = []

    # Only often enough occuring values for hsv
    for x in range(len(hsv_unique)):
        if count[x] > 5:
            new_hsv.append(hsv_unique[x])


    result = [len(new_hsv), len(h_unique), len(s_unique), len(v_unique)]

    return result
