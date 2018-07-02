import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
tiltPin = 17
panPin = 27 #pantilt pin >BCM 17, 27 output set

GPIO.setup(tiltPin, GPIO.OUT)
GPIO.setup(panPin, GPIO.OUT)
GPIO.setwarnings(False)

tilt = GPIO.PWM(tiltPin, 50)
pan = GPIO.PWM(panPin, 50)

tilt.start(0)
pan.start(0)

tilt.ChangeDutyCycle(8)#center point lock
pan.ChangeDutyCycle(8)#center point lock
time.sleep(3)

#------------------------------------------------------

#parent class return to PTmodule ( Tx, Ty, Tw, Th, Cx, Cy and label.)
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

#bounding box class's (Tx ~ label) to my class.
        
class PTmodule(box):
    def __init__(self, Tx, Ty, Tw, Th, Cx, Cy, label, lx, ly):
        box.__init__(self, Tx, Ty, Tw, Th, Cx, Cy, label)
        self.lx = lx#camera's x
        self.ly = ly#camera's y (now) this (x,y) is shold be (0,0)

    #Bounding Box's size    
    def size(self):
        size = self.Tw * self.Th
        print(size)
        return size
    
    #camera's move X & move Y
    def delta(self):#camera
        dx = self.Cx - self.lx
        dy = self.Cy - self.ly

        #center vs camera point
        if (self.Cx != self.lx):
            pan.ChangeDutyCycle((dy-240)/48+13)
            
        if (self.Cy != self.ly):
            tilt.ChangeDutyCycle((dx-320)/64+13)
        #-----------------------------    
            
        loc = (dx, dy) #delta tuple
        center = (self.Cx, self.Cy) #center tuple
        
        print (dx, dy)
        print (loc)#(dx,dy) tuple

        
#test         Tx     Ty   Tw  Th   Cx   Cy label, lx, ly
PT = PTmodule(200, 250, 100, 100, 100, 200, 1, 0, 0)
PT.size()
PT.delta()
