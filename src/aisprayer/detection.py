import requests
import logging
from PIL import ImageDraw, Image, ImageChops
import os
import numpy as np
import yaml

from .config_handler import ConfigHandler
from .interface_helper import Interface


class Detector:
    def __init__(self):
        self.c = ConfigHandler()
        self.api_endpoint = self.c.get("API_ENDPOINT")
        self.last_image = None
        self.interface = Interface()

    def detect(self, image, image_stream):
        alarm = False

        motion = self._detect_motion(image)

        if motion:
            detections = self._detect_object(image, image_stream)
            
            if detections:
                alarm = True
        
        image_stream.seek(0)
        self._send_photo(image_stream.read())

        return alarm


    def _send_photo(self, image): #TODO: break out from detection
        
        with open("/home/pi/secrets.yaml") as f:
            secrets = yaml.load(f, Loader=yaml.FullLoader)

        chat_id = secrets["CHAT_ID"]
        token = secrets["TOKEN"]

        params = {'chat_id': chat_id}
        files = {'photo': image}
        
        apiUrl = f"https://api.telegram.org/bot{token}/sendPhoto"
        resp = requests.post(apiUrl, params, files=files)
        return resp


    def _calculate_image_entropy(self, image):
        w, h = image.size
        a = np.array(image.convert("RGB")).reshape((w * h, 3))
        h, _ = np.histogramdd(a, bins=(16,) * 3, range=((0, 256),) * 3)
        prob = h / np.sum(h)
        prob = prob[prob > 0]
        entropy = -np.sum(prob * np.log2(prob))
        return entropy

    def _detect_motion(self, image):
        resize_size = (128, 96)
        small_image = image.resize(resize_size, Image.ANTIALIAS)

        threshold = self.c.get("MOTION_THRES")

        if self.last_image is None:
            self.last_image = small_image

        difference = ImageChops.difference(small_image, self.last_image)
        entropy = self._calculate_image_entropy(difference)

        self.last_image = small_image
        logging.debug(entropy)

        if entropy > threshold:
            return True

        return False

    def _detect_object(self, image, image_stream):
        response = self._post_image(image_stream)

        try:
            detections = [
                prediction
                for prediction in response["predictions"]
                if (
                    prediction["label"] in self.c.get("TARGETS")
                    and prediction["confidence"] > self.c.get("CONFIDENCE_THRES")
                )
            ]
            logging.debug(detections)

        except Exception:
            detections = []

        if detections:
            detect_image = self._draw_detections(image, detections)
            self.interface.send_image(detect_image, "detect_image")

        return detections

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

    def _post_image(self, image_stream):
        response = requests.post(
            self.api_endpoint, files={"image": image_stream}
        ).json()
        logging.debug(response)
        return response
