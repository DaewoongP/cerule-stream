import argparse
import subprocess as sp

import paho.mqtt.client as paho

import json
import time

parser = argparse.ArgumentParser(description="PtzCamera")
parser.add_argument('-b', '--broker-url', default="safecorners.io:1883", type=str,
                    metavar='PATH', help='mqtt broker address')
parser.add_argument('-o', '--output-url', default='http://localhost:8090/feed1.ffm', type=str,
                    metavar='PATH', help='url used to set up rtsp streaming')


def execute_ffmpeg(output_url):
    command = ['ffmpeg',
               '-f', 'video4linux2',
               '-i', '/dev/video0',
               output_url]
    print(command)
    pipe = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)


def system_message(object, userdata, msg):
    print("{}: {}".format(msg.topic, msg.payload.decode('utf-8')))


def main():
    global args
    args = parser.parse_args()

    # Connect
    client = paho.Client()
    host, port = args.broker_url.split(':')
    client.connect(host, int(port))

    # subscribe a system messages
    client.message_callback_add("SYS/#", system_message)
    client.subscribe("SYS/#")

    # Instantiate ptz module

    # Streaming
    execute_ffmpeg(args.output_url)

    # Loop
    client.loop_forever()


if __name__ == '__main__':
    main()
