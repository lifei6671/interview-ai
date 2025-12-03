from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from core.config import settings
from core.db import get_db
from models.user import User
from services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),db :Session =Depends(get_db)) -> User:
    """
    解析 JWT 返回当前登录用户
    :param token:
    :param db:
    :return:
    """
    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=settings.algorithm)
        user_id_str: str = payload.get("sub") or ""
        if not user_id_str:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
        user_id :int = int(user_id_str)
    except (JWTError,ValueError,TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")

    user = UserService.get_user_by_id(db,user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User disabled")

    return user