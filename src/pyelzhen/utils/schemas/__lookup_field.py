from typing import Any, Optional

from pydantic import BaseModel


class LookupFieldSchema(BaseModel):
    key: Optional[str]
    value: Any
