from wsgiref.util import FileWrapper
from abc import abstractmethod, ABC

from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.views import APIView

from pyelzhen.utils_v0.schemas import QueryParamsSchema, PaginationSchema
from .__macros import QUERY_PARAMS_KEYS


class BaseAPIViewWrapper(ABC, APIView):
    view_creator_func = None
    upload_file_name = None
    is_upload_file_list = False
    requestInputData = None
    RequestLog = None

    @staticmethod
    def __get_logger(request):
        try:
            return request._request.logger
        except:
            return None

    def get(self, request, *args, **kwargs):
        logger = self.__get_logger(request)
        queryParams = self.ready_query_params(
            raw_queryParams=request.GET.dict())

        self.requestInputData = kwargs
        requestInfo = self.authenticate(request, **kwargs)

        has_permission = self.checking_permission(
            requestInfo=requestInfo)
        if not has_permission:
            data = 'this "%s" has no permission in "%s"' % (
                self.view_creator_func.__name__, [
                    item.role_name for item in requestInfo.logged_user.role_list])
            self.log_exception(data, requestInfo)
            body, status = self.get_no_http_permission()
            return Response(body, status=status, content_type='application/json')

        kwargs.update({
            'logged_user_id': requestInfo.logged_user_id,
            'requestInfo': requestInfo,
            'logger': logger,

        })
        if queryParams is not None:
            kwargs.update({
                'queryParams': queryParams
            })

        resultTuple = self.view_creator_func(
            request, **kwargs).get(**kwargs)

        if len(resultTuple) == 2:
            body, status = resultTuple
            return Response(body, status=status,
                            content_type='application/json')
        elif len(resultTuple) == 3:
            body, status, file = resultTuple
            if file is not None:
                return self.response_static_file_image(
                    body=body, status=status, file=file)
        else:
            body, status, file, fileStatus = resultTuple
            if file is not None:
                return self.response_file(
                    body=body, status=status, file=file)

    def post(self, request, *args, **kwargs):
        logger = self.__get_logger(request)
        kwargs.update(request.POST.dict())

        # upload file/image ...
        if self.upload_file_name is not None:
            if len(request.FILES) != 0:
                file = request.FILES[self.upload_file_name]
                kwargs.update({self.upload_file_name: file})

        # upload file/image list ...
        if self.is_upload_file_list:
            if len(request.FILES) != 0:
                kwargs.update({'files': request.FILES})

        self.requestInputData = kwargs

        requestInfo = self.authenticate(request, **kwargs)
        has_permission = self.checking_permission(
            requestInfo=requestInfo)
        if not has_permission:
            data = 'this "%s" has no permission in "%s"' % (
                self.view_creator_func.__name__, [
                    item.role_name for item in requestInfo.logged_user.role_list])
            self.log_exception(data, requestInfo)
            body, status = self.get_no_http_permission()
            return Response(body, status=status,
                            content_type='application/json')

        requestInfo.requestInputData = self.requestInputData
        kwargs2 = {
            'logged_user_id': requestInfo.logged_user_id,
            'requestInfo': requestInfo,
            'inputData': kwargs,
            'logger': logger,

        }
        resultTuple = self.view_creator_func(request, **kwargs).post(**kwargs2)

        if len(resultTuple) == 2:
            body, status = resultTuple
            return Response(body, status=status,
                            content_type='application/json')
        elif len(resultTuple) == 3:
            body, status, file = resultTuple
            if file is not None:
                return self.response_static_file_image(
                    body=body, status=status, file=file)
        else:
            body, status, file, fileStatus = resultTuple
            if file is not None:
                return self.response_file(
                    body=body, status=status, file=file)

    def delete(self, request, *args, **kwargs):
        return Response(status=405)

    def put(self, request, *args, **kwargs):
        return Response(status=405)

    def patch(self, request, *args, **kwargs):
        return Response(status=405)

    @staticmethod
    def response_file(body, status, file):
        response = HttpResponse(content_type='application/pdf')
        response['Access-Control-Allow-Origin'] = '*'
        pdfFileName = 'unknown'
        response['Content-Disposition'] = 'inline; filename="%s"' % pdfFileName
        response.write(file)
        return response

    @staticmethod
    def response_static_file_image(body, status, file):
        file_handle = file.path
        document = open(file_handle, 'rb')
        response = HttpResponse(
            FileWrapper(document),
            content_type='application/msword',
        )
        response['Content-Disposition'] = 'attachment; filename="%s"' % file.name
        return response

    @staticmethod
    def get_no_http_authenticate():
        body = {
            'error': {
                'source': 'authentication',
                'code': 'required',
                'message': 'Authentication required'
            }
        }
        status = 401
        return body, status

    @staticmethod
    def get_no_http_permission():
        body = {
            'error': {
                'source': 'authorization',
                'code': 'required',
                'message': 'permission denied'
            }
        }
        status = 403
        return body, status

    @staticmethod
    @abstractmethod
    def create_authenticate_new_interactor(request):
        pass

    def authenticate(self, request, **kwargs):
        authentication_header = request.META.get('HTTP_AUTHORIZATION')
        if authentication_header is None:
            access_token = None
        else:
            access_token = authentication_header.replace('JWT ', '')
        return self.create_authenticate_new_interactor(
            request=request).set_params(
            access_token=access_token,
            view_creator_func_name=self.view_creator_func.__name__,
            requestInputData=self.requestInputData
        ).execute()

    @staticmethod
    @abstractmethod
    def create_checking_user_permission_interactor():
        pass

    def checking_permission(self, requestInfo):
        return self.create_checking_user_permission_interactor().set_params(
            requestInfo=requestInfo,
            view_creator_func_name=self.view_creator_func.__name__,
        ).execute()

    @staticmethod
    def ready_query_params(raw_queryParams):
        if 'format' in raw_queryParams:
            del raw_queryParams['format']

        if not raw_queryParams:
            return None

        new_queryParams = {}
        for key in raw_queryParams:
            if ',' in raw_queryParams[key]:
                new_queryParams[key] = [
                    x for x in raw_queryParams[key].split(',')]
            else:
                new_queryParams[key] = raw_queryParams[key]

        return new_queryParams

    @staticmethod
    @abstractmethod
    def log_exception(message, requestInfo):
        pass

    def query_params_object(self, value: dict):
        pgt = PaginationSchema(**value)
        qps = QueryParamsSchema(**value)
        qps.pagination = pgt
        qps.filters = self._filter_set(value)
        return qps

    @staticmethod
    def _filter_set(value: dict):
        tmp = value.copy()
        for k in value.keys():
            if k in QUERY_PARAMS_KEYS:
                tmp.pop(k)
            return tmp
