import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
import tensorflow as tf
from eip import PLC

#Uncoment next 2 lines for PLC support
#I am pushing data to a PLC running CLX 5000 software
test = PLC()
test.IPAddress = "172.16.2.161"

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

capture = cv2.VideoCapture(0)
#capture.set(cv2.CAP_PROP_FRAME_WIDTH,416)
#capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 416)

while True:
    stime = time.time()
    ret, frame = capture.read()
    if ret:#quit()
        results = tfnet.return_predict(frame)
        for color, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            label = result['label']
            confidence = result['confidence']
            text = '{}: {:.0f}%'.format(label, confidence * 100)
            textCon = '{:.0f}'.format(confidence * 100)
            frame = cv2.rectangle(frame, tl, br, color, 5)
            frame = cv2.putText(
                frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow('frame', frame)
      # uncomment next 2 lines for PLC support
      # Make a String tag(YOLO_Sting) and a INT tag( YOLO_INT) in your CLX 5000 processor
        ex: test.Write("Nano_YOLO_label", label)
        ex: test.Write("Nano_YOLO_confidence", textCon)
        print('FPS {:.1f}'.format(1 / (time.time() - stime)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #Un coment line below for PLC support
test.Close()
capture.release()
cv2.destroyAllWindows()
