from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import and_

from models import SkillNode, User


class SkillNodeService:

    @staticmethod
    def get_skill_tree(db:Session):
        return db.query(SkillNode).order_by(SkillNode.level,SkillNode.sort_order).all()

    @staticmethod
    def create_skill_tree(
            db:Session,
            user:User|None,
            parent_id:int,
            name:str,
            level:int,
            sort_order:int,
            tags: list[str],
            auto_generated:bool = False
    ):
        """
        创建一个技能树节点
        :param db:
        :param user:
        :param parent_id:
        :param name:
        :param level:
        :param sort_order:
        :param tags:
        :param auto_generated:
        :return:
        """
        row = db.query(SkillNode).filter(
            and_(
                SkillNode.parent_id == parent_id,
                SkillNode.name == name,
                SkillNode.level == level,
            )
        ).first()
        if row :
            raise Exception(f"SkillNode with id {parent_id} and name {name} already exists")

        skill_node = SkillNode(
            parent_id=parent_id,
            name=name,
            level=level,
            sort_order=sort_order,
            tags=tags,
            auto_generated=auto_generated,
            created_by= user.email if user is not None else "AI",
        )
        db.add(skill_node)
        db.commit()
        db.refresh(skill_node)
        return skill_node