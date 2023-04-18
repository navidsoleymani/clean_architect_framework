from typing import Any

from pydantic import BaseModel


class FakerDependencySchema(BaseModel):
    def __init__(self, **kwargs):
        engine = kwargs['engine']
        kwargs['alias'] = kwargs.pop('alias', None) or engine.alias
        super().__init__(**kwargs)

    engine: Any
    alias: str
    priority: int = 1
