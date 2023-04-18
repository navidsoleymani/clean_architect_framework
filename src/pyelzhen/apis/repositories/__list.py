from pydantic import BaseModel

from . import BaseRepository as Base


class List(Base):
    def run(self, output_schema_class: BaseModel, query_params, depth=1) -> BaseModel:
        return self.lister(output_schema_class=output_schema_class, query_params=query_params, depth=depth)
