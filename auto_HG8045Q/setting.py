import json
import os
from typing import Any, Dict

from .singleton import Singleton


class Setting(metaclass=Singleton):
    def __init__(self, filepath: str = None):
        self.path = filepath
        if not os.path.exists(self.path):
            self._generate()

        self.config = self.load()

    def _generate(self) -> None:
        config_format = {
            "username": "",
            "password": "",
            "host": "",
            "language": "english"
        }
        with open(self.path, 'w') as f:
            json.dump(config_format, f, indent=2)

    def load(self) -> Dict[str, Any]:
        with open(self.path, 'r') as f:
            return json.load(f)

    def get(self, key: str) -> str:
        return self.config[key]

    def save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.config, f, indent=2)
