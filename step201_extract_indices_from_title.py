import sys

import configs
from core.common import load_collection

if __name__ == '__main__':
    configs.setting_logger()

    argv = sys.argv[1:]
    tokens_path = argv[0]
    tokens_header_path = argv[1]
    indices_path = argv[2]

    corpus = load_collection(tokens_header_path, tokens_path, encoding=configs.ENCODE_DECODE)
    with open(indices_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        for cc in corpus:
            doc_id = cc['video_id']
            title_tokens = cc['title']

            output = list()
            output.append(doc_id)
            values = ['{}A0.0'.format(ii.split('A')[0]) for ii in title_tokens.split()]
            output.extend(values)
            wf.write('\t'.join(output))
            wf.write('\n')
