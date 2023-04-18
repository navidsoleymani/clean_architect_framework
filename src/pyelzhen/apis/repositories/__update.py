from pydantic import BaseModel
from typing import Optional

from pyelzhen.utils.schemas import LookupFieldSchema
from pyelzhen.__definitions import ALL

from . import BaseRepository as Base


class Update(Base):
    def run(self, output_schema_class: BaseModel, lookup_field: LookupFieldSchema,
            data: BaseModel, update_fields: set = ALL, depth=1) -> Optional[BaseModel]:
        return self.updater(output_schema_class=output_schema_class, lookup_field=lookup_field, data=data,
                            update_fields=update_fields, depth=depth)
