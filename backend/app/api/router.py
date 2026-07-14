from fastapi import APIRouter

from app.api.routes.applications import router as applications_router
from app.api.routes.auth import router as auth_router
from app.api.routes.barrier import router as barrier_router
from app.api.routes.health import router as health_router
from app.api.routes.supervisor import router as supervisor_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(applications_router)
api_router.include_router(supervisor_router)
api_router.include_router(barrier_router)
