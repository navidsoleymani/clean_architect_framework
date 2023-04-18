from typing import Any

from pydantic import BaseModel

from . import (
    LookupFieldSchema,
    QueryParamsSchema,
    request_schema_true_values,
)


class RequestSchema(BaseModel):
    def __init__(self, **kwargs):
        kwargs = request_schema_true_values(**kwargs)
        super().__init__(**kwargs)

    inputData: Any
    lookupField: LookupFieldSchema
    queryParams: QueryParamsSchema
    loggedUserId: int
    requestInfo: Any
    inputDataSchemaClass: Any
    inputFieldNameList: set
