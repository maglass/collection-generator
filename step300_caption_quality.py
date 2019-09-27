import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import configs
from core import common


def _grouping_corpus(data, field):
    corpus_group = dict()
    for dd in data:
        key = dd[field]
        li = corpus_group.get(key, list())
        li.append(dd)
        corpus_group[key] = li

    return corpus_group


def _make_documents(data):
    _documents = list()
    for dd in data:
        term_freq = dict()
        for field in ['title', 'description', 'caption']:
            for tt in dd[field].split():
                term, freq = tt.split('A')
                freq = int(freq)
                tmp = term_freq.get(term, 0)
                term_freq[term] = tmp + freq

        doc = list()
        for term, freq in term_freq.items():
            doc.extend([term] * freq)

        if doc:
            _documents.append(' '.join(doc))

    return _documents


if __name__ == '__main__':
    configs.setting_logger()

    argv = sys.argv[1:]
    tokens_path = argv[0]
    tokens_header_path = argv[1]
    quality_score_path = argv[2]

    corpus = common.load_collection(tokens_header_path, tokens_path, configs.ENCODE_DECODE)
    g_video = _grouping_corpus(corpus, 'channel_id')
    with open(quality_score_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        for values in g_video.values():
            documents = _make_documents(values)
            model = TfidfVectorizer(tokenizer=lambda x: x.split()).fit(documents)

            for vv in values:
                if not vv['caption']:
                    continue

                title_desc = list()
                for tt in vv['title'].split() + vv['description'].split():
                    term, freq = tt.split('A')
                    freq = int(freq)
                    title_desc.extend([term] * freq)

                vec_title_desc = model.transform([' '.join(title_desc)])
                captions = list()
                for tt in vv['caption'].split():
                    term, freq = tt.split('A')
                    freq = int(freq)
                    captions.extend([term] * freq)
                vec_caption = model.transform([' '.join(captions)])

                wf.write('{}\t{}'.format(vv['video_id'], cosine_similarity(vec_title_desc, vec_caption)[0][0]))
                wf.write('\n')
