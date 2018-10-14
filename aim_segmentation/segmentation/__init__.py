import base64
import cv2
import numpy as np
from skimage import img_as_ubyte
from skimage.filters import rank
from skimage.morphology import  disk
from skimage.feature import canny
import segmentation.utils as utils

def get_elements(b64, detailed=True, preview=True):
    img_bgr = utils.read_b64_img(b64)
    img_out = np.copy(img_bgr)

    contours_all_v, contours_all_h = segment(img_bgr, h_blur=13, v_blur=9)

    thickness = 1
    if detailed:
        contours_all = contours_all_h
    else:
        contours_all = contours_all_v
        thickness = 2

    offset, offset1 = 3, 5

    elements = []
    N = len(contours_all)
    for i, c in zip(range(N), contours_all):
        x, y, w, h = cv2.boundingRect(c)

        if w <= 15:
            continue
        if h <= 10:
            continue

        img_out = cv2.rectangle(img_out, (x, y), (x + w, y + h), (0, 0, 255), thickness)

        ele_b64 = base64.b64encode(cv2.imencode(".png", img_bgr[y:y+h, x:x+w])[1])

        elements.append({
            "id": i,
            "tag": "",
            "x_position": x,
            "y_position": y,
            "width": w,
            "height": h,
            "b64": ele_b64
        })

    result = {
        "elements": elements
    }

    if preview:
        b64 = base64.b64encode(cv2.imencode(".png", img_out)[1])
        result["preview"] = b64

    return result

def segment(img_bgr, h_blur=13, v_blur=9):
    BW = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(BW, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    denoised = rank.median(BW, disk(5))
    gradient_denoised = rank.gradient(denoised, disk(1))

    gradient_0 = rank.gradient(img_bgr[:, :, 0], disk(1))
    gradient_1 = rank.gradient(img_bgr[:, :, 1], disk(1))
    gradient_2 = rank.gradient(img_bgr[:, :, 2], disk(1))

    sobelx64f = cv2.Sobel(BW, cv2.CV_64F, 1, 0, ksize=5)
    abs_sobel64f = np.absolute(sobelx64f)
    sobel_8u = np.uint8(abs_sobel64f)
    img_canny = canny(BW)

    _, contours_thresh, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contours_0, _ = cv2.findContours(gradient_0, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contours_1, _ = cv2.findContours(gradient_1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contours_2, _ = cv2.findContours(gradient_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contours_denoised, _ = cv2.findContours(gradient_denoised, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contours_sobel, _ = cv2.findContours(sobel_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    _, contours_canny, _ = cv2.findContours(img_as_ubyte(img_canny), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contours = contours_0 + contours_1 + contours_2 + contours_denoised + contours_sobel + contours_canny

    bbox = utils.remove_overlaps(contours)

    temp = np.zeros_like(BW)

    if bbox != 0:
        for bb in bbox:
            temp = cv2.rectangle(temp, (bb.x1, bb.y1), (bb.x2, bb.y2), (255, 255, 255), 1)

    for c in contours_thresh:
        x, y, w, h = cv2.boundingRect(c)
        temp = cv2.rectangle(temp, (x, y), (x + w, y + h), (255, 255, 255), 1)

    # Horizontal Blurring filter
    size = h_blur # 11
    kmb = np.zeros((size, size))
    kmb[size / 2, :] = np.ones(size)
    kmb = kmb/size

    # Apply horizontal blurring here
    temp = cv2.filter2D(temp, -1, kmb)
    _, contours_all_h, _ = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Vertical Blurring filter
    size = v_blur # 13
    kmb = np.zeros((size, size))
    kmb[:, size / 2] = np.ones(size)
    kmb = kmb/size

    # Apply vertical blurring here
    temp = cv2.filter2D(temp, -1, kmb)
    _, contours_all_v, _ = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours_all_v, contours_all_h
