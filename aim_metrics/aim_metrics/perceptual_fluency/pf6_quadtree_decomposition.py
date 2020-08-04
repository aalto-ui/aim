################################################
# Quadtree - Balance, Symmetry and Equilibrium #
################################################
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
#   The orginial paper [2] proposes 14 metrics for evaluating layout. Currently three are implemented
#   for the other 11 metrics a better segmentation is needed. (Preferably for these three aswell). The three
#   metrics are balance, symmetry and equilibrium.
#
#   Balance can be defined as the distribution of optical weight in a picture.
#   Optical weight refers to the perception that some objects appear heavier than
#   others. Larger objects are heavier, whereas small objects are lighter. Balance in
#   screen design is achieved by providing an equal weight of screen elements, left
#   and right, top and bottom.
#
#   Symmetry is axial duplication: a unit on one side of the centre line is exactly
#   replicated on the other side. Vertical symmetry refers to the balanced arrangement
#   of equivalent elements about a vertical axis, and horizontal symmetry
#   about a horizontal axis. Radial symmetry consists of equivalent elements
#   balanced about two or more axes that intersect at a central point. In two seperate studies
#   this metric has not proven to be significant.
#
#   Equilibrium is a stabilisation, a midway centre of suspension. Equilibrium
#   on a screen is accomplished through centring the layout itself. The centre of the
#   layout coincides with that of the frame.
#
#############
# Technical #
#############
#
#   Inputs: JPG image (base64)
#   Returns: List of 4 items: Balance (float), Symmetry (float), Equilibrium (float), Number of Leaves (int)
#
##############
# References #
##############
#
#   1.  Ngo, D., Teo, L. and Byrne, J. Modelling interface aesthetics. Information Sciences 152, (2003), 25-46.
#
#   2.  Zheng, X., Chakraborty, I., Lin, J. and Rauschenberger, R. Correlating Low-Level Image Statistics with Users'
#       Rapid Aesthetic and Affective Judgments of Web Pages. CHI 2009 ~ Understanding Information, (2009).
#
#   3.  Reinecke, K., Yeh, T. and Miratrix, L. et al. Predicting Users' First Impressions of Website Aesthetics With a
#       Quantification of Perceived Visual Complexity and Colorfulness. CHI, (2013).
#
##############
# Change Log #
##############
#
###############
# Bugs/Issues #
###############
#
#   Entropy is not correctly defined at the moment. See 3 and 1 for better definitions.
#
from skimage import util, color
import numpy as np
import base64
from PIL import Image
from io import BytesIO
import math
import cv2


## -------------- QT functions ---------------##
def balance(leaves, width, height):
    top = []
    right = []
    left = []
    bottom = []

    for leaf in leaves:
        if leaf[0] > width / 2:
            right.append(leaf)
        else:
            left.append(leaf)
        if leaf[1] > height / 2:
            bottom.append(leaf)
        else:
            top.append(leaf)

    w_left = 0.0
    w_top = 0.0
    w_bottom = 0.0
    w_right = 0.0
    center = [width / 2, height / 2]

    for leaf in top:
        area = leaf[2] * leaf[3]
        mid_point_leaf = [leaf[0] + leaf[2] / 2, leaf[1] + leaf[3] / 2]
        distance = abs(mid_point_leaf[0] - center[1])
        score = distance * area
        w_top += score
    for leaf in bottom:
        area = leaf[2] * leaf[3]
        mid_point_leaf = [leaf[0] + leaf[2] / 2, leaf[1] + leaf[3] / 2]
        distance = abs(mid_point_leaf[0] - center[1])
        score = distance * area
        w_bottom += score
    for leaf in left:
        area = leaf[2] * leaf[3]
        mid_point_leaf = [leaf[0] + leaf[2] / 2, leaf[1] + leaf[3] / 2]
        distance = abs(mid_point_leaf[1] - center[0])
        score = distance * area
        w_left += score
    for leaf in right:
        area = leaf[2] * leaf[3]
        mid_point_leaf = [leaf[0] + leaf[2] / 2, leaf[1] + leaf[3] / 2]
        distance = abs(mid_point_leaf[1] - center[0])
        score = distance * area
        w_right += score

    IB_left_right = (w_left - w_right) / max(abs(w_left), abs(w_right))
    IB_top_bottom = (w_top - w_bottom) / max(abs(w_top), abs(w_bottom))
    BM = 1 - float(abs(IB_top_bottom) + abs(IB_left_right)) / 2

    return BM


