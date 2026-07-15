from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exception_handlers import register_exception_handlers
from app.api.middleware.rate_limit import BarrierRateLimitMiddleware
from app.api.middleware.request_id import RequestIdMiddleware
from app.api.openapi import OPENAPI_TAGS
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()

    application = FastAPI(
        title=settings.app_name,
        summary="Parking application management API",
        description=("REST API for managing parking space applications in the Euro PArk residential community"),
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        openapi_tags=OPENAPI_TAGS,
        swagger_ui_parameters={
            "persistAuthorization": True,
        },
        contact={
            "name": "Euro Park API",
        },
    )
    application.add_middleware(
        BarrierRateLimitMiddleware,
        enabled=settings.rate_limit_enabled,
        path=(f"{settings.api_v1_prefix}" "/barrier/check-access"),
        limit=settings.barrier_rate_limit_requests,
        window_seconds=(settings.barrier_rate_limit_window_seconds),
    )
    application.add_middleware(
        RequestIdMiddleware,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(application)

    application.include_router(api_router, prefix=settings.api_v1_prefix)

    return application


app = create_app()
