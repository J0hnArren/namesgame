from pydantic import BaseModel


class AddUserData(BaseModel):
    UserId: str
    Name: str


class ManageNickname(BaseModel):
    UserId: str
    Nickname: str


class GetId(BaseModel):
    Id: str
