from pydantic import BaseModel
from typing import Any, Dict


class JDRequest(BaseModel):
    jd: str


class GenerateResponse(BaseModel):
    skill_tree: Dict[str, Any]
    questions: Dict[str, Any]
