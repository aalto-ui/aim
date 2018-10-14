###########################
# Clutter - JPG File Size #
###########################
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
#   According to the paper by Minukovich and De Angeli (1) the file size (in jpg) is a good indication to indicate
#   the clutter.
#
#############
# Technical #
#############
#
#   Inputs: JPG image (base64)
#   Returns: List of 1 item: JPEG File Size (in bytes) (int)
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
    jpg_size = int(len(b64) * 0.75)

    return [jpg_size]
