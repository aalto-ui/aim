#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Image segmentation utility functions.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Third-party modules
import cv2
import numpy as np

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Amir Hossein Kargaran, Markku Laine"
__date__ = "2021-08-05"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Image segmentation utility functions
# ----------------------------------------------------------------------------


def resize_by_longest_edge(org_im, resize_length):
    height, width = org_im.shape[:2]
    w_h_ratio = width / height

    if height > width:
        resize_w = resize_length * w_h_ratio
        resize_img = cv2.resize(org_im, (int(resize_w), int(resize_length)))
        return resize_img
    else:
        resize_h = resize_length / w_h_ratio
        resize_img = cv2.resize(org_im, (int(resize_length), int(resize_h)))
        return resize_img


def gray_to_gradient(img):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_f = np.copy(img)
    img_f = img_f.astype("float")

    kernel_h = np.array([[0, 0, 0], [0, -1.0, 1.0], [0, 0, 0]])
    kernel_v = np.array([[0, 0, 0], [0, -1.0, 0], [0, 1.0, 0]])
    dst1 = abs(cv2.filter2D(img_f, -1, kernel_h))
    dst2 = abs(cv2.filter2D(img_f, -1, kernel_v))
    gradient = (dst1 + dst2).astype("uint8")
    return gradient


def binarization(org, grad_min, show=False, wait_key=0):
    grey = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
    grad = gray_to_gradient(grey)  # get RoI with high gradient
    rec, binary = cv2.threshold(
        grad, grad_min, 255, cv2.THRESH_BINARY
    )  # enhance the RoI
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, (3, 3))  # remove noises
    if show:
        cv2.imshow("Binary", morph)
        if wait_key is not None:
            cv2.waitKey(wait_key)
    return morph


# Draw
def draw_bounding_box(
    org,
    components,
    color=(0, 255, 0),
    line=1,
    show=False,
    write_path=None,
    name="board",
    is_return=False,
    wait_key=0,
):
    """
    Draw bounding box of components on the original image
    :param wait_key:
    :param is_return:
    :param name:
    :param write_path:
    :param org: original image
    :param components: bbox [(column_min, row_min, column_max, row_max)]
                    -> top_left: (column_min, row_min)
                    -> bottom_right: (column_max, row_max)
    :param color: line color
    :param line: line thickness
    :param show: show or not
    :return: labeled image
    """
    if not show and write_path is None and not is_return:
        return
    board = org.copy()
    for compo in components:
        bbox = compo.put_bbox()
        board = cv2.rectangle(
            board, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, line
        )
    if show:
        cv2.imshow(name, board)
        if wait_key is not None:
            cv2.waitKey(wait_key)
        if wait_key == 0:
            cv2.destroyWindow(name)
    if write_path is not None:
        cv2.imwrite(write_path, board)
    return board


def draw_boundary(components, shape, show=False):
    """
    Draw boundary of objects on the black withe
    :param components: boundary: [top, bottom, left, right]
                        -> up, bottom: (column_index, min/max row border)
                        -> left, right: (row_index, min/max column border) detect range of each row
    :param shape: shape or original image
    :param show: show or not
    :return: drawn board
    """
    board = np.zeros(shape[:2], dtype=np.uint8)  # binary board
    for component in components:
        # up and bottom: (column_index, min/max row border)
        for point in component.boundary[0] + component.boundary[1]:
            board[point[1], point[0]] = 255
        # left, right: (row_index, min/max column border)
        for point in component.boundary[2] + component.boundary[3]:
            board[point[0], point[1]] = 255
    if show:
        cv2.imshow("Rec", board)
        cv2.waitKey(0)
    return board


# File utils
def corners2json(compos, img_shape):
    output = {"img_shape": img_shape, "segments": []}

    for compo in compos:
        c = {
            "id": compo.id,
            "class": compo.category,
            "subclass": compo.subcategory,
        }
        (
            c["column_min"],
            c["row_min"],
            c["column_max"],
            c["row_max"],
        ) = compo.put_bbox()
        c["width"] = compo.width
        c["height"] = compo.height
        output["segments"].append(c)
    return output


