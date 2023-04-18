from typing import Optional

from django.db.models import F, Case
from django.db.models import Model
from pyelzhen.utils_v0.exceptions import (
    EntityDoesNotExistException,
    InvalidEntityException,
)
from pyelzhen.utils_v0.entities import FilteredOutput, BaseENT
from pyelzhen.utils_v0.objects import DataType


class BaseModelProbeTesterRepo:
    SMALL_INFO_SIZE = 'small'
    MEDIUM_INFO_SIZE = 'medium'
    FULL_INFO_SIZE = 'full'
    FOR_LIST = 'for_list'

    def __init__(self, model=None, mapdb=None):
        self._model = model
        self._mapdb = mapdb
        self.count_of_record = 0

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    @property
    def model(self):
        return self._model

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    @property
    def mapdb(self):
        return self._mapdb

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # def check_exist(self, params, excluding={}):
    #     count = self._count(params=params, excluding=excluding)
    #     return count > 0

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def check_exist(self, baseFilterENT):
        count = self.count(baseFilterENT)
        return count > 0

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def set_transition_fields(self, id, transitionHistory_id, transition_id):
        model_updated = self._model.objects.get(id=id)
        model_updated.transitionHistory_id = transitionHistory_id
        model_updated.transition_id = transition_id
        self.save(model_updated)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # def get_by_queryParams(self, queryParms):
    #     params = {}
    #     for key in queryParms:
    #         if isinstance(queryParms[key], list):
    #             params[key.lower() + '__in'] = queryParms[key]
    #         else:
    #             params[key.lower()] = queryParms[key]
    #
    #     productModelName_list = self._model.objects.filter(**params).distinct()
    #     list = []
    #     for item in productModelName_list:
    #         list.append(self._mapdb.decode(item))
    #     return list

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_columns_ordering_pagination(self, baseFilterENT):
        results = self.__get_db_list_with_pagination(baseFilterENT)
        return FilteredOutput(
            results=self.__decode_list(
                db_list=results,
                info_size=self.FOR_LIST),
            # results=results,
            count=self.count_of_record,
            page_size=baseFilterENT.page_size
        )

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_columns_ordering_pagination_dict(self, baseFilterENT, patternDB_dict=None):
        results = self.__get_db_list_with_pagination(baseFilterENT, patternDB_dict=patternDB_dict)
        return FilteredOutput(
            results=results,
            count=self.count_of_record,
            page_size=baseFilterENT.page_size
        )

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_columns_ordering_pagination_mapdb_func(self, baseFilterENT, mapdb_func=None):
        results = self.__get_db_list_with_pagination(baseFilterENT)
        return FilteredOutput(
            results=[mapdb_func(q) for q in results],
            count=self.count_of_record,
            page_size=baseFilterENT.page_size
        )

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_db_by_id(self, id):
        try:
            return self._model.objects.get(id=id)

        except self._model.DoesNotExist:
            raise InvalidEntityException(
                message='This id dose not exist.',
                source='id',
                code='not_exist')

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_db_by_id(self, id):
        return self.__get_db_by_id(id)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_db_by_uuid(self, uuid):
        try:
            return self._model.objects.get(uuid=uuid)

        except self._model.DoesNotExist:
            raise InvalidEntityException(
                message='This uuid does not exist.',
                source='uuid',
                code='not_exist')

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def delete_by_id(self, id):
        try:
            db_Model = self._model.objects.get(id=id).delete()
            return db_Model  # self._mapdb.decode_db(db_Model[1])
        except self._model.DoesNotExist:
            raise EntityDoesNotExistException

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def delete_by_filters(self, baseFilterENT):
        params = self.__convert_to_orm_params(baseFilterENT.filter_list, baseFilterENT)
        excluding = self.__convert_to_orm_params(baseFilterENT.exclude_list, baseFilterENT)
        self._model.objects.filter(**params).exclude(**excluding).delete()

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_columns(self, baseFilterENT):
        db_list = self.__get_db_list(baseFilterENT)
        return self.__decode_list(db_list=db_list, info_size=self.SMALL_INFO_SIZE)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_columns_dict(self, baseFilterENT, patternDB_dict=None):
        return self.__get_db_list(baseFilterENT, patternDB_dict=patternDB_dict)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_columns_mapdb_func(self, baseFilterENT, mapdb_func=None):
        db_list = self.__get_db_list(baseFilterENT)
        return [mapdb_func(q) for q in db_list]

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_columns_mediumInfo(self, baseFilterENT):
        db_list = self.__get_db_list(baseFilterENT)
        return self.__decode_list(db_list=db_list, info_size=self.MEDIUM_INFO_SIZE)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_columns_fullInfo(self, baseFilterENT):
        db_list = self.__get_db_list(baseFilterENT)
        return self.__decode_list(db_list=db_list, info_size=self.FULL_INFO_SIZE)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def save(self, model):
        model.save()

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def decode_db(self, db_model, model_ent):
        if db_model.transition is not None:
            model_ent.transition_id = db_model.transition_id

        if db_model.transitionHistory is not None:
            model_ent.transitionHistory_id = db_model.transitionHistory_id

        model_ent.datetime_created = db_model.datetime_created
        model_ent.datetime_updated = db_model.datetime_updated
        return model_ent

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __create_update_base_db(self, entity, requestInfo=None, make_model_func=None):
        if entity.id is not None and entity.id != 0:
            db_model = self.__make_model_update(entity=entity, requestInfo=requestInfo, make_model_func=make_model_func)
        else:
            db_model = self.__make_model_create(entity=entity, requestInfo=requestInfo, make_model_func=make_model_func)
        self.save(db_model)
        return db_model

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __create_model_from_entity(self, entity, db_model, make_model_func):
        if make_model_func is not None:
            db_model = make_model_func(entity, db_model)
        else:
            db_model = self._mapdb.make_model(entity, db_model)
        return db_model

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __make_model_update(self, entity, requestInfo=None, make_model_func=None):
        db_model = self.__get_db_by_id(id=entity.id)
        db_model = self.__create_model_from_entity(entity=entity, db_model=db_model, make_model_func=make_model_func)
        if requestInfo is not None:
            db_model.user_updated_id = requestInfo.logged_user_id
            db_model.datetime_updated = requestInfo.requested_datetime
            db_model.ip_updated = requestInfo.requested_ip
        return db_model

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __make_model_create(self, entity, requestInfo=None, make_model_func=None):
        db_model = self.__create_model_from_entity(entity=entity, db_model=None, make_model_func=make_model_func)
        if requestInfo is not None:
            db_model.user_created_id = requestInfo.logged_user_id
            db_model.datetime_created = requestInfo.requested_datetime
            db_model.ip_created = requestInfo.requested_ip
        return db_model

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __decode_db(self, db_model, decode_db=None, entity=None):
        if decode_db is None:
            return self._mapdb.decode_db(db_model, entity)
        else:
            return decode_db(db_model, entity)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def create_update_base(self, entity, requestInfo=None, make_model_func=None, decode_db=None):
        db_model = self.__create_update_base_db(entity, requestInfo, make_model_func)
        return self.__decode_db(db_model=db_model, decode_db=decode_db, entity=entity)

        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def bulk_create_base(self, entities, requestInfo=None, make_model_func=None, decode_db=None):
        list_db_model = []
        for entity in entities:
            list_db_model.append(
                self.__make_model_create(entity=entity, requestInfo=requestInfo, make_model_func=make_model_func))
        saved_db_models = self._model.objects.bulk_create(list_db_model)
        i = 0
        for db_model in saved_db_models:
            self.__decode_db(db_model=db_model, decode_db=decode_db, entity=entities[i])
            i = i + 1
        return entities

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def bulk_update(self, entities, columns_to_update, requestInfo=None, make_model_func=None):
        list_db_model = []
        for entity in entities:
            list_db_model.append(
                self.__make_model_update(entity=entity, requestInfo=requestInfo, make_model_func=make_model_func))
        if type(columns_to_update) is set:
            columns_to_update = list(columns_to_update)
        if columns_to_update.count('user_updated_id') == 0:
            columns_to_update.append('user_updated_id')
        if columns_to_update.count('datetime_updated') == 0:
            columns_to_update.append('datetime_updated')
        if columns_to_update.count('ip_updated') == 0:
            columns_to_update.append('ip_updated')
        self._model.objects.bulk_update(list_db_model, columns_to_update)
        return entities

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # def update(self, entity, make_model_func=None, requestInfo=None):
    #     if make_model_func is not None:
    #         db_model = make_model_func(entity)
    #     else:
    #         db_model = self._mapdb.make_model(entity)
    #     if requestInfo is not None:
    #         db_model.user_updated_id = requestInfo.logged_user_id
    #         db_model.datetime_updated = requestInfo.requested_datetime
    #         db_model.ip_updated = requestInfo.requested_ip
    #
    #     self.save(db_model)
    #     return self._mapdb.decode_db(db_model)
    #
    # # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # def create_update(self, entity):
    #     db_Model = self._mapdb.make_model(entity)
    #     self.save(db_Model)
    #     return self._mapdb.decode_db(db_Model)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def count(self, baseFilterENT, patternDB_dict=None):
        params = self.__convert_to_orm_params(baseFilterENT.filter_list, baseFilterENT)
        excluding = self.__convert_to_orm_params(baseFilterENT.exclude_list, baseFilterENT)
        annotate_dict_F = self.__handle_output_fields(
            baseFilterENT.output_fields,
            baseFilterENT.other_annotate_dict,
            patternDB_dict
        )
        return self.__count(params, excluding, annotate_dict_F)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def read_choices(self, choices):
        try:
            return [BaseENT(id=item[0], name=item[1]) for item in choices]
        except:
            raise InvalidEntityException(
                source='read_choices',
                code='choice name',
                message='This choice does not exist.')

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def read_specific_choice(self, choices, id):
        try:
            return choices[id - 1][1]
        except:
            raise InvalidEntityException(
                source='read_choice',
                code='choice name or id',
                message='This choice does not exist.')

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_id(self, id):
        return self.__get_by_id_withSize(id=id, mapdb_fuc=self._mapdb.decode_db)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_id_mediumInfo(self, id):
        return self.__get_by_id_withSize(id=id, mapdb_fuc=self._mapdb.decode_db_mediumInfo)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_id_fullInfo(self, id):
        return self.__get_by_id_withSize(id=id, mapdb_fuc=self._mapdb.decode_db_fullInfo)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_id_mapdb_fuc(self, id, mapdb_fuc):
        return self.__get_by_id_withSize(id=id, mapdb_fuc=mapdb_fuc)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_by_id_withSize(self, id, mapdb_fuc=None):
        db_Model = self.__get_db_by_id(id=id)
        return mapdb_fuc(db_Model)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_uuid(self, uuid):
        return self.__get_by_uuid_withSize(uuid=uuid, mapdb_fuc=self._mapdb.decode_db)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_uuid_mediumInfo(self, uuid):
        return self.__get_by_uuid_withSize(uuid=uuid, mapdb_fuc=self._mapdb.decode_db_mediumInfo)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_uuid_fullInfo(self, uuid):
        return self.__get_by_uuid_withSize(uuid=uuid, mapdb_fuc=self._mapdb.decode_db_fullInfo)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def get_by_uuid_mapdb_fuc(self, uuid, mapdb_fuc):
        return self.__get_by_uuid_withSize(uuid=uuid, mapdb_fuc=mapdb_fuc)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_by_uuid_withSize(self, uuid, mapdb_fuc=None):
        db_Model = self.__get_db_by_uuid(uuid=uuid)
        return mapdb_fuc(db_Model)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __decode_list(self, db_list, info_size):
        entities_list = []
        if info_size == self.SMALL_INFO_SIZE:
            entities_list = [self.mapdb.decode_db(q) for q in db_list]

        elif info_size == self.MEDIUM_INFO_SIZE:
            entities_list = [self.mapdb.decode_db_mediumInfo(q) for q in db_list]


        elif info_size == self.FULL_INFO_SIZE:
            entities_list = [self.mapdb.decode_db_fullInfo(q) for q in db_list]

        elif info_size == self.FOR_LIST:
            entities_list = [self.mapdb.decode_db_for_list(q) for q in db_list]
        return entities_list

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_column(self, column, baseFilter):
        if column in list(self.mapdb.patternDB_dict.keys()):
            return self.mapdb.patternDB_dict[column].db_column
        if column in baseFilter.other_annotate_dict:
            return column
        raise InvalidEntityException(message=f'{column} dose not exists in patternDB',
                                     source='patternDB',
                                     code='column name')

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __do_operator(self, filter):
        if isinstance(filter.value, list):
            filter.column = '%s__in' % filter.column
        elif filter.operator is not None:
            filter.column = '%s__%s' % (filter.column, filter.operator)
        elif isinstance(filter.value, str):
            filter.column = '%s__icontains' % filter.column
        return filter.column

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __convert_to_orm_params(self, filterList, baseFilter):
        params = {}
        if filterList is None:
            return params
        for filter in filterList:
            if filter.value is not None:
                column = self.__get_column(filter.column, baseFilter)
                value = self.__handle_value(filter)
                filter.column = column
                filter.value = value
                params[self.__do_operator(filter)] = value
        return params

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __handle_value(self, filter):
        return (
            [
                self.mapdb.patternDB_dict[filter.column].type_func(val)
                for val in filter.value
            ]
            if type(filter.value) == list
            else self.mapdb.patternDB_dict[filter.column].type_func(filter.value)
        )

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __count(self, params, excluding=None, annotate_dict_F=None, values=None):
        if excluding is None:
            excluding = {}
        if annotate_dict_F is None:
            annotate_dict_F = {}
        if values is None:
            self.count_of_record = self._model.objects.annotate(**annotate_dict_F).filter(**params).exclude(
                **excluding).distinct().count()
        else:
            self.count_of_record = self._model.objects.values(*values).annotate(**annotate_dict_F).filter(
                **params).exclude(
                **excluding).distinct().count()

        # self.count_of_record=2
        return self.count_of_record

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_page_size(self, baseFilterENT):
        return DataType.get_int(baseFilterENT.page_size)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_page(self, baseFilterENT, page_size):
        page = DataType.get_int(baseFilterENT.page)
        number_of_pages = self.__give_number_of_pages(page_size, self.count_of_record)
        if page not in range(1, number_of_pages + 1) and self.count_of_record > 0:
            raise InvalidEntityException(
                source='page',
                code='not_allowed',
                message='This page does not exist.'
            )
        return page

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_column_in_map(self, column, baseFilter):
        if column in list(self.mapdb.patternDB_dict.keys()):
            return self.mapdb.patternDB_dict[column].db_column
        # raise InvalidEntityException(message=f'{column} dose not exists in patternDB',
        #                              source='patternDB',
        #                              code='column name')

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_values_from_output_fields(self, baseFilterENT):
        values = []
        if len(baseFilterENT.output_fields) > 0:
            for item in baseFilterENT.output_fields:
                if item in baseFilterENT.other_annotate_dict:
                    continue
                column = self.__get_column_in_map(column=item, baseFilter=baseFilterENT)
                if column is not None:
                    values.append(column)
        return values

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_db_list(self, baseFilterENT, patternDB_dict=None, needPaging=False):
        results = self.__get_query_list(baseFilterENT, patternDB_dict, needPaging)
        if len(baseFilterENT.output_fields) > 0:
            return results.values(*baseFilterENT.output_fields)
        return results

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_query_list(self, baseFilterENT, patternDB_dict=None, needPaging=False):
        self.annotate_dict_F = self.__handle_output_fields(
            baseFilterENT.output_fields,
            baseFilterENT.other_annotate_dict,
            patternDB_dict
        )
        self.ordering = self.__handle_ordering(baseFilterENT.ordering, self.annotate_dict_F)
        self.params = self.__convert_to_orm_params(baseFilterENT.filter_list, baseFilterENT)
        self.excluding = self.__convert_to_orm_params(baseFilterENT.exclude_list, baseFilterENT)
        self.values = self.__get_values_from_output_fields(baseFilterENT)
        return self.__query_from_model_with_pagination(baseFilterENT) if needPaging else self.__query_from_model(
            baseFilterENT)

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __query_from_model_with_pagination(self, baseFilterENT):
        page_size = self.__get_page_size(baseFilterENT)
        page = self.__get_page(baseFilterENT, page_size)
        if baseFilterENT.need_values_group_by and len(self.values) > 0:
            self.__count(self.params, self.excluding, self.annotate_dict_F, self.values)
            return self._model.objects.values(*self.values).annotate(
                **self.annotate_dict_F
            ).filter(**self.params).exclude(**self.excluding).distinct().order_by(
                *self.ordering
            )[(page - 1) * page_size:page * page_size]
        self.__count(self.params, self.excluding, self.annotate_dict_F)
        return self._model.objects.annotate(
            **self.annotate_dict_F
        ).filter(**self.params).exclude(**self.excluding).distinct().order_by(
            *self.ordering
        )[(page - 1) * page_size:page * page_size]

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __query_from_model(self, baseFilterENT):
        if baseFilterENT.need_values_group_by and len(self.values) > 0:
            return self._model.objects.values(*self.values).annotate(**self.annotate_dict_F).filter(
                **self.params).exclude(
                **self.excluding) \
                .distinct().order_by(
                *self.ordering
            )
        return self._model.objects.annotate(**self.annotate_dict_F).filter(**self.params).exclude(
            **self.excluding) \
            .distinct().order_by(
            *self.ordering
        )

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __handle_ordering(self, ordering_list, annotate_dict_F=None):
        new_ordering_list = []
        for ordering in ordering_list:
            p_ordering = ordering
            sign = ''
            if ordering[0] == '-':
                p_ordering = ordering[1:]
                sign = '-'
            if p_ordering in self.mapdb.patternDB_dict.keys():
                new_ordering_list.append(sign + self.mapdb.patternDB_dict[p_ordering].db_column)
                continue
            if p_ordering in annotate_dict_F:
                new_ordering_list.append(sign + p_ordering)
        return new_ordering_list

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __handle_output_fields(self, output_fields, other_annotate_dict, patternDB_dict=None):
        annotate_dict_F = {}
        if patternDB_dict is None:
            patternDB_dict = {}
        # commented by Ali - 1401/06/30 ...
        # for column in output_fields:
        #     if column in patternDB_dict.keys():
        #         if column != patternDB_dict[column].db_column:
        #             annotate_dict_F[column] = F(patternDB_dict[column].db_column)
        #
        #     elif column in self.mapdb.patternDB_dict.keys():
        #         if column != self.mapdb.patternDB_dict[column].db_column:
        #             annotate_dict_F[column] = F(self.mapdb.patternDB_dict[column].db_column)
        # ...

        # Added by Ali - 1401/06/30 ...
        for column in output_fields:
            if column in patternDB_dict.keys():
                db_column = patternDB_dict[column].db_column
                if column != db_column:
                    annotate_dict_F[column] = F(db_column)

            elif column in self.mapdb.patternDB_dict.keys():
                db_column = self.mapdb.patternDB_dict[column].db_column
                if column != db_column:
                    if isinstance(db_column, str):
                        annotate_dict_F[column] = F(db_column)
                    if isinstance(db_column, Case):
                        annotate_dict_F[column] = db_column
        # ...

        if other_annotate_dict is not None:
            annotate_dict_F.update(other_annotate_dict)
        return annotate_dict_F

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __give_number_of_pages(self, page_size, count):
        number_of_pages = count // page_size
        if count % page_size != 0:
            number_of_pages = number_of_pages + 1
        return number_of_pages

    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    def __get_db_list_with_pagination(self, baseFilterENT, patternDB_dict=None):
        return self.__get_db_list(baseFilterENT, patternDB_dict=patternDB_dict, needPaging=True)

    def __base_get_object(self, last=True, **kwargs) -> Optional[Model]:
        """
        kwargs: -> keys: field_name, values: field_value
        return: django model object or None if the request has a problem receiving data from the database.
        """
        if last:
            rslt = self.model.objects.filter(**kwargs).last()
        else:
            rslt = self.model.objects.filter(**kwargs).first()
        return rslt

    def __base_get_full_object(self, last=True, **kwargs) -> Optional[Model]:
        """
        kwargs: -> keys: field_name, values: field_value
        return: django model object or None if the request has a problem receiving data from the database.
        """
        if last:
            rslt = self.model.objects.filter(**kwargs).last().to_dict(kwargs.get('depth'))
        else:
            rslt = self.model.objects.filter(**kwargs).first().to_dict(kwargs.get('depth'))
        return rslt

    def base_create_or_update_schema_to_model(self, input_data_schema):
        """
        input_data_schema: pydantic.BaseModel instance
        return: pydantic.BaseModel instance
        """

        input_data = input_data_schema.dict_not_null()
        obj = self.model(**input_data)
        self.save(obj)
        input_data_schema = input_data_schema.update(orm_instance=obj)
        return input_data_schema

    def base_update_schema_to_model(self, lookup: dict, input_data_schema, output_schema_class=None):
        """
        input_data_schema: pydantic.BaseModel instance
        return: pydantic.BaseModel instance
        """
        inst = self.base_get_object(**lookup)
        if inst is None:
            return None
        rslt = self.base_save_schema(input_data_schema, output_schema_class=output_schema_class, pk=inst.pk,
                                     uuid=inst.uuid, id=inst.id)
        return rslt

    def base_bulk_create_schema_to_model(self, input_data_schemas):
        """
        input_data_schema: list[pydantic.BaseModel instance]
        return: list[pydantic.BaseModel instance]
        """

        input_data = [s.dict_not_null() for s in input_data_schemas]
        objs = [self.model(**i) for i in input_data]
        self.model.objects.bulk_create(objs)
        input_data_schemas = [s.update(orm_instance=o) for s, o in zip(input_data_schemas, objs)]
        return input_data_schemas

    def base_get_or_create_schema_to_model(self, input_data_schema, lookup_fields: dict = None):
        """
        input_data_schema: pydantic.BaseModel instance
        lookup_fields: -> key: model field name , value: model field name value for get data
        return: pydantic.BaseModel instance
        """

        if not lookup_fields:
            lookup_fields = input_data_schema.dict()
        obj = self.__base_get_object(**lookup_fields)
        if obj:
            rslt = input_data_schema.update(orm_instance=obj)
        else:
            rslt = self.base_create_or_update_schema_to_model(input_data_schema)
        return rslt

    def base_count(self, **kwargs) -> int:
        """
        params: dict, A dictionary of the names and values of the fields to be included in the query.
        excluding:dict, A dictionary of the names and values of the fields that are not to be seen in the query.
        annotate_dict_F:
        values:
        return: The number of records returned in the query.
        """
        params: dict = kwargs.get('params')
        excluding: dict = kwargs.get('excluding')
        annotate_dict_F: dict = kwargs.get('annotate_dict_F')
        values: list = kwargs.get('values')
        return self.__count(params=params, excluding=excluding, annotate_dict_F=annotate_dict_F, values=values)

    def base_get_object(self, **kwargs):
        return self.__base_get_object(**kwargs)

    def base_get_Schema(self, input_data_schema, output_schema_class=None, last=True):
        """
            get the object base on the output schema but just one layer
        """
        lookup_fields = input_data_schema.dict()
        obj = self.__base_get_object(last=last, **lookup_fields)
        ret = input_data_schema
        if obj:
            if output_schema_class:
                ret = output_schema_class()
            ret = ret.update(orm_instance=obj)
        else:
            ret = None
        return ret

    def base_get_full_schema(self, input_data_schema, output_schema_class, last=True, depth=1):
        """
            get object base on the output schema but as many layer as the depth value
        """
        lookup_fields = input_data_schema.dict()
        obj = self.__base_get_object(last=last, **lookup_fields)
        if obj:
            ret = output_schema_class(**(obj.to_dict(depth)))
        else:
            ret = None
        return ret

    def base_get_full_schema_v2(self, lookup_fields, output_schema_class, last=True, depth=1):
        """
            get object base on the output schema but as many layer as the depth value
        """
        # lookup_fields = input_data_schema.dict()
        obj = self.__base_get_object(last=last, **lookup_fields)
        if obj:
            ret = output_schema_class(**(obj.to_dict(depth)))
        else:
            ret = None
        return ret

    def base_save_schema(self, schema, output_schema_class=None, **kwargs):
        """
            Save a django orm object base on schema
            input  object
            output  object
        """
        input_data = schema.dict_not_null()
        input_data.update(kwargs)
        obj = self.model(**input_data)
        self.save(obj)
        if output_schema_class:
            schema = output_schema_class(**obj.__dict__)
        else:
            schema = schema.update(orm_instance=obj)
        return schema
