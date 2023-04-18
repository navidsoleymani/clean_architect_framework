from typing import List, Tuple, Optional

from pydantic import BaseModel
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from . import CookieSchema


class ResponseSchema(BaseModel):
    def __init__(self, **kwargs):
        kwargs['cookies'] = kwargs.get('cookies') or []
        kwargs['content_type'] = kwargs.get('content_type') or 'application/json'
        kwargs['headers'] = kwargs.get('headers') or []
        kwargs['files'] = kwargs.get('files') or []
        super().__init__(**kwargs)

    content: Optional[dict]
    status_code: int = HTTP_200_OK
    cookies: Optional[List[CookieSchema]] = []
    content_type: str = 'application/json'
    headers: Optional[List[Tuple]] = []
    files: Optional[List] = []

    def fire(self):
        rsp = Response(data=self.content, status=self.status_code, content_type=self.content_type, headers=self.headers)
        for c in self.cookies:
            rsp.set_cookie(**c.dict())
        return rsp
