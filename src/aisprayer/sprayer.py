import RPi.GPIO as GPIO
import time


class Sprayer:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)  # , pull_up_down=GPIO.PUD_UP)

    def spray(self):
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.pin, GPIO.LOW)
