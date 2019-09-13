import os
import sys

import configs
from utils import burkets

if __name__ == '__main__':
    configs.setting_logger()
    argv = sys.argv[1:]

    from_path = argv[0]
    bucket_path = argv[1]

    for filename in os.listdir(from_path):
        file_path = os.path.join(from_path, filename)
        bucket_file_path = '{}/{}'.format(bucket_path, filename)
        burkets.upload_file('youtube-collections', bucket_file_path, file_path)
