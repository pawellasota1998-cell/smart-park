from fastapi import FastAPI

from app.api.router import api_router


def create_app() -> FastAPI:

    application = FastAPI(
        title="Eko Park API",
        summary="Parking application management API",
        description=(
            "REST API for managing parking space applications "
            "in the Euro PArk residential community"
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    application.include_router(api_router, prefix="/api/v1")

    return application


app = create_app()
