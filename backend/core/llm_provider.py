from langchain_openai import ChatOpenAI
from services.model_config_service import ModelConfigService

def create_chat_model(temperature: float = 0.4) -> ChatOpenAI:
    """
    创建统一的 ChatOenAI 实例，提供各个 pipeline 调用。
    :param temperature:
    :return:
    """
    cfg = ModelConfigService.get_config()

    return ChatOpenAI(
        model=cfg.model,
        api_key=cfg.api_key,
        base_url=cfg.base_url,
        temperature= temperature or cfg.temperature,
        timeout=cfg.timeout,
    )