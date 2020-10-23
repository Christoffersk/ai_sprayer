from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image


class Camera:
    def __init__(self):
        pass

    def get_image(self):
        return self.image

    def get_stream(self):
        stream = BytesIO()
        self.image.save(stream, "jpeg")
        stream.seek(0)
        return stream

    def capture(self):
        image_stream = BytesIO()
        with PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.capture(image_stream, format="jpeg")
        self.image = Image.open(image_stream)

