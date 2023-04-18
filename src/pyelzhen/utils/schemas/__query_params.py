from pydantic import BaseModel
from typing import Optional

from pyelzhen.__configuration import pagination_base_settings as pg

from . import PaginationSchema


class QueryParamsSchema(BaseModel):
    def __init__(self, **kwargs):
        kwargs['filters'] = kwargs.get('filters') or pg.FILTERS_DEFAULT
        kwargs['orderings'] = kwargs.get('orderings') or pg.ORDERINGS_DEFAULT
        kwargs['pagination'] = kwargs.get('pagination') or PaginationSchema()
        kwargs['base_url'] = kwargs.get('base_url') or ''
        kwargs['values'] = kwargs.get('values') or []
        kwargs['annotates'] = kwargs.get('annotates') or {}
        kwargs['excludes'] = kwargs.get('excludes') or {}
        super().__init__(**kwargs)

    search: Optional[str] = None
    filters: dict
    orderings: list
    pagination: PaginationSchema
    base_url: str
    values: list
    annotates: dict
    excludes: dict
