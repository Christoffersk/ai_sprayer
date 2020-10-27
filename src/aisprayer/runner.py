from time import sleep
import time
import requests
import logging
from PIL import ImageDraw

# from .sprayer import Sprayer
from .camera import Camera
from .detection import Detector
from .sprayer import Sprayer


class Runner:
    def __init__(self, interval, pin, api_endpoint):
        logging.basicConfig(
            filename="/home/pi/logs/aisprayer.log",
            level=logging.INFO,
            format="%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.info("Started")
        self.interval = interval
        self.sprayer = Sprayer(pin)
        self.camera = Camera()
        self.detector = Detector(api_endpoint=api_endpoint)

    def _interval_keeper(self, run_time):
        logging.debug(f"The code runs in {run_time}s")
        if run_time > self.interval:
            logging.warning(f"Code runs to slowly {run_time}s")
        else:
            sleep(self.interval - run_time)

    def run(self):
        while True:
            start_time = time.time()
            self.camera.capture()
            image = self.camera.get_image()
            image_stream = self.camera.get_stream()
            alarm = self.detector.detect(image, image_stream)

            if alarm:
                self.sprayer.spray()
                logging.info("Cat detected")

            run_time = time.time() - start_time
            self._interval_keeper(run_time)