# Bbox
class Bbox:
    def __init__(self, col_min, row_min, col_max, row_max):
        self.col_min = col_min
        self.row_min = row_min
        self.col_max = col_max
        self.row_max = row_max

        self.width = self.col_max - self.col_min
        self.height = self.row_max - self.row_min
        self.box_area = self.width * self.height

    def init_bound(self):
        self.width = self.col_max - self.col_min
        self.height = self.row_max - self.row_min
        self.box_area = self.width * self.height

    def put_bbox(self):
        return self.col_min, self.row_min, self.col_max, self.row_max

    def bbox_resize(self, resize_ratio):
        self.col_min = int(self.col_min * resize_ratio)
        self.row_min = int(self.row_min * resize_ratio)
        self.col_max = int(self.col_max * resize_ratio)
        self.row_max = int(self.row_max * resize_ratio)
        self.init_bound()
        return self

    def bbox_cal_area(self):
        self.box_area = self.width * self.height
        return self.box_area

    def bbox_relation(self, bbox_b):
        """
        :return: -1 : a in b
                 0  : a, b are not intersected
                 1  : b in a
                 2  : a, b are identical or intersected
        """
        col_min_a, row_min_a, col_max_a, row_max_a = self.put_bbox()
        col_min_b, row_min_b, col_max_b, row_max_b = bbox_b.put_bbox()

        # if a is in b
        if (
            col_min_a > col_min_b
            and row_min_a > row_min_b
            and col_max_a < col_max_b
            and row_max_a < row_max_b
        ):
            return -1
        # if b is in a
        elif (
            col_min_a < col_min_b
            and row_min_a < row_min_b
            and col_max_a > col_max_b
            and row_max_a > row_max_b
        ):
            return 1
        # a and b are non-intersect
        elif (col_min_a > col_max_b or row_min_a > row_max_b) or (
            col_min_b > col_max_a or row_min_b > row_max_a
        ):
            return 0
        # intersection
        else:
            return 2

    def bbox_relation_nms(self, bbox_b, bias=(0, 0)):
        """
         Calculate the relation between two rectangles by nms
        :return: -1 : a in b
          0  : a, b are not intersected
          1  : b in a
          2  : a, b are intersected
        """
        col_min_a, row_min_a, col_max_a, row_max_a = self.put_bbox()
        col_min_b, row_min_b, col_max_b, row_max_b = bbox_b.put_bbox()

        bias_col, bias_row = bias
        # get the intersected area
        col_min_s = max(col_min_a - bias_col, col_min_b - bias_col)
        row_min_s = max(row_min_a - bias_row, row_min_b - bias_row)
        col_max_s = min(col_max_a + bias_col, col_max_b + bias_col)
        row_max_s = min(row_max_a + bias_row, row_max_b + bias_row)
        w = np.maximum(0, col_max_s - col_min_s)
        h = np.maximum(0, row_max_s - row_min_s)
        inter = w * h
        area_a = (col_max_a - col_min_a) * (row_max_a - row_min_a)
        area_b = (col_max_b - col_min_b) * (row_max_b - row_min_b)
        iou = inter / (area_a + area_b - inter)
        ioa = inter / self.box_area
        iob = inter / bbox_b.box_area

        if iou == 0 and ioa == 0 and iob == 0:
            return 0

        # contained by b
        if ioa >= 1:
            return -1
        # contains b
        if iob >= 1:
            return 1
        # not intersected with each other
        # intersected
        if iou >= 0.02 or iob > 0.2 or ioa > 0.2:
            return 2
        # if iou == 0:
        # print('ioa:%.5f; iob:%.5f; iou:%.5f' % (ioa, iob, iou))
        return 0

    def bbox_cvt_relative_position(self, col_min_base, row_min_base):
        """
        Convert to relative position based on base coordinator
        """
        self.col_min += col_min_base
        self.col_max += col_min_base
        self.row_min += row_min_base
        self.row_max += row_min_base

    def bbox_merge(self, bbox_b):
        """
        Merge two intersected bboxes
        """
        col_min_a, row_min_a, col_max_a, row_max_a = self.put_bbox()
        col_min_b, row_min_b, col_max_b, row_max_b = bbox_b.put_bbox()
        col_min = min(col_min_a, col_min_b)
        col_max = max(col_max_a, col_max_b)
        row_min = min(row_min_a, row_min_b)
        row_max = max(row_max_a, row_max_b)
        new_bbox = Bbox(col_min, row_min, col_max, row_max)
        return new_bbox

    def bbox_padding(self, image_shape, pad):
        row, col = image_shape[:2]
        self.col_min = max(self.col_min - pad, 0)
        self.col_max = min(self.col_max + pad, col)
        self.row_min = max(self.row_min - pad, 0)
        self.row_max = min(self.row_max + pad, row)


