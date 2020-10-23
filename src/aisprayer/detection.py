import requests
import logging
from PIL import ImageDraw
import os


class Detector:
    def __init__(self):
        pass

    def _detect_object(self, image, image_stream):

        response = self._post_image(image_stream)

        try:
            detections = [
                prediction
                for prediction in response["predictions"]
                if (prediction["label"] == "cat" and prediction["confidence"] > 0.5)
            ]
            logging.info(detections)

        except KeyError:
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
            "http://192.168.1.2:8109/v1/vision/detection", files={"image": image_stream}
        ).json()
        logging.debug(response)
        return response
