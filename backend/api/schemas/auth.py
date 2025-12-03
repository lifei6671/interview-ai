from pydantic import BaseModel, field_validator, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str|None = None

    @field_validator('email')
    def validate_email(cls, v):
        if not v or not v.strip():
            raise ValueError('Email cannot be empty')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if not v or not v.strip():
            raise ValueError('Password cannot be empty')
        return v

class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator('email')
    def validate_email(cls, v):
        if not v or not v.strip():
            raise ValueError('Email cannot be empty')
        return v
    @field_validator('password')
    def validate_password(cls, v):
        if not v or not v.strip():
            raise ValueError('Password cannot be empty')
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

