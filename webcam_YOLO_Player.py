import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
import tensorflow as tf

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
Cap = cv2.VideoCapture('/home/joev/Videos/Color_Video.mp4')
writerC = cv2.VideoWriter('/home/joev/Videos/YOLO_Video.mp4', cv2.VideoWriter_fourcc(*'XVID'),8, (640, 480))

if Cap.isOpened() == False:
    print(
        "Error opening the video file. Please double check your file path for typos. Or move the movie file to the same location as this script/notebook")

# While the video is opened
while Cap.isOpened():

    # Read the video file.
    ret, frameC = Cap.read()
    stime = time.time()
    if ret == True:
        frameC = cv2.resize(frameC, (640, 480))
        results = tfnet.return_predict(frameC)
        for color, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            x_Center = int((((result['topleft']['x']) + (result['bottomright']['x'])) / 2))
            y_Center = int((((result['topleft']['y']) + (result['bottomright']['y'])) / 2))
            label = result['label']
            confidence = result['confidence']
            text = '{}:{:.0f}%'.format(label, confidence * 100)
            frameC = cv2.rectangle(frameC, tl, br, color, 5)
            frameC = cv2.putText(frameC, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        writerC.write(frameC)
        cv2.imshow('frameC', frameC)
        print('FPS {:.1f}'.format(1 / (time.time() - stime)))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()

