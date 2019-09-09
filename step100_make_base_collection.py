import json
import os
import sys
import logging
from datetime import datetime

from core.exceptions import NotValidatedArguments, FailParsingDocument, FailCollectionGenerate
from core.common import clean_text

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
COLLECTION_FIELDS.append('view_cnt')
COLLECTION_FIELDS.append('video_length')
COLLECTION_FIELDS.append('rating')
COLLECTION_FIELDS.append('like_cnt')

CORPUS_FIELDS = list()
CORPUS_FIELDS.append('video_id')
CORPUS_FIELDS.append('channel_name')
CORPUS_FIELDS.append('channel_id')
CORPUS_FIELDS.append('playlist_id')
CORPUS_FIELDS.append('title')
CORPUS_FIELDS.append('description')


def _make_base_collection_and_corpus(youtube_data_path, collection_output_path, corpus_output_path, fields, seq='\t',
                                     null='',
                                     encoding=_ENCODE_DECODE):
    n_total_input = 0
    n_skip_input = 0
    n_video = 0
    start_time = datetime.now()
    collection_wf = open(collection_output_path, 'w', encoding=encoding)
    corpus_wf = open(corpus_output_path, 'w', encoding=encoding)
    youtube_data_reader = open(youtube_data_path, 'r', encoding=_ENCODE_DECODE)
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

                output = list()
                output.append(video_id)
                output.append(channel_name)
                output.append(channel_id)
                output.append(playlist_id)
                output.append(title)
                output.append(description)
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

    information = dict()
    information['n_total_input'] = n_total_input
    information['n_skip_input'] = n_skip_input
    information['n_video'] = n_video
    information['start_time'] = start_time
    information['end_time'] = end_time
    information['running_time'] = running_time
    return information


def _make_header_file(fields, output_path):
    # Make header file
    if not len(fields) == len(set(fields)):
        raise FailCollectionGenerate('Wrong fields (duplicate field): {}'.format(', '.join(fields)))

    with open(output_path, 'w', encoding=_ENCODE_DECODE) as wf:
        wf.write(','.join(fields))

    logging.info('Write header file: {})'.format(output_path))
    logging.info('Fields ({}): {}'.format(len(fields), ', '.join(fields)))


def _parse(youtube):
    yt = youtube
    _doc = dict()
    _doc['type'] = 'video'
    _doc['title'] = yt['title']
    _doc['channel_id'] = yt['channel_id']
    _doc['channel_name'] = yt['channel_name']
    _doc['video_id'] = yt['video_id']
    _doc['playlist_id'] = yt['playlist_id']
    _doc['view_cnt'] = str(yt['views'])
    _doc['rating'] = str(yt['rating'])
    _doc['video_length'] = yt['length']
    _doc['description'] = yt['description']
    return _doc


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    argv = sys.argv[1:]

    youtube_data_path = argv[0]
    collection_path = argv[1]
    collection_header_path = argv[2]
    corpus_path = argv[3]
    corpus_header_path = argv[4]

    _make_header_file(COLLECTION_FIELDS, collection_header_path)
    _make_header_file(CORPUS_FIELDS, corpus_header_path)

    info = _make_base_collection_and_corpus(
        youtube_data_path, collection_path, corpus_path, COLLECTION_FIELDS,
        seq=COLLECTION_VALUE_SEP, null=COLLECTION_NULL_VALUE, encoding=_ENCODE_DECODE)
