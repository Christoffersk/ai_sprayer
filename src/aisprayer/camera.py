from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image


class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        sleep(2)

    def capture(self):
        # Create the in-memory stream
        self.stream = BytesIO()
        self.camera.capture(self.stream, format="jpeg")
        # "Rewind" the stream to the beginning so we can read its content
        self.stream.seek(0)
        image = Image.open(self.stream)

        return image
