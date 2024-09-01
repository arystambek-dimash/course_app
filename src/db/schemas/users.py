from typing import Optional

from pydantic import BaseModel, Field, validator
import re


class PasswordMixin(BaseModel):
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v


class _BaseUserSchema(BaseModel):
    profile_image: Optional[str] = Field(None)
    telephone_number: str = Field(..., alias="number")
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)

    @validator('telephone_number')
    def validate_phone_number(cls, v):
        pattern = r'^\+?1?\d{9,15}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid phone number format')
        return v

    class Config:
        from_attributes = True
        str_strip_whitespace = True
        populate_by_name = True


class UserBase(_BaseUserSchema):
    id: int = Field(..., alias="_id")
    role: str = Field(..., alias="role")


class UserBaseWithPassword(UserBase):
    password: str


class UserInLogin(BaseModel):
    telephone_number: str
    password: str


class UserInRegister(_BaseUserSchema, PasswordMixin):
    role: str


class UserInUpdate(_BaseUserSchema):
    profile_image: Optional[str]
    telephone_number: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str] = Field(None, min_length=8)  # Optional

    @validator('password')
    def validate_optional_password(cls, v):
        if v is not None:
            return PasswordMixin.validate_password(v)
        return v


class UserResponse(BaseModel):
    user: UserBase
    token: str


class UserListResponse(BaseModel):
    users: list[UserBase]
    total: int
    page: int
    size: int
