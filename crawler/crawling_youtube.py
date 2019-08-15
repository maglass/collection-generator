import sys
import json
import logging
import os
from crawler import youtube
from time import sleep
from datetime import datetime

_NOW = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
_CONFIG_OUTPUT_DIRECTORY_PATH = 'data/youtube'


def _load_urls_from_file(path):
    urls = list()
    rf = open(path, 'r', encoding='utf8')
    for line in rf:
        line = line.strip()
        if not line or line.startswith('#'):
            # 빈 줄과 주석 제거
            continue
        values = line.split('\t')
        uu = values[1].strip()
        urls.append(uu)
    rf.close()
    return urls


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    playlist_file_path = sys.argv[1]

    if not os.path.isdir(_CONFIG_OUTPUT_DIRECTORY_PATH):
        os.mkdir(_CONFIG_OUTPUT_DIRECTORY_PATH)

    output_path = os.path.join(_CONFIG_OUTPUT_DIRECTORY_PATH, 'yt-pli-{}'.format(_NOW))
    playlist_urls = _load_urls_from_file(playlist_file_path)
    logging.info('Start crawler play list: {}'.format(output_path))
    logging.info('\n'.join(playlist_urls))

    count = 0
    wf = open(output_path, 'w', encoding='utf8')
    for pli_url in playlist_urls:
        try:
            count += 1
            logging.info('Start playlist: {}'.format(pli_url))
            playlist = youtube.from_playlist_url(pli_url)

            wf.write(json.dumps(playlist, ensure_ascii=False))
            wf.write('\n')

            youtube_ids = playlist.get('video_urls')
            logging.info('Finish: ({}) {}'.format(len(youtube_ids), playlist['title']))

            base_url = 'https://www.youtube.com'
            for ii, vi_url in enumerate(youtube_ids, 1):
                logging.info('Start youtube ({}): {}'.format(ii, vi_url))
                yt = youtube.from_youtube_url('{}/{}'.format(base_url, vi_url))
                wf.write(json.dumps(yt, ensure_ascii=False))
                wf.write('\n')

                logging.info('finish ({}): {}'.format(ii, yt['title']))
                sleep(4)
        except Exception as e:
            logging.error('{} {} {}'.format(count, pli_url, e))

    wf.close()
