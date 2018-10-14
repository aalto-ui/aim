# -------------------------------------------------------------------------------
# Name:        main
# Purpose:     Testing the package pySaliencyMap
#
# Author:      Akisato Kimura <akisato@ieee.org>
#
# Created:     May 4, 2014
# Copyright:   (c) Akisato Kimura 2014-
# Licence:     All rights reserved
# -------------------------------------------------------------------------------

##########################
# Clutter - Edge Density #
##########################
#
#   V1.0
#   29/05/2017
#
#   Implemented by:
#   Akisato Kimura (see vg1_license.txt)
#   (akisato@ieee.org)
#
###########
# Summary #
###########
#
#   Most models of visual search, whether involving overt eye movements or covert shifts of attention, are based on the
#   concept of a saliency map, that is, an explicit two-dimensional map that encodes the saliency or conspicuity of
#   objects in the visual environment. Competition among neurons in this map gives rise to a single winning location
#   that corresponds to the next attended target. Inhibiting this location automatically allows the system to attend
#   to the next most salient location. This code is made by Akisato Kimura and based on the paper by Itti and Koch.
#   In its essence it shows which objects in a picture are most attention grabbing.
#
#############
# Technical #
#############
#
#   Inputs: JPG image (base64)
#   Returns: List of 1 item: Saliency (base64)
#
##############
# References #
##############
#
#   1.  Kimura, A. pySaliencyMap. GitHub, 2017. https://github.com/akisato-/pySaliencyMap.
#
#   2.  Itti, L. and Koch, C. A saliency-based search mechanism for overt and covert shifts of visual attention.
#       Vision Research 40, 10-12 (2000), 1489-1506.
#
##############
# Change Log #
##############
#
###############
# Bugs/Issues #
###############
#
import StringIO
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pySaliencyMap


def execute(b64):
    plt.switch_backend('AGG')
    
    # Read
    b64 = base64.b64decode(b64)
    b64 = BytesIO(b64)
    img = Image.open(b64)
    img= np.array(img)
    
    # Initialize
    imgsize = img.shape
    img_width = imgsize[1]
    img_height = imgsize[0]
    sm = pySaliencyMap.pySaliencyMap(img_width, img_height)
    
    # Computation
    saliency_map = sm.SMGetSM(img)
    plt.imshow(saliency_map, 'gray')
    fig = plt.gcf()
    plt.axis('off')
    buffer = StringIO.StringIO()
    fig.savefig(buffer, format="PNG", bbox_inches='tight', pad_inches=0, transparent=True)
    result = base64.b64encode(buffer.getvalue())
    buffer.close()

    return [result]