# Component
def cvt_compos_relative_pos(compos, col_min_base, row_min_base):
    for compo in compos:
        compo.compo_relative_position(col_min_base, row_min_base)


def compos_containment(compos):
    for i in range(len(compos) - 1):
        for j in range(i + 1, len(compos)):
            relation = compos[i].compo_relation(compos[j])
            if relation == -1:
                compos[j].contain.append(i)
            if relation == 1:
                compos[i].contain.append(j)
    return compos


def compos_update(compos, org_shape):
    for i, compo in enumerate(compos):
        # start from 1, id 0 is background
        compo.compo_update(i + 1, org_shape)

    return compos


class Component:
    def __init__(self, region, image_shape):
        self.id = None
        self.region = region
        self.boundary = self.compo_get_boundary()
        self.bbox = self.compo_get_bbox()
        self.bbox_area = self.bbox.box_area

        self.region_area = len(region)
        self.width = len(self.boundary[0])
        self.height = len(self.boundary[2])
        self.image_shape = image_shape
        self.area = self.width * self.height

        self.category = "Component"
        self.subcategory = None
        self.contain = []

        self.rect_ = None
        self.line_ = None
        self.redundant = False

    def compo_update(self, id, org_shape):
        self.id = id
        self.image_shape = org_shape
        self.width = self.bbox.width
        self.height = self.bbox.height
        self.bbox_area = self.bbox.box_area
        self.area = self.width * self.height

    def put_bbox(self):
        return self.bbox.put_bbox()

    def resize(self, resize_ratio):
        self.bbox.bbox_resize(resize_ratio)
        self.compo_update(self.id, self.image_shape)
        return self

    def compo_update_bbox_area(self):
        self.bbox_area = self.bbox.bbox_cal_area()

    def compo_get_boundary(self):
        """
        get the bounding boundary of an object(region)
        boundary: [top, bottom, left, right]
        -> up, bottom: (column_index, min/max row border)
        -> left, right: (row_index, min/max column border) detect range of each row
        """
        border_up, border_bottom, border_left, border_right = {}, {}, {}, {}
        for point in self.region:
            # point: (row_index, column_index)
            # up, bottom: (column_index, min/max row border) detect range of each column
            if point[1] not in border_up or border_up[point[1]] > point[0]:
                border_up[point[1]] = point[0]
            if (
                point[1] not in border_bottom
                or border_bottom[point[1]] < point[0]
            ):
                border_bottom[point[1]] = point[0]
            # left, right: (row_index, min/max column border) detect range of each row
            if point[0] not in border_left or border_left[point[0]] > point[1]:
                border_left[point[0]] = point[1]
            if (
                point[0] not in border_right
                or border_right[point[0]] < point[1]
            ):
                border_right[point[0]] = point[1]

        boundary = [border_up, border_bottom, border_left, border_right]
        # descending sort
        for i in range(len(boundary)):
            boundary[i] = [[k, boundary[i][k]] for k in boundary[i].keys()]
            boundary[i] = sorted(boundary[i], key=lambda x: x[0])
        return boundary

    def compo_get_bbox(self):
        """
        Get the top left and bottom right points of boundary
        :return: corners: [(top_left, bottom_right)]
                            -> top_left: (column_min, row_min)
                            -> bottom_right: (column_max, row_max)
        """

        col_min, row_min = (
            int(min(self.boundary[0][0][0], self.boundary[1][-1][0])),
            int(min(self.boundary[2][0][0], self.boundary[3][-1][0])),
        )
        col_max, row_max = (
            int(max(self.boundary[0][0][0], self.boundary[1][-1][0])),
            int(max(self.boundary[2][0][0], self.boundary[3][-1][0])),
        )
        bbox = Bbox(col_min, row_min, col_max, row_max)
        return bbox

    def compo_is_rectangle(self, min_rec_evenness, max_dent_ratio, test=False):
        """
        detect if an object is rectangle by evenness and dent of each border
        """
        dent_direction = [1, -1, 1, -1]  # direction for convex

        flat = 0
        parameter = 0
        for n, border in enumerate(self.boundary):
            parameter += len(border)
            # dent detection
            pit = 0  # length of pit
            depth = 0  # the degree of surface changing
            if n <= 1:
                adj_side = max(
                    len(self.boundary[2]), len(self.boundary[3])
                )  # get maximum length of adjacent side
            else:
                adj_side = max(len(self.boundary[0]), len(self.boundary[1]))

            # -> up, bottom: (column_index, min/max row border)
            # -> left, right: (row_index, min/max column border) detect range of each row
            abnm = 0
            for i in range(int(3 + len(border) * 0.02), len(border) - 1):
                # calculate gradient
                difference = border[i][1] - border[i + 1][1]
                # the degree of surface changing
                depth += difference
                # ignore noise at the start of each direction
                if (
                    i / len(border) < 0.08
                    and (dent_direction[n] * difference) / adj_side > 0.5
                ):
                    depth = 0  # reset

                # print(border[i][1], i / len(border), depth, (dent_direction[n] * difference) / adj_side)
                # if the change of the surface is too large, count it as part of abnormal change
                if abs(depth) / adj_side > 0.3:
                    abnm += 1  # count the size of the abnm
                    # if the abnm is too big, the shape should not be a rectangle
                    if abnm / len(border) > 0.1:
                        if test:
                            print("abnms", abnm, abnm / len(border))
                            draw_boundary([self], self.image_shape, show=True)
                        self.rect_ = False
                        return False
                    continue
                else:
                    # reset the abnm if the depth back to normal
                    abnm = 0

                # if sunken and the surface changing is large, then counted as pit
                if (
                    dent_direction[n] * depth < 0
                    and abs(depth) / adj_side > 0.15
                ):
                    pit += 1
                    continue

                # if the surface is not changing to a pit and the gradient is zero, then count it as flat
                if abs(depth) < 1 + adj_side * 0.015:
                    flat += 1
                if test:
                    print(depth, adj_side, flat)
            # if the pit is too big, the shape should not be a rectangle
            if pit / len(border) > max_dent_ratio:
                if test:
                    print("pit", pit, pit / len(border))
                    draw_boundary([self], self.image_shape, show=True)
                self.rect_ = False
                return False
        if test:
            print(flat / parameter, "\n")
            draw_boundary([self], self.image_shape, show=True)
        # ignore text and irregular shape
        if self.height / self.image_shape[0] > 0.3:
            min_rec_evenness = 0.85
        if (flat / parameter) < min_rec_evenness:
            self.rect_ = False
            return False
        self.rect_ = True
        return True

    def compo_is_line(self, min_line_thickness):
        """
        Check this object is line by checking its boundary
        :param min_line_thickness:
        :return: Boolean
        """
        # horizontally
        slim = 0
        for i in range(self.width):
            if (
                abs(self.boundary[1][i][1] - self.boundary[0][i][1])
                <= min_line_thickness
            ):
                slim += 1
        if slim / len(self.boundary[0]) > 0.93:
            self.line_ = True
            return True
        # vertically
        slim = 0
        for i in range(self.height):
            if (
                abs(self.boundary[2][i][1] - self.boundary[3][i][1])
                <= min_line_thickness
            ):
                slim += 1
        if slim / len(self.boundary[2]) > 0.93:
            self.line_ = True
            return True
        self.line_ = False
        return False

    def compo_relation(self, compo_b, bias=(0, 0)):
        """
        :return: -1 : a in b
                 0  : a, b are not intersected
                 1  : b in a
                 2  : a, b are identical or intersected
        """
        return self.bbox.bbox_relation_nms(compo_b.bbox, bias)

    def compo_relative_position(self, col_min_base, row_min_base):
        """
        Convert to relative position based on base coordinator
        """
        self.bbox.bbox_cvt_relative_position(col_min_base, row_min_base)

    def compo_merge(self, compo_b):
        self.bbox = self.bbox.bbox_merge(compo_b.bbox)
        self.compo_update(self.id, self.image_shape)

    def compo_clipping(self, img, pad=0, show=False):
        (column_min, row_min, column_max, row_max) = self.put_bbox()
        column_min = max(column_min - pad, 0)
        column_max = min(column_max + pad, img.shape[1])
        row_min = max(row_min - pad, 0)
        row_max = min(row_max + pad, img.shape[0])
        clip = img[row_min:row_max, column_min:column_max]
        if show:
            cv2.imshow("Clipping", clip)
            cv2.waitKey()
        return clip


