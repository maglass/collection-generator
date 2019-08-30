import os
import logging

import configs

if __name__ == '__main__':
    if not os.path.isdir(configs.OUTPUT_DIRECTORY_PATH):
        os.mkdir(configs.OUTPUT_DIRECTORY_PATH)

    if not os.path.isdir(configs.BASE_COLLECTION_DIRECTORY_PATH):
        os.mkdir(configs.BASE_COLLECTION_DIRECTORY_PATH)
