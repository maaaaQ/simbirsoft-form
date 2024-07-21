import os
from pathlib import Path


def remove_test_dir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    if os.path.isdir(dir_path):
        for f in os.listdir(dir_path):
            if not f.endswith(".mp4") and not f.endswith(".png") and not f.endswith(".txt"):
                continue
            else:
                try:
                    os.remove(os.path.join(dir_path, f))
                except FileNotFoundError:
                    pass
