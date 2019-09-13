import sys

import configs
from core import common


def _load_expanded_indices(path):
    _output = dict()
    with open(path, 'r', encoding=configs.ENCODE_DECODE) as rf:
        for line in rf:
            values = line.rstrip('\n').split('\t')
            doc_id = values[0]
            _indices = values[1:]
            _output[doc_id] = _indices
    return _output


if __name__ == '__main__':
    configs.setting_logger()

    argv = sys.argv[1:]
    collection_path = argv[0]
    collection_header_path = argv[1]
    title_indices_path = argv[2]
    desc_indices_path = argv[3]
    appended_collection_path = argv[4]
    appended_collection_header_path = argv[5]

    fields = common.load_fields(collection_header_path)
    collection = common.load_collection(collection_header_path, collection_path, encoding=configs.ENCODE_DECODE)
    title_indices = _load_expanded_indices(title_indices_path)
    desc_indices = _load_expanded_indices(desc_indices_path)
    with open(appended_collection_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        for cc in collection:
            v_id = cc['video_id']

            title_keywords = list()
            for ii in title_indices.get(v_id, []):
                keyword = ii.split('A')[0]
                title_keywords.append(keyword)

            desc_keywords = list()
            for ii in desc_indices.get(v_id, []):
                keyword = ii.split('A')[0]
                desc_keywords.append(keyword)

            output = [cc[ff] for ff in fields]
            output.append(' '.join(title_keywords))
            output.append(' '.join(desc_keywords))
            wf.write('\t'.join(output))
            wf.write('\n')

    with open(appended_collection_header_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        fields.append('title_indices')
        fields.append('desc_indices')
        wf.write(','.join(fields))
