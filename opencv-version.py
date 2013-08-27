import time
import struct
import Quartz.CoreGraphics as CG
import numpy as np
import copy
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
from cv2 import *
import itertools
import random
import math
import sys

xxxx = ''


def mouseEvent(type, posx, posy):
    theEvent = CGEventCreateMouseEvent(None, type, (posx, posy), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, theEvent)


def mousemove(posx, posy):
    mouseEvent(kCGEventMouseMoved, posx, posy)


def mouseclick(posx, posy):
        #  uncomment this line if you want to force the mouse
        #  to MOVE to the click location first (I found it was not necessary).
        #mouseEvent(kCGEventMouseMoved, posx,posy);
    mouseEvent(kCGEventLeftMouseDown, posx, posy)
    mouseEvent(kCGEventLeftMouseUp, posx, posy)


class ScreenPixel(object):
    """Captures the screen using CoreGraphics, and provides access to
    the pixel values.
    """

    def capture(self, region=None):
        global xxxx

        if region is None:
            region = CG.CGRectInfinite

        # Create screenshot as CGImage
        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        # Intermediate step, get pixel data as CGDataProvider
        prov = CG.CGImageGetDataProvider(image)

        # Copy data out of CGDataProvider, becomes string of bytes
        self._data = CG.CGDataProviderCopyData(prov)
        xxxx = self._data

