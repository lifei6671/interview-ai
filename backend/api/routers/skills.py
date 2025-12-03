from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

from api.schemas.common import ResponseModel
from api.schemas.skill_tree import SkillTreeCreateRequest, SkillTreeResponse
from core.auth import get_current_user
from core.db import get_db
from core.response import success
from models import SkillNode,User
from services import SkillNodeService

router = APIRouter(prefix="/skills", tags=["skills"])

@router.get("/tree",response_model=ResponseModel)
async def get_skill_tree(db:Session = Depends(get_db),user :User = Depends(get_current_user)):
    nodes = SkillNodeService.get_skill_tree(db)
    tree = build_antd_tree(nodes)
    return success(tree)

@router.post("/create",response_model=ResponseModel)
async def create_skill_tree(param:SkillTreeCreateRequest,db:Session = Depends(get_db),user :User = Depends(get_current_user)):

    skill_node = SkillNodeService.create_skill_tree(
        db=db,
        user=user,
        parent_id=param.parent_id,
        name=param.name,
        level=param.level,
        sort_order=param.sort_order,
        tags=param.tags,
        auto_generated=False,
    )
    return success(SkillTreeResponse(
        id=skill_node.id,
        parent_id=skill_node.parent_id,
        name=skill_node.name,
        description=skill_node.description,
        level=skill_node.level,
        sort_order=skill_node.sort_order,
        tags=skill_node.tags,
        auto_generated= skill_node.auto_generated,
        created_by=skill_node.created_by,
        created_on=skill_node.created_at,
    ))

def build_antd_tree(nodes: list[SkillNode]) -> list[dict]:
    """
    将技能树结构构造为UI层的树状数据结构
    :param nodes:
    :return:
    """
    children_map : dict[int,list[SkillNode]] = {node.id:[] for node in nodes}

    root_nodes = []

    for node in nodes:
        # 如果该节点存在父节点，则将当前节点追加到父节点的集合中
        if node.parent_id:
            children_map[node.parent_id].append(node)
        else:
            # 否则该节点即为父节点
            root_nodes.append(node)

    def build(node:SkillNode) -> dict:
        children = children_map[node.id]
        return {
            "key" : str(node.id),
            "name" : node.name,
            "children" : [build(c) for c in children], # 这里要递归的构建整棵树
        }
    # 从根节点开始，构建整棵树
    return [build(node) for node in root_nodes]