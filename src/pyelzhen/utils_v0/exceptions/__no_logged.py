from . import ProbeTesterException


class NoLoggedException(ProbeTesterException):

    def __init__(self, innerexception=None):
        super().__init__(
            source='authentication', code='required',
            message='Authentication required',
            innerexception=innerexception)
