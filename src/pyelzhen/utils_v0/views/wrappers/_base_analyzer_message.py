from rest_framework.response import Response
from rest_framework.views import APIView
from abc import ABC, abstractmethod


class BaseAPIViewWrapperAnalyzerMessage(ABC, APIView):
    view_creator_func = None
    requestInputData = None

    @staticmethod
    def __get_logger(request):
        try:
            return request._request.logger
        except:
            return None

    def get(self, request, *args, **kwargs):
        logger = self.__get_logger(request)
        self.requestInputData = kwargs
        requestInfo = self.authenticate(request, **kwargs)

        if isinstance(requestInfo, dict):
            # authentication error ...
            return Response(requestInfo, status=400,
                            content_type='application/json')

        inputData = {
            'assignedAnalyzer_id': requestInfo.assignedAnalyzer_id,
            'ip_address': requestInfo.requested_ip,
            'requestInfo': requestInfo,
            'logger': logger,
        }
        kwargs.update(inputData)
        body, status = self.view_creator_func(
            request, **kwargs).get(**kwargs)
        return Response(body, status=status,
                        content_type='application/json')

    def post(self, request, *args, **kwargs):
        logger = self.__get_logger(request)
        self.requestInputData = request.data
        requestInfo = self.authenticate(request, **kwargs)

        if isinstance(requestInfo, dict):
            # authentication error ...
            return Response(requestInfo, status=400,
                            content_type='application/json')

        kwargs.update({
            'assignedAnalyzer_id': requestInfo.assignedAnalyzer_id,
            'ip_address': requestInfo.requested_ip,
            'inputData': request.data,
            'requestInfo': requestInfo,
            'logger': logger,
        })
        body, status = self.view_creator_func(
            request, **kwargs).post(**kwargs)

        return Response(body, status=status,
                        content_type='application/json')

    @staticmethod
    @abstractmethod
    def create_authenticate_assigned_analyzer_interactor(request):
        pass

    def authenticate(self, request, **kwargs):
        token = request.query_params.get('token', None)

        return self.create_authenticate_assigned_analyzer_interactor(
            request=request).set_params(
            hashedUid=token,
            requestInputData=self.requestInputData
        ).execute()
