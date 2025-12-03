from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from core.llm_provider import create_chat_model


def build_skill_extract_chain():
    with open("prompts/skill_extract.prompt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "user",
                """
以下是招聘 JD：

{jd_text}

请抽取对应的能力树 Skill Tree。
""",
            ),
        ]
    )

    parser = JsonOutputParser()
    llm = create_chat_model(temperature=0.3)
    chain = prompt | llm | parser
    return chain
