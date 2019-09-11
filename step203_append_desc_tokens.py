import logging
import os
import sys

import configs
from core import common


def _load_corpus(h_path, c_path):
    # Load fields from header file
    fields = common.load_fields(h_path)

    # Load corpus
    n_fields = len(fields)
    n_skip = 0
    _corpus = list()
    with open(c_path, 'r', encoding=configs.ENCODE_DECODE) as rf:
        for n_line, line in enumerate(rf):
            values = line.rstrip('\n').split('\t')
            if not n_fields == len(values):
                logging.warning('Skip line "not equal field ({}), values ({})'.format(n_fields, len(values)))
                logging.warning(values)
                n_skip += 1
                continue
            cor = {ff: vv for ff, vv in zip(fields, values)}
            _corpus.append(cor)
    logging.info('load corpus: {:,} skip: {:,}'.format(len(_corpus), n_skip))
    return _corpus


def _load_expanded_indices(path):
    _output = dict()
    with open(path, 'r', encoding=configs.ENCODE_DECODE) as rf:
        for line in rf:
            values = line.rstrip('\n').split('\t')
            doc_id = values[0]
            _indices = values[1:]
            _output[doc_id] = _indices
    return _output


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    argv = sys.argv[1:]
    collection_path = argv[0]
    collection_header_path = argv[1]
    title_indices_path = argv[2]
    desc_indices_path = argv[3]
    appended_collection_path = argv[4]
    appended_collection_header_path = argv[5]

    fields = common.load_fields(collection_header_path)
    collection = _load_corpus(collection_header_path, collection_path)
    title_indices = _load_expanded_indices(title_indices_path)
    desc_indices = _load_expanded_indices(desc_indices_path)
    with open(appended_collection_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        for cc in collection:
            v_id = cc['video_id']

            title_keywords = list()
            for ii in title_indices.get(v_id, []):
                keyword = ii.split('A')[0]
                title_keywords.append(keyword)

            desc_keywords = list()
            for ii in desc_indices.get(v_id, []):
                keyword = ii.split('A')[0]
                desc_keywords.append(keyword)

            output = [cc[ff] for ff in fields]
            output.append(' '.join(title_keywords))
            output.append(' '.join(desc_keywords))
            wf.write('\t'.join(output))
            wf.write('\n')

    with open(appended_collection_header_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        fields.append('title_indices')
        fields.append('desc_indices')
        wf.write(','.join(fields))
