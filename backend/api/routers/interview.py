import json
from fastapi import APIRouter
from sse_starlette import EventSourceResponse

from api.schemas.interview import JDRequest, GenerateResponse
from pipelines.pipeline import generate_interview

router = APIRouter(prefix="/interview", tags=["interview"])


@router.post("/generate", response_model=GenerateResponse)
async def generate(jd_req: JDRequest) -> GenerateResponse:
    """
    普通 JSON 接口，一次性返回所有结果。
    """
    result = generate_interview(jd_req.jd)
    return GenerateResponse(**result)


@router.post("/generate_stream")
async def generate_stream(jd_req: JDRequest):
    """
    SSE 流式接口：按事件推送 skill_tree 和 questions。
    """

    async def event_generator():
        # 状态事件
        yield {"event": "status", "data": "processing"}

        result = generate_interview(jd_req.jd)

        # 先推技能树
        yield {
            "event": "skill_tree",
            "data": json.dumps(result["skill_tree"], ensure_ascii=False),
        }

        # 再逐题推送
        for q in result["questions"].get("questions", []):
            yield {
                "event": "question",
                "data": json.dumps(q, ensure_ascii=False),
            }

        # 结束事件
        yield {"event": "done", "data": "ok"}

    return EventSourceResponse(event_generator())
