from datetime import datetime

from pydantic import BaseModel, field_validator


class RoleProfileCreateRequest(BaseModel):
    role_name: str
    description: str

    @field_validator('role_name')
    def validate_role_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Role name cannot be empty')
        return v


class RoleProfileResponse(BaseModel):
    id : int
    role_name : str
    description : str
    created_at : datetime
    created_by:str
    updated_at : datetime
    updated_by : str

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S'),
        }

class RoleProfileDeleteRequest(BaseModel):
    id: int

    @field_validator('id')
    def validate_id(cls, v):
        if not v or v <= 0:
            raise ValueError('Role ID cannot be negative')
        return v

class RoleProfileUpdateRequest(BaseModel):
    id : int
    role_name : str
    description : str

    @field_validator('id')
    def validate_id(cls, v):
        if not v or v <= 0:
            raise ValueError('Role ID cannot be empty')
        return v
    @field_validator('role_name')
    def validate_role_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Role name cannot be empty')
        return v
    @field_validator('description')
    def validate_description(cls, v):
        if not v or not v.strip():
            raise ValueError('Role description cannot be empty')
        return v