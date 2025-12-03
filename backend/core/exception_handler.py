from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

from api.schemas.common import ResponseModel
from core.exceptions import BusinessException
from .logger import logger
from .config import settings

async def http_exception_handler(request: Request, exc: HTTPException) :
    return JSONResponse(
        status_code=200,
        content = ResponseModel(status=exc.status_code,errmsg=exc.detail).model_dump(),
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError)  :
    formatted = [
        {
            "loc": err.get("loc", []),
            "msg": err.get("msg", ""),
            "type": err.get("type", "")
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=200,
        content=ResponseModel( status=422, errmsg="参数校验错误",data=formatted).model_dump(),
    )

async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, BusinessException):
        return JSONResponse(
            status_code=200,
            content=ResponseModel(
                status=exc.status_code or 500,
                errmsg=exc.errmsg,
                data=None
            ).model_dump(),
        )

    logger.error(
        f"请求路径：{request.url.path} 发生异常",
        exc_info=True  # exc_info=True 会记录完整异常堆栈
    )
    if isinstance(exc, HTTPException ):
        return JSONResponse(
            status_code=exc.status_code,
            content=ResponseModel(
                status=exc.status_code,
                errmsg=exc.detail or "HTTP 请求异常",
                data=None
            ).model_dump()
        )

    if isinstance(exc, SQLAlchemyError):
        if settings.env.is_dev():
            errmsg = f"数据库错误：{str(exc)}"
        else:
            errmsg = f"数据库操作失败，请联系管理员"
        return JSONResponse(
            status_code=200,
            content=ResponseModel(
                status=500,
                errmsg= errmsg,
                data=None
            ).model_dump()
        )
    errmsg = f"系统错误：{str(exc)}"
    return JSONResponse(
        status_code=200,
        content=ResponseModel(
            status=500,
            errmsg=errmsg,
            data=None
        ).model_dump()
    )