# Detection


def merge_intersected_compos(compos):
    changed = True
    while changed:
        changed = False
        temp_set = []
        for compo_a in compos:
            merged = False
            for compo_b in temp_set:
                if compo_a.compo_relation(compo_b) == 2:
                    compo_b.compo_merge(compo_a)
                    merged = True
                    changed = True
                    break
            if not merged:
                temp_set.append(compo_a)
        compos = temp_set.copy()
    return compos


def rm_contained_compos_not_in_block(compos):
    """
    remove all components contained by others that are not Block
    """
    marked = np.full(len(compos), False)
    for i in range(len(compos) - 1):
        for j in range(i + 1, len(compos)):
            relation = compos[i].compo_relation(compos[j])
            if relation == -1 and compos[j].category != "Block":
                marked[i] = True
            if relation == 1 and compos[i].category != "Block":
                marked[j] = True
    new_compos = []
    for i in range(len(marked)):
        if not marked[i]:
            new_compos.append(compos[i])
    return new_compos


def rm_line(
    binary, max_line_thickness, min_line_length_ratio, show=False, wait_key=0
):
    def is_valid_line(line):
        line_length = 0
        line_gap = 0
        for j in line:
            if j > 0:
                if line_gap > 5:
                    return False
                line_length += 1
                line_gap = 0
            elif line_length > 0:
                line_gap += 1
        if line_length / width > min_line_length_ratio:
            return True
        return False

    height, width = binary.shape[:2]

    start_row, end_row = -1, -1
    check_line = False
    check_gap = False
    for i, row in enumerate(binary):
        # line_ratio = (sum(row) / 255) / width
        # if line_ratio > 0.9:
        if is_valid_line(row):
            # new start: if it is checking a new line, mark this row as start
            if not check_line:
                start_row = i
                check_line = True
        else:
            # end the line
            if check_line:
                # thin enough to be a line, then start checking gap
                if i - start_row < max_line_thickness:
                    end_row = i
                    check_gap = True
                else:
                    start_row, end_row = -1, -1
                check_line = False
        # check gap
        if check_gap and i - end_row > max_line_thickness:
            binary[start_row:end_row] = 0
            start_row, end_row = -1, -1
            check_line = False
            check_gap = False

    if (check_line and (height - start_row) < max_line_thickness) or check_gap:
        binary[start_row:end_row] = 0

    if show:
        cv2.imshow("No-line binary", binary)
        if wait_key is not None:
            cv2.waitKey(wait_key)
            cv2.destroyWindow("No-line binary")

    return binary


