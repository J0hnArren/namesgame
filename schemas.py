from pydantic import BaseModel


class AddUserData(BaseModel):
    UserId: str
    Name: str


class UsedNames(BaseModel):
    name_id: str
