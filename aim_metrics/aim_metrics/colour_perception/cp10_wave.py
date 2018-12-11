###############################################
# WAVE (Weighted Affective Valence Estimates) #
###############################################
#
#   V1.0
#   23/11/2018
#
#   Implemented by:
#   Yustynn Panicker
#   (yustynn.panicker@aalto.fi)
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
#   This is the mean of a simple mapping of pixel colors to the color preference values
#   experimentally obtained by Palmer and Schloss.
#
#   Under their hypothesis that people's color preferences reflect their dispositions
#   towards objects of those colors, they had participants grade their feelings towards
#   sets of objects of particular colors, and used those gradings to construct these
#   color preference values.
#
#   It should be noted that these preferences are likely significantly influenced by
#   sociocultural factors, and thus this particular set of preference values may not
#   accurately reflect all website visitors' impressions of the color scheme.
#
#############
# Technical #
#############
#
#   Inputs: PNG image (base64)
#   Returns: List of 1 item: Average WAVE Score Across Pixels (float)
#
##############
# References #
##############
#
#   1.  Palmer, S.E. and Schloss, K.B. An Ecological Valence Theory of Human Color Preference.
#       Proceedings of the National Academy of Sciences 107, 19 (2010), 8877-8882.
#
##############
# Change Log #
##############
#
###############
# Bugs/Issues #
###############
#
import base64
import numpy as np
from io import BytesIO
from PIL import Image

WAVE_COLOR_TO_SCORE = {
    (24, 155, 154): 0.6377440347071583,
    (37, 152, 114): 0.7125813449023862,
    (59, 125, 181): 0.7396963123644252,
    (86, 197, 208): 0.8297180043383949,
    (96, 163, 215): 1.0,
    (101, 190, 131): 0.648590021691974,
    (115, 56, 145): 0.8080260303687636,
    (124, 159, 201): 0.8318872017353579,
    (126, 152, 68): 0.3579175704989154,
    (129, 199, 144): 0.5726681127982647,
    (133, 204, 208): 0.5932754880694144,
    (156, 78, 155): 0.6843817787418656,
    (159, 90, 48): 0.18329718004338397,
    (162, 32, 66): 0.8481561822125814,
    (162, 115, 167): 0.7451193058568331,
    (162, 149, 59): 0.0,
    (164, 219, 228): 0.7028199566160521,
    (170, 194, 228): 0.7537960954446855,
    (177, 200, 101): 0.33731019522776573,
    (179, 208, 68): 0.4652928416485901,
    (184, 158, 199): 0.63882863340564,
    (193, 224, 196): 0.46095444685466386,
    (204, 119, 141): 0.4859002169197397,
    (208, 154, 119): 0.39154013015184386,
    (218, 198, 118): 0.49132321041214755,
    (224, 231, 153): 0.2928416485900217,
    (235, 45, 92): 0.5488069414316703,
    (242, 149, 185): 0.4577006507592191,
    (243, 145, 51): 0.7114967462039046,
    (251, 200, 166): 0.3741865509761389,
    (252, 232, 158): 0.5140997830802604,
    (253, 228, 51): 0.7201735357917572
}

match_colors = list(WAVE_COLOR_TO_SCORE.keys())


def execute(pngb64):
    """
    Average WAVE score - average WAVE score across pixels (float)

    :param pngb64: PNG image (base64)
    :return: List of 1 item: average WAVE score across pixels (float)
    """

    im = Image.open(BytesIO(base64.b64decode(pngb64)))
    imarr = np.array(im)
    imarr = np.delete(imarr, 3, axis=2)  # remove alpha values

    ax1, ax2, _ = imarr.shape
    num_match_colors = len(match_colors)

    # repeated values for every possible match color
    repeated_imarr = np.tile(imarr, num_match_colors) \
        .reshape(ax1, ax2, num_match_colors, 3)

    l2_norms = ((repeated_imarr - np.array(match_colors)) ** 2).sum(axis=3)

    match_indices = l2_norms.argmin(axis=2).flatten()
    wave_values = [WAVE_COLOR_TO_SCORE[match_colors[i]] for i in match_indices]


    return [np.mean(wave_values)]
