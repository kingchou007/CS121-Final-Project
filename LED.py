import RPi.GPIO as GPIO
import time

PIN_R = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_R, GPIO.OUT)

GPIO.output(PIN_R, GPIO.HIGH)
time.sleep(10)

GPIO.output(PIN_R, GPIO.LOW)


