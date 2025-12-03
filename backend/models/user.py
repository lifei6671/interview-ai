from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(50),nullable=False)
    email = Column(String(255), unique=True,nullable=False,index=True)
    password_hash = Column(String,nullable=False)
    is_active = Column(Boolean,default=True,nullable=False)
    role = Column(String(50),nullable=False,default='admin',comment='用户角色：admin/user')
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)