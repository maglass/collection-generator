from core import index
import logging
import sys

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    index_name = sys.argv[1]
    collection_path = sys.argv[2]
    header_path = sys.argv[3]

    logging.info(index_name)
    logging.info(collection_path)
    logging.info(header_path)

    index.delete(index_name)
    index.create(index_name)
    index.bulk(index_name, collection_path, header_path)
