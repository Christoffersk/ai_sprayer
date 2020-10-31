import requests
import sys
import io


class Interface:
    def __init__(self):
        pass

    def send_image(self, image, tag):
        url = "http://localhost:5000/update_image"
        buffer = io.BytesIO()
        image.save(buffer, "JPEG")
        buffer.seek(0)
        payload = {tag: ("image.jpg", buffer, "image/jpeg")}
        response = requests.post(url, files=payload)
        return response
