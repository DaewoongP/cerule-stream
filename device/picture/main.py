from time import sleep
from picamera import PiCamera
import datetime

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
    now = datetime.datetime.now()
    camera.capture('capture/{}.jpg' % now)


client = paho.Client()

client.message_callback_add("mqtt/size", on_size)#callback to function
event

client.connect("localhost", 1883)#broker set
client.subscribe("mqtt/#")#sub 'ptz'

client.loop_forever()

