import re


def url_join(*args):
    return '/'.join(a.strip('/') for a in args)


def clean_text(text):
    return re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