def compo_filter(compos, min_area, img_shape):
    max_height = img_shape[0] * 0.8
    compos_new = []
    for compo in compos:
        if compo.area < min_area:
            continue
        if compo.height > max_height:
            continue
        ratio_h = compo.width / compo.height
        ratio_w = compo.height / compo.width
        if (
            ratio_h > 50
            or ratio_w > 40
            or (
                min(compo.height, compo.width) < 8
                and max(ratio_h, ratio_w) > 10
            )
        ):
            continue
        compos_new.append(compo)
    return compos_new


def is_block(clip, thread):
    """
    Block is a rectangle border enclosing a group of compos (consider it as a wireframe)
    Check if a compo is block by checking if the inner side of its border is blank
    """
    side = 4  # scan 4 lines inner forward each border
    # top border - scan top down
    blank_count = 0
    for i in range(1, 5):
        if sum(clip[side + i]) / 255 > thread * clip.shape[1]:
            blank_count += 1
    if blank_count > 2:
        return False
    # left border - scan left to right
    blank_count = 0
    for i in range(1, 5):
        if sum(clip[:, side + i]) / 255 > thread * clip.shape[0]:
            blank_count += 1
    if blank_count > 2:
        return False

    side = -4
    # bottom border - scan bottom up
    blank_count = 0
    for i in range(-1, -5, -1):
        if sum(clip[side + i]) / 255 > thread * clip.shape[1]:
            blank_count += 1
    if blank_count > 2:
        return False
    # right border - scan right to left
    blank_count = 0
    for i in range(-1, -5, -1):
        if sum(clip[:, side + i]) / 255 > thread * clip.shape[0]:
            blank_count += 1
    if blank_count > 2:
        return False
    return True


