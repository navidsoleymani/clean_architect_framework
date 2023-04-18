from . import ProbeTesterException


class EntityDoesNotExistException(ProbeTesterException):
    def __init__(self, innerexception=None, entityName=None):
        super().__init__(
            source='entity', code='not found',
            message='Entity not found' if entityName is None else f'{entityName} not found',
            innerexception=innerexception)
