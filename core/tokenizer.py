import requests
import json
from time import sleep
from . import common
from .exceptions import FailAnalysisText

_ELASTIC_SEARCH_HOST = 'http://13.125.252.81:9200'


def tokenize(text):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = common.url_join(_ELASTIC_SEARCH_HOST, 'collection-nori', '_analyze')

    data = json.dumps({
        "analyzer": "nori",
        "text": text
    })

    rr = requests.get(url, data=data, headers=headers)
    if not rr.status_code == 200:
        raise FailAnalysisText(rr.text)
    sleep(1)
    content = rr.json()

    return [t['token'] for t in content['tokens']]


def close():
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = common.url_join(_ELASTIC_SEARCH_HOST, 'analyzer-000')
    rr = requests.delete(url, headers=headers)
    print(rr.content)


def make_analyzer():
    data = {
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "analyzer-000": {
                            "type": "custom",
                            "tokenizer": "tokenizer-000",
                            "filter": ["lowercase", "filter-000"]
                        }
                    },
                    "tokenizer": {
                        "tokenizer-000": {
                            "type": "nori_tokenizer",
                            "decompound_mode": "mixed",
                            "user_dictionary": "dictionaries/compound.txt"
                        }
                    },
                    "filter": {
                        "filter-000": {
                            "type": "nori_part_of_speech",
                            "stoptags": [
                                "E",
                                "IC",
                                "J",
                                "MAG",
                                "MM",
                                "NA",
                                "NR",
                                "SC",
                                "SE",
                                "SF",
                                "SH",
                                "SL",
                                "SN",
                                "SP",
                                "SSC",
                                "SSO",
                                "SY",
                                "UNA",
                                "UNKNOWN",
                                "VA",
                                "VCN",
                                "VCP",
                                "VSV",
                                "VV",
                                "VX",
                                "XPN",
                                "XR",
                                "XSA",
                                "XSN",
                                "XSV"
                            ]
                        },
                        "synonym": {
                            "type": "synonym",
                            "synonym": {
                                "type": "synonym",
                                "synonyms": ["foo, bar => baz"]
                            }
                        }
                    },
                }
            }
        }
    }

    body = json.dumps(data)
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    close()
    url = common.url_join(_ELASTIC_SEARCH_HOST, 'analyzer-000')
    rr = requests.put(url, headers=headers, data=body)
    print(rr.content)
