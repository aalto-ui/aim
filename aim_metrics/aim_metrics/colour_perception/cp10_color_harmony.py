############################################
# Color Harmony - Distance to Color Scheme #
############################################
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
#   Harmonic colors are sets of colors that are aesthetically pleasing
#   in terms of human visual perception. The notion of color harmony in this work is based on the schemes
#   developed by Matsuda [Matsuda 1995; Tokumaru et al. 2002], which descend from Itten's notions of
#   harmony [Itten 1960], widely accepted in applicable fields involving colors. (See paper for al references)
#
#   This paper uses distance to colourschemes to "enhance" photographs. This is not proven for user interfaces.
#   There, though it is common practice in design their is limited scientific evidence in the paper the formulated
#   this formalism.
#
#   Also note that colourscheme X will most likely will be the closest in distance. This does not mean it is the best
#   this is due how X is defined. (It covers a large part of the hue circle and is spaced in such a way that the max
#   distance to a border is relatively small compared to other colour schemes.
#
#   For an overview of what the schemes look like, please take a look at the paper.
#
#############
# Technical #
#############
#
#   Inputs: File path to image
#   Returns: 8 item float list of distance to colour schemes
#       order: i, V, L, L_inverse, I, T, X, Y
#
##############
# References #
##############
#
#   1.  Cohen-Or, D., Sorkine, O., Gal, R., Leyvand, T. and Xu, Y. Color harmonization.
#       ACM Transactions on Graphics 25, 3 (2006), 624.
#
##############
# Change Log #
##############
#
###############
# Bugs/Issues #
###############
#
from skimage import io, util, transform, color
import math
import collections
import numpy as np
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt


def execute(b64):
    # Input, colour reduction, get rid of unnescessary data, scale down, and get it in the correct structure
    b64 = base64.b64decode(b64)
    b64 = BytesIO(b64)
    img = Image.open(b64)
    img = util.img_as_ubyte(img)
    img = img / 255.
    img = color.rgb2hsv(img)
    img = img.reshape(-1, 3)
    img = np.delete(img, 2, 1)
    img = [tuple(l) for l in img]

    # Find all unique h, s combinations
    hist = collections.Counter(img)
    hist = hist.items()
    
    # Get everything in their own array
    h = []
    s = []
    frequency = []

    for x in range(len(hist)):
        if hist[x][1] > 5: # Find some argument for this, most papers regarding this topic use 5
            h.append(int(hist[x][0][0] * 360))
            s.append(hist[x][0][1])
            frequency.append(hist[x][1])

    dist_i_all = []
    dist_V_all = []
    dist_L_inverse_all = []
    dist_L_all = []
    dist_I_all = []
    dist_T_all = []
    dist_X_all = []
    dist_Y_all = []

    # For every angle in the colour spectra
    for alpha in range(1, 361):
        dist_i = 0.0
        dist_V = 0.0
        dist_L = 0.0
        dist_L_inverse = 0.0
        dist_I = 0.0
        dist_T = 0.0
        dist_Y = 0.0
        dist_X = 0.0

        # For every unique h,s combination
        for pixel in range(len(h)):
            # Calculated to total distance of an image to each colour space
            dist_i += borders_i(alpha, h[pixel], s[pixel]) * frequency[pixel]
            dist_V += borders_V(alpha, h[pixel], s[pixel]) * frequency[pixel]
            dist_L += borders_L(alpha, h[pixel], s[pixel]) * frequency[pixel]
            dist_L_inverse += borders_L_inverse(alpha, h[pixel], s[pixel]) * frequency[pixel]
            dist_I += borders_I(alpha, h[pixel], s[pixel]) * frequency[pixel]
            dist_T += borders_T(alpha, h[pixel], s[pixel]) * frequency[pixel]
            dist_X += borders_X(alpha, h[pixel], s[pixel]) * frequency[pixel]
            dist_Y += borders_Y(alpha, h[pixel], s[pixel]) * frequency[pixel]

        # Add the total distance to the list
        dist_i_all.append(dist_i)
        dist_V_all.append(dist_V)
        dist_L_inverse_all.append(dist_L_inverse)
        dist_L_all.append(dist_L)
        dist_I_all.append(dist_I)
        dist_T_all.append(dist_T)
        dist_X_all.append(dist_X)
        dist_Y_all.append(dist_Y)

    # Find the shortest distance for each colour spectrum
    distances = [min(dist_i_all), min(dist_V_all), min(dist_L_all), min(dist_L_inverse_all), min(dist_I_all),
                 min(dist_T_all), min(dist_X_all), min(dist_Y_all)]

    # Find the angle of at which that spectrum occurce
    alphas = [dist_i_all.index(distances[0]), dist_V_all.index(distances[1]), dist_L_all.index(distances[2]),
              dist_L_inverse_all.index(distances[3]), dist_I_all.index(distances[4]),
              dist_T_all.index(distances[5]), dist_X_all.index(distances[6]), dist_Y_all.index(distances[7])]


    # Create a list of hues of 360 of occurences. This is mainly useful for visualizing stuff
    pixels = []
    for i in range(0, 360):
        if i in h:
            pixels.append(frequency[h.index(i)])
        else:
            pixels.append(0)


    results_all = [distances, alphas, pixels]

    #   plt.plot(dist_i_all, 'r', linewidth=1.0, label="i")
    #   plt.plot(dist_V_all, 'g', linewidth=1.0, label="V")
    #   plt.plot(dist_L_all, 'b', linewidth=1.0, label="L")
    #   plt.plot(dist_L_inverse_all, 'y', linewidth=1.0, label="L Inverse")
    #   plt.plot(dist_I_all, 'm', linewidth=1.0, label="I")
    #   plt.plot(dist_T_all, 'k', linewidth=1.0, label="T")
    #   plt.plot(dist_X_all, 'c', linewidth=1.0, label="X")
    #   plt.plot(dist_Y_all, '#ee7600', linewidth=1.0, label="Y")
    #   plt.ylabel('distance')
    #   plt.xlabel('alpha')
    #   plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #   plt.show()

    # get the minimal of all. Maybe at alpha to it?
    # score = min(results_all)
    # scheme = results_all.index(score)
    # result = [score, scheme]
    return results_all


