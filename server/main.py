import argparse
import subprocess as sp
import time
import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import cv2
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
parser.add_argument('-i', '--input-url', default="rtsp://localhost:5454/live.rtsp", type=str,
                    metavar='PATH', help='url used to open a rtsp streaming')
parser.add_argument('-o', '--output-url', default="rtmp://localhost:1935/hls/live", type=str,
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


def stream_factory(output_url, width, height, fps):
    output_command = ['ffmpeg',
                      '-f', 'rawvideo',
                      '-vcodec', 'rawvideo',
                      '-s', '{}x{}'.format(int(width), int(height)),  # size of one frame
                      '-pix_fmt', 'rgb24',
                      '-r', '{}'.format(fps),  # frames per second
                      '-i', '-',  # The input comes from a pipe
                      '-an',  # Tells FFMPEG not to expect any audio
                      '-vcodec', 'libx264',
                      '-f', 'flv',
                      '{}'.format(output_url)]
    return output_command


def system_message(object, userdata, msg):
    print("{}: {}".format(msg.topic, msg.payload.decode('utf-8')))


def prep_image(img, inp_dim):
    """ Prepare image for inputting to the neural network.
    Returns a Variable
    """
    orig_im = img
    dim = orig_im.shape[1], orig_im.shape[0]
    img = cv2.resize(orig_im, (inp_dim, inp_dim))
    img_ = img[:, :, ::-1].transpose((2, 0, 1)).copy()
    img_ = torch.from_numpy(img_).float().div(255.0).unsqueeze(0)
    return img_, orig_im, dim


def write(x, img, classes, colors):
    c1 = tuple(x[1:3].int())
    c2 = tuple(x[3:5].int())
    cls = int(x[-1])
    label = "{0}".format(classes[cls])
    color = random.choice(colors)
    cv2.rectangle(img, c1, c2,color, 1)
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
    c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
    cv2.rectangle(img, c1, c2,color, -1)
    cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 1);
    return img


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
    cap = cv2.VideoCapture(args.input_url)

    assert cap.isOpened(), 'Cannot capture source {}'.format(args.input_url)

    # Inspect input stream
    input_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    input_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    input_fps = cap.get(cv2.CAP_PROP_FPS)
    print("[input stream] width: {}, height: {}, fps: {}".format(input_width, input_height, input_fps))

    # Open output stream
    output_command = stream_factory(args.output_url, input_width, input_height, input_fps)
    print(output_command)
    output_stream = sp.Popen(output_command, stdin=sp.PIPE, stderr=sp.PIPE)

    frames = 0
    start = time.time()

    while cap.isOpened():
        ret, frame = cap.read()  # frame size: 640x360x3(=691200)
        if ret:
            # Our detect operations on the frame come here

            img, orig_im, dim = prep_image(frame, inp_dim)

            if CUDA:
                im_dim = im_dim.cuda()
                img = img.cuda()

            output = model(Variable(img), CUDA)
            output = write_results(output, confidence, num_classes, nms=True, nms_conf=nms_thesh)

            if type(output) == int:
                frames += 1
                print("FPS of the video is {:5.2f}".format(frames / (time.time() - start)))
                cv2.imshow("frame", orig_im)
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
                continue

            output[:, 1:5] = torch.clamp(output[:, 1:5], 0.0, float(inp_dim)) / inp_dim

            output[:, [1, 3]] *= frame.shape[1]
            output[:, [2, 4]] *= frame.shape[0]

            classes = load_classes('yolo/data/coco.names')
            colors = pkl.load(open("yolo/pallete", "rb"))

            # Overlay on screen
            list(map(lambda x: write(x, orig_im, classes, colors), output))
            # Send a BBoxes

            # Display the resulting frame
            cv2.imshow("frame", orig_im)
            print(orig_im.size)
            frames += 1
            print("FPS of the video is {:5.2f}".format(frames / (time.time() - start)))

            # Write rtmp stream
            output_stream.stdin.write(frame.tostring())
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

