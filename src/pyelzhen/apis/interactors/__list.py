from pyelzhen.utils.schemas import QueryParamsSchema

from . import BaseInteractor as Base


class List(Base):
    query_params: QueryParamsSchema

    def set_params(self, *args, **kwargs):
        super().set_params(*args, **kwargs)
        self.query_params = kwargs.get('query_params') or self.request.queryParams
        return self

    def execute(self):
        ret = super().execute(query_params=self.query_params)
        return ret
