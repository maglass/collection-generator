import re
import logging


def url_join(*args):
    return '/'.join(a.strip('/') for a in args)


def load_fields(header_path, sep=','):
    with open(header_path, 'r') as rf:
        line = rf.readline()
        fields = [ll.strip() for ll in line.split(sep)]
        logging.info("Load fields: {}".format(', '.join(fields)))

    if not len(fields) == len(set(fields)):
        logging.warning('Duplicate fields: {}'.format(fields))

    return fields


hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')


def extract_hangul(text):
    return ' '.join(''.join(hangul.sub('', text)).split())


def clean_text(text):
    return re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
