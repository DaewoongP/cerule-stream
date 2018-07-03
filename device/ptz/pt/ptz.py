import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
tiltPin = 17
panPin = 27
SG_freq = 50
GPIO.setup(tiltPin, GPIO.OUT)
GPIO.setup(panPin, GPIO.OUT)
tilt = GPIO.PWM(tiltPin, SG_freq)
pan = GPIO.PWM(panPin, SG_freq)

tilt.start(7.5)
pan.start(7.5)

class move:
        
    def right(self, pan_angle):
        pan_angle = pan_angle + 10
        print(1/20*pan_angle +3)        
        if (pan_angle > 180):
            pan.ChangeDutyCycle(7.5)
        else:
            pan.ChangeDutyCycle(1/20*pan_angle +3)
        
    def left(self, pan_angle):
        pan_angle = pan_angle - 10        
        if (pan_angle < 0):
            pan.ChangeDutyCycle(7.5)
        else:
            pan.ChangeDutyCycle(1/20*pan_angle +3)

            
    def up(self, tilt_angle):
        tilt_angle = tilt_angle + 10
        if (tilt_angle > 180):
            tilt.ChangeDutyCycle(7.5)
        else:
            tilt.ChangeDutyCycle(1/20*tilt_angle +3)

    def down(self, tilt_angle):
        tilt_angle = tilt_angle - 10
        if (tilt_angle < 0):
            tilt.ChangeDutyCycle(7.5)
        else:
            tilt.ChangeDutyCycle(1/20*tilt_angle +3)
    
