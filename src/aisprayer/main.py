from .runner import Runner

from .frontend import run_frontend
import threading


def run():
    # Backend
    runner = Runner()
    threading.Thread(target=runner.run).start()

    # Frontend
    run_frontend()

