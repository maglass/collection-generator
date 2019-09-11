from time import sleep
import requests
import elasticsearch
from elasticsearch import helpers
from elasticsearch import Elasticsearch
import logging
import json
from . import common

_ELASTIC_SEARCH_HOST = 'http://13.125.252.81:9200'
_client = Elasticsearch(hosts=_ELASTIC_SEARCH_HOST)


def test_tokenize(text):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = common.url_join(_ELASTIC_SEARCH_HOST, 'tokens', '_analyze')

    data = json.dumps({
        "analyzer": "analyzer-000",
        "text": text
    })

    rr = requests.get(url, data=data, headers=headers)
    if not rr.status_code == 200:
        print(rr)
        return

    content = rr.json()
    return [t['token'] for t in content['tokens']]


def _get_index_create_template():
    with open('data/index-template-v0.0.2.json', 'r') as rf:
        template = rf.read()
        return template


def _create_index(name):
    body = _get_index_create_template()
    print(_client.indices.create(name, body=body))


def bulk(index_name, collection_path, header_path, buffer_size=100, sleep_time=0.5):
    def _flush(_buffer):
        logging.info('index {}'.format(len(_buffer)))
        docs = list()
        for bb in _buffer:
            doc = {
                '_index': index_name,
                '_type': '_doc',
                '_id': bb['video_id'],
            }
            doc.update(bb)
            docs.append(doc)

        elasticsearch.helpers.bulk(_client, docs)
        _buffer[:] = list()

    fields = _get_fields(header_path)
    with open(collection_path, 'r', encoding='utf8') as rf:
        buffer = list()
        for line in rf:
            values = line.rstrip('\n').split('\t')
            _id, doc = _p_doc(fields, values)

            buffer.append(doc)
            if buffer_size <= len(buffer):
                _flush(buffer)
                sleep(sleep_time)

    _flush(buffer)


def _get_fields(path):
    rf = open(path, 'r', encoding='utf8')
    line = rf.readline()
    rf.close()
    return line.strip().split(',')


def _p_doc(_fields, _values):
    _doc = {ff: vv for ff, vv in zip(_fields, _values)}
    doc_id = _doc['video_id']
    return doc_id, _doc


def term(doc_id, index_name):
    headers = {'Content-Type': 'application/json'}
    url = 'http://13.125.252.81:9200/{}/_doc/{}/_termvectors'.format(index_name, doc_id)

    body = {
        "fields": ["title", 'description'],
        "offsets": True,
        "payloads": True,
        "positions": True,
        "term_statistics": True,
        "field_statistics": True
    }
    rr = requests.get(url, headers=headers, data=json.dumps(body))
    sleep(0.4)
    content = rr.json()
    title = set(content['term_vectors']['title']['terms'].keys())
    description = set(content['term_vectors']['description']['terms'].keys())
    return {'title': title, 'description': description}


def run(collection_path, header_path, title_desc_tokens_path, title_desc_tokens_header_path):
    logging.getLogger().setLevel(logging.INFO)
    index_name = 'tokens'
    _client.indices.delete(index_name)
    _create_index(index_name)
    bulk(index_name, collection_path, header_path)

    logging.info('start')
    fields = _get_fields(header_path)
    with open(collection_path, 'r', encoding='utf8') as rf, \
            open(title_desc_tokens_path, 'w', encoding='utf8') as wf:
        for n_line, line in enumerate(rf):
            values = line.rstrip('\n').split('\t')
            _id = values[fields.index('video_id')]
            aa = term(_id, 'tokens')
            output = list()
            for ff, vv in zip(fields, values):
                if ff == 'title' or ff == 'description':
                    output.append(' '.join(list(aa[ff])))
                    continue
                output.append(vv)
            wf.write('\t'.join(map(str, output)))
            wf.write('\n')
            if n_line and n_line % 100 == 0:
                logging.info('running: {}'.format(n_line))

    with open(header_path, 'r', encoding='utf8') as rf, \
            open(title_desc_tokens_header_path, 'w', encoding='utf8') as wf:
        wf.write(rf.read())
