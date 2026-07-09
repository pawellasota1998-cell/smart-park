from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings

def create_app() -> FastAPI:

    application = FastAPI(
        title=settings.app_name,
        summary="Parking application management API",
        description=(
            "REST API for managing parking space applications "
            "in the Euro PArk residential community"
        ),
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    application.include_router(api_router, prefix=settings.api_v1_prefix)

    return application


app = create_app()