# Seems unreasonably high, this is the case in the paper as well however
def equilibrium(leaves, width, height):
    area = []
    dx = []
    dy = []
    for leaf in leaves:
        area.append(float(leaf[2]) * float(leaf[3]))
        dx.append(abs(float(leaf[0] + leaf[2] / 2) - float(width) / 2))
        dy.append(abs(float(leaf[1] + leaf[3] / 2) - float(height) / 2))

    sum_x = 0.0
    sum_y = 0.0
    for n in range(len(dx)):
        sum_x += area[n] * dx[n]
        sum_y += area[n] * dx[n]
    EM_x = (2 * sum_x) / (int(width) * len(leaves) * sum(area))
    EM_y = (2 * sum_y) / (int(height) * len(leaves) * sum(area))

    EM = 1 - float(abs(EM_x) + abs(EM_y)) / 2

    return EM


def symmetry(leaves, width, height):
    UL_leaves = []
    UR_leaves = []
    LL_leaves = []
    LR_leaves = []

    for leaf in leaves:
        if leaf[0] > width / 2 and leaf[1] < height / 2:
            UR_leaves.append(leaf)
        elif leaf[0] <= width / 2 and leaf[1] < height / 2:
            UL_leaves.append(leaf)
        elif leaf[0] > width / 2 and leaf[1] >= height / 2:
            LR_leaves.append(leaf)
        elif leaf[0] <= width / 2 and leaf[1] >= height / 2:
            LL_leaves.append(leaf)

    X_j = []
    Y_j = []
    H_j = []
    B_j = []
    T_j = []
    R_j = []

    all_leaves = [UL_leaves, UR_leaves, LL_leaves, LR_leaves]
    x_center = width / 2
    y_center = height / 2
    
    # With j being respectively: UL;UR,LL;LR
    for j in all_leaves:
        X_score = 0
        Y_score = 0
        H_score = 0
        B_score = 0
        T_score = 0
        R_score = 0
        for leaf in j:
            x_leaf = leaf[0] + leaf[2] / 2
            X_score += abs(x_leaf - x_center)
            y_leaf = leaf[1] + leaf[3] / 2
            Y_score += abs(y_leaf - y_center)
            H_score += leaf[3]
            B_score += leaf[2]
            T_score += abs(y_leaf - y_center) / abs(x_leaf - x_center)
            R_score += (((x_leaf - x_center) ** 2) + ((y_leaf - y_center) ** 2)) ** 0.5

        X_j.append(X_score)
        Y_j.append(Y_score)
        H_j.append(H_score)
        B_j.append(B_score)
        T_j.append(T_score)
        R_j.append(R_score)

    # Normalize
    X_j[:] = [x / max(X_j) for x in X_j]
    Y_j[:] = [y / max(Y_j) for y in Y_j]
    H_j[:] = [h / max(H_j) for h in H_j]
    B_j[:] = [b / max(B_j) for b in B_j]
    T_j[:] = [r / max(R_j) for r in R_j]
    R_j[:] = [t / max(T_j) for t in T_j]

    SYM_ver = (abs(X_j[0] - X_j[1]) + abs(X_j[2] - X_j[3]) + abs(Y_j[0] - Y_j[1]) + abs(Y_j[2] - Y_j[3]) + abs(
        H_j[0] - H_j[1]) + abs(H_j[2] - H_j[3]) + abs(B_j[0] - B_j[1]) + abs(B_j[2] - B_j[3]) + abs(
        T_j[0] - T_j[1]) + abs(T_j[2] - T_j[3]) + abs(R_j[0] - R_j[1]) + abs(R_j[2] - R_j[3])) / 12

    SYM_hor = (abs(X_j[0] - X_j[2]) + abs(X_j[1] - X_j[3]) + abs(Y_j[0] - Y_j[2]) + abs(Y_j[1] - Y_j[3]) + abs(
        H_j[0] - H_j[2]) + abs(H_j[1] - H_j[3]) + abs(B_j[0] - B_j[2]) + abs(B_j[1] - B_j[3]) + abs(
        T_j[0] - T_j[2]) + abs(T_j[1] - T_j[3]) + abs(R_j[0] - R_j[2]) + abs(R_j[1] - R_j[3])) / 12

    SYM_rot = (abs(X_j[0] - X_j[3]) + abs(X_j[1] - X_j[2]) + abs(Y_j[0] - Y_j[3]) + abs(Y_j[1] - Y_j[2]) + abs(
        H_j[0] - H_j[3]) + abs(H_j[1] - H_j[2]) + abs(B_j[0] - B_j[3]) + abs(B_j[1] - B_j[2]) + abs(
        T_j[0] - T_j[3]) + abs(T_j[1] - T_j[2]) + abs(R_j[0] - R_j[3]) + abs(R_j[1] - R_j[2])) / 12

    SYM = 1 - (abs(SYM_ver) + abs(SYM_hor) + abs(SYM_rot)) / 3

    return SYM


