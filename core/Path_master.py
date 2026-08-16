import os
from pathlib import Path

CURRENT_DIR: str = Path().parent.absolute().as_posix()  # path to current dir where script is stored


def check_for_file(file_name: str):
    return os.path.exists(CURRENT_DIR + os.sep + file_name)


def create_build_files_dir():
    pass


def delete_build_files():
    pass
