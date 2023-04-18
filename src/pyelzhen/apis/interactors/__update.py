from pyelzhen.utils.schemas import LookupFieldSchema

from . import BaseInteractor as Base


class Update(Base):
    lookup_field: LookupFieldSchema = None
    update_fields: set = None

    def set_params(self, *args, **kwargs):
        super().set_params(*args, **kwargs)
        self.lookup_field = kwargs.get('lookup_field') or self.request.lookupField
        self.update_fields = kwargs.get('update_fields') or self.request.inputFieldNameList
        return self

    def execute(self):
        ret = super().execute(
            lookup_field=self.lookup_field, data=self.data, update_fields=self.update_fields)
        return ret
