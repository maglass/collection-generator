import os
import logging
import sys

import configs
from utils import burkets

if __name__ == '__main__':
    configs.setting_logger()

    directory_name = sys.argv[1]

    if not os.path.isdir(configs.OUTPUT_DIRECTORY_PATH):
        logging.info('Make directory: {}'.format(configs.OUTPUT_DIRECTORY_PATH))
        os.mkdir(configs.OUTPUT_DIRECTORY_PATH)

    output_root_dir = configs.get_local_output_root_directory_path(directory_name)
    logging.info('Make directory: {}'.format(output_root_dir))
    os.mkdir(output_root_dir)

    step01_output_directory_path = configs.get_step01_output_directory_path(directory_name)
    logging.info('Make directory: {}'.format(step01_output_directory_path))
    os.mkdir(step01_output_directory_path)

    step02_output_directory_path = configs.get_step02_output_directory_path(directory_name)
    logging.info('Make directory: {}'.format(step02_output_directory_path))
    os.mkdir(step02_output_directory_path)

    step03_output_directory_path = configs.get_step03_output_directory_path(directory_name)
    logging.info('Make directory: {}'.format(step03_output_directory_path))
    os.mkdir(step03_output_directory_path)

    burkets.mkdir('youtube-collections', directory_name)
    logging.info('Make directory in bucket: {}'.format(directory_name))

    bucket_step01_output_path = configs.get_bucket_step01_output_directory_path(directory_name)
    logging.info('Make directory in bucket: {}'.format(bucket_step01_output_path))
    burkets.mkdir('youtube-collections', bucket_step01_output_path)

    bucket_step02_output_path = configs.get_bucket_step02_output_directory_path(directory_name)
    logging.info('Make directory in bucket: {}'.format(bucket_step02_output_path))
    burkets.mkdir('youtube-collections', bucket_step02_output_path)

    bucket_step03_output_path = configs.get_bucket_step03_output_directory_path(directory_name)
    logging.info('Make directory in bucket: {}'.format(bucket_step03_output_path))
    burkets.mkdir('youtube-collections', bucket_step03_output_path)
