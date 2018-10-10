from time import sleep
from picamera import PiCamera
import datetime
import paho.mqtt.client as paho

camera = PiCamera()
# camera.start_preview()

# Camera Configuration
camera.framerate = 30
camera.resolution = (640, 480)
fps = 1 / camera.framerate

# Camera warm-up time
sleep(2)
while True:
    sleep(fps)
    capture_time = datetime.datetime.now()
    img_name = "{}-{}-{}-{}.jpg".format(capture_time.hour, capture_time.minute, capture_time.second, capture_time.microsecond))
    camera.capture(img_name)

# camera.stop_preview()