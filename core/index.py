import requests
import logging
import json
from time import sleep
from . import configs
from . import common


def create(index_name, host=None):
    if not host:
        host = configs.ELASTIC_SEARCH_HOST

    url = common.url_join(host, index_name)
    if exist(url):
        raise Exception('Exist index: {}'.format(index_name))
    else:
        template = _get_create_index_template()
        body = json.dumps(template)
        headers = {'Content-Type': 'application/json; charset=utf-8'}

        rr = requests.put(url, headers=headers, data=body)
        if not rr.status_code == 200:
            raise Exception('Error create index')

        logging.info("Success create index: {}".format(index_name))


def add_alias(index_name, alias, host=None):
    if not host:
        host = configs.ELASTIC_SEARCH_HOST
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = common.url_join(host, '_aliases')
    actions = [{"add": {"index": index_name, "alias": alias}}]
    body = json.dumps({"actions": actions})
    rr = requests.post(url, headers=headers, data=body)


def switch_alias(index_name, alias, host=None):
    if not host:
        host = configs.ELASTIC_SEARCH_HOST

    registered_index_names = _get_index_names_with_alias(alias)
    if not registered_index_names:
        add_alias(index_name, alias)
    else:
        actions = list()
        prev_index_name = registered_index_names[0]
        actions.append({"remove": {"index": prev_index_name, "alias": alias}})
        actions.append({"add": {"index": index_name, "alias": alias}})

        body = json.dumps({'actions': actions})
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = common.url_join(host, '_aliases')
        requests.post(url, data=body, headers=headers)


def _get_index_names_with_alias(alias_name, host=None):
    if not host:
        host = configs.ELASTIC_SEARCH_HOST
    url = common.url_join(host, '_alias', alias_name)
    rr = requests.get(url)
    if rr.status_code == 404:
        return list()

    content = rr.json()
    index_names = list(content.keys())
    index_names.sort()
    return index_names


def bulk(index_name, collection_path, header_path, host=None, buffer_size=100, sleep_time=0.3):
    def _p_doc(_fields, _values):
        _doc = {ff: vv for ff, vv in zip(_fields, _values)}
        if _doc['video_id']:
            doc_id = _doc['video_id']
        else:
            doc_id = _doc['playlist_id']
        return doc_id, _doc

    def _flush(_buffer):
        logging.info('index {}'.format(len(_buffer) // 2))
        body = '\n'.join(json.dumps(b) for b in _buffer) + '\n'
        requests.post(url, headers=headers, data=body)
        _buffer[:] = list()

    if not host:
        host = configs.ELASTIC_SEARCH_HOST

    buffer_size *= 2
    url = common.url_join(host, index_name, '_doc', '_bulk?pretty')
    headers = {'Content-Type': 'application/x-ndjson'}

    fields = _get_fields(header_path)
    with open(collection_path, 'r', encoding='utf8') as rf:
        buffer = list()
        seen = set()
        for line in rf:
            values = line.rstrip('\n').split('\t')
            _id, doc = _p_doc(fields, values)
            if _id in seen:
                logging.info('duplicate')
                seen.add(_id)
            buffer.append({"index": {"_id": _id}})
            buffer.append(doc)
            if buffer_size <= len(buffer):
                _flush(buffer)
                sleep(sleep_time)

        _flush(buffer)


def exist(url):
    rr = requests.head(url)
    return rr.status_code == 200


def delete(index_name, host=None):
    if not host:
        host = configs.ELASTIC_SEARCH_HOST

    url = common.url_join(host, index_name)
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    rr = requests.delete(url, headers=headers)
    if not rr.status_code == 200:
        logging.info('Error delete index')
    else:
        logging.info('Success delete index: {}'.format(index_name))


def _get_create_index_template():
    properties = dict()
    properties['type'] = {"type": "keyword"}
    properties['video_id'] = {"type": "keyword"}
    properties['playlist_id'] = {"type": "keyword"}

    properties['title'] = {"type": "text"}
    properties['description'] = {"type": "text"}
    properties['views'] = {"type": "keyword"}
    properties['length'] = {"type": "keyword"}
    properties['rating'] = {"type": "float"}
    properties['video_ids'] = {"type": "keyword"}

    _doc = dict()
    _doc['properties'] = properties

    output = dict()
    output['mappings'] = dict()
    output['mappings']['_doc'] = _doc
    return output


def _get_fields(path):
    rf = open(path, 'r', encoding='utf8')
    line = rf.readline()
    rf.close()
    return line.strip().split('\t')
