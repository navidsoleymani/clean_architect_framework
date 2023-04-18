from typing import Set, Optional

from pydantic import BaseModel


class ControllerParamsSchema(BaseModel):
    inputFieldNames: Optional[Set[str]]
    outputFieldNames: Optional[Set[str]]
