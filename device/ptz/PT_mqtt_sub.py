import paho.mqtt.client as paho
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
tiltPin = 17
panPin = 27

GPIO.setup(tiltPin, GPIO.OUT)
GPIO.setup(panPin, GPIO.OUT)
GPIO.setwarnings(False)

tilt = GPIO.PWM(tiltPin, 50)
pan = GPIO.PWM(panPin, 50)

tilt.start(0)
pan.start(0)

tilt.ChangeDutyCycle(8)
pan.ChangeDutyCycle(8)#center point lock

time.sleep(3)

#------------------------------------------------------

class box:
    def __init__(self, Tx, Ty, Tw, Th, Cx, Cy, label):
        self.Tx = Tx#x - corner
        self.Ty = Ty#y - corner
        self.Tw = Tw#width - box
        self.Th = Th#width - box
        self.Cx = Cx#x - box center
        self.Cy = Cy#y - box center
        self.label = label#Label

#------------------------------------------------------

class PTmodule(box):
    def __init__(self, Tx, Ty, Tw, Th, Cx, Cy, label, lx, ly):
        box.__init__(self, Tx, Ty, Tw, Th, Cx, Cy, label)
        self.lx = lx#camera's x
        self.ly = ly#camera's y (now) this (x,y) is shold be (0,0)
        
    def size(self):#bounding box's size return
        size = self.Tw * self.Th
        print(size)
        return size

    def delta(self):#camera
        dx = self.Cx - self.lx
        dy = self.Cy - self.ly

        #center vs camera point
        if (self.Cx != self.lx):
            pan.ChangeDutyCycle((dx-240)/48+13)
            
        if (self.Cy != self.ly):
            tilt.ChangeDutyCycle((dy-320)/64+13)
        #-----------------------------    
            
        loc = (dx, dy) #delta tuple
        center = (self.Cx, self.Cy) #center tuple
        
        print (dx, dy)
        print (loc)#(dx,dy) tuple

#   setup      Tx   Ty    Tw   Th   Cx  Cy  label lx ly
PT = PTmodule(-150, 250, 100, 100, 100, 200, 1, 0, 0)

#------------------------------------------------------
x = 8
y = 8
def on_size(object, userdata, msg):
    PT.size()

def on_delta(object, userdata, msg):
    PT.delta()

def on_moveX(object, userdata, msg):
    if (move_x >= 0) #App's key >
        pan.ChangeDutyCycle(x = x+1)
    if (move_x <= 0) #App's key <
        pan.ChangeDutyCycle(x = x-1)
    
def on_moveY(object, userdata, msg):
    if (move_y >= 0) #App's key ^
        tilt.ChangeDutyCycle(y = y+1)
    if (move_y <= 0) #App's key v
        tilt.ChangeDutyCycle(y = y-1)
    
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    #size = int(str(msg.payload)[2:3])

    
client = paho.Client()#...

client.message_callback_add("ptz/size", on_size)#callback to function
client.message_callback_add("ptz/delta", on_delta)
client.message_callback_add("ptz/message", on_message)

client.connect("localhost", 1883)#broker set
client.subscribe("ptz/#")#sub 'ptz'

client.loop_forever()

