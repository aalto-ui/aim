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
#   In the paper by Miniukovich and De Angeli suggest (among others) two factors for an indication for colourfulness
#   The number of dynamic clusters and the number of colours per dynamic cluster.
#
#   "The number of dynamic clusters of colors after color reduction (more than 5 pixels). If a difference between
#   two colors in a color cube is less than or equal to 3, two colors are united in the same cluster, which continues
#   recursively for all colors. Only clusters containing more than 5 values are counted."
#
#   The number of clusters has not proven statiscally relevant. The number of colours per clusters is. Both are returned
#   with this function.
#
#############
# Technical #
#############
#
#   Inputs: JPG image (base64)
#   Returns: List of 2 items: Number of Clusters (int), Average number of colours per Cluster (int)
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
from operator import itemgetter
from skimage import util
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
    img = img.reshape(-1, 3)
    img = [tuple(l) for l in img]
    hist = collections.Counter(img)
    hist = hist.items()
    frequency = []

    # Create list from histogram
    for x in range(len(hist)):
        add = [hist[x][0][0], hist[x][0][1], hist[x][0][2], hist[x][1]]
        frequency.append(add)

    # Sort the pixels on frequency. This way we can cut the while loop short
    frequency = sorted(frequency, key=itemgetter(3))
    k = len(frequency) - 1

    # Create first cluster
    center_of_clusters = []
    add = [frequency[0][0], frequency[0][1], frequency[0][2], frequency[0][3], 1]
    center_of_clusters.append(add)

    # Find for all colour points a cluster
    while k >= 0:

        # Only colour points with enough presence
        if frequency[k][3] < 6:
            break
        else:
            belong1cluster = False

            # For every colour point calculate distance to all clusters
            for center in range(len(center_of_clusters)):
                point_freq = np.array([frequency[k][0], frequency[k][1], frequency[k][2]])
                point_center = np.array([center_of_clusters[center][0], center_of_clusters[center][1],
                                         center_of_clusters[center][2]])
                distance = np.linalg.norm(point_freq - point_center)

                # If a cluster is close enough, add this colour and recalculate the cluster
                # Now the colour goes to the first cluster fullfilling this. Maybe it should be also the closest?
                if distance <= 3:
                    new_count = center_of_clusters[center][3] + frequency[k][3]
                    new_center = [
                        int((
                                point_freq[0] * frequency[k][3] + point_center[0] * center_of_clusters[center][
                                    3]) / new_count),
                        int((
                                point_freq[1] * frequency[k][3] + point_center[1] * center_of_clusters[center][
                                    3]) / new_count),
                        int((
                                point_freq[2] * frequency[k][3] + point_center[2] * center_of_clusters[center][
                                    3]) / new_count)]
                    center_of_clusters[center][0] = new_center[0]
                    center_of_clusters[center][1] = new_center[1]
                    center_of_clusters[center][2] = new_center[2]
                    center_of_clusters[center][3] = new_count
                    center_of_clusters[center][4] += 1
                    belong1cluster = True
                    break

            # Create new cluster if the colour point is not close enough to other clusters
            if belong1cluster == False:
                add = [frequency[k][0], frequency[k][1], frequency[k][2], frequency[k][3], 1]
                center_of_clusters.append(add)
            k -= 1

    # Only keep clusters with more than 5 colour entries
    new_center_of_clusters = []
    for x in range(len(center_of_clusters)):
        if center_of_clusters[x][4] > 5:
            new_center_of_clusters.append(center_of_clusters[x])

    # Number of clusters, not statistically relevant
    count_dynamic_cluster = len(new_center_of_clusters)

    # Average number of colours per cluster
    average_colour_dynamic_cluster = 0
    for x in range(len(new_center_of_clusters)):
        average_colour_dynamic_cluster += new_center_of_clusters[x][4]

    try:
        average_colour_dynamic_cluster = average_colour_dynamic_cluster / count_dynamic_cluster
    except ZeroDivisionError:
        average_colour_dynamic_cluster = 0

    result = [int(count_dynamic_cluster), int(average_colour_dynamic_cluster)]
    
    return result
