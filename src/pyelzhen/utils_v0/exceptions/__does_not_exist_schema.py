from . import ProbeTesterException


class DoesNotExistSchemaException(ProbeTesterException):
    def __init__(self, innerexception=None, schema_name=None):
        super().__init__(
            source='pydantic.BaseModel',
            code='not found',
            message='Schema not found' if schema_name is None else f'{schema_name} not found',
            innerexception=innerexception,
        )
