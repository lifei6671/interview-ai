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