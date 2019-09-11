class NotValidatedArguments(BaseException):
    def __init__(self, arguments, because):
        super().__init__('{} args: {}'.format(because, ' '.join(arguments)))


class FailRequestAPI(BaseException):
    def __init__(self, msg, url, params=None):
        if not params:
            super().__init__('msg: {} url: {}'.format(msg, url))
        else:
            super().__init__('msg: {} url: {} params: {}'.format(msg, url, params))


class FailCollectionGenerate(BaseException):
    pass


class FailParsingDocument(BaseException):
    pass


class FailAnalysisText(BaseException):
    pass
