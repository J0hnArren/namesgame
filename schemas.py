from pydantic import BaseModel


class NewName(BaseModel):
    id: str
    # SberID: str
    name: str


class UsedNames(BaseModel):
    name_id: str
