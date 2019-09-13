import json
import logging
import sys
from datetime import datetime

import configs
from core.textutils import clean_text
from core.exceptions import FailParsingDocument, FailCollectionGenerate

_ENCODE_DECODE = 'utf8'

COLLECTION_VALUE_SEP = '\t'
COLLECTION_NULL_VALUE = ''

COLLECTION_FIELDS = list()
COLLECTION_FIELDS.append('type')
COLLECTION_FIELDS.append('channel_id')
COLLECTION_FIELDS.append('channel_name')
COLLECTION_FIELDS.append('video_id')
COLLECTION_FIELDS.append('playlist_id')
COLLECTION_FIELDS.append('title')
COLLECTION_FIELDS.append('views')
COLLECTION_FIELDS.append('length')
COLLECTION_FIELDS.append('rating')

CORPUS_FIELDS = list()
CORPUS_FIELDS.append('video_id')
CORPUS_FIELDS.append('channel_name')
CORPUS_FIELDS.append('channel_id')
CORPUS_FIELDS.append('playlist_id')
CORPUS_FIELDS.append('title')
CORPUS_FIELDS.append('description')
CORPUS_FIELDS.append('caption_type')
CORPUS_FIELDS.append('caption')

CAPTION_TYPES = dict()
CAPTION_TYPES['korea'] = '<Caption lang="한국어" code="ko">'
CAPTION_TYPES['auto-korean'] = '<Caption lang="한국어 (자동 생성됨)" code="ko">'


def _make_base_collection_and_corpus(youtube_path, collection_output_path, corpus_output_path, fields, seq='\t',
                                     null='', encoding=_ENCODE_DECODE):
    n_total_input = 0
    n_skip_input = 0
    n_video = 0
    start_time = datetime.now()
    collection_wf = open(collection_output_path, 'w', encoding=encoding)
    corpus_wf = open(corpus_output_path, 'w', encoding=encoding)
    youtube_data_reader = open(youtube_path, 'r', encoding=_ENCODE_DECODE)
    for n, line in enumerate(youtube_data_reader):
        try:
            n_total_input += 1
            data = json.loads(line)
            d_type = data['type']
            if d_type == 'youtube':
                n_video += 1
                doc = _parse(data)
                collection_wf.write(seq.join(str(doc.get(ff, null)) for ff in fields))
                collection_wf.write('\n')

                video_id = doc['video_id']
                channel_name = doc['channel_name']
                channel_id = doc['channel_id']
                playlist_id = doc['playlist_id']
                title = clean_text(doc['title']).replace('\n', ' ').replace('\t', ' ')
                description = clean_text(doc['description']).replace('\n', ' ').replace('\t', ' ')
                caption_type = doc['caption_type']
                caption = clean_text(' '.join(doc['caption']))

                output = list()
                output.append(video_id)
                output.append(channel_name)
                output.append(channel_id)
                output.append(playlist_id)
                output.append(title)
                output.append(description)
                output.append(caption_type)
                output.append(caption)
                corpus_wf.write('\t'.join(output))
                corpus_wf.write('\n')

            if 0 < n and (n % 100 == 0):
                logging.info('Running: {}'.format(n))
        except Exception as e:
            n_skip_input += 1
            logging.error("line: {}".format(n))
            logging.error(FailParsingDocument(e))

    youtube_data_reader.close()
    collection_wf.close()
    corpus_wf.close()
    end_time = datetime.now()
    running_time = end_time - start_time
    logging.info("End make base collection: {} running: {}".format(end_time, running_time))


def _parse(youtube):
    yt = youtube
    _doc = dict()
    _doc['type'] = 'video'
    _doc['title'] = yt['title']
    _doc['channel_id'] = yt['channel_id']
    _doc['channel_name'] = yt['channel_name']
    _doc['video_id'] = yt['video_id']
    _doc['playlist_id'] = yt['playlist_id']
    _doc['views'] = str(yt['views'])
    _doc['rating'] = str(yt['rating'])
    _doc['length'] = yt['length']
    _doc['description'] = yt['description']

    caption_type, caption = _get_captions(yt['captions'])
    _doc['caption_type'] = caption_type
    _doc['caption'] = caption

    return _doc


def _get_captions(captions):
    caption_names = [cc[0] for cc in captions]

    if CAPTION_TYPES['auto-korean'] in caption_names:
        caption_type = 'auto-korean'
        caption_idx = caption_names.index('<Caption lang="한국어 (자동 생성됨)" code="ko">')
        selected = captions[caption_idx][1]
    else:
        caption_type = 'not-exists'
        selected = ''

    preprocessed = _handling(selected)
    return caption_type, preprocessed


def _handling(caption):
    caption = caption.replace('\t', ' ')
    caption = caption.split('\n')
    text = caption[2::4]
    return text


def _make_header_file(fields, output_path):
    # Make header file
    if not len(fields) == len(set(fields)):
        raise FailCollectionGenerate('Wrong fields (duplicate field): {}'.format(', '.join(fields)))

    with open(output_path, 'w', encoding=_ENCODE_DECODE) as wf:
        wf.write(','.join(fields))

    logging.info('Write header file: {})'.format(output_path))
    logging.info('Fields ({}): {}'.format(len(fields), ', '.join(fields)))


if __name__ == '__main__':
    configs.setting_logger()

    argv = sys.argv[1:]

    youtube_data_path = argv[0]
    collection_path = argv[1]
    collection_header_path = argv[2]
    corpus_path = argv[3]
    corpus_header_path = argv[4]

    _make_header_file(COLLECTION_FIELDS, collection_header_path)
    _make_header_file(CORPUS_FIELDS, corpus_header_path)
    _make_base_collection_and_corpus(youtube_data_path, collection_path, corpus_path, COLLECTION_FIELDS,
                                     seq=COLLECTION_VALUE_SEP, null=COLLECTION_NULL_VALUE, encoding=_ENCODE_DECODE)
