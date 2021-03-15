#!/usr/bin/env python3

import os
import cv2
import time
import datetime
import psutil
from glob import glob

SPLIT_TIME_SEC = 300
DISK_USAGE_MAX = 80

GST_STR_CAM =  'nvarguscamerasrc \
  ! video/x-raw(memory:NVMM), width=3264, height=1848, format=(string)NV12, framerate=(fraction)21/1 \
  ! nvvidconv ! video/x-raw, width=(int)1920, height=(int)1080, format=(string)BGRx \
  ! videoconvert \
  ! appsink'

GST_STR_264 = 'appsrc \
  ! autovideoconvert \
  ! omxh264enc \
  ! video/x-h264, width=(int)1920, height=(int)1080, framerate=(fraction)21/1, stream-format=(string)byte-stream \
  ! h264parse \
  ! qtmux \
  ! filesink location=movie/fr_{}.mp4'

def main():
    cap = cv2.VideoCapture(GST_STR_CAM, cv2.CAP_GSTREAMER)

    while True:
        # check disk usage and delete
        usage = psutil.disk_usage('/').percent
        if usage > DISK_USAGE_MAX:
            movie_list = sorted(glob('movie/*.mp4'))
            if len(movie_list):
                old_movie = movie_list[0]
                os.remove(old_movie)
                print(old_movie, "deleted")

        file_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out = cv2.VideoWriter(GST_STR_264.format(file_name), cv2.CAP_GSTREAMER, 0, 21.0, (1920, 1080))

        start_time = time.time()
        while (time.time() - start_time) < SPLIT_TIME_SEC:
            ret, img = cap.read()
            if ret != True:
                break

            out.write(img)
            cv2.imshow('Preview', img)

            # break check
            key = cv2.waitKey(10)
            if key == ord('q'):
                break

        else:
            out.release()
            continue
        out.release()
        break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
