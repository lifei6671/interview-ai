from typing import Dict, Any
from .skill_extract import build_skill_extract_chain
from .skill_to_questions import build_skill_to_questions_chain


def generate_interview(jd_text: str) -> Dict[str, Any]:
    """
    总流水线：JD → SkillTree → Questions
    返回结构：
    {
      "skill_tree": {...},
      "questions": {...}
    }
    """
    skill_chain = build_skill_extract_chain()
    skill_tree = skill_chain.invoke({"jd_text": jd_text})

    question_chain = build_skill_to_questions_chain()
    questions = question_chain.invoke({"skill_tree": skill_tree})

    return {
        "skill_tree": skill_tree,
        "questions": questions,
    }
