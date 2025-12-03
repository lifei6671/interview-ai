from datetime import datetime

from pydantic import BaseModel, field_validator


class SkillTreeCreateRequest(BaseModel):
    parent_id: int = 0
    name: str
    description: str = ''
    level: int = 1
    sort_order: int = 1
    tags: list[str] = []

    @field_validator("name")
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v


class SkillTreeResponse(BaseModel):
    id: int
    parent_id: int
    name: str
    description: str
    level: int
    sort_order: int
    tags: list[str]
    auto_generated:bool
    created_on: datetime
    created_by: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S'),
        }