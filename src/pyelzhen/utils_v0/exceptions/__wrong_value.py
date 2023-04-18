from . import ProbeTesterException


class WrongValueException(ProbeTesterException):
    def __init__(self, innerexception=None):
        super().__init__(
            source='value', code='not found',
            message='wrong value', innerexception=innerexception)