# Below here we define all formulas to calculate length to each border in each spectra. This is based on:
# https://igl.ethz.ch/projects/color-harmonization/harmonization.pdf
PI = math.pi
TAU = 2 * PI


# https://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles
def smallest_angle(x, y):
    a = (x - y) % TAU
    b = (y - x) % TAU
    return -a if a < b else b


def borders_i(alpha, pixel_angle, saturation): # Input degrees, hue degrees
    # Get the borders of all areas and translate to radians
    border = [math.radians((alpha - 18 / 2) % 360), math.radians((alpha + 18 / 2) % 360)]
    pixel_angle = math.radians(pixel_angle)
    
    # Get the distance to each border
    distance = []
    for x in range(len(border)):
        distance.append(abs(smallest_angle(border[x], pixel_angle)))
    distance_alpha = abs(smallest_angle(pixel_angle, math.radians(alpha)))

    if distance_alpha <= math.radians(18 / 2):
        result = 0.0

        # else it is the distance to the closest border
    else:
        result = min(distance) * saturation

        #   print math.radians(alpha), math.radians(18 / 2), border[0], border[1], pixel_angle, distance[0], distance[1], distance_alpha, result
    return result


def borders_V(alpha, pixel_angle, saturation):
    # Get the borders of all areas and translate to radians
    border = [math.radians((alpha - 93.6 / 2) % 360), math.radians((alpha + 93.6 / 2) % 360)]
    pixel_angle = math.radians(pixel_angle)

    # Get the distance to each border
    distance = []
    for x in range(len(border)):
        distance.append(abs(smallest_angle(border[x], pixel_angle)))
    distance_alpha = abs(smallest_angle(pixel_angle, math.radians(alpha)))
    if distance_alpha < math.radians(93.6 / 2):
        result = 0
    # else it is the distance to the closest border
    else:
        result = min(distance) * saturation

    return result


def borders_L(alpha, pixel_angle, saturation):
    # Get the borders of all areas and translate to radians
    border = [math.radians((alpha - 93.6 / 2) % 360), math.radians((alpha + 93.6 / 2) % 360),
              math.radians((alpha + 90 - 18 / 2) % 360), math.radians((alpha + 90 + 18 / 2) % 360)]
    
    # Get the distance to each border
    pixel_angle = math.radians(pixel_angle)
    distance = []
    for x in range(len(border)):
        distance.append(abs(smallest_angle(border[x], pixel_angle)))
    distance_alpha = abs(smallest_angle(pixel_angle, math.radians(alpha)))
    distance_alpha_2 = abs(smallest_angle(pixel_angle, (math.radians((alpha + 90) % 360))))

    if distance_alpha <= math.radians(93.6 / 2) or distance_alpha_2 <= math.radians(18 / 2):
        result = 0
    # else it is the distance to the closest border
    else:
        result = min(distance) * saturation

    return result


