##publish.

import paho.mqtt.client as paho
import time

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

client = paho.Client()#client.
client.on_publish = on_publish
client.connect("broker.mqttdashboard.com", 1883)#broker(mqttdashboard.com) connection
client.loop_start()#maybe..connect loop.

while True:
    temperature = read_from_imaginary_thermometer()#temperature recieve
    #publish                    topic.                      payload.          
    (rc, mid) = client.publish("encyclopedia/temperature", str(temperature), qos=1)
    #qos=0 > give message 1 or 0 / qos=1 > give message 1 or 2,3,4... / qos=2 > give message "1"
    time.sleep(30)

##subscribe.
import paho.mqtt.client as paho

#when broker subscribe recieve.
def on_subscribe(client, userdata, mid, granted_qos):#granted_qos > qos's code list
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

#callback from on_message
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("broker.mqttdashboard.com", 1883)
client.subscribe("encycloperdia/#", qos=1)

client.loop_forever()
