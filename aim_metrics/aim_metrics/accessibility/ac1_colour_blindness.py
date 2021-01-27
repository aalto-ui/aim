###########################################################
# Colour Blindness - Deuteranope, Protanope and Tratanope #
###########################################################
#
#   V1.0
#   29/05/2017
#
#   Implemented by:
#   Thomas Langerak
#   (hello@thomaslangerak.nl)
#
#   Based on:
#   https://moinmo.in/AccessibleMoin?action=AttachFile&do=get&target=daltonize.py
#   By:
#   Oliver Siemoneit (see ac1_original_header.txt)
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
#   (Taken from 1)
#   Color vision deficiency (CVD) affects approximately 200 million people worldwide, compromising the ability of these
#   individuals to effectively perform color and visualization-related tasks. This has a significant impact on their
#   private and professional lives. We present a physiologically-based model for simulating color vision. Our model is
#   based on the stage theory of human color vision and is derived from data reported in electrophysiological studies.
#   It is the first model to consistently handle normal color vision, anomalous trichromacy, and dichromacy in a
#   unified way. We have validated the proposed model through an experimental evaluation involving groups of color
#   vision deficient individuals and normal color vision ones. Our model can provide insights and feedback on how to
#   improve visualization experiences for individuals with CVD. It also provides a framework for testing hypotheses
#   about some aspects of the retinal photoreceptors in color vision deficient individuals.
#
#############
# Technical #
#############
#
#   Inputs: JPG image (base64)
#   Returns: List of 3 items: Deuteranopia (base64), Protanopia (base64), Tritanopia (base64)

##############
# References #
##############
#
#   1.  Machado, G., Oliveira, M. and Fernandes, L. A Physiologically-based Model for Simulation of Color Vision
#       Deficiency. IEEE Transactions on Visualization and Computer Graphics 15, 6 (2009), 1291-1298.
#
##############
# Change Log #
##############
#
###############
# Bugs/Issues #
###############
#
#   Can make it a nested loop instead of doing three times the same things in the loop
#
import StringIO
import numpy
import base64
from PIL import Image
from io import BytesIO


def execute(b64):
    # Get image data
    b64 = base64.b64decode(b64)
    b64 = BytesIO(b64)
    img = Image.open(b64)
    im = img.convert('RGB')
    RGB = numpy.asarray(im, dtype=float)

    # Transformation matrix for Deuteranope (a form of red/green color deficit)
    deut_matrix = numpy.array(
        [[0.367322, 0.860646, -0.227968],
        [0.280085, 0.672501,  0.047413],
        [-0.011820, 0.042940,  0.968881]]
    )
    # Transformation matrix for Protanope (another form of red/green color deficit)
    prot_matrix = numpy.array(
        [[0.152286, 1.052583, -0.204868],
        [0.114503, 0.786281, 0.099216],
        [-0.003882, -0.048116, 1.051998]]
    )
    # Transformation matrix for Tritanope (a blue/yellow deficit - very rare)
    trit_matrix = numpy.array(
        [[1.255528, -0.076749, -0.178779],
         [-0.078411, 0.930809, 0.147602],
         [0.004733, 0.691367, 0.303900]]
    )

    # Transform the image using each matrix
    rgb_d = numpy.zeros_like(RGB)
    rgb_p = numpy.zeros_like(RGB)
    rgb_t = numpy.zeros_like(RGB)
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            rgb = RGB[i, j, :3]
            rgb_d[i, j, :3] = numpy.dot(deut_matrix, rgb)
            rgb_p[i, j, :3] = numpy.dot(prot_matrix, rgb)
            rgb_t[i, j, :3] = numpy.dot(trit_matrix, rgb)


    # Make sure that all numbers are within 0-255 due to conversions
    for i in range(RGB.shape[0]):
        for j in range(RGB.shape[1]):
            rgb_d[i, j, 0] = max(0, rgb_d[i, j, 0])
            rgb_d[i, j, 0] = min(255, rgb_d[i, j, 0])
            rgb_d[i, j, 1] = max(0, rgb_d[i, j, 1])
            rgb_d[i, j, 1] = min(255, rgb_d[i, j, 1])
            rgb_d[i, j, 2] = max(0, rgb_d[i, j, 2])
            rgb_d[i, j, 2] = min(255, rgb_d[i, j, 2])

            rgb_p[i, j, 0] = max(0, rgb_p[i, j, 0])
            rgb_p[i, j, 0] = min(255, rgb_p[i, j, 0])
            rgb_p[i, j, 1] = max(0, rgb_p[i, j, 1])
            rgb_p[i, j, 1] = min(255, rgb_p[i, j, 1])
            rgb_p[i, j, 2] = max(0, rgb_p[i, j, 2])
            rgb_p[i, j, 2] = min(255, rgb_p[i, j, 2])

            rgb_t[i, j, 0] = max(0, rgb_t[i, j, 0])
            rgb_t[i, j, 0] = min(255, rgb_t[i, j, 0])
            rgb_t[i, j, 1] = max(0, rgb_t[i, j, 1])
            rgb_t[i, j, 1] = min(255, rgb_t[i, j, 1])
            rgb_t[i, j, 2] = max(0, rgb_t[i, j, 2])
            rgb_t[i, j, 2] = min(255, rgb_t[i, j, 2])

    # Save as image into buffer
    sim_d = rgb_d.astype('uint8')
    sim_p = rgb_p.astype('uint8')
    sim_t = rgb_t.astype('uint8')
    im_d = Image.fromarray(sim_d, mode='RGB')
    im_p = Image.fromarray(sim_p, mode='RGB')
    im_t = Image.fromarray(sim_t, mode='RGB')
    d_string = StringIO.StringIO()
    p_string = StringIO.StringIO()
    t_string = StringIO.StringIO()
    im_d.save(d_string, format="PNG")
    im_p.save(p_string, format="PNG")
    im_t.save(t_string, format="PNG")

    # Encode it as base64
    d_b64 = base64.b64encode(d_string.getvalue())
    p_b64 = base64.b64encode(p_string.getvalue())
    t_b64 = base64.b64encode(t_string.getvalue())

    d_string.close()
    p_string.close()
    t_string.close()

    return [d_b64, p_b64, t_b64]
