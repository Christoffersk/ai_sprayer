from .runner import Runner

from .frontend import run_frontend
import threading

PUMPPIN = 4
INTERVAL = 2
API_ENDPOINT = "http://192.168.1.2:8109/v1/vision/detection"


def run():
    # Backend
    runner = Runner(interval=INTERVAL, pin=PUMPPIN, api_endpoint=API_ENDPOINT)
    threading.Thread(target=runner.run).start()

    # Frontend
    run_frontend()

