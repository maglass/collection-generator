import logging
import sys
from datetime import datetime

import configs
from core import pipeline

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.INFO)

    argv = sys.argv[1:]
    now = argv[0]
    yt_data_path = argv[1]

    steps = list()

    step01_collection_path = configs.get_step01_collection_path(now)
    step01_collection_header_path = configs.get_step01_collection_header_path(now)
    step01_corpus_path = configs.get_step01_corpus_path(now)
    step01_corpus_header_path = configs.get_step01_corpus_header_path(now)
    steps.append(
        ['Generate Base collection', 'python', 'step100_make_base_collection.py',
         yt_data_path,
         step01_collection_path, step01_collection_header_path,
         step01_corpus_path, step01_corpus_header_path])

    step01_output_path = configs.get_step01_output_directory_path(now)
    step01_bucket_output_path = configs.get_bucket_step01_output_directory_path(now)
    steps.append(
        ['Update base collection to bucket', 'python', 'step101_upload_base_collection.py',
         step01_output_path, step01_bucket_output_path])

    pipeline.run(steps)
