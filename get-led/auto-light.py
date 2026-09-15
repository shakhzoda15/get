import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
photo = 6
GPIO.setup(photo, GPIO.IN)
state = GPIO.input(photo)
while True:
    state = not state
    GPIO.output(led, state)
    time.sleep(0.2)