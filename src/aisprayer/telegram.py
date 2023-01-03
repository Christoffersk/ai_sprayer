import yaml
import requests

    
def send_photo(image_stream): #TODO: break out from detection
    
    with open("/home/pi/secrets.yaml") as f:
        secrets = yaml.load(f, Loader=yaml.FullLoader)

    chat_id = secrets["CHAT_ID"]
    token = secrets["TOKEN"]

    image_stream.seek(0)
    image = image_stream.read()
    
    params = {'chat_id': chat_id}
    files = {'photo': image}
    
    apiUrl = f"https://api.telegram.org/bot{token}/sendPhoto"
    resp = requests.post(apiUrl, params, files=files)
    return resp
