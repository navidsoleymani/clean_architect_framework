import math
from datetime import timedelta

from django.utils import timezone
from pyelzhen.utils_v0.functions import isSpringSummer


class RequestLog:
    # LOG_TYPE = (
    #     (1, 'Info'),
    #     (2, 'ProbeTesterException'),
    #     (3, 'Exception')
    # )

    def __init__(
            self,
            # type=None,
            requestInfo=None,
            errorMessage=None,
            levelName=None,
            resultMessage=None
            # exceptionMessage=None
    ):
        # self._type = type
        self._requestInfo = requestInfo
        self._errorMessage = errorMessage
        self._levelName = levelName
        self._resultMessage = resultMessage
        # self._exceptionMessage = exceptionMessage
        self.removePasswordFromInput()

    # @property
    # def type(self):
    #     return self._type
    #
    # @type.setter
    # def type(self, value):
    #     self._type = value

    @property
    def requestInfo(self):
        return self._requestInfo

    @requestInfo.setter
    def requestInfo(self, value):
        self._requestInfo = value

    @property
    def errorMessage(self):
        return self._errorMessage

    @errorMessage.setter
    def errorMessage(self, value):
        self._errorMessage = value

    @property
    def levelName(self):
        return self._levelName

    @levelName.setter
    def levelName(self, value):
        self._levelName = value

    @property
    def resultMessage(self):
        return self._resultMessage

    @resultMessage.setter
    def resultMessage(self, value):
        self._resultMessage = value

    # @property
    # def exceptionMessage(self):
    #     return self._exceptionMessage
    #
    # @exceptionMessage.setter
    # def exceptionMessage(self, value):
    #     self._exceptionMessage = value
    def removePasswordFromInput(self):
        if self._requestInfo is not None:
            if 'password' in self._requestInfo.requestInputData:
                self._requestInfo.requestInputData['password'] = "*******"
            if 'Password' in self.requestInfo.requestInputData:
                self._requestInfo.requestInputData['Password'] = "*******"
            if 'PASSWORD' in self.requestInfo.requestInputData:
                self._requestInfo.requestInputData['PASSWORD'] = "*******"
            if 're_password' in self.requestInfo.requestInputData:
                self._requestInfo.requestInputData['re_password'] = "*******"
            if 'current_password' in self.requestInfo.requestInputData:
                self._requestInfo.requestInputData['current_password'] = "*******"
            if 'repeated_password' in self.requestInfo.requestInputData:
                self._requestInfo.requestInputData['repeated_password'] = "*******"

    def calculate_durationOfView(self):
        if self.requestInfo is None:
            return
        now = timezone.now()
        self.requestInfo.durationOfView = now - self.requestInfo.requested_datetime
        self.requestInfo.durationOfView = self.requestInfo.durationOfView.total_seconds() * 1000

    def calculate_iran_datetime(self):
        tehran_offset = 3.5
        if isSpringSummer():
            tehran_offset += 1

        minute, hour = math.modf(tehran_offset)
        minute = minute * 60

        if self.requestInfo is not None and self.requestInfo.requested_datetime is not None:
            this_time = self.requestInfo.requested_datetime
            self.calculate_durationOfView()
            run_time = self.requestInfo.durationOfView
        else:
            this_time = timezone.now()
            run_time = '-0-'

        iran_datetime = this_time + timedelta(hours=hour, minutes=minute)
        self.requestInfo.requested_datetime_ir = iran_datetime
        message = 'UTC datetime: %s\n' % this_time
        message += 'Iran datetime: %s\n' % iran_datetime
        message += 'Run time of view: %s ms\n' % run_time
        return message

    def print_url(self):
        message = ''
        if self.requestInfo.absolute_url is not None:
            message += 'Request URL: %s\n' % self.requestInfo.absolute_url
        if self.requestInfo.resource2 is not None:
            message += 'View creator function: %s\n' % self.requestInfo.resource2.componentName
        return message

    def print_logged_user(self):
        message = ''
        if self.requestInfo.logged_user_id is not None:
            message += 'User id: %s\n' % self.requestInfo.logged_user_id
            if self.requestInfo.logged_user is not None:
                if self.requestInfo.logged_user.email is not None:
                    message += 'User email: %s\n' % self.requestInfo.logged_user.email
        else:
            message += 'User: Anonymous\n'
        return message

    def print_assignedAnalyzer(self):
        message = ''
        if self.requestInfo.assignedAnalyzer_id is not None:
            message += 'Assigned analyzer id: %s\n' % self.requestInfo.assignedAnalyzer_id
            if self.requestInfo.assignedAnalyzer is not None:
                message += 'Assigned analyzer SN: %s\n' % self.requestInfo.assignedAnalyzer.docItemDetails.productInstance.serial_number
                message += 'Assigned analyzer user: %s\n' % self.requestInfo.assignedAnalyzer.user.email
        else:
            message += 'Assigned analyzer: Anonymous\n'

        return message

    def printRequestInputData(self):
        message = ''
        if self.requestInfo.requestInputData is not None:
            message += 'Request input Data: %s\n\n' % self.requestInfo.requestInputData
        return message

    def print_errorMessage(self):
        message = ''
        if self.errorMessage is not None:
            message += 'Error message: %s\n' % self.errorMessage
        return message

    def generate_resultMessage(self):
        self.resultMessage = '........................ %s LOG ........................\n' % self.levelName
        self.resultMessage += self.calculate_iran_datetime()
        self.resultMessage += self.print_url()
        self.resultMessage += self.print_logged_user()
        self.resultMessage += self.print_assignedAnalyzer()
        self.resultMessage += self.printRequestInputData()
        self.resultMessage += self.print_errorMessage()
