from sqlalchemy.orm import Session

from core.security import hash_password, verify_password, create_access_token
from models.user import User
from core.logger import logger


class UserService:
    """
    用户相关处理方法
    """
    @staticmethod
    def register_user(db :Session,email:str,password:str,nickname:str|None):
        """
        注册新用户
        :param db: 数据驱动
        :param email: 邮箱
        :param password:原始密码
        :param nickname: 昵称
        :return: 用户信息
        """
        # 先查询用户的邮箱是否存在
        exists = db.query(User).filter(User.email==email).first()
        if exists:
            logger.error("user email is exist:email={}".format(email))
            raise Exception("Email already registered")

        user = User(
            email = email,
            password_hash=hash_password(password),
            nickname =nickname or "",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db :Session,email:str,password:str):
        """
        用户登录验证
        :param db:
        :param email:
        :param password:
        :return:
        """
        user = db.query(User).filter(User.email==email).first()
        if not user:
            logger.error("user authenticate fail,user does not exist:email={}".format(email))
            return None
        if not verify_password(password, str(user.password_hash)):
            logger.error("user authenticate fail,password is error:email={}".format(email))
            return None
        return user

    @staticmethod
    def create_login_token(user :User):
        return create_access_token({"sub": str(user.id),"email":user.email})

    @staticmethod
    def get_user_by_id(db:Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        return user