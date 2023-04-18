from pydantic import BaseModel as BModel
from pyelzhen.__configuration import pagination_base_settings as pg
from typing import Optional


class PaginationSchema(BModel):
    def __init__(self, **kwargs):
        kwargs['page_size'] = kwargs.get('page_size') or pg.PAGE_SIZE_DEFAULT
        kwargs['page'] = kwargs.get('page') or pg.PAGE_NUMBER_DEFAULT
        super().__init__(**kwargs)

    page_size: int
    page: int
    next: Optional[str] = None
    previous: Optional[str] = None
