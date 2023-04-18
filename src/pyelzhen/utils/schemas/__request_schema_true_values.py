from . import (
    LookupFieldSchema,
    QueryParamsSchema,
    PaginationSchema,
)


def __input_data(**kwargs):
    tmp = kwargs.get('defaultValues') or {}
    input_data = kwargs.get('inputData')
    tmp.update(input_data)
    input_field_name_list = kwargs.get('inputFieldNameList') or {}
    tmp_ = tmp.copy()
    for k, v in tmp.items():
        if k not in input_field_name_list:
            tmp_.pop(k)
    tmp = tmp_
    hard_information = kwargs.get('hardInformation') or {}
    tmp.update(hard_information)
    schema_class = kwargs.get('inputDataSchemaClass')
    ret = schema_class(**tmp) if tmp and schema_class else tmp
    return ret


def __input_data_schema_class(**kwargs):
    ret = kwargs.get('inputDataSchemaClass')
    return ret


def __lookup_field(**kwargs):
    ret = LookupFieldSchema(key=kwargs.get('lookupFieldKey'), value=kwargs.get('lookupFieldValue'))
    return ret


def __query_params(**kwargs):
    pgn = PaginationSchema(
        page_size=kwargs.get('pageSize'), page=kwargs.get('page'),
        next=kwargs.get('next'), previous=kwargs.get('previous'), )
    ret = QueryParamsSchema(
        search=kwargs.get('search'), filters=kwargs.get('filters'),
        orderings=kwargs.get('orderings'), pagination=pgn)
    return ret


def __logged_user_id(**kwargs):
    ret = kwargs.get('logged_user_id')
    return ret


def __request_info(**kwargs):
    ret = kwargs.get('requestInfo')
    return ret


def __input_field_name_list(**kwargs):
    ret = kwargs.get('inputFieldNameList') or []
    ret = set(ret)
    return ret


def request_schema_true_values(**kwargs):
    req = {
        'inputData': __input_data(**kwargs),
        'lookupField': __lookup_field(**kwargs),
        'queryParams': __query_params(**kwargs),
        'loggedUserId': __logged_user_id(**kwargs),
        'requestInfo': __request_info(**kwargs),
        'inputDataSchemaClass': __input_data_schema_class(**kwargs),
        'inputFieldNameList': __input_field_name_list(**kwargs),
    }
    return req
