import os
import logging

ENCODE_DECODE = 'utf8'

OUTPUT_DIRECTORY_PATH = 'output'

STEP1_DIRECTORY_NAME = 'step01'
STEP01_COLLECTION_FILE_NAME = 'base_collection.tsv'
STEP01_COLLECTION_HEADER_FILE_NAME = 'base_collection_header.csv'
STEP01_CORPUS_FILE_NAME = 'corpus.tsv'
STEP01_CORPUS_HEADER_FILE_NAME = 'corpus_header.csv'


def setting_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(logging.INFO)


def get_local_output_root_directory_path(directory_name):
    return os.path.join(OUTPUT_DIRECTORY_PATH, directory_name)


def get_step01_output_directory_path(directory_name):
    root_output_dir = get_local_output_root_directory_path(directory_name)
    return os.path.join(root_output_dir, STEP1_DIRECTORY_NAME)


def get_bucket_step01_output_directory_path(directory_name):
    return '{}/{}'.format(directory_name, STEP1_DIRECTORY_NAME)


def get_step01_collection_header_path(directory_name):
    step01_output_directory_path = get_step01_output_directory_path(directory_name)
    return os.path.join(step01_output_directory_path, STEP01_COLLECTION_HEADER_FILE_NAME)


def get_step01_collection_path(directory_name):
    step01_output_directory_path = get_step01_output_directory_path(directory_name)
    return os.path.join(step01_output_directory_path, STEP01_COLLECTION_FILE_NAME)


def get_step01_corpus_path(directory_name):
    step01_output_directory_path = get_step01_output_directory_path(directory_name)
    return os.path.join(step01_output_directory_path, STEP01_CORPUS_FILE_NAME)


def get_step01_corpus_header_path(directory_name):
    step01_output_directory_path = get_step01_output_directory_path(directory_name)
    return os.path.join(step01_output_directory_path, STEP01_CORPUS_HEADER_FILE_NAME)


STEP02_DIRECTORY_NAME = 'step02'
STEP02_DESC_TOKENS_NAME = 'title_desc_tokens.tsv'
STEP02_DESC_TOKENS_HEADER_NAME = 'title_desc_tokens_header.csv'
STEP02_TITLE_INDICES_NAME = 'title_indices.tsv'
STEP02_DESC_INDICES_NAME = 'desc_indices.tsv'
STEP02_DESC_INDICES_HEADER_NAME = 'desc_indices_header.csv'
STEP02_APPENDED_COLLECTION_NAME = 'appended_desc_indices_collection.tsv'
STEP02_APPENDED_COLLECTION_HEADER_NAME = 'appended_desc_indices_collection_header.csv'


def get_step02_output_directory_path(directory_name):
    root_output_dir = get_local_output_root_directory_path(directory_name)
    return os.path.join(root_output_dir, STEP02_DIRECTORY_NAME)


def get_bucket_step02_output_directory_path(directory_name):
    return '{}/{}'.format(directory_name, STEP02_DIRECTORY_NAME)


def get_step02_desc_tokens_path(directory_name):
    step02_output = get_step02_output_directory_path(directory_name)
    return os.path.join(step02_output, STEP02_DESC_TOKENS_NAME)


def get_step02_desc_tokens_header_path(directory_name):
    step02_output = get_step02_output_directory_path(directory_name)
    return os.path.join(step02_output, STEP02_DESC_TOKENS_HEADER_NAME)


def get_step02_title_indices_path(directory_name):
    step02_output = get_step02_output_directory_path(directory_name)
    return os.path.join(step02_output, STEP02_TITLE_INDICES_NAME)


def get_step02_desc_indices_path(directory_name):
    step02_output = get_step02_output_directory_path(directory_name)
    return os.path.join(step02_output, STEP02_DESC_INDICES_NAME)


def get_step02_desc_indices_header_path(directory_name):
    step02_output = get_step02_output_directory_path(directory_name)
    return os.path.join(step02_output, STEP02_DESC_INDICES_HEADER_NAME)


def get_step02_append_collection_path(directory_name):
    step02_output = get_step02_output_directory_path(directory_name)
    return os.path.join(step02_output, STEP02_APPENDED_COLLECTION_NAME)


def get_step02_append_collection_header_path(directory_name):
    step02_output = get_step02_output_directory_path(directory_name)
    return os.path.join(step02_output, STEP02_APPENDED_COLLECTION_HEADER_NAME)


STEP03_DIRECTORY_NAME = 'step03'
STEP03_CAPTION_QUALITY_PATH = 'caption_quality.tsv'
STEP03_IMAGE_QUALITY_PATH = 'image_quality.tsv'
STEP03_APPEND_CAPTION_QUALITY_COLLECTION = 'appended_caption_quality_collection.tsv'
STEP03_APPEND_CAPTION_QUALITY_HEADER_COLLECTION = 'appended_caption_quality_collection_header.csv'


def get_step03_output_directory_path(directory_name):
    root_output_dir = get_local_output_root_directory_path(directory_name)
    return os.path.join(root_output_dir, STEP03_DIRECTORY_NAME)


def get_bucket_step03_output_directory_path(directory_name):
    return '{}/{}'.format(directory_name, STEP03_DIRECTORY_NAME)


def get_step03_caption_quality_score_path(directory_name):
    output_dir = get_step03_output_directory_path(directory_name)
    return os.path.join(output_dir, STEP03_CAPTION_QUALITY_PATH)


def get_step03_image_quality_score_path(directory_name):
    output_dir = get_step03_output_directory_path(directory_name)
    return os.path.join(output_dir, STEP03_IMAGE_QUALITY_PATH)


def appended_get_step03_caption_quality_collection_path(directory_name):
    output_dir = get_step03_output_directory_path(directory_name)
    return os.path.join(output_dir, STEP03_APPEND_CAPTION_QUALITY_COLLECTION)


def get_step03_caption_quality_collection_header_path(directory_name):
    output_dir = get_step03_output_directory_path(directory_name)
    return '{}/{}'.format(output_dir, STEP03_APPEND_CAPTION_QUALITY_HEADER_COLLECTION)