if __name__ == '__main__':
    # Timer helper-function
    import contextlib
    part_y1 = 22
    part_x1 = 0
    part_x2 = 536
    part_y2 = 379

    part_y1 = 294
    part_x1 = 50
    part_x2 = 586
    part_y2 = 650
    score_x1 = 0
    score_y1 = 3
    score_x2 = 64
    score_y2 = 11
    box = (part_x1, part_y1, part_x2, part_y2)
    box2 = (score_x1, score_y1, score_x2, score_y2)
    answers_bell = []
    answers_rabbit = []
    answers_bird = []
    not_answers = []
    time_s = 0
    last_x = 0
    last_y = 0
    last_gap = -1
    last_max = 0
    the_one = 0

    @contextlib.contextmanager
    def timer(msg):
        start = time.time()
        yield
        end = time.time()
        print "%s: %.02fms" % (msg, (end - start) * 1000)

    def get_img_array(box):
        if box[2] - box[0] < (box[3] - box[1]) * 1.6:
            region = CG.CGRectMake(box[0], box[1], (box[3] - box[1]) * 1.6, box[3] - box[1])
        else:
            region = CG.CGRectMake(box[0], box[1], box[2] - box[0],  (box[2] - box[0]) / 1.6)
        sp.capture(region=region)
        pixel_size = len(xxxx) / 4
        #img1 = imread("/Users/selfdir/Documents/littlerabbit/material/1.png")
        nparr = np.fromstring(xxxx, np.uint8)
        nparr = np.reshape(nparr, (-1, 4))
        nparr = np.delete(nparr, 3, 1)
        if box[2] - box[0] < (box[3] - box[1]) * 1.6:
            nparr = np.reshape(nparr, (box[3] - box[1], pixel_size / (box[3] - box[1]), 3))
            nparr = nparr[0:box[3] - box[1], 0:box[2] - box[0]]
        else:
            nparr = np.reshape(nparr, ((box[2] - box[0]) / 1.6, pixel_size / (box[2] - box[0]) * 1.6, 3))
            nparr = nparr[0:box[3] - box[1], 0:box[2] - box[0]]
        return nparr

    sp = ScreenPixel()
    up_rabbit_1 = imread("/Users/selfdir/Documents/littlerabbit/xxx.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
    up_rabbit_1 = up_rabbit_1[::2, ::2]
    up_rabbit_2 = imread("/Users/selfdir/Documents/littlerabbit/xxx2.png", cv.CV_LOAD_IMAGE_GRAYSCALE)
    up_rabbit_2 = up_rabbit_2[::2, ::2]
    stand_bell = imread("/Users/selfdir/Documents/littlerabbit/stand/stand_bell.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
    stand_bell = threshold(stand_bell, 128, 255, THRESH_BINARY)[1]
    stand_bell, hierarchy = findContours(stand_bell, RETR_TREE, CHAIN_APPROX_SIMPLE)
    stand_bell = stand_bell[0]

    while True:
        with timer("onecost"):
            nparr = get_img_array(box)
            #element = getStructuringElement(MORPH_RECT, (2, 2))
            #nptemp = erode(nptemp, element)
            nparr_temp = nparr[118:245:2, ::2]
            nparr_temp = cvtColor(nparr_temp, COLOR_BGR2GRAY)
            divide_numb = 0.73
            if sys.argv[1] == 'left':
                result1 = matchTemplate(up_rabbit_1, nparr_temp, TM_CCOEFF_NORMED).max()
                if result1 < divide_numb:
                    the_one = up_rabbit_1
                    continue
            elif sys.argv[1] == 'right':
                result2 = matchTemplate(up_rabbit_2, nparr_temp, TM_CCOEFF_NORMED).max()
                if result2 < divide_numb:
                    the_one = up_rabbit_2
                    continue
            else:
                result2 = matchTemplate(up_rabbit_2, nparr_temp, TM_CCOEFF_NORMED).max()
                if result2 < divide_numb:
                    result1 = matchTemplate(up_rabbit_1, nparr_temp, TM_CCOEFF_NORMED).max()
                    if result1 < divide_numb:
                        continue
                    else:
                        the_one = up_rabbit_1
                else:
                    the_one = up_rabbit_2
            '''nparr = get_img_array(box)
            nparr_temp = nparr[118:245:2, ::2]
            nparr_temp = cvtColor(nparr_temp, COLOR_BGR2GRAY)
            k = 0
            while matchTemplate(the_one, nparr_temp, TM_CCOEFF_NORMED).max() > divide_numb * 1.03 and k < 3:
                #time.sleep(random.random() * 0.008)
                k += 1
                nparr = get_img_array(box)
                nparr_temp = nparr[118:245:2, ::2]
                nparr_temp = cvtColor(nparr_temp, COLOR_BGR2GRAY)'''
            wrong_check = True
            while wrong_check:
                nparr2 = copy.deepcopy(nparr)
                nparr = cvtColor(nparr, COLOR_BGR2GRAY)
                nparr = threshold(nparr, 128, 255, THRESH_BINARY)[1]
                element = getStructuringElement(MORPH_RECT, (4, 4))
                nparr = erode(nparr, element)
                contours, hierarchy = findContours(nparr, RETR_TREE, CHAIN_APPROX_SIMPLE)
                for i in contours:
                    x, y, w, h = boundingRect(i)
                    #rectangle(nparr, (x, y), (x + w, y + h), (255, 0, 0), 1)
                    #hu_temp = HuMoments(moments(i))
                    #print -np.sign(hu_temp) * np.log10(np.abs(hu_temp))
                    if y < 4 or y + h > part_y2 - part_y1 - 5:
                        continue
                    temp_area = contourArea(i)
                    if temp_area < 10:
                        continue
                    if temp_area < 15:
                        time_s = 1001
                    if time_s <= 1000:
                        if matchShapes(i, stand_bell, cv.CV_CONTOURS_MATCH_I1, 0) < 0.35 and w < h:
                            answers_bell.append([x, y, w, h])
                            #rectangle(nparr2, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        else:
                            not_answers.append([x, y, w, h])
                    else:
                        if temp_area < 25:
                            answers_bell.append([x, y, w, h])
                            #rectangle(npori, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        else:
                            not_answers.append([x, y, w, h])
                        #rectangle(npori, (x, y), (x + w, y + h), (0, 0, 255), 1)
                wrong_check = False
                if len(not_answers) > 2 or len(not_answers) == 0:
                    wrong_check = True
                    answers_bell = []
                    answers_rabbit = []
                    answers_bird = []
                    not_answers = []
                    nparr = get_img_array(box)
            if len(not_answers) == 1:
                answers_rabbit = not_answers[0]
                #rectangle(nparr2, (answers_rabbit[0], answers_rabbit[1]), (answers_rabbit[0] + answers_rabbit[2], answers_rabbit[1] + answers_rabbit[3]), (0, 0, 255), 2)
            if len(not_answers) == 2:
                if not_answers[0][2] * not_answers[0][3] > not_answers[1][2] * not_answers[1][3]:
                    answers_rabbit = not_answers[0]
                    answers_bird = not_answers[1]
                else:
                    answers_rabbit = not_answers[1]
                    answers_bird = not_answers[0]
                #rectangle(nparr2, (answers_rabbit[0], answers_rabbit[1]), (answers_rabbit[0] + answers_rabbit[2], answers_rabbit[1] + answers_rabbit[3]), (0, 0, 255), 2)
                #rectangle(nparr2, (answers_bird[0], answers_bird[1]), (answers_bird[0] + answers_bird[2], answers_bird[1] + answers_bird[3]), (0, 255, 0), 2)
            if answers_rabbit:
                print "find rabbit"
                target_bell = []
                temp_incr = 0
                for i in answers_bell:
                    temp_incr += 1
                    if i[1] < answers_rabbit[1] + 90 and (i[1] + i[3] - answers_bell[-1][1] - answers_bell[-1][3]) % 57 <= (i[1] + i[3] - answers_bell[-1][1] - answers_bell[-1][3]) / 57:
                        target_bell = i
                        break
                if temp_incr > 2:
                    for i in answers_bell:
                        if i[1] < answers_rabbit[1] + 90 and (i[1] + i[3] - answers_bell[-2][1] - answers_bell[-2][3]) % 57 <= (i[1] + i[3] - answers_bell[-2][1] - answers_bell[-2][3]) / 57:
                            target_bell = i
                            break
                if target_bell:
                    if target_bell[0] - answers_rabbit[0] > 4:
                        last_gap = 1
                        mousemove(part_x1 + 3 + target_bell[0] + target_bell[2] + math.pow((target_bell[0] - answers_rabbit[0]), 1.8) * 0.00035, part_y2 - 30)
                        last_x = target_bell[0]
                        last_y = target_bell[1]
                    elif answers_rabbit[0] - target_bell[0] > 4:
                        last_gap = 0
                        mousemove(part_x1 + target_bell[0] - math.pow((answers_rabbit[0] - target_bell[0]), 1.8) * 0.00035, part_y2 - 30)
                        last_x = target_bell[0]
                        last_y = target_bell[1]
            answers_bell = []
            answers_rabbit = []
            answers_bird = []
            not_answers = []
            #imshow("window", npori)
            #if waitKey(0) == 27:
             #   destroyAllWindows()
