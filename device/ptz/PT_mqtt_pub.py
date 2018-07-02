import paho.mqtt.client as paho

import time

client = paho.Client()

client.connect("localhost", 1883)

while True:
    
    client.publish("ptz/size", "asdf")
    time.sleep(1)
    client.publish("ptz/delta", "bbbb")
    time.sleep(1)
