from time import sleep
import time
import requests
import logging
from PIL import ImageDraw

# from .sprayer import Sprayer
from .camera import Camera


class Runner:
    def __init__(self, interval, pin):
        logging.basicConfig(filename="/home/pi/aisprayer.log", level=logging.DEBUG)
        logging.info("Started")
        self.interval = interval
        # self.sprayer = Sprayer(pin)
        self.camera = Camera()

    def _detect_object(self):
        image = self.camera.capture()

        response = self._post_image(self.camera.stream)
        print(response)
        logging.debug(response)
        if response:
            detections = [
                prediction
                for prediction in response["predictions"]
                if (prediction["label"] == "cat" and prediction["confidence"] > 0.5)
            ]
            logging.debug(detections)

            if detections:
                self._save_image(image, detections)
        else:
            detections = []

        return detections

    def _save_image(self, image, detections):
        image_with_rect = self._draw_detections(image, detections)
        image_with_rect.save("current.jpeg")

    def _draw_detections(self, image, detections):
        for prediction in detections:
            shape = [
                (prediction["x_min"], prediction["y_min"]),
                (prediction["x_max"], prediction["y_max"]),
            ]

            # create rectangle image
            img_drawer = ImageDraw.Draw(image)
            img_drawer.rectangle(shape, outline="red", width=3)
            img_drawer.text(
                (prediction["x_min"], prediction["y_min"]),
                str(prediction["confidence"]),
            )
            img_drawer.text(
                (prediction["x_min"], prediction["y_min"] + 30),
                str(prediction["label"]),
            )

        return image

    def _post_image(self, image):
        response = requests.post(
            "http://192.168.1.2:8109/v1/vision/detection", files={"image": image}
        ).json()
        logging.debug(response)
        return response

    def _interval_keeper(self, run_time):
        logging.debug(f"The code runs in {run_time}s")
        if run_time > self.interval:
            print("Error - Code runs to slowly")
        else:
            sleep(self.interval - run_time)

    def run(self):
        while True:
            start_time = time.time()

            alarm = self._detect_object()
            if alarm:
                # self.sprayer.spray()
                logging.info("Cat detected")

            run_time = time.time() - start_time
            self._interval_keeper(run_time)
