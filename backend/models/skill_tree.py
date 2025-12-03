# models/skill_tree.py
from __future__ import annotations

from typing import List, Optional

from sqlalchemy import (
    Integer,
    String,
    Text,
    Boolean,
    TIMESTAMP,
    func,
    ForeignKey,
    Numeric,
    UniqueConstraint,
    Index, Column, DateTime,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class SkillNode(Base):
    """
    技能树节点：纯知识结构，不绑定难度 / 权重
    """
    __tablename__ = "skill_node"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("skill_node.id", ondelete="CASCADE"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=False,default='')

    # 1 = 领域, 2 = 大类, 3 = 技能点, 4 = 知识点
    level: Mapped[int] = mapped_column(Integer, nullable=False)

    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # PostgreSQL TEXT[]
    tags: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        nullable=True,
    )

    auto_generated: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_by: Mapped[str] = mapped_column(String, nullable=False)
    updated_by: Mapped[Optional[str]] = mapped_column(String, nullable=False,default='')

    created_at: Mapped[Optional[str]] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[Optional[str]] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # 自关联关系：父节点 / 子节点
    parent: Mapped[Optional["SkillNode"]] = relationship(
        "SkillNode",
        remote_side=[id],
        back_populates="children",
    )
    children: Mapped[List["SkillNode"]] = relationship(
        "SkillNode",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    # 与 RoleSkill / CandidateSkill 反向关系
    role_skills: Mapped[List["RoleSkill"]] = relationship(
        "RoleSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )

    candidate_skills: Mapped[List["CandidateSkill"]] = relationship(
        "CandidateSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("idx_skill_node_parent", "parent_id"),
        Index("idx_skill_node_level", "level"),
        Index("idx_skill_node_tags", "tags", postgresql_using="gin"),
    )


class RoleProfile(Base):
    """
    岗位画像，例如：
    - Golang 初级工程师
    - Golang 高级工程师
    - 资深架构师
    """
    __tablename__ = "role_profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    role_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False,default='')

    created_by = Column(String, nullable=False,default='')
    updated_by  = Column(String, nullable=False,default='')

    created_at  = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # 一个岗位配置多个技能要求
    role_skills: Mapped[List["RoleSkill"]] = relationship(
        "RoleSkill",
        back_populates="role",
        cascade="all, delete-orphan",
    )


class RoleSkill(Base):
    """
    岗位对某个技能点的「难度 & 权重」定义
    注意：难度 / 权重 与岗位和候选人有关，不写在技能树上
    """
    __tablename__ = "role_skill"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("role_profile.id", ondelete="CASCADE"),
        nullable=False,
    )
    skill_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("skill_node.id", ondelete="CASCADE"),
        nullable=False,
    )

    difficulty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        doc="岗位要求的难度等级，1~5",
    )

    weight: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=1.0,
        doc="该技能在岗位中的权重，用于题目分布控制",
    )

    must_have: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at: Mapped[Optional[str]] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[Optional[str]] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # 关系：一个 RoleProfile 下有很多 RoleSkill；一个 SkillNode 也可能被多个岗位引用
    role: Mapped["RoleProfile"] = relationship(
        "RoleProfile",
        back_populates="role_skills",
    )
    skill: Mapped["SkillNode"] = relationship(
        "SkillNode",
        back_populates="role_skills",
    )

    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "skill_id",
            name="role_skill__role_id_skill_id",
        ),
    )


class CandidateProfile(Base):
    """
    候选人画像：与 user 绑定，用于记录候选人的基础信息/简历
    """
    __tablename__ = "candidate_profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    years_experience: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    level: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="候选人级别，如 P4/P5/Junior/Senior",
    )

    resume_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="原始简历文本，可用于 embedding / LLM 分析",
    )

    created_at: Mapped[Optional[str]] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[Optional[str]] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    candidate_skills: Mapped[List["CandidateSkill"]] = relationship(
        "CandidateSkill",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )


class CandidateSkill(Base):
    """
    候选人在某个技能点上的评估，用于：
    - 从简历 / LLM 抽取能力
    - 人工面试打分
    """
    __tablename__ = "candidate_skill"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    candidate_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("candidate_profile.id", ondelete="CASCADE"),
        nullable=False,
    )
    skill_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("skill_node.id", ondelete="CASCADE"),
        nullable=False,
    )

    confidence: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2),
        nullable=True,
        doc="模型对候选人在该技能上的置信度",
    )

    level_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        doc="技能掌握程度，1~5，可以是 LLM 评分或人工打分",
    )

    source: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="来源：resume / llm_extract / manual 等",
    )

    created_at: Mapped[Optional[str]] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    candidate: Mapped["CandidateProfile"] = relationship(
        "CandidateProfile",
        back_populates="candidate_skills",
    )
    skill: Mapped["SkillNode"] = relationship(
        "SkillNode",
        back_populates="candidate_skills",
    )

    __table_args__ = (
        UniqueConstraint(
            "candidate_id",
            "skill_id",
            name="candidate_skill__candidate_id_skill_id",
        ),
    )
