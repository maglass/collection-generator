from core import analysis

if __name__ == '__main__':
    # analysis.close()
    analysis.make_analyzer()
    print(analysis.tokenize('세바시 강연'))
