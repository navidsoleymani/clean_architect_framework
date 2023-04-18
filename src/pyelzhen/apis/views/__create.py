from rest_framework.status import HTTP_201_CREATED

from . import BaseAPIView as Base


class Create(Base):
    def __init__(self, interactor, **kwargs):
        kwargs['expected_status_code'] = kwargs.get('expected_status_code') or HTTP_201_CREATED
        super().__init__(interactor=interactor, **kwargs)
