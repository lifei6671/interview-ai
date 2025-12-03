from typing import List,Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session,Query

from core.exceptions import ResourceNotFoundError, ResourceDuplicateError
from models import User, RoleProfile


class RoleProfileService:
    @staticmethod
    def get_by_id(db:Session, role_id: int) -> RoleProfile | None:
        query : Query[RoleProfile] = db.query(RoleProfile)
        return query.filter(RoleProfile.id == role_id).first()

    @staticmethod
    def list(db:Session, skip: int = 0, limit: int = 100) -> List[RoleProfile]:
        return (db.query(RoleProfile).
                order_by(RoleProfile.created_at.desc()).
                offset(skip).
                limit(limit).
                all())

    @staticmethod
    def create(db:Session, user: User,role_name:str,description :str):
        """
        创建一个岗位画像
        :param db:
        :param user:
        :param role_name: 画像名称
        :param description: 画像描述
        :return:
        """
        row = db.query(RoleProfile).filter(RoleProfile.role_name == role_name).one_or_none()
        if row:
            raise ResourceDuplicateError(f"角色名称 [{role_name}] 已被使用")

        role_profile = RoleProfile(
            role_name = role_name,
            description= description or '',
            created_by=user.email if user is not None else '',
        )

        db.add(role_profile)
        db.commit()
        db.refresh(role_profile)
        return role_profile

    @staticmethod
    def delete_by_id(db:Session, user :User,role_id: int):
        """
        删除一个岗位画像
        :param db:
        :param user:
        :param role_id:
        :return:
        """
        db.query(RoleProfile).filter(RoleProfile.id == role_id).delete()
        db.commit()
        return True

    @staticmethod
    def update_by_id(
            db:Session,
            user :User,
            role_id: int,
            role_name: str,
            description :str | None
    )-> RoleProfile:
        """
        根据id更新一个岗位画像
        :param db: 数据库会话
        :param user: 操作人（可用于日志/审计）
        :param role_id: 岗位ID（必传）
        :param role_name: 新岗位名称（必传，非空）
        :param description: 新描述（可选）
        :return: 更新后的 RoleProfile 实例
        :raises ResourceNotFoundError: 岗位ID不存在
        :raises DuplicateNameError: 岗位名称已被占用
        :raises ValueError: 岗位名称为空
        """

        role_profile : Optional[RoleProfile] = db.query(RoleProfile).filter(RoleProfile.id == role_id).one_or_none()
        if not role_profile:
            raise ResourceNotFoundError(f"Role with id {role_id} does not exist")

        # 查询角色名是否被占用
        exist : Optional[RoleProfile]  = db.query(RoleProfile).filter(
            and_(
                RoleProfile.id != role_id,
                RoleProfile.role_name == role_name.strip()
            )
        ).one_or_none()
        if exist:
            raise DuplicateNameError(f"角色名称 [{role_name}] 已被使用")

        role_profile.role_name = role_name.strip()
        role_profile.description = description or ''
        role_profile.updated_by = user.email if user is not None else None

        db.commit()
        db.refresh(role_profile)
        return role_profile