##-------------------Quadtree Functions---------------------##
# Currently RGB entropy is calculated and intensity.
# The papers also refer to textons. This is not implemented as of yet:
# Representing and Recognizing the Visual Appearance of Materials using Three-dimensional Textons
# THOMAS LEUNG AND JITENDRA MALIK, International Journal of Computer Vision 43(1), 29-44, 2001
def intensity_entropy(inp):
    img = color.rgb2lab(inp)
    l_bins = 20
    L = []
    img = img.reshape(-1, 3)
    img = [tuple(l) for l in img]
    for pixel in img:
        L.append(pixel[0])

    p, x = np.histogram(L, bins=l_bins, range=(0, 100), normed=True)
    p.ravel()
    p = p * 100.
    p = p + 0.000000000001
    p_log = [math.log(y) for y in p]
    p_result = p * p_log
    result = np.sum(p_result)

    return result


# The uncertainty of colour in a leaf, given the leaf. Based on the shannon entropy
def color_entropy(inp):
    inp = inp / 255.
    img = color.rgb2hsv(inp)
    h_bins = 30
    s_bins = 32
    H = []
    S = []
    img = img.reshape(-1, 3)
    img = [tuple(l) for l in img]
    for pixel in img:
        H.append(pixel[0] * 360.)
        S.append(pixel[1] * 100.)

    h, x = np.histogram(H, bins=h_bins, range=(0, 360), density=True)
    s, y = np.histogram(S, bins=s_bins, range=(0, 100), density=True)

    h = h.ravel()
    h = h * 100.
    h = h + 0.000000000001
    h_log = [math.log(y) for y in h]
    h_result = h * h_log

    s = s.ravel()
    s = s * 100.
    s = s + 0.000000000001
    s_log = [math.log(y) for y in s]
    s_result = s * s_log
    result = abs(np.sum(h_result) + np.sum(s_result)) / 2

    return result


# Recursion
def quadtree(leaf, res_leaf, cor_size, i):
    ent_color = color_entropy(leaf)
    ent_int = intensity_entropy(leaf)
    height, width, depth = leaf.shape
    color_thres = 55 # Some threshold that seems okay, this seems quite heavily website dependend. (eg google vs alibaba)
    intensity_thresh = 70 # This is totally based on nothing. So somebody should figure this out (well the entropy in general)
    # It is partially based on the paper, however it seems to be working different)

    # If entropy fullfulls requirements or the website has not been divided in enough leaves and there is still room for division:
    if (ent_color < color_thres or ent_int > intensity_thresh or i < 2) and height / 2 > 8 and width / 2 > 8:
        i += 1
        # Divide the leaf in 4 new leaves
        new_leaf = [leaf[0:height / 2, 0:width / 2], leaf[height / 2:height, 0:width / 2],
                    leaf[0:height / 2, width / 2:width], leaf[height / 2:height, width / 2:width]]

        # Coordinates and size of each leaf
        new_cor_size = [(cor_size[0] + 0, cor_size[1] + 0, width / 2, height / 2),
                        (cor_size[0] + 0, cor_size[1] + height / 2, width / 2, height / 2),
                        (cor_size[0] + width / 2, cor_size[1] + 0, width / 2, height / 2),
                        (cor_size[0] + width / 2, cor_size[1] + height / 2, width / 2, height / 2)
                        ]
        for x in range(len(new_leaf)):
            # Run recursively
            quadtree(new_leaf[x], res_leaf, new_cor_size[x], i)
    else:
        # If not, append the coordinates and size
        res_leaf.append(cor_size)
    return


## ----------------- MAIN ------------------ ##
def execute(b64):
    b64 = base64.b64decode(b64)
    b64 = BytesIO(b64)
    img = Image.open(b64)
    img = np.array(img)
    img = util.img_as_ubyte(img)

    res_leaf = []
    cor_size = (0, 0, img.shape[1], img.shape[0])
    quadtree(img, res_leaf, cor_size, 0)
    #    fig, ax = plt.subplots(1)
    #    for rect in res_leaf:
    #        rect = patches.Rectangle((rect[0], rect[1]), rect[2], rect[3], linewidth=0.1, edgecolor='b', facecolor='none')
    #        ax.add_patch(rect)

    #   ax.imshow(img)
    #   plt.show()
    b = balance(res_leaf, img.shape[1], img.shape[0])
    s = symmetry(res_leaf, img.shape[1], img.shape[0])
    e = equilibrium(res_leaf, img.shape[1], img.shape[0])
    n = len(res_leaf)

    return [b, s, e, n]
