from pathlib import Path
from utils.app_root_dir import app_root_dir
from utils.print_error import print_error


def get_file_path(filename):
    if not Path(filename).is_absolute():
        filename = app_root_dir() / filename

    if not Path(filename).exists():
        print_error("Error: The specified file does not exist.\n")
        return None

    return filename
