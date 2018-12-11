from aim_metrics.colour_perception import cp1_png_file_size as cp1
from aim_metrics.colour_perception import cp2_number_of_colours as cp2
from aim_metrics.colour_perception import cp3_HSV_avg as cp3
from aim_metrics.colour_perception import cp4_HSV_unique as cp4
from aim_metrics.colour_perception import cp5_LAB_avg as cp5
from aim_metrics.colour_perception import cp6_hassler_susstrunk as cp6
from aim_metrics.colour_perception import cp7_static_clusters as cp7
from aim_metrics.colour_perception import cp8_dynamic_clusters as cp8
from aim_metrics.colour_perception import cp9_luminance_sd as cp9
from aim_metrics.colour_perception import cp10_wave as cp10

from aim_metrics.perceptual_fluency import pf1_edge_density as pf1
from aim_metrics.perceptual_fluency import pf2_edge_congestion as pf2
from aim_metrics.perceptual_fluency import pf3_jpeg_file_size as pf3
from aim_metrics.perceptual_fluency import pf4_figure_ground_contrast as pf4
from aim_metrics.perceptual_fluency import pf5_pixel_symmetry as pf5
from aim_metrics.perceptual_fluency import pf6_quadtree_decomposition as pf6
from aim_metrics.perceptual_fluency import pf7_white_space as pf7
from aim_metrics.perceptual_fluency import pf8_grid_quality as pf8

from aim_metrics.visual_guidance import vg1_saliency as vg1
from aim_metrics.visual_guidance import vg2_visual_search as vg2

from aim_metrics.accessibility import ac1_colour_blindness as ac1

metrics_mapping = {
    'cp1': {
        'executor': cp1,
        'format': 'png'
    },
    'cp2': {
        'executor': cp2,
        'format': 'png',
        'type': 0
    },
    'cp3': {
        'executor': cp3,
        'format': 'jpg',
    },
    'cp4': {
        'executor': cp4,
        'format': 'jpg',
    },
    'cp5': {
        'executor': cp5,
        'format': 'jpg',
    },
    'cp6': {
        'executor': cp6,
        'format': 'jpg',
    },
    'cp7': {
        'executor': cp7,
        'format': 'jpg',
    },
    'cp8': {
        'executor': cp8,
        'format': 'jpg',
    },
    'cp9': {
        'executor': cp9,
        'format': 'jpg',
    },
    'cp10': {
        'executor': cp10,
        'format': 'png',
    },
    'pf1': {
        'executor': pf1,
        'format': 'jpg',
    },
    'pf2': {
        'executor': pf2,
        'format': 'png',
    },
    'pf3': {
        'executor': pf3,
        'format': 'jpg',
    },
    'pf4': {
        'executor': pf4,
        'format': 'png',
    },
    'pf5': {
        'executor': pf5,
        'format': 'png',
    },
    'pf6': {
        'executor': pf6,
        'format': 'jpg',
    },
    'pf7': {
        'executor': pf7,
        'format': 'seg',
    },
    'pf8': {
        'executor': pf8,
        'format': 'seg',
    },
    'vg1': {
        'executor': vg1,
        'format': 'jpg',
    },
    'vg2': {
        'executor': vg2,
        'format': 'seg',
    },
    'ac1': {
        'executor': ac1,
        'format': 'jpg',
    },
}


def execute_metric(metric, pngb64, jpgb64, seg_elements):
    metric_config = metrics_mapping[metric]
    result = []
    if metric_config['format'] == 'png':
        if 'type' in metric_config:
            result = metric_config['executor'].execute(
                pngb64,
                metric_config['type'])
        else:
            result = metric_config['executor'].execute(pngb64)
    elif metric_config['format'] == 'jpg':
        result = metric_config['executor'].execute(jpgb64)
    elif metric_config['format'] == 'seg':
        result = metric_config['executor'].execute(pngb64, seg_elements)
    return result
