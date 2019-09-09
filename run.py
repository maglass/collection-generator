import logging
import sys
from datetime import datetime

from core import pipeline

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.INFO)

    yt_data_path = sys.argv[1]

    steps = list()
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    steps.append(['Setting directory', 'python', 'step000_setting_directory.py', now])
    steps.append(['Step01', 'python', 'step100.py', now, yt_data_path])
    steps.append(['Step02', 'python', 'step200.py', now])

    pipeline.run(steps)
