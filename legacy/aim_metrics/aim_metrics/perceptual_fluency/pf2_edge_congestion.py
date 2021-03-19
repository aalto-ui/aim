################################
# Complexity - Edge Congestion #
################################
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
#   (Taken from 2)
#   Discriminating and tracing a line in a line congestion situation can be problematic. This issue often emerges in the
#   domain of large-graph visualization. Wong et al. [41] stated the problem: 'the density of edges is so great that
#   they obscure nodes, individual edges and even visual information beneath the graph'. They also proposed an
#   interactive solution to edge congestion - in graphs the edges were bent away from users' point of attention without
#   changing the number of nodes or edges. A more sophisticated discussion of edge congestion comes from the research on
#   crowding and is grounded on the notion of critical spacing - the distance between objects at which object perception
#   starts to degrade [16]. For example, the crowding model of visual clutter [36] uses eccentricity-based critical
#   spacing to account for information loss in peripheral visual field. However, the accompanying algorithm accounts
#   simultaneously for both visual clutter and edge congestion, and might need reconfiguration to account for edge
#   congestion only.
#
#############
# Technical #
#############
#
#   Inputs: PNG image (base64)
#   Returns: List of 1 item: Edge Congestion (float)
#
##############
# References #
##############
#
#   1.  Levi, D. Crowding. An essential bottleneck for object recognition: A mini-review. Vision Research 48, 5 (2008),
#   635-654.
#
#   2.  Miniukovich, A. and De Angeli, A. Quantification of interface visual complexity. Proceedings of the 2014
#   International Working Conference on Advanced Visual Interfaces - AVI '14, (2014).
#
#   3.  van den Berg, R., Cornelissen, F. and Roerdink, J. A crowding model of visual clutter. Journal of Vision 9, 4
#   (2009), 24-24.
#
#   4.  Wong, N., Carpendale, S., and Greenberg, S. EdgeLens: 2003. An Interactive Method for Managing Edge Congestion
#   in Graphs. IEEE Symposium on Information Visualization (October 19-21, 2003), 51-58.
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
import math
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
    height, width, depth = img.shape
    borders = np.zeros((img.shape[0], img.shape[1]), dtype=np.int)

    # Do edge detection. create_border return 0 or 255 depending on the difference with neigboring pixels
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            borders[y][x] = create_border(img, borders, y, x)

    count_edge = 0
    count_uncongested = 0
    threshold = 4 # Paper says 20, this is insane. The amount of pixels a person needs to differentiate between two elements

    # Create numpy array from list
    borders = np.array(borders)

    # Assumme screen border is always a border
    for x in range(threshold, width - threshold):
        for y in range(threshold, height - threshold):
            if borders[y][x] == 255:
                count_edge += 1

                # Sum left, right, up, down for number of pixels in threshold
                arr_right = borders[y, x + 1:x + threshold]
                sum_right = sum(arr_right)
                arr_left = borders[y, x - threshold:x - 1]
                sum_left = sum(arr_left)
                arr_up = borders[y + 1:y + threshold, x]
                sum_up = sum(arr_up)
                arr_down = borders[y - threshold:y - 1, x]
                sum_down = sum(arr_down)

                # If the sum is zero, it means there are no other pixels nearby. It needs to be in all directions non-0
                # for a pixel to be congested
                if sum_right == 0 or sum_left == 0 or sum_up == 0 or sum_down == 0:
                    count_uncongested += 1

    try:
        count_congested = count_edge - count_uncongested
        result = float(count_congested) / float(count_edge)
    except ZeroDivisionError:
        result = 0

    return [result]


def create_border(img, borders, y, x):
    r1 = int(img[y][x][0])
    g1 = int(img[y][x][1])
    b1 = int(img[y][x][2])

    points_2 = [
        [y, x + 1],
        [y, x - 1],
        [y + 1, x],
        [y - 1, x]
    ]

    ret = 0
    for n in range(4):
        x2 = points_2[n][1]
        y2 = points_2[n][0]

        r2 = int(img[y2][x2][0])
        g2 = int(img[y2][x2][1])
        b2 = int(img[y2][x2][2])

        dst_r = math.fabs(r2 - r1)
        dst_g = math.fabs(g2 - g1)
        dst_b = math.fabs(b2 - b1)

        if (dst_r > 50 or dst_b > 50 or dst_g > 50) and borders[y2][x2] == 0:
            ret = 255
            break

    return ret
