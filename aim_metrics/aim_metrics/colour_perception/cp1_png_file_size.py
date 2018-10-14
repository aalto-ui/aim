###############################
# Color Range - PNG File Size #
###############################
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
#   According to the paper by Minukovich and De Angeli (1) the file size (in png) is a good indication to indicate
#   the colour range. The higher the file size the more colourful the image is likely to be. Of course this is also
#   depended on the size (in pixels). This function returns the file size in bytes. It does not account for the
#   dimensions.
#
#############
# Technical #
#############
#
#   Inputs: PNG image (base64)
#   Returns: List of 1 item: PNG File Size (in bytes) (int)
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
def execute(b64):
    png_size = int(len(b64) * 0.75)

    return [png_size]
