import sys

import configs
from core import pipeline

if __name__ == '__main__':
    configs.setting_logger()

    argv = sys.argv[1:]
    directory_name = argv[0]

    steps = list()
    corpus_path = configs.get_step01_corpus_path(directory_name)
    corpus_header_path = configs.get_step01_corpus_header_path(directory_name)
    tokens_path = configs.get_step02_desc_tokens_path(directory_name)
    tokens_header_path = configs.get_step02_desc_tokens_header_path(directory_name)
    steps.append(['Tokenize corpus', 'python', 'step200_tokenize_corpus.py',
                  corpus_path, corpus_header_path, tokens_path, tokens_header_path])

    title_indices_path = configs.get_step02_title_indices_path(directory_name)
    steps.append(['Extract indices from descriptions', 'python', 'step201_extract_indices_from_title.py',
                  tokens_path, tokens_header_path, title_indices_path])

    desc_black_keywords_path = 'dictionary/desc_blacks.txt'
    desc_indices_path = configs.get_step02_desc_indices_path(directory_name)
    steps.append(['Extract indices from descriptions', 'python', 'step202_extract_indices_from_desc.py',
                  tokens_path, tokens_header_path, desc_indices_path, desc_black_keywords_path])

    collection_path = configs.get_step01_collection_path(directory_name)
    collection_header_path = configs.get_step01_collection_header_path(directory_name)
    appended_collection_path = configs.get_step02_append_collection_path(directory_name)
    appended_collection_header_path = configs.get_step02_append_collection_header_path(directory_name)
    steps.append(['Append tokens', 'python', 'step203_append_desc_tokens.py',
                  collection_path, collection_header_path,
                  title_indices_path,
                  desc_indices_path,
                  appended_collection_path, appended_collection_header_path])

    step02_output_path = configs.get_step02_output_directory_path(directory_name)
    step02_bucket_output_path = configs.get_bucket_step02_output_directory_path(directory_name)
    steps.append(
        ['Update base collection to bucket', 'python', 'step101_upload_base_collection.py',
         step02_output_path, step02_bucket_output_path])

    pipeline.run(steps)
