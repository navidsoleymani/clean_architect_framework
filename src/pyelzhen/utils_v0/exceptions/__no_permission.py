from . import ProbeTesterException


class NoPermissionException(ProbeTesterException):

    def __init__(self, innerexception=None):
        super().__init__(
            source='permission', code='denied',
            message='Permission denied', innerexception=innerexception)
