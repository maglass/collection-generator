import logging
import sys
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

import configs
from core import common
from core.textutils import extract_hangul


def _grouping(data, field, value):
    g_corpus = dict()
    g_text = dict()
    for dd in data:
        key = dd[field]
        li = g_corpus.get(key, list())
        li.append(dd)
        g_corpus[key] = li

        li = g_text.get(key, list())
        li.append(dd[value])
        g_text[key] = li

    return g_corpus, g_text


def _extract_indices(_text, _docs):
    if not _text:
        logging.warning('Empty text')
        return list()
    # tf, idf 학습
    model = TfidfVectorizer(tokenizer=lambda x: x.split()).fit(_text)
    word_names = np.array(model.get_feature_names())
    vectors = model.transform(_text).toarray()

    _indices = dict()
    for vec, dd in zip(vectors, _docs):
        top_words = np.argsort(vec)
        top_words = top_words.flatten()[::-1]
        top_words = top_words[:10]

        idx = [(word_names[ii], vec[ii]) for ii in top_words if vec[ii] > 0.0]
        video_id = dd['video_id']
        _indices[video_id] = idx
    return _indices


def _handling_text(_text, _docs, _black_keywords):
    removed_text = _remove_duplicate_text(_text)
    removed_hangul_text = [extract_hangul(tt) for tt in removed_text]

    remove_stop_words_text = list()
    for tt, dd in zip(removed_hangul_text, _docs):
        stop_words = list()
        stop_words.append(dd['title'])
        stop_words.append(dd['channel_name'])
        stop_words.extend(_black_keywords)
        remove_stop_words_text.append(_remove_words(tt, stop_words))

    result_text = list()
    result_doc = list()
    for tt, dd in zip(remove_stop_words_text, _docs):
        if not tt:
            continue
        result_text.append(tt)
        result_doc.append(dd)
    return result_text, result_doc


def _remove_duplicate_text(_text):
    counter = Counter(_text)

    result = list()
    for tt in _text:
        if counter[tt] > 1:
            result.append("")
        else:
            result.append(tt)
    return result


def _remove_words(_text, _stop_words):
    for sw in _stop_words:
        _text = _text.replace(sw, '')
    return _text


def _load_desc_black_keywords(path):
    _output = set()
    with open(path, 'r', encoding=configs.ENCODE_DECODE) as rf:
        for line in rf:
            value = line.strip()
            if value:
                _output.add(value)

    return _output


def _expand_words(_text):
    new = list()
    for tt in _text:
        temp = list()
        _values = tt.split()
        for vv in _values:
            vvv = vv.split('A')
            kk = vvv[0]
            ff = int(vvv[1])
            eee = ' '.join([kk] * ff)
            temp.append(eee)
        new.append(' '.join(temp))
    return new


if __name__ == '__main__':
    configs.setting_logger()

    argv = sys.argv[1:]
    tokens_path = argv[0]
    tokens_header_path = argv[1]
    indices_path = argv[2]
    black_keywords_path = argv[3]

    corpus = common.load_collection(tokens_header_path, tokens_path, configs.ENCODE_DECODE)
    black_keywords = _load_desc_black_keywords(black_keywords_path)

    total = dict()
    indices = dict()
    group, group_text = _grouping(corpus, 'playlist_id', 'description')
    for p_id, docs in group.items():
        text = group_text[p_id]
        text = _expand_words(text)
        pre_text, pre_docs = _handling_text(text, docs, black_keywords)
        if not pre_text:
            continue
        ind = _extract_indices(pre_text, pre_docs)
        indices.update(ind)

    logging.info('extract index: {:,}'.format(len(indices)))
    with open(indices_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        for v_id, index in indices.items():
            output = list()
            output.append(v_id)
            values = ['{}A{}'.format(ii[0], ii[1]) for ii in index]
            output.extend(values)
            wf.write('\t'.join(output))
            wf.write('\n')
