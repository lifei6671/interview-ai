from pydantic import BaseModel
from typing import Any,Optional

class ResponseModel(BaseModel):
    status:int = 0
    errmsg : Optional[str] = ""
    data: Optional[Any] = None
