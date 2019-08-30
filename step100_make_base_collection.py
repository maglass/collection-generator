import json
import os
import sys
import logging
from datetime import datetime
from utils import burkets

import configs
from core.exceptions import NotValidatedArguments, FailParsingDocument, FailCollectionGenerate
from core.common import clean_text


def _make_header_file(fields, output_path):
    # Make header file
    if not len(fields) == len(set(fields)):
        raise FailCollectionGenerate('Wrong fields (duplicate field): {}'.format(', '.join(fields)))

    with open(output_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        wf.write(','.join(fields))

    logging.info('Write header file: {})'.format(output_path))
    logging.info('Fields ({}): {}'.format(len(fields), ', '.join(fields)))


def _make_base_collection_and_corpus(reader, collection_output_path, corpus_output_path, fields, seq='\t', null='',
                                     encoding='utf8'):
    n_total_input = 0
    n_skip_input = 0
    n_video = 0
    start_time = datetime.now()
    collection_wf = open(collection_output_path, 'w', encoding=encoding)
    corpus_wf = open(corpus_output_path, 'w', encoding=encoding)
    for n, line in enumerate(reader):
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
                title = clean_text(doc['title']).replace('\n', ' ').replace('\t', ' ')
                description = clean_text(doc['description']).replace('\n', ' ').replace('\t', ' ')
                output = list()
                output.append(video_id)
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


def _check_and_save_summary(summary, save_path):
    with open(save_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        header = summary.keys()
        values = [summary[ff] for ff in header]
        wf.write('\t'.join(header))
        wf.write('\n')

        wf.write('\t'.join(map(str, values)))
        wf.write('\n')

    n_total_input = summary['n_total_input']
    n_skip_input = summary['n_skip_input']
    n_video = summary['n_video']
    running_time = summary['running_time']

    # Check base collection
    logging.info('Total youtube data rows: {}'.format(n_total_input))
    logging.info('Skip youtube data rows: {}'.format(n_skip_input))
    logging.info('Number of video: {}'.format(n_video, n_video / n_total_input))
    logging.info('Running time: {}'.format(running_time))
    if n_skip_input > (n_total_input * 0.20):
        raise FailCollectionGenerate(
            'Fail because too much skip documents: {} / {}'.format(n_skip_input, n_total_input))


def _get_reader(path):
    return open(path, 'r', encoding=configs.ENCODE_DECODE)


def _parse(youtube):
    yt = youtube
    _doc = dict()
    _doc['type'] = 'video'
    _doc['title'] = yt['title']
    _doc['video_id'] = yt['video_id']
    _doc['view_cnt'] = str(yt['views'])
    _doc['rating'] = str(yt['rating'])
    _doc['video_length'] = yt['length']
    _doc['description'] = yt['description']
    return _doc


def _check_validated_arguments(arguments):
    if not len(arguments) == 2:
        raise NotValidatedArguments(arguments, "Invalidated argument number")

    if not os.path.isfile(arguments[0]):
        raise NotValidatedArguments(arguments, "Not exists youtube data file")

    if os.path.isdir(arguments[1]):
        raise NotValidatedArguments(arguments, "Already exists base-collection directory")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    argv = sys.argv[1:]

    _check_validated_arguments(argv)
    youtube_data_path = argv[0]
    output_dir_path = argv[1]

    os.mkdir(output_dir_path)

    # Make header file
    header_path = os.path.join(output_dir_path, configs.CORPUS_HEADER_NAME)
    _make_header_file(configs.DOC_FIELDS, header_path)

    corpus_header_path = os.path.join(output_dir_path, configs.CORPUS_HEADER_NAME)
    _make_header_file(['video_id', 'title', 'description'], corpus_header_path)
    # Make collection file
    base_collection_path = os.path.join(output_dir_path, configs.BASE_COLLECTION_FILE_NAME)

    corpus_path = os.path.join(output_dir_path, configs.CORPUS_FILE_NAME)
    youtube_data_reader = _get_reader(youtube_data_path)
    info = _make_base_collection_and_corpus(youtube_data_reader, base_collection_path, corpus_path, configs.DOC_FIELDS,
                                            seq=configs.COLLECTION_VALUE_SEP, null=configs.COLLECTION_NULL_VALUE,
                                            encoding=configs.ENCODE_DECODE)
    youtube_data_reader.close()

    # Check collection
    summary_path = os.path.join(output_dir_path, configs.BASE_COLLECTION_SUMMARY_FILE_NAME)
    _check_and_save_summary(info, summary_path)