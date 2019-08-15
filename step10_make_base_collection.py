import json
import os
from core import docparser
from datetime import datetime

_DOC_FIELDS = list()
_DOC_FIELDS.append('type')
_DOC_FIELDS.append('video_id')
_DOC_FIELDS.append('playlist_id')
_DOC_FIELDS.append('title')
_DOC_FIELDS.append('view_cnt')
_DOC_FIELDS.append('video_length')
_DOC_FIELDS.append('rating')
_DOC_FIELDS.append('video_ids')
_DOC_FIELDS.append('video_cnt')

if __name__ == '__main__':
    youtube_data_path = 'data/youtube/sample-youtube-data-2019-08-08'

    now = datetime.now().strftime('%Y-%m-%d')
    collection_root_path = 'data/base_collections/{}'.format(now)
    if not os.path.isdir(collection_root_path):
        os.mkdir(collection_root_path)

    header_path = os.path.join(collection_root_path, 'header.csv')
    with open(header_path, 'w', encoding='utf8') as wf:
        wf.write(','.join(_DOC_FIELDS))

    collection_path = os.path.join(collection_root_path, 'base_collection')
    with open(youtube_data_path, 'r', encoding='utf8') as rf, open(collection_path, 'w', encoding='utf8') as wf:
        try:
            for line in rf:
                data = json.loads(line)
                _type = data['type']
                if _type == 'youtube':
                    doc = docparser.to_video(data)
                elif _type == 'playlist':
                    doc = docparser.to_playlist(data)

                wf.write('\t'.join(str(doc.get(fi, '')) for fi in _DOC_FIELDS))
                wf.write('\n')
        except Exception as e:
            print(e)
