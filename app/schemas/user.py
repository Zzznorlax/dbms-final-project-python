
from pydantic import BaseModel, Field
from app.utils.enum import EnumBase


class UserType(EnumBase):
    buyer = "買家"
    seller = "賣家"


class TokenDTO(BaseModel):

    id: int = Field(
        ...,
    )

    token: str = Field(
        ...,
        description="JWT token"
    )


class UserLoginDTO(BaseModel):

    email: str = Field(
        ...,
        description="Login email"
    )

    password: str = Field(
        ...,
        description="User's password"
    )


class UserBaseDTO(BaseModel):

    name: str = Field(
        ...,
        description="User's name"
    )

    phone: str = Field(
        ...,
        description="User's phone"
    )


class UserCreateDTO(UserBaseDTO):

    email: str = Field(
        ...,
        description="User's email"
    )

    password: str = Field(
        ...,
        description="User's password"
    )

    kind: UserType = Field(
        ...,
        description="User's type",
        alias="type"
    )


class UserRespDTO(UserBaseDTO):

    id: int = Field(
        ...,
        description="User's DB ID"
    )

    kind: UserType = Field(
        ...,
        description="User's type",
        alias="type"
    )

    email: str = Field(
        ...,
        description="User's email"
    )
