# get image from webcam
# openCV image processing
# serial signals to arduino
# http request to server
import cv2 # using openCV library
import requests # for http request
import os
import datetime
import serial # for communication with Arduino
from stream_stability import check_stream_stability

# declare
server_url = 'http://172.20.10.3:5000/process_image' 
arduino = '/dev/ttyUSB0'

def imageCapture():
    # image capture
    ret, frame = cam.read()
    if(ret):
        return frame

def imageProcess(cam):
    # image Process
    # if object exists and to be classified, return true
    isStable, frame = check_stream_stability(cam, MOTION_THRESHOLD=5000)
    return isStable, frame

def signal(c):
    # send signal to arduino
    #!/usr/bin/env python3
    ser = serial.Serial(arduino, 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        ser.write(c.encode('utf-8'))
        line = ser.readline().decode('utf-8').rstrip()
        if(line == 'F'):
            return True
        else: continue

def httpRequest(frame):
    # send image and request classification result
    f = cv2.imencode('.jpg', frame) #.tostring() # convert cv2 to jpg
    files = {'image': ('filename.jpg', f, 'image/jpeg')}
    start = datetime.datetime.now()
    response = requests.post(server_url, files=files) # request for result
    end = datetime.datetime.now()
    # print("Response time: {} ms".format(int((end-start).microseconds/1000)))

    if response.status_code == 200:
        result = response.json()['result']
        return result
    else:
        return "NULL"

if __name__ == "__main__":
    cam = cv2.VideoCapture(0) # setup cam
    while(True):
        # check stability
        proceed, pic = imageProcess(cam=cam)
        if(proceed):
            result = httpRequest(frame=pic)
        else:
            continue

        # communicate with Arduino
        if(result == 'L'):
            finish = signal('L')
        elif(result == 'R'):
            finish = signal('R')
        else:
            continue
    cam.release()
    cv2.destroyAllWindows()