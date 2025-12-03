from typing import List

from sqlalchemy import and_,desc
from sqlalchemy.orm import Session

from core.db import SessionLocal
from core.logger import logger
from models.model_config import ModelConfig as ModelConfigORM
from models.user import User


class ModelConfigService:
    """
    从数据库读取模型的配置文件
    """
    _cache = None
    _expire_ts = 0
    _ttl = 60

    @classmethod
    def get_config(cls) :
        import time
        now =time.time()
        ## 这里使用缓存
        if cls._cache and now < cls._expire_ts:
            return cls._cache

        db : Session = SessionLocal()
        # 从数据库读取一条模型的皮脂
        row = db.query(ModelConfigORM).order_by(ModelConfigORM.id.desc()).first()

        db.close()

        if not row:
            raise RuntimeError("model config not found")

        cls._cache = row
        cls._expire_ts = now + cls._ttl
        return row

    @classmethod
    def get(cls,model_id : int) :
        """
        使用主键查询一条模型配置
        :param model_id:
        :return:
        """
        db : Session = SessionLocal()
        row = db.query(ModelConfigORM).filter(ModelConfigORM.id == model_id).first()
        db.close()

        if not row:
            logger.error("model config not found: id={}".format(model_id))
            raise RuntimeError("model config not found: id={}".format(model_id))

        return row

    @staticmethod
    def get_by_provider_with_model_name(db :Session,provider:str,model_name:str) :
        """
        根据模型提供商和模型名称查询模型信息
        :param db:
        :param provider:
        :param model_name:
        :return:
        """
        row = (db.query(ModelConfigORM).
               filter(ModelConfigORM.provider == provider).
               filter(ModelConfigORM.model_name == model_name).
               first())
        db.close()
        if not row:
            logger.error("model config not found: provider={} model_name={}".format(provider,model_name))
        return row

    @staticmethod
    def create(
            db :Session,
            provider:str,
            model_name:str,
            api_key:str,
            base_url:str,
            timeout :int|None,
            temperature:float|None,
            user : User,
    ):
        """
        创建一个大模型配置
        :param db:
        :param provider:
        :param model_name:
        :param api_key:
        :param base_url:
        :param timeout:
        :param temperature:
        :param user:
        :return:
        """
        row = db.query(ModelConfigORM).filter(
            and_(
                ModelConfigORM.provider == provider,
                ModelConfigORM.model_name == model_name
            )
        ). one_or_none()
        if row:
            raise Exception("model already exists: provider={} model_name={}".format(provider,model_name))

        model_info = ModelConfigORM(
            provider=provider,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature or 0.04,
            timeout=timeout or 60,
            create_user=user.email,
        )
        db.add(model_info)
        db.commit()
        db.refresh(model_info)
        return model_info

    @staticmethod
    def list(db :Session,provider:str,model_name:str) -> List[ModelConfigORM]:
        """
        查询大模型列表
        :param db:
        :param provider:
        :param model_name:
        :return:
        """
        query = db.query(ModelConfigORM)

        if provider and provider.strip() != "":
            query .filter(ModelConfigORM.provider == provider.strip())

        if model_name and model_name.strip() != "":
            query .filter(ModelConfigORM.model_name == model_name.strip())

        result = query.order_by(desc(ModelConfigORM.id)).all()
        return result