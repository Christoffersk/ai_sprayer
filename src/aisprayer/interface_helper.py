import requests
import io

url = "https://www.w3schools.com/python/demopage.php"
myobj = {"somekey": "somevalue"}

x = requests.post(url, data=myobj)


class Interface:
    def __init__():
        pass

    def send_image(self, image):
        url = "http://localhost:5000/update_photo"
        data = io.BytesIO()
        image.save(data, "JPEG")
        files = {"image": image}
        requests.post(url, files=files)