def borders_L_inverse(alpha, pixel_angle, saturation):
    # Get the borders of all areas and translate to radians
    border = [math.radians((alpha - 93.6 / 2) % 360), math.radians((alpha + 93.6 / 2) % 360),
              math.radians((alpha - 90 - 18 / 2) % 360), math.radians((alpha - 90 + 18 / 2) % 360)]
    # Get the distance to each border
    pixel_angle = math.radians(pixel_angle)
    distance = []

    for x in range(len(border)):
        distance.append(abs(smallest_angle(border[x], pixel_angle)))
    distance_alpha = abs(smallest_angle(pixel_angle, math.radians(alpha)))
    distance_alpha_2 = abs(smallest_angle(pixel_angle, (math.radians((alpha - 90) % 360))))

    if distance_alpha <= math.radians(93.6 / 2) or distance_alpha_2 <= math.radians(18 / 2):
        result = 0
    # else it is the distance to the closest border
    else:
        result = min(distance) * saturation

    return result


def borders_I(alpha, pixel_angle, saturation):
    # Get the borders of all areas and translate to radians
    border = [math.radians((alpha - 18 / 2) % 360), math.radians((alpha + 18 / 2) % 360),
              math.radians((alpha + 180 - 18 / 2) % 360), math.radians((alpha + 180 + 18 / 2) % 360)]
    pixel_angle = math.radians(pixel_angle)
    
    # Get the distance to each border
    distance = []
    for x in range(len(border)):
        distance.append(abs(smallest_angle(border[x], pixel_angle)))
    distance_alpha = abs(smallest_angle(pixel_angle, math.radians(alpha)))
    distance_alpha_2 = abs(smallest_angle(pixel_angle, (math.radians(alpha + 180 % 360))))
    if distance_alpha <= math.radians(18 / 2) or distance_alpha_2 <= math.radians(18 / 2):
        result = 0
    # else it is the distance to the closest border
    else:
        result = min(distance) * saturation

    return result


def borders_T(alpha, pixel_angle, saturation):
    # Get the borders of all areas and translate to radians
    border = [math.radians((alpha - 180 / 2) % 360), math.radians((alpha + 180 / 2) % 360)]
    pixel_angle = math.radians(pixel_angle)

    # Get the distance to each border
    distance = []
    for x in range(len(border)):
        distance.append(abs(smallest_angle(border[x], pixel_angle)))
    distance_alpha = abs(smallest_angle(pixel_angle, math.radians(alpha)))

    if distance_alpha <= math.radians(180 / 2):
        result = 0
    # else it is the distance to the closest border
    else:
        result = min(distance) * saturation

    return result


def borders_Y(alpha, pixel_angle, saturation):
    # Get the borders of all areas and translate to radians
    border = [math.radians((alpha - 93.6 / 2) % 360), math.radians((alpha + 93.6 / 2) % 360),
              math.radians((alpha + 180 - 18 / 2) % 360), math.radians((alpha + 180 + 18 / 2) % 360)]
    pixel_angle = math.radians(pixel_angle)
    
    # Get the distance to each border
    distance = []
    for x in range(len(border)):
        distance.append(abs(smallest_angle(border[x], pixel_angle)))
    distance_alpha = abs(smallest_angle(pixel_angle, math.radians(alpha)))
    distance_alpha_2 = abs(smallest_angle(pixel_angle, (math.radians((alpha + 180) % 360))))
    if distance_alpha <= math.radians(93.6 / 2) or distance_alpha_2 <= math.radians(18 / 2):
        result = 0
    # else it is the distance to the closest border
    else:
        result = min(distance) * saturation

    return result


def borders_X(alpha, pixel_angle, saturation):
    # Get the borders of all areas and translate to radians
    border = [math.radians((alpha - 93.6 / 2) % 360), math.radians((alpha + 93.6 / 2) % 360),
              math.radians((alpha + 180 - 93.6 / 2) % 360), math.radians((alpha + 180 + 93.6 / 2) % 360)]
    pixel_angle = math.radians(pixel_angle)

    # Get the distance to each border
    distance = []
    for x in range(len(border)):
        distance.append(abs(smallest_angle(border[x], pixel_angle)))
    distance_alpha = abs(smallest_angle(pixel_angle, math.radians(alpha)))
    distance_alpha_2 = abs(smallest_angle(pixel_angle, (math.radians((alpha + 180) % 360))))
    if distance_alpha <= math.radians(93.6 / 2) or distance_alpha_2 <= math.radians(93.6 / 2):
        result = 0
    # else it is the distance to the closest border
    else:
        result = min(distance) * saturation

    return result
