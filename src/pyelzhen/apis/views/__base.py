from typing import List, Tuple, Optional

from rest_framework.status import HTTP_200_OK

from pyelzhen.__definitions import ALL
from pyelzhen.utils.schemas import RequestSchema
from pyelzhen.utils.schemas import ResponseSchema, CookieSchema
from pyelzhen.utils_v0.exceptions import serialize_exceptions


class Base:
    """
    This layer is made and customized to manage the data received from the client side as well as the data sent to
    the client side. In this layer, you can validate, structure and serialize the received data and then pass the data
     to the lower layers.
    """
    request: RequestSchema

    def __init__(self, interactor, **kwargs):
        """
        In creating an instance of this class, we set the following fields.

        :param interactor:  This parameter is received to connect the view layer with the interactor layer, and setting
                            the value of this parameter is mandatory. This parameter is of the type of a factory of an
                            interactor class.
        :param input_schema_class:  In this parameter, we specify in which schema the received data should be sent to
                                    the lower layers - this schema manages data generation and structuring of data
                                     received from the client. Setting this parameter is also mandatory.
        :param output_schema_class: In this parameter, we specify in which schema the sent data should be entered into
                                    the view layer - this schema manages the data generation and structuring of the
                                    received data from the lower layers. Setting this parameter is mandatory.
        :param input_field_name_list:   This parameter can filter the input data. This parameter is received as a
                                        dictionary or a set. If the input data is at a depth of one, you can send this
                                        filtering as a set, and if you want to filter the data of lower depths of
                                        the schema, you must enter the input value as a dictionary as below.
                                        example:
                                            - depth == 1
                                                - :{
                                                    'field1',
                                                    'field2',
                                                    'field3',
                                                    ...
                                                }
                                            - depth > 1
                                                - :{
                                                    'field1' : True,
                                                    'field2': {
                                                        'field2.1' : True,
                                                        'field2.2' : True,
                                                        'field2.2' : {
                                                            'field2.2.1' : True,
                                                            },
                                                    },
                                                    'field3':True,
                                                    ...
                                                }
        :param output_field_name_list:  This parameter can filter the output data. This parameter is received as
                                        a dictionary or a set. If the data sent to the client is at a depth of one,
                                        you can send this filtering as a set, and if you want to filter the data of
                                        lower depths of the schema, you must enter the input value as a dictionary
                                        as below.
                                        example:
                                            - depth == 1
                                                - :{
                                                    'field1',
                                                    'field2',
                                                    'field3',
                                                    ...
                                                }
                                            - depth > 1
                                                - :{
                                                    'field1' : True,
                                                    'field2': {
                                                        'field2.1' : True,
                                                        'field2.2' : True,
                                                        'field2.2' : {
                                                            'field2.2.1' : True,
                                                            },
                                                    },
                                                    'field3':True,
                                                    ...
                                                }
        :param lookup_field_key:    You will sometimes need to read a record from the database. You must request
                                    this record with one or more values that this record is unique for this data.
                                    You can specify the title of the lookup field (or lookup fields) in this parameter.
                                     Note that this value is exactly the same value that you save the field or
                                     fields with this title in your database. This value is received as a string or a
                                     list of strings. Entering this value is optional in normal mode, and if it is
                                     not set, this value is equal to the set ID.
        :param expected_status_code:    This parameter is created to specify the status of your personalized code and
                                        is optionally set.
        """
        self.interactor = interactor

        self.input_schema_class = kwargs.get('input_schema_class')
        self.output_schema_class = kwargs.get('output_schema_class')

        self.input_field_name_list = kwargs.get('input_field_name_list')
        self.output_field_name_list = kwargs.get('output_field_name_list') or ALL

        self.lookup_field_key = kwargs.get('lookup_field_key')

        self.expected_status_code = kwargs.get('expected_status_code') or HTTP_200_OK

        self.default_values = kwargs.get('default_values')
        self.hard_information = kwargs.get('hard_information')

    @serialize_exceptions
    def post(self, **kwargs):
        self.request = RequestSchema(
            inputDataSchemaClass=self.input_schema_class,
            lookupFieldKey=self.lookup_field_key,
            inputFieldNameList=self.input_field_name_list,
            lookupFieldValue=kwargs.get('inputData').get(self.lookup_field_key) if kwargs.get('inputData') else None,
            defaultValues=self.default_values,
            hardInformation=self.hard_information,
            **kwargs,
        )
        rslt = self.interactor.set_params(
            request=self.request,
            outputDataSchemaClass=self.output_schema_class,
        ).execute()
        rsp = self.response(rslt)
        return rsp

    def response(
            self, value, cookies: Optional[List[CookieSchema]] = None, content_type: str = None,
            headers: Optional[List[Tuple]] = None, files: Optional[List] = None):
        if value is None:
            rsp = value, self.expected_status_code
        else:
            value = value if type(
                value) == dict else value.dict() if self.output_field_name_list == ALL else value.dict(
                include=self.output_field_name_list)
            rsp = value, self.expected_status_code
        content, status_code = rsp
        rsp = ResponseSchema(
            content=content, status_code=status_code, cookies=cookies,
            content_type=content_type, headers=headers, files=files)
        return rsp
