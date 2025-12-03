from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    category:str
    skill : str
    strategy:str
    level:str
    question : str
    tags: List[str]