import re


def url_join(*args):
    return '/'.join(a.strip('/') for a in args)


def clean_text(text):
    return re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)

if __name__ == '__main__':
    print(type(clean_text('asfdasfasdfa34###34sf')))