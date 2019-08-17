import json
import os
import sys
import configs
import logging

from core import docparser
from core.exception import NotValidatedArguments, FailParsingDocument, FailCollectionGenerate


def _check_validated_arguments(arguments):
    if not len(arguments) == 2:
        raise NotValidatedArguments(arguments, "Invalidated argument number")

    if not os.path.isfile(arguments[0]):
        raise NotValidatedArguments(arguments, "Not exists youtube data file")

    if os.path.isdir(arguments[1]):
        raise NotValidatedArguments(arguments, "Already exists base-collection directory")


if __name__ == '__main__':
    """
    data_path:
        . Youtube 데이터 파일 경로
    collection_dir_path:
        . 생성될 header, base-collection 파일을 저장할 디렉토리 경로
    """
    logging.getLogger().setLevel(logging.INFO)
    argv = sys.argv[1:]
    _check_validated_arguments(argv)

    data_path = argv[0]
    output_dir_path = argv[1]

    # Make output directory
    os.mkdir(output_dir_path)

    # Make header file
    fields = configs.DOC_FIELDS
    header_path = os.path.join(output_dir_path, configs.HEADER_FILE_NAME)
    with open(header_path, 'w', encoding=configs.ENCODE_DECODE) as wf:
        wf.write('\t'.join(fields))

    # Make collection file
    seq = configs.COLLECTION_VALUE_SEP
    null = configs.COLLECTION_NULL_VALUE
    collection_path = os.path.join(output_dir_path, configs.BASE_COLLECTION_FILE_NAME)

    n_total = 0
    n_skip = 0
    rf = open(data_path, 'r', encoding=configs.ENCODE_DECODE)
    wf = open(collection_path, 'w', encoding=configs.ENCODE_DECODE)
    for line in rf:
        n_total += 1

        try:
            data = json.loads(line)
            d_type = data['type']
            if d_type == 'youtube':
                doc = docparser.to_video(data)
            elif d_type == 'playlist':
                doc = docparser.to_playlist(data)
            else:
                raise FailParsingDocument()
            wf.write(seq.join(str(doc.get(ff, null)) for ff in fields))
            wf.write('\n')
        except Exception as e:
            n_skip += 1
            logging.error(e)

    rf.close()
    wf.close()

    n_documents = n_total - n_skip
    logging.info('Total youtube data rows: {}'.format(n_total))
    logging.info('Skip youtube data rows: {}'.format(n_skip))
    logging.info('Collection documents num: {}'.format(n_documents))
    if n_documents < (n_total * 0.8):
        raise FailCollectionGenerate('Fail because too much skip documents: {} / {}'.format(n_skip, n_total))
