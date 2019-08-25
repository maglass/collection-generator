import subprocess
import sys
import os
from datetime import datetime
import configs


def _setting_directories():
    if not os.path.isdir(configs.OUTPUT_DIRECTORY_PATH):
        os.mkdir(configs.OUTPUT_DIRECTORY_PATH)

    if not os.path.isdir(configs.BASE_COLLECTION_DIRECTORY_PATH):
        os.mkdir(configs.BASE_COLLECTION_DIRECTORY_PATH)


if __name__ == '__main__':
    yt_data_path = sys.argv[1]

    _setting_directories()
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    # Make output directory
    collection_root_path = os.path.join(configs.BASE_COLLECTION_DIRECTORY_PATH, now)
    subprocess.call(['python', 'step00_make_base_collection.py', yt_data_path, collection_root_path])
