import logging
import sys

import configs
from core import text





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
    logging.getLogger().setLevel(logging.INFO)
    text.run(corpus_path, corpus_header_path, title_desc_tokens_path, title_desc_tokens_header_path)
