"""
Refactor By: Hydra
Date: 08 Nov 2022
"""
from pydantic import BaseModel as BModel
from elzhen_framework._elzhen_base_settings import pagination_base_settings as pgb_settings
from typing import Optional, List


class OutputList(BModel):
    results: List = list()
    count: int = 0
    page_size: int = pgb_settings.PAGE_SIZE_DEFAULT
    page: int = pgb_settings.PAGE_NUMBER_DEFAULT
    next: Optional[str] = None
    previous: Optional[str] = None
