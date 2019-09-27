import sys
import logging
import requests

import configs
from core import common
from time import sleep

if __name__ == '__main__':
    configs.setting_logger()

    argv = sys.argv[1:]
    collection_path = argv[0]
    collection_header_path = argv[1]
    quality_score_path = argv[2]

    corpus = common.load_collection(collection_header_path, collection_path, configs.ENCODE_DECODE)
    with open(quality_score_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        for ii, cc in enumerate(corpus):
            v_id = cc['video_id']
            img = 'https://img.youtube.com/vi/' + cc['video_id'] + '/maxresdefault.jpg'
            rr = requests.head(img)
            if not rr.status_code == 200:
                logging.info('{}\t{}\t{}'.format(v_id, rr.status_code, img))
                wf.write('{}\t{}'.format(v_id, 0))
            else:
                wf.write('{}\t{}'.format(v_id, 1))

            wf.write('\n')
            sleep(0.1)
            if ii and ii % 100 == 0:
                logging.info('Run: {:,}'.format(ii))
