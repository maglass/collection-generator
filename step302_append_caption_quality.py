import sys

import configs
from core import common


def _load_quality(path):
    _output = dict()
    with open(path, 'r', encoding=configs.ENCODE_DECODE) as rf:
        for line in rf:
            values = line.rstrip('\n').split('\t')
            doc_id = values[0]
            ss = float(values[1])
            _output[doc_id] = ss
    return _output


if __name__ == '__main__':
    configs.setting_logger()

    argv = sys.argv[1:]
    collection_path = argv[0]
    collection_header_path = argv[1]
    quality_path = argv[2]
    image_path = argv[3]

    appended_collection_path = argv[4]
    appended_collection_header_path = argv[5]

    fields = common.load_fields(collection_header_path)
    collection = common.load_collection(collection_header_path, collection_path, configs.ENCODE_DECODE)
    quality = _load_quality(quality_path)
    image_quality = _load_quality(image_path)
    with open(appended_collection_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        for cc in collection:
            v_id = cc['video_id']
            score = quality.get(v_id, 0)
            image_score = image_quality.get(v_id, 0)
            output = [cc[ff] for ff in fields]
            output.append(score)
            output.append(image_score)
            wf.write('\t'.join(map(str, output)))
            wf.write('\n')

    with open(appended_collection_header_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        fields.append('caption_quality')
        fields.append('image_quality')
        wf.write(','.join(fields))
