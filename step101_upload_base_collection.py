import json
import os

import sys
import logging
from datetime import datetime
from utils import burkets

import configs
from core.exceptions import NotValidatedArguments, FailParsingDocument, FailCollectionGenerate
from core.common import clean_text


def _check_validated_arguments(arguments):
    if not len(arguments) == 1:
        raise NotValidatedArguments(arguments, "Invalidated argument number")

    if not os.path.isdir(arguments[0]):
        raise NotValidatedArguments(arguments, "Not exists base-collection data file")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    argv = sys.argv[1:]
    _check_validated_arguments(argv)

    base_collection_path = argv[0]
    base_collection_root_dir_name = os.path.basename(base_collection_path)

    burkets.mkdir('youtube-collections', base_collection_root_dir_name)
    for filename in os.listdir(base_collection_path):
        file_path = os.path.join(base_collection_path, filename)
        bucket_path = '{}/{}'.format(base_collection_root_dir_name, filename)
        burkets.upload_file('youtube-collections', bucket_path, file_path)
