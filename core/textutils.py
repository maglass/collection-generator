import re
import requests
import json
import logging
from time import sleep

from elasticsearch import Elasticsearch, helpers

from . import common
from .exceptions import FailRequestAPI

_ELASTIC_SEARCH_HOST = 'http://13.125.252.81:9200'
_INDEX_NAME = 'tokens'

_client = Elasticsearch(hosts=_ELASTIC_SEARCH_HOST)

_ANALYZER_NAME = "analyzer-000"
_TEMPLATE_PATH = 'D:\workspace\collection-generator\data\index-template-v0.0.2.json'

_HUNGUL = re.compile('[^ ㄱ-ㅣ가-힣]+')


def extract_hangul(text):
    return ' '.join(''.join(_HUNGUL.sub('', text)).split())


def clean_text(text):
    return re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)


def tokenize(text, analyzer_name):
    headers = dict()
    headers['Content-Type'] = 'application/json; charset=utf-8'

    params = dict()
    params['analyzer'] = analyzer_name
    params['text'] = text
    data = json.dumps(params)

    url = common.url_join(_ELASTIC_SEARCH_HOST, _INDEX_NAME, '_analyze')
    rr = requests.get(url, data=data, headers=headers)
    if not rr.status_code == 200:
        FailRequestAPI(rr.content, url)
        return

    content = rr.json()
    print(content)
    return [t['token'] for t in content['tokens']]


def tokenize_corpus(corpus_path, header_path, tokens_path, tokens_header_path, version):
    logging.getLogger().setLevel(logging.INFO)
    build_tokenizer(version)
    _index_corpus(_INDEX_NAME, corpus_path, header_path)

    logging.info('Start search docs and get tokens')

    fields = _get_fields(header_path)
    idx_doc_id = fields.index('video_id')
    with open(corpus_path, 'r', encoding='utf8') as rf, \
            open(tokens_path, 'w', encoding='utf8') as wf:

        for n_line, line in enumerate(rf):
            values = line.rstrip('\n').split('\t')

            doc_id = values[idx_doc_id]
            tokens = search_and_get_tokens(doc_id)

            output = list()
            for ff, vv in zip(fields, values):
                if ff not in ['title', 'description', 'caption']:
                    output.append(vv)
                else:
                    # title, description, caption 토큰으로 변경
                    output.append(' '.join(list(tokens[ff])))

            wf.write('\t'.join(map(str, output)))
            wf.write('\n')

            if n_line and n_line % 100 == 0:
                logging.info('Running: {}'.format(n_line))

    logging.info('Write tokens header: {}'.format(tokens_header_path))
    with open(header_path, 'r', encoding='utf8') as rf, \
            open(tokens_header_path, 'w', encoding='utf8') as wf:
        wf.write(rf.read())


def build_tokenizer(version):
    if _client.indices.exists(_INDEX_NAME):
        _client.indices.delete(_INDEX_NAME)

    _create_index(version)


def _index_corpus(index_name, collection_path, header_path, buffer_size=100, sleep_time=1):
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

        helpers.bulk(_client, docs)
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


def search_and_get_tokens(doc_id):
    headers = dict()
    headers['Content-Type'] = 'application/json; charset=utf-8'

    params = dict()
    params['fields'] = ["title", 'description', 'caption']
    data = json.dumps(params)
    url = common.url_join(_ELASTIC_SEARCH_HOST, _INDEX_NAME, '_doc', doc_id, '_termvectors')

    rr = requests.get(url, headers=headers, data=data)
    if not rr.status_code == 200:
        raise FailRequestAPI(rr.content, url, data)
    content = rr.json()
    sleep(0.5)

    terms = content['term_vectors']['title']['terms']
    title = ['{}A{}'.format(tt[0], tt[1]['term_freq']) for tt in terms.items()]

    terms = content['term_vectors']['description']['terms']
    description = ['{}A{}'.format(tt[0], tt[1]['term_freq']) for tt in terms.items()]

    terms = content['term_vectors']['caption']['terms']
    caption = ['{}A{}'.format(tt[0], tt[1]['term_freq']) for tt in terms.items()]
    return {'title': title, 'description': description, 'caption': caption}


def _create_index(version):
    body = _get_index_create_template(version)
    print(_client.indices.create(_INDEX_NAME, body=body))


def _get_index_create_template(version):
    index_template_path = 'data/index_templates/index-template-{}.json'.format(version)
    with open(index_template_path, 'r') as rf:
        template = rf.read()
        return template


def _get_fields(path):
    rf = open(path, 'r', encoding='utf8')
    line = rf.readline()
    rf.close()
    return line.strip().split(',')


def _p_doc(_fields, _values):
    _doc = {ff: vv for ff, vv in zip(_fields, _values)}
    doc_id = _doc['video_id']
    return doc_id, _doc
