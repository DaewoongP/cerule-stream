import argparse
import subprocess as sp

import paho.mqtt.client as paho


parser = argparse.ArgumentParser(description="cerule-stream object detection server.")
parser.add_argument('-b', '--broker-url', default="safecorners.io:1883", type=str,
                    metavar='PATH', help='mqtt broker address')
parser.add_argument('-i', '--input-url', default='http://localhost:8090/feed1.ffm', type=str,
                    metavar='PATH', help='url used to open a rtsp streaming')
parser.add_argument('-o', '--output-url', default='http://localhost:8090/feed1.ffm', type=str,
                    metavar='PATH', help='url used to set up rtmp streaming')


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
    client.message_callback_add("$SYS/#", system_message)
    client.subscribe("$SYS/#")

    # Open rtsp stream

    # Send a BBoxes

    # Overlay on screen

    # Write rtmp stream

    # Loop
    client.loop_forever()


if __name__ == '__main__':
    main()

