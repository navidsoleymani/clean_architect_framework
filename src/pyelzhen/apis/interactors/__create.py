from . import BaseInteractor as Base


class Create(Base):
    def execute(self):
        ret = super().execute(data=self.data)
        return ret
