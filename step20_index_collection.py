from core import index
import logging
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    index_name = 'collection-2019-08-15'
    collection_path = 'data/collections/collection-2019-08-14'
    header_path = 'data/collections/header.csv'

    index.delete(index_name)
    index.create(index_name)
    index.bulk(index_name, collection_path, header_path)
