import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
tiltPin = 17
panPin = 27
SG_freq = 50
GPIO.setup(tiltPin, GPIO.OUT)
GPIO.setup(panPin, GPIO.OUT)
tilt = GPIO.PWM(tiltPin, SG_freq)
pan = GPIO.PWM(panPin, SG_freq)

tilt_angle = 90
pan_angle = 90

tilt.start(7.5)
pan.start(7.5)

while True:
    time.sleep(1)
    for pan_angle in range(0,181,10):
        pan.ChangeDutyCycle(1/20*pan_angle +3)
        print("duty ="+str(1/20*pan_angle+3))
        print("angle = "+str(pan_angle)+"\n")
        time.sleep(1)
    pan.ChangeDutyCycle(7.5)
   