def compo_block_recognition(binary, compos, block_side_length=0.15):
    height, width = binary.shape
    for compo in compos:
        if (
            compo.height / height > block_side_length
            and compo.width / width > block_side_length
        ):
            clip = compo.compo_clipping(binary)
            if is_block(clip, thread=0.15):
                compo.category = "Block"
    return compos


def component_detection(
    binary,
    min_obj_area,
    min_rec_evenness,
    max_dent_ratio,
    step_h=5,
    step_v=2,
    rec_detect=False,
    show=False,
    test=False,
):
    """
    take the binary image as input.
    calculate the connected regions -> get the bounding boundaries of them -> check if those regions are rectangles
    return all boundaries and boundaries of rectangles
    :param test:
    :param show:
    :param rec_detect:
    :param step_v:
    :param step_h:
    :param binary: Binary image from pre-processing
    :param min_obj_area: If not pass then ignore the small object
    :param min_rec_evenness: If not pass then this object cannot be rectangular
    :param max_dent_ratio: If not pass then this object cannot be rectangular
    :return: boundary: [top, bottom, left, right]
                        -> up, bottom: list of (column_index, min/max row border)
                        -> left, right: list of (row_index, min/max column border) detect range of each row
    """
    mask = np.zeros((binary.shape[0] + 2, binary.shape[1] + 2), dtype=np.uint8)
    compos_all = []
    compos_rec = []
    compos_nonrec = []
    row, column = binary.shape[0], binary.shape[1]
    for i in range(0, row, step_h):
        for j in range(i % 2, column, step_v):
            if binary[i, j] == 255 and mask[i, j] == 0:
                # get connected area
                # region = util.boundary_bfs_connected_area(binary, i, j, mask)

                mask_copy = mask.copy()
                ff = cv2.floodFill(
                    binary, mask, (j, i), None, 0, 0, cv2.FLOODFILL_MASK_ONLY
                )
                if ff[0] < min_obj_area:
                    continue
                mask_copy = mask - mask_copy
                region = np.reshape(
                    cv2.findNonZero(mask_copy[1:-1, 1:-1]), (-1, 2)
                )
                region = [(p[1], p[0]) for p in region]

                # filter out some compos
                component = Component(region, binary.shape)
                # calculate the boundary of the connected area
                # ignore small area
                if component.width <= 3 or component.height <= 3:
                    continue
                # check if it is line by checking the length of edges
                # if component.compo_is_line(line_thickness):
                #     continue

                if test:
                    print("Area:%d" % (len(region)))
                    draw_boundary([component], binary.shape, show=True)

                compos_all.append(component)

                if rec_detect:
                    # rectangle check
                    if component.compo_is_rectangle(
                        min_rec_evenness, max_dent_ratio
                    ):
                        component.rect_ = True
                        compos_rec.append(component)
                    else:
                        component.rect_ = False
                        compos_nonrec.append(component)

                if show:
                    print("Area:%d" % (len(region)))
                    draw_boundary(compos_all, binary.shape, show=True)

    # draw_boundary(compos_all, binary.shape, show=True)
    if rec_detect:
        return compos_rec, compos_nonrec
    else:
        return compos_all


