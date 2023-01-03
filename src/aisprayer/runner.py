from time import sleep
import time
import requests
import logging
from PIL import ImageDraw

# from .sprayer import Sprayer
from .camera import Camera
from .detection import Detector
from .sprayer import Sprayer
from .config_handler import ConfigHandler
from .interface_helper import Interface
from .telegram import send_photo

class Runner:
    def __init__(self):
        logging.basicConfig(
            filename="/home/pi/logs/aisprayer.log",
            level=logging.INFO,
            format="%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.info("Started")
        self.c = ConfigHandler()
        self.sprayer = Sprayer()
        self.camera = Camera()
        self.detector = Detector()
        self.interface = Interface()
        self.last_image_time = time.time()

    def _interval_keeper(self, run_time):
        logging.debug(f"The code runs in {run_time}s")
        if run_time > self.c.get("PROGRAM_INTERVAL"):
            logging.warning(f"Code runs to slowly {run_time}s")
        else:
            sleep(self.c.get("PROGRAM_INTERVAL") - run_time)

    def run(self):
        while True:
            start_time = time.time()
            self.camera.capture()
            image = self.camera.get_image()
            image_stream = self.camera.get_stream()
            alarm = self.detector.detect(image, image_stream)

            if time.time() - self.last_image_time > self.c.get(
                "CAMERA_UPDATE_INTERVAL"
            ):
                self.last_image_time = time.time()
                self.interface.send_image(image, "image")

            if alarm:
                send_photo(image_stream)
                self.sprayer.spray()
                logging.info("Cat detected")
                for i in range(5):
                    sleep(50)
                    send_photo(image_stream)

            run_time = time.time() - start_time
            self._interval_keeper(run_time)
