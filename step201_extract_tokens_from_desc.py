import logging
import numpy as np
import os
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import dot
from numpy.linalg import norm
from textwrap import wrap
import configs
import sys
from core import common

from core.common import extract_hangul


def _load_corpus(h_path, c_path):
    # Load fields from header file
    fields = common.load_fields(h_path)

    # Load corpus
    n_fields = len(fields)
    n_skip = 0
    _corpus = list()
    with open(c_path, 'r', encoding=configs.ENCODE_DECODE) as rf:
        for n_line, line in enumerate(rf):
            values = line.rstrip('\n').split('\t')
            if not n_fields == len(values):
                logging.warning('Skip line "not equal field ({}), values ({})'.format(n_fields, len(values)))
                n_skip += 1
                continue
            cor = {ff: vv for ff, vv in zip(fields, values)}
            _corpus.append(cor)
    logging.info('load corpus: {:,} skip: {:,}'.format(len(_corpus), n_skip))
    return _corpus


def _grouping_corpus(data, field, value):
    corpus_group = dict()
    text_group = dict()
    for dd in data:
        key = dd[field]
        li = corpus_group.get(key, list())
        li.append(dd)
        corpus_group[key] = li

        li = text_group.get(key, list())
        li.append(dd[value])
        text_group[key] = li

    return corpus_group, text_group


def _extract_indices(_text, _docs):
    if not _text:
        logging.warning('Empty text')
        return list()
    # tf, idf 학습
    model = TfidfVectorizer(tokenizer=lambda x: x.split()).fit(_text)
    word_names = np.array(model.get_feature_names())
    vectors = model.transform(_text).toarray()

    output = dict()
    for vec, dd in zip(vectors, _docs):
        top_words = np.argsort(vec).flatten()[::-1]
        top_words = top_words[:15]

        _indices = [(word_names[ii], vec[ii]) for ii in top_words]
        video_id = dd['video_id']
        output[video_id] = _indices
    return output


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


def cosine_sim(one, other):
    return dot(one, other) / (norm(one) * norm(other))


def _calculate_sim_title_text(_text, _docs):
    title_text = list()
    for tt, dd in zip(_text, _docs):
        merged = ' '.join([tt, dd['title']])
        title_text.append(merged)

    # tf, idf 학습
    model = TfidfVectorizer(tokenizer=lambda x: x.split()).fit(title_text)

    sims = list()
    for tt, dd in zip(_text, _docs):
        title_vec = model.transform([dd['title']])
        title_vec = title_vec.toarray().flatten()
        text_vec = model.transform([tt])
        text_vec = text_vec.toarray().flatten()
        ss = cosine_sim(title_vec, text_vec)
        sims.append(ss)
    return sims


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


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    argv = sys.argv[1:]
    tokens_path = argv[0]
    tokens_header_path = argv[1]
    indices_path = argv[2]
    indices_header_path = argv[3]
    black_keywords_path = argv[4]

    corpus = _load_corpus(tokens_header_path, tokens_path)
    black_keywords = _load_desc_black_keywords(black_keywords_path)
    total = dict()
    indices = dict()
    g_playlist, g_text = _grouping_corpus(corpus, 'playlist_id', 'description')
    for p_id, docs in g_playlist.items():
        text = g_text[p_id]
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
