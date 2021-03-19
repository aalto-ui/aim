################
# Grid Quality #
################
#
#   V1.0
#   28/09/2018
#
#   Implemented by:
#   Morteza Shiripour
#   (shiripour.morteza@aalto.fi)
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
#############
# Technical #
#############
#
#   Inputs: PNG image (base64), segmentation elements (list)
#   Returns: List of 1 item: Number of Alignment Lines (int)
#
##############
# References #
##############
#
#   1.  Miniukovich, A. and De Angeli, A. Computation of Interface Aesthetics.
#       Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems - CHI '15, (2015).
#
##############
# Change Log #
##############
#
###############
# Bugs/Issues #
###############
#
import numpy


def execute(b64, seg_elements):
    # Calculating the number of elements
    num_element = len(seg_elements)

    # Converting json file to the python's dictionary format
    data_dict = {'pos_X': [0 for _ in range(num_element)], 'pos_Y': [0 for _ in range(num_element)], 'Shapes_W': [0 for _ in range(num_element)], 'Shapes_H': [0 for _ in range(num_element)]}
    for i in range(num_element):
        data_dict['pos_X'][i] = seg_elements[i]["x_position"]
        data_dict['pos_Y'][i] = seg_elements[i]["y_position"]
        data_dict['Shapes_W'][i] = seg_elements[i]["width"]
        data_dict['Shapes_H'][i] = seg_elements[i]["height"]

    # A function to return the number of alignment lines in one dimension
    def alignment(dna1, dna2):
        data = dna1 + dna2

        # Calculating the number of elements
        align = len(set(data))

        return align


    # Finding end point of each element
    end_x = [0 for _ in range(num_element)]
    end_y = [0 for _ in range(num_element)]
    for i in range(num_element):
        end_x[i] = numpy.sum([data_dict['pos_X'][i], data_dict['Shapes_W'][i]], axis=0)
        end_y[i] = numpy.sum([data_dict['pos_Y'][i], data_dict['Shapes_H'][i]], axis=0)

    # Calculating the number of alignment lines based on the  and horizontally
    num_align_x = alignment(data_dict['pos_X'], end_x)
    num_align_y = alignment(data_dict['pos_Y'], end_y)

    # Total number of alignment lines
    fit_align = sum([num_align_x, num_align_y])

    return [fit_align]
