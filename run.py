import subprocess
import os
import sys
from datetime import datetime
import logging
from core import index

if __name__ == '__main__':
    path = sys.argv[1]

    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    collection_root_path = 'data/base_collections/{}'.format(now)
    subprocess.call(['python', 'step00_make_base_collection.py', path, collection_root_path])

    index_name = 'collection-{}'.format(now)
    collection_path = os.path.join(collection_root_path, 'base_collection')
    header_path = os.path.join(collection_root_path, 'header.tsv')
    subprocess.call(['python', 'step10_index_collection.py', index_name, collection_path, header_path])

    # TODO: check collection and index
    index.switch_alias(index_name, 'collection-service')
