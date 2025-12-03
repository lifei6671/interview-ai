from pydantic import BaseModel, field_validator


class ModelResponse(BaseModel):
    id : int
    provider : str
    api_key:str
    base_url:str
    model_name: str
    temperature: float
    timeout :int

    class Config:
        from_attributes = True

class ModelRequest(BaseModel):
    provider : str
    api_key: str
    base_url: str
    model_name: str
    temperature: float = 0.04
    timeout: int = 60

    @field_validator('provider')
    def validate_provider(cls, v):
        if not v or not v.strip():
            raise ValueError('Provider cannot be empty')
        return v
    @field_validator('api_key')
    def validate_api_key(cls, v):
        if not v or not v.strip():
            raise ValueError('API key cannot be empty')
        return v
    @field_validator('base_url')
    def validate_base_url(cls, v):
        if not v or not v.strip():
            raise ValueError('Base url cannot be empty')
        return v
    @field_validator('model_name')
    def validate_model_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Model cannot be empty')
        return v

class ModelListRequest(BaseModel):
    provider : str = None
    model_name: str = None