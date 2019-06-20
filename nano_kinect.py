# coding: utf-8

# An example using startStreams

import numpy as np
import cv2
import sys
import time
import tensorflow as tf
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame


try:
    from pylibfreenect2 import OpenGLPacketPipeline
    pipeline = OpenGLPacketPipeline()
except:
    try:
        from pylibfreenect2 import OpenCLPacketPipeline
        pipeline = OpenCLPacketPipeline()
    except:
        from pylibfreenect2 import CpuPacketPipeline
        pipeline = CpuPacketPipeline()
#print("Packet pipeline:", type(pipeline).__name__)

enable_rgb = True
enable_depth = True

fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No device connected!")
    sys.exit(1)

serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)

types = 0
if enable_rgb:
    types |= FrameType.Color
if enable_depth:
    types |= (FrameType.Ir | FrameType.Depth)
listener = SyncMultiFrameListener(types)

# Register listeners
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)

if enable_rgb and enable_depth:
    device.start()
else:
    device.startStreams(rgb=enable_rgb, depth=enable_depth)


from darkflow.net.build import TFNet
config = tf.ConfigProto(log_device_placement=True)
config.gpu_options.allow_growth = True
with tf.Session(config=config) as sess:
    options = {
            'model': 'cfg/yolov2-tiny-voc.cfg',
            'load': 'bin/yolov2-tiny-voc.weights',
            'threshold': 0.2,
            'gpu': 1.0
                    }
    tfnet = TFNet(options)

colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]


while True:
    stime = time.time()
    frames = listener.waitForNewFrame()

    if enable_rgb:
        frame = frames["color"]
        frame = cv2.resize(frame.asarray(),(int(1920 / 2), int(1080 / 2)))
        frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2RGB)

    if enable_depth:
        framed = frames["depth"]
        frameD = framed.asarray()
        frameDepth = framed.asarray()
        frameDepth = np.reshape(frameDepth,(424, 512))
        frameD = frameD.astype(np.uint8)
        frameD = cv2.cvtColor(frameD,cv2.COLOR_GRAY2RGB)

    def click_event (event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, y,)
            print(int(frameDepth[y][x]))

    results = tfnet.return_predict(frame)
    for color1, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            x_Center = int((((result['topleft']['x']) + (result['bottomright']['x']))/2))
            y_Center = int((((result['topleft']['y']) + (result['bottomright']['y']))/2))
            #Tweek on 'x_Center /1.42) -115' to adjust alignment
            Center = (int(x_Center /1.42) -115, int(y_Center *.8))
            CenterC = int(x_Center), int(y_Center)
            Pixel = frameDepth[int(y_Center * .8)]
            #this 'x_Center /1.42) -115' must be same as above if changed
            Pixel_Depth = Pixel[int(x_Center /1.42) -115]
            label = result['label']
            confidence = result['confidence']
            text = '{}: {:.0f}%'.format(label, confidence * 100)
            textD = 'Depth{} mm'.format(int(Pixel_Depth))
            frame = cv2.rectangle(frame, tl, br, color1, 5)
            frameD = cv2.circle(frameD, Center, 10, color1, -1)
            frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            frame = cv2.putText(frame, textD,CenterC, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('frame', frame)
    cv2.imshow('frameD', frameD) 
    cv2.setMouseCallback('frameD', click_event)
    print('FPS {:.1f}'.format(1 / (time.time() - stime)))
    listener.release(frames)

    key = cv2.waitKey(delay=1)
    if key == ord('q'):
        break

device.stop()
device.close()

sys.exit(0)
