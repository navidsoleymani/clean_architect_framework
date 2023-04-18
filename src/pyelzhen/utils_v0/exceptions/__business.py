from . import ProbeTesterException


class BusinessException(ProbeTesterException):
    def __init__(self, message, innerexception=None):
        super().__init__(
            source='value', code='Business',
            message=message, innerexception=innerexception)
