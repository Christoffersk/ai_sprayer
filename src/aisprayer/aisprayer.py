import threading

# from flask import Flask

from .runner import Runner

# app = Flask(__name__)

SERVOPIN = 4
INTERVAL = 1

runner = Runner(interval=INTERVAL, pin=SERVOPIN)

runner_thread = threading.Thread(target=runner.run, args=(), kwargs={})
runner_thread.start()

