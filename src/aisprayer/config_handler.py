import yaml
import os
import time
import logging
import json


class ConfigHandler:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        self._load_config()
        self.interval = self.config["PROGRAM_INTERVAL"]

    def _load_config(self):
        with open(self.config_path) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def update_config(self, config_change):
        self.config.update(config_change)
        with open(self.config_path, "w") as f:
            yaml.dump(self.config, f)

    def get(self, variable):
        mod_time = os.path.getmtime(self.config_path)
        current_time = time.time()
        if current_time - mod_time < (self.interval + 1):
            self._load_config()

        return self.config[variable]

