from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.responses import JSONResponse

from api.schemas.common import ResponseModel


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
    return JSONResponse(
        status_code=200,
        content=ResponseModel(
            status=500,
            errmsg=str(exc),
            data=None
        ).model_dump()
    )