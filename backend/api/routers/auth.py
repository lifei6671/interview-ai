from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from api.schemas.auth import RegisterRequest,LoginRequest,TokenResponse
from api.schemas.common import ResponseModel
from core.response import success
from services.user_service import UserService
from core.db import get_db

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",response_model=ResponseModel)
def register(req : RegisterRequest,db: Session = Depends(get_db)):
     user = UserService.register_user(db,str(req.email),req.password,req.nickname)

     return success({"id":user.id,"email":user.email,"nickname":user.nickname})

@router.post("/login",response_model=ResponseModel)
def login(req : LoginRequest,db: Session = Depends(get_db)):
    user = UserService.authenticate(db,req.email,req.password)
    if not user:
        raise HTTPException(status_code=401,detail="Incorrect email or password")

    token = UserService.create_login_token(user)
    return success(TokenResponse(access_token=token,token_type="Bearer"))

