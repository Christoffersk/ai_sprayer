from .runner import Runner

from .frontend import run_frontend
import threading

PUMPPIN = 4
INTERVAL = 2


def run():
    # Backend
    runner = Runner(interval=INTERVAL, pin=PUMPPIN)
    threading.Thread(target=runner.run).start()

    # Frontend
    run_frontend()

