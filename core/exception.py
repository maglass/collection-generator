class NotValidatedArguments(BaseException):
    def __init__(self, arguments, because):
        super().__init__('{} args: {}'.format(because, ' '.join(arguments)))


class FailParsingDocument(BaseException):
    pass


class FailCollectionGenerate(BaseException):
    pass
