from pydantic import BaseModel

from . import BaseRepository as Base


class Create(Base):

    def run(self, output_schema_class: BaseModel, data: BaseModel, depth=1) -> BaseModel:
        return self.creator(output_schema_class=output_schema_class, data=data, depth=depth)
