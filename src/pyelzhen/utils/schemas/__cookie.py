from datetime import datetime

from pydantic import BaseModel


class CookieSchema(BaseModel):
    key: str
    value: str = ''
    max_age: int = None
    expires: datetime = None
    path: str = '/'
    domain: str = None
    secure: bool = False
    httponly: bool = False
    samesite: str = None
