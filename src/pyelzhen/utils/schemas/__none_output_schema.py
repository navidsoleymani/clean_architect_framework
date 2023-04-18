from pydantic import BaseModel


class NoneOutputSchema(BaseModel):
    id: int
    pk: int
