class ProbeTesterException(Exception):

    def __init__(self, source, code, message, innerexception=None):
        super().__init__(message)
        self._source = source
        self._code = code
        self._innerexception = innerexception

    @property
    def source(self):
        return self._source

    @property
    def code(self):
        return self._code

    @property
    def innerexception(self):
        return self._innerexception
