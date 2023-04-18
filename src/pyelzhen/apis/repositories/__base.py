from typing import Optional, List, Union

from pydantic import BaseModel

from pyelzhen.__definitions import ALL, EMPTY
from pyelzhen.utils.schemas import (
    LookupFieldSchema,
    PaginationOutputSchema,
    QueryParamsSchema,
)

from .__base_ import BaseModelProbeTesterRepo
from .__macro import FIRST


class Base(BaseModelProbeTesterRepo):
    _queryset = None
    output_schema_class = None

    def __base_save_to_db(self, obj, force_insert, force_update, using, update_fields, many=False):
        if not many:
            obj.save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
            ret = obj
        else:
            ret = self.model.objects.bulk_create(obj)
        return ret

    @staticmethod
    def base_update_to_db(query, data: dict):
        query.update(**data)
        return query[0]

    def base_insert_to_db(self, obj, many=False):
        ret = self.__base_save_to_db(
            obj=obj, force_insert=True, force_update=False,
            using=None, update_fields=None, many=many)
        return ret

    def output(self, data, many=False, depth=1):
        if many:
            if len(data):
                if type(data[0]) == dict:
                    ret = [self.output_schema_class(**i) for i in data]
                else:
                    ret = [self.output_schema_class(**i.to_dict(depth=depth)) for i in data]
            else:
                ret = []
        else:
            ret = self.output_schema_class(**data.to_dict(depth=depth))
        return ret

    def get_queryset(self):
        if self._queryset is None:
            self._queryset = self.model.objects
        return self._queryset

    def creator(
            self, output_schema_class: BaseModel, data: Union[BaseModel, List[BaseModel]],
            depth=1, include_fields: set = ALL,
            exclude_fields: set = EMPTY, **kwargs) -> Union[BaseModel, List[BaseModel]]:
        if type(data) is not list:
            ret = self.__creator(
                output_schema_class=output_schema_class, data=data, depth=depth,
                include_fields=include_fields, exclude_fields=exclude_fields)
        else:
            ret = self.__bulk_creator(
                output_schema_class=output_schema_class, data=data, depth=depth,
                include_fields=include_fields, exclude_fields=exclude_fields)
        return ret

    def __creator(
            self, output_schema_class: BaseModel, data: BaseModel, depth=1,
            include_fields: set = ALL, exclude_fields: set = EMPTY) -> BaseModel:

        exclude_fields = exclude_fields if exclude_fields != EMPTY else set()

        self.output_schema_class = output_schema_class
        input_data = data.dict(exclude=exclude_fields) \
            if include_fields == ALL else data.dict(include=include_fields, exclude=exclude_fields)
        input_data = self.__data_standardization_for_insert_to_db(input_data)
        obj = self.model(**input_data)
        obj = self.base_insert_to_db(obj)
        return self.output(data=obj, depth=depth)

    def __bulk_creator(
            self, output_schema_class: BaseModel, data: List[BaseModel], depth=1,
            include_fields: set = ALL, exclude_fields: set = EMPTY) -> List[BaseModel]:
        exclude_fields = exclude_fields if exclude_fields != EMPTY else set()

        self.output_schema_class = output_schema_class
        objs = []
        for i in data:
            input_data = i.dict(exclude=exclude_fields) \
                if include_fields == ALL else i.dict(include=include_fields, exclude=exclude_fields)
            input_data = self.__data_standardization_for_insert_to_db(input_data)
            obj = self.model(**input_data)
            objs.append(obj)
        objs = self.base_insert_to_db(objs, many=True)
        return self.output(data=objs, depth=depth, many=True)

    def lister(self, output_schema_class: BaseModel,
               query_params: QueryParamsSchema, depth=1, paginate=True, **kwargs) -> BaseModel:
        self.output_schema_class = output_schema_class
        insts = self.set_controllers_by_query_params(query_params)
        if paginate:
            ret = self.pagination(
                data=insts,
                page=query_params.pagination.page,
                page_size=query_params.pagination.page_size,
                url=query_params.base_url,
                depth=depth,
            )
        else:
            ret = self.output(data=insts, many=True, depth=depth)
        return ret

    def set_controllers_by_query_params(self, query_params):
        queryset = self.get_queryset()
        if len(query_params.values):
            queryset = queryset.values(*query_params.values)
        if len(query_params.annotates):
            queryset = queryset.annotate(**query_params.annotates)
        if len(query_params.filters):
            queryset = queryset.filter(**query_params.filters)
        if len(query_params.excludes):
            queryset = queryset.exclude(**query_params.excludes)
        queryset = queryset.distinct()
        if len(query_params.orderings):
            queryset = queryset.order_by(*query_params.orderings)
        queryset = queryset.all()
        return queryset

    def pagination(self, data, page, page_size, url, depth=1):
        cnt = data.count()
        data = self.output(data=data, many=True, depth=depth)
        ret = PaginationOutputSchema(
            count=cnt,
            page_number=page,
            page_size=page_size,
            result=data,
            url=url,
        )
        return ret

    def retriever(
            self, output_schema_class: BaseModel, lookup_field: Union[LookupFieldSchema, List],
            last_or_first: str = FIRST, depth=1, **kwargs) -> Optional[BaseModel]:
        self.output_schema_class = output_schema_class
        lkpf = lookup_field if type(lookup_field) is List else [lookup_field]
        filters = self.__filters(*lkpf)
        query_set = self.get_queryset().filter(**filters)
        query_set = query_set.first() if last_or_first == FIRST else query_set.last()
        if query_set is None:
            return None
        return self.output(query_set, depth=depth)

    @staticmethod
    def __filters(*args):
        ret = {}
        for i in args:
            if type(i) is LookupFieldSchema:
                ret[i.key] = i.value
        return ret

    def updater(self, output_schema_class: BaseModel, lookup_field: LookupFieldSchema,
                data: BaseModel, update_fields: set = ALL, depth=1, **kwargs) -> Optional[BaseModel]:
        self.output_schema_class = output_schema_class
        input_data = data.dict() if update_fields == ALL else data.dict(include=update_fields)
        obj = self.get_queryset().filter(**{lookup_field.key: lookup_field.value}).last()
        if obj is None:
            return None
        obj = self.base_update_to_db(
            query=self.get_queryset().filter(pk=obj.pk), data=input_data)
        return self.output(data=obj, depth=depth)

    def __data_standardization_for_insert_to_db(self, data: dict):
        tmp = data.copy()
        for key, value in data.items():
            if key in self.__many_to_ones_list:
                if type(value) == dict:
                    value = value['id']
                tmp.pop(key)
                tmp[f'{key}_id'] = value
        return tmp

    @property
    def __many_to_ones_list(self):
        ret = []
        for i in self.model._meta.get_fields():
            if i.many_to_one or i.one_to_one:
                ret.append(i.name)
        return ret
