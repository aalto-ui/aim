#######################################
# Complexity - Figure-Ground Contrast #
#######################################
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
#   (Taken from 2)
#   Psychologists often use luminance or color contrast to manipulate perceptual fluency. For example, Reber et al.
#   showed participants phrases in green or red on a white background (high contrast condition), and in yellow or
#   light-blue color on a white background (low contrast condition). The high-contrast phrases were judged as true
#   facts significantly above the chance level, whereas the low-contrast phrases were not. The authors attributed
#   it to the difference in reading difficulty, and thus, processing fluency. Similarly, Reber et al. showed
#   participants 70% black (high contrast) and 30% black (low contrast) words on a white background. In the high
#   contrast scenario, the participants were significantly faster at detecting and recognizing words. Hall et al.
#   explored text readability of web pages, and found white-black text-background combinations to be more readable
#   than light- and dark-blue, or cyan-black combinations. However, the studies above did not measure contrast
#   automatically.
#
#############
# Technical #
#############
#
#   Inputs: PNG image (base64)
#   Returns: List of 1 item: Figure-Ground Contrast (float)
#
##############
# References #
##############
#
#   1.  Hall, R. and Hanna, P. The impact of web page text-background colour combinations on readability, retention,
#       aesthetics and behavioural intention. Behaviour & Information Technology 23, 3 (2004), 183-195.
#
#   2.  Miniukovich, A. and De Angeli, A. Quantification of interface visual complexity. Proceedings of the 2014
#       International Working Conference on Advanced Visual Interfaces - AVI '14, (2014).
#
#   3.  Reber, R., Winkielman, P. and Schwarz, N. Effects of Perceptual Fluency on Affective Judgments. Psychological
#       Science 9, 1 (1998), 45-48.
#
#   4.  Reber, R., Wurtz, P. and Zimmermann, T. Exploring 'fringe' consciousness: The subjective experience of
#       perceptual fluency and its objective bases. Consciousness and Cognition 13, 1 (2004), 47-60.
#
##############
# Change Log #
##############
#
###############
# Bugs/Issues #
###############
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

    # Get the number of edge pixels per level. See 1
    edge_per_level = []
    for x in range(1, 8):
        # Blur is needed: https://dsp.stackexchange.com/questions/4716/differences-between-opencv-canny-and-matlab-canny
        img_la = cv2.GaussianBlur(img_la, (7, 7), 2)
        cd = cv2.Canny(img_la, x * 0.04, x * 0.1) # Higher level from 0.1-0.7, lower level is 40% of higher
        number_edges = np.count_nonzero(cd) # Number of edge pixels
        edge_per_level.append(number_edges)

    difference = []
    
    # Calculate the difference between each level
    for x in range(len(edge_per_level) - 1):
        difference.append(edge_per_level[x] - edge_per_level[x + 1])

    # Give weight per level. Lower levels have more impact so higher weight
    weighted_sum = 0
    for x in range(len(difference)):
        weighted_sum += difference[x] * (1.0 - ((x - 1.0) / 6.0))

    # Normalize
    try:
        result = [weighted_sum / (edge_per_level[0] - edge_per_level[5])]
    except ZeroDivisionError:
        result = [0]

    return result
