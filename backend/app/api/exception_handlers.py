import logging

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("app.errors")


def register_exception_handlers(
    app: FastAPI,
) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        request_id = getattr(
            request.state,
            "request_id",
            None,
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "detail": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed.",
                    "errors": jsonable_encoder(exc.errors()),
                    "request_id": request_id,
                }
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request,
        exc: SQLAlchemyError,
    ) -> JSONResponse:
        request_id = getattr(
            request.state,
            "request_id",
            None,
        )
        logger.exception(
            "Database error request_id=%s",
            request_id,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": {
                    "code": "DATABASE_ERROR",
                    "message": "Database operation failed.",
                    "request_id": request_id,
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        request_id = getattr(
            request.state,
            "request_id",
            None,
        )
        logger.exception(
            "Unhandled error request_id=%s",
            request_id,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Unexpected server error.",
                    "request_id": request_id,
                }
            },
        )
