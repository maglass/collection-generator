import sys
import os
import configs

import logging
from core import tokenizer
from core.exceptions import FailCollectionGenerate


def tokenize(x):
    return x.split()
    # return analysis.tokenize(x)


def _make_header_file(fields, output_path):
    with open(output_path, 'w', encoding='utf8') as wf:
        wf.write(','.join(fields))

    logging.info('Write header file: {})'.format(output_path))
    logging.info('Fields ({}): {}'.format(len(fields), ', '.join(fields)))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    argv = sys.argv[1:]
    corpus_path = argv[0]
    corpus_header_path = argv[1]
    title_desc_tokens_path = argv[2]
    title_desc_tokens_header_path = argv[3]

    with open(corpus_path, 'r', encoding=configs.ENCODE_DECODE) as rf, \
            open(title_desc_tokens_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        for n_line, line in enumerate(rf):
            values = line.rstrip('\n').split('\t')

            doc_id = values[0]
            channel_name = values[1]
            channel_id = values[2]
            playlist_id = values[3]
            title = values[4]
            description = values[5]

            output = list()
            output.append(doc_id)
            output.append(channel_name)
            output.append(channel_id)
            output.append(playlist_id)
            output.append(' '.join(tokenize(title)))
            output.append(' '.join(tokenize(description)))
            wf.write('\t'.join(output))
            wf.write('\n')

            if n_line and n_line % 100 == 0:
                print('Run: {}'.format(n_line))

    with open(corpus_header_path, 'r', encoding=configs.ENCODE_DECODE) as rf, \
            open(title_desc_tokens_header_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        wf.write(rf.read())
