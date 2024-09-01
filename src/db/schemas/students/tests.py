from pydantic import BaseModel


class _BaseTestSchema(BaseModel):
    name: str
