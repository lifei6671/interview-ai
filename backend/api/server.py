from fastapi import FastAPI
from api.routers import interview, health,auth,llm,skills,role
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)


def create_app() -> FastAPI:
    app = FastAPI(title="JD Interview Generator API")

    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception,global_exception_handler)

    app.include_router(health.router, prefix="/api")
    app.include_router(interview.router, prefix="/api")

    app.include_router(auth.router, prefix="/api")

    app.include_router(llm.router, prefix="/api")

    app.include_router(skills.router, prefix="/api")

    app.include_router(role.router, prefix="/api")

    return app


app = create_app()
