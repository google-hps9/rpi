import cv2
import numpy as np
import queue
import datetime

BUFFER_SIZE = 5
DIFF_THRESHOLD = 30

buffer = queue.Queue(maxsize=BUFFER_SIZE)


def check_stream_stability(cap, MOTION_THRESHOLD=3000):
    ret, frame = cap.read()

    return True, frame 

    start = datetime.datetime.now()


    global buffer
    while not buffer.full():
        ret, frame = cap.read()
        buffer.put(frame)


    ret, curr_frame = cap.read()

    average_frame = np.mean(list(buffer.queue), axis=0).astype(np.uint8)

    diff_frame = cv2.absdiff(curr_frame, average_frame)

    _, thresholded_frame = cv2.threshold(diff_frame, DIFF_THRESHOLD, 255, cv2.THRESH_BINARY)
    motion_pixels = np.count_nonzero(thresholded_frame == 255)
    print("motion pixels:",motion_pixels)


    cv2.imshow('Original Frame', curr_frame)
    cv2.imshow('Tresholded Frame Difference with Buffer', thresholded_frame)

    buffer.get()
    buffer.put(curr_frame)

    end = datetime.datetime.now()
    # print("check stability time: {} ms".format(int((end-start).microseconds/1000)))
    if motion_pixels > MOTION_THRESHOLD:
        # print("Motion Detected !!!")
        return False, curr_frame
    # print("Stable !!!")
    return True, curr_frame


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    print(type(cap))
    check_stream_stability(cap)
