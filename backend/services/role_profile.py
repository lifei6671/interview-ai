from typing import List

from sqlalchemy.orm import Session,Query

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
            raise Exception(f"Role with name {role_name} already exists")

        role_profile = RoleProfile(
            role_name = role_name,
            description= description or '',
            created_by=user.email if user is not None else '',
        )

        db.add(role_profile)
        db.commit()
        db.refresh(role_profile)
        return role_profile
