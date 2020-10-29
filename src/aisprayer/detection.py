import requests
import logging
from PIL import ImageDraw, Image, ImageChops
import os
import numpy as np


class Detector:
    def __init__(self, api_endpoint, targets):
        self.api_endpoint = api_endpoint
        self.targets = targets
        self.last_image = None

    def detect(self, image, image_stream):
        alarm = False

        motion = self._detect_motion(image)

        if motion:
            detections = self._detect_object(image, image_stream)

            if detections:
                alarm = True

        return alarm

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

        threshold = 0.2

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
                    prediction["label"] in self.targets
                    and prediction["confidence"] > 0.5
                )
            ]
            logging.debug(detections)

        except Exception:
            detections = []

        if detections:
            self._save_image(image, detections)

        return detections

    def _save_image(self, image, detections):
        image_path = os.path.join(
            os.path.dirname(__file__), "static", "current_rect.jpg"
        )
        image_with_rect = self._draw_detections(image, detections)
        image_with_rect.save(image_path)

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
