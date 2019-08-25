import os

ENCODE_DECODE = 'utf8'

OUTPUT_DIRECTORY_PATH = 'output'
BASE_COLLECTION_DIRECTORY_NAME = 'base_collections'
BASE_COLLECTION_DIRECTORY_PATH = os.path.join(OUTPUT_DIRECTORY_PATH, BASE_COLLECTION_DIRECTORY_NAME)

HEADER_FILE_NAME = 'header.tsv'
BASE_COLLECTION_FILE_NAME = 'base_collection.tsv'
BASE_COLLECTION_INFO_FILE_NAME = 'information.tsv'

COLLECTION_VALUE_SEP = '\t'
COLLECTION_NULL_VALUE = ''

DOC_FIELDS = list()
DOC_FIELDS.append('type')
DOC_FIELDS.append('video_id')
DOC_FIELDS.append('playlist_id')
DOC_FIELDS.append('title')
DOC_FIELDS.append('view_cnt')
DOC_FIELDS.append('video_length')
DOC_FIELDS.append('rating')
DOC_FIELDS.append('like_cnt')
DOC_FIELDS.append('video_ids')
DOC_FIELDS.append('video_cnt')
