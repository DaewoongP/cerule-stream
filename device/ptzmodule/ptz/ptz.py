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
        
    def x(self, dx):
        duty = (dx - 320) / 64 + 12
        if (duty>= 11):
            pan.ChangeDutyCycle(7)
        elif (duty <= 3):
            pan.ChangeDutyCycle(7)
        else:
            pan.ChangeDutyCycle(duty)

    def y(self, dy):
        duty = (dy - 240) / 48 + 12
        if (duty>= 11):
            tilt.ChangeDutyCycle(7)
        elif (duty <= 3):
            tilt.ChangeDutyCycle(7)
        else:
            tilt.ChangeDutyCycle(duty)
