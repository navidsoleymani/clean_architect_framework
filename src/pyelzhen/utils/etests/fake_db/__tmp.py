from typing import Any, List
from abc import ABC
import re

from pydantic import BaseModel as BaseModelSchema
from django.apps import apps

from pyelzhen.utils.schemas import FakerDependencySchema
from pyelzhen.__definitions import ALL, EMPTY


class Object(BaseModelSchema):
    """
    This is a tool for structuring objects and managing the different types of displays of these updates.
    You must set the schema class and object generated by DjangoORM so that you can receive the stored data in schema,
    object DjangoORM or pk formats.
    """
    schema_class: Any
    db: Any

    def sch(self, depth):
        ret = self.schema_class(**self.db.to_dict(depth=depth))
        return ret

    def pk(self):
        ret = self.db.pk
        return ret


class FakeDataCreator(ABC):
    """
    Using this tool, you can create temporary data to use this data for your tests.
    properties:
        app_name: This property represents the name of the Django app that must be set as required.
                  The type format of this is this property string.
        model_name: This property represents the name of the Django model that must be set as required.
                    The type format of this is this property string.
        schema: This property represents schema-class that must be set as required.
                The type format of this is this property pydantic.BaseModel.
        default_values: This property represents default values that must be set as optional.
                The type format of this is this property dictionary.
        dependencies: This property represents the prerequisites for building a model,
                      which itself is a class of the same type that must be set arbitrarily.
                      But keep in mind that filling these prerequisites, although optional, causes a camera.
                       The type format of this is a list of classes with the same type.

    tools:
        get: This tool helps you to produce an object of your choice.
        create: This tool helps you get an object that you have already created.
        orphan: This tool helps you to create and receive an object without considering a specific dependency.
    """

    def __init__(self, **kwargs):
        """
        You can reset the default values when creating an instance of this class.
        """
        self.default_values.update(kwargs)

    repository = None
    app_name = None
    model_name = None
    schema = None
    default_values = {}
    dependencies: List[FakerDependencySchema] = []

    @property
    def model(self):
        return apps.get_model(self.app_name, self.model_name)

    @property
    def alias(self):
        tmp = self.model_name[0]
        name = self.model_name[1:]
        for char in name:
            if re.Match('[A-Z]', char):
                tmp = tmp + '_' + char
            else:
                tmp = tmp + char
        ret = tmp.lower()
        return ret

    def id_generator(self):
        tmp = len(self.__objects) + 1
        objs = self.__objects.copy()
        while True:
            if tmp not in objs.keys():
                break
            tmp += 1
        return tmp

    __objects = {}

    def get(self, pk=None, display='id', depth=1):
        """
        This tool helps you to produce an object of your choice.

        input arguments:
            pk: This field is the characteristic of an object in the database (abbreviation of primary key).
            display: This field is used to specify the display type of the returned object.
                default -> id
                all-type -> [sch, db, id]
                    sch: return pydantic.BaseModel object type
                    db: return django.db.models.Model object type
                    id: return integer
            depth: This is a control field to specify to which layer the database objects should be detailed
                   if the output object is equal to 'sch'.
        return: id(int) or db(django.db.models.Model) or sch(pydantic.BaseModel)
        """
        pk = pk if pk is not None else 1
        obj = self.__objects.get(pk)
        if obj is None:
            ret = None
        else:
            ret = self.__display_switcher(obj=self.__objects[pk], display=display, depth=depth)
        return ret

    # def create(self, display='id', depth=1, **kwargs):
    #     """
    #     This tool helps you get an object that you have already created.
    #
    #     input arguments:
    #         display: This field is used to specify the display type of the returned object.
    #             default -> id
    #             all-type -> [sch, db, id]
    #                 sch: return pydantic.BaseModel object type
    #                 db: return django.db.models.Model object type
    #                 id: return integer
    #         depth: This is a control field to specify to which layer the database objects should be detailed
    #                if the output object is equal to 'sch'.
    #         kwargs: In this section, we can enter input fields to create a new object, or any other control field...
    #     return: id(int) or db(django.db.models.Model) or sch(pydantic.BaseModel)
    #     """
    #     values = self.default_values.copy()
    #     values.update(kwargs)
    #     data = self.schema(**values)
    #     data_pk = self.id_generator()
    #     data.pk = data.id = data_pk
    #     input_data = self.__data_standardization_for_insert_to_db(data.dict())
    #     instance = self.model.objects.create(**input_data)
    #     self.__objects[data_pk] = Object(schema_class=self.schema, db=instance)
    #     return self.get(data_pk, display=display, depth=depth)

    @property
    def output_schema_class(self):
        return self.schema

    @property
    def input_schema_class(self):
        return self.schema

    def create(self, display='id', depth=1, **kwargs):
        tmp = self.default_values
        tmp.update(dict(kwargs))
        data = self.input_schema_class(**tmp)
        ret = self.repository.creator(output_schema_class=self.output_schema_class, data=data, depth=depth)
        return ret

    def orphan(self, display='id', depth=1):
        """
        This tool helps you to create and receive an object without considering a specific dependency.

        input arguments:
            display: This field is used to specify the display type of the returned object.
                default -> id
                all-type -> [sch, db, id]
                    sch: return pydantic.BaseModel object type
                    db: return django.db.models.Model object type
                    id: return integer
            depth: This is a control field to specify to which layer the database objects should be detailed
                   if the output object is equal to 'sch'.
        return: id(int) or db(django.db.models.Model) or sch(pydantic.BaseModel)
        """
        ret = self.get(display=display, depth=depth)
        if not ret:
            dependencies_orphan = self.__dependencies_maker()
            ret = self.create(display=display, depth=depth, **dependencies_orphan)
        return ret

    __dependencies: list = None

    def __dependencies_getter(self, include: list = ALL, exclude: list = EMPTY):
        if self.__dependencies is None:
            dependencies = self.dependencies
            if include != ALL:
                tmp = []
                for i in self.dependencies:
                    if i.engine in include:
                        tmp.append(i)
                dependencies = tmp
            if exclude != EMPTY:
                tmp = dependencies
                for i in self.dependencies:
                    if i.engine in exclude:
                        tmp.remove(i)
            self.__dependencies = dependencies
        return self.__dependencies

    def __dependencies_maker(self, include: list = ALL, exclude: list = EMPTY):
        ret = {}
        dependencies = self.__dependencies_getter(include=include, exclude=exclude)
        for d in dependencies:
            inst = d.engine()
            ret[f'{d.alias}'] = inst.orphan()
        return ret

    # @staticmethod
    # def __display_switcher(obj, display='id', depth=1):
    #     if obj is None:
    #         ret = None
    #     elif display == 'id':
    #         ret = obj.db.pk
    #     elif display == 'sch':
    #         ret = obj.sch(depth=depth)
    #     elif display == 'db':
    #         ret = obj.db
    #     else:
    #         ret = None
    #     return ret
    #
    # def __data_standardization_for_insert_to_db(self, data: dict):
    #     tmp = data.copy()
    #     for key, value in data.items():
    #         if key in self.__many_to_ones_list:
    #             if type(value) == dict:
    #                 value = value['id']
    #             tmp.pop(key)
    #             tmp[f'{key}_id'] = value
    #     return tmp
    #
    # @property
    # def __many_to_ones_list(self):
    #     ret = []
    #     for i in self.model._meta.get_fields():
    #         if i.many_to_one or i.one_to_one:
    #             ret.append(i.name)
    #     return ret