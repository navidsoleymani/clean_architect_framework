import re
from abc import ABC
from typing import List

from pyelzhen.utils.schemas import FakerDependencySchema
from pyelzhen.utils.schemas import LookupFieldSchema
from .__macros import LAST


class FakeDataCreator(ABC):

    def __init__(self, **kwargs):
        self.default_values.update(kwargs)

    repository = None
    schema = None
    default_values = {}
    dependencies: List[FakerDependencySchema] = []

    @property
    def alias(self):
        model_name = self.get_repository().model.__name__
        tmp = model_name[0]
        name = model_name[1:]
        for char in name:
            if re.Match('[A-Z]', char):
                tmp = tmp + '_' + char
            else:
                tmp = tmp + char
        ret = tmp.lower()
        return ret

    def get(self, pk=None, depth=1):
        lookup_field = LookupFieldSchema(key='pk', value=pk) if pk else []
        ret = self.get_repository().retriever(
            output_schema_class=self.output_schema_class, lookup_field=lookup_field, last_or_first=LAST, depth=depth)
        return ret

    @property
    def output_schema_class(self):
        return self.schema

    @property
    def input_schema_class(self):
        return self.schema

    def create(self, input_data: dict = None, depth=1, **kwargs):
        if input_data is None:
            input_data = dict()
        tmp = self.default_values
        tmp.update(input_data)
        data = self.input_schema_class(**tmp)
        ret = self.get_repository().creator(
            output_schema_class=self.output_schema_class, data=data, depth=depth, **kwargs)
        return ret

    def orphan(self, depth=1):
        ret = self.get(depth=depth)
        if not ret:
            dependencies_orphan = self.__dependencies_maker()
            ret = self.create(depth=depth, input_data=dependencies_orphan)
        return ret

    def __dependencies_maker(self):
        ret = {}
        dependencies = self.dependencies
        for d in dependencies:
            inst = d.engine()
            obj = inst.orphan()
            ret[f'{d.alias}'] = self.__get_pk(obj)
        return ret

    @staticmethod
    def __get_pk(obj):
        if obj is None:
            pk = None
        elif type(obj) is str:
            pk = obj
        else:
            pk = obj.pk
        return pk

    def get_repository(self):
        return self.repository()
