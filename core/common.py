import logging


def load_fields(header_path, sep=','):
    with open(header_path, 'r', encoding='utf8') as rf:
        line = rf.readline()
        fields = [ll.strip() for ll in line.split(sep)]
        logging.info("Load fields: {}".format(', '.join(fields)))

    if not len(fields) == len(set(fields)):
        logging.warning('Duplicate fields: {}'.format(fields))

    return fields


def load_collection(h_path, c_path, encoding):
    fields = load_fields(h_path)

    # Load corpus
    n_fields = len(fields)
    n_skip = 0
    _corpus = list()
    with open(c_path, 'r', encoding=encoding) as rf:
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


def url_join(*args):
    return '/'.join(a.strip('/') for a in args)
