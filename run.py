import subprocess
import sys
import os
import logging
from datetime import datetime

import configs


def _run_pipeline(steps):
    pipeline_start_time = datetime.now()
    logging.info("[[Start pipeline at {}]]".format(pipeline_start_time))
    for ii, ss in enumerate(steps):
        step_name = ss[0]
        cmd = ss[1:]
        start_time = datetime.now()
        logging.info('>> ({}) Start {} at {}'.format(ii, step_name, start_time))

        subprocess.call(cmd)

        end_time = datetime.now()
        logging.info('<< Finish: {} at {} (running time: {})'.format(step_name, end_time, (end_time - start_time)))
    pipeline_end_time = datetime.now()
    logging.info(
        "[[Finish pipeline at {} (running time: {})]]".format(pipeline_end_time,
                                                              pipeline_end_time - pipeline_start_time))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.INFO)

    yt_data_path = sys.argv[1]

    steps = list()
    steps.append(
        ['Setting directory', 'python', 'step000_setting_directory.py'])

    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    collection_root_path = os.path.join(configs.BASE_COLLECTION_DIRECTORY_PATH, now)
    steps.append(
        ['Generate Base collection', 'python', 'step100_make_base_collection.py', yt_data_path, collection_root_path])

    steps.append(
        ['Update base collection to bucket', 'python', 'step101_upload_base_collection.py', collection_root_path])

    _run_pipeline(steps)
