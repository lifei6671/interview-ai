from datetime import datetime,timedelta

from jose import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    对密码进行hash加密
    :param password: 原文密码
    :return:
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    对比原文和密文密码是否一致
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)

def  create_access_token(data: dict,expires_delta: timedelta = timedelta(minutes=10)):
    """
    创建一个请求token
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    # 计算过期时间，如果没有传入则使用默认配置的时间
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)