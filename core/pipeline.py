import logging
import subprocess
from datetime import datetime


def run(steps):
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
