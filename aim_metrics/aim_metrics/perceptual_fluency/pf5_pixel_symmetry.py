###############################
# Complexity - Pixel Symmetry #
###############################
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
#   One of the Gestalt principles, mirror symmetry - the similarity of an object reflection across a straight axis -
#   was claimed to improve interface design. However, quantifying symmetry might be problematic in HCI. Psychologists
#   mainly studied mirror symmetry of relatively simple objects, such as dot and line patterns, or human faces.
#
#############
# Technical #
#############
#
#   Inputs: PNG image (base64)
#   Returns: List of 1 item: Normalized Symmetry (float)
#
##############
# References #
##############
#
#   1.  Miniukovich, A. and De Angeli, A. Quantification of interface visual complexity. Proceedings of the 2014
#       International Working Conference on Advanced Visual Interfaces - AVI '14, (2014).
#
##############
# Change Log #
##############
#
###############
# Bugs/Issues #
###############
#
#   Limiting the number of pixels is not working yet.
#
import cv2
from skimage import util, color
import numpy as np
import base64
from PIL import Image
from io import BytesIO


def get_pixels_in_radius(x, y, width, height, radius):
    # Get x border
    if x < radius:
        rad_x_left = -x
        rad_x_right = radius
    elif width - x < radius:
        rad_x_right = 1 * (width - x)
        rad_x_left = -radius
    else:
        rad_x_left = -radius
        rad_x_right = radius

    # Get y borders
    if y < radius:
        rad_y_top = -y
        rad_y_bottom = radius
    elif height - y < radius:
        rad_y_bottom = 1 * (height - y)
        rad_y_top = -radius
    else:
        rad_y_top = -radius
        rad_y_bottom = radius

    pixels = []
    for m in range(rad_x_left, rad_x_right):
        for n in range(rad_y_top, rad_y_bottom):
            if m != 0 or n != 0:
                pixel = [x + m, y + n]
                pixels.append(pixel)

    return pixels


def execute(b64):
    b64 = base64.b64decode(b64)
    b64 = BytesIO(b64)
    img = Image.open(b64)
    img = np.array(img)
    img_la = color.rgb2gray(img)
    img_la = util.img_as_ubyte(img_la)

    # See sigma here: https://dsp.stackexchange.com/questions/4716/differences-between-opencv-canny-and-matlab-canny
    img_la = cv2.GaussianBlur(img_la, (7, 7), 2)
    edges = cv2.Canny(img_la, 0.11, 0.27)

    height, width = edges.shape

    # Set all pixels in radius of an edge pixel to 0
    # This is not going good yet
    radius = 3
    all_key = 0
    for y in range(height):
        for x in range(width):
            if edges[y][x] != 0:
                all_key += 1
                pixels_in_radius = get_pixels_in_radius(x, y, width, height, radius)
                for pixel in pixels_in_radius:
                    edges[pixel[1], pixel[0]] = 0

    img = Image.fromarray(edges, 'L')
    # img.show()
    symmetry_radius = 4
    
    # Check vertical symmetry
    sym_key = 0
    for y in range(height):
        for x in range(width / 2):
            if edges[y][x] != 0:
                vertical_pixels = get_pixels_in_radius(width - x, y, width, height, symmetry_radius)
                horizontal_pixels = get_pixels_in_radius(x, height - y, width, height, symmetry_radius)

                for pixel in vertical_pixels:
                    if edges[int(pixel[1]), int(pixel[0])] != 0:
                        sym_key += 1
                        break

                for pixel in horizontal_pixels:
                    if edges[int(pixel[1]), int(pixel[0])] != 0:
                        sym_key += 1
                        break

    try:
        sym_normalized = (float(sym_key) / float(all_key)) * ((float((all_key - 1) * symmetry_radius) / float(width * height)) ** -1)
    except ZeroDivisionError:
        sym_normalized = 0

    return [sym_normalized]
