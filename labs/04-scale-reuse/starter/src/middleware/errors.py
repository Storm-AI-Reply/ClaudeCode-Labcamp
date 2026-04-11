from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.errors import AppError
from src.utils import format_error


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=format_error(exc.message, exc.status_code),
        )
