"""
Refactor By: Hydra
Date: 15 Nov 2022
"""
from pydantic import BaseModel as BModel
from typing import List, Optional
from . import PaginationSchema


class QueryParams(BModel):
    search: Optional[str] = None
    output_fields: Optional[List[str]] = None
    ordering: Optional[List[str]] = None
    pagination: PaginationSchema = PaginationSchema()
    filters: Optional[List[str]] = None
