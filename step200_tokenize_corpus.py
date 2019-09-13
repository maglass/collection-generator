import sys

import configs
from core import textutils

if __name__ == '__main__':
    configs.setting_logger()

    argv = sys.argv[1:]
    corpus_path = argv[0]
    corpus_header_path = argv[1]
    title_desc_tokens_path = argv[2]
    title_desc_tokens_header_path = argv[3]
    version = 'v0.0.2'
    textutils.tokenize_corpus(corpus_path, corpus_header_path, title_desc_tokens_path,
                              title_desc_tokens_header_path, version)
