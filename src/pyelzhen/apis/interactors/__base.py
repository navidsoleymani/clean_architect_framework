from pyelzhen.utils.schemas import RequestSchema, NoneOutputSchema
from typing import Optional


class Base:
    request: RequestSchema
    logged_user_id = None
    data = None
    requestInfo = None
    __output_schema_class = None

    @property
    def output_schema_class(self):
        return self.__output_schema_class

    @output_schema_class.setter
    def output_schema_class(self, value):
        if value is None:
            value = NoneOutputSchema
        self.__output_schema_class = value

    def __init__(self, repository):
        self.repository = repository

    def set_params(self, *args, **kwargs):
        self.request: Optional[RequestSchema] = kwargs.get('request')
        self.logged_user_id = kwargs.get('logged_user_id') or self.request.loggedUserId
        self.data = kwargs.get('data') or self.request.inputData
        self.requestInfo = kwargs.get('requestInfo') or self.request.requestInfo
        self.output_schema_class = kwargs.get('outputDataSchemaClass')
        return self

    def execute(self, **kwargs):
        ret = self.repository.run(output_schema_class=self.output_schema_class, **kwargs)
        return ret
