from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from core.llm_provider import create_chat_model

def build_skill_to_questions_chain():
    with open("prompts/question_generate.prompt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "user",
                """
以下是技能树 Skill Tree：

{skill_tree}

请基于技能树生成高质量的“反八股文”面试题。
""",
            ),
        ]
    )

    parser = JsonOutputParser()
    llm = create_chat_model(temperature=0.7)
    chain = prompt | llm | parser
    return chain
