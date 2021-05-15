from pydantic import BaseModel


class NamesList(BaseModel):
    NameID: str
    # SberID: str
    Name: str
    Sex: str
    Rate: int


class UsedNames(BaseModel):
    NameID: str
