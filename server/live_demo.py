import argparse
import subprocess as sp
import time
import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
from yolo.util import *
from yolo.darknet import Darknet
from yolo.preprocess import prep_image, inp_to_image
import pandas as pd
import random
import argparse
import pickle as pkl
import cv2

import paho.mqtt.client as paho


parser = argparse.ArgumentParser(description="cerule-stream object detection server.")
parser.add_argument('-b', '--broker-url', default="safecorners.io:1883", type=str,
                    metavar='PATH', help='mqtt broker address')
parser.add_argument('-i', '--input-url', default='rtsp://localhost:5454/live.rtsp', type=str,
                    metavar='PATH', help='url used to open a rtsp streaming')
parser.add_argument('-o', '--output-url', default='rtmp://localhost:1935/hls/live', type=str,
                    metavar='PATH', help='url used to set up rtmp streaming')
parser.add_argument('--config-file', default="yolo/cfg/yolov3.cfg", type=str,
                    metavar='PATH', help='config file defined a yolo layers')
parser.add_argument('--weights-file', default="yolo/weights/yolov3.weights", type=str,
                    metavar='PATH', help="yolo pretrained weight file")
parser.add_argument("--confidence", dest="confidence", help="Object Confidence to filter predictions", default=0.25)
parser.add_argument("--nms_thresh", dest="nms_thresh", help="NMS Threshhold", default=0.4)
parser.add_argument("--reso", dest='reso', help="Input resolution of the network. Increase to increase accuracy. Decrease to increase speed",
                    default="160", type=str)
parser.add_argument('--num_classes', default=80, type=int)


def system_message(object, userdata, msg):
    print("{}: {}".format(msg.topic, msg.payload.decode('utf-8')))


def main():
    global args
    args = parser.parse_args()

    # Yolo
    confidence = float(args.confidence)
    nms_thesh = float(args.nms_thresh)
    start = 0
    CUDA = torch.cuda.is_available()

    num_classes = 80
    bbox_attrs = 5 + num_classes
    model = Darknet(args.config_file)
    model.load_weights(args.weights_file)

    model.net_info["height"] = args.reso
    inp_dim = int(model.net_info["height"])

    assert inp_dim % 32 == 0
    assert inp_dim > 32

    if CUDA:
        model.cuda()

    model.eval()

    # Connect
    client = paho.Client()
    host, port = args.broker_url.split(':')
    client.connect(host, int(port))

    # subscribe a system messages
    client.message_callback_add("$SYS/#", system_message)
    client.subscribe("$SYS/#")

    # Open rtsp stream
    cap = cv2.VideoCapture(0)

    assert cap.isOpened(), 'Cannot capture source {}'.format(args.input_url)

    # Inspect input stream
    input_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    input_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    input_fps = cap.get(cv2.CAP_PROP_FPS)
    print("[input stream] width: {}, height: {}, fps: {}".format(input_width, input_height, input_fps))

    while cap.isOpened():
        ret, frame = cap.read()  # frame size: 640x360x3(=691200)
        if ret:
            # Our detect operations on the frame come here

            # Send a BBoxes

            # Overlay on screen


            # Display the resulting frame
            cv2.imshow('frame', frame)
            print(frame.size)
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close
    cap.release()
    cv2.destroyAllWindows()
    client.disconnect()


if __name__ == '__main__':
    main()

