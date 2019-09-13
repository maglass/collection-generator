from core import textutils

if __name__ == '__main__':
    textutils.build_tokenizer('final')
    print(textutils.tokenize('다린'))
    # corpus_path = 'output/2019-09-12-19-40-50/step01/corpus.tsv'
    # corpus_header_path = 'output/2019-09-12-19-40-50/step01/corpus_header.csv'
    # 
    # output_path = 'tokens_nori.tsv'
    # output_header = 'header_nori.csv'
    # version = 'nori'
    # textutils.tokenize_corpus(corpus_path, corpus_header_path, output_path,
    #                           output_header, version)
