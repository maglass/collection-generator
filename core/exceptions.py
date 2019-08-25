class NotValidatedArguments(BaseException):
    def __init__(self, arguments, because):
        super().__init__('{} args: {}'.format(because, ' '.join(arguments)))


class FailCollectionGenerate(BaseException):
    pass


class FailParsingDocument(BaseException):
    pass
