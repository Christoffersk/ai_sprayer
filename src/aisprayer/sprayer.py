import RPi.GPIO as GPIO
import time

from .config_handler import ConfigHandler



class Sprayer:
    def __init__(self):
        self.c = ConfigHandler()
        self.pin = self.c.get("PUMPPIN")
        self.last_spray = time.time()
        self.spray_counter = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def spray(self):
        if time.time() - self.last_spray > self.c.get("SPRAY_SPACING"):
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(self.c.get("SPRAY_TIME"))
            GPIO.output(self.pin, GPIO.LOW)
            self.last_spray = time.time()
            self.spray_counter += 1

    def reset_spray_counter(self):
        self.spray_counter = 0
