from typing import Optional, List

from pyelzhen.__configuration import pagination_base_settings as pg
from pydantic import BaseModel as BModel


class OutputListSchema(BModel):
    def __init__(self, **kwargs):
        kwargs['results'] = kwargs.get('results') or []
        kwargs['count'] = kwargs.get('count') or 0
        kwargs['page_size'] = kwargs.get('page_size') or pg.PAGE_SIZE_DEFAULT
        kwargs['page'] = kwargs.get('page') or pg.PAGE_NUMBER_DEFAULT
        kwargs['next'] = kwargs.get('next')
        kwargs['previous'] = kwargs.get('previous')
        super().__init__(**kwargs)

    results: List
    count: int
    page_size: int
    page: int
    next: Optional[str]
    previous: Optional[str]
