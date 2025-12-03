from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.schemas.common import ResponseModel
from api.schemas.role_profile import RoleProfileCreateRequest, RoleProfileResponse
from core.auth import get_current_user
from core.db import get_db
from core.response import success
from models import User, RoleProfile
from services.role_profile import RoleProfileService

router = APIRouter(prefix="/role_profile", tags=["Role Profile"])

@router.get("/list", response_model=ResponseModel)
async def get_list(db:Session = Depends(get_db),user:User = Depends(get_current_user)):
    role_profiles = RoleProfileService.list(db)

    return success([RoleProfileResponse(
        id=item.id,
        role_name=item.role_name,
        description=item.description or '',
        created_by=item.created_by,
        created_at=item.created_at,
        updated_at=item.updated_at,
        updated_by=item.updated_by,
    ) for item in role_profiles])


@router.post("/create", response_model=ResponseModel)
async def create_role_profile(
        param:RoleProfileCreateRequest,
        db:Session = Depends(get_db),
        user:User = Depends(get_current_user)
):
    role_profile = RoleProfileService.create(
        db=  db,
        user=user,
        role_name=param.role_name,
        description = param.description
    )
    return success({
        "id":role_profile.id,
        "name":role_profile.role_name,
        "description":role_profile.description,
    })