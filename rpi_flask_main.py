from flask import Flask, request,Response, jsonify, render_template
import numpy as np
import datetime
import os
import cv2
import threading
import requests # for http request
import serial # for communication with Arduino
from stream_stability import check_stream_stability
import time

# declare 
arduino = '/dev/ttyUSB0'
app = Flask(__name__)
app.debug = True

@app.route('/captured_image')
def getCapturedImage():
    
    # check stability
    cam = cv2.VideoCapture(0)
    while True:
        isStable, frame = imageProcess() 
        if isStable:
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                return Response(buffer.tobytes(), mimetype='image/jpeg')
    
    return 'Failed to capture image', 500


@app.route('/arduino_signal', methods=['POST'])
def sendArduinoSignal():
    
    result = request.form.get('text_data')

    finish = False
    # communicate with Arduino
    if(result == 'L'):
        finish = signal('L')
    elif(result == 'R'):
        finish = signal('R')
    elif(result == 'T'):
        finish == signal('T')

    print("arduino signal has been sent:",result)
    return jsonify({'done':finish})


def imageProcess():
    # image Process
    # if object exists and to be classified, return true
    isStable, frame = check_stream_stability(5000)

def signal(c):
    # send signal to arduino
    #!/usr/bin/env python3
    ser = serial.Serial(arduino, 9600, timeout=1)
    ser.reset_input_buffer()
    time.sleep(5)
    ser.write(c.encode('utf-8'))
    while True:
        line = ser.readline().decode('utf-8').rstrip()
        if(line == 'F'):
            return True
        else: continue
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5555)

