import os
from flask import Flask
from utils.app_root_dir import app_root_dir


class FlaskService(Flask):
    def __init__(self, *args, **kwargs):
        root_path = kwargs.pop("root_path", app_root_dir())
        super().__init__(*args, root_path=root_path, **kwargs)
        self.root_path = root_path
