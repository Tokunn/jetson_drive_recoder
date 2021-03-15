#!/usr/bin/env python3

import cv2

GST_STR_CAM =  'nvarguscamerasrc \
    ! video/x-raw(memory:NVMM), width=3264, height=1848, format=(string)NV12, framerate=(fraction)21/1 \
    ! nvvidconv ! video/x-raw, width=(int)1920, height=(int)1080, format=(string)BGRx \
    ! videoconvert \
    ! appsink'

# GST_STR_264 = 'appsrc \
#   ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)NV12, framerate=(fraction)21/1 \
#   ! nvv4l2h264enc maxperf-enable=1 bitrate=8000000 \
#   ! h264parse \
#   ! qtmux \
#   ! filesink location=filename_h264.mp4'

#   ! video/x-raw, format=(string)I420, width=(int)1920, height=(int)1080 \
GST_STR_264 = 'appsrc \
  ! autovideoconvert \
  ! omxh264enc \
  ! video/x-h264, width=(int)1920, height=(int)1080, framerate=(fraction)21/1, stream-format=(string)byte-stream \
  ! h264parse \
  ! qtmux \
  ! filesink location=file_test.mp4'

  # ! video/x-raw, format=(string)I420, width=(int)1920, height=(int)1080, framerate=(fraction)21/1 \
# GST_STR_264 = 'appsrc \
#   ! autovideoconvert \
#   ! omxh264enc \
#   ! matroskamux \
#   ! filesink location=filetest.mp4'


def main():
    cap = cv2.VideoCapture(GST_STR_CAM, cv2.CAP_GSTREAMER)
    out = cv2.VideoWriter(GST_STR_264, cv2.CAP_GSTREAMER, 0, 21.0, (1920, 1080))

    while True:
        ret, img = cap.read()
        if ret != True:
            break

        out.write(img)
        cv2.imshow('Gstreamer CSI', img)

        key = cv2.waitKey(10)
        if key == ord('q'):
            break
    # out.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
