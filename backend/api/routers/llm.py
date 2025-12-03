from sqlalchemy.orm import Session

from api.schemas.common import ResponseModel
from api.schemas.model import ModelRequest, ModelListRequest, ModelResponse
from core.auth import get_current_user
from core.db import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Query
from models.user import User
from core.response import success
from services.model_config_service import ModelConfigService

router = APIRouter(   prefix="/llm",    tags=["llm"],)

@router.post("/create", response_model=ResponseModel)
def create_model(
        req :ModelRequest,
        db :Session = Depends(get_db),
        user:User = Depends(get_current_user)
):
    model_info = ModelConfigService.create(
        db,
        req.provider,
        req.model_name,
        req.api_key,
        req.base_url,
        timeout=req.timeout,
        temperature=req.temperature,
        user = user,
    )
    return success({"id": model_info.id,"provider":model_info.provider,"model_name":model_info.model_name})


@router.get("/list", response_model=ResponseModel)
def list_model(
        provider :str = Query(None),
        model_name :str = Query(None),
        db:Session = Depends(get_db), user:User = Depends(get_current_user)):
    model_list = ModelConfigService.list(
        db,
        provider,
        model_name,
    )

    return success({"list":[ModelResponse.model_validate(c) for c in model_list]})