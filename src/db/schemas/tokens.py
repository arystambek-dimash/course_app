from datetime import datetime, timedelta

from pydantic import BaseModel, Field


class Payload(BaseModel):
    id: int = Field(..., alias="_id")
    exp: timedelta = Field(..., alias="exp")


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True
