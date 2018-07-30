import argparse
import subprocess as sp

import cv2

import paho.mqtt.client as paho


parser = argparse.ArgumentParser(description="cerule-stream object detection server.")
parser.add_argument('-b', '--broker-url', default="safecorners.io:1883", type=str,
                    metavar='PATH', help='mqtt broker address')
parser.add_argument('-i', '--input-url', default='rtsp://localhost:5454/live.rtsp', type=str,
                    metavar='PATH', help='url used to open a rtsp streaming')
parser.add_argument('-o', '--output-url', default='rtmp://localhost:1935/dash/live', type=str,
                    metavar='PATH', help='url used to set up rtmp streaming')


def stream_factory(output_url, width, height, fps):
    output_command = ['ffmpeg',
                      '-f', 'rawvideo',
                      '-vcodec', 'rawvideo',
                      '-s', '{}x{}'.format(width, height),  # size of one frame
                      '-pix_fmt', 'rgb24',
                      '-r', fps,  # frames per second
                      '-i', '-',  # The input comes from a pipe
                      '-an',  # Tells FFMPEG not to expect any audio
                      '-vcodec', 'libx264',
                      '-f', 'flv',
                      output_url]
    return output_command


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
    cap = cv2.VideoCapture(args.input_url)

    assert cap.isOpened(), 'Cannot capture source {}'.format(args.input_url)

    # Inspect input stream
    input_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    input_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    input_fps = cap.get(cv2.CAP_PROP_FPS)
    print("[input stream] width: {}, height: {}, fps: {}".format(input_width, input_height, input_fps))

    # Open output stream
    output_command = stream_factory(args.output_url, input_width, input_height, input_fps)
    output_stream = sp.Popen(output_command, stdin=sp.PIPE, stderr=sp.PIPE)

    while cap.isOpened():
        ret, frame = cap.read()  # frame size: 640x360x3(=691200)
        if ret:
            # Our detect operations on the frame come here

            # Send a BBoxes

            # Overlay on screen


            # Display the resulting frame
            cv2.imshow('frame', frame)
            print(frame.size)
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

