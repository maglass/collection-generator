import sys
import logging
from datetime import datetime

from core import pipeline

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(logging.INFO)

    youtube_data_path = sys.argv[1]
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    steps = list()
    steps.append(['Setting directory', 'python', 'step000_setting_directory.py', now])
    steps.append(['Step01', 'python', 'step100.py', now, youtube_data_path])
    steps.append(['Step02', 'python', 'step200.py', now])
    steps.append(['Step03', 'python', 'step300.py', now])
    pipeline.run(steps)
