from sqlalchemy import Column,Integer,String,Float,Text,DateTime,func

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ModelConfig(Base):
    __tablename__ = 'model_config'

    id = Column(Integer,primary_key=True,index=True,autoincrement=True,comment="主键")
    provider = Column(String(50),nullable=False,comment="模型提供商名称")
    api_key = Column(Text,nullable=False,comment="秘钥")
    base_url = Column(Text,nullable=False,comment="请求接口地址")
    model_name = Column(String(100),nullable=False,comment="模型名称")
    temperature = Column(Float,nullable=False,default=0.4,comment="温度")
    timeout = Column(Integer,nullable=False,default=60,comment="超时时间")
    updated_at = Column(DateTime,nullable=False,server_default=func.now(),onupdate=func.now())
    updated_user = Column(Text,nullable=False,default="",comment="最后更新人")
    create_at = Column(DateTime,nullable=False,server_default=func.now(),comment="创建时间")
    create_user = Column(Text,nullable=False,default="")
