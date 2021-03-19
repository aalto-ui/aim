#############################
# Visual Search Performance #
#############################
#
#   V1.0
#   29/05/2017
#
#   Implemented by:
#   Samuli De Pascale
#   (samuli.depascale@aalto.fi)
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
#   Returns: List of 1 item: Search Speed (base64)
#
##############
# References #
##############
#
#   1.  Jokinen, J.P.P., Sarcar, S., Oulasvirta, A., Silpasuwanchai, C., Wang, Z., Ren, X.
#       Modelling Learning of New Keyboard Layouts. Proceedings of the 35th Annual ACM Conference
#       on Human Factors in Computing Systems - CHI '17, (2017).
#
##############
# Change Log #
##############
#
###############
# Bugs/Issues #
###############
#
import hashlib
import json
import base64
import colorsys
from subprocess32 import call
import numpy as np
import pandas as pd
from pandas import errors
import cv2
import aim_metrics.colour_perception.cp3_HSV_avg as cp3
from tornado.options import options

def_resolution = 921600.0


def execute(b64, elements):
    try:
        processed = {}
        for ele in elements:
            processed_ele = {}
            avg_hue = cp3.execute(ele['b64'])[0]
            if avg_hue > 300 or avg_hue < 60:
                processed_ele['color'] = 'red'
            elif avg_hue > 60 and avg_hue < 180:
                processed_ele['color'] = 'green'
            else:
                processed_ele['color'] = 'blue'
            if (ele['width'] + ele['height']) / def_resolution < 0.02:
                processed_ele['size'] = 'small'
            elif (ele['width'] + ele['height']) / def_resolution < 0.15:
                processed_ele['size'] = 'medium'
            else:
                processed_ele['size'] = 'large'
            processed_ele['id'] = str(ele['id'])
            processed_ele['fulltext'] = ''
            processed_ele['height'] = ele['height']
            processed_ele['width'] = ele['width']
            processed_ele['importance'] = '1'
            processed_ele['logo'] = 0
            processed_ele['shape'] = 'rectangle'
            processed_ele['target'] = 1
            processed_ele['text'] = hashlib.md5(ele['b64']).hexdigest()
            processed_ele['type'] = 'unlabeled'
            processed_ele['word_count'] = 1
            processed_ele['x_position'] = ele['x_position']
            processed_ele['y_position'] = ele['y_position']
            processed[str(ele['id'])] = processed_ele

        name = options.name
        with open("configs/vg2_" + name + ".json", "w") as file:
            file.write(json.dumps(processed))
        call([options.layout_learning_path, "inputs/vg2_" + name + ".txt"])

        try:
            data = pd.read_csv("outputs/vg2_" + name + ".csv")
            tasktimes = \
                data[['target', 'tasktime']].groupby('target').mean().reset_index()
            min_val = tasktimes['tasktime'].min()
            max_val = tasktimes['tasktime'].max()
            tasktimes['tasktime'] = \
                (tasktimes['tasktime'] - min_val) / (max_val - min_val)

            img = base64.b64decode(b64)
            npimg = np.fromstring(img, dtype=np.uint8)
            img = cv2.imdecode(npimg, 1)
            img_overlay = img.copy()
            img_out = img.copy()

            for key, element in processed.iteritems():
                time = tasktimes.loc[tasktimes['target'] == element['text']]
                time = time['tasktime']
                h = (0 + int(time * 240)) / 360.0
                # r, g, b = colorsys.hls_to_rgb(h, 1, 0.5)
                r, g, b = colorsys.hls_to_rgb(h, 0.5, 1)
                rgb = (int(r * 255), int(g * 255), int(b * 255))
                x = element['x_position']
                y = element['y_position']
                height = element['height']
                width = element['width']
                cv2.rectangle(img_overlay, (x, y), (x + width, y + height), rgb, -1)

            cv2.addWeighted(img_overlay, 0.5, img_out, 0.5, 0, img_out)

            cv2.rectangle(img_out, (0, 0), (1279, 799), (0, 0, 0), 1)

            img_scale = np.zeros((120, 1280, 3), np.uint8)
            img_scale[:, :] = (255, 255, 255)

            cv2.rectangle(img_scale, (99, 49), (580, 91), (0, 0, 0), 1)

            for dist in range(0, 240):
                h = (0 + dist) / 360.0
                r, g, b = colorsys.hls_to_rgb(h, 0.5, 1)
                rgb = (int(r * 255), int(g * 255), int(b * 255))
                cv2.rectangle(img_scale, (100 + (dist * 2), 50),
                              (100 + (dist * 2) + 1, 90), rgb, -1)

            cv2.putText(img_scale, 'Average search time in seconds:', (20, 35),
                        cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img_scale, '{0:.2f}s'.format(min_val), (20, 80),
                        cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img_scale, '{0:.2f}s'.format(max_val), (585, 80),
                        cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 0), 1, cv2.LINE_AA)

            img_out = np.concatenate((img_out, img_scale), axis=0)

            return [base64.b64encode(cv2.imencode(".png", img_out)[1])]
        except errors.EmptyDataError:
            # For handling screenshots of fully white web pages etc.
            min_val = 0
            max_val = 0
            img = base64.b64decode(b64)
            npimg = np.fromstring(img, dtype=np.uint8)
            img = cv2.imdecode(npimg, 1)
            img_overlay = img.copy()
            img_out = img.copy()
            cv2.addWeighted(img_overlay, 0.5, img_out, 0.5, 0, img_out)
            cv2.rectangle(img_out, (0, 0), (1279, 799), (0, 0, 0), 1)
            img_scale = np.zeros((120, 1280, 3), np.uint8)
            img_scale[:, :] = (255, 255, 255)
            cv2.rectangle(img_scale, (99, 49), (580, 91), (0, 0, 0), 1)
            cv2.putText(img_scale, 'Average search time in seconds:', (20, 35),
                        cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img_scale, '{0:.2f}s'.format(min_val), (20, 80),
                        cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(img_scale, '{0:.2f}s'.format(max_val), (585, 80),
                        cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 0), 1, cv2.LINE_AA)
            img_out = np.concatenate((img_out, img_scale), axis=0)

            return [base64.b64encode(cv2.imencode(".png", img_out)[1])]
    except:
        # FIX: Quick fix for handling unexpected errors with high-resolution images
        return [""]
