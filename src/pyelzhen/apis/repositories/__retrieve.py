from pydantic import BaseModel
from typing import Optional

from pyelzhen.utils.schemas import LookupFieldSchema

from . import BaseRepository as Base
from .__macro import FIRST


class Retrieve(Base):
    def run(self, output_schema_class: BaseModel, lookup_field: LookupFieldSchema, last_or_first: str = FIRST,
            depth=1) -> Optional[BaseModel]:
        return self.retriever(output_schema_class=output_schema_class, lookup_field=lookup_field,
                              last_or_first=last_or_first, depth=depth)