def nested_components_detection(
    grey,
    grad_thresh,
    line_thickness,
    min_rec_evenness,
    max_dent_ratio,
    step_h=10,
    step_v=10,
    show=False,
):
    """
    :param grad_thresh:
    :param show:
    :param step_h:
    :param step_v:
    :param line_thickness:
    :param max_dent_ratio:
    :param min_rec_evenness:
    :param grey: grey-scale of original image
    :return: corners: list of [(top_left, bottom_right)]
                        -> top_left: (column_min, row_min)
                        -> bottom_right: (column_max, row_max)
    """
    compos = []
    mask = np.zeros((grey.shape[0] + 2, grey.shape[1] + 2), dtype=np.uint8)
    broad = np.zeros((grey.shape[0], grey.shape[1], 3), dtype=np.uint8)
    broad_all = broad.copy()

    row, column = grey.shape[0], grey.shape[1]
    for x in range(0, row, step_h):
        for y in range(0, column, step_v):
            if mask[x, y] == 0:
                # region = flood_fill_bfs(grey, x, y, mask)

                # flood fill algorithm to get background (layout block)
                mask_copy = mask.copy()
                ff = cv2.floodFill(
                    grey,
                    mask,
                    (y, x),
                    None,
                    grad_thresh,
                    grad_thresh,
                    cv2.FLOODFILL_MASK_ONLY,
                )
                # ignore small regions
                if ff[0] < 500:
                    continue
                mask_copy = mask - mask_copy
                region = np.reshape(
                    cv2.findNonZero(mask_copy[1:-1, 1:-1]), (-1, 2)
                )
                region = [(p[1], p[0]) for p in region]

                compo = Component(region, grey.shape)

                if compo.height < 30:
                    continue

                if compo.area / (row * column) > 0.9:
                    continue
                elif compo.area / (row * column) > 0.7:
                    compo.redundant = True

                # get the boundary of this region
                # ignore lines
                if compo.compo_is_line(line_thickness):
                    continue
                # ignore non-rectangle as blocks must be rectangular
                if not compo.compo_is_rectangle(
                    min_rec_evenness, max_dent_ratio
                ):
                    continue
                # if block.height/row < min_block_height_ratio:
                #     continue
                compos.append(compo)
    if show:
        cv2.imshow("Flood-fill all", broad_all)
        cv2.imshow("Block", broad)
        cv2.waitKey()
    return compos


def nesting_inspection(
    grey,
    compos,
    ffl_block,
    line_thickness,
    min_rec_evenness,
    max_dent_ratio,
    show=False,
):
    """
    Inspect all big compos through block division by flood-fill
    :param show:
    :param max_dent_ratio:
    :param min_rec_evenness:
    :param line_thickness:
    :param grey:
    :param compos:
    :param ffl_block: gradient threshold for flood-fill
    :return: nesting compos
    """
    nesting_compos = []
    for i, compo in enumerate(compos):
        if compo.height > 50:
            replace = False
            clip_grey = compo.compo_clipping(grey)
            n_compos = nested_components_detection(
                clip_grey,
                grad_thresh=ffl_block,
                line_thickness=line_thickness,
                min_rec_evenness=min_rec_evenness,
                max_dent_ratio=max_dent_ratio,
                show=show,
            )
            cvt_compos_relative_pos(
                n_compos, compo.bbox.col_min, compo.bbox.row_min
            )

            for n_compo in n_compos:
                if n_compo.redundant:
                    compos[i] = n_compo
                    replace = True
                    break
            if not replace:
                nesting_compos += n_compos
    return nesting_compos


def transform_img(image: np.ndarray, image_shape) -> np.ndarray:
    """
    Transform function, resizes input images to fit in the network input size

    Args:
        image: input image
        image_shape: shape of resize

    Returns:
        resized and normalized array of image
    """
    image_resized: np.ndarray = cv2.resize(image, image_shape[:2])
    image_resized_normalized: np.ndarray = (image_resized / 255).astype(
        "float32"
    )
    image_resized_normalized = np.array([image_resized_normalized])
    return image_resized_normalized
