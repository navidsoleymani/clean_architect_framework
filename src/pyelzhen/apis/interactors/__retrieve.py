from pyelzhen.utils.schemas import LookupFieldSchema

from . import BaseInteractor as Base


class Retrieve(Base):
    lookup_field: LookupFieldSchema = None

    def set_params(self, *args, **kwargs):
        super().set_params(*args, **kwargs)
        self.lookup_field = kwargs.get('lookup_field') or self.request.lookupField
        return self

    def execute(self):
        ret = super().execute(lookup_field=self.lookup_field)
        return ret
