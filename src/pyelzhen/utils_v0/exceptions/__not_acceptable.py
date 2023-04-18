from . import ProbeTesterException


class NotAcceptableException(ProbeTesterException):
    def __init__(self, innerexception=None):
        super().__init__(
            source='value', code='notAcceptable',
            message='not acceptable', innerexception=innerexception)
