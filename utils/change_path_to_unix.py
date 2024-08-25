from pathlib import Path


def change_path_to_unix(path):
    return Path(path).as_posix()
