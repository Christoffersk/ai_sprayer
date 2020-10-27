from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
import os


class Camera:
    def __init__(self):
        self.camera = PiCamera()

    def save_image(self, filename):
        image_path = os.path.join(os.path.dirname(__file__), "static", filename)
        self.image.save(image_path)

    def get_image(self):
        return self.image

    def get_stream(self):
        stream = BytesIO()
        self.image.save(stream, "jpeg")
        stream.seek(0)
        return stream

    def capture(self):
        image_stream = BytesIO()
        self.camera.capture(image_stream, format="jpeg")

        self.image = Image.open(image_stream)

