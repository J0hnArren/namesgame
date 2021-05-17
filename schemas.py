from pydantic import BaseModel


class AddUserData(BaseModel):
    UserId: str
    UserName: str
    Name: str


class AddNickname(BaseModel):
    UserId: str
    Nickname: str


class GetId(BaseModel):
    Id: str