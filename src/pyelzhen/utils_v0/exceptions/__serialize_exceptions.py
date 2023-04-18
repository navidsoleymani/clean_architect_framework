import traceback

from pyelzhen.__settings import probeTesterlogger
from . import *
from pyelzhen.utils_v0.serializers import ProbeTesterExceptionSerializer
from pyelzhen.utils_v0.entities import RequestLog

exception_status_code_mapper = {
    InvalidEntityException: 422,
    EntityDoesNotExistException: 404,
    ConflictException: 409,
    NoLoggedException: 401,
    NoPermissionException: 403,
    BusinessException: 300,
    NotAcceptableException: 406,
    WrongValueException: 422,
    ProbeTesterExceptionSerializer: 400,
    InvalidSchemaException: 422,
    DoesNotExistSchemaException: 404,
}


def serialize_exceptions(func):
    def func_wrapper(*args, **kwargs):
        try:
            result_func = func(*args, **kwargs)
            requestLog = RequestLog(requestInfo=kwargs['requestInfo']) \
                if 'requestInfo' in kwargs else RequestLog()
            probeTesterlogger.info(requestLog)
            return result_func
        except ProbeTesterException as e:
            requestLog = RequestLog(requestInfo=kwargs['requestInfo']) \
                if 'requestInfo' in kwargs else RequestLog()
            requestLog.errorMessage = e
            probeTesterlogger.exception(requestLog)
            # print debug tracing ...
            traceback.print_exc()
            body = ProbeTesterExceptionSerializer.serialize(e)
            status = exception_status_code_mapper[type(e)]
        except Exception as e:
            requestLog = RequestLog(requestInfo=kwargs['requestInfo']) \
                if 'requestInfo' in kwargs else RequestLog()
            requestLog.errorMessage = e
            probeTesterlogger.exception(requestLog)
            # print debug tracing ...
            traceback.print_exc()
            # unknown exception has been thrown id = 1000
            body = {"unknown exception has been thrown id = 1000"}
            status = 400
        return body, status

    return func_wrapper
