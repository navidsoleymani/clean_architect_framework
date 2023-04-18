import re
import uuid
from datetime import datetime

import pandas as pd


class DataType:
    @staticmethod
    def set_none_value_to_string_empty(value):
        if value is None:
            return ""
        if str(value).strip() == 'undefined':
            return ""
        if str(value).strip() == 'null':
            return ""
        if str(value).strip().lower() == 'none':
            return ""
        if str(value).strip() == '':
            return ""
        return str(value)

    @staticmethod
    def get_none_value(value):
        if value is None:
            return None
        if value == '':
            return None
        if str(value).lower().strip() == 'undefined':
            return None
        if value == ' ':
            return None
        if str(value).lower().strip() == 'null':
            return None
        if str(value).lower() == 'none':
            return None
        return value

    @staticmethod
    def get_id(value):
        if DataType.get_none_value(value) is None:
            return None
        return int(value)


    @staticmethod
    def get_bool(value):
        if DataType.get_none_value(value) is None:
            return None
        value = str(value).strip().lower()
        if value == 'true':
            return True

        if value == 'True':
            return True

        if value == 'yes':
            return True

        if value == '1':
            return True
        if value == 'false':
            return False

        if value == 'False':
            return False

        if value == 'no':
            return False

        if value == '0':
            return False

        return None

    @staticmethod
    def get_int(value):

        if DataType.get_none_value(value) is None:
            return None

        return int(value)

    @staticmethod
    def get_float(value):

        if DataType.get_none_value(value) is None:
            return None

        return float(value)

    @staticmethod
    def get_date(value):

        if DataType.get_none_value(value) is None:
            return None
        if type(value) is str:
            return value
        if type(value) is int:
            return pd.to_datetime(value, format='%Y%m%d')
        return value.strftime('%Y/%d/%m')

    @staticmethod
    def get_date_dash_yyyymmdd(value):
        return value.strftime('%Y-%m-%d')

    @staticmethod
    def get_date_dash_yyyymmddhhmmss(value):
        return value.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_time(value):
        if DataType.get_none_value(value) is None:
            return None
        if type(value) is str:
            return value

    @staticmethod
    def get_string(value):
        result = DataType.get_none_value(value)
        if not result:
            return result
        else:
            return str(result).strip()

    @staticmethod
    def get_string_for_serialize(value):
        data = DataType.get_none_value(value)
        if data is None:
            return ''
        return data

    @staticmethod
    def get_string_without_tags(value):
        result = DataType.set_none_value_to_string_empty(value)
        text = re.sub('<.*?>', '', result)
        return text


    @staticmethod
    def get_date_yyyymmdd(datetime):
        return datetime.strftime('%Y%m%d')

    @staticmethod
    def get_uuid(value):
        try:
            return uuid.UUID(str(value))
        except ValueError:
            return None

    @staticmethod
    def get_float_2_decimal(value):
        if value is None:
            return 0
        if value == '':
            return 0

        return round(float(value), 2)

    @staticmethod
    def get_date_str_with_slash(value):
        if DataType.get_none_value(value) is None:
            return None
        if type(value) is str:
            value = value.split('/')
            value = value[2] + '-' + value[1] + '-' + value[0]
            print(value)
            return value

    @staticmethod
    def get_date_salsh_mmddYYYY(value):
        if DataType.get_none_value(value) is None:
            return None
        if type(value) is str:
            date_obj = datetime.strptime(value,'%m/%d/%Y')
            return date_obj